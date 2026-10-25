"""Shared toolkit for the 'Why Brain-Like AI Failed' Manim chapters.

Every chapter is a Scene subclass of `Chapter`. Animations are keyed to spoken words:
`self.at("dot product")` returns the time that phrase starts in the active voice track,
and `self.cue("dot product", anims...)` waits until then and plays. Because the same scene
code is driven by the word timings of each voice, both voice sets get frame-accurate sync.

VOICE env var selects the track: "standard" (default) or "cloned".
"""
from __future__ import annotations

import json, os, re, sys, difflib
import numpy as np
from manim import *

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(ROOT)
ASSETS = os.path.join(ROOT, "assets")
VOICE = os.environ.get("VOICE", "standard")

# ── palette ──────────────────────────────────────────────────────────────────────────
BG = "#0B0E13"
C_BLUE, C_TEAL, C_GREEN = "#58C4DD", "#5CD0B3", "#83C167"
C_YELLOW, C_GOLD, C_ORANGE = "#FFE066", "#F0AC5F", "#FF8C42"
C_RED, C_PINK, C_PURPLE = "#FC6255", "#E46CB4", "#9A72AC"
C_GREY, C_DIM, C_ICE = "#8A93A3", "#3A4250", "#BFE9FF"
Q_COL, K_COL, V_COL = "#FF8C42", "#58C4DD", "#83C167"
FONT = "Avenir Next"
MONO = "Menlo"

config.background_color = BG


# ── narration timeline ───────────────────────────────────────────────────────────────
_NUM = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
        "eight": "8", "nine": "9", "ten": "10", "sixteen": "16", "twenty": "20", "fifty": "50", "sixty": "60",
        "seventy": "70", "eighty": "80", "ninety": "90", "hundred": "100", "first": "1st"}


def _norm(w: str) -> str:
    w = w.lower().replace("’", "'")
    w = re.sub(r"[^a-z0-9]", "", w)
    return _NUM.get(w, w)


def draft_timing(ch: int) -> dict:
    """Approximate word timings from the V2 script text (for previews before audio exists)."""
    src = open(os.path.join(PROJECT, "VOICEOVER_SCRIPT_V2.md"), encoding="utf-8").read()
    text = dict((int(n), t) for n, t in re.findall(r"## CHAPTER (\d+):[^\n]*\n.*?```text\n(.*?)```", src, re.S))[ch]
    t, words = 0.4, []
    for para in text.strip().split("\n\n"):
        for w in para.split():
            dur = 0.16 + 0.045 * len(w)
            words.append({"w": w, "s": round(t, 3), "e": round(t + dur, 3)})
            t += dur + (0.32 if w.endswith((",", ":", ";")) else 0.55 if w.endswith((".", "?", "!")) else 0.04)
        t += 0.6
    return {"duration": t + 0.5, "words": words}


class Timeline:
    def __init__(self, voice: str, ch: int):
        path = os.path.join(ROOT, "timing", f"{voice}_ch{ch:02d}.json")
        d = json.load(open(path)) if os.path.exists(path) else draft_timing(ch)
        self.duration = d["duration"]
        self.words = [w for w in d["words"] if _norm(w["w"])]
        self.toks = [_norm(w["w"]) for w in self.words]
        self.cursor = 0

    def find(self, phrase: str, after: float | None = None, end=False) -> float:
        """Start (or end) time of the best fuzzy match of `phrase` at/after the cursor.
        Candidates further from the cursor are penalised, so a near-perfect early match
        always beats a similar-looking phrase later in the chapter."""
        parts = [_norm(p) for p in phrase.replace("-", " ").split()]
        parts = [p for p in parts if p]
        target = "".join(parts)
        n = len(parts)
        start_i = self.cursor
        if after is not None:
            start_i = next((i for i, w in enumerate(self.words) if w["s"] >= after - 0.05), len(self.words) - 1)
        best, best_i, best_j, best_r = -1.0, None, None, 0.0
        for i in range(start_i, min(len(self.toks), start_i + 120)):
            for span in range(max(1, n - 2), n + 3):
                j = min(len(self.toks), i + span)
                r = difflib.SequenceMatcher(None, "".join(self.toks[i:j]), target).ratio()
                score = r - 0.003 * (i - start_i)
                if score > best + 1e-6:
                    best, best_i, best_j, best_r = score, i, j, r
        if best_i is None or best_r < 0.72:
            raise ValueError(f"cue not found: {phrase!r} (best {best_r:.2f})")
        self.cursor = best_i
        return self.words[best_j - 1]["e"] if end else self.words[best_i]["s"]


