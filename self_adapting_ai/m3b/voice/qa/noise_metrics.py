"""Noise / air metrics: noise floor, HF (5-12 kHz) energy in quiet frames, breathiness proxy (HF/LF in speech)."""
import sys, subprocess, numpy as np, scipy.signal as sg, soundfile as sf
def load(p, sr=24000):
    out = subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"])
    return np.frombuffer(out, np.float32), sr
def metrics(p):
    y, sr = load(p)
    f, t, S = sg.spectrogram(y, sr, nperseg=1024, noverlap=768)
    P = S + 1e-14
    frame_db = 10 * np.log10(P.sum(0))
    q = frame_db < np.percentile(frame_db, 15)            # quietest 15% = noise floor frames
    sp = frame_db > np.percentile(frame_db, 60)           # loud frames = speech
    hf, lf, mf = (f >= 5000) & (f <= 12000), (f >= 80) & (f <= 1000), (f >= 1000) & (f < 5000)
    db = lambda x: 10 * np.log10(x + 1e-14)
    return dict(noise_floor_db=float(np.percentile(frame_db, 15) - np.percentile(frame_db, 99)),
                hf_in_quiet_db=float(db(P[hf][:, q].mean())), hf_minus_lf_speech_db=float(db(P[hf][:, sp].mean()) - db(P[lf][:, sp].mean())),
                flatness_hf_speech=float(np.exp(np.mean(np.log(P[hf][:, sp]))) / np.mean(P[hf][:, sp])))
if __name__ == "__main__":
    for p in sys.argv[1:]:
        m = metrics(p); print(f"{p.split('/')[-1][:44]:44s} floor {m['noise_floor_db']:6.1f} dB | HF@quiet {m['hf_in_quiet_db']:6.1f} dB | HF-LF speech {m['hf_minus_lf_speech_db']:6.1f} dB | HF flat {m['flatness_hf_speech']:.2f}")
