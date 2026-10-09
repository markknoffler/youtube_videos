#!/usr/bin/env python3
"""
Stitches all 10 Manim rendered scenes with Coqui TTS voiceover audio.
Uses continuous PTS scaling (setpts=(A_dur/V_dur)*PTS) so animations play smoothly
and continuously across the entire narration duration with ZERO long frozen pauses!
"""

import os
import json
import subprocess

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANIM_DIR = os.path.join(PROJECT_DIR, "manim")
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
TIMINGS_JSON = os.path.join(AUDIO_DIR, "audio_timings_25min.json")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SCENES = [
    "Scene1_TheMonolith",
    "Scene2_TheBiologicalDream",
    "Scene3_SelfOrganizingHypothesis",
    "Scene4_TheParadox",
    "Scene5_Theorem1_RankCollapse",
    "Scene6_Theorem2_RoutingBounds",
    "Scene7_Theorem3_HardwareBarrier",
    "Scene8_EmpiricalBenchmarks",
    "Scene9_FrontierLabs",
    "Scene10_The10YearFrontier"
]

def get_duration(file_path):
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
    print("=== Continuous Muxing: 10 Chapters with Zero Wait Gaps ===")
    
    quality_dirs = [
        os.path.join(MANIM_DIR, "media", "videos", "script", "1080p60"),
        os.path.join(MANIM_DIR, "media", "videos", "script", "480p15"),
    ]
    
    video_dir = None
    for qd in quality_dirs:
        if os.path.exists(qd):
            video_dir = qd
            break
            
    if not video_dir:
        raise FileNotFoundError("Could not find rendered video directory!")
        
    print(f"Using rendered scene video directory: {video_dir}")
    
    with open(TIMINGS_JSON, 'r') as f:
        timings = json.load(f)
        
    muxed_scene_files = []
    concat_list_file = os.path.join(OUTPUT_DIR, "concat_list_25min.txt")
    
    for scene in SCENES:
        raw_video = os.path.join(video_dir, f"{scene}.mp4")
        audio_file = os.path.join(AUDIO_DIR, f"{scene}.wav")
        muxed_scene_output = os.path.join(OUTPUT_DIR, f"muxed_{scene}.mp4")
        
        if not os.path.exists(raw_video):
            raise FileNotFoundError(f"Missing video for scene: {raw_video}")
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Missing audio for scene: {audio_file}")
            
        v_dur = get_duration(raw_video)
        a_dur = get_duration(audio_file)
        
        print(f"\nProcessing {scene}: Video = {v_dur:.2f}s | Audio = {a_dur:.2f}s")
        
        # Smooth continuous speed scaling: stretch video so animation moves continuously throughout narration!
        speed_factor = a_dur / max(v_dur, 0.1)
        vf_filter = f"setpts={speed_factor:.4f}*PTS,fps=30"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", raw_video,
            "-i", audio_file,
            "-filter_complex", f"[0:v]{vf_filter}[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            muxed_scene_output
        ]
        
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out_dur = get_duration(muxed_scene_output)
        print(f"  -> Generated {muxed_scene_output} (Continuous duration: {out_dur:.2f}s, Zero freeze gaps)")
        muxed_scene_files.append(muxed_scene_output)
        
    # Write concat list
    with open(concat_list_file, 'w') as f:
        for fpath in muxed_scene_files:
            f.write(f"file '{fpath}'\n")
            
    final_output = os.path.join(OUTPUT_DIR, "final_explainer_video_25min.mp4")
    print(f"\nConcatenating all 10 chapters into {final_output}...")
    
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        final_output
    ]
    subprocess.run(concat_cmd, check=True)
    
    total_dur = get_duration(final_output)
    print(f"\n=========================================================")
    print(f"🎉 25-MINUTE PRODUCTION VIDEO READY: {final_output}")
    print(f"Total Runtime: {total_dur:.2f} seconds ({total_dur/60:.2f} minutes)")
    print(f"=========================================================")

if __name__ == "__main__":
    main()