# ── base scene ───────────────────────────────────────────────────────────────────────
class Chapter(MovingCameraScene):
    CH = 0

    def setup(self):
        super().setup()
        self.tl = Timeline(VOICE, self.CH)
        self.camera.background_color = BG

    @property
    def now(self) -> float:
        return self.renderer.time

    def at(self, phrase, end=False, after=None) -> float:
        if isinstance(phrase, (int, float)):
            return float(phrase)
        return self.tl.find(phrase, after=after, end=end)

    def hold_until(self, t: float):
        if t - self.now > 1 / 30:
            self.wait(t - self.now)

    def cue(self, phrase, *anims, rt: float = 1.2, lead: float = 0.15, **kw):
        """Wait for `phrase` to be spoken (minus a small lead), then play anims."""
        t = self.at(phrase) - lead if phrase is not None else self.now
        self.hold_until(t)
        if anims:
            self.play(*anims, run_time=rt, **kw)

    def times(self, *phrases):
        """Resolve cue phrases in narration order → self.C[phrase] = start time."""
        self.C, missing = {}, []
        for p in phrases:
            try:
                self.C[p] = self.tl.find(p)
            except ValueError:
                self.C[p] = None
                missing.append(p)
        # interpolate any phrase the TTS skipped between its resolved neighbours
        keys = list(self.C)
        for i, k in enumerate(keys):
            if self.C[k] is None:
                prev = next((self.C[keys[j]] for j in range(i - 1, -1, -1) if self.C[keys[j]] is not None), 0.0)
                nxt = next((self.C[keys[j]] for j in range(i + 1, len(keys)) if self.C[keys[j]] is not None), self.tl.duration)
                self.C[k] = (prev + nxt) / 2
        if missing:
            print(f"[cues ch{self.CH} {VOICE}] interpolated: {missing}", file=sys.stderr)
        for a_, b_ in zip(keys, keys[1:]):
            if self.C[b_] < self.C[a_]:
                print(f"[order ch{self.CH} {VOICE}] {b_!r} before {a_!r}", file=sys.stderr)
        return self.C

    def t(self, key):
        return self.C[key] if isinstance(key, str) else float(key)

    def go(self, key, *anims, rt=1.0, upto=None, lead=0.12, **kw):
        """Hold until cue `key`, then play `anims`; run time is capped so we finish before `upto`."""
        if key is not None:
            late = self.now - (self.t(key) - lead)
            if late > 0.4:
                print(f"[late ch{self.CH} {VOICE}] {key!r} by {late:.1f}s", file=sys.stderr)
            self.hold_until(self.t(key) - lead)
        if anims:
            if upto is not None:
                rt = max(0.25, min(rt, self.t(upto) - lead - self.now - 0.05))
            self.play(*anims, run_time=rt, **kw)

    def then(self, *anims, rt=1.0, upto=None, **kw):
        self.go(None, *anims, rt=rt, upto=upto, **kw)

    def word_times(self, text, start):
        """Spoken start time of every word of `text`, aligned from time `start` on."""
        words = text.split()
        toks = [_norm(w) for w in words]
        i0 = next((i for i, w in enumerate(self.tl.words) if w["s"] >= start - 0.3), 0)
        win = self.tl.toks[i0:i0 + int(len(toks) * 1.5) + 5]
        sm = difflib.SequenceMatcher(None, toks, win, autojunk=False)
        out = [None] * len(toks)
        for a, b_, n in sm.get_matching_blocks():
            for k in range(n):
                out[a + k] = self.tl.words[i0 + b_ + k]["s"]
        known = [(i, t) for i, t in enumerate(out) if t is not None] or [(0, start)]
        for i in range(len(out)):
            if out[i] is None:
                lo = max([k for k in known if k[0] < i], default=(i, start), key=lambda k: k[0])
                hi = min([k for k in known if k[0] > i], default=(i, lo[1] + 0.3 * (i - lo[0])), key=lambda k: k[0])
                out[i] = lo[1] + (hi[1] - lo[1]) * (i - lo[0]) / max(1, hi[0] - lo[0])
        return out

    def karaoke(self, words_mob, times, on=C_YELLOW, off=C_GREY, done=WHITE):
        """Updater: each word lights up as it is spoken, then settles to `done`."""
        def upd(m):
            now = self.now
            for w, t in zip(m, times):
                if now < t:
                    w.set_color(off)
                elif now < t + 0.45:
                    w.set_color(on)
                else:
                    w.set_color(done)
        words_mob.add_updater(upd)
        return words_mob

    def stage(self, *keep):
        """Everything currently visible except `keep` (for a clean FadeOut)."""
        return Group(*[m for m in self.mobjects if m not in keep and not isinstance(m, ValueTracker)
                       and type(m) is not Mobject])

    def finish(self, tail: float = 0.6):
        self.hold_until(self.tl.duration + tail)


