"""Post-render subtitles: script-text lines (timed from the aligned spoken words) rendered as
transparent PNGs and overlaid with ffmpeg. Also writes an .srt for YouTube.
usage: python burn_captions.py <voice> <ch> <in.mp4> <out.mp4>"""
import os, sys, subprocess, tempfile
sys.argv, args = sys.argv[:1], sys.argv[1:]
from common import caption_lines, write_srt, ROOT
from PIL import Image, ImageDraw, ImageFont

voice, ch, src, dst = args[0], int(args[1]), args[2], args[3]
W, H = 1920, 1080
font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 40, index=0)
lines = caption_lines(voice, ch)
tmp = tempfile.mkdtemp(prefix=f"cap{ch:02d}_")
blank = os.path.join(tmp, "blank.png"); Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)


def card(text, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=font)
    tw, th = x1 - x0, y1 - y0
    cx, cy = W // 2, H - 62
    pad_x, pad_y = 22, 12
    d.rounded_rectangle((cx - tw // 2 - pad_x, cy - th // 2 - pad_y, cx + tw // 2 + pad_x, cy + th // 2 + pad_y + 6), radius=10, fill=(0, 0, 0, 165))
    d.text((cx - tw // 2 - x0, cy - th // 2 - y0), text, font=font, fill=(255, 255, 255, 255))
    im.save(path)


# ffconcat slideshow: blank gaps + one card per line, durations from the word timings
entries, t = [], 0.0
for k, ln in enumerate(lines):
    if ln["s"] > t + 0.01:
        entries.append((blank, ln["s"] - t)); t = ln["s"]
    p = os.path.join(tmp, f"{k:04d}.png"); card(ln["text"], p)
    entries.append((p, max(0.05, ln["e"] - t))); t = ln["e"]
entries.append((blank, 2.0))
lst = os.path.join(tmp, "list.txt")
with open(lst, "w") as f:
    f.write("ffconcat version 1.0\n")
    for p, d_ in entries:
        f.write(f"file '{p}'\nduration {d_:.3f}\n")
    f.write(f"file '{blank}'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-f", "concat", "-safe", "0", "-i", lst,
                "-filter_complex", "[1:v]format=rgba,fps=30[c];[0:v][c]overlay=0:0:eof_action=pass:shortest=0[v]",
                "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "copy", dst], check=True)
write_srt(voice, ch, os.path.splitext(dst)[0] + ".srt")
print("captioned", dst, len(lines), "lines")
