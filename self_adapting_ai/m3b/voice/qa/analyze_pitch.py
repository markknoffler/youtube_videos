"""Per-segment pitch (Praat autocorrelation) for a finished voice set, vs its direction tags."""
import json, os, sys, subprocess, numpy as np, parselmouth
HERE = os.path.dirname(os.path.abspath(__file__)); VOICE_DIR = os.path.dirname(HERE)
sys.path.insert(0, VOICE_DIR)
from direction import direction_chapters
SA = os.path.dirname(os.path.dirname(VOICE_DIR))
voice, adir, sdir = sys.argv[1], sys.argv[2], sys.argv[3]
D = direction_chapters()
rows = []
for ch in range(1, 13):
    wav = f"/tmp/qa_{voice}_{ch:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SA}/{adir}/Scene{ch:02d}.mp3", "-ac", "1", "-ar", "16000", wav], check=True)
    snd = parselmouth.Sound(wav)
    pitch = snd.to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=400, voicing_threshold=0.5)
    t = pitch.xs(); f0 = pitch.selected_array["frequency"]
    for sg in json.load(open(f"{SA}/{sdir}/Scene{ch:02d}_segments.json"))["segments"]:
        m = (t >= sg["s"]) & (t <= sg["e"]) & (f0 > 0)
        if m.sum() < 8: continue
        d = D[ch][sg["i"]]
        rows.append(dict(ch=ch, i=sg["i"], f0=float(np.median(f0[m])), p=d.get("p"), e=d.get("e"), x=d.get("x"), s=d.get("s"), text=sg["text"][:60]))
f = np.array([r["f0"] for r in rows]); ref = np.median(f)
for r in rows: r["st"] = 12 * np.log2(r["f0"] / ref)
json.dump(rows, open(f"/tmp/pitch3_{voice}.json", "w"))
print(f"{voice}: median F0 {ref:.0f} Hz | segments {len(rows)} | std {np.std([r['st'] for r in rows]):.2f} st | "
      f"|dev|>2st: {sum(abs(r['st'])>2 for r in rows)} | >3st: {sum(abs(r['st'])>3 for r in rows)}")
for key in ("p", "x", "e"):
    g = {}
    for r in rows: g.setdefault(r[key], []).append(r["st"])
    print(" by", key, {k: f"{np.mean(v):+.1f}st (n={len(v)})" for k, v in sorted(g.items(), key=lambda kv: str(kv[0]))})
firsts = [r["st"] for r in rows if r["i"] == 0]
print(f" chapter-first segments: mean {np.mean(firsts):+.1f} st, values {[round(x,1) for x in firsts]}")
print(" worst 12:")
for r in sorted(rows, key=lambda r: -abs(r["st"]))[:12]:
    print(f"  ch{r['ch']:02d}#{r['i']:03d} {r['f0']:.0f} Hz {r['st']:+.1f}st p={r['p']} e={r['e']} x={r['x']} | {r['text']}")
