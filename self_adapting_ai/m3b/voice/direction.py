"""Parse VOICE_DIRECTION_V2.md into segments and validate against VOICEOVER_SCRIPT_V2.md."""
import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SA = os.path.dirname(os.path.dirname(HERE))
SEG = re.compile(r"^(?P<nv>(?:<(?:breath|sigh|laugh)>\s*)?)(?:\[(?P<dir>[^\]]*)\]\s*)?(?P<text>.*?)\s*(?P<pause>/{1,3})?\s*$")


def script_chapters(path=os.path.join(SA, "VOICEOVER_SCRIPT_V2.md")):
    s = open(path, encoding="utf-8").read()
    return {int(n): t.strip() for n, t in re.findall(r"## CHAPTER (\d+):[^\n]*\n.*?```text\n(.*?)```", s, re.S)}


def direction_chapters(path=os.path.join(SA, "VOICE_DIRECTION_V2.md")):
    s = open(path, encoding="utf-8").read()
    out = {}
    for n, body in re.findall(r"^## CH(\d+)\n(.*?)(?=^## CH|\Z)", s, re.S | re.M):
        segs = []
        for line in body.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            m = SEG.match(line)
            d = dict(kv.split("=") for kv in (m["dir"] or "").split())
            segs.append(dict(text=m["text"], nv=m["nv"].strip("<> ") or None, pause=len(m["pause"] or ""), **d))
        out[int(n)] = segs
    return out


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


if __name__ == "__main__":
    S, D = script_chapters(), direction_chapters()
    ok = True
    for n in sorted(S):
        a = norm(" ".join(x["text"] for x in D.get(n, [])))
        b = norm(S[n])
        if a != b:
            ok = False
            i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            print(f"CH{n:02d} MISMATCH at {i}:\n  dir: ...{a[max(0,i-60):i+60]}\n  scr: ...{b[max(0,i-60):i+60]}")
        else:
            print(f"CH{n:02d} ok  {len(D[n])} segments")
    sys.exit(0 if ok else 1)