# ── text helpers ─────────────────────────────────────────────────────────────────────
def T(s, size=28, color=WHITE, weight=NORMAL, font=FONT, **kw):
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def M(*s, size=40, color=WHITE, **kw):
    return MathTex(*s, font_size=size, color=color, **kw)


def mono(s, size=20, color=C_GREY, **kw):
    return Text(s, font=MONO, font_size=size, color=color, **kw)


def glow(mob: VMobject, color=None, layers=5, width=14, opacity=0.18):
    """Soft halo by stacking wide translucent strokes behind a copy of `mob`."""
    color = color or mob.get_color()
    g = VGroup()
    for i in range(layers):
        c = mob.copy().set_fill(opacity=0)
        c.set_stroke(color, width=width * (i + 1) / layers, opacity=opacity * (1 - i / layers))
        g.add(c)
    return g


def label_box(text, color=C_BLUE, size=22, pad=0.18, fill=0.12):
    t = T(text, size=size, color=color)
    r = SurroundingRectangle(t, buff=pad, color=color, stroke_width=1.5, corner_radius=0.08)
    r.set_fill(color, fill)
    return VGroup(r, t)


# ── mechanism components ─────────────────────────────────────────────────────────────
class NeuralNet(VGroup):
    """3b1b-style layered network; edges coloured by weight sign, width by magnitude."""

    def __init__(self, sizes=(4, 6, 6, 3), width=6, height=4, r=0.13, seed=1, edge_op=0.5, **kw):
        super().__init__(**kw)
        rng = np.random.default_rng(seed)
        self.layers = VGroup()
        xs = np.linspace(-width / 2, width / 2, len(sizes))
        for x, n in zip(xs, sizes):
            ys = np.linspace(height / 2, -height / 2, n) if n > 1 else [0]
            layer = VGroup(*[Circle(r, color=WHITE, stroke_width=2).set_fill(BLACK, 1).move_to([x, y, 0]) for y in ys])
            self.layers.add(layer)
        self.edges = VGroup()
        self.weights = []
        for a, b in zip(self.layers[:-1], self.layers[1:]):
            g = VGroup()
            for na in a:
                for nb in b:
                    w = rng.normal()
                    self.weights.append(w)
                    ln = Line(na.get_center(), nb.get_center(), buff=r,
                              stroke_width=0.6 + 2.2 * min(abs(w), 1.6) / 1.6,
                              color=C_BLUE if w > 0 else C_RED, stroke_opacity=edge_op * min(1, 0.35 + abs(w) / 2))
                    g.add(ln)
            self.edges.add(g)
        self.add(self.edges, self.layers)

    def activate(self, li, values):
        return AnimationGroup(*[n.animate.set_fill(interpolate_color(ManimColor(BLACK), ManimColor(WHITE), v), 1)
                                for n, v in zip(self.layers[li], values)])

    def flow(self, li, color=C_YELLOW, time_width=0.5):
        """Signal pulses travelling along every edge between layer li and li+1."""
        return LaggedStart(*[ShowPassingFlash(e.copy().set_stroke(color, 3.2, 1), time_width=time_width)
                             for e in self.edges[li]], lag_ratio=0.004)

    def forward(self, values_per_layer, color=C_YELLOW):
        seq = []
        for li in range(len(self.layers)):
            seq.append(self.activate(li, values_per_layer[li]))
            if li < len(self.edges):
                seq.append(self.flow(li, color))
        return Succession(*seq)


