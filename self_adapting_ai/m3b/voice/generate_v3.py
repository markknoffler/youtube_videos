#!/usr/bin/env python3
"""V3 voice generation — gated, identity-stable, lossless.

What changed from V2 (and why):
  * No pitch tags, and emotion tags that raised pitch by 4–15 semitones are mapped to neutral
    ones. Measured on V2: `pitch_high` moved the standard voice +8.5 st (a female register);
    confusion/elation/surprise moved it +10…+15 st. Identity collapses past ~3 st.
  * Every phrase is gated before it is accepted: ASR text match, median-pitch drift ≤ 2.2 st
    from the voice's target, pitch range ≤ 10 st, and ECAPA speaker similarity ≥ threshold.
    Failed phrases are regenerated (different seed, cooler sampling, then fewer tags).
  * Cached phrases from earlier runs are re-gated and replaced if they fail.
  * Output is lossless FLAC with digital silence in the gaps; denoising/mastering happens
    afterwards in m3b/voice/postprocess.py, uniformly over the whole chapter (no per-phrase noise).

Needs the gate server running (see qa_gate_server.py), the Higgs server (or Fish), and
faster-whisper (CPU) for the ASR check.
"""
import argparse, json, os, re, sys, time
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generate_v2 as g2                                   # backends + audio helpers
from direction import direction_chapters

SA, SR = g2.SA, g2.SR
# emotions that pulled the voice's pitch far from its median in V2 → calmer equivalents
EMOTION_MAP = {"confusion": "contemplation", "surprise": "awe", "elation": "contentment", "amusement": "contentment",
               "enthusiasm": "awe", "determination": "pride", "sadness": "longing", "arousal": None, "anger": None}
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def n2w(n):
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
    if n < 1000: return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + n2w(n % 100))
    if n < 10000: return n2w(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + n2w(n % 1000))
    return str(n)


def spoken(s):
    """ASR hypotheses write numbers as digits; compare in words."""
    s = re.sub(r"(\d+)\s*\.\s*(\d+)", lambda m: n2w(int(m[1])) + " point " + " ".join(ONES[int(c)] for c in m[2]), s)
    s = s.replace("%", " percent")
    return re.sub(r"\d+", lambda m: n2w(int(m[0])), s)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", spoken(s).lower().replace("-", " ")).split()


def asr_score(asr, y, text):
    if asr is None:
        return 1.0
    segs, _ = asr.transcribe(y, language="en", beam_size=1)
    import difflib
    return difflib.SequenceMatcher(None, norm(" ".join(s.text for s in segs)), norm(text)).ratio()


