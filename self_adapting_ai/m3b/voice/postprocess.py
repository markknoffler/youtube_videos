#!/usr/bin/env python3
"""Uniform chapter mastering on the Mac (run with ~/dfn_venv/bin/python):
  cloned : DeepFilterNet denoise → steep 9 kHz low-pass → de-esser → constant room tone → -16 LUFS MP3
  standard: constant room tone → -16 LUFS MP3 (already clean; no denoise, to avoid artifacts)
Processing the whole chapter at once means every phrase gets identical treatment, and the room tone
is one continuous bed — so noise never switches on and off between phrases.
usage: postprocess.py <cloned|standard> [chapters...]"""
import os, sys, subprocess, numpy as np, soundfile as sf, scipy.signal as sg
HERE = os.path.dirname(os.path.abspath(__file__)); SA = os.path.dirname(os.path.dirname(HERE))
voice, chs = sys.argv[1], [int(c) for c in sys.argv[2:]] or range(1, 13)
src_dir, out_dir = os.environ.get("SRC_DIR", f"{SA}/audio_v3_{voice}"), os.environ.get("OUT_DIR", f"{SA}/audio_final_{voice}")
os.makedirs(out_dir, exist_ok=True)
SRC_EXT = os.environ.get("SRC_EXT", "flac")
if voice == "cloned":
    from df.enhance import enhance, init_df
    import torch
    model, state, _ = init_df()
rng = np.random.default_rng(5)
for ch in chs:
    src = f"{src_dir}/Scene{ch:02d}.{SRC_EXT}"
    tmp = f"/tmp/pp_{voice}_{ch:02d}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "48000", tmp + "_in.wav"], check=True)
    y, sr = sf.read(tmp + "_in.wav", dtype="float32")
    if voice == "cloned":
        y = enhance(model, state, torch.from_numpy(y)[None])[0].numpy()
        y = sg.fftconvolve(y, sg.firwin(1025, 9000, fs=sr, window=("kaiser", 9.0)), mode="same").astype(np.float32)
        sf.write(tmp + "_dn.wav", y, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp + "_dn.wav", "-af", "deesser=i=0.5:m=0.5:f=0.5", tmp + "_ds.wav"], check=True)
        y, _ = sf.read(tmp + "_ds.wav", dtype="float32")
    # one continuous, very quiet room-tone bed (pink-ish, about -66 dBFS) under the whole chapter
    w = rng.normal(size=len(y)).astype(np.float32)
    b, a = sg.butter(1, 1500, fs=sr); bed = sg.lfilter(b, a, w); bed = bed / (np.abs(bed).max() + 1e-9) * 10 ** (-66 / 20) * 3
    sf.write(tmp + "_mix.wav", np.clip(y + bed, -1, 1), sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp + "_mix.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2",
                    "-c:a", "libmp3lame", "-b:a", "192k", f"{out_dir}/Scene{ch:02d}.mp3"], check=True)
    for f in ("_in", "_dn", "_ds", "_mix"):
        if os.path.exists(tmp + f + ".wav"): os.remove(tmp + f + ".wav")
    print("mastered", voice, ch, flush=True)
