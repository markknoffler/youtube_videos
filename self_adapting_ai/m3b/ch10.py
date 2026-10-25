"""Chapter 10 — The Hidden Hebb: linear attention is a fast-weight Hebbian memory."""
from common import *

HVD = json.load(open(os.path.join(ROOT, "experiments", "hebb_vs_delta.json")))


def outer_heat(v, k, cell=0.22, col=C_GREEN):
    M_ = np.outer(v, k)
    return heatmap((M_ - M_.min()) / (np.ptp(M_) + 1e-9), cell=cell, cmap=(BLACK, col, WHITE))


class Ch10(Chapter):
    CH = 10

    def construct(self):
        C = self.times(
            "So far, this has been", "But there is a twist", "changes everything", "Go back to the Hebbian", "adding up outer products",
            "drown in crosstalk", "Now look closely", "Strip the softmax", "something extraordinary", "Every new token writes",
            "running matrix", "Every query reads", "That is Hebb's rule", "Exactly", "In 2021", "proved it formally",
            "fast weight programmer", "slow network that learns", "while it is thinking", "The idea is older", "In 2016",
            "faster than learning", "slower than thought", "neurally plausible", "So the Transformer never", "out of the synapse",
            "into the activations", "And the crosstalk", "capacity wall", "delta rule", "read what the memory", "store only the error",
            "We tested this", "thirty-two associations", "forty-nine percent", "seventy-eight percent", "every single one after three",
            "This is exactly where", "forgetting gate", "Titans go further", "rewrites its own weights", "driven by surprise",
            "Self-adapting intelligence did arrive", "Not as a brain-shaped", "dense, differentiable memory", "inside the monolith")
        frame = self.camera.frame
        tag = T("10 · THE HIDDEN HEBB", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        self.add(tag)
        rng = np.random.default_rng(10)

        # ── recap strip of failures, then the twist ───────────────────────────────────
        spec = VGroup(*[Rectangle(width=0.18, height=2.0 if i == 0 else 0.05).set_stroke(width=0).set_fill(C_PINK, 0.9) for i in range(9)]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        hops = VGroup(*[Dot(radius=0.07, color=C_GREEN) for _ in range(7)]).arrange(RIGHT, buff=0.32)
        hops.add(*[Line(hops[i].get_center(), hops[i + 1].get_center(), color=C_GREEN, stroke_width=2) for i in range(6)])
        thr = VGroup(Rectangle(width=2.4, height=0.3).set_stroke(width=0).set_fill(C_ORANGE, 0.9),
                     Rectangle(width=0.05, height=0.3).set_stroke(width=0).set_fill(C_GREEN, 0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        strip = VGroup(*[VGroup(m, T(l, size=16, color=C_GREY).next_to(m, DOWN, buff=0.25)) for m, l in
                         [(spec, "rank collapse"), (hops, "routing latency"), (thr, "hardware lottery")]]).arrange(RIGHT, buff=1.2).move_to(UP * 0.4)
        self.go("So far, this has been", LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in strip], lag_ratio=0.3), rt=1.6)
        self.go("But there is a twist", strip.animate.set_opacity(0.25), rt=0.8)
        self.go("changes everything", Rotate(strip, PI / 2, axis=UP), rt=0.8)
        self.remove(strip)

        # ── the Hebbian memory from ch04: M = Σ v kᵀ, built from outer products ───────
        d = 8
        Ms = np.zeros((d, d))
        Mg = heatmap(Ms + 0.5, cell=0.3, cmap=(BLACK, C_GREEN, WHITE)).move_to(RIGHT * 2.6)
        Ml = M(r"M = \sum_i v_i\, k_i^{\top}", size=34, color=C_GREEN).next_to(Mg, UP, buff=0.25)
        self.go("Go back to the Hebbian", FadeIn(Mg), Write(Ml), rt=1.0)
        for j in range(3):
            v, k = rng.normal(size=d), rng.normal(size=d)
            vc = heatmap((v[:, None] - v.min()) / np.ptp(v), cell=0.3, cmap=(BLACK, V_COL, WHITE)).move_to(LEFT * 4.4)
            kr = heatmap((k[None] - k.min()) / np.ptp(k), cell=0.3, cmap=(BLACK, K_COL, WHITE)).next_to(vc, UR, buff=0.15)
            op = outer_heat(v, k, cell=0.3).move_to(LEFT * 1.6)
            Ms += np.outer(v, k)
            self.play(FadeIn(vc), FadeIn(kr), run_time=0.3)
            self.play(ReplacementTransform(VGroup(vc, kr), op), run_time=0.45)
            self.play(op.animate.move_to(Mg).set_opacity(0),
                      *[sq.animate.set_fill(heat_color(val, (BLACK, C_GREEN, WHITE))) for sq, val in zip(Mg, ((Ms - Ms.min()) / np.ptp(Ms)).flatten())],
                      run_time=0.5)
            self.remove(op)
        bars = VGroup(*[Rectangle(width=0.32, height=0.2 + 1.4 * v).set_stroke(width=0).set_fill(C_PINK if i else C_GREEN, 0.9)
                        for i, v in enumerate([1.0, 0.8, 0.55, 0.62, 0.4, 0.7])]).arrange(RIGHT, buff=0.08, aligned_edge=DOWN).move_to(LEFT * 3.4 + DOWN * 1.6)
        bl = T("recall: crosstalk", size=16, color=C_PINK).next_to(bars, DOWN, buff=0.15)
        self.go("drown in crosstalk", *[GrowFromEdge(b, DOWN) for b in bars], FadeIn(bl), rt=1.0, upto="Now look closely")
        memory = VGroup(Mg, Ml)

        # ── strip the softmax: (QKᵀ)V → Q(KᵀV) — the running matrix ──────────────────
        self.go("Now look closely", FadeOut(VGroup(bars, bl)), memory.animate.scale(0.75).to_corner(UR, buff=0.5).shift(DOWN * 0.4), rt=1.0)
        eq1 = M(r"y = ", r"\mathrm{softmax}", r"\big(QK^{\top}\big)", r"V", size=48).move_to(UP * 2.2 + LEFT * 1.2)
        self.then(Write(eq1), rt=0.9, upto="Strip the softmax")
        self.go("Strip the softmax", eq1[1].animate.set_color(C_RED).set_opacity(0.0), rt=1.0)
        eq2 = M(r"y_t = ", r"\Big(\sum_{i\le t} v_i\, k_i^{\top}\Big)", r"\,q_t", size=48).move_to(eq1)
        eq2[2].set_color(Q_COL); eq2[1].set_color(C_GREEN)
        self.go("something extraordinary", TransformMatchingShapes(eq1, eq2), rt=1.4)
        # token stream writing into S_t
        S = np.zeros((d, d))
        Sg = heatmap(S + 0.5, cell=0.28, cmap=(BLACK, C_GREEN, WHITE)).move_to(DOWN * 0.9)
        Sl = always_redraw(lambda: M(r"S_t", size=32, color=C_GREEN).next_to(Sg, LEFT, buff=0.25))
        toks = token_row(["the", "cat", "sat", "on", "the", "mat"], color=C_GREY, size=20).move_to(DOWN * 3.0)
        self.go("Every new token writes", FadeIn(toks, lag_ratio=0.1), FadeIn(Sg), rt=0.8)
        self.add(Sl)
        Seq = M(r"S_t = S_{t-1} + v_t\, k_t^{\top}", size=34, color=C_GREEN).next_to(Sg, RIGHT, buff=0.6)
        self.go("running matrix", Write(Seq), rt=0.8)
        for j, tk in enumerate(toks):
            v, k = rng.normal(size=d), rng.normal(size=d)
            S += np.outer(v, k)
            Sn = (S - S.min()) / (np.ptp(S) + 1e-9)
            pulse = outer_heat(v, k, cell=0.12).move_to(tk.get_top() + UP * 0.5)
            self.play(FadeIn(pulse, shift=UP * 0.2), Indicate(tk, color=C_GREEN), run_time=0.22)
            self.play(pulse.animate.move_to(Sg).scale(2.3).set_opacity(0), *[sq.animate.set_fill(heat_color(val, (BLACK, C_GREEN, WHITE))) for sq, val in zip(Sg, Sn.flatten())], run_time=0.33)
            self.remove(pulse)
        qv = heatmap(rng.random((d, 1)), cell=0.28, cmap=(BLACK, Q_COL, WHITE)).next_to(Sg, RIGHT, buff=0.3)
        yv = heatmap(rng.random((d, 1)), cell=0.28, cmap=(BLACK, C_YELLOW, WHITE))
        read = M(r"y = S_t\, q", size=34)
        self.go("Every query reads", FadeOut(Seq), FadeIn(qv, shift=LEFT * 0.3), rt=0.6)
        yv.next_to(qv, RIGHT, buff=0.5)
        self.then(ShowPassingFlash(SurroundingRectangle(Sg, color=Q_COL, buff=0.05)), TransformFromCopy(qv, yv), Write(read.next_to(Sg, UP, buff=0.3)), rt=1.0, upto="That is Hebb's rule")

        # ── side by side with Hebb's rule; matching terms light up together ──────────
        hebb = M(r"\Delta w_{ij}", "=", r"\eta", r"\;y_i", r"\;x_j", size=46).move_to(LEFT * 3.4 + UP * 0.6)
        attn = M(r"\Delta S", "=", r"\;", r"\;v_t", r"\;k_t^{\top}", size=46).move_to(RIGHT * 3.0 + UP * 0.6)
        hebb[3].set_color(C_PINK); hebb[4].set_color(C_BLUE); attn[3].set_color(V_COL); attn[4].set_color(K_COL)
        hl_ = T("Hebb, 1949: post × pre", size=18, color=C_GREY).next_to(hebb, DOWN, buff=0.3)
        al_ = T("linear attention: value × key", size=18, color=C_GREY).next_to(attn, DOWN, buff=0.3)
        self.go("That is Hebb's rule", FadeOut(VGroup(toks, Sg, qv, yv, read, eq2, memory)), rt=0.6)
        self.remove(Sl)
        self.then(Write(hebb), Write(attn), FadeIn(hl_), FadeIn(al_), rt=1.2)
        links = VGroup(CurvedArrow(hebb[3].get_top(), attn[3].get_top(), angle=-0.5, color=C_YELLOW), CurvedArrow(hebb[4].get_bottom(), attn[4].get_bottom(), angle=0.5, color=C_YELLOW))
        eqs = M(r"\equiv", size=80, color=C_YELLOW).move_to(UP * 0.6 + LEFT * 0.2)
        self.go("Exactly", Create(links), FadeIn(eqs, scale=1.6), rt=0.9)

        # ── Schlag, Irie & Schmidhuber 2021 — the exact sentence ──────────────────────
        pg = PaperPage("schlag", 0, height=6.8).move_to(RIGHT * 3.4 + DOWN * 1.8)
        h1 = pg.hl("We show the formal equivalence of linearised self-")
        h2 = pg.hl("attention mechanisms and fast weight controllers")
        self.go("In 2021", VGroup(hebb, attn, hl_, al_, links, eqs).animate.scale(0.6).to_edge(LEFT, buff=0.4).shift(UP * 1.6), FadeIn(pg, shift=UP), rt=1.2)
        self.go("proved it formally", frame.animate.scale(0.5).move_to(h1.get_center() + DOWN * 0.15), rt=1.0)
        self.then(FadeIn(h1), FadeIn(h2), rt=0.8, upto="fast weight programmer")
        self.go("fast weight programmer", frame.animate.scale(2.0).move_to(ORIGIN), FadeOut(Group(pg, h1, h2)), rt=1.2)
        slow = VGroup(RoundedRectangle(width=2.8, height=2.2, corner_radius=0.15, color=C_ICE, stroke_width=2.5).set_fill(C_ICE, 0.08),
                      T("slow net", size=20, color=C_ICE)).move_to(LEFT * 2.4 + DOWN * 0.8)
        slow[1].next_to(slow[0], DOWN, buff=0.12)
        slow_w = heatmap(rng.random((6, 6)), cell=0.28, cmap=(BLACK, C_ICE, WHITE)).move_to(slow[0])
        fast = heatmap(np.full((6, 6), 0.5), cell=0.34, cmap=(BLACK, C_GREEN, WHITE)).move_to(RIGHT * 2.6 + DOWN * 0.8)
        fast_l = T("fast weights", size=20, color=C_GREEN).next_to(fast, DOWN, buff=0.12)
        instr = VGroup(*[Arrow(slow[0].get_right(), fast.get_left(), buff=0.15, color=C, stroke_width=3).shift(UP * dy) for C, dy in [(K_COL, 0.3), (V_COL, -0.3)]])
        il = VGroup(M("k_t", color=K_COL, size=26).next_to(instr[0], UP, buff=0.05), M("v_t", color=V_COL, size=26).next_to(instr[1], DOWN, buff=0.05))
        self.then(FadeIn(slow), FadeIn(slow_w), FadeIn(fast), FadeIn(fast_l), rt=0.6)
        grad = Arrow(slow[0].get_top() + UP * 0.6, slow[0].get_top(), buff=0.05, color=C_RED)
        grl = M(r"\nabla\mathcal{L}", size=26, color=C_RED).next_to(grad, RIGHT, buff=0.1)
        self.go("slow network that learns", GrowArrow(grad), FadeIn(grl), *[sq.animate.set_fill(heat_color(rng.random(), (BLACK, C_ICE, WHITE))) for sq in slow_w], rt=1.2)
        fv = np.full(36, 0.5)
        flick = ValueTracker(1.0)

        def fl(m, dt):
            nonlocal fv
            fv = np.clip(fv + flick.get_value() * rng.normal(size=36) * 0.12, 0, 1)
            for sq, val in zip(m, fv):
                sq.set_fill(heat_color(val, (BLACK, C_GREEN, WHITE)))
        self.go("while it is thinking", *[GrowArrow(a) for a in instr], FadeIn(il), rt=0.8)
        fast.add_updater(fl)
        self.add(fast)

        # ── Ba & Hinton 2016: three timescales ───────────────────────────────────────
        self.go("The idea is older", VGroup(slow, slow_w, grad, grl, instr, il).animate.scale(0.6).to_corner(DL, buff=0.5),
                VGroup(fast, fast_l).animate.scale(0.6).to_corner(DR, buff=0.5), rt=1.0)
        pg2 = PaperPage("ba2016", 0, height=4.6).move_to(LEFT * 3.6 + UP * 0.6)
        h3 = pg2.hl("fast weights")
        self.go("In 2016", FadeIn(pg2, shift=RIGHT), rt=0.8)
        self.then(FadeIn(h3), rt=0.5)
        ax = NumberLine(x_range=[-3, 9, 1], length=6.0, color=C_GREY).move_to(RIGHT * 2.8 + UP * 0.3)
        axl = T("timescale (log₁₀ seconds)", size=14, color=C_GREY).next_to(ax, DOWN, buff=0.15)
        bands = [("activations", -2.5, -0.5, C_YELLOW), ("fast weights", 0, 3, C_GREEN), ("slow weights", 5, 8.8, C_ICE)]
        bandm = VGroup()
        for nm, a, b, col in bands:
            r = Rectangle(width=ax.n2p(b)[0] - ax.n2p(a)[0], height=0.35).set_stroke(width=0).set_fill(col, 0.8)
            r.move_to((ax.n2p(a) + ax.n2p(b)) / 2 + UP * 0.45)
            bandm.add(VGroup(r, T(nm, size=14, color=col).next_to(r, UP, buff=0.08)))
        self.go("faster than learning", Create(ax), FadeIn(axl), FadeIn(bandm[2]), FadeIn(bandm[1]), rt=1.0)
        self.go("slower than thought", FadeIn(bandm[0]), Indicate(bandm[1], color=WHITE), rt=1.0)
        self.go("neurally plausible", Indicate(h3, color=C_YELLOW), rt=1.0, upto="So the Transformer never")

        # ── Hebb moves from the synapse into the activations ─────────────────────────
        fast.clear_updaters()
        self.go("So the Transformer never", FadeOut(Group(pg2, h3, ax, axl, bandm)), FadeOut(VGroup(hebb, attn, hl_, al_, links, eqs)), FadeOut(VGroup(slow, slow_w, grad, grl, instr, il, fast, fast_l)), rt=0.9)
        syn = VGroup(Circle(0.4, color=C_BLUE, stroke_width=3).move_to(LEFT * 4.4), Circle(0.4, color=C_PINK, stroke_width=3).move_to(LEFT * 1.8))
        syn.add(Line(syn[0].get_right(), syn[1].get_left(), color=C_YELLOW, stroke_width=6))
        sl_ = T("synapse", size=18, color=C_GREY).next_to(syn, DOWN, buff=0.3)
        heq = M(r"\Delta w = \eta\, y\, x", size=34, color=C_YELLOW).next_to(syn, UP, buff=0.3)
        self.then(FadeIn(syn), FadeIn(sl_), Write(heq), rt=0.8)
        stream_p = Line(RIGHT * 0.4 + DOWN * 0.2, RIGHT * 6.4 + DOWN * 0.2)
        st = Stream(stream_p, n=14, speed=0.35, color=C_GREEN, radius=0.07, square=True)
        st_l = T("activations (the residual stream)", size=18, color=C_GREEN).next_to(stream_p, DOWN, buff=0.3)
        self.go("out of the synapse", heq.animate.move_to(RIGHT * 3.4 + UP * 0.6), syn[2].animate.set_stroke(opacity=0.2), rt=1.4)
        self.go("into the activations", FadeIn(st), FadeIn(st_l), Flash(RIGHT * 3.4 + UP * 0.6, color=C_YELLOW, line_length=0.5, num_lines=16), rt=1.0,
                upto="And the crosstalk")

        # ── capacity wall and the delta rule; then the measured curves ────────────────
        st.clear_updaters()
        self.go("And the crosstalk", FadeOut(VGroup(syn, sl_, heq, st, st_l)), rt=0.6)
        ax2 = LiveAxes([0, 64, 16], [0, 1, 0.25], width=5.6, height=3.4, x_label="associations stored (d = 64)").move_to(LEFT * 3.0 + DOWN * 0.3)
        ticks = VGroup(*[T(f"{int(v * 100)}%", size=14, color=C_GREY).next_to(ax2.ax.c2p(0, v), LEFT, buff=0.1) for v in (0.25, 0.5, 0.75, 1.0)])
        xs = np.array(HVD["n_pairs"], float)
        tr = ValueTracker(2)
        c_h = ax2.live_curve(xs, np.array(HVD["hebb"]), tr, color=C_PINK)
        self.then(FadeIn(ax2), FadeIn(ticks), rt=0.6)
        self.add(c_h)
        self.go("capacity wall", tr.animate(rate_func=linear).set_value(64), FadeIn(T("pure Hebbian  M += v kᵀ", size=16, color=C_PINK).next_to(ax2, UP, buff=0.1).align_to(ax2, LEFT)), rt=1.6)
        deq = M(r"S \mathrel{+}=", r"\beta", r"\big(v - ", r"S k", r"\big)\, k^{\top}", size=40).move_to(RIGHT * 3.4 + UP * 1.8)
        deq[3].set_color(C_YELLOW)
        self.go("delta rule", Write(deq), rt=1.0)
        pred = VGroup(*[Rectangle(width=0.28, height=h).set_stroke(width=0).set_fill(C_YELLOW, 0.85) for h in (0.9, 0.5, 1.2, 0.3)]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        targ = VGroup(*[Rectangle(width=0.28, height=h).set_stroke(width=0).set_fill(V_COL, 0.85) for h in (1.3, 0.4, 0.6, 0.9)]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        err = VGroup(*[Rectangle(width=0.28, height=max(0.05, abs(a - b))).set_stroke(width=0).set_fill(C_RED, 0.85) for a, b in zip((1.3, 0.4, 0.6, 0.9), (0.9, 0.5, 1.2, 0.3))]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        grp = VGroup(VGroup(pred, T("S k  (predicted)", size=14, color=C_YELLOW)).arrange(DOWN, buff=0.1),
                     VGroup(targ, T("v  (target)", size=14, color=V_COL)).arrange(DOWN, buff=0.1),
                     VGroup(err, T("error → write", size=14, color=C_RED)).arrange(DOWN, buff=0.1)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to(RIGHT * 3.4 + DOWN * 0.4)
        self.go("read what the memory", FadeIn(grp[0], shift=UP * 0.2), Indicate(deq[3]), rt=0.9)
        self.go("store only the error", FadeIn(grp[1], shift=UP * 0.2), rt=0.5)
        self.then(TransformFromCopy(VGroup(grp[0][0], grp[1][0]), grp[2][0]), FadeIn(grp[2][1]), rt=0.9, upto="We tested this")
        tr2 = ValueTracker(2)
        c_d = ax2.live_curve(xs, np.array(HVD["delta"]), tr2, color=C_YELLOW)
        c_d3 = ax2.live_curve(xs, np.array(HVD["delta_3sweeps"]), tr2, color=C_GREEN)
        self.go("We tested this", FadeOut(grp), deq.animate.scale(0.7).to_corner(UR, buff=0.6).shift(DOWN * 0.4), rt=0.8)
        self.add(c_d, c_d3)
        i32 = HVD["n_pairs"].index(32)
        vline = DashedLine(ax2.ax.c2p(32, 0), ax2.ax.c2p(32, 1), color=C_GREY)
        self.go("thirty-two associations", Create(vline), tr2.animate(rate_func=linear).set_value(32), rt=1.2)
        lab = lambda key, col, txt, dy: VGroup(Dot(ax2.ax.c2p(32, HVD[key][i32]), color=col), T(txt, size=16, color=col).next_to(ax2.ax.c2p(32, HVD[key][i32]), RIGHT, buff=0.15).shift(UP * dy))
        self.go("forty-nine percent", FadeIn(lab("hebb", C_PINK, f"Hebbian {HVD['hebb'][i32]:.0%}", 0)), rt=0.6)
        self.go("seventy-eight percent", FadeIn(lab("delta", C_YELLOW, f"delta, 1 pass {HVD['delta'][i32]:.0%}", 0)), rt=0.6)
        self.go("every single one after three", FadeIn(lab("delta_3sweeps", C_GREEN, f"delta, 3 passes {HVD['delta_3sweeps'][i32]:.0%}", -0.05)),
                tr2.animate(rate_func=linear).set_value(64), rt=1.4)
        meas = T("measured on this M3 · keys correlated (ρ = 0.6) · 40 trials", size=14, color=C_GREY).next_to(ax2, DOWN, buff=0.55)
        self.then(FadeIn(meas), rt=0.4, upto="This is exactly where")

        # ── DeltaNet gates, Titans surprise ────────────────────────────────────────────
        self.remove(c_h, c_d, c_d3)
        self.go("This is exactly where", FadeOut(self.stage(tag, deq)), rt=0.8)
        geq = M(r"S_t = ", r"\alpha_t", r"\,S_{t-1} + \beta_t\big(v_t - S_{t-1}k_t\big)k_t^{\top}", size=38).move_to(UP * 2.0)
        geq[1].set_color(C_ORANGE)
        mem = heatmap(rng.random((8, 8)), cell=0.32, cmap=(BLACK, C_GREEN, WHITE)).move_to(LEFT * 3.4 + DOWN * 0.8)
        self.then(ReplacementTransform(deq, geq), FadeIn(mem), rt=1.0)
        gate_l = T("α: forget gate", size=18, color=C_ORANGE).next_to(mem, DOWN, buff=0.2)
        self.go("forgetting gate", Indicate(geq[1], color=C_ORANGE, scale_factor=1.4), FadeIn(gate_l), mem.animate.set_opacity(0.35), rt=1.2)
        net = NeuralNet((4, 6, 4), width=3.0, height=2.6, seed=8, edge_op=0.7).move_to(RIGHT * 3.2 + DOWN * 0.8)
        tl_ = T("Titans: neural memory", size=18, color=C_PURPLE).next_to(net, UP, buff=0.2)
        self.go("Titans go further", FadeIn(net), FadeIn(tl_), rt=0.8)
        sur = ValueTracker(0.1)
        meter = always_redraw(lambda: VGroup(Rectangle(width=0.3, height=2.4, color=C_DIM).set_fill(C_DIM, 0.2),
                                             Rectangle(width=0.3, height=max(0.02, 2.4 * sur.get_value())).set_stroke(width=0)
                                             .set_fill(interpolate_color(ManimColor(C_GREEN), ManimColor(C_RED), sur.get_value()), 0.9)).arrange(ORIGIN).next_to(net, RIGHT, buff=0.4))
        sl2 = T("surprise", size=14, color=C_GREY).next_to(net, RIGHT, buff=0.25).shift(DOWN * 1.5)
        self.add(meter)
        self.then(FadeIn(sl2), rt=0.3)
        self.go("rewrites its own weights", sur.animate.set_value(0.9), LaggedStart(*[e.animate.set_stroke(C_RED, width=3) for g in net.edges for e in g], lag_ratio=0.01), rt=1.2)
        sq = M(r"\text{surprise} = \nabla_M \,\ell(M; x_t)", size=30, color=C_PURPLE).to_edge(DOWN, buff=0.6)
        self.go("driven by surprise", Write(sq), sur.animate.set_value(0.15), LaggedStart(*[e.animate.set_stroke(C_BLUE if rng.random() > 0.4 else C_RED, width=1.4) for g in net.edges for e in g], lag_ratio=0.01),
                rt=1.6, upto="Self-adapting intelligence did arrive")

        # ── the monolith, with a living memory inside ────────────────────────────────
        self.remove(meter)
        self.go("Self-adapting intelligence did arrive", FadeOut(self.stage(tag)), rt=0.8)
        lg = living_graph(20, center=LEFT * 3.6 + UP * 0.2, radius=1.4, seed=4)
        thr0 = lg.thr.get_value(); lg.thr.set_value(0.01)
        self.add(lg[0])
        self.go("Not as a brain-shaped", FadeIn(lg.nodes), lg.thr.animate.set_value(thr0), rt=0.8)
        self.then(lg.nodes.animate.set_opacity(0.15), lg.thr.animate.set_value(0.01), rt=0.8)
        mono = monolith(8, w=2.6, h=0.42, color=C_ICE).move_to(RIGHT * 2.2 + UP * 0.1)
        core = heatmap(np.full((5, 5), 0.5), cell=0.26, cmap=(BLACK, C_GREEN, WHITE)).move_to(mono)
        cv = np.full(25, 0.5)

        def pulse_core(m, dt):
            nonlocal cv
            cv = np.clip(cv + rng.normal(size=25) * 0.1, 0, 1)
            for s_, val in zip(m, cv):
                s_.set_fill(heat_color(val, (BLACK, C_GREEN, WHITE)))
        self.go("dense, differentiable memory", FadeIn(mono), rt=0.8)
        self.then(FadeIn(core, scale=0.4), rt=0.5)
        core.add_updater(pulse_core)
        self.add(core)
        glowc = glow(SurroundingRectangle(core, buff=0.05, color=C_GREEN), C_GREEN, opacity=0.35)
        self.go("inside the monolith", FadeIn(glowc), frame.animate.scale(0.7).move_to(mono), rt=2.0)
        self.finish()
