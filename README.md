# YouTube Videos: The AI Pedagogical Masterclass Series

This repository contains the complete production pipeline, 3D blackboard animation code, mathematical models, experimental benchmarks, and narration scripts for technical video masterclasses.

---

## Featured Video: Why Brain-Like AI Failed (And What We Built Instead)

**The Modular Emergence Paradox** — A 25:00.00 continuous 3D pedagogical masterclass explaining why biological plasticity (Hebbian learning, self-organizing maps, dynamic synaptic rewiring) failed to produce modern artificial intelligence, and why the "frozen" Transformer monolith won in physical silicon.

### Video Specifications
- **Runtime:** 25:00.00 (45,000 frames @ 30 FPS)
- **Resolution:** 1280 × 720 (16:9 widescreen)
- **Renderer:** Remotion + Three.js / React Three Fiber + 3D Mathematical Blackboard
- **Audio:** 10 chapters mastered to exactly 150.00s each

---

## Repository Structure

```
youtube_videos/
├── README.md                           # Master repository documentation
├── .gitignore                          # Git exclusions (large videos, caches, node_modules)
└── self_adapting_ai/                   # Masterclass project workspace
    ├── ELEVENLABS_VOICEOVER_SCRIPTS.md # Complete chapter-by-chapter ElevenLabs scripts
    ├── render_masterclass.sh           # Automated 10-chapter render & concat pipeline
    ├── remotion_studio/                # Remotion video generation framework
    │   ├── src/
    │   │   ├── Root.tsx                # Remotion root configuration
    │   │   ├── components/             # 3D blackboard components & HUD overlays
    │   │   │   ├── Scene01_MonolithBlackboard.tsx
    │   │   │   ├── HolographicAssetWindow.tsx
    │   │   │   ├── CyberSubtitles.tsx
    │   │   │   └── ...
    │   │   ├── data/
    │   │   │   └── subtitles.json      # Sentence-synchronized subtitle timestamps
    │   │   └── scenes/
    │   │       └── MasterScenes.tsx    # 10 chapter composition wrappers
    │   └── public/
    │       ├── assets/real_world/      # ArXiv papers, researcher portraits, logos
    │       └── audio_natural/          # Mastered chapter soundtracks (150.00s each)
    ├── scripts/
    │   ├── masterclass_text.py         # 10-chapter technical narration script
    │   ├── generate_neural_speech.py   # Edge-TTS documentary narration pipeline
    │   ├── generate_all_subtitles.py   # Sentence boundary extraction
    │   ├── ingest_elevenlabs_audio.py  # Conformance pipeline for external voiceovers
    │   └── ...
    ├── audio_elevenlabs/               # Drop folder for ElevenLabs audio files
    ├── papers/                         # Landmark ArXiv research papers referenced
    └── output/                         # Rendered masterclass video output
```

---

## Quick Start & Reproduction

### 1. Install Dependencies
```bash
cd self_adapting_ai/remotion_studio
npm install
```

### 2. Preview in Remotion Studio
```bash
npx remotion studio
```
Open [http://localhost:3000](http://localhost:3000) in your browser to inspect and interact with the 3D blackboards across all 10 chapters.

### 3. Render the Complete Masterclass
```bash
cd self_adapting_ai
./render_masterclass.sh
```
This builds the bundle, renders all 10 chapters at 8x concurrency, stitches them losslessly via FFmpeg, and verifies output metadata into `output/masterclass_25min_complete.mp4`.

---

## The 10 Masterclass Chapters

1. **Chapter 01: The Monolith of Modern AI** — The frozen parametric landscape from GPT-6 Astra to Gemini 4.
2. **Chapter 02: The Biological Dream** — 86 billion neurons, 20 watts, and living synaptic plasticity.
3. **Chapter 03: The Self-Organizing Hypothesis** — Hebb, Oja, Kohonen, and the bottom-up wiring dream.
4. **Chapter 04: The Modular Emergence Paradox** — Why living graphs collapsed while rigid monoliths discovered modular induction heads.
5. **Chapter 05: Theorem 1: Rank Collapse & The Oja Trap** — Lyapunov spectral decay and the eigenvalue trap of local plasticity.
6. **Chapter 06: Theorem 2: Routing Expressivity & Graph Latency** — The Moore Bound, logarithmic graph diameters, and gradient decay.
7. **Chapter 07: Theorem 3: The Hardware Lottery & Credit Assignment** — Dense systolic GEMM tensor cores versus irregular pointer thrashing.
8. **Chapter 08: Empirical Proof: The Live Diagnostic Benchmark** — Pitting dynamic rewiring against modular Transformers in PyTorch.
9. **Chapter 09: What Frontier Labs Discovered** — Multi-Head Latent Attention (MLA) and fine-grained MoE routing.
10. **Chapter 10: The 10-Year Frontier** — Fast weights, test-time training (TTT), liquid neural ODEs, and neuromorphic silicon.
