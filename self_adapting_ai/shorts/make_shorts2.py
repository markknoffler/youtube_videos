"""Cut 15 vertical (1080x1920) shorts/reels out of the finished standard-voice video.

Each clip: blurred full-bleed background, the original frame (bottom caption strip cropped off) in the
middle, a hook line above, big word-wrapped captions below, a small channel footer.
usage: python make_shorts.py [--preview]     (--preview prints the snapped windows and exits)
"""
import os, re, subprocess, sys, tempfile, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = f"{ROOT}/output/Why_Brain-Like_AI_Failed_Standard_Best_Voice.mp4"
SRT = f"{ROOT}/output/Why_Brain-Like_AI_Failed_Standard_Best_Voice.srt"
OUT = f"{HERE}/out2"
W, H = 1080, 1920
FONT = "/System/Library/Fonts/Avenir Next.ttc"

# (slug, hook line, target start "m:ss", target end "m:ss")
CLIPS = [
    ("n01-etched-in-stone",     "Every AI you use is carved in stone",                       "1:05",  "Consider the computational lifecycle", "ancient stone monuments"),
    ("n02-brain-vs-datacenter", "A brain: 20 watts.\nA GPU cluster: megawatts.",              "4:40",  "Now compare this living", "frozen tensors"),
    ("n03-stdp",                "Fire together, and the synapse physically thickens",        "3:40",  "Under the governing laws", "metabolic energy"),
    ("n04-oja-kohonen",         "One neuron found the main pattern. No teacher.",            "5:49",  "In the decades that followed", "topological manifold"),
    ("n05-holy-grail",          "The holy grail of AI that never worked",                    "6:35",  "The self-organizing hypothesis", "representational collapse"),
    ("n06-cant-pay-attention",  "Why brain-like networks can't pay attention",               "11:06", "Now look at what is fundamentally required", "context-sensitive attention"),
    ("n07-five-hops",           "Brain-like graph: 5+ hops.\nAttention: 1 hop.",              "13:00", "If an architecture contains one million", "synthesized"),
    ("n08-bitter-lesson",       "The bitter lesson of 70 years of AI",                       "14:00", "In 2019", "theoretical elegance"),
    ("n09-blind-credit",        "Why local learning wanders blind",                          "15:56", "Furthermore, consider credit assignment", "every compute dollar spent"),
    ("n10-laptop-showdown",     "Brain-like net vs Transformer, live on a laptop",           "16:24", "To test these theorems", "one hundred epochs"),
    ("n11-latent-attention",    "DeepSeek's trick: compress the memory",                     "19:45", "Second, through Multi-head", "irregular graph rewiring"),
    ("n12-titans",              "An AI that rewrites its own weights while it thinks",       "22:39", "This is exactly where the frontier", "inside the monolith"),
    ("n13-rewire-tiles",        "Rewire tiles, not synapses",                                "23:30", "The first idea", "naive implementation"),
    ("n14-fast-weights",        "Synapses faster than learning,\nslower than thought",       "21:40", "In 2021", "into the activations"),
    ("n15-spectral-homeostasis","Can a local rule keep many modes alive?",                   "24:03", "The second idea", "the way attention does"),
]


def secs(s):
    m, r = s.split(":"); return int(m) * 60 + float(r)


def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def t(s):
    h, m, r = s.split(":"); sec, ms = r.split(","); return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def load_cues():
    out = []
    for b in open(SRT).read().strip().split("\n\n"):
        l = b.split("\n"); a, e = l[1].split(" --> ")
        out.append(dict(s=t(a), e=t(e), text=" ".join(l[2:])))
    return out


END = re.compile(r"[.?!…:]\"?$")


NORM = lambda x: re.sub(r"[^a-z0-9 ]", "", x.lower().replace("-", " "))


def find(cues, t0, start_phrase, end_phrase):
    sp = NORM(start_phrase)

    def starts_here(k):
        a = NORM(cues[k]["text"]); j = a + " " + NORM(cues[k + 1]["text"] if k + 1 < len(cues) else "")
        return j.find(sp) == 0 or a.find(sp) == 0
    cand = [k for k, c in enumerate(cues) if c["s"] >= t0 - 12 and starts_here(k)]
    if not cand:
        near = [c["text"] for c in cues if t0 - 12 <= c["s"] <= t0 + 25 and sp.split()[0] in NORM(c["text"])]
        raise SystemExit(f"start phrase not at a cue start: {start_phrase!r}; near: {near}")
    i = cand[0]
    ep = NORM(end_phrase)
    j = next(k for k in range(i, len(cues)) if ep in NORM(cues[k - 1]["text"] + " " + cues[k]["text"]) and NORM(cues[k]["text"]).rstrip().endswith(ep.split()[-1]))
    return i, j


