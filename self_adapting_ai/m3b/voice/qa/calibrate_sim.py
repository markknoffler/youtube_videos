import sys, json, subprocess, numpy as np
sys.path.insert(0, "m3b/voice/qa"); sys.path.insert(0, "m3b/voice")
from speaker_sim import embed
voice, ref = sys.argv[1], sys.argv[2]
rows = json.load(open(f"/tmp/pitch_{voice}.json"))
R = embed(ref)
by = {}
for r in rows:
    sg = json.load(open(f"audio_v2_{voice}/Scene{r['ch']:02d}_segments.json"))["segments"][r["i"]]
    if sg["e"] - sg["s"] < 1.0: continue
    r["sim"] = float(R @ embed(f"audio_v2_{voice}/Scene{r['ch']:02d}.mp3", sg["s"], sg["e"])); by[(r["ch"], r["i"])] = r
rows = list(by.values()); sims = np.array([r["sim"] for r in rows]); st = np.array([abs(r["st"]) for r in rows])
print(f"{voice}: n={len(rows)} sim median {np.median(sims):.2f} p10 {np.percentile(sims,10):.2f} p90 {np.percentile(sims,90):.2f}")
for lo, hi in [(0, 1), (1, 2), (2, 3), (3, 6), (6, 30)]:
    m = (st >= lo) & (st < hi)
    if m.sum(): print(f"  |pitch dev| {lo}-{hi} st: n={m.sum():3d}  mean sim {sims[m].mean():.2f}  min {sims[m].min():.2f}")
json.dump(rows, open(f"/tmp/sim_{voice}.json", "w"))
