#!/usr/bin/env python3
"""V2 voice generation: directed, segment-level synthesis with human pause statistics.

Pipeline per chapter (both voice sets share the same direction):
  1. VOICE_DIRECTION_V2.md → segments (text + emotion/speed/pitch/expressiveness + pause class).
  2. Each segment is synthesised on its own with the backend's control syntax
     (Higgs TTS 3 inline tokens, or Fish S2 Pro free-form tags), same reference every time.
  3. Optional ASR check (faster-whisper): a segment whose transcript drifts from its text is
     regenerated with a new seed (up to --retries).
  4. Leading/trailing silence is trimmed; pauses are re-inserted from log-normal fits of the
     user's measured pause distributions (voice_ref/user_prosody_stats.json), filled with a
     very low room tone instead of digital silence.
  5. Chapter → -16 LUFS MP3 in audio_v2_<voice>/SceneNN.mp3 + segment timing JSON.

Voices:
  cloned   — reference voice_ref/user_ref_22s.wav (+ exact transcript).
  standard — the model's own built-in voice (no human reference); the first generated segment
             of chapter 1 becomes the reference for every later segment so the timbre is fixed.

Run on the server, GPU 1 only:
  CUDA_VISIBLE_DEVICES=1 python m3b/voice/generate_v2.py --backend higgs --voice cloned --chapters all
"""
import argparse, base64, difflib, io, json, os, re, subprocess, sys, time
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from direction import direction_chapters  # noqa: E402

REF_WAV = os.path.join(SA, "voice_ref", "user_ref_22s.wav")
REF_TXT = open(os.path.join(SA, "voice_ref", "user_ref_22s.txt")).read().strip()
STATS = json.load(open(os.path.join(SA, "voice_ref", "user_prosody_stats.json")))
SR = 24000
CALIBRATION = ("Every great idea in science begins as a question. Some questions take a lifetime to answer, "
               "and some of them, quietly, change the way we see everything around us.")

HIGGS_SPEED = {"vs": "<|prosody:speed_very_slow|>", "s": "<|prosody:speed_slow|>", "f": "<|prosody:speed_fast|>"}
HIGGS_PITCH = {"lo": "<|prosody:pitch_low|>", "hi": "<|prosody:pitch_high|>"}
HIGGS_EXPR = {"hi": "<|prosody:expressive_high|>", "lo": "<|prosody:expressive_low|>"}
FISH_SPEED = {"vs": "speaking very slowly", "s": "speaking slowly", "f": "speaking a little faster"}
FISH_PITCH = {"lo": "in a lower, deeper pitch", "hi": "with a slightly raised pitch"}
FISH_EXPR = {"hi": "with strong emphasis", "lo": "softly, understated"}
FISH_EMO = {"contemplation": "thoughtful", "awe": "in awe", "enthusiasm": "enthusiastic", "determination": "determined",
            "surprise": "surprised", "confusion": "puzzled", "amusement": "amused", "bitterness": "wry and bitter",
            "sadness": "sad", "relief": "relieved", "pride": "proud", "longing": "wistful", "contentment": "warm",
            "fear": "uneasy", "helplessness": "resigned", "elation": "delighted"}


# ── prompt construction ──────────────────────────────────────────────────────────────
def higgs_text(seg):
    t = ""
    if seg.get("e"):
        t += f"<|emotion:{seg['e']}|>"
    t += HIGGS_SPEED.get(seg.get("s"), "") + HIGGS_PITCH.get(seg.get("p"), "") + HIGGS_EXPR.get(seg.get("x"), "")
    body = seg["text"]
    if seg.get("nv") == "laugh":
        body = "<|sfx:laughter|>Heh. " + body
    elif seg.get("nv") == "sigh":
        body = "<|sfx:sigh|>Hhh. " + body
    return t + body


def fish_text(seg):
    parts = [FISH_EMO[seg["e"]]] if seg.get("e") else []
    parts += [FISH_SPEED[seg["s"]]] if seg.get("s") else []
    parts += [FISH_PITCH[seg["p"]]] if seg.get("p") else []
    parts += [FISH_EXPR[seg["x"]]] if seg.get("x") else []
    nv = {"breath": "[inhale] ", "sigh": "[sigh] ", "laugh": "[chuckle] "}.get(seg.get("nv"), "")
    return nv + (f"[{', '.join(parts)}] " if parts else "") + seg["text"]


