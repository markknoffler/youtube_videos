"""Chapter 10 — The 10-year horizon: four converging mechanisms, and the monolith comes alive."""
from common import *


class Ch10(Chapter):
    CH = 10

    def construct(self):
        C = self.times(
            "Where does this leave", "next decade", "The future of intelligence", "biological chaos", "brute-force frozen",
            "The true frontier", "global bilinear attention", "localized structural plasticity", "Over the next ten years",
            "four pioneering", "First, Neuromorphic", "Next-generation silicon", "crossbar arrays", "physical layer",
            "continuous local plasticity", "von Neumann", "Second, Fast-Weights", "pioneering frameworks", "dynamically update",
            "meta-gradients", "episodic memory", "Third, Liquid", "Continuous-time dynamical", "internal time constants",
            "unpredictable real-time", "without losing stability", "And fourth", "autonomous agentic", "inspect and rewrite",
            "at runtime", "task performance", "As hardware designers", "asynchronous sparsity", "algorithmic theorists",
            "credit assignment in continuous", "finally dissolve", "The monolith of modern", "threshold of superhuman",
            "Yet the artificial minds", "frozen statues", "silicon stone", "They will be living", "self-adapting cognitive",
            "Thank you for joining", "mathematical proofs", "experimental source", "benchmark data", "research papers", "description below")
        frame = self.camera.frame
        tag = T("10 · THE 10-YEAR HORIZON", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        self.add(tag)

        # ── bridge: routing streams from ch09 flow into a decade axis ─────────────────
        axis = NumberLine(x_range=[2026, 2036, 2], length=11, color=C_GREY, include_numbers=True, font_size=18,
                          decimal_number_config=dict(group_with_commas=False, num_decimal_places=0)).to_edge(DOWN, buff=0.6)
        rs = [Stream(VMobject().set_points_smoothly([LEFT * 7 + UP * (1.5 - 0.6 * i), LEFT * 2 + UP * 0.2 * i, RIGHT * 7 + UP * (0.5 - 0.4 * i)]),
                     n=6, speed=0.3, color=c, radius=0.05, square=True) for i, c in enumerate([C_YELLOW, C_TEAL, C_PINK, C_BLUE])]
        self.add(*rs)
        q = T("What comes next?", size=40, weight=BOLD).move_to(UP * 2.4)
        self.go("Where does this leave", Write(q), rt=1.2)
        self.go("next decade", Create(axis), rt=1.2, upto="The future of intelligence")

        # ── neither chaos nor ice ─────────────────────────────────────────────────────
        for s in rs:
            s.clear_updaters()
        self.go("The future of intelligence", FadeOut(VGroup(*rs)), q.animate.scale(0.6).to_edge(UP, buff=0.4), rt=0.8)
        chaos = living_graph(22, center=LEFT * 3.6 + UP * 0.4, radius=1.5, seed=9)
        chaos.nodes.amp.set_value(0.7)
        ice = monolith(6, w=2.2, h=0.36, color=C_ICE).move_to(RIGHT * 3.6 + UP * 0.4)
        self.add(chaos[0])
        self.go("biological chaos", FadeIn(chaos.nodes), rt=0.6)
        x1 = cross(s=0.5).move_to(LEFT * 3.6 + UP * 0.4)
        self.then(Create(x1), rt=0.6)
        self.go("brute-force frozen", FadeIn(ice), rt=0.6)
        x2 = cross(s=0.5).move_to(RIGHT * 3.6 + UP * 0.4)
        self.then(Create(x2), rt=0.6, upto="The true frontier")

        # ── unification: attention arcs + local plastic edges on the same nodes ───────
        self.go("The true frontier", FadeOut(VGroup(chaos.nodes, x1, x2, ice)), rt=0.8)
        self.remove(chaos[0])
        pts = [np.array([np.cos(a) * 3.0, np.sin(a) * 1.5, 0]) + UP * 0.3 for a in np.linspace(0, TAU, 12, endpoint=False)]
        nodes = VGroup(*[Dot(p, radius=0.09, color=WHITE) for p in pts])
        arcs = VGroup(*[ArcBetweenPoints(pts[i], pts[j], angle=0.5).set_stroke(C_BLUE, 1.6, 0.6) for i in range(12) for j in range(i + 3, 12, 3)])
        local = VGroup(*[Line(pts[i], pts[(i + 1) % 12], color=C_GREEN, stroke_width=3) for i in range(12)])
        self.then(FadeIn(nodes, lag_ratio=0.05), rt=0.6)
        self.go("global bilinear attention", Create(arcs, lag_ratio=0.03), rt=1.2)
        self.go("localized structural plasticity", Create(local, lag_ratio=0.05), rt=1.0)
        uni = M(r"h' =", r"\mathrm{softmax}(QK^{\top}/\sqrt d)\,V", r"\;+\;", r"\Delta W_{\text{local}}(t)\,h", size=34).next_to(nodes, DOWN, buff=0.5)
        uni[1].set_color(C_BLUE); uni[3].set_color(C_GREEN)
        wobble = ValueTracker(0)
        local.add_updater(lambda m, dt: [l.set_stroke(width=2 + 1.5 * np.sin(wobble.get_value() * 3 + i)) for i, l in enumerate(m)])
        self.then(Write(uni), wobble.animate.set_value(3), rt=1.4, upto="Over the next ten years")

        # ── four pillars, each its own live mechanism ─────────────────────────────────
        local.clear_updaters()
        self.go("Over the next ten years", FadeOut(VGroup(nodes, arcs, local, uni, q)), rt=0.8)
        quads = [LEFT * 3.55 + UP * 1.45, RIGHT * 3.55 + UP * 1.45, LEFT * 3.55 + DOWN * 1.75, RIGHT * 3.55 + DOWN * 1.75]
        frames_ = VGroup(*[RoundedRectangle(width=6.8, height=3.0, corner_radius=0.15, stroke_color=c, stroke_width=1.6).set_fill(c, 0.04).move_to(p)
                           for p, c in zip(quads, [C_ORANGE, C_PINK, C_TEAL, C_PURPLE])])
        titles = VGroup(*[T(s, size=18, color=c, weight=BOLD).next_to(f.get_corner(UL), DR, buff=0.12) for s, c, f in
                          zip(["① neuromorphic & analog", "② fast weights · test-time training", "③ liquid networks · neural ODEs", "④ self-compiling graphs"],
                              [C_ORANGE, C_PINK, C_TEAL, C_PURPLE], frames_)])
        self.go("four pioneering", FadeOut(axis), LaggedStart(*[Create(f) for f in frames_], lag_ratio=0.2), rt=1.4)

        # ① memristor crossbar: I_j = Σ_i G_ij V_i, conductances update in place
        o1 = quads[0] + LEFT * 1.0 + DOWN * 0.15
        rows, cols = 5, 6
        wl = VGroup(*[Line(o1 + LEFT * 1.6 + UP * (0.9 - 0.45 * i), o1 + RIGHT * 1.4 + UP * (0.9 - 0.45 * i), color=C_ORANGE, stroke_width=2) for i in range(rows)])
        bl = VGroup(*[Line(o1 + LEFT * 1.2 + RIGHT * 0.5 * j + UP * 1.1, o1 + LEFT * 1.2 + RIGHT * 0.5 * j + DOWN * 1.1, color=C_BLUE, stroke_width=2) for j in range(cols)])
        rngG = np.random.default_rng(4)
        G = rngG.random((rows, cols))
        mem = VGroup(*[Square(0.16).set_stroke(width=0).set_fill(heat_color(G[i, j], (BLACK, C_ORANGE, C_YELLOW)), 1).move_to(wl[i].get_start() * [0, 1, 0] + bl[j].get_start() * [1, 0, 0])
                       for i in range(rows) for j in range(cols)])
        vin = VGroup(*[M(f"V_{i + 1}", size=18, color=C_ORANGE).next_to(wl[i], LEFT, buff=0.08) for i in range(rows)])
        bitstreams = [Stream(Line(b.get_start(), b.get_end()), n=4, speed=0.5, color=C_BLUE, radius=0.035) for b in bl]
        ohm = M(r"I_j=\sum_i G_{ij}V_i", size=26, color=C_ORANGE).move_to(quads[0] + RIGHT * 2.2 + UP * 0.2)
        loihi = T("Loihi 2 · memristor arrays", size=14, color=C_GREY).next_to(ohm, DOWN, buff=0.2)
        self.go("First, Neuromorphic", FadeIn(titles[0]), rt=0.5)
        self.go("Next-generation silicon", Create(wl, lag_ratio=0.1), Create(bl, lag_ratio=0.1), FadeIn(vin), FadeIn(loihi), rt=1.2)
        self.go("crossbar arrays", FadeIn(mem, lag_ratio=0.02), rt=0.9)
        self.go("physical layer", Write(ohm), *[FadeIn(s) for s in bitstreams], rt=1.0)
        G2 = np.clip(G + rngG.normal(size=G.shape) * 0.35, 0, 1)
        self.go("continuous local plasticity", *[sq.animate.set_fill(heat_color(v, (BLACK, C_ORANGE, C_YELLOW))) for sq, v in zip(mem, G2.flatten())], rt=1.4)
        vn = VGroup(T("CPU ⇄ memory bus", size=14, color=C_RED), cross(s=0.15)).arrange(RIGHT, buff=0.15).next_to(loihi, DOWN, buff=0.15)
        self.go("von Neumann", FadeIn(vn), rt=0.8, upto="Second, Fast-Weights")

        # ② test-time training: hidden state is a weight matrix updated per token
        o2 = quads[1]
        Wt = heatmap(rngG.random((5, 5)), cell=0.3, cmap=(BLACK, C_PINK, WHITE)).move_to(o2 + LEFT * 1.6 + DOWN * 0.2)
        Wl_ = M("W_t", size=26, color=C_PINK).next_to(Wt, UP, buff=0.1)
        ttt = M(r"W_t = W_{t-1} - \eta\,\nabla_W \ell(W_{t-1}; x_t)", size=24, color=C_PINK).move_to(o2 + RIGHT * 1.3 + UP * 0.5)
        ttt_l = T("Sun et al. 2024 · TTT layers", size=14, color=C_GREY).next_to(ttt, DOWN, buff=0.15)
        trow = token_row(["x₁", "x₂", "x₃", "x₄", "x₅"], color=C_PINK, size=16).move_to(o2 + RIGHT * 1.3 + DOWN * 0.7)
        self.go("Second, Fast-Weights", FadeIn(titles[1]), FadeIn(Wt), FadeIn(Wl_), rt=0.8)
        self.go("pioneering frameworks", Write(ttt), FadeIn(ttt_l), rt=1.2)
        self.go("dynamically update", FadeIn(trow, lag_ratio=0.1), rt=0.5)
        for k in range(5):
            Wv = rngG.random(25)
            self.play(Indicate(trow[k], color=WHITE), ShowPassingFlash(Line(trow[k].get_left(), Wt.get_right()).set_stroke(C_PINK, 3)),
                      *[sq.animate.set_fill(heat_color(v, (BLACK, C_PINK, WHITE))) for sq, v in zip(Wt, Wv)], run_time=0.5)
        self.go("episodic memory", Indicate(Wt, color=WHITE), rt=0.8, upto="Third, Liquid")

        # ③ liquid time-constant ODE: state x(t) under input I(t), τ adapts
        o3 = quads[2]
        lax = Axes(x_range=[0, 10, 2], y_range=[-1.5, 1.5, 1], x_length=4.0, y_length=1.9, axis_config=dict(color=C_DIM, include_tip=False)).move_to(o3 + LEFT * 1.0 + DOWN * 0.2)
        ts = np.linspace(0, 10, 600)
        I = np.sign(np.sin(ts * 0.9)) * 1.0 + 0.3 * np.sin(ts * 4)
        x = np.zeros_like(ts); tau = np.zeros_like(ts)
        for k in range(1, len(ts)):
            tau[k] = 0.25 + 1.2 / (1 + abs(I[k]) * 2)
            x[k] = x[k - 1] + (ts[1] - ts[0]) * (-x[k - 1] / tau[k] + np.tanh(I[k]) / tau[k] * 0.9)
        tt = ValueTracker(0)
        cx = LiveAxes.live_curve(VGroup(lax) if False else type("o", (), {"ax": lax})(), ts, x, tt, color=C_TEAL)
        ci = LiveAxes.live_curve(type("o", (), {"ax": lax})(), ts, 0.4 * I - 1.0, tt, color=C_GREY, width=1.5, dot=False)
        lode = M(r"\frac{dx}{dt}=-\frac{x}{\tau(I)}+f(x,I)", size=24, color=C_TEAL).move_to(o3 + RIGHT * 2.2 + UP * 0.4)
        taul = always_redraw(lambda: VGroup(M(r"\tau =", size=24), DecimalNumber(tau[int(np.clip(tt.get_value() / 10 * 599, 0, 599))], num_decimal_places=2, font_size=24, color=C_TEAL))
                             .arrange(RIGHT, buff=0.1).next_to(lode, DOWN, buff=0.3))
        self.go("Third, Liquid", FadeIn(titles[2]), Create(lax), rt=0.6)
        self.add(cx, ci)
        self.go("Continuous-time dynamical", Write(lode), tt.animate(rate_func=linear).set_value(2.5), rt=1.4)
        self.add(taul)
        self.go("internal time constants", tt.animate(rate_func=linear).set_value(5), rt=1.4)
        self.go("unpredictable real-time", tt.animate(rate_func=linear).set_value(7.5), rt=1.4)
        self.go("without losing stability", tt.animate(rate_func=linear).set_value(10), rt=1.4, upto="And fourth")

        # ④ self-compiling graph: an agent inspects and rewrites its own DAG
        o4 = quads[3]
        ops = ["embed", "attend", "mlp", "route", "decode"]
        boxes = VGroup(*[label_box(s, C_PURPLE, size=14) for s in ops]).arrange(RIGHT, buff=0.35).move_to(o4 + UP * 0.2)
        darr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=C_PURPLE, stroke_width=2, max_tip_length_to_length_ratio=0.3) for a, b in zip(boxes[:-1], boxes[1:])])
        perf = ValueTracker(0.45)
        pb_bg = Rectangle(width=4.0, height=0.2, color=C_DIM).set_fill(C_DIM, 0.3).move_to(o4 + DOWN * 1.0)
        pb = always_redraw(lambda: Rectangle(width=4.0 * perf.get_value(), height=0.2).set_stroke(width=0).set_fill(C_PURPLE, 0.9).move_to(pb_bg.get_left(), aligned_edge=LEFT))
        pbl = T("task performance", size=13, color=C_GREY).next_to(pb_bg, DOWN, buff=0.08)
        self.go("And fourth", FadeIn(titles[3]), FadeIn(boxes, lag_ratio=0.1), FadeIn(darr), rt=0.8)
        self.add(pb)
        self.then(FadeIn(pb_bg), FadeIn(pbl), rt=0.4)
        lens = Circle(0.35, color=WHITE, stroke_width=2).move_to(boxes[0])
        self.go("autonomous agentic", FadeIn(lens), rt=0.4)
        self.go("inspect and rewrite", lens.animate.move_to(boxes[2]), rt=0.8)
        newb = VGroup(label_box("moe", C_YELLOW, size=14), label_box("mlp′", C_YELLOW, size=14)).arrange(DOWN, buff=0.1).move_to(boxes[2])
        self.go("at runtime", ReplacementTransform(boxes[2], newb), Flash(newb.get_center(), color=C_YELLOW), rt=0.8)
        self.go("task performance", perf.animate.set_value(0.85), rt=1.0, upto="As hardware designers")

        # ── convergence: the four systems connect into one architecture ───────────────
        quadgroups = [VGroup(frames_[0], titles[0], wl, bl, mem, vin, ohm, loihi, vn), VGroup(frames_[1], titles[1], Wt, Wl_, ttt, ttt_l, trow),
                      VGroup(frames_[2], titles[2], lax, lode), VGroup(frames_[3], titles[3], boxes[:2], boxes[3:], newb, darr, pb_bg, pbl, lens)]
        self.remove(taul, cx, ci, pb, *bitstreams)
        cpos = [LEFT * 2.2 + UP * 1.2, RIGHT * 2.2 + UP * 1.2, LEFT * 2.2 + DOWN * 1.5, RIGHT * 2.2 + DOWN * 1.5]
        self.go("As hardware designers", *[g.animate.scale(0.5).move_to(p) for g, p in zip(quadgroups, cpos)], rt=1.6)
        hub = Circle(0.6, color=WHITE, stroke_width=2.5).set_fill(BG, 1).move_to(DOWN * 0.15)
        links = VGroup(*[Line(hub.get_center(), p, color=c, stroke_width=2.5) for p, c in zip(cpos, [C_ORANGE, C_PINK, C_TEAL, C_PURPLE])])
        self.go("asynchronous sparsity", Create(links), rt=0.8)
        self.then(GrowFromCenter(hub), rt=0.5)
        flows = [Stream(Line(p, hub.get_center()), n=4, speed=0.6, color=c, radius=0.05) for p, c in zip(cpos, [C_ORANGE, C_PINK, C_TEAL, C_PURPLE])]
        self.go("algorithmic theorists", *[FadeIn(f) for f in flows], rt=0.8)
        self.go("credit assignment in continuous", hub.animate.set_stroke(C_YELLOW), rt=0.8)
        self.go("finally dissolve", *[g.animate.set_opacity(0.0) for g in quadgroups], FadeOut(links), *[FadeOut(f) for f in flows], rt=1.2, upto="The monolith of modern")
        self.remove(*quadgroups, *flows)

        # ── the monolith returns — then its rigid surfaces become motion ─────────────
        mono = monolith(8, w=2.6, h=0.42, color=C_ICE).move_to(UP * 0.2)
        frost = glow(SurroundingRectangle(mono, buff=0.12, color=C_ICE, corner_radius=0.1), C_ICE, opacity=0.25)
        self.go("The monolith of modern", ReplacementTransform(hub, mono), FadeIn(frost), rt=1.4)
        thr = DashedLine(LEFT * 6, RIGHT * 6, color=C_GOLD).move_to(DOWN * 2.8)
        thl = T("threshold of superhuman reasoning", size=18, color=C_GOLD).next_to(thr, UP, buff=0.1).to_edge(RIGHT, buff=0.6)
        self.go("threshold of superhuman", Create(thr), FadeIn(thl), thr.animate.move_to(UP * 2.9), thl.animate.move_to(UP * 3.15 + RIGHT * 3.4), rt=2.0)
        cracks = VGroup(*[VMobject(stroke_color=WHITE, stroke_width=1.5).set_points_as_corners(
            [l.get_center() + LEFT * 1.2 + RIGHT * 2.4 * a + UP * 0.18 * ((-1) ** k) for k, a in enumerate(np.linspace(0, 1, 7))]) for l in mono])
        self.go("Yet the artificial minds", Indicate(mono, color=C_ICE), rt=1.0)
        self.go("frozen statues", Create(cracks, lag_ratio=0.1), rt=1.2)
        # each rigid layer becomes a living wave
        phase = ValueTracker(0)

        def waves():
            g = VGroup()
            ph = phase.get_value()
            for i, l in enumerate(mono):
                c = l.get_center()
                xs = np.linspace(-1.6, 1.6, 60)
                col = interpolate_color(ManimColor(C_BLUE), ManimColor(C_GREEN), i / 7)
                pts_ = [c + np.array([x * (1 + 0.15 * np.sin(ph + i)), 0.16 * np.sin(3 * x + ph * (1 + 0.2 * i) + i), 0]) for x in xs]
                g.add(VMobject(stroke_color=col, stroke_width=3).set_points_smoothly(pts_))
            return g
        wv = always_redraw(waves)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 2.0))
        self.add(phase)
        self.go("silicon stone", FadeOut(VGroup(mono, frost, cracks)), FadeIn(wv), rt=1.4)
        field = SpikeField(n=40, width=12.5, height=6.4, rate=3, seed=11, color=C_GREEN)
        field.alpha.set_value(0)
        self.add(field)
        arcsL = VGroup(*[ArcBetweenPoints(mono[i].get_left() + LEFT * 0.2, mono[j].get_left() + LEFT * 0.2, angle=1.2).set_stroke(C_BLUE, 2, 0.7) for i, j in [(0, 3), (2, 6), (1, 7), (4, 7)]])
        arcsR = VGroup(*[ArcBetweenPoints(mono[i].get_right() + RIGHT * 0.2, mono[j].get_right() + RIGHT * 0.2, angle=-1.2).set_stroke(C_GREEN, 2, 0.7) for i, j in [(0, 4), (3, 7), (1, 5)]])
        self.go("They will be living", field.alpha.animate.set_value(0.8), Create(arcsL), Create(arcsR), rt=1.6)
        breath = ValueTracker(0)
        arcsL.add_updater(lambda m, dt: m.set_stroke(opacity=0.4 + 0.4 * np.sin(phase.get_value())))
        arcsR.add_updater(lambda m, dt: m.set_stroke(opacity=0.4 + 0.4 * np.cos(phase.get_value() * 1.3)))
        self.go("self-adapting cognitive", field.rate.animate.set_value(6), rt=1.4, upto="Thank you for joining")

        # ── end card, the living system keeps moving behind it ───────────────────────
        self.go("Thank you for joining", FadeOut(VGroup(thr, thl)), field.alpha.animate.set_value(0.35), rt=0.8)
        endt = T("Why Brain-Like AI Failed", size=46, weight=BOLD).move_to(UP * 2.4)
        self.then(Write(endt), rt=1.0)
        items = VGroup(*[VGroup(Dot(color=c), T(s, size=24, color=c)).arrange(RIGHT, buff=0.2) for s, c in
                         [("mathematical proofs", C_YELLOW), ("experimental source code", C_GREEN), ("benchmark data", C_BLUE), ("research papers", C_PINK)]])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 2.0)
        for key, it in zip(["mathematical proofs", "experimental source", "benchmark data", "research papers"], items):
            self.go(key, FadeIn(it, shift=RIGHT * 0.2), rt=0.5)
        self.go("description below", Indicate(items, color=WHITE, scale_factor=1.03), rt=1.0)
        self.finish(tail=2.0)
