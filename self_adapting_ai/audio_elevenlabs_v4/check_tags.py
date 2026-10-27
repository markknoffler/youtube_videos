import re, sys
sys.path.insert(0, "../m3b/voice")
from direction import script_chapters, norm
S = script_chapters()
for n in map(int, sys.argv[1:]):
    t = open(f"tagged/ch{n:02d}.txt").read()
    plain = re.sub(r"\[[^\]]*\]\s*", "", t)
    print(n, "OK" if norm(plain) == norm(S[n]) else "MISMATCH", len(t), "chars", len(re.findall(r"\[[^\]]*\]", t)), "tags")