def heat_color(v, cmap=(BLACK, C_BLUE, C_YELLOW)):
    a, b, c = (ManimColor(x) for x in cmap)
    v = float(np.clip(v, 0, 1))
    return interpolate_color(a, b, v * 2) if v < 0.5 else interpolate_color(b, c, (v - 0.5) * 2)


def heatmap(M_, cell=0.34, cmap=(BLACK, C_BLUE, C_YELLOW), stroke=0.6):
    """Grid of squares coloured by matrix values in [0, 1]."""
    rows, cols = M_.shape
    g = VGroup()
    for i in range(rows):
        for j in range(cols):
            sq = Square(cell, stroke_width=stroke, stroke_color=C_DIM).set_fill(heat_color(M_[i, j], cmap), 1)
            sq.move_to([j * cell, -i * cell, 0])
            g.add(sq)
    g.center()
    return g


def set_heat(grid, M_, cmap=(BLACK, C_BLUE, C_YELLOW)):
    for sq, v in zip(grid, M_.flatten()):
        sq.set_fill(heat_color(v, cmap), 1)
    return grid


def token_row(words, color=C_GREY, size=22, buff=0.12, box=True):
    g = VGroup()
    for w in words:
        t = T(w, size=size, color=WHITE)
        if box:
            r = SurroundingRectangle(t, buff=0.1, color=color, stroke_width=1.4, corner_radius=0.06).set_fill(color, 0.15)
            g.add(VGroup(r, t))
        else:
            g.add(t)
    g.arrange(RIGHT, buff=buff)
    return g


def vec_column(vals, color=WHITE, size=20, h=0.32):
    """Bracketed column of numbers, for showing token vectors."""
    nums = VGroup(*[T(f"{v:+.2f}", size=size, color=color, font=MONO) for v in vals]).arrange(DOWN, buff=h - 0.2)
    l = Line(nums.get_corner(UL) + LEFT * 0.1, nums.get_corner(DL) + LEFT * 0.1, color=C_GREY, stroke_width=2)
    r = Line(nums.get_corner(UR) + RIGHT * 0.1, nums.get_corner(DR) + RIGHT * 0.1, color=C_GREY, stroke_width=2)
    tl = Line(l.get_start(), l.get_start() + RIGHT * 0.08, color=C_GREY, stroke_width=2)
    bl = Line(l.get_end(), l.get_end() + RIGHT * 0.08, color=C_GREY, stroke_width=2)
    tr = Line(r.get_start(), r.get_start() + LEFT * 0.08, color=C_GREY, stroke_width=2)
    brr = Line(r.get_end(), r.get_end() + LEFT * 0.08, color=C_GREY, stroke_width=2)
    return VGroup(nums, l, r, tl, bl, tr, brr)


def image(path, height=3.0):
    full = path if os.path.isabs(path) else os.path.join(ASSETS, path)
    return ImageMobject(full).set_height(height)


def framed_image(path, height=3.0, color=C_GREY, caption=None, cap_size=18):
    im = image(path, height)
    fr = SurroundingRectangle(im, buff=0.0, color=color, stroke_width=2)
    g = Group(im, fr)
    if caption:
        g.add(T(caption, size=cap_size, color=C_GREY).next_to(fr, DOWN, buff=0.12))
    return g


def highlight_bar(mob_or_rect, color=C_YELLOW, opacity=0.28):
    r = Rectangle(width=mob_or_rect.width, height=mob_or_rect.height).move_to(mob_or_rect)
    r.set_stroke(width=0).set_fill(color, opacity)
    return r


class LiveAxes(VGroup):
    """Axes + a curve that is drawn progressively from data as a tracker advances."""

    def __init__(self, x_range, y_range, width=5, height=3, x_label="", y_label="", **kw):
        super().__init__()
        self.ax = Axes(x_range=x_range, y_range=y_range, x_length=width, y_length=height,
                       axis_config=dict(color=C_GREY, stroke_width=2, include_tip=False, font_size=18),
                       **kw)
        self.add(self.ax)
        if x_label:
            self.add(T(x_label, size=16, color=C_GREY).next_to(self.ax.x_axis, DOWN, buff=0.3))
        if y_label:
            self.add(T(y_label, size=16, color=C_GREY).rotate(PI / 2).next_to(self.ax.y_axis, LEFT, buff=0.3))

    def live_curve(self, xs, ys, tracker: ValueTracker, color=C_BLUE, width=3, dot=True):
        ax = self.ax

        def build():
            k = tracker.get_value()
            n = int(np.clip(np.searchsorted(xs, k, side="right"), 2, len(xs)))
            pts = [ax.c2p(x, y) for x, y in zip(xs[:n], ys[:n])]
            m = VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(pts) if len(pts) > 2 else VMobject()
            return m

        curve = always_redraw(build)
        out = VGroup(curve)
        if dot:
            def d():
                k = tracker.get_value()
                n = int(np.clip(np.searchsorted(xs, k, side="right"), 1, len(xs))) - 1
                return Dot(ax.c2p(xs[n], ys[n]), radius=0.06, color=color)
            out.add(always_redraw(d))
        return out


