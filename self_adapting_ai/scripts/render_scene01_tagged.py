#!/usr/bin/env python3
"""
Render Scene 01 with Fine-Grained Human Voice Tags (Fish Audio S2 Pro - 4B Dual-AR).
Generates two sets with emotional prosody, breath intakes, and realistic cadence:
1. Cloned Voice: Zero-shot clone with user's voice prompt + inline tags.
2. Standard Voice: Native Fish Audio S2 Pro studio narrator + inline tags.

Strictly runs Scene 01 on GPU 0 with CPU codec.
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
import soundfile as sf
import torch

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

PROJECT_ROOT = Path("/home/user/Desktop/Deep_learning_projects/youtube/youtube_videos")
REPO_DIR = PROJECT_ROOT / "youtube_videos"
ENGINE_DIR = PROJECT_ROOT / "fish_speech_engine"
CHECKPOINT_DIR = ENGINE_DIR / "checkpoints" / "s2-pro"
REF_AUDIO_PATH = PROJECT_ROOT / "reference_voice_clean.wav"

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

# Richly annotated Scene 01 text with fine-grained voice tags:
# - [inhale] for human breath intakes before sentences
# - [short pause] after commas, colons, and clauses (0.15s - 0.25s)
# - [pause] after periods and thought transitions (0.5s - 0.8s)
# - [emphasis] for conceptual keywords
# - [thoughtful tone], [serious tone], [low voice], [sigh] for dramatic narrative depth
TAGGED_PARAGRAPHS = [
    (
        "[inhale] Welcome to this technical masterclass. [pause] "
        "Look around at the current frontier of artificial intelligence: [short pause] "
        "OpenAI's GPT-6 Astra, [short pause] Anthropic's Claude 5.5, [short pause] "
        "Google DeepMind's Gemini 4, [short pause] and Mythos. [pause]"
    ),
    (
        "[inhale] Across every benchmark in mathematical reasoning, [short pause] "
        "software synthesis, [short pause] and multi-turn dialogue, [short pause] "
        "these systems exhibit remarkable cognitive capabilities. [pause] "
        "[thoughtful tone] Yet behind the dazzling demonstrations lies a profound [short pause] "
        "and unsettling architectural truth. [pause]"
    ),
    (
        "[serious tone] [inhale] Every single foundational model in production today [short pause] "
        "is a [emphasis] frozen, [short pause] static monolith of computation. [pause]"
    ),
    (
        "[inhale] Consider the computational lifecycle of a modern language model. [pause] "
        "Over several months of pre-training, [short pause] "
        "clusters of tens of thousands of GPUs consume millions of kilowatt hours [short pause] "
        "to optimize hundreds of billions of numerical parameters [short pause] "
        "across trillions of tokens. [pause]"
    ),
    (
        "[inhale] During this training epoch, [short pause] "
        "the system learns by updating its numerical weights through stochastic gradient descent. [pause] "
        "[thoughtful tone] But the exact instant that training completes, [short pause] "
        "the learning process halts forever. [pause]"
    ),
    (
        "[low voice] [inhale] The neural weights are etched into silicon [short pause] "
        "like ancient stone monuments. [pause] "
        "When you query the model at inference time, [short pause] "
        "whether you ask it to compose a simple haiku [short pause] "
        "or prove a subtle theorem in algebraic geometry, [short pause] "
        "[emphasis] not a single synapse moves. [pause]"
    ),
    (
        "[sigh] [short pause] No new connections form. [pause] "
        "No outdated pathways dissolve. [pause] "
        "[serious tone] The network cannot dynamically reallocate its internal routing topology [short pause] "
        "to adapt to the complexity of your request. [pause]"
    ),
    (
        "[inhale] In our live terminal, [short pause] examine the attention implementation. [pause] "
        "The projection weights—[short pause] W Q, [short pause] W K, [short pause] and W V—[short pause] "
        "are loaded into GPU high-bandwidth memory as fixed FP16 tensors. [pause] "
        "Every single incoming token vector [short pause] is multiplied against these identical, [short pause] "
        "immutable arrays. [pause]"
    ),
    (
        "[inhale] While activations change dynamically from token to token, [short pause] "
        "the underlying parametric landscape [short pause] is completely rigid and invariant. [pause]"
    ),
    (
        "[thoughtful tone] [inhale] Why has the entire multi-billion dollar enterprise of artificial intelligence [short pause] "
        "consolidated around this rigid, [short pause] unyielding architectural paradigm? [pause] "
        "In this investigation, [short pause] we explore the deep mathematical, [short pause] "
        "physical, [short pause] and hardware forces that created the modern AI monolith... [pause] "
        "and why the tantalizing dream of truly self-adapting intelligence [short pause] "
        "has proven so fiercely difficult [short pause] to realize in physical silicon. [pause]"
    ),
]


def convert_wav_to_mp3(wav_path: Path, mp3_path: Path):
    cmd = [
        "ffmpeg", "-y", "-i", str(wav_path),
        "-codec:a", "libmp3lame", "-b:a", "192k",
        str(mp3_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def generate_scene01(model, decode_one_token, codec, device_model, mode, prompt_tokens=None):
    out_dir = CLONED_OUTPUT_DIR if mode == "cloned" else STANDARD_OUTPUT_DIR
    out_mp3 = out_dir / "Scene01.mp3"
    temp_wav = out_dir / "Scene01_tagged_temp.wav"

    tagged_text = "\n".join(f"<|speaker:0|> {p}" for p in TAGGED_PARAGRAPHS)

    print("\n" + "=" * 70)
    print(f"GENERATING SCENE 01 [{mode.upper()} VOICE WITH FINE-GRAINED HUMAN TAGS]")
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
        chunk_length=400,
        prompt_text=prompt_text_arg,
        prompt_tokens=prompt_tokens_arg,
    )

    all_codes = []
    chunk_idx = 0
    for resp in generator:
        if resp.action == "sample":
            all_codes.append(resp.codes)
            chunk_idx += 1
            print(f"  [Chunk {chunk_idx:02d}] Generated VQ Codes: {resp.codes.shape}")
        elif resp.action == "next":
            if all_codes:
                merged = torch.cat(all_codes, dim=1)
                print(f"\n  Decoding full chapter VQ codes: {merged.shape} on CPU...")
                dec_t0 = time.time()
                waveform = decode_to_audio(merged.to("cpu"), codec)
                print(f"  Decoded in {time.time() - dec_t0:.2f}s")

                audio_np = waveform.cpu().float().numpy()
                sf.write(temp_wav, audio_np, codec.sample_rate)
                convert_wav_to_mp3(temp_wav, out_mp3)

                if temp_wav.exists():
                    temp_wav.unlink()

                # Mirror cloned version to pipeline targets
                if mode == "cloned":
                    shutil.copy2(out_mp3, ELEVENLABS_DIR / "Scene01.mp3")
                    shutil.copy2(out_mp3, FISH_S2_PRO_DIR / "Scene01.mp3")

                dur = len(audio_np) / codec.sample_rate
                elapsed = time.time() - t0
                sz = out_mp3.stat().st_size / (1024 * 1024)
                print(f"[✓] Scene01.mp3 ({mode}) successfully synthesized!")
                print(f"    Duration:  {dur:.2f}s ({dur/60:.2f} min)")
                print(f"    File Size: {sz:.2f} MB")
                print(f"    Time:      {elapsed:.1f}s ({elapsed/60:.2f} min)")
            all_codes = []

    torch.cuda.empty_cache()


def main():
    device_model = "cuda:0"
    print("=" * 70)
    print("HUMAN VOICE-TAGGED SCENE 01 SYNTHESIS (FISH AUDIO S2 PRO)")
    print(f"Device: {device_model} ({torch.cuda.get_device_name(0)})")
    print("=" * 70)

    CLONED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STANDARD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ELEVENLABS_DIR.mkdir(parents=True, exist_ok=True)
    FISH_S2_PRO_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[1/3] Loading Fish Audio S2 Pro Dual-AR (4B params) on GPU 0...")
    t0 = time.time()
    model, decode_one_token = init_model(CHECKPOINT_DIR, device_model, torch.bfloat16, compile=False)
    model.config.max_seq_len = 8192
    with torch.device(device_model):
        model.setup_caches(max_batch_size=1, max_seq_len=8192, dtype=next(model.parameters()).dtype)
    model._cache_setup_done = True
    print(f"      Model ready in {time.time() - t0:.2f}s | GPU 0 Allocated: {torch.cuda.memory_allocated(0)/(1024**3):.2f} GB")

    print("\n[2/3] Loading DAC Codec on CPU...")
    codec = load_codec_model(CHECKPOINT_DIR / "codec.pth", "cpu", torch.float32)
    print(f"      Codec ready on CPU (Sample rate: {codec.sample_rate} Hz)")

    print(f"\n[3/3] Encoding reference prompt from {REF_AUDIO_PATH.name} on CPU...")
    prompt_tokens = encode_audio(REF_AUDIO_PATH, codec, "cpu").cpu()
    print(f"      Prompt tokens encoded: {prompt_tokens.shape}")

    # Generate Set 1: Cloned Voice
    generate_scene01(model, decode_one_token, codec, device_model, mode="cloned", prompt_tokens=prompt_tokens)

    # Generate Set 2: Standard Studio Voice
    generate_scene01(model, decode_one_token, codec, device_model, mode="standard", prompt_tokens=None)

    print("\n" + "=" * 70)
    print("SCENE 01 DUAL-SET GENERATION COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
