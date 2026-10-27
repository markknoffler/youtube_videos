"""Transcribe the hand-downloaded ElevenLabs files and match each to a chapter/part prompt (audio_elevenlabs_v4/prompts)."""
import glob, json, os, re, difflib, subprocess, sys
from faster_whisper import WhisperModel
SA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = f"{SA}/audio_elevenlabs_v4"
files = sorted(glob.glob(f"{SA}/ElevenLabs_*.mp3") + glob.glob(os.path.expanduser("~/Downloads/ElevenLabs_2026-10-27T09_07_57*.mp3")))
n = lambda s: re.sub(r"\[[^\]]*\]", " ", s).lower().replace("-", " ")
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", n(s)).split()
parts = {}
for f in glob.glob(f"{V4}/prompts/ch*_part*.txt"):
    k = re.search(r"ch(\d+)_part(\d)", f); parts[(int(k[1]), int(k[2]))] = norm(open(f).read())
m = WhisperModel("base.en", device="cpu", compute_type="int8")
out = []
for f in files:
    segs, info = m.transcribe(f, beam_size=1, vad_filter=False)
    got = norm(" ".join(s.text for s in segs))
    sc = sorted(((difflib.SequenceMatcher(None, got, p, autojunk=False).ratio(), k) for k, p in parts.items()), reverse=True)[:2]
    out.append(dict(file=f, dur=round(info.duration, 1), best=sc[0][1], r=round(sc[0][0], 3), second=sc[1][1], r2=round(sc[1][0], 3), head=" ".join(got[:8])))
    print(os.path.basename(f)[11:30], os.path.basename(f)[-12:], round(info.duration), sc[0][1], round(sc[0][0], 2), "|", sc[1][1], round(sc[1][0], 2), flush=True)
json.dump(out, open(f"{V4}/dropped_matches.json", "w"), indent=1)
