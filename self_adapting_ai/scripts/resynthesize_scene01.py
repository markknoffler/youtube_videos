#!/usr/bin/env python3
"""
Re-synthesize Scene 01 with the 2026 SOTA models and update subtitles.json.
"""

import os
import sys
import json
import subprocess
import asyncio
import edge_tts

OUTPUT_AUDIO_DIR = "remotion_studio/public/audio_natural"
OUTPUT_SUBTITLES_JSON = "remotion_studio/src/data/subtitles.json"
VOICE = "en-US-ChristopherNeural"
FPS = 30
TARGET_DURATION_SEC = 150.0

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from masterclass_text import EXPANDED_CHAPTERS

async def resynthesize_scene01():
    scene_key = "Scene01_TheMonolith"
    short_key = "Scene01"
    temp_dir = f"audio/temp_{short_key}"
    os.makedirs(temp_dir, exist_ok=True)
    
    data = EXPANDED_CHAPTERS[scene_key]
    paragraphs = data["paragraphs"]
    para_files = []
    cues = []
    current_time_offset = 0.0
    
    print(f"Synthesizing {short_key} with 2026 SOTA models...")
    
    for idx, p_text in enumerate(paragraphs):
        p_mp3 = os.path.join(temp_dir, f"p_{idx:02d}.mp3")
        
        communicate = edge_tts.Communicate(p_text, VOICE, rate="+0%")
        para_cues = []
        
        with open(p_mp3, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    s_sec = chunk["offset"] / 10_000_000
                    d_sec = chunk["duration"] / 10_000_000
                    para_cues.append({
                        "text": chunk["text"].strip(),
                        "startSec": round(current_time_offset + s_sec, 2),
                        "endSec": round(current_time_offset + s_sec + d_sec, 2)
                    })
                    
        dur_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", p_mp3
        ]
        dur = float(subprocess.check_output(dur_cmd).decode().strip())
        
        if not para_cues:
            para_cues.append({
                "text": p_text.strip(),
                "startSec": round(current_time_offset, 2),
                "endSec": round(current_time_offset + dur, 2)
            })
            
        for c in para_cues:
            cues.append({
                "index": len(cues) + 1,
                "startSec": c["startSec"],
                "endSec": c["endSec"],
                "startFrame": int(c["startSec"] * FPS),
                "endFrame": int(c["endSec"] * FPS),
                "text": c["text"]
            })
            
        para_files.append(p_mp3)
        pause_mp3 = os.path.join(temp_dir, f"pause_{idx:02d}.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", "0.45", "-q:a", "9", pause_mp3
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        para_files.append(pause_mp3)
        current_time_offset += dur + 0.45
        print(f"  [P{idx+1}/{len(paragraphs)}] synthesized ({dur:.1f}s)")
        
    concat_list = os.path.join(temp_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for pf in para_files:
            f.write(f"file '{os.path.abspath(pf)}'\n")
            
    raw_stitched = os.path.join(temp_dir, "stitched.wav")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-ar", "44100", "-ac", "2", raw_stitched
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    dur_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", raw_stitched
    ]
    actual_dur = float(subprocess.check_output(dur_cmd).decode().strip())
    print(f"  Actual spoken duration: {actual_dur:.2f}s")
    
    final_out = os.path.join(OUTPUT_AUDIO_DIR, f"{scene_key}_natural.wav")
    if actual_dur < TARGET_DURATION_SEC:
        pad_needed = TARGET_DURATION_SEC - actual_dur
        pad_filter = f"apad=pad_dur={pad_needed:.3f}"
    else:
        pad_filter = f"atrim=0:{TARGET_DURATION_SEC},afade=t=out:st=149.0:d=1.0"
        
    master_filter = (
        f"{pad_filter},"
        "equalizer=f=120:t=q:w=1.2:g=2.0,"
        "equalizer=f=3500:t=q:w=1.0:g=1.2,"
        "alimiter=limit=0.95"
    )
    
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_stitched,
        "-af", master_filter,
        "-ar", "44100", "-ac", "2",
        final_out
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  Mastered Scene 01 audio exported to: {final_out}")
    
    # Update subtitles.json
    with open(OUTPUT_SUBTITLES_JSON, "r") as f:
        sub_data = json.load(f)
        
    sub_data["Scene01"] = cues
    with open(OUTPUT_SUBTITLES_JSON, "w") as f:
        json.dump(sub_data, f, indent=2)
        
    print(f"  Updated Scene01 in {OUTPUT_SUBTITLES_JSON} with {len(cues)} cues.")

if __name__ == "__main__":
    asyncio.run(resynthesize_scene01())
