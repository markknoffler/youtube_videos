# Voice V3 — diagnosis, research, and fixes

## What was wrong in V2 (measured on the delivered audio, 367 phrases per voice)

| Symptom | Measurement | Cause |
|---|---|---|
| Standard voice suddenly sounds female, often at chapter/paragraph starts | phrases tagged `pitch_high`: **+8.5 st** (cloned +6.8 st); chapter-first phrases up to +10.5 st; worst phrases ~315 Hz vs a 128 Hz voice | my direction file put pitch tags on 94 phrases, mostly paragraph/chapter openers |
| Same effect from emotion tags | `confusion` +11.7/+14.7 st, `elation` +14.7/+9.7, `surprise` +5.1/+12.2, `determination` +3.6, `enthusiasm` +2.8 | the model maps these emotions to a much higher register |
| Identity collapses with the jump | ECAPA similarity to the voice: 0.84 (|Δpitch| < 1 st) → 0.67 (3–6 st) → **0.46 (> 6 st)** | speaker identity is carried by pitch *and* formants; both move |
| Clone has hiss/"shhh", noise comes and goes | raw recording noise floor −21.7 dB; HF bursts across 4–12 kHz on every word; generated clone copied it, plus buzzing bands at 6–11 kHz in some phrases; gaps between phrases were near-digital silence | noisy mic recording → noisy clone prompt → noise transferred into speech; per-phrase noise vs silent gaps made it pump |

## Research used (all downloaded to papers/voice and papers/tts, parsed from the repo)
* Wang et al. 2024, *Noise robustness of flow-matching zero-shot TTS* (arXiv 2406.05699): noise in the audio prompt is **transferred into the generated speech**; speech-enhancement of the prompt raises quality (DNSMOS 3.01→3.28) but processing artifacts can hurt speaker characteristics → denoise moderately and verify identity.
* Schröter et al., *DeepFilterNet* (arXiv 2110.05588, 2305.08227): low-complexity full-band speech enhancement via deep filtering; used here for the clone reference and the clone chapters.
* Desplanques et al., *ECAPA-TDNN* (arXiv 2005.07143): the speaker-verification embedding used as the per-phrase identity gate.
* Kuwabara (Eurospeech 2003), voice individuality: individuality is far more sensitive to formant shifts than to F0 changes → a pitch tag that also moves formants changes *who* is speaking.
* Earlier: Farrús et al. 2016 (paragraph prosody), Trouvain 2002 (tempo), Carlson 2006 (hesitation lengthening), Fish S2 and dots.tts reports.

## Fixes
1. **No pitch tags** (all 94 removed). Intonation inside a phrase is left to the model; natural variation is a few semitones.
2. **Emotion remap** for the high-pitch emotions (`MAP` in generate_v3.py) so expression comes from pace, emphasis, pauses.
3. **Per-phrase gates** (generate_v3.py + qa_gate_server.py): ASR text match, median-F0 drift ≤ 2.2 st from the voice's target (clone 120 Hz, standard 128 Hz), F0 range ≤ 10 st inside the phrase, ECAPA similarity ≥ 0.62 (clone) / 0.70 (standard). Failed phrases are regenerated with other seeds, cooler sampling, then fewer tags; older cached phrases are re-gated.
4. **Clean clone reference** (`voice_ref/user_ref_clean.wav`): DeepFilterNet on the whole recording, steep 8.8 kHz low-pass, de-esser; identity vs the original recording 0.895 (old clip 0.863).
5. **Uniform mastering** (`postprocess.py`): whole-chapter DeepFilterNet (clone only), 9 kHz low-pass, de-esser, one continuous −66 dBFS room-tone bed, −16 LUFS. On a test chapter: noise floor −37 → −55 dB with identity unchanged (0.804 → 0.809).
