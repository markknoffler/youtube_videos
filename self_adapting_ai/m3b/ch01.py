"""Chapter 01 — The Monolith of Modern AI."""
from common import *


class Ch01(Chapter):
    CH = 1

    def construct(self):
        C = self.times(
            "Look around", "GPT-6", "Claude 5.5", "Gemini 4", "Mythos", "mathematical reasoning", "software synthesis",
            "multi-turn", "remarkable cognitive", "Yet behind", "unsettling", "Every single foundational", "frozen, static monolith",
            "Consider the computational", "several months", "tens of thousands of GPUs", "kilowatt hours",
            "hundreds of billions", "trillions of tokens", "During this training", "updating its numerical",
            "stochastic gradient descent", "But the exact instant", "halts forever", "etched into silicon", "When you query",
            "simple haiku", "algebraic geometry", "not a single synapse", "No new connections", "No outdated",
            "cannot dynamically reallocate", "complexity of your request", "live terminal", "W Q", "high-bandwidth memory",
            "FP16", "Every single incoming", "identical, immutable", "While activations", "rigid and invariant",
            "Why has the entire", "multi-billion", "rigid, unyielding", "In this investigation", "mathematical, physical",
            "hardware forces", "modern AI monolith", "tantalizing dream", "fiercely difficult", "physical silicon")
        frame = self.camera.frame

        # ── opening: a coordinate space draws itself ────────────────────────────────
        plane = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                            background_line_style=dict(stroke_color=C_BLUE, stroke_width=1, stroke_opacity=0.10),
                            axis_config=dict(stroke_opacity=0))
        tag = T("01 · THE MONOLITH", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        title = T("Why Brain-Like AI Failed", size=54, weight=BOLD)
        sub = T("and what we built instead", size=26, color=C_GREY).next_to(title, DOWN)
        self.play(Create(plane, lag_ratio=0.02), Write(title), run_time=2.0)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)

        # ── the frontier landscape: hub + branches grow as each model is named ─────
        hub = Circle(0.55, color=WHITE, stroke_width=2.5).set_fill(BG, 1)
        hub_q = M(r"f_\theta", size=40)
        hub_g = VGroup(glow(hub, C_BLUE), hub, hub_q)
        spots = [LEFT * 4.6 + UP * 2.2, RIGHT * 4.6 + UP * 2.2, LEFT * 4.6 + DOWN * 2.2, RIGHT * 4.6 + DOWN * 2.2]
        names = [("GPT-6 Astra", "OpenAI", C_GREEN), ("Claude 5.5", "Anthropic", C_ORANGE),
                 ("Gemini 4", "Google DeepMind", C_BLUE), ("Mythos", "frontier lab", C_PURPLE)]
        nodes, branches, streams, labels = VGroup(), VGroup(), [], VGroup()
        for p, (nm, org, col) in zip(spots, names):
            n = Circle(0.32, color=col, stroke_width=2.5).set_fill(col, 0.15).move_to(p)
            br = Line(p, ORIGIN, buff=0.0, color=col, stroke_width=2, stroke_opacity=0.6)
            br.put_start_and_end_on(p + 0.32 * normalize(-p), 0.55 * normalize(p))
            lab = VGroup(T(nm, size=24, color=col, weight=BOLD), T(org, size=15, color=C_GREY)).arrange(DOWN, buff=0.06)
            lab.next_to(n, UP if p[1] > 0 else DOWN, buff=0.15)
            nodes.add(n); branches.add(br); labels.add(lab)
            streams.append(Stream(br, n=7, speed=0.45, color=col, radius=0.045, square=True))
        self.go("Look around", FadeOut(title, shift=UP), FadeOut(sub, shift=UP), FadeIn(tag),
                GrowFromCenter(hub_g), rt=1.2, upto="GPT-6")
        self.then(*[Create(b) for b in branches], rt=1.0, upto="GPT-6")
        for key, i in zip(["GPT-6", "Claude 5.5", "Gemini 4", "Mythos"], range(4)):
            self.go(key, GrowFromCenter(nodes[i]), FadeIn(labels[i], shift=0.2 * normalize(spots[i])),
                    Indicate(branches[i], color=WHITE, scale_factor=1.0), rt=0.7)
            self.add(streams[i])

        # benchmark gauges grow per spoken domain
        domains = [("math", C_YELLOW), ("code", C_TEAL), ("dialogue", C_PINK)]
        gauges = [VGroup() for _ in range(3)]
        rng = np.random.default_rng(7)
        scores = 0.6 + 0.35 * rng.random((4, 3))
        for i, p in enumerate(spots):
            side = RIGHT if p[0] < 0 else LEFT
            base = p + side * 0.75 + DOWN * 0.45
            for k, (dn, col) in enumerate(domains):
                b = Rectangle(width=0.22, height=1.1 * scores[i, k]).set_stroke(width=0).set_fill(col, 0.85)
                b.move_to(base + side * k * 0.3, aligned_edge=DOWN)
                gauges[k].add(b)
        legend = VGroup(*[VGroup(Square(0.18).set_fill(c, 1).set_stroke(width=0), T(dn, size=18, color=c)).arrange(RIGHT, buff=0.1)
                          for dn, c in domains]).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.35)
        for k, key in enumerate(["mathematical reasoning", "software synthesis", "multi-turn"]):
            self.go(key, *[GrowFromEdge(b, DOWN) for b in gauges[k]], FadeIn(legend[k], shift=UP * 0.2), rt=0.8)
        all_g = VGroup(*gauges)
        self.go("remarkable cognitive", LaggedStart(*[Indicate(b, color=WHITE, scale_factor=1.15) for b in all_g], lag_ratio=0.05),
                hub.animate.set_stroke(C_YELLOW), rt=1.4, upto="Yet behind")

        # push into the hub: something rigid lives inside
        lattice = VGroup(*[Square(0.07).set_stroke(C_ICE, 0.6).set_fill(C_ICE, 0.25) for _ in range(49)]).arrange_in_grid(7, 7, buff=0.035)
        lattice.move_to(hub)
        self.go("Yet behind", all_g.animate.set_opacity(0.15), legend.animate.set_opacity(0.2),
                frame.animate.scale(0.32).move_to(hub), FadeOut(hub_q), rt=2.2, upto="unsettling")
        self.go("unsettling", LaggedStart(*[FadeIn(s, scale=0.3) for s in lattice], lag_ratio=0.03), rt=1.6,
                upto="Every single foundational")

        # every branch collapses into one shared architecture → the monolith freezes
        mono = monolith(8, w=2.4, h=0.4, color=C_BLUE).move_to(ORIGIN)
        for s in streams:
            s.clear_updaters()
        self.go("Every single foundational", frame.animate.scale(1 / 0.32).move_to(ORIGIN),
                *[n.animate.move_to(ORIGIN).scale(0.2).set_opacity(0) for n in nodes],
                *[FadeOut(l) for l in labels], *[FadeOut(s) for s in streams], FadeOut(all_g), FadeOut(legend),
                *[Uncreate(b) for b in branches], rt=1.8, upto="frozen, static monolith")
        self.then(ReplacementTransform(VGroup(hub_g, lattice), mono), rt=1.0, upto="frozen, static monolith")
        front = Line(LEFT * 1.6, RIGHT * 1.6, color=C_ICE, stroke_width=4).next_to(mono, DOWN, buff=0.05)
        frost = glow(SurroundingRectangle(mono, buff=0.12, color=C_ICE, corner_radius=0.1), C_ICE, opacity=0.25)
        theta = M(r"\theta^{*}\ \text{frozen}", size=34, color=C_ICE).next_to(mono, RIGHT, buff=0.5)
        self.go("frozen, static monolith", front.animate.next_to(mono, UP, buff=0.05),
                LaggedStart(*[l.animate.set_color(C_ICE).set_fill(C_ICE, 0.18) for l in mono], lag_ratio=0.12),
                FadeIn(frost), Write(theta), rt=2.0, upto="Consider the computational")
        self.remove(front)

        # ── lifecycle: months of training, GPUs, energy, parameters, tokens ──────────
        self.go("Consider the computational", VGroup(mono, frost).animate.scale(0.8).move_to(RIGHT * 4.2 + UP * 0.4),
                FadeOut(theta), rt=1.2)
        tl_line = Line(LEFT * 6.2, RIGHT * 6.2, color=C_GREY, stroke_width=2).to_edge(DOWN, buff=0.9)
        split = tl_line.point_from_proportion(0.72)
        pre = Line(tl_line.get_start(), split, color=C_ORANGE, stroke_width=6)
        inf = Line(split, tl_line.get_end(), color=C_ICE, stroke_width=6)
        pre_l = T("pre-training", size=20, color=C_ORANGE).next_to(pre, DOWN, buff=0.15)
        inf_l = T("inference", size=20, color=C_ICE).next_to(inf, DOWN, buff=0.15)
        self.then(Create(tl_line), FadeIn(pre_l), FadeIn(inf_l), rt=0.9, upto="several months")
        prog = ValueTracker(0.001)
        pre_live = always_redraw(lambda: Line(tl_line.get_start(), tl_line.point_from_proportion(max(0.001, 0.72 * prog.get_value())),
                                              color=C_ORANGE, stroke_width=6))
        marker = always_redraw(lambda: Triangle(color=C_ORANGE).set_fill(C_ORANGE, 1).scale(0.09).rotate(PI)
                               .next_to(tl_line.point_from_proportion(0.72 * prog.get_value()), UP, buff=0.05))
        months = VGroup(*[Line(UP * 0.08, DOWN * 0.08, color=C_GREY).move_to(tl_line.point_from_proportion(0.72 * k / 6)) for k in range(1, 7)])
        self.add(pre_live, marker)
        self.go("several months", prog.animate(rate_func=linear).set_value(0.35), FadeIn(months, lag_ratio=0.2), rt=2.4,
                upto="tens of thousands of GPUs")

        gpu = VGroup(*[RoundedRectangle(width=0.32, height=0.22, corner_radius=0.03, stroke_width=0.8, stroke_color=C_DIM)
                       for _ in range(12 * 7)]).arrange_in_grid(7, 12, buff=0.06).move_to(LEFT * 3.4 + UP * 1.4)
        gpu_l = T("GPU cluster  ×  25,000", size=24, color=C_GREY).next_to(gpu, UP, buff=0.15)
        heat = ValueTracker(0)
        rng2 = np.random.default_rng(1)

        def heat_up(m, dt):
            h = heat.get_value()
            for sq in m:
                sq.set_fill(interpolate_color(ManimColor(C_DIM), ManimColor(C_ORANGE), np.clip(h * (0.6 + 0.4 * rng2.random()), 0, 1)), 1)
        gpu.add_updater(heat_up)
        self.add(gpu)
        self.go("tens of thousands of GPUs", LaggedStart(*[FadeIn(s, scale=0.5) for s in gpu], lag_ratio=0.005),
                FadeIn(gpu_l), heat.animate.set_value(1), prog.animate(rate_func=linear).set_value(0.5), rt=1.6, upto="kilowatt hours")

        kwh = counter(0, unit="kWh", size=40, color=C_ORANGE)
        kwh_l = T("energy", size=22, color=C_GREY)
        params = counter(0, unit="parameters", size=40, color=C_YELLOW)
        params_l = T("weights θ", size=22, color=C_GREY)
        stats = VGroup(VGroup(kwh_l, kwh).arrange(RIGHT, buff=0.3), VGroup(params_l, params).arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        stats.next_to(gpu, DOWN, buff=0.35).align_to(gpu, LEFT)
        self.go("kilowatt hours", FadeIn(stats[0]), rt=0.3)
        self.then(kwh.tracker.animate.set_value(51_000_000),
                prog.animate(rate_func=linear).set_value(0.65), rt=1.6, upto="hundreds of billions")
        self.go("hundreds of billions", FadeIn(stats[1]), rt=0.3)
        self.then(params.tracker.animate.set_value(405_000_000_000),
                prog.animate(rate_func=linear).set_value(0.8), rt=1.8, upto="trillions of tokens")
        tok_path = CubicBezier(gpu.get_right() + RIGHT * 0.1, gpu.get_right() + RIGHT * 2.0, mono.get_left() + LEFT * 2 + UP,
                               mono.get_left() + LEFT * 0.1)
        tok_stream = Stream(tok_path, n=22, speed=0.5, color=C_YELLOW, radius=0.05, square=True)
        tok_c = counter(0, unit="tokens", size=32, color=C_YELLOW).next_to(tok_path.point_from_proportion(0.5), UP, buff=0.35)
        self.go("trillions of tokens", FadeIn(tok_stream), FadeIn(tok_c), rt=0.3)
        self.then(tok_c.tracker.animate.set_value(15_000_000_000_000),
                prog.animate(rate_func=linear).set_value(0.92), rt=1.8, upto="During this training")

        # ── SGD on a loss landscape while weights flicker ─────────────────────────────
        lifecycle = VGroup(gpu, gpu_l, stats, tok_c)
        ax = Axes(x_range=[-3, 3], y_range=[-2, 2], x_length=5.4, y_length=3.6, axis_config=dict(stroke_opacity=0)).move_to(LEFT * 3.3 + UP * 0.9)
        rings = VGroup(*[Ellipse(width=5.2 * k / 7, height=3.4 * k / 7, color=interpolate_color(ManimColor(C_BLUE), ManimColor(C_PURPLE), k / 7),
                                 stroke_width=1.6, stroke_opacity=0.7).move_to(ax.c2p(0.4, -0.2)) for k in range(1, 8)])
        rng3 = np.random.default_rng(5)
        p = np.array([-2.5, 1.5]); path = [p.copy()]
        for _ in range(70):
            g = np.array([(p[0] - 0.4) / 1.6, (p[1] + 0.2) / 0.7])
            p = p - 0.09 * g + 0.11 * rng3.normal(size=2) * np.linalg.norm(g) ** 0.5
            path.append(p.copy())
        path = np.array(path)
        sgd_t = ValueTracker(0)
        trail = always_redraw(lambda: VMobject(stroke_color=C_YELLOW, stroke_width=2.2).set_points_as_corners(
            [ax.c2p(*q) for q in path[:max(2, int(sgd_t.get_value()) + 1)]]))
        ball = always_redraw(lambda: Dot(ax.c2p(*path[int(sgd_t.get_value())]), radius=0.09, color=C_YELLOW))
        Wgrid = heatmap(np.random.rand(5, 5), cell=0.42).move_to(RIGHT * 0.9 + UP * 1.3)
        Wlab = M(r"\theta", size=36).next_to(Wgrid, UP, buff=0.15)
        flick = ValueTracker(1.0)
        rng4 = np.random.default_rng(9)
        Wvals = rng4.random(25)

        def flicker(m, dt):
            nonlocal Wvals
            Wvals = np.clip(Wvals + flick.get_value() * rng4.normal(size=25) * 0.08, 0, 1)
            set_heat(m, Wvals.reshape(5, 5))
        eq = M(r"\theta_{t+1}", r"=", r"\theta_t", r"-", r"\eta", r"\,\nabla_\theta \mathcal{L}(\theta_t)", size=40).move_to(LEFT * 1.2 + DOWN * 1.6)
        self.go("During this training", FadeOut(lifecycle), FadeOut(tok_stream), Create(rings, lag_ratio=0.1), rt=1.2, upto="updating its numerical")
        self.add(trail, ball)
        Wgrid.add_updater(flicker)
        self.go("updating its numerical", FadeIn(Wgrid), Write(Wlab), Write(eq[0:3]), sgd_t.animate(rate_func=linear).set_value(25),
                rt=2.0, upto="stochastic gradient descent")
        self.go("stochastic gradient descent", Write(eq[3:]), sgd_t.animate(rate_func=linear).set_value(55),
                prog.animate(rate_func=linear).set_value(0.98), rt=2.0, upto="But the exact instant")

        # training ends: the descent stops, the update term dies, a freeze front crosses θ
        done = DashedLine(split + UP * 0.6, split + DOWN * 0.3, color=WHITE, stroke_width=2)
        done_l = T("training complete", size=16).next_to(done, UP, buff=0.08)
        self.go("But the exact instant", sgd_t.animate.set_value(70), prog.animate.set_value(1.0), Create(done), FadeIn(done_l),
                flick.animate.set_value(0), rt=1.6, upto="halts forever")
        cross = Line(eq[3].get_left(), eq[5].get_right(), color=C_RED, stroke_width=4)
        sweep = Line(UP * 1.2, DOWN * 1.2, color=C_ICE, stroke_width=5).next_to(Wgrid, LEFT, buff=0.05)
        self.go("halts forever", Create(cross), eq[3:].animate.set_opacity(0.3), sweep.animate.next_to(Wgrid, RIGHT, buff=0.05),
                rt=1.4, upto="etched into silicon")
        Wgrid.clear_updaters()
        self.then(Wgrid.animate.set_color(C_ICE).set_fill(opacity=0.5), FadeOut(sweep), rt=0.6, upto="etched into silicon")

        # etched: values become fixed numbers, carried into the monolith
        stone = matrix_mob(np.round(Wvals.reshape(5, 5)[:3, :3] * 2 - 1, 1), size=22, color=C_ICE).scale(0.9).move_to(Wgrid)
        self.go("etched into silicon", ReplacementTransform(Wgrid, stone), FadeOut(Wlab), rt=1.0, upto="When you query")
        self.then(stone.animate.scale(0.25).move_to(mono), FadeOut(VGroup(rings, trail, ball, eq, cross)),
                  Flash(mono.get_center(), color=C_ICE, line_length=0.4, num_lines=14), rt=1.4, upto="When you query")
        self.remove(trail, ball)

        # ── inference: different prompts flow, synapses never move ───────────────────
        net = NeuralNet((5, 7, 7, 4), width=5.4, height=3.6, seed=4).move_to(RIGHT * 1.2 + UP * 0.3)
        for e in net.edges:
            e.set_color(C_ICE)
        self.go("When you query", FadeOut(VGroup(tl_line, pre_live, marker, months, pre_l, inf_l, done, done_l, stone)),
                ReplacementTransform(VGroup(mono, frost), net), rt=1.4, upto="simple haiku")
        dw = VGroup(M(r"\Delta w =", size=34), DecimalNumber(0.0, num_decimal_places=4, font_size=34, color=C_ICE)).arrange(RIGHT)
        dw.to_corner(UR, buff=0.6)
        self.then(FadeIn(dw), rt=0.5, upto="simple haiku")
        p1 = token_row(["compose", "a", "haiku"], color=C_TEAL).move_to(LEFT * 4.6 + UP * 1.4)
        p2 = token_row(["prove", "a", "theorem", "in", "alg.", "geometry"], color=C_PINK, size=18).move_to(LEFT * 4.6 + DOWN * 1.2)
        rngA = np.random.default_rng(2)
        acts1 = [rngA.random(n) for n in (5, 7, 7, 4)]
        acts2 = [rngA.random(n) for n in (5, 7, 7, 4)]
        self.go("simple haiku", FadeIn(p1, shift=RIGHT), rt=0.6)
        self.then(p1.copy().animate.scale(0.3).move_to(net.layers[0]).set_opacity(0), net.forward(acts1, color=C_TEAL), rt=2.0,
                  upto="algebraic geometry")
        self.go("algebraic geometry", FadeIn(p2, shift=RIGHT), rt=0.6)
        self.then(p2.copy().animate.scale(0.3).move_to(net.layers[0]).set_opacity(0), net.forward(acts2, color=C_PINK), rt=1.6,
                  upto="not a single synapse")
        self.go("not a single synapse", LaggedStart(*[Indicate(e, color=WHITE, scale_factor=1.0) for e in net.edges], lag_ratio=0.2),
                Indicate(dw, color=C_ICE), rt=1.6, upto="No new connections")

        # a would-be new connection is rejected; a fading pathway snaps back
        a, b = net.layers[0][1], net.layers[2][5]
        newe = DashedLine(a.get_center(), b.get_center(), color=C_GREEN, stroke_width=3)
        self.go("No new connections", Create(newe), rt=0.7)
        self.then(newe.animate.set_color(C_RED).scale(0.05), rt=0.6, upto="No outdated")
        self.remove(newe)
        old = net.edges[1][9]
        self.go("No outdated", old.animate.set_stroke(opacity=0.02), rt=0.6)
        self.then(old.animate.set_stroke(C_ICE, opacity=1, width=3), rt=0.5, upto="cannot dynamically reallocate")
        self.then(old.animate.set_stroke(width=1.4, opacity=0.5), rt=0.4, upto="cannot dynamically reallocate")

        # same compute for easy and hard requests
        bars = VGroup()
        for i, (lab, cx, col) in enumerate([("haiku", 0.25, C_TEAL), ("theorem", 0.95, C_PINK)]):
            cplx = Rectangle(width=0.35, height=2.4 * cx).set_stroke(width=0).set_fill(col, 0.85)
            comp = Rectangle(width=0.35, height=1.3).set_stroke(width=0).set_fill(C_ICE, 0.85)
            g = VGroup(cplx, comp).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
            g.add(T(lab, size=16, color=col).next_to(g, DOWN, buff=0.1))
            bars.add(g)
        bars.arrange(RIGHT, buff=0.6, aligned_edge=DOWN).move_to(LEFT * 4.6 + DOWN * 0.2)
        bkey = VGroup(T("difficulty", size=15, color=C_GREY), T("compute spent", size=15, color=C_ICE)).arrange(DOWN, aligned_edge=LEFT).next_to(bars, UP, buff=0.3)
        self.go("cannot dynamically reallocate", FadeOut(p1), FadeOut(p2), *[GrowFromEdge(g[0], DOWN) for g in bars],
                *[FadeIn(g[2]) for g in bars], FadeIn(bkey), rt=1.2)
        self.go("complexity of your request", *[GrowFromEdge(g[1], DOWN) for g in bars], rt=1.0, upto="live terminal")

        # ── the live terminal: frozen projections in HBM ─────────────────────────────
        src = ('class Attention(nn.Module):\n'
               '    def __init__(self, d):\n'
               '        self.W_q = nn.Linear(d, d)\n'
               '        self.W_k = nn.Linear(d, d)\n'
               '        self.W_v = nn.Linear(d, d)\n'
               '    def forward(self, x):\n'
               '        q, k, v = self.W_q(x), self.W_k(x), self.W_v(x)\n'
               '        A = softmax(q @ k.T / sqrt(d))\n'
               '        return A @ v\n'
               '\n'
               '>>> model.half().requires_grad_(False)')
        code = code_block(src, size=17).scale(0.9).to_edge(LEFT, buff=0.4).shift(UP * 0.5)
        self.go("live terminal", FadeOut(VGroup(net, dw, bars, bkey)), FadeIn(code.background),
                LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.12), rt=2.4, upto="W Q")
        rows = code.code_lines
        hls = [highlight_bar(rows[i], col, 0.25) for i, col in zip((2, 3, 4), (Q_COL, K_COL, V_COL))]
        rngW = np.random.default_rng(11)
        mats = VGroup()
        for col, nm in zip((Q_COL, K_COL, V_COL), ("W_Q", "W_K", "W_V")):
            hm = heatmap(rngW.random((6, 6)), cell=0.26, cmap=(BLACK, col, WHITE))
            mats.add(VGroup(hm, M(nm, size=30, color=col).next_to(hm, UP, buff=0.1)))
        mats.arrange(RIGHT, buff=0.45).move_to(RIGHT * 3.6 + UP * 1.6)
        tW = self.t("W Q")
        for i in range(3):
            self.go(tW + 0.9 * i, FadeIn(hls[i]), TransformFromCopy(rows[2 + i], mats[i]), rt=0.8)
        hbm = RoundedRectangle(width=6.2, height=2.6, corner_radius=0.15, color=C_GREY, stroke_width=2).move_to(RIGHT * 3.6 + UP * 1.35)
        cells = VGroup(*[Square(0.12).set_stroke(C_DIM, 0.6) for _ in range(40)]).arrange_in_grid(2, 20, buff=0.04).next_to(hbm, DOWN, buff=-0.45)
        hbm_l = T("GPU HBM3  ·  80 GB", size=16, color=C_GREY).next_to(hbm, UP, buff=0.08).align_to(hbm, LEFT)
        self.go("high-bandwidth memory", Create(hbm), FadeIn(hbm_l), FadeIn(cells, lag_ratio=0.02), rt=1.2, upto="FP16")
        locks = VGroup()
        for m in mats:
            lk = VGroup(Arc(0.09, 0, PI, color=C_ICE, stroke_width=2.5).shift(UP * 0.09), RoundedRectangle(width=0.24, height=0.18, corner_radius=0.03,
                        color=C_ICE, stroke_width=2).set_fill(C_ICE, 0.4))
            lk.next_to(m, DOWN, buff=0.08)
            tag16 = T("fp16", size=13, color=C_ICE, font=MONO).next_to(lk, RIGHT, buff=0.08)
            locks.add(VGroup(lk, tag16))
        self.go("FP16", LaggedStart(*[FadeIn(l, scale=1.4) for l in locks], lag_ratio=0.2), rt=1.0, upto="Every single incoming")

        # each token is multiplied by the SAME three arrays → q, k, v
        tok_cols = VGroup()
        for i, w in enumerate(["The", "cat", "sat", "on"]):
            col = heatmap(rngW.random((6, 1)), cell=0.18, cmap=(BLACK, C_GREY, WHITE))
            col.add(T(w, size=14, color=C_GREY).next_to(col, DOWN, buff=0.06))
            tok_cols.add(col)
        tok_cols.arrange(RIGHT, buff=0.35).move_to(RIGHT * 1.6 + DOWN * 1.9)
        self.go("Every single incoming", FadeIn(tok_cols, lag_ratio=0.2, shift=UP * 0.2), rt=0.9)
        outs = VGroup()
        anims = []
        for i, tc in enumerate(tok_cols):
            trip = VGroup(*[heatmap(rngW.random((6, 1)), cell=0.13, cmap=(BLACK, c, WHITE)) for c in (Q_COL, K_COL, V_COL)]).arrange(RIGHT, buff=0.04)
            trip.move_to(RIGHT * (3.8 + 0.75 * i) + DOWN * 1.9)
            outs.add(trip)
            anims.append(Succession(
                AnimationGroup(*[ShowPassingFlash(Line(tc.get_top(), m[0].get_bottom()).set_stroke(c, 3), time_width=0.6)
                                 for m, c in zip(mats, (Q_COL, K_COL, V_COL))]),
                AnimationGroup(*[TransformFromCopy(tc[:6], trip[j]) for j in range(3)])))
        qkv_l = VGroup(M("q", color=Q_COL, size=26), M("k", color=K_COL, size=26), M("v", color=V_COL, size=26)).arrange(RIGHT, buff=0.08)
        self.then(LaggedStart(*anims, lag_ratio=0.35), rt=3.2, upto="identical, immutable")
        qkv_l.next_to(outs, DOWN, buff=0.12)
        self.go("identical, immutable", FadeIn(qkv_l), *[Indicate(m, color=WHITE, scale_factor=1.05) for m in mats], rt=1.2, upto="While activations")

        # activations change, parameters don't — two live traces
        lp = LiveAxes([0, 10, 2], [0, 2, 1], width=5.2, height=2.4, x_label="token t").move_to(LEFT * 3.4 + DOWN * 0.3)
        xs = np.linspace(0, 10, 200)
        ys_a = 1.0 + 0.45 * np.sin(xs * 2.3) * np.cos(xs * 0.7) + 0.2 * np.sin(xs * 5.1)
        ys_w = np.full_like(xs, 0.04)
        tr = ValueTracker(0)
        ca = lp.live_curve(xs, ys_a, tr, color=C_YELLOW)
        cw = lp.live_curve(xs, ys_w, tr, color=C_ICE)
        la = M(r"\|h_t\|", size=28, color=C_YELLOW).next_to(lp.ax.c2p(10, 1.6), RIGHT, buff=0.1)
        lw = M(r"\|W_t - W_0\| = 0", size=28, color=C_ICE).next_to(lp.ax.c2p(10, 0.05), RIGHT, buff=0.1)
        self.go("While activations", FadeOut(code), *[FadeOut(h) for h in hls], FadeIn(lp), rt=0.9)
        self.add(ca, cw)
        self.then(tr.animate(rate_func=linear).set_value(10), FadeIn(la), rt=3.5, upto="rigid and invariant")
        self.go("rigid and invariant", Write(lw), Indicate(cw, color=WHITE), rt=1.0, upto="Why has the entire")

        # ── consolidation: an entire industry of identical monoliths ─────────────────
        clones = VGroup(*[monolith(6, w=1.3, h=0.26, gap=0.06, color=C_ICE) for _ in range(5)]).arrange(RIGHT, buff=0.55).move_to(UP * 0.6)
        tags = VGroup(*[T(s, size=15, color=c) for s, c in [("GPT-6", C_GREEN), ("Claude 5.5", C_ORANGE), ("Gemini 4", C_BLUE),
                                                            ("Mythos", C_PURPLE), ("…", C_GREY)]])
        for tg, cl in zip(tags, clones):
            tg.next_to(cl, DOWN, buff=0.15)
        self.remove(ca, cw)
        self.go("Why has the entire", FadeOut(VGroup(lp, la, lw, mats, hbm, hbm_l, cells, locks, tok_cols, outs, qkv_l)),
                LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in clones], lag_ratio=0.15), FadeIn(tags, lag_ratio=0.15), rt=1.4)
        usd = counter(0, size=40, color=C_GOLD)
        usd_l = T("$", size=40, color=C_GOLD)
        usd_g = VGroup(usd_l, usd).arrange(RIGHT, buff=0.1).to_edge(DOWN, buff=1.4)
        usd_l.add_updater(lambda m: m.next_to(usd, LEFT, buff=0.1))
        self.go("multi-billion", FadeIn(usd_g), rt=0.3)
        self.then(usd.tracker.animate.set_value(300_000_000_000), rt=2.0, upto="rigid, unyielding")
        self.go("rigid, unyielding", *[Indicate(c, color=WHITE, scale_factor=1.04) for c in clones], rt=1.2, upto="In this investigation")

        # three forces beneath the monolith
        center = clones[2]
        self.go("In this investigation", FadeOut(VGroup(*clones[:2], *clones[3:], tags, usd_g)),
                center.animate.scale(1.6).move_to(UP * 1.6), rt=1.2)
        usd_l.clear_updaters()
        pillars = VGroup()
        icons = []
        for k, (nm, col) in enumerate([("Mathematics", C_YELLOW), ("Topology", C_GREEN), ("Hardware", C_ORANGE)]):
            pil = Rectangle(width=2.4, height=1.6, color=col, stroke_width=2).set_fill(col, 0.08)
            lab = T(nm, size=20, color=col).next_to(pil, DOWN, buff=0.1)
            pillars.add(VGroup(pil, lab))
        pillars.arrange(RIGHT, buff=0.6).move_to(DOWN * 1.6)
        # mini mechanisms inside pillars
        eig = VGroup(*[Rectangle(width=0.18, height=1.2 * 0.75 ** i).set_stroke(width=0).set_fill(C_YELLOW, 0.9) for i in range(8)]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        eig.move_to(pillars[0][0])
        gr = VGroup(*[Dot(radius=0.05, color=C_GREEN).move_to(pillars[1][0].get_center() + 0.6 * np.array([np.cos(a), 0.8 * np.sin(a), 0]))
                      for a in np.linspace(0, TAU, 8, endpoint=False)])
        gr.add(*[Line(gr[i].get_center(), gr[(i + 1) % 8].get_center(), color=C_GREEN, stroke_width=1.5) for i in range(8)])
        chip = VGroup(*[Square(0.16).set_stroke(C_ORANGE, 1).set_fill(C_ORANGE, 0.3) for _ in range(24)]).arrange_in_grid(4, 6, buff=0.05).move_to(pillars[2][0])
        words = [self.t("mathematical, physical"), self.t("mathematical, physical") + 0.8, self.t("hardware forces")]
        for k, mech in enumerate([eig, gr, chip]):
            self.go(words[k], FadeIn(pillars[k], shift=UP * 0.3), FadeIn(mech, lag_ratio=0.05), rt=0.7)
        braces = VGroup(*[Line(p.get_top(), center.get_bottom(), color=p[0].get_color(), stroke_width=2, stroke_opacity=0.7) for p in pillars])
        self.go("modern AI monolith", Create(braces), *[Indicate(p[0], color=WHITE, scale_factor=1.03) for p in pillars], rt=1.2,
                upto="tantalizing dream")

        # the living alternative reaches for silicon — and cannot take hold
        lg = living_graph(24, center=LEFT * 4.9 + UP * 1.4, radius=1.3)
        lg_l = T("self-adapting network", size=18, color=C_GREEN).next_to(LEFT * 4.9 + UP * 1.4, DOWN, buff=1.6)
        target_thr = lg.thr.get_value()
        lg.thr.set_value(0.01)
        self.hold_until(self.t("tantalizing dream") - 0.12)
        self.add(lg[0])
        self.play(FadeIn(lg.nodes), FadeIn(lg_l), lg.thr.animate.set_value(target_thr), run_time=1.2)
        self.then(lg.nodes.amp.animate.set_value(0.55), rt=1.5, upto="fiercely difficult")
        self.go("fiercely difficult", lg.thr.animate.set_value(0.2), rt=1.5, upto="physical silicon")
        self.go("physical silicon", lg.nodes.amp.animate.set_value(0.05), center.animate.set_color(C_ICE), rt=1.2)
        self.finish()