def level_seg(seg, level):
    """level 0: mapped emotion + speed + expressiveness; 1: no emotion; 2: speed only; 3: plain."""
    s = dict(seg); s.pop("p", None)
    if s.get("e") in EMOTION_MAP:
        s["e"] = EMOTION_MAP[s["e"]]
        if s["e"] is None: s.pop("e")
    if level >= 1: s.pop("e", None)
    if level >= 2: s.pop("x", None)
    if level >= 3: s.pop("s", None); s["nv"] = None
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["higgs", "fish"], default="higgs")
    ap.add_argument("--voice", choices=["cloned", "standard"], required=True)
    ap.add_argument("--chapters", default="all")
    ap.add_argument("--url", default="http://localhost:8000")
    ap.add_argument("--model", default="bosonai/higgs-audio-v3-tts-4b")
    ap.add_argument("--gate", default="http://127.0.0.1:8765")
    ap.add_argument("--ref-wav"); ap.add_argument("--ref-text-file")
    ap.add_argument("--cache", help="segment cache dir (can point at an older run to re-gate and reuse it)")
    ap.add_argument("--out", help="output dir (default audio_v3_<voice>)")
    ap.add_argument("--attempts", type=int, default=8)
    ap.add_argument("--max-st", type=float, default=2.2, help="max |median F0 drift| from the voice's target, semitones")
    ap.add_argument("--max-range", type=float, default=10.0, help="max p5–p95 F0 range inside one phrase, semitones")
    ap.add_argument("--min-sim", type=float, default=None, help="min ECAPA similarity (default 0.70 standard / 0.62 cloned)")
    ap.add_argument("--min-asr", type=float, default=0.70, help="ASR word-match floor (small.en mishears jargon, so not stricter)")
    ap.add_argument("--max-st-short", type=float, default=2.5, help="pitch-drift limit for phrases under 1.3 s")
    ap.add_argument("--seed-offset", type=int, default=0, help="shift all seeds so a re-run does NOT repeat earlier takes")
    ap.add_argument("--fish-engine", default="/home/user/Desktop/Deep_learning_projects/youtube/youtube_videos/fish_speech_engine")
    args = ap.parse_args()
    import requests
    min_sim = args.min_sim if args.min_sim is not None else (0.62 if args.voice == "cloned" else 0.70)

    D = direction_chapters()
    chs = sorted(D) if args.chapters == "all" else [int(c) for c in args.chapters.split(",")]
    be = g2.Higgs(args.url, args.model) if args.backend == "higgs" else g2.Fish(args.fish_engine, os.path.join(args.fish_engine, "checkpoints", "s2-pro"))
    try:
        from faster_whisper import WhisperModel
        asr = WhisperModel("small.en", device="cpu", compute_type="int8")
    except Exception as e:  # noqa: BLE001
        print("[asr] DISABLED:", e); asr = None

    out_dir = args.out or os.path.join(SA, f"audio_v3_{args.voice}"); os.makedirs(out_dir, exist_ok=True)
    work = args.cache or os.path.join(out_dir, "_segments"); os.makedirs(work, exist_ok=True)
    if args.ref_wav:
        ref_wav = args.ref_wav; ref_text = open(args.ref_text_file or args.ref_wav + ".txt").read().strip()
    elif args.voice == "cloned":
        ref_wav = os.path.join(SA, "voice_ref", "user_ref_clean.wav"); ref_text = open(os.path.join(SA, "voice_ref", "user_ref_clean.txt")).read().strip()
    else:
        sys.exit("standard voice needs --ref-wav (the frozen reference from the V2 run)")
    print(f"[v3] voice={args.voice} ref={ref_wav} gates: |st|<={args.max_st} range<={args.max_range} sim>={min_sim} asr>={args.min_asr}", flush=True)

    def gate(y, seg, tmp):
        sf.write(tmp, y, SR)
        r = requests.post(args.gate + "/score", json=dict(path=tmp, voice=args.voice), timeout=120).json()
        asr_s = asr_score(asr, y, seg["text"]) if g2.plausible(y, seg["text"]) else 0.0
        short = r["dur"] < 1.3                          # identity/range are unreliable on tiny clips, but PITCH still is checked
        if "st" not in r:                               # <80 ms voiced: nothing to measure
            ok, pen = asr_s >= args.min_asr, 0.0
        elif short:
            ok = asr_s >= args.min_asr and abs(r["st"]) <= args.max_st_short
            pen = 0.08 * max(0, abs(r["st"]) - 1.0)
        else:
            ok = asr_s >= args.min_asr and abs(r["st"]) <= args.max_st and r["range_st"] <= args.max_range and r["sim"] >= min_sim
            pen = 0.06 * max(0, abs(r["st"]) - 1.0) + 0.02 * max(0, r["range_st"] - 8) + max(0, min_sim - r["sim"])
        return ok, asr_s - pen + (0 if short or "st" not in r else r["sim"] * 0.5), dict(r, asr=round(asr_s, 3))

    tmp = os.path.join(work, "_gate_tmp.wav")
    stats = dict(total=0, reused=0, regen=0, weak=0, attempts=0)
    for ch in chs:
        rng = np.random.default_rng(1000 + ch)
        pieces, timing, t, t0 = [np.zeros(int(0.35 * SR), np.float32)], [], 0.35, time.time()
        for i, seg in enumerate(D[ch]):
            cache = os.path.join(work, f"ch{ch:02d}_{i:03d}.wav")
            meta, y = None, None
            if os.path.exists(cache):
                y0 = sf.read(cache, dtype="float32")[0]
                ok, _, m = gate(y0, seg, tmp)
                if ok: y, meta = y0, dict(m, attempts=0, reused=True); stats["reused"] += 1
                else: os.remove(cache)
            if y is None:
                best = (-9, None, None)
                for k in range(args.attempts):
                    level = 0 if k < 2 else 1 if k < 4 else 2 if k < 5 else 3
                    temp = 0.75 if k < 2 else 0.70 if k < 4 else 0.62
                    cand = g2.trim(be.synth(level_seg(seg, level), ref_wav, ref_text, seed=args.seed_offset + ch * 1000 + i * 10 + k, temperature=temp))
                    ok, score, m = gate(cand, seg, tmp); stats["attempts"] += 1
                    if score > best[0]: best = (score, cand, dict(m, attempts=k + 1, level=level))
                    if ok: break
                    print(f"  ch{ch:02d} seg{i:03d} attempt {k + 1} rejected: asr {m['asr']} st {m.get('st', 0):+.1f} range {m.get('range_st', 0):.1f} sim {m['sim']:.2f}", flush=True)
                else:
                    best[2]["weak"] = True; stats["weak"] += 1
                    print(f"  ch{ch:02d} seg{i:03d} WEAK after {args.attempts} attempts (best kept): {seg['text'][:50]}", flush=True)
                y, meta = best[1], best[2]; sf.write(cache, y, SR); stats["regen"] += 1
            stats["total"] += 1
            pieces.append(g2.fade(y))
            timing.append(dict(i=i, s=round(t, 3), e=round(t + len(y) / SR, 3), text=seg["text"], **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in meta.items()}))
            t += len(y) / SR
            gap = g2.pause_seconds(rng, seg["pause"]) if i < len(D[ch]) - 1 else 0.8
            pieces.append(np.zeros(int(gap * SR), np.float32)); t += gap
        wav = np.concatenate(pieces); wav = wav / max(1e-6, np.abs(wav).max()) * 0.89     # peak-normalise only; loudness is set in post
        sf.write(os.path.join(out_dir, f"Scene{ch:02d}.flac"), wav, SR, format="FLAC", subtype="PCM_16")
        json.dump(dict(chapter=ch, voice=args.voice, backend=args.backend, gates=dict(max_st=args.max_st, max_range=args.max_range, min_sim=min_sim), segments=timing),
                  open(os.path.join(out_dir, f"Scene{ch:02d}_segments.json"), "w"), indent=1)
        print(f"[done] {args.voice} ch{ch:02d}: {t / 60:.2f} min audio in {(time.time() - t0) / 60:.1f} min | running totals {stats}", flush=True)
    print("[v3] FINISHED", stats)


if __name__ == "__main__":
    main()
