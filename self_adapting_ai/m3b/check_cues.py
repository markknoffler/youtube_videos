"""Resolve every chapter's cue list in both voices; print weak or suspicious matches."""
import re, ast, sys, difflib
_argv = sys.argv[:] ; sys.argv = ["x"]
import common
from common import Timeline, _norm
for ch in range(1, 13):
    src = open(f"ch{ch:02d}.py").read()
    m = re.search(r"self\.times\((.*?)\)\n", src, re.S)
    phrases = ast.literal_eval("(" + m.group(1) + ",)")
    for v in _argv[1:] or ("standard", "cloned"):
        tl = Timeline(v, ch)
        prev = 0
        for p in phrases:
            try:
                t = tl.find(p)
                i = tl.cursor
                n = len(p.split())
                got = " ".join(w["w"] for w in tl.words[i:i + n])
                r = difflib.SequenceMatcher(None, "".join(_norm(x) for x in p.replace("-"," ").split()), "".join(tl.toks[i:i + n])).ratio()
                flag = "  <-- WEAK" if r < 0.8 else ""
                if t - prev > 25: flag += "  <-- GAP"
                if flag: print(f"ch{ch} {v} {p!r} -> {got!r} @{t:.1f} r={r:.2f}{flag}")
                prev = t
            except ValueError:
                print(f"ch{ch} {v} {p!r} MISSING")
