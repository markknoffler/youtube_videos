import sys, os, json, difflib, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from faster_whisper import WhisperModel
from generate_v3 import norm
SA = "/Users/samreedhbhuyan/Desktop/Win_C/youtube_videos/self_adapting_ai"
voice = sys.argv[1]; items = [tuple(map(int, x.split(":"))) for x in sys.argv[2:]]
m = WhisperModel("small.en", device="cpu", compute_type="int8")
for ch, i in items:
    y, sr = sf.read(f"{SA}/audio_v3_{voice}/Scene{ch:02d}.flac", dtype="float32")
    sg = json.load(open(f"{SA}/audio_v3_{voice}/Scene{ch:02d}_segments.json"))["segments"][i]
    a, b = max(0, int((sg["s"] - 0.12) * sr)), min(len(y), int((sg["e"] + 0.12) * sr))
    segs, _ = m.transcribe(y[a:b], language="en", beam_size=5)
    got = " ".join(s.text for s in segs).strip()
    r = difflib.SequenceMatcher(None, norm(got), norm(sg["text"])).ratio()
    print(f"ch{ch:02d}#{i:03d} {'WEAK ' if sg.get('weak') else 'ok   '} r={r:.2f} dur={sg['dur']:.1f} st={sg.get('st', 0):+.1f} sim={sg['sim']:.2f} | want: {sg['text'][:45]} | heard: {got[:50]}")
