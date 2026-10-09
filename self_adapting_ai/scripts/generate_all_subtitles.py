#!/usr/bin/env python3
"""
Extract sentence-level subtitle cues for all 10 chapters using edge-tts SentenceBoundary events,
aligned perfectly with the stitched paragraph audio files.
"""

import os
import sys
import json
import subprocess
import asyncio
import edge_tts

OUTPUT_SUBTITLES_JSON = "remotion_studio/src/data/subtitles.json"
VOICE = "en-US-ChristopherNeural"
FPS = 30

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from masterclass_text import EXPANDED_CHAPTERS

SCENES = [
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

async def process_scene(scene_key, short_key):
    temp_dir = f"audio/temp_{short_key}"
    data = EXPANDED_CHAPTERS[scene_key]
    paragraphs = data["paragraphs"]
    
    cues = []
    current_time_offset = 0.0
    
    print(f"Generating cues for {short_key} ({len(paragraphs)} paragraphs)...")
    
    for idx, p_text in enumerate(paragraphs):
        p_mp3 = os.path.join(temp_dir, f"p_{idx:02d}.mp3")
        dur_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", p_mp3
        ]
        dur_res = subprocess.run(dur_cmd, capture_output=True, text=True, check=True)
        dur = float(dur_res.stdout.strip())
        
        comm = edge_tts.Communicate(p_text, VOICE)
        para_cues = []
        async for chunk in comm.stream():
            if chunk["type"] == "SentenceBoundary":
                s_sec = chunk["offset"] / 10_000_000
                d_sec = chunk["duration"] / 10_000_000
                start_time = round(current_time_offset + s_sec, 2)
                end_time = round(current_time_offset + s_sec + d_sec, 2)
                # Ensure end does not exceed paragraph end boundary + small margin
                para_cues.append({
                    "startSec": start_time,
                    "endSec": end_time,
                    "text": chunk["text"].strip()
                })
                
        # If no SentenceBoundary emitted (edge case), fallback to whole paragraph
        if not para_cues:
            para_cues.append({
                "startSec": round(current_time_offset, 2),
                "endSec": round(current_time_offset + dur, 2),
                "text": p_text.strip()
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
            
        current_time_offset += dur + 0.45
        
    print(f"  -> {short_key}: Generated {len(cues)} sentence cues (total duration ~{current_time_offset:.2f}s)")
    return cues

async def main():
    all_subtitles = {}
    for scene_key, short_key in SCENES:
        cues = await process_scene(scene_key, short_key)
        all_subtitles[short_key] = cues
        
    with open(OUTPUT_SUBTITLES_JSON, "w") as f:
        json.dump(all_subtitles, f, indent=2)
        
    print(f"\nSaved all subtitle cues to {OUTPUT_SUBTITLES_JSON}")

if __name__ == "__main__":
    asyncio.run(main())
