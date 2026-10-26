#!/usr/bin/env python3
"""Build VOICE_DIRECTION_V3.md from V2 by merging stubborn short fragments into neighbouring phrases.
A merged phrase keeps the tags of its LONGER part and the pause class of its LAST part.
The concatenated text is unchanged, so direction.py validation against the script still passes."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from direction import direction_chapters, SA

# (chapter, first index, last index) — consecutive phrases to speak as ONE phrase
MERGES = [(9, 4, 5), (9, 6, 7), (10, 4, 5), (10, 14, 15), (10, 17, 18), (10, 26, 27), (10, 35, 36),
          (11, 5, 6), (11, 16, 18), (11, 29, 30), (11, 33, 34), (11, 35, 36)]


def fmt(seg):
    tags = " ".join(f"{k}={seg[k]}" for k in ("e", "s", "x") if seg.get(k))
    nv = f"<{seg['nv']}> " if seg.get("nv") else ""
    return f"{nv}{'[' + tags + '] ' if tags else ''}{seg['text']}" + (" " + "/" * seg["pause"] if seg["pause"] else "")


D = direction_chapters(os.path.join(SA, "VOICE_DIRECTION_V2.md"))
src = open(os.path.join(SA, "VOICE_DIRECTION_V2.md"), encoding="utf-8").read()
out = src
for ch, segs in D.items():
    skip, lines = set(), []
    for a, b, c in [(m[1], m[1], m[2]) for m in MERGES if m[0] == ch]:
        parts = segs[a:c + 1]
        longest = max(parts, key=lambda p: len(p["text"]))
        merged = dict(longest, text=" ".join(p["text"] for p in parts), pause=parts[-1]["pause"], nv=parts[0].get("nv"))
        lines.append((a, c, merged))
    i, new = 0, []
    while i < len(segs):
        hit = next((m for m in lines if m[0] == i), None)
        if hit:
            new.append(fmt(hit[2])); i = hit[1] + 1
        else:
            new.append(fmt(segs[i])); i += 1
    block = re.search(rf"^## CH{ch:02d}\n(.*?)(?=^## CH|\Z)", out, re.S | re.M)
    out = out[:block.start(1)] + "\n".join(new) + "\n\n" + out[block.end(1):]
open(os.path.join(SA, "VOICE_DIRECTION_V3.md"), "w", encoding="utf-8").write(out)
n2 = direction_chapters(os.path.join(SA, "VOICE_DIRECTION_V3.md"))
print("phrases per chapter V2→V3:", {c: (len(D[c]), len(n2[c])) for c in D if len(D[c]) != len(n2[c])})
