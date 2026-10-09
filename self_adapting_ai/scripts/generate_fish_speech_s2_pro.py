#!/usr/bin/env python3
"""
Generate realistic studio-grade voiceovers for all 10 chapters of the YouTube video
using Fish Audio S2 Pro (4B Dual-AR model) with zero-shot voice cloning of the user's voice.

Dual-GPU Allocation:
- GPU 0 (RTX 4000 Ada - 20GB): 4B Dual-AR Transformer (Fast & Slow AR)
- GPU 1 (RTX 3060 - 12GB): DAC Audio Codec (Encoder & Decoder)

Outputs:
- self_adapting_ai/audio_fish_s2_pro/Scene01.mp3 ... Scene10.mp3
- self_adapting_ai/audio_elevenlabs/Scene01.mp3 ... Scene10.mp3
"""

import os
import sys
import re
import time
import shutil
import subprocess
from pathlib import Path
import numpy as np
import torch

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

PROJECT_ROOT = Path("/home/user/Desktop/Deep_learning_projects/youtube/youtube_videos")
REPO_DIR = PROJECT_ROOT / "youtube_videos"
ENGINE_DIR = PROJECT_ROOT / "fish_speech_engine"
CHECKPOINT_DIR = ENGINE_DIR / "checkpoints" / "s2-pro"
REF_AUDIO_PATH = PROJECT_ROOT / "reference_voice_clean.wav"
SCRIPTS_MD_PATH = REPO_DIR / "self_adapting_ai" / "ELEVENLABS_VOICEOVER_SCRIPTS.md"
TARGET_OUTPUT_DIR = REPO_DIR / "self_adapting_ai" / "audio_fish_s2_pro"
ELEVENLABS_DIR = REPO_DIR / "self_adapting_ai" / "audio_elevenlabs"

# Add fish_speech_engine to path
sys.path.insert(0, str(ENGINE_DIR))

from fish_speech.models.text2semantic.inference import (
    init_model,
    load_codec_model,
    encode_audio,
    decode_to_audio,
    generate_long,
)
import soundfile as sf

REF_TEXT = (
    "The Man with the Golden Gun was written by Ian Fleming, pictured and is the final "
    "novel in the James Bond series. It was published by Jonathan Cape in the United Kingdom "
    "on 1st April 1965."
)


def parse_scripts(md_path: Path):
    content = md_path.read_text(encoding="utf-8")
    pattern = r"## CHAPTER (\d+):[^\n]*\n.*?```text\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)
    chapters = {}
    for num_str, text in matches:
        ch_num = int(num_str)
        chapters[ch_num] = text.strip()
    return chapters


