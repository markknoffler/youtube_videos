#!/usr/bin/env python3
"""
Fish Audio S2 Pro (4B Dual-AR) Voiceover Generator.
Generates two distinct sets of studio-grade voiceover tracks for all 10 chapters:
1. Cloned Voice: Zero-shot voice clone using the user's reference voice.
   - Outputs: self_adapting_ai/audio_fish_s2_pro_cloned/Scene01.mp3 ... Scene10.mp3
   - Mirrored to: self_adapting_ai/audio_elevenlabs/Scene01.mp3 ... Scene10.mp3
   - Mirrored to: self_adapting_ai/audio_fish_s2_pro/Scene01.mp3 ... Scene10.mp3
2. Standard Voice: Native Fish Audio S2 Pro studio narrator voice (no prompt conditioning).
   - Outputs: self_adapting_ai/audio_fish_s2_pro_standard/Scene01.mp3 ... Scene10.mp3

Architectural Improvements:
- Continuous Multi-Turn Generation: All turns are synthesized in a single generative
  conversation context without inserting artificial digital zero silence.
- Unified Neural Codec Decoding: Autoregressive VQ codes are accumulated across all turns
  and decoded in ONE pass per chapter, preserving continuous breath, acoustic presence,
  and natural pacing with zero 10-second dropoffs.
- GPU 0 Isolation: Strict execution on GPU 0 with KV-cache clamped to 8192 tokens (~10.7 GB VRAM),
  running side-by-side with active training jobs without OOM. Codec runs on CPU (0 MB GPU VRAM).
"""

import os
import sys
import re
import time
import shutil
import argparse
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

CLONED_OUTPUT_DIR = REPO_DIR / "self_adapting_ai" / "audio_fish_s2_pro_cloned"
STANDARD_OUTPUT_DIR = REPO_DIR / "self_adapting_ai" / "audio_fish_s2_pro_standard"
ELEVENLABS_DIR = REPO_DIR / "self_adapting_ai" / "audio_elevenlabs"
FISH_S2_PRO_DIR = REPO_DIR / "self_adapting_ai" / "audio_fish_s2_pro"

REF_TEXT = (
    "The Man with the Golden Gun was written by Ian Fleming, pictured and is the final "
    "novel in the James Bond series. It was published by Jonathan Cape in the United Kingdom "
    "on 1st April 1965."
)

sys.path.insert(0, str(ENGINE_DIR))

from fish_speech.models.text2semantic.inference import (
    init_model,
    load_codec_model,
    encode_audio,
    decode_to_audio,
    generate_long,
)
import soundfile as sf


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


def get_audio_duration(audio_path: Path) -> float:
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ]
        out = subprocess.check_output(cmd).decode().strip()
        return float(out)
    except Exception:
        return 0.0


