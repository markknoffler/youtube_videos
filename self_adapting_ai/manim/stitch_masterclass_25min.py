#!/usr/bin/env python3
"""
Masterclass 25-Minute Stitching Pipeline
Stitches all 10 Manim scenes (720p 30fps) with their corresponding 150.0s mastered narration audio.
Uses continuous PTS scaling to eliminate frozen pause gaps.
Outputs: output/masterclass_25min_complete.mp4 (45,000 frames, 1,500.0 seconds, exactly 25:00)
"""

import os
import sys
import subprocess
import json

SCENES = [
    "Scene01_TheMonolith",
    "Scene02_TheBiologicalDream",
    "Scene03_TheSelfOrganizingHypothesis",
    "Scene04_TheParadox",
    "Scene05_Theorem1_RankCollapse",
    "Scene06_Theorem2_RoutingBounds",
    "Scene07_Theorem3_HardwareBarrier",
    "Scene08_EmpiricalBenchmarks",
    "Scene09_FrontierLabs",
    "Scene10_The10YearFrontier"
]

def get_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    return float(subprocess.check_output(cmd).decode().strip())

def main():
    video_dir = "manim_media_masterclass/videos/script_masterclass/720p30"
    audio_dir = "audio/masterclass_25min"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = "output/temp_masterclass_scenes"
    os.makedirs(temp_dir, exist_ok=True)
    
    stitched_scene_files = []
    
    print("\n=======================================================")
    print("STEP 1: SYNCING EACH SCENE WITH 150.0s CONTINUOUS MOTION")
    print("=======================================================")
    
    for idx, scene in enumerate(SCENES, 1):
        v_file = os.path.join(video_dir, f"{scene}.mp4")
        a_file = os.path.join(audio_dir, f"{scene}_mastered.wav")
        out_scene = os.path.join(temp_dir, f"{scene}_synced.mp4")
        
        if not os.path.exists(v_file):
            raise FileNotFoundError(f"Missing video: {v_file}")
        if not os.path.exists(a_file):
            raise FileNotFoundError(f"Missing audio: {a_file}")
            
        v_dur = get_duration(v_file)
        a_dur = get_duration(a_file)
        target_dur = 150.0
        
        print(f"[{idx}/10] {scene}: Video={v_dur:.2f}s, Audio={a_dur:.2f}s -> Target={target_dur:.2f}s")
        
        # Scale video PTS to match audio duration continuously
        pts_scale = target_dur / v_dur
        cmd = [
            "ffmpeg", "-y",
            "-i", v_file,
            "-i", a_file,
            "-filter_complex",
            f"[0:v]setpts={pts_scale:.6f}*PTS,scale=1280:720,fps=30[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", "150.0",
            out_scene
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        actual_dur = get_duration(out_scene)
        print(f"       -> Generated: {out_scene} ({actual_dur:.2f}s)")
        stitched_scene_files.append(out_scene)
        
    print("\n=======================================================")
    print("STEP 2: CONCATENATING ALL 10 SCENES INTO 25-MIN MASTER")
    print("=======================================================")
    
    concat_list = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_list, "w") as f:
        for fpath in stitched_scene_files:
            abs_path = os.path.abspath(fpath)
            f.write(f"file '{abs_path}'\n")
            
    final_output = os.path.join(output_dir, "masterclass_25min_complete.mp4")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        final_output
    ]
    subprocess.run(concat_cmd, check=True)
    
    final_dur = get_duration(final_output)
    total_frames = int(final_dur * 30)
    print("\n=======================================================")
    print(f"MASTERCLASS 25-MINUTE PRODUCTION COMPLETE!")
    print(f"Output File: {final_output}")
    print(f"Total Duration: {final_dur:.2f} seconds ({final_dur/60.0:.2f} minutes)")
    print(f"Total Frames: {total_frames} @ 30 FPS")
    print("=======================================================\n")
    
    # Copy to Remotion Studio public folder
    remotion_public = "remotion_studio/public/masterclass_25min.mp4"
    subprocess.run(["cp", final_output, remotion_public], check=True)
    print(f"Copied to Remotion Studio: {remotion_public}")

if __name__ == "__main__":
    main()
