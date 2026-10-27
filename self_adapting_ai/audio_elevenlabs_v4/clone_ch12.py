#!/usr/bin/env python3
"""Generate ch12 (the only chapter ElevenLabs narration is missing) by cloning the real
"Chuck Miller" voice from chapters 1-11 via the locally-hosted Higgs Audio v3.

Reference: 3 clips of different energy, extracted from ch03.mp3 (see build_ref_clips.py),
all three passed in the `references` list so the clone draws on the voice's full range
rather than one static reading. Text is split sentence-by-sentence, exactly as in
VOICEOVER_SCRIPT_V2.md ch12 (word-for-word - ElevenLabs's own [tag] markers are mapped to
Higgs emotion control-tokens, never spoken literally, per tagged/ch12.txt + make_tagged.py's
TAGS[12] cue map).

No pitch/range gating (V2/V3's gates made the voice sleepy - this is a different, much more
expressive target). Multiple takes per sentence, scored by ASR word-match + proximity to the
ElevenLabs prosody measured on ch03.mp3 (wps ~2.2, pitch SD ~5-5.6 st, p5-p95 range ~17-19 st);
only takes that are FAR off those numbers are rejected outright, the rest are ranked and the
best kept.
"""
import argparse, base64, difflib, json, os, re, sys, time
import numpy as np
import soundfile as sf
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.path.join(os.path.dirname(HERE), "m3b", "voice")
sys.path.insert(0, VOICE)
import generate_v2 as g2  # noqa: E402  (trim, fade, to_sr, SR)

SR = g2.SR
V4 = HERE
REF_DIR = os.path.join(V4, "clone_ref")
URL = "http://localhost:8711/v1/audio/speech"
MODEL = "bosonai/higgs-audio-v3-tts-4b"

# ElevenLabs [tag] -> Higgs emotion control-token. "curious"/"excited" have no exact Higgs
# equivalent; "contemplation"/"enthusiasm" are the closest without the extreme pitch-shift risk
# measured on "elation"/"surprise" in the V2 audit. "serious" -> "determination" (firm, grave).
TAG_MAP = {"curious": "contemplation", "excited": "enthusiasm", "serious": "determination"}

SENTENCES = [
    (1, "Where does this leave the grand frontier of self-adapting artificial intelligence over the next decade?", "curious"),
    (2, "The future of intelligence will not be a regression to biological chaos, nor will it be an indefinite continuation of brute-force frozen weights.", None),
    (3, "The true frontier is the profound unification of global bilinear attention with continuous, localized structural plasticity.", "excited"),
    (4, "Over the next ten years, this revolution will unfold across four pioneering technical pillars.", None),
    (5, "First, Neuromorphic and Analog Hardware: next-generation silicon, like Intel Loihi 2 and memristor crossbar arrays, designed from the physical layer up to execute continuous local plasticity without memory thrashing or von Neumann bottlenecks.", "excited"),
    (6, "Second, Fast-Weights and Test-Time Training: pioneering frameworks like TTT, where neural weights dynamically update during inference using localized meta-gradients, bridging the gap between static weights and episodic memory.", None),
    (7, "Third, Liquid State Networks and Neural ODEs: continuous-time dynamical systems whose internal time constants adapt to unpredictable real-time streaming environments without losing stability.", None),
    (8, "And fourth, Self-Compiling Cognitive Graphs: autonomous agentic systems that continuously inspect and rewrite their own high-level computational graphs at runtime based on task performance.", None),
    (9, "As hardware designers create native support for asynchronous sparsity, and algorithmic theorists solve credit assignment in continuous dynamical systems, the boundary between static silicon and living intelligence will finally dissolve.", "excited"),
    (10, "The monolith of modern artificial intelligence has carried humanity to the threshold of superhuman reasoning.", None),
    (11, "Yet the artificial minds of tomorrow will not be frozen statues etched in silicon stone.", "serious"),
    (12, "They will be living, breathing, self-adapting cognitive architectures.", None),
    (13, "Thank you for joining this technical masterclass.", "excited"),
    (14, "All mathematical proofs, experimental source code, benchmark data, and research papers are indexed in the description below.", None),
]

TARGET = dict(wps_lo=1.8, wps_hi=2.5, pitch_sd_lo=3.5, pitch_sd_hi=7.0, range_lo=12.0, range_hi=24.0)
# "far below" reject thresholds - generous; we removed the old gates on purpose
REJECT = dict(asr_min=0.70, pitch_sd_min=2.5, wps_min=1.2, wps_max=3.2)

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def n2w(n):
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
    return str(n)


def norm(s):
    s = re.sub(r"\b(\d+)\b", lambda m: n2w(int(m[1])), s)
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).split()


def load_references():
    refs = []
    for name in ("calm", "excited", "serious"):
        wav, txt = f"{REF_DIR}/chuck_{name}.wav", f"{REF_DIR}/chuck_{name}.txt"
        data = base64.b64encode(open(wav, "rb").read()).decode()
        text = open(txt).read().strip()
        refs.append(dict(audio_path=f"data:audio/wav;base64,{data}", text=text))
    return refs


