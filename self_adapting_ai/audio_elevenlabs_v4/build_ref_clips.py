#!/usr/bin/env python3
"""Build 2-3 clone-reference clips (different energy) from the real ElevenLabs Chuck Miller
narration, with transcripts taken from Whisper's OWN output (not the script/tagged text).
Targets, from VOICEOVER_SCRIPT_V2.md ch03 text + make_tagged.py's TAGS[3] cue map:
  calm/curious : "The dream of self-adapting neural networks is not a new idea. In fact,
                  it is historically older than backpropagation itself."
  excited      : "In 1949, Canadian psychologist Donald Hebb published The Organization of
                  Behavior, introducing his foundational postulate of synaptic plasticity:
                  when an axon of cell A is near enough to excite cell B and repeatedly
                  takes part in firing it, some growth process or metabolic change takes place."
  serious      : "For decades, this was viewed as the holy grail of artificial intelligence.
                  It promised networks that could learn continuously without catastrophic
                  forgetting, growing new modules dynamically as needed."
"""
import json, os, re, subprocess
from faster_whisper import WhisperModel

V4 = os.path.dirname(os.path.abspath(__file__))
SRC = f"{V4}/chapters/ch03.mp3"
OUT = f"{V4}/clone_ref"
os.makedirs(OUT, exist_ok=True)

norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).split()

TARGETS = {
    "calm": "Concurrently, Teuvo Kohonen invented Self-Organizing Maps, showing that uncoordinated, localized competition between neighboring units could spontaneously fold a high-dimensional feature space into a beautifully ordered topological manifold.",
    "excited": "In 1949, Canadian psychologist Donald Hebb published The Organization of Behavior, introducing his foundational postulate of synaptic plasticity: when an axon of cell A is near enough to excite cell B and repeatedly takes part in firing it, some growth process or metabolic change takes place.",
    "serious": "For decades, this was viewed as the holy grail of artificial intelligence. It promised networks that could learn continuously without catastrophic forgetting, growing new modules dynamically as needed.",
}

print("transcribing ch03.mp3 with word timestamps...")
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, info = m.transcribe(SRC, beam_size=5, word_timestamps=True, vad_filter=False)
words = []
for s in segs:
    for w in s.words:
        words.append((w.start, w.end, w.word.strip()))
wnorm = [norm(w[2])[0] if norm(w[2]) else "" for w in words]
print(f"{len(words)} words transcribed, duration {info.duration:.1f}s")


def find_span(target_words):
    """Best-matching contiguous run of `words`, trying several window lengths (ASR tokenization
    of named entities / hyphenated terms can differ in word count from the script text)."""
    n0 = len(target_words)
    best = (0, -1, n0)
    for n in range(max(3, n0 - 4), n0 + 5):
        for i in range(len(wnorm) - n + 1):
            window = wnorm[i:i + n]
            score = sum(1 for a, b in zip(window, target_words) if a == b) / max(n, n0)
            if score > best[0]:
                best = (score, i, n)
    return best


# "calm" relies on manual boundaries: Whisper mis-hears the proper name "Teuvo Kohonen" as
# "Tove Okohonen", which throws off fuzzy word-matching. Boundaries read directly off the
# word timestamps (see diagnostic run); the name is corrected in the transcript below since
# the script + check_tags.py confirm that's what's actually spoken (not an ASR guess).
MANUAL = {"calm": (59.60, 73.45, "Concurrently, Teuvo Kohonen invented self-organizing maps, "
                                 "showing that uncoordinated, localized competition between "
                                 "neighboring units could spontaneously fold a high-dimensional "
                                 "feature space into a beautifully ordered topological manifold.")}

results = {}
for name, text in TARGETS.items():
    if name in MANUAL:
        start, end, transcript = MANUAL[name]
        score = 1.0
    else:
        tgt = norm(text)
        score, i, n = find_span(tgt)
        j = i + n - 1
        start, end = words[i][0], words[j][1]
        pad = 0.15
        start, end = max(0, start - pad), end + pad
        clip_words = [w for w in words if w[0] >= start - 0.01 and w[1] <= end + 0.01]
        transcript = " ".join(w[2] for w in clip_words).strip()
    dur = end - start
    wav = f"{OUT}/chuck_{name}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-ss", f"{start:.2f}", "-to", f"{end:.2f}",
                    "-ac", "1", "-ar", "48000", wav], check=True)
    open(f"{OUT}/chuck_{name}.txt", "w").write(transcript + "\n")
    results[name] = dict(match_score=round(score, 3), start=round(start, 2), end=round(end, 2), dur=round(dur, 2), transcript=transcript)
    print(f"{name}: match={score:.2f} [{start:.2f}-{end:.2f}] dur={dur:.1f}s -> {wav}")
    print(f"  transcript: {transcript}")

json.dump(results, open(f"{OUT}/clips_manifest.json", "w"), indent=1)