class Cloud3D(VGroup):
    """Cheap 3D point cloud: points live in R^3, projected each frame with a rotating view."""

    def __init__(self, pts, colors, radius=0.035, scale=1.0, yaw=None, pitch=0.35, **kw):
        super().__init__(**kw)
        self.P = np.array(pts, float)
        self.target = self.P.copy()
        self.yaw = yaw or ValueTracker(0)
        self.pitch = pitch
        self.s = scale
        for c in colors:
            self.add(Dot(radius=radius, color=c))
        self.add_updater(lambda m, dt: m._project())

    def _project(self):
        a, b = self.yaw.get_value(), self.pitch
        Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
        Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
        Q = self.P @ (Rx @ Ry).T
        center = self.get_center() if False else getattr(self, "anchor", ORIGIN)
        for d, q in zip(self.submobjects, Q):
            depth = (q[2] + 3) / 6
            d.move_to(center + self.s * np.array([q[0], q[1], 0]))
            d.set_opacity(np.clip(0.35 + 0.65 * depth, 0.2, 1))


# ── real paper pages with line-accurate highlights ───────────────────────────────────
PDFS = {
    "attention": os.path.join(PROJECT, "papers", "1706.03762v7_Attention_Is_All_You_Need.pdf"),
    "lottery": os.path.join(PROJECT, "papers", "2009.06489v2_The_Hardware_Lottery.pdf"),
    "oswald": os.path.join(ASSETS, "pdf", "2212.07677.pdf"),
    "wann": os.path.join(PROJECT, "papers", "gaier_2019_weight_agnostic_neural_networks.pdf"),
    "kan": os.path.join(PROJECT, "papers", "liu_2024_kan_kolmogorov_arnold_networks.pdf"),
    "liquid": os.path.join(PROJECT, "papers", "hasani_2020_liquid_time_constant_networks.pdf"),
    "node": os.path.join(PROJECT, "papers", "1806.07366v5_Neural_Ordinary_Differential_Equations.pdf"),
    "kirsch": os.path.join(PROJECT, "papers", "kirsch_2023_towards_general_meta_plasticity.pdf"),
    "miconi": os.path.join(PROJECT, "papers", "miconi_2021_hebbian_meta_learning.pdf"),
    "deepseek": os.path.join(ASSETS, "pdf", "2412.19437.pdf"),
    "deepseek2": os.path.join(ASSETS, "pdf", "2405.04434.pdf"),
    "induction": os.path.join(ASSETS, "pdf", "2209.11895.pdf"),
    "ttt": os.path.join(ASSETS, "pdf", "2407.04620.pdf"),
    "schlag": os.path.join(PROJECT, "papers", "new", "2102.11174.pdf"),
    "ba2016": os.path.join(PROJECT, "papers", "new", "1610.06258.pdf"),
    "rigl": os.path.join(PROJECT, "papers", "new", "1911.11134.pdf"),
    "eprop": os.path.join(PROJECT, "papers", "new", "1901.09049.pdf"),
    "titans": os.path.join(PROJECT, "papers", "new", "2501.00663.pdf"),
}


