"""Master the ElevenLabs takes into audio_final_best/ and write word timings.  usage: prepare_best.py 1 2 3 [--take 2]"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); SA = os.path.dirname(ROOT)
RAW = f"{SA}/audio_elevenlabs_v4/raw"; DST = f"{SA}/audio_final_best"; os.makedirs(DST, exist_ok=True)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
take = int(sys.argv[sys.argv.index("--take") + 1]) if "--take" in sys.argv else 1
chs = [int(a) for a in args if a != str(take) or "--take" not in sys.argv] if args else range(1, 13)
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
for ch in chs:
    src = f"{SA}/audio_elevenlabs_v4/chapters/ch{ch:02d}.mp3"; dst = f"{DST}/Scene{ch:02d}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "1", "-b:a", "192k", dst], check=True)
    out = f"{ROOT}/timing/v3best_ch{ch:02d}.json"
    segs, info = m.transcribe(dst, word_timestamps=True, beam_size=5, vad_filter=False)
    words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
    json.dump({"duration": info.duration, "words": words}, open(out, "w"), indent=0)
    print(f"ch{ch:02d}: {info.duration:.1f}s, {len(words)} words", flush=True)
