"""Chapter 07 — Theorem 3: The Hardware Lottery & the Credit Assignment Barrier."""
from common import *

BENCH = json.load(open(os.path.join(ROOT, "experiments", "dense_vs_sparse.json")))


def chip(name, sub, color, w=2.6, h=1.7):
    body = RoundedRectangle(width=w, height=h, corner_radius=0.12, color=color, stroke_width=2.5).set_fill(color, 0.1)
    pins = VGroup(*[Line(UP * 0.12, DOWN * 0.12, color=C_GREY, stroke_width=2).move_to(body.get_top() + RIGHT * x + UP * 0.12) for x in np.linspace(-w / 2 + 0.2, w / 2 - 0.2, 9)])
    pins.add(*[p.copy().move_to(body.get_bottom() + RIGHT * (p.get_x() - body.get_x()) + DOWN * 0.12) for p in pins[:9]])
    die = Square(h * 0.45, color=color, stroke_width=1.5).set_fill(color, 0.3).move_to(body)
    lab = VGroup(T(name, size=20, color=color, weight=BOLD), T(sub, size=14, color=C_GREY)).arrange(DOWN, buff=0.05).next_to(body, DOWN, buff=0.25)
    return VGroup(pins, body, die, lab)


class Ch07(Chapter):
    CH = 7

    def construct(self):
        C = self.times(
            "Our third", "forged in physical silicon", "Theorem 3", "In 2019", "The Bitter Lesson", "His conclusion", "biggest lesson",
            "general methods", "most effective", "This principle", "Hardware Lottery", "success of an AI", "fits existing",
            "theoretical elegance", "Modern AI supercomputers", "H100s", "TPU", "wafer-scale", "not biological brain",
            "dense systolic", "When performing dense", "computational utilization", "petaflops", "streaming contiguous", "on-chip SRAM",
            "Hopper architecture", "16 by 16", "per clock cycle", "Any deviation", "stalls the execution", "sacrificing up to",
            "Now examine", "self-rewiring sparse", "Pointers, irregular", "dynamic edge mutations", "thrash", "DRAM latency",
            "uncoalesced", "plunging hardware", "less than", "Furthermore, consider", "Reverse-mode automatic",
            "exact analytical gradient", "single backward pass", "Local plasticity rules lack", "localized node perturbations",
            "variance of the gradient", "scales exponentially", "sequence length T", "Without global backpropagation",
            "wander blindly", "while dense Transformers", "scale monotonically", "compute dollar")
        frame = self.camera.frame
        tag = T("07 · THEOREM 3 — THE HARDWARE LOTTERY", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        card = VGroup(RoundedRectangle(width=4.4, height=2.5, corner_radius=0.15, color=C_ORANGE, stroke_width=2).set_fill(C_ORANGE, 0.08),
                      VGroup(T("Theorem 3", size=30, color=C_ORANGE, weight=BOLD), T("hardware lottery", size=20)).arrange(DOWN, buff=0.15))
        self.add(card, tag)
        head = VGroup(T("Theorem 3", size=26, color=C_ORANGE, weight=BOLD), T("Hardware lottery & credit assignment", size=22)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.75)
        wafer = Circle(2.6, color=C_GREY, stroke_width=2).set_fill(C_DIM, 0.3)
        dies = VGroup(*[Square(0.38).set_stroke(C_ORANGE, 1).set_fill(C_ORANGE, 0.12).move_to([x, y, 0])
                        for x in np.arange(-2.2, 2.3, 0.44) for y in np.arange(-2.2, 2.3, 0.44) if x * x + y * y < 2.3 ** 2])
        self.go("Our third", Indicate(card, color=C_ORANGE), rt=1.0)
        self.go("forged in physical silicon", card.animate.scale(0.5).to_edge(UP, buff=1.0).set_opacity(0), FadeIn(wafer), FadeIn(dies, lag_ratio=0.005), rt=1.4)
        self.go("Theorem 3", FadeIn(head, shift=DOWN * 0.2), VGroup(wafer, dies).animate.scale(0.45).to_corner(DR, buff=0.4), rt=1.4)
        self.remove(card)

        # ── The Bitter Lesson: the real essay, the exact sentence ──────────────────────
        bl = framed_image(os.path.join(ASSETS, "shots", "bitter_lesson_top.png"), height=2.6).move_to(LEFT * 2.8 + UP * 1.2)
        im = bl[0]
        hl_rect = Rectangle(width=im.width * 0.99, height=im.height * 0.09).set_stroke(width=0).set_fill(C_YELLOW, 0.3)
        hl_rect.move_to(im.get_top() + DOWN * im.height * 0.455)
        hl2 = hl_rect.copy().shift(DOWN * im.height * 0.07).stretch(0.12, 0, about_edge=LEFT)
        self.go("In 2019", FadeIn(bl, shift=RIGHT), rt=1.0)
        self.go("The Bitter Lesson", Indicate(bl[1], color=WHITE), rt=0.8)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=4.6, y_length=2.8, axis_config=dict(color=C_GREY, include_tip=False)).move_to(LEFT * 2.8 + DOWN * 2.0)
        axl = VGroup(T("compute →", size=16, color=C_GREY).next_to(ax.x_axis, DOWN, buff=0.1), T("performance", size=16, color=C_GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.1))
        tr = ValueTracker(0.01)
        xs = np.linspace(0, 10, 100)
        hk = ax.plot(lambda x: 5 * (1 - np.exp(-x)) + 0.2, x_range=[0, 10], color=C_PINK)
        gm = ax.plot(lambda x: 0.9 * x + 0.2, x_range=[0, 10], color=C_GREEN)
        hkl = T("built-in human knowledge", size=14, color=C_PINK).next_to(ax.c2p(10, 5.2), UP, buff=0.05).shift(LEFT * 0.6)
        gml = T("search + learning", size=14, color=C_GREEN).next_to(ax.c2p(9, 8.4), LEFT, buff=0.1)
        self.go("His conclusion", Create(ax), FadeIn(axl), rt=0.8)
        self.go("biggest lesson", FadeIn(hl_rect), Create(hk), FadeIn(hkl), rt=1.4)
        self.go("general methods", FadeIn(hl2), Create(gm), FadeIn(gml), rt=1.6)
        self.go("most effective", Indicate(gm, color=WHITE), rt=1.0, upto="This principle")

        # ── Hooker's Hardware Lottery: shapes of ideas vs. the shape of the chip ──────
        page = PaperPage("lottery", 0, height=6.4).move_to(RIGHT * 3.4 + DOWN * 1.6)
        h1 = page.hl("hardware lottery to describe when a")
        h2 = page.hl("research idea wins because it is suited to the available software and hard")
        self.go("This principle", FadeIn(page, shift=LEFT), FadeOut(Group(bl, hl_rect, hl2)), rt=1.0)
        self.go("Hardware Lottery", FadeIn(h1), frame.animate.scale(0.6).move_to(h1.get_center() + LEFT * 1.0), rt=1.2)
        self.go("success of an AI", FadeIn(h2), rt=0.8)
        self.go("fits existing", frame.animate.scale(1 / 0.6).move_to(ORIGIN), FadeOut(Group(page, h1, h2, ax, axl, hk, gm, hkl, gml)), rt=1.2)
        slot = VGroup(Rectangle(width=6, height=0.2).set_stroke(width=0).set_fill(C_GREY, 1).shift(LEFT * 1.8),
                      Rectangle(width=6, height=0.2).set_stroke(width=0).set_fill(C_GREY, 1).shift(RIGHT * 4.2))
        slot.move_to(DOWN * 1.0)
        hole = Square(1.0, color=C_ORANGE, stroke_width=3).move_to(slot.get_center() + DOWN * 0.0)
        hw_l = T("existing hardware: dense matrix tiles", size=18, color=C_ORANGE).next_to(slot, DOWN, buff=0.3)
        ideas = VGroup(Square(0.9, color=C_BLUE, stroke_width=3).set_fill(C_BLUE, 0.4), Circle(0.5, color=C_GREEN, stroke_width=3).set_fill(C_GREEN, 0.4),
                       Triangle(color=C_PINK, stroke_width=3).set_fill(C_PINK, 0.4).scale(0.6), Star(6, outer_radius=0.55, color=C_YELLOW, stroke_width=3).set_fill(C_YELLOW, 0.4))
        ideas.arrange(RIGHT, buff=0.9).move_to(UP * 2.0)
        il = VGroup(*[T(s, size=14, color=c) for s, c in [("dense GEMM", C_BLUE), ("sparse graph", C_GREEN), ("spiking", C_PINK), ("dynamic rewiring", C_YELLOW)]])
        for l, i in zip(il, ideas):
            l.next_to(i, UP, buff=0.15)
        self.then(FadeIn(slot), Create(hole), FadeIn(hw_l), FadeIn(ideas, lag_ratio=0.2), FadeIn(il, lag_ratio=0.2), rt=1.0, upto="theoretical elegance")
        drops = []
        for k, idea in enumerate(ideas):
            drops.append(Succession(idea.animate(run_time=0.4).move_to(hole.get_center() + UP * 1.0),
                                    idea.animate(run_time=0.4).move_to(hole.get_center() + DOWN * 1.4) if k == 0 else
                                    idea.animate(run_time=0.4, rate_func=there_and_back).shift(DOWN * 0.45).set_color(C_RED)))
        self.go("theoretical elegance", LaggedStart(*drops, lag_ratio=0.5), FadeOut(il), rt=2.6, upto="Modern AI supercomputers")

        # ── the chips; zoom into a systolic tensor engine ─────────────────────────────
        self.go("Modern AI supercomputers", FadeOut(VGroup(slot, hole, hw_l, ideas, wafer, dies)), rt=0.6)
        chips = VGroup(chip("NVIDIA H100", "Hopper · tensor cores", C_GREEN), chip("Google TPU v5e", "MXU systolic arrays", C_BLUE),
                       chip("Cerebras WSE", "wafer-scale engine", C_ORANGE, w=2.2, h=2.2)).arrange(RIGHT, buff=0.8).move_to(UP * 0.4)
        for key, c_ in zip(["H100s", "TPU", "wafer-scale"], chips):
            self.go(key, FadeIn(c_, shift=UP * 0.3), rt=0.6)
        brain = VGroup(*[Dot(radius=0.04, color=C_GREEN).move_to(DOWN * 2.6 + np.array([np.cos(a) * 1.0, np.sin(a) * 0.5, 0]) * np.random.rand()) for a in np.linspace(0, TAU, 30)])
        nob = VGroup(brain, cross().scale(1.5).move_to(DOWN * 2.6), T("not brain emulators", size=18, color=C_RED).next_to(DOWN * 2.6, RIGHT, buff=1.4))
        self.go("not biological brain", FadeIn(nob), rt=0.8)
        arr = systolic(10, 10, cell=0.34, color=C_ORANGE).move_to(RIGHT * 1.0 + DOWN * 0.3)
        wf = ValueTracker(-4)
        self.go("dense systolic", FadeOut(nob), FadeOut(chips[0]), FadeOut(chips[2]), ReplacementTransform(chips[1], arr), rt=1.2)
        wavefront(arr, wf)

        # dense GEMM: tiles of A from the left, B from the top, contiguous, in lockstep
        hbm = RoundedRectangle(width=2.0, height=4.6, corner_radius=0.1, color=C_GREY).move_to(LEFT * 5.2 + DOWN * 0.3)
        hbm_l = T("HBM", size=18, color=C_GREY).next_to(hbm, UP, buff=0.1)
        sram = RoundedRectangle(width=1.2, height=3.6, corner_radius=0.1, color=C_TEAL).move_to(LEFT * 2.8 + DOWN * 0.3)
        sram_l = T("SRAM", size=18, color=C_TEAL).next_to(sram, UP, buff=0.1)
        blocks = VGroup(*[Rectangle(width=1.6, height=0.32).set_stroke(C_BLUE, 1).set_fill(C_BLUE, 0.35) for _ in range(12)]).arrange(DOWN, buff=0.05).move_to(hbm)
        p1 = Line(hbm.get_right(), sram.get_left())
        p2 = Line(sram.get_right(), arr.get_left())
        s1 = Stream(p1, n=8, speed=0.9, color=C_BLUE, radius=0.08, square=True)
        s2 = Stream(p2, n=8, speed=0.9, color=C_TEAL, radius=0.08, square=True)
        self.go("When performing dense", FadeIn(hbm), FadeIn(hbm_l), FadeIn(blocks, lag_ratio=0.05), FadeIn(sram), FadeIn(sram_l), rt=1.0)
        self.then(wf.animate(rate_func=linear).set_value(22), rt=1.6, upto="computational utilization")
        util = ValueTracker(0)
        gauge_bg = Rectangle(width=0.5, height=3.6, color=C_DIM).set_fill(C_DIM, 0.3).move_to(RIGHT * 5.6 + DOWN * 0.3)
        gauge = always_redraw(lambda: Rectangle(width=0.5, height=max(0.01, 3.6 * util.get_value())).set_stroke(width=0)
                              .set_fill(interpolate_color(ManimColor(C_RED), ManimColor(C_GREEN), util.get_value()), 0.9).move_to(gauge_bg.get_bottom(), aligned_edge=DOWN))
        upct = always_redraw(lambda: VGroup(Integer(int(100 * util.get_value()), font_size=32), T("%", size=20)).arrange(RIGHT, buff=0.05).next_to(gauge_bg, UP, buff=0.15))
        ul = T("utilization", size=16, color=C_GREY).next_to(gauge_bg, DOWN, buff=0.12)
        self.add(gauge_bg, gauge, upct)
        self.go("computational utilization", util.animate.set_value(0.93), FadeIn(ul), wf.animate(rate_func=linear).set_value(-4), rt=1.6)
        pf = VGroup(M(r"\sim 10^{15}", size=34, color=C_ORANGE), T("FLOP/s", size=18, color=C_ORANGE)).arrange(RIGHT, buff=0.1).next_to(arr, UP, buff=0.2)
        self.go("petaflops", Write(pf), wf.animate(rate_func=linear).set_value(22), rt=1.4)
        self.add(s1, s2)
        self.go("streaming contiguous", FadeIn(s1), wf.animate(rate_func=linear).set_value(-4), rt=1.4)
        self.go("on-chip SRAM", FadeIn(s2), Indicate(sram, color=C_TEAL), wf.animate(rate_func=linear).set_value(22), rt=1.4)
        tile = SurroundingRectangle(arr[0:1], buff=0).set_stroke(width=0)
        t16 = Square(arr.width * 1.0, color=C_YELLOW, stroke_width=4).move_to(arr)
        t16l = T("16 × 16 MMA tile", size=18, color=C_YELLOW).next_to(arr, DOWN, buff=0.2)
        clk = counter(0, size=26, color=C_YELLOW).next_to(t16l, DOWN, buff=0.1)
        clk_l = T("clock", size=14, color=C_GREY).next_to(clk, LEFT, buff=0.15)
        self.go("Hopper architecture", wf.animate(rate_func=linear).set_value(-4), rt=1.2)
        self.go("16 by 16", Create(t16), FadeIn(t16l), FadeIn(clk), FadeIn(clk_l), rt=0.8)
        self.go("per clock cycle", clk.tracker.animate(rate_func=linear).set_value(48), wf.animate(rate_func=linear).set_value(22), rt=1.8, upto="Any deviation")
        # a single irregularity: the stream breaks, PEs idle
        self.go("Any deviation", s1.speed.animate.set_value(0.08), s2.speed.animate.set_value(0.08), rt=0.8)
        self.go("stalls the execution", util.animate.set_value(0.05), arr.animate.set_color(C_DIM), rt=1.2)
        self.go("sacrificing up to", Indicate(upct, color=C_RED), rt=0.8, upto="Now examine")

        # ── a self-rewiring sparse graph on the same machine: pointer chasing ─────────
        arr.clear_updaters()
        self.go("Now examine", FadeOut(VGroup(t16, t16l, clk, clk_l, pf, s1, s2, hbm_l, sram_l)), FadeOut(blocks), rt=0.6)
        self.remove(s1, s2)
        mem = VGroup(*[Square(0.22).set_stroke(C_DIM, 1).set_fill(C_DIM, 0.2) for _ in range(16 * 20)]).arrange_in_grid(20, 16, buff=0.02).move_to(hbm)
        mem.stretch_to_fit_height(4.4).stretch_to_fit_width(1.9)
        self.go("self-rewiring sparse", ReplacementTransform(hbm, mem), arr.animate.set_color(C_ORANGE).set_fill(opacity=0.05), rt=1.0)
        rngp = np.random.default_rng(4)
        addrs = rngp.integers(0, len(mem), 18)
        chase = VGroup()
        for a, b in zip(addrs, addrs[1:]):
            chase.add(CurvedArrow(mem[a].get_center(), mem[b].get_center(), angle=0.8, color=C_RED, stroke_width=2, tip_length=0.1))
        self.go("Pointers, irregular", LaggedStart(*[Succession(Create(c), mem[b].animate.set_fill(C_RED, 0.9)) for c, b in zip(chase, addrs[1:])], lag_ratio=0.25), rt=2.4)
        cache = VGroup(*[Rectangle(width=1.0, height=0.28).set_stroke(C_TEAL, 1).set_fill(C_TEAL, 0.2) for _ in range(8)]).arrange(DOWN, buff=0.04).move_to(sram)
        miss = T("MISS", size=22, color=C_RED, weight=BOLD).next_to(sram, DOWN, buff=0.25)
        self.go("dynamic edge mutations", ReplacementTransform(sram, cache), rt=0.6)
        self.go("thrash", LaggedStart(*[Succession(c.animate(run_time=0.15).set_fill(C_RED, 0.8), c.animate(run_time=0.15).set_fill(C_TEAL, 0.2)) for c in [*cache, *cache[::-1]]], lag_ratio=0.15),
                FadeIn(miss), rt=1.8)
        lat = VGroup(T("DRAM latency", size=16, color=C_GREY), counter(0, unit="ns", size=30, color=C_RED)).arrange(RIGHT, buff=0.2).next_to(arr, UP, buff=0.25)
        self.go("DRAM latency", FadeIn(lat), rt=0.3)
        self.then(lat[1].tracker.animate.set_value(112), rt=1.0, upto="uncoalesced")
        rnd = [arr[i] for i in rngp.choice(len(arr), 8, replace=False)]
        self.go("uncoalesced", *[r.animate.set_fill(C_ORANGE, 0.9) for r in rnd], Flash(miss, color=C_RED), rt=0.8)
        self.go("plunging hardware", util.animate.set_value(0.4), rt=0.4)
        self.then(util.animate.set_value(0.07), rt=1.0, upto="less than")
        # the real measurement on this laptop
        mb = BENCH.get("mps", BENCH["cpu"])
        bench_bg = RoundedRectangle(width=5.4, height=2.0, corner_radius=0.15, stroke_color=C_YELLOW, stroke_width=1.5).set_fill(BG, 0.95).move_to(LEFT * 2.6 + UP * 1.55)
        lg = lambda v: np.log10(max(v, 1))
        b1 = Rectangle(width=3.6 * lg(mb["dense_gflops"]) / 3.3, height=0.42).set_stroke(width=0).set_fill(C_ORANGE, 0.9)
        b2 = Rectangle(width=3.6 * lg(mb["sparse_gflops"]) / 3.3 + 0.03, height=0.42).set_stroke(width=0).set_fill(C_GREEN, 0.9)
        rows = VGroup(VGroup(T("dense GEMM", size=16, color=C_ORANGE), b1, T(f"{mb['dense_gflops']:.0f} GFLOP/s", size=16)).arrange(RIGHT, buff=0.15),
                      VGroup(T("sparse gather", size=16, color=C_GREEN), b2, T(f"{mb['sparse_gflops']:.1f} GFLOP/s", size=16)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rows.move_to(bench_bg).shift(DOWN * 0.15)
        btitle = T(f"measured on this M3 · {mb['dense_gflops'] / mb['sparse_gflops']:.0f}× gap", size=16, color=C_YELLOW).next_to(bench_bg.get_top(), DOWN, buff=0.15)
        self.go("less than", FadeIn(bench_bg), FadeIn(btitle), rt=0.4)
        self.then(GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT), FadeIn(rows[0][0]), FadeIn(rows[1][0]), FadeIn(rows[0][2]), FadeIn(rows[1][2]), rt=1.2, upto="Furthermore, consider")

        # ── credit assignment: exact backward pass vs noisy local perturbation ─────────
        self.go("Furthermore, consider", FadeOut(self.stage(tag, head)), rt=0.8)
        self.remove(gauge, upct)
        chain = VGroup(*[Circle(0.28, color=WHITE, stroke_width=2).set_fill(BLACK, 1) for _ in range(7)]).arrange(RIGHT, buff=0.9).move_to(UP * 1.6)
        labs = VGroup(*[M(s, size=24).move_to(c) for s, c in zip(["x", "h_1", "h_2", "h_3", "h_4", "h_5", r"\mathcal{L}"], chain)])
        fw = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=C_BLUE, stroke_width=3) for a, b in zip(chain[:-1], chain[1:])])
        self.go("Reverse-mode automatic", FadeIn(chain, lag_ratio=0.1), FadeIn(labs, lag_ratio=0.1), LaggedStart(*[GrowArrow(a) for a in fw], lag_ratio=0.2), rt=1.4)
        bw = VGroup(*[CurvedArrow(b.get_bottom() + DOWN * 0.05, a.get_bottom() + DOWN * 0.05, angle=-0.9, color=C_RED, stroke_width=3, tip_length=0.15) for a, b in zip(chain[:-1], chain[1:])][::-1])
        geq = M(r"\frac{\partial \mathcal L}{\partial \theta_1}=\frac{\partial \mathcal L}{\partial h_5}\cdots\frac{\partial h_2}{\partial h_1}\frac{\partial h_1}{\partial \theta_1}", size=32, color=C_RED).next_to(chain, DOWN, buff=1.0)
        self.go("exact analytical gradient", LaggedStart(*[Create(b) for b in bw], lag_ratio=0.25), rt=1.6)
        self.go("single backward pass", Write(geq), LaggedStart(*[ShowPassingFlash(b.copy().set_stroke(WHITE, 5)) for b in bw], lag_ratio=0.15), rt=1.6,
                upto="Local plasticity rules lack")
        # local version: no backward arrows; each node guesses with noise
        self.go("Local plasticity rules lack", FadeOut(bw), FadeOut(geq), rt=0.8)
        jit = ValueTracker(0)
        rngj = np.random.default_rng(2)
        phase = rngj.random((6, 2)) * TAU

        def local_guess():
            t = jit.get_value()
            g = VGroup()
            for i, c in enumerate(chain[1:]):
                a = phase[i, 0] + 3 * t * (1 + i * 0.3)
                L = 0.35 + 0.25 * np.sin(phase[i, 1] + 5 * t)
                g.add(Arrow(c.get_bottom(), c.get_bottom() + L * np.array([np.cos(a), -abs(np.sin(a)) - 0.3, 0]), buff=0, color=C_GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.3))
            return g
        lgv = always_redraw(local_guess)
        self.add(lgv)
        self.go("localized node perturbations", jit.animate(rate_func=linear).set_value(1.5), rt=1.6)
        # variance cloud vs horizon T
        vax = Axes(x_range=[-4, 4], y_range=[-3, 3], x_length=5.0, y_length=3.0, axis_config=dict(color=C_DIM, include_tip=False)).move_to(LEFT * 3.2 + DOWN * 1.6)
        Tt = ValueTracker(1)
        true_g = np.array([1.5, 0.8])
        samp = rngj.normal(size=(140, 2))

        def vcloud():
            s = 0.25 * np.exp(0.17 * Tt.get_value())
            return VGroup(*[Dot(vax.c2p(*np.clip(true_g + s * z, [-4, -3], [4, 3])), radius=0.045, color=C_GREEN).set_opacity(0.8) for z in samp])
        vc = always_redraw(vcloud)
        tg = Arrow(vax.c2p(0, 0), vax.c2p(*true_g), buff=0, color=C_RED, stroke_width=4)
        Tl = always_redraw(lambda: M(r"T = %d" % int(Tt.get_value()), size=32, color=C_YELLOW).next_to(vax, UP, buff=0.1))
        vplot = Axes(x_range=[0, 20, 5], y_range=[0, 40, 10], x_length=4.2, y_length=2.6, axis_config=dict(color=C_GREY, include_tip=False, font_size=16),
                     x_axis_config=dict(include_numbers=True)).move_to(RIGHT * 3.6 + DOWN * 1.6)
        vpl = VGroup(T("horizon T", size=14, color=C_GREY).next_to(vplot.x_axis, DOWN, buff=0.3), M(r"\mathrm{Var}[\hat g]\propto e^{cT}", size=26, color=C_GREEN).next_to(vplot, UP, buff=0.05))
        vcurve = always_redraw(lambda: vplot.plot(lambda x: min(40, 0.12 * np.exp(0.36 * x) * 4), x_range=[0, max(0.1, Tt.get_value())], color=C_GREEN))
        self.go("variance of the gradient", Create(vax), GrowArrow(tg), rt=0.6)
        self.add(vc, Tl)
        self.then(Create(vplot), FadeIn(vpl), jit.animate(rate_func=linear).set_value(3), rt=1.0)
        self.add(vcurve)
        self.go("scales exponentially", Tt.animate(rate_func=linear).set_value(8), jit.animate(rate_func=linear).set_value(5), rt=1.6)
        self.go("sequence length T", Tt.animate(rate_func=linear).set_value(16), jit.animate(rate_func=linear).set_value(7), rt=1.8, upto="Without global backpropagation")

        # ── outcomes: blind wandering vs monotone scaling with compute ─────────────────
        self.remove(lgv, vc, Tl, vcurve)
        self.go("Without global backpropagation", FadeOut(self.stage(tag, head)), rt=0.8)
        land = Axes(x_range=[-3, 3], y_range=[-2, 2], x_length=5.6, y_length=3.8, axis_config=dict(stroke_opacity=0)).move_to(LEFT * 3.4 + DOWN * 0.3)
        rings = VGroup(*[Ellipse(width=5.4 * k / 6, height=3.6 * k / 6, color=C_PURPLE, stroke_width=1.4, stroke_opacity=0.5 + 0.08 * k).move_to(land.c2p(0.6, -0.3)) for k in range(1, 7)])
        rw = [np.array([-2.4, 1.4])]
        rngr = np.random.default_rng(9)
        for _ in range(90):
            rw.append(np.clip(rw[-1] + 0.28 * rngr.normal(size=2), [-2.8, -1.8], [2.8, 1.8]))
        gd = [np.array([-2.4, 1.4])]
        for _ in range(40):
            p = gd[-1]; g = np.array([(p[0] - 0.6) / 1.4, (p[1] + 0.3) / 0.6])
            gd.append(p - 0.12 * g)
        kk = ValueTracker(0)
        rwp = always_redraw(lambda: VMobject(stroke_color=C_GREEN, stroke_width=2).set_points_as_corners([land.c2p(*q) for q in rw[:max(2, int(kk.get_value() * 90))]]))
        gdp = always_redraw(lambda: VMobject(stroke_color=C_BLUE, stroke_width=3).set_points_as_corners([land.c2p(*q) for q in gd[:max(2, int(kk.get_value() * 40))]]))
        self.then(Create(rings, lag_ratio=0.1), rt=0.6)
        self.add(rwp)
        lgl = VGroup(T("local rules: random walk", size=16, color=C_GREEN), T("backprop: descent", size=16, color=C_BLUE)).arrange(DOWN, aligned_edge=LEFT).next_to(land, UP, buff=0.1)
        self.go("wander blindly", kk.animate(rate_func=linear).set_value(0.7), FadeIn(lgl[0]), rt=2.0)
        self.add(gdp)
        self.go("while dense Transformers", kk.animate(rate_func=linear).set_value(1.0), FadeIn(lgl[1]), rt=1.2)
        sl = Axes(x_range=[18, 26, 2], y_range=[0, 4, 1], x_length=4.6, y_length=3.0, axis_config=dict(color=C_GREY, include_tip=False, font_size=16),
                  x_axis_config=dict(include_numbers=True)).move_to(RIGHT * 3.6 + DOWN * 0.3)
        sll = VGroup(M(r"\log_{10}\text{compute (FLOPs)}", size=20, color=C_GREY).next_to(sl.x_axis, DOWN, buff=0.35), T("loss", size=16, color=C_GREY).next_to(sl, UP, buff=0.05))
        trn = sl.plot(lambda x: 3.6 * 10 ** (-0.05 * (x - 18)), x_range=[18, 26], color=C_BLUE)
        son = sl.plot(lambda x: 3.2 + 0.15 * np.sin(5 * x), x_range=[18, 26], color=C_GREEN)
        self.go("scale monotonically", Create(sl), FadeIn(sll), Create(trn), rt=1.6)
        self.go("compute dollar", Create(son), rt=1.0)
        self.finish()
