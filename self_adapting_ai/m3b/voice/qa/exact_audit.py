"""Exact per-phrase audit: cut each phrase from the lossless FLAC (generator timeline) and transcribe it alone."""
import sys, os, json, re, difflib, numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from faster_whisper import WhisperModel
from generate_v3 import norm
SA = "/Users/samreedhbhuyan/Desktop/Win_C/youtube_videos/self_adapting_ai"
m = WhisperModel("small.en", device="cpu", compute_type="int8")
out = []
for voice in sys.argv[1:]:
    for ch in range(1, 13):
        y, sr = sf.read(f"{SA}/audio_v3_{voice}/Scene{ch:02d}.flac", dtype="float32")
        for sg in json.load(open(f"{SA}/audio_v3_{voice}/Scene{ch:02d}_segments.json"))["segments"]:
            a, b = max(0, int((sg["s"] - 0.12) * sr)), min(len(y), int((sg["e"] + 0.12) * sr))
            segs, _ = m.transcribe(y[a:b], language="en", beam_size=5)
            got = " ".join(s.text for s in segs)
            r = difflib.SequenceMatcher(None, norm(got), norm(sg["text"])).ratio()
            if r < 0.72:
                out.append(dict(voice=voice, ch=ch, i=sg["i"], r=round(r, 2), text=sg["text"], heard=got.strip()))
        print(voice, ch, "done", flush=True)
json.dump(out, open(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/../timing/exact_audit_{'_'.join(sys.argv[1:])}.json", "w"), indent=1)
print("flagged", len(out))
