"""ECAPA-TDNN speaker embeddings (SpeechBrain, CPU). usage: speaker_sim.py ref.wav a.wav b.wav ..."""
import sys, subprocess, numpy as np, torch
from speechbrain.inference.speaker import EncoderClassifier
_enc = None
def embed(path, start=None, end=None):
    global _enc
    if _enc is None:
        _enc = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="/tmp/ecapa", run_opts={"device": "cpu"})
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(start), "-to", str(end)] if start is not None else []) + ["-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    y = torch.from_numpy(np.frombuffer(subprocess.check_output(cmd), np.float32).copy())[None]
    with torch.no_grad():
        e = _enc.encode_batch(y)[0, 0]
    return (e / e.norm()).numpy()
if __name__ == "__main__":
    ref = embed(sys.argv[1])
    for p in sys.argv[2:]:
        print(f"{p.split('/')[-1]:40s} cos-sim to ref = {float(ref @ embed(p)):.3f}")