def higgs_text(sentence, tag):
    return (f"<|emotion:{TAG_MAP[tag]}|>" if tag else "") + sentence


def synth(refs, sentence, tag, seed, temperature=0.85):
    body = dict(model=MODEL, input=higgs_text(sentence, tag), response_format="wav", temperature=temperature,
                top_k=50, top_p=0.95, max_new_tokens=1024, seed=seed, references=refs)
    r = requests.post(URL, json=body, timeout=600)
    r.raise_for_status()
    y, sr = sf.read(__import__("io").BytesIO(r.content), dtype="float32")
    return g2.to_sr(y, sr)


def pitch_stats(y):
    import parselmouth
    snd = parselmouth.Sound(y.astype(np.float64), SR)
    f0 = snd.to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=350, voicing_threshold=0.5).selected_array["frequency"]
    f0 = f0[f0 > 0]
    if len(f0) < 8:
        return None
    st = 12 * np.log2(f0 / np.median(f0))
    return dict(pitch_sd=float(st.std()), range=float(np.percentile(st, 95) - np.percentile(st, 5)))


def asr_match(asr, y, text):
    segs, _ = asr.transcribe(y, language="en", beam_size=1)
    hyp = " ".join(s.text for s in segs)
    return difflib.SequenceMatcher(None, norm(hyp), norm(text)).ratio()


def score_take(asr, y, text):
    dur = len(y) / SR
    nwords = len(text.split())
    wps = nwords / dur if dur > 0 else 0
    asr_r = asr_match(asr, y, text)
    ps = pitch_stats(y)
    reject = asr_r < REJECT["asr_min"] or wps < REJECT["wps_min"] or wps > REJECT["wps_max"] or (ps and ps["pitch_sd"] < REJECT["pitch_sd_min"])
    score = asr_r * 2.0
    if ps:
        score -= 0.04 * max(0, abs(ps["pitch_sd"] - 5.2) - 1.0)
        score -= 0.03 * max(0, abs(ps["range"] - 17.5) - 3.0)
    score -= 0.15 * max(0, abs(wps - 2.1) - 0.3)
    meta = dict(dur=round(dur, 2), wps=round(wps, 2), asr=round(asr_r, 3),
                pitch_sd=round(ps["pitch_sd"], 2) if ps else None, range=round(ps["range"], 1) if ps else None)
    return (not reject), score, meta


def gen_sentence(refs, asr, idx, text, tag, attempts, seed_offset, log):
    best = (-9, None, None)
    for k in range(attempts):
        seed = seed_offset + idx * 100 + k
        temp = 0.85 if k < 3 else 0.75
        y = g2.trim(synth(refs, text, tag, seed, temp))
        ok, score, meta = score_take(asr, y, text)
        if score > best[0]:
            best = (score, y, dict(meta, attempt=k + 1, ok=ok))
        tag_s = f" [{tag}]" if tag else ""
        print(f"  seg{idx:02d}{tag_s} attempt {k + 1}: {meta} {'OK' if ok else 'reject'}", file=log, flush=True)
        if ok and score > 1.5:
            break
    return best[1], best[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="only sentences 1-2 (~20s), for a quick sanity check")
    ap.add_argument("--attempts", type=int, default=5)
    ap.add_argument("--seed-offset", type=int, default=11000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    refs = load_references()
    from faster_whisper import WhisperModel
    asr = WhisperModel("small.en", device="cpu", compute_type="int8")

    sentences = SENTENCES[:2] if args.test else SENTENCES
    out = args.out or (f"{V4}/ch12_test.wav" if args.test else f"{V4}/chapters/ch12.wav")

    pieces, metas, t0 = [np.zeros(int(0.35 * SR), np.float32)], [], time.time()
    for idx, text, tag in sentences:
        y, meta = gen_sentence(refs, asr, idx, text, tag, args.attempts, args.seed_offset, sys.stdout)
        pieces.append(g2.fade(y))
        pieces.append(np.zeros(int(0.35 * SR), np.float32))
        metas.append(dict(i=idx, text=text, tag=tag, **meta))
        print(f"[seg{idx:02d}] done: {meta}", flush=True)

    wav = np.concatenate(pieces)
    wav = wav / max(1e-6, np.abs(wav).max()) * 0.89
    sf.write(out, wav, SR)
    dur = len(wav) / SR
    overall = pitch_stats(wav) or {}
    full_text = " ".join(t for _, t, _ in sentences)
    full_asr = asr_match(asr, wav, full_text)
    print(f"[ch12{'_test' if args.test else ''}] FINISHED dur={dur:.1f}s wall={(time.time() - t0) / 60:.1f}min "
          f"asr={full_asr:.3f} pitch_sd={overall.get('pitch_sd')} range={overall.get('range')} -> {out}", flush=True)
    json.dump(dict(segments=metas, dur=round(dur, 1), asr=round(full_asr, 3), pitch_sd=overall.get("pitch_sd"), range=overall.get("range")),
              open(out.replace(".wav", "_segments.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
