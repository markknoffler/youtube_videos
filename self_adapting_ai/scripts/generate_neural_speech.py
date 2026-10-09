#!/usr/bin/env python3
"""
Generate Studio-Grade Neural Documentary Speech for all 10 Chapters using edge-tts
Voice: en-US-ChristopherNeural (Authoritative BBC/PBS Documentary Narrator)
Generates:
1. Clean 44.1kHz audio files for all 10 scenes in remotion_studio/public/audio_natural/
2. Precise sentence-level subtitle timestamps in remotion_studio/src/data/subtitles.json
3. Exactly 150.00 seconds per scene with clean ambient tail padding
"""

import os
import sys
import json
import re
import subprocess
import asyncio
import edge_tts

OUTPUT_AUDIO_DIR = "remotion_studio/public/audio_natural"
OUTPUT_SUBTITLES_JSON = "remotion_studio/src/data/subtitles.json"
VOICE = "en-US-ChristopherNeural"
FPS = 30
TARGET_DURATION_SEC = 150.0

os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from masterclass_text import EXPANDED_CHAPTERS

def parse_vtt(vtt_text):
    """Parse WebVTT cues into timestamps and text."""
    cues = []
    blocks = vtt_text.strip().split("\n\n")
    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        # Find timestamp line (e.g. 00:00:01.200 --> 00:00:05.400)
        time_line_idx = -1
        for i, line in enumerate(lines):
            if "-->" in line:
                time_line_idx = i
                break
        if time_line_idx == -1:
            continue
        
        time_part = lines[time_line_idx]
        text_parts = lines[time_line_idx + 1:]
        text = " ".join(text_parts).strip()
        
        start_str, end_str = time_part.split("-->")
        def to_sec(s):
            s = s.strip()
            parts = s.split(":")
            if len(parts) == 3:
                h, m, sec = parts
                return float(h) * 3600 + float(m) * 60 + float(sec)
            elif len(parts) == 2:
                m, sec = parts
                return float(m) * 60 + float(sec)
            return float(s)
            
        start_sec = to_sec(start_str)
        end_sec = to_sec(end_str)
        if text:
            cues.append({
                "startSec": round(start_sec, 2),
                "endSec": round(end_sec, 2),
                "text": text
            })
    return cues

async def synthesize_chapter(scene_key, short_key, data):
    print(f"\n=======================================================")
    print(f"Synthesizing {short_key}: {data['title']}")
    print(f"=======================================================")
    
    temp_dir = f"audio/temp_{short_key}"
    os.makedirs(temp_dir, exist_ok=True)
    
    paragraphs = data["paragraphs"]
    para_files = []
    all_cues = []
    current_time_offset = 0.0
    
    for idx, p_text in enumerate(paragraphs):
        p_mp3 = os.path.join(temp_dir, f"p_{idx:02d}.mp3")
        p_vtt = os.path.join(temp_dir, f"p_{idx:02d}.vtt")
        
        # Synthesize paragraph with edge-tts
        communicate = edge_tts.Communicate(p_text, VOICE, rate="+0%")
        submaker = edge_tts.SubMaker()
        
        with open(p_mp3, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.feed(chunk)
                    
        # Write VTT
        vtt_content = submaker.get_srt()
        with open(p_vtt, "w") as f:
            f.write(vtt_content)
            
        # Get actual duration of this paragraph
        dur_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", p_mp3
        ]
        dur_res = subprocess.run(dur_cmd, capture_output=True, text=True, check=True)
        dur = float(dur_res.stdout.strip())
        
        # Parse cues and adjust with current_time_offset
        cues = parse_vtt(vtt_content)
        for c in cues:
            start_s = round(current_time_offset + c["startSec"], 2)
            end_s = round(current_time_offset + c["endSec"], 2)
            all_cues.append({
                "index": len(all_cues) + 1,
                "startSec": start_s,
                "endSec": end_s,
                "startFrame": int(start_s * FPS),
                "endFrame": int(end_s * FPS),
                "text": c["text"]
            })
            
        para_files.append(p_mp3)
        # 0.45s natural breathing pause between paragraphs
        pause_mp3 = os.path.join(temp_dir, f"pause_{idx:02d}.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", "0.45", "-q:a", "9", pause_mp3
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        para_files.append(pause_mp3)
        current_time_offset += dur + 0.45
        print(f"  [P{idx+1}/{len(paragraphs)}] synthesized ({dur:.1f}s, total so far: {current_time_offset:.1f}s)")
        
    # Concatenate all paragraphs into full scene audio
    concat_list = os.path.join(temp_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for pf in para_files:
            f.write(f"file '{os.path.abspath(pf)}'\n")
            
    raw_stitched = os.path.join(temp_dir, "stitched.wav")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-ar", "44100", "-ac", "2", raw_stitched
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Check total speech duration
    dur_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", raw_stitched
    ]
    dur_res = subprocess.run(dur_cmd, capture_output=True, text=True, check=True)
    actual_dur = float(dur_res.stdout.strip())
    print(f"  Actual spoken speech duration: {actual_dur:.2f}s")
    
    # Master final audio to exactly 150.00 seconds:
    # 1. Subtle warm broadcast compression & gentle high-shelf warmth
    # 2. Pad with silence to exactly 150.00 seconds
    final_out = os.path.join(OUTPUT_AUDIO_DIR, f"{scene_key}_natural.wav")
    
    # Pad to 150.0s if needed or trim smoothly with fadeout if slightly over
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
    
    cmd_master = [
        "ffmpeg", "-y", "-i", raw_stitched,
        "-af", master_filter,
        "-ar", "44100", "-ac", "2",
        final_out
    ]
    subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  Final mastered audio exported to: {final_out} (Exactly {TARGET_DURATION_SEC}s)")
    
    return all_cues

async def main():
    scene_map = [
        ("Scene01_TheMonolith", "Scene01"),
        ("Scene02_TheBiologicalDream", "Scene02"),
        ("Scene03_TheSelfOrganizingHypothesis", "Scene03"),
        ("Scene04_TheParadox", "Scene04"),
        ("Scene05_Theorem1_RankCollapse", "Scene05"),
        ("Scene06_Theorem2_RoutingBounds", "Scene06"),
        ("Scene07_Theorem3_HardwareBarrier", "Scene07"),
        ("Scene08_EmpiricalBenchmarks", "Scene08"),
        ("Scene09_FrontierLabs", "Scene09"),
        ("Scene10_The10YearFrontier", "Scene10"),
    ]
    
    all_subtitles = {}
    for scene_key, short_key in scene_map:
        data = EXPANDED_CHAPTERS[scene_key]
        cues = await synthesize_chapter(scene_key, short_key, data)
        all_subtitles[short_key] = cues
        
    with open(OUTPUT_SUBTITLES_JSON, "w") as f:
        json.dump(all_subtitles, f, indent=2)
        
    print(f"\n=======================================================")
    print(f"All 10 chapters synthesized with en-US-ChristopherNeural!")
    print(f"Synchronized subtitles saved to {OUTPUT_SUBTITLES_JSON}")
    print(f"=======================================================")

if __name__ == "__main__":
    asyncio.run(main())