# ── backends ─────────────────────────────────────────────────────────────────────────
class Higgs:
    def __init__(self, url, model):
        import requests
        self.rq, self.url, self.model = requests, url.rstrip("/") + "/v1/audio/speech", model

    def synth(self, seg, ref_wav, ref_text, seed, temperature=0.8, voice="default"):
        body = dict(model=self.model, input=higgs_text(seg), response_format="wav", temperature=temperature,
                    top_k=50, top_p=0.95, max_new_tokens=1024, seed=seed)
        if ref_wav:
            data = base64.b64encode(open(ref_wav, "rb").read()).decode()
            body["references"] = [dict(audio_path=f"data:audio/wav;base64,{data}", text=ref_text)]
        else:
            body["voice"] = voice
        r = self.rq.post(self.url, json=body, timeout=600)
        r.raise_for_status()
        y, sr = sf.read(io.BytesIO(r.content), dtype="float32")
        return to_sr(y, sr)


class Fish:
    def __init__(self, engine_dir, ckpt):
        import torch
        sys.path.insert(0, engine_dir)
        from fish_speech.models.text2semantic.inference import init_model, load_codec_model, encode_audio, decode_to_audio, generate_long
        self.torch, self.encode_audio, self.decode, self.gen = torch, encode_audio, decode_to_audio, generate_long
        self.model, self.dot = init_model(ckpt, "cuda:0", torch.bfloat16, compile=False)
        self.model.config.max_seq_len = 3072
        with torch.device("cuda:0"):
            self.model.setup_caches(max_batch_size=1, max_seq_len=3072, dtype=next(self.model.parameters()).dtype)
        self.model._cache_setup_done = True
        self.codec = load_codec_model(os.path.join(ckpt, "codec.pth"), "cpu", torch.float32)
        self._ref_cache = {}

    def synth(self, seg, ref_wav, ref_text, seed, temperature=0.75, voice=None):
        torch = self.torch
        torch.manual_seed(seed)
        pt = None
        if ref_wav:
            if ref_wav not in self._ref_cache:
                self._ref_cache[ref_wav] = self.encode_audio(ref_wav, self.codec, "cpu").cpu()
            pt = self._ref_cache[ref_wav]
        codes = []
        for resp in self.gen(model=self.model, device="cuda:0", decode_one_token=self.dot, text=fish_text(seg), num_samples=1,
                             max_new_tokens=1024, top_p=0.85, top_k=40, temperature=temperature, compile=False,
                             iterative_prompt=True, chunk_length=300, prompt_text=[ref_text] if pt is not None else None,
                             prompt_tokens=[pt] if pt is not None else None):
            if resp.action == "sample":
                codes.append(resp.codes)
        y = self.decode(torch.cat(codes, dim=1).to("cpu"), self.codec).cpu().float().numpy().reshape(-1)
        torch.cuda.empty_cache()
        return to_sr(y, self.codec.sample_rate)


# ── audio utilities ──────────────────────────────────────────────────────────────────
def to_sr(y, sr):
    if y.ndim > 1:
        y = y.mean(1)
    if sr == SR:
        return y.astype(np.float32)
    n = int(len(y) * SR / sr)
    return np.interp(np.linspace(0, len(y) - 1, n), np.arange(len(y)), y).astype(np.float32)


def trim(y, thr_db=-42, keep=0.04):
    win = int(0.02 * SR)
    e = np.sqrt(np.convolve(y ** 2, np.ones(win) / win, mode="same") + 1e-12)
    on = np.nonzero(20 * np.log10(e / (e.max() + 1e-9)) > thr_db)[0]
    if len(on) == 0:
        return y
    a, b = max(0, on[0] - int(keep * SR)), min(len(y), on[-1] + int(keep * SR))
    return y[a:b]


def lognorm(rng, median, p90, lo, hi):
    sigma = np.log(p90 / median) / 1.2816
    return float(np.clip(median * np.exp(sigma * rng.normal()), lo, hi))


def pause_seconds(rng, cls):
    c, s = STATS["comma_pause_ms"], STATS["sentence_pause_ms"]
    if cls == 0:
        return float(rng.uniform(0.05, 0.14))
    if cls == 1:
        return lognorm(rng, c["median"] / 1000, c["p90"] / 1000, 0.09, 0.62)
    if cls == 2:
        return lognorm(rng, max(0.34, s["median"] / 1000), 1.05, 0.22, 1.25)
    return float(np.clip(rng.lognormal(np.log(1.0), 0.25), 0.7, 1.6))


def room_tone(rng, seconds, level_db=-62):
    n = int(seconds * SR)
    w = rng.normal(size=n)
    pink = np.cumsum(w); pink -= np.convolve(pink, np.ones(400) / 400, mode="same")
    pink /= (np.abs(pink).max() + 1e-9)
    return (pink * 10 ** (level_db / 20)).astype(np.float32)