def generate_scene(
    model,
    decode_one_token,
    codec,
    device_model: str,
    scene_num: int,
    ch_text: str,
    output_dir: Path,
    mode: str,
    prompt_tokens: torch.Tensor = None,
):
    scene_id = f"Scene{scene_num:02d}"
    out_mp3 = output_dir / f"{scene_id}.mp3"
    temp_wav = output_dir / f"{scene_id}_temp.wav"

    paragraphs = [p.strip() for p in ch_text.split("\n\n") if p.strip()]
    total_words = sum(len(p.split()) for p in paragraphs)

    # Format turns with speaker tags for multi-turn autoregressive continuity
    tagged_text = "\n".join(f"<|speaker:0|> {p}" for p in paragraphs)

    print("\n" + "=" * 70)
    print(f"GENERATING [{mode.upper()}] {scene_id} ({len(paragraphs)} paragraphs, {total_words} words)")
    print(f"Target: {out_mp3}")
    print("=" * 70)

    t0 = time.time()

    prompt_text_arg = [REF_TEXT] if (mode == "cloned" and prompt_tokens is not None) else None
    prompt_tokens_arg = [prompt_tokens] if (mode == "cloned" and prompt_tokens is not None) else None

    generator = generate_long(
        model=model,
        device=device_model,
        decode_one_token=decode_one_token,
        text=tagged_text,
        num_samples=1,
        max_new_tokens=1024,
        top_p=0.8,
        top_k=30,
        temperature=0.7,
        compile=False,
        iterative_prompt=True,
        chunk_length=350,
        prompt_text=prompt_text_arg,
        prompt_tokens=prompt_tokens_arg,
    )

    all_codes = []
    chunk_count = 0

    for resp in generator:
        if resp.action == "sample":
            all_codes.append(resp.codes)
            chunk_count += 1
            print(f"  [Chunk {chunk_count:02d}] Synthesized VQ codes: {resp.codes.shape}")
        elif resp.action == "next":
            if all_codes:
                merged_codes = torch.cat(all_codes, dim=1)
                print(f"\n  Decoding full chapter VQ codes: {merged_codes.shape} on CPU...")
                dec_t0 = time.time()
                audio_waveform = decode_to_audio(merged_codes.to("cpu"), codec)
                print(f"  Decoded in {time.time() - dec_t0:.2f}s")

                audio_np = audio_waveform.cpu().float().numpy()
                sf.write(temp_wav, audio_np, codec.sample_rate)
                convert_wav_to_mp3(temp_wav, out_mp3)

                if temp_wav.exists():
                    temp_wav.unlink()

                # Mirror if cloned
                if mode == "cloned":
                    mirror1 = ELEVENLABS_DIR / f"{scene_id}.mp3"
                    shutil.copy2(out_mp3, mirror1)
                    mirror2 = FISH_S2_PRO_DIR / f"{scene_id}.mp3"
                    shutil.copy2(out_mp3, mirror2)

                dur = len(audio_np) / codec.sample_rate
                elapsed = time.time() - t0
                file_mb = out_mp3.stat().st_size / (1024 * 1024)
                print(f"[✓] {scene_id}.mp3 ({mode}) successfully completed!")
                print(f"    Duration:  {dur:.2f}s ({dur/60:.2f} min)")
                print(f"    File Size: {file_mb:.2f} MB")
                print(f"    Time:      {elapsed:.1f}s ({elapsed/60:.2f} min)")
                print(f"    Output:    {out_mp3}")
            all_codes = []

    # Clean cache between scenes
    torch.cuda.empty_cache()