class PaperPage(Group):
    """A rendered PDF page as an image, plus `self.hl(text)` → rectangle over that text."""

    def __init__(self, key, page=0, height=6.0, clip=None, dpi=170):
        super().__init__()
        import fitz
        doc = fitz.open(PDFS[key])
        pg = doc[page]
        self.rect = clip or pg.rect
        out_dir = os.path.join(ASSETS, "pages")
        os.makedirs(out_dir, exist_ok=True)
        cid = "full" if clip is None else "_".join(str(int(v)) for v in clip)
        png = os.path.join(out_dir, f"{key}_p{page}_{cid}_{dpi}.png")
        if not os.path.exists(png):
            pg.get_pixmap(dpi=dpi, clip=self.rect).save(png)
        self.key, self.page_no = key, page
        self.rect = tuple(self.rect)
        self.img = ImageMobject(png).set_height(height)
        self.frame = SurroundingRectangle(self.img, buff=0, color=C_GREY, stroke_width=1.5)
        self.shadow = Rectangle(width=self.img.width, height=self.img.height).set_stroke(width=0).set_fill(BLACK, 0.6)
        self.shadow.move_to(self.img).shift(0.08 * DR)
        self.add(self.shadow, self.img, self.frame)

    def _to_scene(self, r):
        rx0, ry0, rx1, ry1 = self.rect
        W, H = rx1 - rx0, ry1 - ry0
        ul = self.img.get_corner(UL)
        sx, sy = self.img.width / W, self.img.height / H
        x0, y0 = (r.x0 - rx0) * sx, (r.y0 - ry0) * sy
        return ul + np.array([x0 + r.width * sx / 2, -(y0 + r.height * sy / 2), 0]), r.width * sx, r.height * sy

    def hl(self, text, color=C_YELLOW, opacity=0.35, which=0, pad=0.02):
        import fitz
        hits = fitz.open(PDFS[self.key])[self.page_no].search_for(text, clip=fitz.Rect(*self.rect))
        if not hits:
            raise ValueError(f"text not found on page: {text!r}")
        # merge all quads belonging to the `which`-th occurrence (multi-line hits are consecutive)
        rects = VGroup()
        for r in hits[which:which + 1] if len(text) < 40 else hits:
            c, w, h = self._to_scene(r)
            rects.add(Rectangle(width=w + pad, height=h + pad).move_to(c).set_stroke(width=0).set_fill(color, opacity))
        return rects


class Stream(VGroup):
    """Particles flowing continuously along `path` — each particle is a unit of signal.
    `speed` (path-fractions per second) can be animated through `self.speed` tracker."""

    def __init__(self, path: VMobject, n=12, speed=0.25, color=C_YELLOW, radius=0.04, square=False, fade_ends=True):
        super().__init__()
        self.path = path
        self.speed = ValueTracker(speed)
        self.phase = np.linspace(0, 1, n, endpoint=False) + np.random.default_rng(len(path.points)).random(n) * 0.02
        for _ in range(n):
            p = Square(radius * 2.2).set_stroke(width=0).set_fill(color, 1) if square else Dot(radius=radius, color=color)
            self.add(p)
        self.fade_ends = fade_ends
        self.add_updater(Stream._tick)
        Stream._tick(self, 0)

    @staticmethod
    def _tick(m, dt):
        m.phase = (m.phase + dt * m.speed.get_value()) % 1
        for p, a in zip(m.submobjects, m.phase):
            p.move_to(m.path.point_from_proportion(a))
            if m.fade_ends:
                p.set_opacity(min(1, 6 * min(a, 1 - a)))


def counter(value, fmt=0, size=30, color=WHITE, unit="", tracker=None):
    tr = tracker if tracker is not None else ValueTracker(value)
    d = DecimalNumber(value, num_decimal_places=fmt, font_size=size, color=color, group_with_commas=True)
    d.add_updater(lambda m: m.set_value(tr.get_value()))
    g = VGroup(d)
    if unit:
        u = T(unit, size=size * 0.6, color=C_GREY)
        u.add_updater(lambda m: m.next_to(d, RIGHT, buff=0.1, aligned_edge=DOWN))
        g.add(u)
    g.tracker = tr
    return g


def monolith(n_layers=6, w=2.2, h=0.42, gap=0.1, color=C_ICE):
    """Stack of Transformer layers (attention + MLP) — the frozen 'monolith'."""
    g = VGroup()
    for i in range(n_layers):
        a = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color, stroke_width=1.6).set_fill(color, 0.10)
        lab = T("Attention" if i % 2 == 0 else "MLP", size=14, color=color)
        lab.move_to(a)
        g.add(VGroup(a, lab))
    g.arrange(UP, buff=gap)
    return g


def code_block(src, size=18, hl_lines=()):
    c = Code(code_string=src, language="python", formatter_style="monokai", background="window",
             add_line_numbers=False, paragraph_config=dict(font=MONO, font_size=size))
    c.background.set_fill(BLACK, 0.85).set_stroke(C_DIM, 1.5)
    return c


