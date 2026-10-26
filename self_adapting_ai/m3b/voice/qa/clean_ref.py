"""Denoise the user's recording in several ways; score noise + identity."""
import sys, subprocess, numpy as np, soundfile as sf, torch
from df.enhance import enhance, init_df
m, state, _ = init_df()
SRC = "my_voice/my_voice_3mins.m4a"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-ac", "1", "-ar", str(state.sr()), "/tmp/ref/raw48.wav"], check=True)
y, sr = sf.read("/tmp/ref/raw48.wav", dtype="float32")
x = torch.from_numpy(y)[None]
for name, lim in [("dfn_full", None), ("dfn_lim18", 18.0), ("dfn_lim12", 12.0)]:
    out = enhance(m, state, x, atten_lim_db=lim)[0].numpy()
    sf.write(f"/tmp/ref/{name}.wav", out, sr)
    print(name, "done", flush=True)
