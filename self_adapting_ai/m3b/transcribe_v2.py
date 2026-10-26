"""Word timings for the V2 voice sets + per-segment fidelity audit."""
import json, os, re, difflib
from faster_whisper import WhisperModel
ROOT = os.path.dirname(os.path.abspath(__file__)); SA = os.path.dirname(ROOT)
m = WhisperModel("small.en", device="cpu", compute_type="int8")
n = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).split()
audit = []
for voice in ("cloned", "standard"):
    for ch in range(1, 13):
        out = os.path.join(ROOT, "timing", f"v2{voice}_ch{ch:02d}.json")
        mp3 = os.path.join(SA, f"audio_v2_{voice}", f"Scene{ch:02d}.mp3")
        if not os.path.exists(out):
            segs, info = m.transcribe(mp3, word_timestamps=True, beam_size=5, vad_filter=False)
            words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
            json.dump({"duration": info.duration, "words": words}, open(out, "w"), indent=0)
        words = json.load(open(out))["words"]
        segj = json.load(open(os.path.join(SA, f"audio_v2_{voice}", f"Scene{ch:02d}_segments.json")))["segments"]
        for sg in segj:
            got = " ".join(w["w"] for w in words if w["s"] >= sg["s"] - 0.15 and w["e"] <= sg["e"] + 0.25)
            r = difflib.SequenceMatcher(None, n(got), n(sg["text"])).ratio()
            if r < 0.7:
                audit.append(dict(voice=voice, ch=ch, i=sg["i"], r=round(r, 2), text=sg["text"], heard=got))
        print(voice, ch, "done", flush=True)
json.dump(audit, open(os.path.join(ROOT, "timing", "v2_audit.json"), "w"), indent=1)
print("flagged", len(audit))
