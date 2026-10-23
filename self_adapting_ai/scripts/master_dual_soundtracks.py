#!/usr/bin/env python3
"""
Dual-Soundtrack Master & Video Multiplexer for 25-Minute Masterclass:
'Why Brain-Like AI Failed (And What We Built Instead)'

This script:
1. Conforms and masters both audio sets (Cloned User Voice and Standard Deep Narrator Voice)
   for all 10 chapters to exactly 150.000 seconds each.
2. Ingests them into remotion_studio/public/audio_cloned/, remotion_studio/public/audio_standard/,
   and remotion_studio/public/audio_natural/.
3. Synthesizes two broadcast-grade, seamless 25:00.00 (1500.00s) soundtracks with continuous ambient bed.
4. Generates two complete YouTube-ready masterclass videos:
   - output/Why_Brain-Like_AI_Failed_Cloned_Voice.mp4 (User's Voice)
   - output/Why_Brain-Like_AI_Failed_Standard_Voice.mp4 (Standard Deep Male Voice)
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/samreedhbhuyan/Desktop/Win_C/youtube_videos/self_adapting_ai")
PUBLIC_DIR = BASE_DIR / "remotion_studio" / "public"
OUTPUT_DIR = BASE_DIR / "output"
AMBIENT_BED = PUBLIC_DIR / "audio_natural" / "ambient_bed.wav"

CLONED_SRC_DIR = BASE_DIR / "audio_fish_s2_pro_cloned"
STANDARD_SRC_DIR = BASE_DIR / "audio_fish_s2_pro_standard"

PUBLIC_CLONED_DIR = PUBLIC_DIR / "audio_cloned"
PUBLIC_STANDARD_DIR = PUBLIC_DIR / "audio_standard"
PUBLIC_NATURAL_DIR = PUBLIC_DIR / "audio_natural"

SCENES = [
    ("Scene01", "Scene01_TheMonolith"),
    ("Scene02", "Scene02_TheBiologicalDream"),
    ("Scene03", "Scene03_TheSelfOrganizingHypothesis"),
    ("Scene04", "Scene04_TheParadox"),
    ("Scene05", "Scene05_Theorem1_RankCollapse"),
    ("Scene06", "Scene06_Theorem2_RoutingBounds"),
    ("Scene07", "Scene07_Theorem3_HardwareBarrier"),
    ("Scene08", "Scene08_EmpiricalBenchmarks"),
    ("Scene09", "Scene09_FrontierLabs"),
    ("Scene10", "Scene10_The10YearFrontier"),
]

TARGET_DURATION = 150.0  # seconds per chapter (4500 frames @ 30fps)


def get_duration(filepath: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(filepath)
    ]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)


def conform_chapter_audio(src_mp3: Path, out_wav: Path):
    """Conforms chapter vocal track to exactly 150.00s with broadcast EQ and limiter."""
    dur = get_duration(src_mp3)
    out_wav.parent.mkdir(parents=True, exist_ok=True)

    if dur < TARGET_DURATION:
        pad_needed = TARGET_DURATION - dur
        audio_filter = (
            f"apad=pad_dur={pad_needed:.3f},"
            "equalizer=f=80:t=q:w=1.0:g=-3.0,"  # cut sub-rumble
            "equalizer=f=3200:t=q:w=1.2:g=1.8,"  # vocal clarity boost
            "alimiter=limit=0.95"
        )
    else:
        tempo = dur / TARGET_DURATION
        audio_filter = (
            f"atempo={tempo:.4f},"
            "equalizer=f=80:t=q:w=1.0:g=-3.0,"
            "equalizer=f=3200:t=q:w=1.2:g=1.8,"
            "alimiter=limit=0.95"
        )

    cmd = [
        "ffmpeg", "-y", "-i", str(src_mp3),
        "-af", audio_filter,
        "-t", f"{TARGET_DURATION:.3f}",
        "-ar", "48000", "-ac", "2",
        str(out_wav)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_full_soundtrack(voice_type: str, scene_wavs: list, out_full_wav: Path):
    """
    Concatenates 10 conformed chapters (1500.00s) and mixes continuous ambient bed
    with EBU R128 broadcast normalization (-16.0 LUFS, -1.5 dBFS true peak).
    """
    print(f"\nBuilding full 25-minute soundtrack for [{voice_type}]...")
    concat_list_path = OUTPUT_DIR / f"concat_{voice_type}.txt"
    with open(concat_list_path, "w") as f:
        for p in scene_wavs:
            f.write(f"file '{p.resolve()}'\n")

    vocal_concat_wav = OUTPUT_DIR / f"vocals_concat_{voice_type}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(vocal_concat_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    vocal_dur = get_duration(vocal_concat_wav)
    print(f"  Vocal stream duration: {vocal_dur:.2f}s")

    # Mix with continuous ambient bed & apply broadcast loudnorm
    # Ambient bed volume 0.032 sits tastefully beneath vocals
    filter_complex = (
        "[0:a]volume=1.0[vocal];"
        "[1:a]volume=0.032[bed];"
        "[vocal][bed]amix=inputs=2:duration=first:dropout_transition=2,"
        "loudnorm=I=-16.0:TP=-1.5:LRA=10.0[master]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(vocal_concat_wav),
        "-stream_loop", "-1", "-i", str(AMBIENT_BED),
        "-filter_complex", filter_complex,
        "-map", "[master]",
        "-t", f"{vocal_dur:.3f}",
        "-ar", "48000", "-ac", "2",
        str(out_full_wav)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    concat_list_path.unlink(missing_ok=True)
    vocal_concat_wav.unlink(missing_ok=True)
    print(f"  Full soundtrack exported: {out_full_wav} ({get_duration(out_full_wav):.2f}s)")


def mux_video_with_soundtrack(video_src: Path, audio_src: Path, video_out: Path):
    """Muxes the high-fidelity video track with the master soundtrack."""
    print(f"\nMuxing final master video: {video_out.name} ...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_src),
        "-i", str(audio_src),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "320k",
        "-movflags", "+faststart",
        str(video_out)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  Master video generated: {video_out}")


def main():
    print("=" * 70)
    print("MASTERCLASS DUAL-SOUNDTRACK PRODUCTION & VIDEO PIPELINE")
    print("=" * 70)

    PUBLIC_CLONED_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_STANDARD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Process Cloned Voice Chapters
    cloned_wavs = []
    print("\n--- Conforming Set 1: Cloned Voice (User Voice) ---")
    for short_key, full_name in SCENES:
        src = CLONED_SRC_DIR / f"{short_key}.mp3"
        out_cloned = PUBLIC_CLONED_DIR / f"{full_name}_cloned.wav"
        out_natural = PUBLIC_NATURAL_DIR / f"{full_name}_natural.wav"
        conform_chapter_audio(src, out_cloned)
        shutil.copyfile(out_cloned, out_natural)
        cloned_wavs.append(out_cloned)
        print(f"  {short_key} conformed -> {out_cloned.name} ({get_duration(out_cloned):.2f}s)")

    # 2. Process Standard Voice Chapters
    standard_wavs = []
    print("\n--- Conforming Set 2: Standard Voice (Studio Deep Male) ---")
    for short_key, full_name in SCENES:
        src = STANDARD_SRC_DIR / f"{short_key}.mp3"
        out_std = PUBLIC_STANDARD_DIR / f"{full_name}_standard.wav"
        conform_chapter_audio(src, out_std)
        standard_wavs.append(out_std)
        print(f"  {short_key} conformed -> {out_std.name} ({get_duration(out_std):.2f}s)")

    # 3. Build Full 25-Minute Master Soundtracks
    cloned_soundtrack = OUTPUT_DIR / "masterclass_25min_cloned_soundtrack.wav"
    build_full_soundtrack("cloned", cloned_wavs, cloned_soundtrack)

    standard_soundtrack = OUTPUT_DIR / "masterclass_25min_standard_soundtrack.wav"
    build_full_soundtrack("standard", standard_wavs, standard_soundtrack)

    # 4. Multiplex Videos
    source_video = OUTPUT_DIR / "masterclass_25min_complete.mp4"
    if not source_video.exists():
        print(f"Error: Base video {source_video} not found!")
        sys.exit(1)

    # Video 1: Cloned Voice
    video_cloned_1 = OUTPUT_DIR / "Why_Brain-Like_AI_Failed_Cloned_Voice.mp4"
    video_cloned_2 = OUTPUT_DIR / "masterclass_25min_cloned.mp4"
    mux_video_with_soundtrack(source_video, cloned_soundtrack, video_cloned_1)
    shutil.copyfile(video_cloned_1, video_cloned_2)

    # Video 2: Standard Voice
    video_std_1 = OUTPUT_DIR / "Why_Brain-Like_AI_Failed_Standard_Voice.mp4"
    video_std_2 = OUTPUT_DIR / "masterclass_25min_standard.mp4"
    mux_video_with_soundtrack(source_video, standard_soundtrack, video_std_1)
    shutil.copyfile(video_std_1, video_std_2)

    print("\n" + "=" * 70)
    print("PRODUCTION COMPLETE: BOTH MASTERCLASS VIDEOS GENERATED")
    print("=" * 70)
    print(f"1. Cloned Voice:   {video_cloned_1} ({video_cloned_1.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"2. Standard Voice: {video_std_1} ({video_std_1.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
