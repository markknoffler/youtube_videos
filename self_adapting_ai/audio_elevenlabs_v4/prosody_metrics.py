"""Pace / pitch-variation / pause metrics for a list of audio files with their word counts.  usage: prosody_metrics.py file:words ..."""
import sys, subprocess, re, numpy as np, parselmouth
def metrics(path, words):
    snd = parselmouth.Sound(path); dur = snd.duration
    f0 = snd.to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=350, voicing_threshold=0.5).selected_array["frequency"]; f0 = f0[f0 > 0]
    st = 12 * np.log2(f0 / np.median(f0))
    sil = subprocess.run(["ffmpeg", "-i", path, "-af", "silencedetect=n=-35dB:d=0.25", "-f", "null", "-"], capture_output=True, text=True).stderr
    pauses = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", sil)]
    return dict(dur=round(dur, 1), wps=round(words / dur, 2), f0_med=round(float(np.median(f0))), pitch_sd_st=round(float(st.std()), 2),
                pitch_p5_p95_st=round(float(np.percentile(st, 95) - np.percentile(st, 5)), 1), pauses=len(pauses), pause_total=round(sum(pauses), 1),
                pause_mean=round(float(np.mean(pauses)), 2) if pauses else 0, speech_wps=round(words / (dur - sum(pauses)), 2))
if __name__ == "__main__":
    for a in sys.argv[1:]:
        p, w = a.rsplit(":", 1); print(p.split("/")[-1][:40], metrics(p, int(w)))
