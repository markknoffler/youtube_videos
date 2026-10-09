#!/usr/bin/env python3
"""
Synthesizes the complete 25-minute 10-chapter voiceover narration using Coqui TTS (FastPitch + HiFiGAN).
Saves individual WAV tracks in audio/ and records exact durations in audio/audio_timings_25min.json.
"""

import os
import json
import time
import subprocess
from TTS.api import TTS

AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio"))
SCENES_JSON = os.path.join(AUDIO_DIR, "scenes_narration_25min.json")
TIMINGS_JSON = os.path.join(AUDIO_DIR, "audio_timings_25min.json")

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except:
        return 0.0

def main():
    print("=== Initializing Coqui TTS for 25-Minute Masterclass ===")
    tts = TTS('tts_models/en/ljspeech/fast_pitch', progress_bar=False, gpu=False)
    
    with open(SCENES_JSON, 'r') as f:
        scenes = json.load(f)
        
    timings = {}
    
    for scene_id, text in scenes.items():
        out_wav = os.path.join(AUDIO_DIR, f"{scene_id}.wav")
        print(f"\n--- Synthesizing Narration for: {scene_id} ---")
        t0 = time.time()
        tts.tts_to_file(text=text, file_path=out_wav)
        dur = get_audio_duration(out_wav)
        timings[scene_id] = {
            "wav_path": out_wav,
            "duration": dur,
            "char_count": len(text),
            "synthesis_time": time.time() - t0
        }
        print(f"Generated {scene_id}.wav | Duration: {dur:.2f}s | Synthesized in {time.time() - t0:.2f}s")
        
    with open(TIMINGS_JSON, 'w') as f:
        json.dump(timings, f, indent=2)
        
    total_audio_dur = sum(item["duration"] for item in timings.values())
    print(f"\n=== Audio Synthesis Complete ===")
    print(f"Total Video Narration Runtime: {total_audio_dur:.2f} seconds ({total_audio_dur/60:.2f} minutes)")
    print(f"Saved timings to {TIMINGS_JSON}")

if __name__ == "__main__":
    main()
