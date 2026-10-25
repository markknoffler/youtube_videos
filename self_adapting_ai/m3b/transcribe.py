"""Word-level timestamps for every chapter of both voice sets (faster-whisper)."""
import json, sys, os
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = {"cloned": "audio_fish_s2_pro_cloned", "standard": "audio_fish_s2_pro_standard"}
model = WhisperModel("small.en", device="cpu", compute_type="int8")
for voice, d in SETS.items():
    for i in range(1, 11):
        out = os.path.join(ROOT, "m3b", "timing", f"{voice}_ch{i:02d}.json")
        if os.path.exists(out):
            continue
        segs, info = model.transcribe(os.path.join(ROOT, d, f"Scene{i:02d}.mp3"),
                                      word_timestamps=True, beam_size=5, vad_filter=False)
        words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)}
                 for s in segs for w in s.words]
        json.dump({"duration": info.duration, "words": words}, open(out, "w"), indent=0)
        print(voice, i, len(words), flush=True)