def convert_wav_to_mp3(wav_path: Path, mp3_path: Path):
    cmd = [
        "ffmpeg", "-y", "-i", str(wav_path),
        "-codec:a", "libmp3lame", "-b:a", "192k",
        str(mp3_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def is_valid_audio(audio_path: Path, min_duration: float = 30.0) -> bool:
    if not audio_path.exists() or audio_path.stat().st_size < 10000:
        return False
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ]
        out = subprocess.check_output(cmd).decode().strip()
        dur = float(out)
        return dur >= min_duration
    except Exception:
        return False


def main():
    print("=" * 70)
    print("FISH AUDIO S2 PRO (4B DUAL-AR) DUAL-GPU VOICE GENERATION PIPELINE")
    print("=" * 70)
    device_model = "cuda:0"
    device_codec = "cuda:1"
    precision = torch.bfloat16

    print(f"Model GPU:  {device_model} ({torch.cuda.get_device_name(0)})")
    print(f"Codec GPU:  {device_codec} ({torch.cuda.get_device_name(1)})")
    print(f"Checkpoint: {CHECKPOINT_DIR}")
    print(f"Output Dir: {TARGET_OUTPUT_DIR}")
    print(f"ElevenLabs: {ELEVENLABS_DIR}")
    print("=" * 70)

    TARGET_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ELEVENLABS_DIR.mkdir(parents=True, exist_ok=True)

    chapters = parse_scripts(SCRIPTS_MD_PATH)
    print(f"Parsed {len(chapters)} chapters from {SCRIPTS_MD_PATH.name}")

    # Check which chapters need generation
    todo = []
    for ch_num in sorted(chapters.keys()):
        scene_name = f"Scene{ch_num:02d}.mp3"
        target_file = TARGET_OUTPUT_DIR / scene_name
        if is_valid_audio(target_file):
            print(f"[✓] {scene_name} already exists and is valid. Skipping.")
        else:
            todo.append(ch_num)

    if not todo:
        print("\nAll 10 chapters are already generated!")
        return

    print(f"\nChapters to generate: {todo}")

    print("\n[1/3] Loading Fish Audio S2 Pro Dual-AR Transformer (4B params) on GPU 0...")
    t0 = time.time()
    model, decode_one_token = init_model(CHECKPOINT_DIR, device_model, precision, compile=False)
    
    # Optimize KV Cache memory footprint to 4096 tokens (prevents CUDA OOM)
    model.config.max_seq_len = 4096
    with torch.device(device_model):
        model.setup_caches(max_batch_size=1, max_seq_len=4096, dtype=next(model.parameters()).dtype)
    model._cache_setup_done = True
    print(f"      Model loaded in {time.time() - t0:.2f}s (GPU 0 Memory: {torch.cuda.memory_allocated(0)/(1024**3):.2f} GB)")

    print("[2/3] Loading DAC Codec on GPU 1...")
    codec = load_codec_model(CHECKPOINT_DIR / "codec.pth", device_codec, precision)
    print(f"      Codec loaded! (GPU 1 Memory: {torch.cuda.memory_allocated(1)/(1024**3):.2f} GB)")

    print(f"[3/3] Encoding reference voice from {REF_AUDIO_PATH.name} on GPU 1...")
    prompt_tokens = encode_audio(REF_AUDIO_PATH, codec, device_codec).cpu()
    print(f"      Reference prompt tokens encoded: shape {prompt_tokens.shape}")

    silence_pause = np.zeros(int(0.35 * codec.sample_rate), dtype=np.float32)
    overall_start = time.time()

    for ch_num in todo:
        scene_id = f"Scene{ch_num:02d}"
        ch_text = chapters[ch_num]
        paragraphs = [p.strip() for p in ch_text.split("\n\n") if p.strip()]
        total_words = sum(len(p.split()) for p in paragraphs)

        print("\n" + "-" * 70)
        print(f"GENERATING {scene_id} ({len(paragraphs)} paragraphs, {total_words} words)")
        print("-" * 70)

        chapter_audio_parts = []
        ch_start = time.time()

        for p_idx, para in enumerate(paragraphs, 1):
            p_words = len(para.split())
            p_t0 = time.time()

            generator = generate_long(
                model=model,
                device=device_model,
                decode_one_token=decode_one_token,
                text=para,
                num_samples=1,
                max_new_tokens=1024,
                top_p=0.8,
                top_k=30,
                temperature=0.7,
                compile=False,
                iterative_prompt=True,
                chunk_length=300,
                prompt_text=[REF_TEXT],
                prompt_tokens=[prompt_tokens],
            )

            codes = []
            for resp in generator:
                if resp.action == "sample":
                    codes.append(resp.codes)
                elif resp.action == "next":
                    if codes:
                        merged = torch.cat(codes, dim=1)
                        # Decode on GPU 1 where codec lives
                        p_audio = decode_to_audio(merged.to(device_codec), codec)
                        p_wav = p_audio.cpu().float().numpy()
                        chapter_audio_parts.append(p_wav)
                        # Add natural pause between paragraphs
                        if p_idx < len(paragraphs):
                            chapter_audio_parts.append(silence_pause)
                        dur = len(p_wav) / codec.sample_rate
                        gen_t = time.time() - p_t0
                        print(f"  [{p_idx:02d}/{len(paragraphs):02d}] {p_words:2d} words -> {dur:.2f}s audio (in {gen_t:.2f}s)")
                        del merged, p_audio
                    codes = []

            # Clear cache between paragraphs to prevent memory accumulation
            torch.cuda.empty_cache()

        # Combine all audio pieces
        full_ch_wav = np.concatenate(chapter_audio_parts)
        ch_dur = len(full_ch_wav) / codec.sample_rate

        # Temporary WAV file
        temp_wav = TARGET_OUTPUT_DIR / f"{scene_id}_temp.wav"
        sf.write(temp_wav, full_ch_wav, codec.sample_rate)

        # Convert to high-fidelity MP3
        out_mp3 = TARGET_OUTPUT_DIR / f"{scene_id}.mp3"
        convert_wav_to_mp3(temp_wav, out_mp3)

        # Mirror to audio_elevenlabs
        mirror_mp3 = ELEVENLABS_DIR / f"{scene_id}.mp3"
        shutil.copy2(out_mp3, mirror_mp3)

        # Clean up temp wav
        if temp_wav.exists():
            temp_wav.unlink()

        ch_elapsed = time.time() - ch_start
        file_size_mb = out_mp3.stat().st_size / (1024 * 1024)
        print(f"\n[DONE] {scene_id}.mp3 successfully generated!")
        print(f"       Duration: {ch_dur:.2f}s ({ch_dur/60:.2f} min)")
        print(f"       File Size: {file_size_mb:.2f} MB")
        print(f"       Time taken: {ch_elapsed:.1f}s (Speedup: {ch_dur/ch_elapsed:.2f}x realtime)")

    total_time = time.time() - overall_start
    print("\n" + "=" * 70)
    print("ALL REQUESTED CHAPTERS GENERATION COMPLETE!")
    print(f"Total processing time: {total_time/60:.2f} minutes")
    print("=" * 70)

    # Verification report
    print("\n--- FINAL VERIFICATION TABLE ---")
    for ch_num in range(1, 11):
        f = TARGET_OUTPUT_DIR / f"Scene{ch_num:02d}.mp3"
        if f.exists():
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(f)]
            dur = float(subprocess.check_output(cmd).decode().strip())
            sz = f.stat().st_size / (1024 * 1024)
            print(f"Scene{ch_num:02d}.mp3: {dur:.2f}s | {sz:.2f} MB | {f}")
        else:
            print(f"Scene{ch_num:02d}.mp3: MISSING")


if __name__ == "__main__":
    main()
