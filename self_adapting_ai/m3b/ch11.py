"""Chapter 11 — Ideas of my own: four research directions, each shown as a working mechanism."""
from common import *

TILE = json.load(open(os.path.join(ROOT, "experiments", "tile_sparsity.json")))["cpu"]


def notebook_card(title, idx, color):
    box = RoundedRectangle(width=3.2, height=1.1, corner_radius=0.12, color=color, stroke_width=2).set_fill(color, 0.08)
    txt = VGroup(T(f"idea {idx}", size=14, color=C_GREY), T(title, size=18, color=color, weight=BOLD)).arrange(DOWN, buff=0.06).move_to(box)
    return VGroup(box, txt)


def card_state(c, on):
    """Highlight or dim an idea card without filling its box solid."""
    return AnimationGroup(c[0].animate.set_stroke(opacity=1 if on else 0.25).set_fill(opacity=0.12 if on else 0.02),
                          c[1].animate.set_opacity(1 if on else 0.3))


class Ch11(Chapter):
    CH = 11

    def construct(self):
        C = self.times(
            "Before we look", "ideas of my own", "research directions", "may be wrong", "worth someone's PhD", "The first idea",
            "rewire tiles", "starve the GPU", "does not see synapses", "small dense tiles", "So what if structural", "growing and pruning whole",
            "the way RigL", "still rewires", "stays dense", "On my laptop", "five and a half", "naive implementation", "A real block-sparse",
            "The second idea", "spectral homeostasis", "collapses toward", "homeostatic plasticity", "shape of the spectrum", "gently pushed back",
            "measure locally", "The question I would", "keep many modes", "The third idea", "let the network sleep", "fast learning from slow",
            "hippocampus records", "sleep replays", "could do the same", "written during every", "Then, offline", "Plasticity at inference",
            "Two timescales", "catastrophic forgetting", "And the fourth", "three-factor learning", "eligibility traces", "single broadcast",
            "approximate backpropagation", "Pair that with", "might finally be tamed", "If any of these", "run with it", "moves forward")
        frame = self.camera.frame
        tag = T("11 · IDEAS OF MY OWN", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        self.add(tag)
        rng = np.random.default_rng(11)

        # ── a notebook page with four empty slots ─────────────────────────────────────
        lines = VGroup(*[Line(LEFT * 6.4, RIGHT * 6.4, color=C_BLUE, stroke_width=1, stroke_opacity=0.12).shift(UP * (3.2 - 0.45 * i)) for i in range(15)])
        margin = Line(UP * 3.6 + LEFT * 5.6, DOWN * 3.6 + LEFT * 5.6, color=C_RED, stroke_width=1.2, stroke_opacity=0.35)
        head = T("research directions", size=40, weight=BOLD).move_to(UP * 2.4)
        cards = VGroup(*[notebook_card(t, i + 1, c) for i, (t, c) in enumerate(
            [("tile-level rewiring", C_ORANGE), ("spectral homeostasis", C_YELLOW), ("sleep & consolidation", C_PURPLE), ("three-factor credit", C_GREEN)])])
        cards.arrange_in_grid(2, 2, buff=(0.6, 0.4)).move_to(DOWN * 0.4)
        self.go("Before we look", Create(lines, lag_ratio=0.05), Create(margin), rt=1.2)
        self.go("ideas of my own", Write(head), rt=1.0)
        self.go("research directions", LaggedStart(*[FadeIn(c[0]) for c in cards], lag_ratio=0.2), rt=1.0)
        qm = T("?", size=60, color=C_GREY).next_to(head, RIGHT, buff=0.3)
        self.go("may be wrong", FadeIn(qm, scale=1.5), rt=0.6)
        self.go("worth someone's PhD", LaggedStart(*[FadeIn(c[1]) for c in cards], lag_ratio=0.2), FadeOut(qm), rt=1.2, upto="The first idea")
        page = VGroup(lines, margin)

        # ── idea 1: rewire tiles, not synapses ─────────────────────────────────────────
        dock = cards.copy().scale(0.62).arrange(DOWN, buff=0.18).to_edge(RIGHT, buff=0.25).shift(DOWN * 0.3)
        self.go("The first idea", FadeOut(head), *[c.animate.move_to(d_).scale(0.62) for c, d_ in zip(cards, dock)], page.animate.set_opacity(0.4), rt=1.0)
        self.then(*[card_state(c, i == 0) for i, c in enumerate(cards)], rt=0.4)
        n, cell = 16, 0.24
        grid = VGroup(*[Square(cell).set_stroke(C_DIM, 0.6).set_fill(C_DIM, 0.15) for _ in range(n * n)]).arrange_in_grid(n, n, buff=0.02).move_to(LEFT * 3.6 + DOWN * 0.5)
        mask = rng.random(n * n) < 0.1
        self.go("rewire tiles", FadeIn(grid, lag_ratio=0.001), rt=0.8)
        self.then(*[grid[i].animate.set_fill(C_GREEN, 0.95) for i in np.nonzero(mask)[0]], rt=0.8)
        unl = T("90% sparse · scattered synapses", size=16, color=C_GREEN).next_to(grid, DOWN, buff=0.2)
        self.go("starve the GPU", FadeIn(unl), LaggedStart(*[Indicate(grid[i], color=C_RED, scale_factor=1.4) for i in np.nonzero(mask)[0][:20]], lag_ratio=0.05), rt=1.4)
        tiles = VGroup(*[Square(cell * 4 + 0.06).set_stroke(C_ORANGE, 2.2).set_fill(opacity=0) for _ in range(16)]).arrange_in_grid(4, 4, buff=0.02).move_to(grid)
        self.go("does not see synapses", Create(tiles, lag_ratio=0.05), rt=1.0)
        self.go("small dense tiles", Indicate(tiles, color=C_ORANGE, scale_factor=1.02), rt=0.8)
        # tile-level plasticity: whole blocks grow and prune; survivors are dense
        keep = [1, 6, 11, 12]
        def block_cells(b):
            bi, bj = divmod(b, 4)
            return [grid[(bi * 4 + i) * n + bj * 4 + j] for i in range(4) for j in range(4)]
        self.go("So what if structural", *[sq.animate.set_fill(C_DIM, 0.15) for sq in grid], rt=0.6)
        self.go("growing and pruning whole", *[sq.animate.set_fill(C_ORANGE, 0.9) for b in keep for sq in block_cells(b)], rt=0.9)
        for grow, prune in [(3, 6), (9, 1)]:
            self.play(*[sq.animate.set_fill(C_ORANGE, 0.9) for sq in block_cells(grow)], *[sq.animate.set_fill(C_RED, 0.5) for sq in block_cells(prune)], run_time=0.45)
            self.play(*[sq.animate.set_fill(C_DIM, 0.15) for sq in block_cells(prune)], run_time=0.3)
        rigl = T("grow / prune whole tiles (RigL-style, by magnitude & gradient)", size=16, color=C_ORANGE).next_to(grid, UP, buff=0.2)
        self.go("the way RigL", FadeIn(rigl), FadeOut(unl), rt=0.6)
        self.go("still rewires", *[Indicate(sq, color=WHITE, scale_factor=1.05) for b in (3, 9) for sq in block_cells(b)], rt=0.8)
        self.go("stays dense", Flash(tiles[11], color=C_ORANGE), rt=0.6, upto="On my laptop")
        # measured throughput, log scale
        bars_bg = RoundedRectangle(width=5.0, height=3.0, corner_radius=0.15, stroke_color=C_DIM).set_fill(BG, 0.95).move_to(RIGHT * 1.3 + DOWN * 0.6)
        lg = lambda v: np.log10(max(v, 1.0))
        rows = []
        for nm, key, col in [("dense matmul", "dense_gflops", C_BLUE), ("16×16 tiles", "tile16_gflops", C_ORANGE), ("scattered synapses", "unstructured_gflops", C_GREEN)]:
            b = Rectangle(width=0.05 + 2.4 * lg(TILE[key]) / 3.0, height=0.36).set_stroke(width=0).set_fill(col, 0.9)
            rows.append(VGroup(T(nm, size=15, color=col), b, T(f"{TILE[key]:.1f} GFLOP/s", size=14)).arrange(RIGHT, buff=0.15))
        rows = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(bars_bg).shift(DOWN * 0.15)
        bt = T("same 90% sparsity · measured on this M3 (log scale)", size=14, color=C_YELLOW).next_to(bars_bg.get_top(), DOWN, buff=0.12)
        self.go("On my laptop", FadeIn(bars_bg), FadeIn(bt), *[FadeIn(r[0]) for r in rows], rt=0.6)
        self.then(*[GrowFromEdge(r[1], LEFT) for r in rows], *[FadeIn(r[2]) for r in rows], rt=1.2)
        ratio = TILE["tile16_gflops"] / TILE["unstructured_gflops"]
        ratio_l = T(f"{ratio:.1f}× faster than scattered", size=20, color=C_ORANGE, weight=BOLD).next_to(bars_bg, DOWN, buff=0.2)
        self.go("five and a half", Write(ratio_l), Indicate(rows[1], color=C_ORANGE), rt=1.0)
        self.go("A real block-sparse", Indicate(rows[0], color=C_BLUE), rt=1.0, upto="The second idea")

        # ── idea 2: spectral homeostasis ─────────────────────────────────────────────
        self.go("The second idea", FadeOut(VGroup(grid, tiles, rigl, bars_bg, bt, rows, ratio_l)), card_state(cards[0], False), card_state(cards[1], True), rt=1.0)
        base = Line(LEFT * 6.0, LEFT * 0.6, color=C_GREY).move_to(LEFT * 3.3 + DOWN * 2.2)
        K = 12
        lam = ValueTracker(0)        # 0 → healthy spread, 1 → collapsed

        def spec():
            a = lam.get_value()
            hs = [(1 - a) * 2.2 * 0.85 ** i + a * (2.4 if i == 0 else 0.03) for i in range(K)]
            return VGroup(*[Rectangle(width=0.32, height=max(0.02, h)).set_stroke(width=0).set_fill(C_YELLOW if i == 0 else C_TEAL, 0.9)
                            .move_to(base.get_left() + RIGHT * (0.3 + i * 0.42), aligned_edge=DOWN) for i, h in enumerate(hs)])
        sp = always_redraw(spec)
        self.go("spectral homeostasis", Create(base), rt=0.4)
        self.add(sp)
        rk = always_redraw(lambda: VGroup(T("effective rank", size=16, color=C_GREY), DecimalNumber(1 + 10 * (1 - lam.get_value()) ** 1.5, num_decimal_places=1, font_size=34, color=C_YELLOW))
                           .arrange(DOWN, buff=0.08).next_to(base, UP, buff=2.8).align_to(base, LEFT))
        self.add(rk)
        self.go("collapses toward", lam.animate.set_value(0.9), rt=1.8)
        thermo = VGroup(RoundedRectangle(width=0.5, height=3.0, corner_radius=0.2, color=C_GREY).set_fill(C_DIM, 0.2))
        thermo.move_to(RIGHT * 0.9 + DOWN * 0.6)
        target = DashedLine(thermo.get_left() + LEFT * 0.2, thermo.get_right() + RIGHT * 0.2, color=C_GREEN).move_to(thermo.get_center() + UP * 0.6)
        tl_ = T("target rank r*", size=14, color=C_GREEN).next_to(target, RIGHT, buff=0.15)
        lvl = always_redraw(lambda: Rectangle(width=0.4, height=max(0.02, 2.9 * (1 - lam.get_value()))).set_stroke(width=0)
                            .set_fill(interpolate_color(ManimColor(C_RED), ManimColor(C_GREEN), 1 - lam.get_value()), 0.9).move_to(thermo.get_bottom() + UP * 0.05, aligned_edge=DOWN))
        self.go("homeostatic plasticity", FadeIn(thermo), Create(target), FadeIn(tl_), rt=0.8)
        self.add(lvl)
        heq = M(r"\Delta W = \eta\,(yx^{\top} - yy^{\top}W)", r"\;-\;\gamma\,\big(r^{*} - \hat r_{\text{eff}}\big)\,\nabla_W \hat r_{\text{eff}}", size=30).move_to(RIGHT * 0.6 + UP * 2.4)
        heq[1].set_color(C_GREEN)
        prop = T("proposed — not a published rule", size=14, color=C_GREY).next_to(heq, DOWN, buff=0.15)
        self.go("shape of the spectrum", Write(heq[0]), rt=1.0)
        self.go("gently pushed back", Write(heq[1]), FadeIn(prop), lam.animate.set_value(0.25), rt=2.0)
        loc = T("uses only local covariance statistics", size=16, color=C_TEAL).next_to(prop, DOWN, buff=0.3)
        self.go("measure locally", FadeIn(loc), rt=0.6)
        self.go("The question I would", lam.animate.set_value(0.45), rt=1.0)
        self.go("keep many modes", lam.animate.set_value(0.1), Indicate(VGroup(heq), color=C_YELLOW), rt=1.6, upto="The third idea")

        # ── idea 3: sleep — fast memory by day, replay into slow weights by night ────
        self.remove(sp, rk, lvl)
        self.go("The third idea", FadeOut(VGroup(base, thermo, target, tl_, heq, prop, loc)), card_state(cards[1], False), card_state(cards[2], True), rt=1.0)
        sky = ValueTracker(0)        # 0 day, 1 night
        sun = always_redraw(lambda: Circle(0.35, color=C_YELLOW).set_fill(C_YELLOW, 0.8 * (1 - sky.get_value())).set_stroke(opacity=1 - sky.get_value())
                            .move_to(LEFT * 5.2 + UP * (1.8 - 1.2 * sky.get_value())))
        moon = always_redraw(lambda: Circle(0.3, color=C_ICE).set_fill(C_ICE, 0.7 * sky.get_value()).set_stroke(opacity=sky.get_value())
                             .move_to(LEFT * 5.2 + UP * (0.6 + 1.2 * sky.get_value())))
        self.add(sun, moon)
        fastm = heatmap(np.zeros((6, 6)), cell=0.3, cmap=(BLACK, C_PURPLE, WHITE)).move_to(LEFT * 2.6 + DOWN * 0.6)
        fl = T("fast memory (hippocampus · delta-rule weights)", size=14, color=C_PURPLE).next_to(fastm, DOWN, buff=0.15)
        slowm = monolith(6, w=2.0, h=0.34, color=C_ICE).move_to(RIGHT * 1.8 + DOWN * 0.6)
        sl_ = T("slow weights (cortex · backprop)", size=14, color=C_ICE).next_to(slowm, DOWN, buff=0.15)
        self.go("let the network sleep", FadeIn(fastm), FadeIn(fl), FadeIn(slowm), FadeIn(sl_), rt=1.0)
        self.go("fast learning from slow", Indicate(fastm, color=C_PURPLE), Indicate(slowm, color=C_ICE), rt=1.0)
        fv = np.zeros(36)
        chats = VGroup(*[label_box(s, C_PURPLE, size=14) for s in ("chat 1", "chat 2", "chat 3")]).arrange(DOWN, buff=0.15).move_to(LEFT * 5.2 + DOWN * 1.6)
        self.go("hippocampus records", FadeIn(chats, lag_ratio=0.3), rt=0.6)
        for c in chats:
            idx = rng.choice(36, 8, replace=False); fv[idx] = np.clip(fv[idx] + 0.6, 0, 1)
            self.play(c.animate.move_to(fastm).scale(0.3).set_opacity(0), *[fastm[i].animate.set_fill(heat_color(fv[i], (BLACK, C_PURPLE, WHITE))) for i in idx], run_time=0.5)
        self.go("sleep replays", sky.animate.set_value(1), rt=1.0)
        rp = Stream(ArcBetweenPoints(fastm.get_right(), slowm.get_left(), angle=-0.8), n=10, speed=0.6, color=C_PURPLE, radius=0.06)
        self.then(FadeIn(rp), rt=0.4)
        self.go("could do the same", *[sq.animate.set_fill(heat_color(0.0, (BLACK, C_PURPLE, WHITE))) for sq in fastm], slowm.animate.set_color(C_PURPLE), rt=1.6)
        self.go("written during every", sky.animate.set_value(0), slowm.animate.set_color(C_ICE), rt=1.0)
        self.go("Then, offline", sky.animate.set_value(1), rt=1.0)
        two = VGroup(M(r"\text{plasticity at inference}", size=26, color=C_PURPLE), M(r"\text{stability in training}", size=26, color=C_ICE)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        self.go("Plasticity at inference", Write(two), rt=1.2)
        self.go("Two timescales", sky.animate.set_value(0), rt=1.0)
        self.go("catastrophic forgetting", sky.animate.set_value(1), rt=1.4, upto="And the fourth")

        # ── idea 4: three-factor learning (e-prop) ─────────────────────────────────────
        rp.clear_updaters()
        self.remove(sun, moon)
        self.go("And the fourth", FadeOut(VGroup(fastm, fl, slowm, sl_, rp, two)), card_state(cards[2], False), card_state(cards[3], True), rt=1.0)
        pre = Circle(0.35, color=C_BLUE, stroke_width=3).move_to(LEFT * 4.6 + DOWN * 0.2)
        post = Circle(0.35, color=C_PINK, stroke_width=3).move_to(LEFT * 1.4 + DOWN * 0.2)
        syn = Line(pre.get_right(), post.get_left(), color=C_YELLOW, stroke_width=4)
        self.go("three-factor learning", FadeIn(pre), FadeIn(post), Create(syn), rt=0.8)
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1.1, 1], x_length=4.4, y_length=1.6, axis_config=dict(color=C_GREY, include_tip=False)).move_to(RIGHT * 1.6 + UP * 0.9)
        trace = ax.plot(lambda t: np.exp(-(t - 0.6) / 1.4) if t > 0.6 else t / 0.6, x_range=[0, 6], color=C_GREEN)
        el = M(r"e_{ij}(t)", size=28, color=C_GREEN).next_to(ax, LEFT, buff=0.15)
        self.go("eligibility traces", Create(ax), Create(trace), FadeIn(el), Flash(syn.get_center(), color=C_GREEN), rt=1.4)
        wave = Arc(radius=2.2, start_angle=PI * 1.15, angle=PI * 0.7, color=C_ORANGE, stroke_width=4).move_to(LEFT * 3.0 + UP * 2.6)
        ll = M(r"L(t)", size=30, color=C_ORANGE).next_to(wave, UP, buff=0.05)
        self.go("single broadcast", Create(wave), FadeIn(ll), *[ShowPassingFlash(Line(LEFT * 3.0 + UP * 2.4, p).set_stroke(C_ORANGE, 4)) for p in (pre.get_top(), syn.get_center(), post.get_top())], rt=1.2)
        rule = M(r"\Delta w_{ij} = \eta\;", r"L(t)", r"\;\cdot\;", r"e_{ij}(t)", size=40).move_to(RIGHT * 1.6 + DOWN * 1.4)
        rule[1].set_color(C_ORANGE); rule[3].set_color(C_GREEN)
        self.go("approximate backpropagation", Write(rule), syn.animate.set_stroke(width=8), rt=1.4)
        pg = PaperPage("eprop", 0, height=3.6).to_corner(DL, buff=0.4)
        hl = pg.hl("Biologically inspired alternatives to backpropagation through time")
        self.go("Pair that with", FadeIn(pg, shift=UP), FadeIn(hl), rt=0.9)
        self.go("might finally be tamed", Indicate(rule, color=C_YELLOW), rt=1.2, upto="If any of these")

        # ── outro: all four cards light up ─────────────────────────────────────────────
        self.go("If any of these", FadeOut(Group(pre, post, syn, ax, trace, el, wave, ll, rule, pg, hl)), rt=0.8)
        self.then(cards.animate.scale(1 / 0.62).arrange_in_grid(2, 2, buff=(0.6, 0.4)).move_to(DOWN * 0.2), page.animate.set_opacity(1), rt=1.2)
        self.then(*[card_state(c, True) for c in cards], rt=0.4)
        self.go("run with it", LaggedStart(*[Indicate(c, color=WHITE, scale_factor=1.06) for c in cards], lag_ratio=0.25), rt=1.6)
        self.go("moves forward", *[c[0].animate.set_fill(c[0].get_color(), 0.3) for c in cards], rt=1.0)
        self.finish()