def matrix_mob(vals, size=24, color=WHITE, h_buff=0.9, v_buff=0.55, fmt="{:.1f}"):
    m = Matrix([[fmt.format(v) for v in row] for row in vals], h_buff=h_buff, v_buff=v_buff,
               element_to_mobject=lambda s: T(s, size=size, color=color, font=MONO),
               bracket_config=dict(color=C_GREY))
    return m


def living_graph(n=26, center=ORIGIN, radius=1.6, seed=3, color=C_GREEN):
    """Organic graph whose nodes drift and whose edges sprout/prune by proximity every frame."""
    rng = np.random.default_rng(seed)
    base = np.array([center + radius * np.array([*(rng.random(2) * 2 - 1), 0]) for _ in range(n)])
    nodes = VGroup(*[Dot(p, radius=0.05, color=color) for p in base])
    nodes.t = 0.0
    nodes.base = base
    nodes.freq = rng.random((n, 2)) * 1.5 + 0.4
    nodes.amp = ValueTracker(0.25)

    def drift(m, dt):
        m.t += dt
        a = m.amp.get_value()
        for i, d in enumerate(m):
            d.move_to(m.base[i] + a * np.array([np.sin(m.t * m.freq[i, 0] + i), np.cos(m.t * m.freq[i, 1] + 2 * i), 0]))
    nodes.add_updater(drift)
    thr = ValueTracker(0.95 * radius / 1.6)

    def edges():
        g = VGroup()
        pts = [d.get_center() for d in nodes]
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.linalg.norm(pts[i] - pts[j])
                if dist < thr.get_value():
                    op = 1 - dist / thr.get_value()
                    g.add(Line(pts[i], pts[j], stroke_width=1.6, color=color, stroke_opacity=0.9 * op))
        return g
    e = always_redraw(edges)
    grp = VGroup(e, nodes)
    grp.nodes, grp.thr = nodes, thr
    return grp


class SpikeField(VGroup):
    """Neurons (somata + short dendrites) that fire asynchronously as Poisson processes.
    Each spike flashes the soma and launches a pulse along one of its outgoing synapses.
    Structure never changes size (pulses come from a fixed pool) so it can be animated safely;
    fade it with `field.alpha`, not set_opacity."""

    def __init__(self, n=40, width=10, height=5.5, rate=3.0, seed=2, color=C_GREEN, k=3, center=ORIGIN, pool=60):
        super().__init__()
        rng = np.random.default_rng(seed)
        self.rng = rng
        self.pos = np.array([center + np.array([(rng.random() - 0.5) * width, (rng.random() - 0.5) * height, 0]) for _ in range(n)])
        self.rate = ValueTracker(rate)
        self.alpha = ValueTracker(1.0)
        self.color = color
        self.dendrites = VGroup()
        for p in self.pos:
            for a in rng.random(3) * TAU:
                L = 0.18 + 0.15 * rng.random()
                d = ArcBetweenPoints(p, p + L * np.array([np.cos(a), np.sin(a), 0]), angle=0.6 * (rng.random() - 0.5))
                self.dendrites.add(d.set_stroke(color, 1.2, 0.45))
        self.syn = []
        self.synapses = VGroup()
        self.out = [[] for _ in range(n)]
        for i, p in enumerate(self.pos):
            dists = np.linalg.norm(self.pos - p, axis=1)
            for j in np.argsort(dists)[1:k + 1]:
                ln = Line(p, self.pos[j], stroke_width=1.0, color=color, stroke_opacity=0.22)
                self.synapses.add(ln)
                self.out[i].append(ln)
        self.somata = VGroup(*[Dot(p, radius=0.06, color=color).set_fill(color, 0.55) for p in self.pos])
        self.glowv = np.zeros(n)
        self.pulses = VGroup(*[Dot(radius=0.045, color=C_YELLOW).set_opacity(0) for _ in range(pool)])
        self.pstate = [None] * pool
        self._last_alpha = None
        self.add(self.synapses, self.dendrites, self.somata, self.pulses)
        self.add_updater(SpikeField._tick)

    def recolor(self, color):
        self.color = color
        self.synapses.set_stroke(color)
        self.dendrites.set_stroke(color)

    @staticmethod
    def _tick(m, dt):
        r, al = m.rate.get_value(), m.alpha.get_value()
        if m._last_alpha != al:
            m.synapses.set_stroke(opacity=0.22 * al)
            m.dendrites.set_stroke(opacity=0.45 * al)
            m._last_alpha = al
        if dt > 0:
            fire = m.rng.random(len(m.somata)) < r * dt / 3
            for i in np.nonzero(fire)[0]:
                m.glowv[i] = 1.0
                free = next((k for k, st in enumerate(m.pstate) if st is None), None)
                if free is not None and m.out[i]:
                    m.pstate[free] = [m.out[i][m.rng.integers(len(m.out[i]))], 0.0]
            m.glowv *= np.exp(-dt * 6)
        c0, c1 = ManimColor(m.color), ManimColor(WHITE)
        for i, s in enumerate(m.somata):
            g = m.glowv[i]
            s.set_fill(interpolate_color(c0, c1, g), (0.55 + 0.45 * g) * al)
            s.set_stroke(opacity=0)
            s.scale_to_fit_width(0.12 + 0.12 * g)
        for k, pd in enumerate(m.pulses):
            st = m.pstate[k]
            if st is None:
                pd.set_opacity(0)
                continue
            st[1] += dt * 2.5
            if st[1] >= 1:
                m.pstate[k] = None
                pd.set_opacity(0)
            else:
                pd.move_to(st[0].point_from_proportion(st[1])).set_opacity(al)