def main():
    parser = argparse.ArgumentParser(description="Generate Fish Audio S2 Pro dual-set voiceovers")
    parser.add_argument(
        "--mode",
        choices=["all", "cloned", "standard"],
        default="all",
        help="Which voice set to generate: cloned, standard, or all (both)"
    )
    parser.add_argument(
        "--scenes",
        type=str,
        default="all",
        help="Comma-separated scene numbers to generate (e.g. '1,2,3' or 'all')"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration even if file exists and is valid"
    )
    args = parser.parse_args()

    device_model = "cuda:0"
    print("=" * 70)
    print("FISH AUDIO S2 PRO DUAL-SET VOICE GENERATION PIPELINE")
    print(f"Mode:    {args.mode.upper()}")
    print(f"Scenes:  {args.scenes}")
    print(f"Device:  {device_model} ({torch.cuda.get_device_name(0)})")
    print("=" * 70)

    CLONED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STANDARD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ELEVENLABS_DIR.mkdir(parents=True, exist_ok=True)
    FISH_S2_PRO_DIR.mkdir(parents=True, exist_ok=True)

    chapters = parse_scripts(SCRIPTS_MD_PATH)
    print(f"Parsed {len(chapters)} chapters from {SCRIPTS_MD_PATH.name}")

    if args.scenes == "all":
        scene_list = sorted(chapters.keys())
    else:
        scene_list = [int(s.strip()) for s in args.scenes.split(",") if s.strip()]

    modes_to_run = []
    if args.mode in ("cloned", "all"):
        modes_to_run.append("cloned")
    if args.mode in ("standard", "all"):
        modes_to_run.append("standard")

    # Load S2-Pro on GPU 0
    print("\n[1/3] Loading Fish Audio S2 Pro Dual-AR (4B params) on GPU 0...")
    t0 = time.time()
    model, decode_one_token = init_model(CHECKPOINT_DIR, device_model, torch.bfloat16, compile=False)
    model.config.max_seq_len = 8192
    with torch.device(device_model):
        model.setup_caches(max_batch_size=1, max_seq_len=8192, dtype=next(model.parameters()).dtype)
    model._cache_setup_done = True
    print(f"      Model ready in {time.time() - t0:.2f}s | GPU 0 Allocated: {torch.cuda.memory_allocated(0)/(1024**3):.2f} GB")

    # Load DAC Codec on CPU
    print("\n[2/3] Loading DAC Codec on CPU...")
    codec = load_codec_model(CHECKPOINT_DIR / "codec.pth", "cpu", torch.float32)
    print(f"      Codec loaded on CPU (Sample rate: {codec.sample_rate} Hz)")

    # Encode reference prompt if cloned mode requested
    prompt_tokens = None
    if "cloned" in modes_to_run:
        print(f"\n[3/3] Encoding reference voice from {REF_AUDIO_PATH.name} on CPU...")
        prompt_tokens = encode_audio(REF_AUDIO_PATH, codec, "cpu").cpu()
        print(f"      Prompt tokens shape: {prompt_tokens.shape}")

    total_pipeline_start = time.time()

    for mode in modes_to_run:
        out_dir = CLONED_OUTPUT_DIR if mode == "cloned" else STANDARD_OUTPUT_DIR
        print("\n" + "#" * 70)
        print(f"STARTING SET: {mode.upper()} VOICE")
        print(f"Target Directory: {out_dir}")
        print("#" * 70)

        for sc in scene_list:
            if sc not in chapters:
                continue
            target_mp3 = out_dir / f"Scene{sc:02d}.mp3"
            if not args.force and is_valid_audio(target_mp3):
                existing_dur = get_audio_duration(target_mp3)
                print(f"[✓] Scene{sc:02d}.mp3 ({mode}) already exists ({existing_dur:.1f}s). Skipping.")
                continue

            generate_scene(
                model=model,
                decode_one_token=decode_one_token,
                codec=codec,
                device_model=device_model,
                scene_num=sc,
                ch_text=chapters[sc],
                output_dir=out_dir,
                mode=mode,
                prompt_tokens=prompt_tokens,
            )

    pipeline_time = time.time() - total_pipeline_start
    print("\n" + "=" * 70)
    print("DUAL-SET GENERATION PIPELINE FINISHED!")
    print(f"Total time elapsed: {pipeline_time/60:.2f} minutes")
    print("=" * 70)

    print("\n--- FINAL VERIFICATION TABLE ---")
    print(f"{'Scene':<10} | {'Cloned (Duration / Size)':<28} | {'Standard (Duration / Size)':<28}")
    print("-" * 72)
    for sc in range(1, 11):
        cf = CLONED_OUTPUT_DIR / f"Scene{sc:02d}.mp3"
        sf_file = STANDARD_OUTPUT_DIR / f"Scene{sc:02d}.mp3"

        c_info = f"{get_audio_duration(cf):.1f}s ({cf.stat().st_size/(1024**2):.1f}MB)" if cf.exists() else "MISSING"
        s_info = f"{get_audio_duration(sf_file):.1f}s ({sf_file.stat().st_size/(1024**2):.1f}MB)" if sf_file.exists() else "MISSING"

        print(f"Scene{sc:02d}    | {c_info:<28} | {s_info:<28}")


if __name__ == "__main__":
    main()
