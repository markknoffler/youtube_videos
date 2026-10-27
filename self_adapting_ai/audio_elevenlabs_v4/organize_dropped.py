"""Move the hand-downloaded ElevenLabs files into takes/chNN/chNN_partK_takeX.mp3 and join the best take of each part into chapters/chNN.mp3."""
import json, os, shutil, subprocess, collections
V4 = os.path.dirname(os.path.abspath(__file__)); SA = os.path.dirname(V4)
M = json.load(open(f"{V4}/dropped_matches.json")); g = collections.defaultdict(list)
for m in sorted(M, key=lambda m: m["file"].replace(".mp3", "").replace(" (", "~(")):   # base file, then (1), (2)...
    g[tuple(m["best"])].append(m)
os.makedirs(f"{V4}/chapters", exist_ok=True); manifest = {}
for (c, p), ms in sorted(g.items()):
    d = f"{V4}/takes/ch{c:02d}"; os.makedirs(d, exist_ok=True); best = None
    for i, m in enumerate(ms):
        dst = f"{d}/ch{c:02d}_part{p}_take{'ABCD'[i]}.mp3"
        if m["file"].startswith(SA + "/ElevenLabs_"): shutil.move(m["file"], dst)
        else: shutil.copy(m["file"], dst)            # the Downloads copy stays where it is
        m["new"] = dst
        if best is None or m["r"] > best["r"] + 0.005: best = m
    manifest.setdefault(c, {})[p] = dict(chosen=os.path.basename(best["new"]), takes=[dict(file=os.path.basename(m["new"]), dur=m["dur"], r=m["r"]) for m in ms])
trim = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse"
for c, parts in sorted(manifest.items()):
    inputs, fc = [], []
    for k, p in enumerate((1, 2, 3)):
        inputs += ["-i", f"{V4}/takes/ch{c:02d}/{parts[p]['chosen']}"]; fc.append(f"[{k}:a]{trim},apad=pad_dur=0.35[a{k}]")
    fc = ";".join(fc) + ";[a0][a1][a2]concat=n=3:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[o]", "-c:a", "libmp3lame", "-b:a", "192k", f"{V4}/chapters/ch{c:02d}.mp3"], check=True)
for c, src in ((1, "ch01_take1.mp3"), (2, "ch02_take1.mp3")):
    shutil.copy(f"{V4}/raw/{src}", f"{V4}/chapters/ch{c:02d}.mp3"); manifest[c] = {"all": dict(chosen=src)}
json.dump(manifest, open(f"{V4}/manifest.json", "w"), indent=1)
for c in sorted(manifest): print(c, round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{V4}/chapters/ch{c:02d}.mp3"])), 1))