def systolic(rows=8, cols=8, cell=0.32, color=C_ORANGE):
    g = VGroup(*[Square(cell).set_stroke(color, 1.2).set_fill(color, 0.08) for _ in range(rows * cols)])
    g.arrange_in_grid(rows, cols, buff=0.05)
    g.rows, g.cols = rows, cols
    return g


def wavefront(grid, tracker, color=C_ORANGE, width=2.5):
    """Updater: anti-diagonal wavefront at position tracker (in cell units) lights the PEs."""
    def upd(m):
        k = tracker.get_value()
        for idx, sq in enumerate(m):
            i, j = divmod(idx, m.cols)
            d = abs((i + j) - k)
            sq.set_fill(color, 0.08 + 0.85 * max(0, 1 - d / width))
    grid.add_updater(upd)
    return grid


def bulb(color=C_YELLOW, scale=1.0):
    glass = Circle(0.35, color=color, stroke_width=2).set_fill(color, 0.25)
    base = VGroup(*[Line(LEFT * 0.14, RIGHT * 0.14, color=C_GREY, stroke_width=3).shift(DOWN * (0.42 + 0.07 * k)) for k in range(3)])
    fil = VMobject(stroke_color=color, stroke_width=2).set_points_smoothly([LEFT * 0.12 + DOWN * 0.3, LEFT * 0.08, RIGHT * 0.08, RIGHT * 0.12 + DOWN * 0.3])
    return VGroup(glow(glass, color, opacity=0.3), glass, fil, base).scale(scale)


def wrap_words(text, width=6.0, size=26, font=FONT, color=C_GREY, line_buff=0.22, slant=NORMAL):
    """Text laid out in lines ≤ `width`; returns a VGroup with one sub-VGroup per word (baseline-correct)."""
    words = text.split()
    probe = lambda s_: Text(s_, font=font, font_size=size, slant=slant).width
    lines, cur = [], []
    for w in words:
        if cur and probe(" ".join(cur + [w])) > width:
            lines.append(cur); cur = []
        cur.append(w)
    lines.append(cur)
    out, rows = VGroup(), VGroup()
    for ln in lines:
        t = Text(" ".join(ln), font=font, font_size=size, color=color, slant=slant)
        k = 0
        row = VGroup()
        for w in ln:
            n = len(w)
            row.add(VGroup(*t.submobjects[k:k + n]))
            k += n
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=line_buff)
    for r in rows:
        out.add(*r.submobjects)
    return out


def check(color=C_GREEN, s=0.25):
    return VMobject(stroke_color=color, stroke_width=5).set_points_as_corners([LEFT * s + UP * 0.0, LEFT * s * 0.3 + DOWN * s * 0.7, RIGHT * s + UP * s * 0.8])


def cross(color=C_RED, s=0.22):
    return VGroup(Line(UL * s, DR * s, color=color, stroke_width=5), Line(UR * s, DL * s, color=color, stroke_width=5))