def fade(y, ms=12):
    n = min(len(y) // 2, int(ms / 1000 * SR))
    if n > 0:
        y = y.copy(); r = np.linspace(0, 1, n)
        y[:n] *= r; y[-n:] *= r[::-1]
    return y


# ── ASR check ────────────────────────────────────────────────────────────────────────
class Checker:
    def __init__(self):
        try:
            from faster_whisper import WhisperModel
            self.m = WhisperModel("small.en", device="cpu", compute_type="int8")
        except Exception as e:  # noqa: BLE001
            print("[asr] disabled:", e); self.m = None

    def score(self, y, text):
        if self.m is None:
            return 1.0
        segs, _ = self.m.transcribe(y, language="en", beam_size=1)
        hyp = " ".join(s.text for s in segs)
        n = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " "))
        return difflib.SequenceMatcher(None, n(hyp).split(), n(text).split()).ratio()


def plausible(y, text):
    secs = len(y) / SR
    wps = len(text.split()) / max(secs, 1e-3)
    return 0.9 <= wps <= 5.2


# ── main ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["higgs", "fish"], required=True)
    ap.add_argument("--voice", choices=["cloned", "standard"], required=True)
    ap.add_argument("--chapters", default="all")
    ap.add_argument("--url", default="http://localhost:8000")
    ap.add_argument("--model", default="bosonai/higgs-audio-v3-tts-4b")
    ap.add_argument("--fish-engine", default="/home/user/Desktop/Deep_learning_projects/youtube/youtube_videos/fish_speech_engine")
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--min-asr", type=float, default=0.86)
    ap.add_argument("--std-voice", default="default", help="backend preset for the standard (non-cloned) voice")
    ap.add_argument("--std-seed", type=int, default=7, help="seed for the standard-voice calibration passage")
    args = ap.parse_args()

    D = direction_chapters()
    chs = sorted(D) if args.chapters == "all" else [int(c) for c in args.chapters.split(",")]
    be = Higgs(args.url, args.model) if args.backend == "higgs" else Fish(args.fish_engine, os.path.join(args.fish_engine, "checkpoints", "s2-pro"))
    asr = Checker()
    out_dir = os.path.join(SA, f"audio_v2_{args.voice}"); os.makedirs(out_dir, exist_ok=True)
    work = os.path.join(out_dir, "_segments"); os.makedirs(work, exist_ok=True)

    ref_wav, ref_text = (REF_WAV, REF_TXT) if args.voice == "cloned" else (None, None)
    std_ref = os.path.join(out_dir, "standard_voice_ref.wav")
    if args.voice == "standard":
        # Freeze the model's own built-in voice once: synthesise a neutral calibration passage with
        # the preset, then use it as the fixed reference so timbre never drifts between segments.
        if not os.path.exists(std_ref):
            # pitch_low deepens the model's own default voice (~-3 semitones) without cloning anyone
            cal = dict(text=CALIBRATION, e="contemplation", p="lo", s="s")
            y = trim(be.synth(cal, None, None, seed=args.std_seed, voice=args.std_voice))
            sf.write(std_ref, y, SR); open(std_ref + ".txt", "w").write(CALIBRATION)
        ref_wav, ref_text = std_ref, open(std_ref + ".txt").read()

    for ch in chs:
        rng = np.random.default_rng(1000 + ch)
        pieces, timing, t = [room_tone(rng, 0.35)], [], 0.35
        t0 = time.time()
        for i, seg in enumerate(D[ch]):
            cache = os.path.join(work, f"ch{ch:02d}_{i:03d}.wav")
            if os.path.exists(cache):
                y = sf.read(cache, dtype="float32")[0]
            else:
                best, best_s = None, -1
                for k in range(args.retries):
                    y = trim(be.synth(seg, ref_wav, ref_text, seed=ch * 1000 + i * 10 + k))
                    s = asr.score(y, seg["text"]) if plausible(y, seg["text"]) else 0.0
                    if s > best_s:
                        best, best_s = y, s
                    if s >= args.min_asr:
                        break
                    print(f"  ch{ch:02d} seg{i:03d} retry {k + 1} (asr {s:.2f})")
                y = best
                sf.write(cache, y, SR)
            pieces.append(fade(y))
            timing.append(dict(i=i, s=round(t, 3), e=round(t + len(y) / SR, 3), text=seg["text"]))
            t += len(y) / SR
            gap = pause_seconds(rng, seg["pause"]) if i < len(D[ch]) - 1 else 0.8
            pieces.append(room_tone(rng, gap)); t += gap
        wav = os.path.join(work, f"Scene{ch:02d}.wav")
        sf.write(wav, np.concatenate(pieces), SR)
        mp3 = os.path.join(out_dir, f"Scene{ch:02d}.mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000",
                        "-ac", "2", "-c:a", "libmp3lame", "-b:a", "192k", mp3], check=True)
        json.dump(dict(chapter=ch, voice=args.voice, backend=args.backend, segments=timing),
                  open(os.path.join(out_dir, f"Scene{ch:02d}_segments.json"), "w"), indent=1)
        print(f"[done] {args.voice} ch{ch:02d}: {t / 60:.2f} min audio in {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()
