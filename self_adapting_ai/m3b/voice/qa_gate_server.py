#!/usr/bin/env python3
"""Segment quality gate: pitch drift + speaker identity, served over localhost HTTP.

Run it in its OWN venv (never inside a training env — speechbrain pulls its own torch):
  python -m venv ~/sb_venv && ~/sb_venv/bin/pip install speechbrain soundfile praat-parselmouth "numpy<2.3"
  ~/sb_venv/bin/python m3b/voice/qa_gate_server.py --voice cloned=voice_ref/user_ref_clean.wav:120 \
        --voice standard=audio_v2_standard/standard_voice_ref.wav:128
POST /score {"path": "seg.wav", "voice": "cloned"} → {"sim", "f0", "st", "range_st", "dur", "voiced"}
  sim  = ECAPA-TDNN cosine similarity to that voice's reference
  st   = median F0 of the segment relative to the voice's target F0, in semitones
"""
import argparse, json, numpy as np, soundfile as sf, scipy.signal as sg, parselmouth, torch
from http.server import BaseHTTPRequestHandler, HTTPServer
from speechbrain.inference.speaker import EncoderClassifier

enc = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="/tmp/ecapa", run_opts={"device": "cpu"})
VOICES = {}


def load16(path):
    y, sr = sf.read(path, dtype="float32")
    y = y.mean(1) if y.ndim > 1 else y
    return y, sr, (sg.resample_poly(y, 16000, sr).astype(np.float32) if sr != 16000 else y)


def embed(y16):
    with torch.no_grad():
        e = enc.encode_batch(torch.from_numpy(y16)[None])[0, 0]
    return (e / e.norm()).numpy()


def f0_stats(y, sr):
    p = parselmouth.Sound(y.astype(np.float64), sr).to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=400, voicing_threshold=0.5)
    f = p.selected_array["frequency"]
    return f[f > 0]


def prepare(spec):
    name, rest = spec.split("=", 1)
    path, _, tgt = rest.partition(":")
    y, sr, y16 = load16(path)
    f = f0_stats(y, sr)
    VOICES[name] = dict(emb=embed(y16), f0=float(tgt) if tgt else float(np.median(f)))
    print(f"[gate] voice {name}: ref {path} target F0 {VOICES[name]['f0']:.0f} Hz (ref median {np.median(f):.0f} Hz)", flush=True)


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        v = VOICES[req["voice"]]
        y, sr, y16 = load16(req["path"])
        f = f0_stats(y, sr)
        out = dict(dur=len(y) / sr, voiced=int(len(f)), sim=float(v["emb"] @ embed(y16)))
        if len(f) >= 8:
            out.update(f0=float(np.median(f)), st=float(12 * np.log2(np.median(f) / v["f0"])),
                       range_st=float(12 * np.log2(np.percentile(f, 95) / np.percentile(f, 5))))
        body = json.dumps(out).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--voice", action="append", required=True, help="name=ref.wav[:targetF0Hz]")
    a = ap.parse_args()
    for s in a.voice:
        prepare(s)
    print(f"[gate] listening on 127.0.0.1:{a.port}", flush=True)
    HTTPServer(("127.0.0.1", a.port), H).serve_forever()