def snap(cues, s0, e0):
    """start on the first cue at/after s0 that begins a sentence; end on the first sentence-final cue at/after e0."""
    i = next(k for k, c in enumerate(cues) if c["s"] >= s0 - 0.5 and (k == 0 or END.search(cues[k - 1]["text"])))
    j = next(k for k, c in enumerate(cues) if k >= i and c["e"] >= e0 and END.search(c["text"]))
    return i, j


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= maxw: cur = trial
        else: lines.append(cur); cur = w
    return lines + [cur]


def caption_png(text, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 54, index=0)
    lines = wrap(d, text, f, W - 220)
    lh = 70; y0 = 1190
    for k, ln in enumerate(lines):
        tw = d.textlength(ln, font=f); x = (W - tw) / 2; y = y0 + k * lh
        d.rounded_rectangle((x - 22, y - 6, x + tw + 22, y + lh - 8), radius=14, fill=(0, 0, 0, 170))
        d.text((x, y), ln, font=f, fill=(255, 255, 255, 255))
    im.save(path)


def static_png(hook, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 64, index=0)
    lines = []
    for part in hook.split("\n"): lines += wrap(d, part, f, W - 220)
    y = 345
    for ln in lines:
        tw = d.textlength(ln, font=f); d.text(((W - tw) / 2, y), ln, font=f, fill=(255, 196, 94, 255),
                                               stroke_width=3, stroke_fill=(0, 0, 0, 255)); y += 82
    ft = ImageFont.truetype(FONT, 34, index=0)
    foot = "MOONSHOT ENGINEERING"
    tw = d.textlength(foot, font=ft); d.text(((W - tw) / 2, 1400), foot, font=ft, fill=(255, 255, 255, 230))
    ft2 = ImageFont.truetype(FONT, 27, index=0)
    sub = "full 28-min breakdown on YouTube"
    tw = d.textlength(sub, font=ft2); d.text(((W - tw) / 2, 1448), sub, font=ft2, fill=(190, 200, 220, 220))
    im.save(path)


def render(slug, hook, cues, i, j):
    s, e = cues[i]["s"], cues[j]["e"]
    tmp = tempfile.mkdtemp(prefix=f"sh_{slug}_")
    blank = f"{tmp}/blank.png"; Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)
    static = f"{tmp}/static.png"; static_png(hook, static)
    entries, tt = [], s
    for k in range(i, j + 1):
        c = cues[k]
        if c["s"] > tt + 0.01: entries.append((blank, c["s"] - tt)); tt = c["s"]
        p = f"{tmp}/{k:04d}.png"; caption_png(c["text"], p)
        entries.append((p, max(0.05, c["e"] - tt))); tt = c["e"]
    lst = f"{tmp}/list.txt"
    with open(lst, "w") as f:
        f.write("ffconcat version 1.0\n")
        for p, dd in entries: f.write(f"file '{p}'\nduration {dd:.3f}\n")
        f.write(f"file '{blank}'\n")
    dur = e - s
    fc = (
        f"[0:v]split[a][b];"
        f"[a]scale=-2:{H},crop={W}:{H},gblur=sigma=40,eq=brightness=-0.28:saturation=0.9[bg];"
        f"[b]crop=1920:930:0:0,scale={W}:-2[fg];"
        f"[bg][fg]overlay=0:620[base];"
        f"[1:v]format=rgba,fps=30[cap];[2:v]format=rgba[st];"
        f"[base][st]overlay=0:0[b2];[b2][cap]overlay=0:0:eof_action=pass[v];"
        f"[0:a]afade=t=in:st=0:d=0.12,afade=t=out:st={dur - 0.25:.2f}:d=0.25[a]"
    )
    os.makedirs(OUT, exist_ok=True)
    out = f"{OUT}/{slug}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{dur:.3f}", "-i", SRC,
                    "-f", "concat", "-safe", "0", "-i", lst, "-loop", "1", "-t", f"{dur:.3f}", "-i", static,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
    return out, s, e


if __name__ == "__main__":
    cues = load_cues(); meta = []
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for slug, hook, a, sp, ep in CLIPS:
        if only and not any(o in slug for o in only): continue
        i, j = find(cues, secs(a), sp, ep)
        s, e = cues[i]["s"], cues[j]["e"]
        print(f"{slug}: {ts(s)[3:]} -> {ts(e)[3:]} ({e - s:.0f}s)\n   starts: {cues[i]['text'][:70]}\n   ends:   {cues[j]['text'][-70:]}")
        if "--preview" in sys.argv: continue
        out, s, e = render(slug, hook, cues, i, j)
        meta.append(dict(slug=slug, file=out, start=s, end=e, dur=e - s, hook=hook.replace("\n", " ")))
    if meta: json.dump(meta, open(f"{HERE}/shorts_meta2.json", "w"), indent=1)
