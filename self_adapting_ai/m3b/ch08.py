"""Chapter 08 — Empirical benchmark: in-context associative recall, measured on this machine."""
from common import *

RES = json.load(open(os.path.join(ROOT, "experiments", "results_p16.json")))
EP = RES["epochs"]
CFG = RES["config"]
LOG = [l.rstrip() for l in open(os.path.join(ROOT, "experiments", "p16.log")) if l.startswith("ep")]


class Ch08(Chapter):
    CH = 8

    def construct(self):
        C = self.times(
            "To test these", "live diagnostic experiment", "PyTorch", "We pitted", "defining capability", "associative recall",
            "In this benchmark", "arbitrary key-value", "must dynamically retrieve", "queried with", "later in the sequence",
            "The first contender", "continuous Hebbian", "localized synaptic competition", "structural edge pruning",
            "The second contender", "two-layer attention Transformer", "ordinary backpropagation", "Both models saw",
            "sixty-four dimensional", "sixteen key-value pairs", "thirteen possible values", "The results were unequivocal",
            "For the first forty epochs", "Both networks hovered", "seven point seven", "never left that floor", "flatlined near twelve",
            "completely unable", "kept compressing", "drifted down from forty-nine", "without ever learning", "And the gradient paths",
            "Structural mutations are discrete", "step function", "could not send credit", "poor local minima", "did something remarkable",
            "Around epoch forty-five", "from under thirty percent", "settled at one hundred", "That sudden leap", "The theory survived",
            "Without all-to-all", "cannot sustain", "dense matrix multiplications win")
        frame = self.camera.frame
        tag = T("08 · EMPIRICAL BENCHMARK", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        self.add(tag)

        # ── the actual experiment code, then its actual log ───────────────────────────
        src = ("def batch(n):\n"
               "    keys = randperm(NK)[:P]          # 16 random keys\n"
               "    vals = randint(0, NV, (P,))      # 13 possible values\n"
               "    seq  = [k1, v1, k2, v2, ..., kP, vP, q]\n"
               "    return seq, vals[q_index]\n\n"
               "tf = Transformer(layers=2, heads=4, d=64)\n"
               "so = SelfOrganizing(H=64, k=16)  # Oja + prune\n"
               "for ep in range(100):\n"
               "    train(tf, backprop=True)\n"
               "    so.plasticity(local_only=True)")
        code = code_block(src, size=16).scale(0.85).to_edge(LEFT, buff=0.4).shift(UP * 0.6)
        self.go("To test these", FadeIn(code.background), rt=0.5)
        self.go("live diagnostic experiment", LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in code.code_lines], lag_ratio=0.1), rt=2.0)
        term = RoundedRectangle(width=6.2, height=3.6, corner_radius=0.12, stroke_color=C_DIM).set_fill(BLACK, 0.9).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        prompt = mono("$ python experiments/assoc_recall.py   # Apple M3 · mps", size=14, color=C_GREEN).next_to(term.get_corner(UL), DR, buff=0.15)
        log_lines = VGroup(*[mono(l, size=13, color=C_GREY) for l in [LOG[i] for i in (0, 4, 9, 24, 44, 48, 49, 74, 99)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        log_lines.next_to(prompt, DOWN, aligned_edge=LEFT, buff=0.2)
        self.go("PyTorch", FadeIn(term), Write(prompt), rt=0.9)
        self.then(LaggedStart(*[FadeIn(l) for l in log_lines], lag_ratio=0.3), rt=2.0, upto="defining capability")
        hl = highlight_bar(log_lines[6], C_YELLOW, 0.25)
        self.go("defining capability", FadeIn(hl), rt=0.6)

        # ── the task built from objects: K1 V1 … K16 V16, query ───────────────────────
        self.go("associative recall", FadeOut(VGroup(code, term, prompt, log_lines, hl)), rt=0.8)
        rng = np.random.default_rng(5)
        keys = [f"K{i}" for i in range(1, 17)]
        vals = [str(v) for v in rng.integers(0, 13, 16)]
        cells = VGroup()
        for k, v in zip(keys, vals):
            kb = label_box(k, K_COL, size=15, pad=0.08)
            vb = label_box(v, V_COL, size=15, pad=0.08)
            cells.add(VGroup(kb, vb).arrange(RIGHT, buff=0.04))
        cells.arrange_in_grid(2, 8, buff=(0.18, 0.25)).move_to(UP * 1.9)
        q = label_box("K7", Q_COL, size=20, pad=0.12).move_to(RIGHT * 0.0 + UP * 0.25)
        qa = VGroup(q, T("→  ?", size=26)).arrange(RIGHT, buff=0.2).move_to(UP * 0.2)
        task_l = T("16 key→value bindings, then a query  ·  33 tokens  ·  chance = 1/13", size=18, color=C_GREY).next_to(cells, UP, buff=0.25)
        self.go("In this benchmark", FadeIn(task_l), rt=0.6)
        self.go("arbitrary key-value", LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in cells], lag_ratio=0.08), rt=2.0)
        self.go("must dynamically retrieve", FadeIn(qa, shift=UP * 0.2), rt=0.6)
        bind = cells[6]
        self.go("queried with", Indicate(bind[0], color=Q_COL, scale_factor=1.3), Create(ArcBetweenPoints(q.get_top(), bind[0].get_bottom(), angle=0.4).set_stroke(Q_COL, 3)), rt=1.0)
        ans = label_box(vals[6], V_COL, size=20, pad=0.12).move_to(qa[1][0].get_right() + RIGHT * 0.5)
        self.go("later in the sequence", TransformFromCopy(bind[1], ans), FadeOut(qa[1][0][-1]), rt=1.0, upto="The first contender")
        task = VGroup(cells, task_l, qa, ans)
        # stays at the top as the shared input for both machines
        self.then(task.animate.scale(0.55).to_edge(UP, buff=0.35).shift(RIGHT * 0.8), FadeOut(*[m for m in self.mobjects if isinstance(m, ArcBetweenPoints)]), rt=0.8,
                  upto="The first contender")

        # ── two machines side by side ────────────────────────────────────────────────
        div = DashedLine(UP * 2.0, DOWN * 3.6, color=C_DIM)
        lt = T("Self-Organizing Dynamic Rewiring Net", size=20, color=C_GREEN).move_to(LEFT * 3.6 + UP * 1.75)
        rt_ = T("Modular Attention Transformer", size=20, color=C_BLUE).move_to(RIGHT * 3.6 + UP * 1.75)
        self.go("The first contender", Create(div), FadeIn(lt), rt=0.6)
        rngg = np.random.default_rng(2)
        sp = [LEFT * 3.6 + DOWN * 0.1 + np.array([1.9 * np.cos(a), 1.2 * np.sin(a), 0]) * (0.6 + 0.4 * rngg.random()) for a in np.linspace(0, TAU, 14, endpoint=False)]
        sn = VGroup(*[Dot(p, radius=0.07, color=C_GREEN) for p in sp])
        sedge = {}
        for i in range(14):
            for j in rngg.choice(14, 3, replace=False):
                if i != j and (j, i) not in sedge:
                    sedge[(i, j)] = Line(sp[i], sp[j], color=C_GREEN, stroke_width=1.8, stroke_opacity=0.7)
        sev = VGroup(*sedge.values())
        self.then(FadeIn(sn), Create(sev, lag_ratio=0.02), rt=1.0)
        self.go("continuous Hebbian", LaggedStart(*[ShowPassingFlash(e.copy().set_stroke(C_YELLOW, 4)) for e in sev], lag_ratio=0.03), rt=1.2)
        inh = VGroup(*[CurvedArrow(sp[i] + UP * 0.12, sp[(i + 1) % 14] + UP * 0.12, angle=-1.2, color=C_RED, stroke_width=2, tip_length=0.1) for i in range(0, 14, 3)])
        self.go("localized synaptic competition", LaggedStart(*[Create(a) for a in inh], lag_ratio=0.15), rt=1.0)
        weak = [e for k, e in list(sedge.items())[::3]]
        self.go("structural edge pruning", *[e.animate.set_stroke(C_RED, opacity=0.9) for e in weak], FadeOut(inh), rt=0.6)
        self.then(*[Uncreate(e) for e in weak], rt=0.8, upto="The second contender")
        # transformer block diagram with Q/K/V lanes
        blocks = VGroup()
        for L_ in range(2):
            att = RoundedRectangle(width=3.4, height=0.55, corner_radius=0.08, color=C_BLUE).set_fill(C_BLUE, 0.15)
            heads = VGroup(*[Square(0.3).set_stroke(C_BLUE, 1).set_fill(C_BLUE, 0.5) for _ in range(4)]).arrange(RIGHT, buff=0.2).move_to(att)
            mlp = RoundedRectangle(width=3.4, height=0.45, corner_radius=0.08, color=C_PURPLE).set_fill(C_PURPLE, 0.15)
            ml = T("MLP", size=14, color=C_PURPLE).move_to(mlp)
            blocks.add(VGroup(VGroup(att, heads), VGroup(mlp, ml)).arrange(UP, buff=0.12))
        blocks.arrange(UP, buff=0.25).move_to(RIGHT * 3.6 + DOWN * 0.3)
        resid = Line(blocks.get_bottom() + DOWN * 0.3, blocks.get_top() + UP * 0.3, color=C_GREY, stroke_width=2).shift(LEFT * 2.0)
        self.go("The second contender", FadeIn(rt_), rt=0.4)
        self.go("two-layer attention Transformer", FadeIn(blocks, lag_ratio=0.1, shift=UP * 0.2), Create(resid), rt=1.2)
        bpa = VGroup(*[Arrow(blocks.get_top() + UP * 0.2 + RIGHT * x, blocks.get_bottom() + DOWN * 0.1 + RIGHT * x, buff=0, color=C_RED, stroke_width=2.5,
                             max_tip_length_to_length_ratio=0.06) for x in (-1.2, 0, 1.2)])
        self.go("ordinary backpropagation", LaggedStart(*[GrowArrow(a_) for a_ in bpa], lag_ratio=0.2), rt=0.9)
        cfg = VGroup(*[VGroup(T(a_, size=16, color=C_GREY), T(b_, size=16, font=MONO)).arrange(RIGHT, buff=0.3) for a_, b_ in
                       [("embedding d", "64"), ("pairs / sequence", f"{CFG['pairs']}  ({CFG['tokens']} tokens)"), ("possible values", f"{CFG['values']}"),
                        ("epochs", "100 × 40 steps"), ("device", "Apple M3 · mps")]])
        for r in cfg:
            r[1].align_to(cfg[0][1], LEFT)
        cfg.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cfgb = VGroup(SurroundingRectangle(cfg, buff=0.2, color=C_DIM, corner_radius=0.1).set_fill(BG, 0.95), cfg).move_to(DOWN * 2.6)
        self.go("Both models saw", FadeIn(cfgb, shift=UP * 0.2), FadeOut(bpa), rt=0.8)
        self.go("sixty-four dimensional", Indicate(cfg[0], color=C_YELLOW), rt=0.6)
        self.go("sixteen key-value pairs", Indicate(cfg[1], color=C_YELLOW), rt=0.6)
        self.go("thirteen possible values", Indicate(cfg[2], color=C_YELLOW), rt=0.6, upto="The results were unequivocal")

        # ── training telemetry, generated while the models run ───────────────────────
        self.go("The results were unequivocal", FadeOut(cfgb), FadeOut(VGroup(sn, sev, blocks, resid)), lt.animate.scale(0.8).move_to(LEFT * 4.2 + UP * 1.6),
                rt_.animate.scale(0.8).move_to(RIGHT * 2.6 + UP * 1.6), FadeOut(div), rt=1.2)
        xs = np.array([e["epoch"] for e in EP], float)
        ax = LiveAxes([0, 100, 20], [0, 1, 0.25], width=5.6, height=3.0, x_label="epoch").move_to(LEFT * 2.6 + DOWN * 0.6)
        ticks = VGroup(*[T(f"{int(v * 100)}%", size=14, color=C_GREY).next_to(ax.ax.c2p(0, v), LEFT, buff=0.1) for v in (0.25, 0.5, 0.75, 1.0)])
        eps, eps_r = ValueTracker(1), ValueTracker(1)
        c_tf = ax.live_curve(xs, np.array([e["tf_acc"] for e in EP]), eps, color=C_BLUE)
        c_so = ax.live_curve(xs, np.array([e["so_acc"] for e in EP]), eps, color=C_GREEN)
        rk = LiveAxes([0, 100, 20], [0, 64, 16], width=4.0, height=3.0, x_label="epoch").move_to(RIGHT * 3.8 + DOWN * 0.6)
        r_tf = rk.live_curve(xs, np.array([e["tf_rank"] for e in EP]), eps_r, color=C_BLUE)
        r_so = rk.live_curve(xs, np.array([e["so_rank"] for e in EP]), eps_r, color=C_GREEN)
        acc_t = T("recall accuracy", size=18).next_to(ax, UP, buff=0.05)
        rk_t = T("effective rank of the query representation (of 64)", size=16).next_to(rk, UP, buff=0.05)
        epoch_l = always_redraw(lambda: VGroup(T("epoch", size=16, color=C_GREY), Integer(int(eps.get_value()), font_size=30)).arrange(RIGHT, buff=0.15).move_to(UP * 1.05))
        at = lambda tr, key: EP[int(np.clip(tr.get_value(), 1, 100)) - 1][key]
        ro_tf = always_redraw(lambda: T(f"{at(eps, 'tf_acc'):.1%}", size=18, color=C_BLUE, font=MONO).next_to(rt_, RIGHT, buff=0.25))
        ro_so = always_redraw(lambda: T(f"{at(eps, 'so_acc'):.1%}", size=18, color=C_GREEN, font=MONO).next_to(lt, RIGHT, buff=0.25))
        chance = DashedLine(ax.ax.c2p(0, CFG["chance"]), ax.ax.c2p(100, CFG["chance"]), color=C_RED, stroke_width=2)
        chance_l = T("chance 1/13 = 7.7%", size=14, color=C_RED).next_to(chance, UP, buff=0.04).align_to(chance, RIGHT)
        self.then(FadeIn(ax), FadeIn(ticks), FadeIn(acc_t), FadeIn(rk), FadeIn(rk_t), rt=0.8)
        self.add(c_tf, c_so, r_tf, r_so, epoch_l, ro_tf, ro_so)
        # the long plateau: both models near chance for forty epochs
        self.go("For the first forty epochs", eps.animate(rate_func=linear).set_value(40), rt=2.6)
        self.go("Both networks hovered", Create(chance), FadeIn(chance_l), rt=0.8)
        self.go("seven point seven", Indicate(chance_l, color=C_RED, scale_factor=1.3), rt=0.8)
        self.go("never left that floor", Indicate(c_so, color=WHITE), rt=0.8)
        self.go("flatlined near twelve", Indicate(ro_so, color=C_GREEN, scale_factor=1.4), rt=0.8)
        cut = list(sedge.values())[1]
        self.go("completely unable", rt=0.1)
        # the rank telemetry runs the full 100 epochs on its own clock
        so_rank_l = always_redraw(lambda: T(f"{at(eps_r, 'so_rank'):.1f}", size=18, color=C_GREEN, font=MONO).next_to(rk.ax.c2p(100, 64), DOWN, buff=0.1).shift(LEFT * 0.3))
        tf_rank_l = always_redraw(lambda: T(f"{at(eps_r, 'tf_rank'):.1f}", size=18, color=C_BLUE, font=MONO).next_to(rk.ax.c2p(100, 64), DOWN, buff=0.45).shift(LEFT * 0.3))
        self.go("kept compressing", FadeIn(so_rank_l), FadeIn(tf_rank_l), rt=0.5)
        self.go("drifted down from forty-nine", eps_r.animate(rate_func=linear).set_value(100), rt=2.4)
        self.go("without ever learning", Indicate(so_rank_l, color=C_GREEN, scale_factor=1.5), rt=0.9, upto="And the gradient paths")

        # ── why: pruning is a step function — no gradient crosses it ───────────────────
        step_ax = Axes(x_range=[-1, 1, 0.5], y_range=[0, 1.2, 1], x_length=3.0, y_length=1.6, axis_config=dict(color=C_GREY, include_tip=False)).move_to(LEFT * 4.6 + DOWN * 3.1)
        step = VGroup(Line(step_ax.c2p(-1, 0), step_ax.c2p(0.2, 0), color=C_ORANGE, stroke_width=4), Line(step_ax.c2p(0.2, 1), step_ax.c2p(1, 1), color=C_ORANGE, stroke_width=4),
                      DashedLine(step_ax.c2p(0.2, 0), step_ax.c2p(0.2, 1), color=C_ORANGE))
        sl = VGroup(M(r"m_{ij}=\mathbb{1}[|w_{ij}|>\tau]", size=22, color=C_ORANGE).next_to(step_ax, UP, buff=0.05),
                    M(r"\partial m/\partial w = 0 \ \text{or}\ \infty", size=22, color=C_RED).next_to(step_ax, RIGHT, buff=0.15))
        self.go("And the gradient paths", VGroup(ax, ticks, acc_t, chance, chance_l).animate.shift(UP * 0.4), rt=0.6)
        self.go("Structural mutations are discrete", cut.animate.set_stroke(C_RED, 4), Create(step_ax), rt=0.8)
        self.go("step function", Create(step), Write(sl[0]), Uncreate(cut), rt=1.0)
        self.then(Write(sl[1]), Flash(step_ax.c2p(0.2, 0.5), color=C_RED), rt=0.8, upto="could not send credit")
        lm = Axes(x_range=[0, 6], y_range=[0, 3], x_length=3.0, y_length=1.6, axis_config=dict(stroke_opacity=0)).move_to(LEFT * 0.6 + DOWN * 3.1)
        f = lambda x: 1.6 + 0.9 * np.sin(1.7 * x) - 0.25 * x
        curve = lm.plot(f, x_range=[0, 6], color=C_PURPLE)
        ball = Dot(lm.c2p(1.0, f(1.0)), radius=0.09, color=C_GREEN)
        self.go("could not send credit", FadeIn(curve), FadeIn(ball), rt=0.8)
        self.then(ball.animate.move_to(lm.c2p(2.7, f(2.7)) + UP * 0.09), rt=0.8, upto="poor local minima")
        self.go("poor local minima", Wiggle(ball), FadeIn(T("stuck", size=16, color=C_GREEN).next_to(lm.c2p(2.7, f(2.7)), UP, buff=0.2)), rt=1.0, upto="did something remarkable")

        # ── the transformer's phase change ───────────────────────────────────────────
        line923 = DashedLine(ax.ax.c2p(0, 0.923), ax.ax.c2p(100, 0.923), color=C_BLUE, stroke_width=1.5)
        l923 = T("92.3%", size=14, color=C_BLUE).next_to(line923, LEFT, buff=0.1)
        self.go("did something remarkable", Indicate(c_tf, color=WHITE), rt=0.8)
        self.go("Around epoch forty-five", eps.animate(rate_func=linear).set_value(45), FadeIn(line923), FadeIn(l923), rt=1.2)
        jump = VGroup(Dot(ax.ax.c2p(45, at(eps, "tf_acc") if False else EP[44]["tf_acc"]), color=C_YELLOW, radius=0.07), Dot(ax.ax.c2p(49, EP[48]["tf_acc"]), color=C_YELLOW, radius=0.07))
        brace = BraceBetweenPoints(ax.ax.c2p(45, 1.04), ax.ax.c2p(49, 1.04), UP, color=C_YELLOW)
        bl_ = T("4 epochs", size=14, color=C_YELLOW).next_to(brace, UP, buff=0.05)
        self.go("from under thirty percent", eps.animate(rate_func=linear).set_value(49), FadeIn(jump), GrowFromCenter(brace), FadeIn(bl_), rt=1.6)
        self.go("settled at one hundred", eps.animate(rate_func=linear).set_value(100), rt=1.6)
        phase = VGroup(T("phase change", size=16, color=C_YELLOW, weight=BOLD), T("cf. induction-head formation", size=13, color=C_YELLOW), T("Olsson et al. 2022", size=13, color=C_GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(ax.ax.c2p(75, 0.55))
        self.go("That sudden leap", FadeIn(phase, shift=UP * 0.2), Indicate(brace, color=C_YELLOW), rt=1.2, upto="The theory survived")
        cross_ep = next(e["epoch"] for e in EP if e["tf_acc"] >= 0.923)
        self.remove(c_tf, c_so, r_tf, r_so, epoch_l, ro_tf, ro_so, so_rank_l, tf_rank_l)
        self.go("The theory survived", FadeOut(self.stage(tag, task)), rt=0.8)

        # ── final: real singular-value spectra and a results table ────────────────────
        s_tf, s_so = np.array(RES["tf_spectrum"]), np.array(RES["so_spectrum"])
        base = Line(LEFT * 6.0, LEFT * 0.4, color=C_GREY).move_to(LEFT * 3.2 + DOWN * 2.6)

        def bars(s, col, x0):
            return VGroup(*[Rectangle(width=0.075, height=max(0.01, 2.6 * v)).set_stroke(width=0).set_fill(col, 0.9)
                            .move_to(base.get_left() + RIGHT * (x0 + i * 0.085), aligned_edge=DOWN) for i, v in enumerate(s)])
        bt, bs = bars(s_tf, C_BLUE, 0.1), bars(s_so, C_GREEN, 0.1)
        bs.shift(UP * 0.0)
        spec_t = T("singular values of the final representations (σᵢ/σ₁)", size=16).next_to(base, UP, buff=3.0).align_to(base, LEFT)
        leg = VGroup(T("Transformer", size=16, color=C_BLUE), T("self-organizing", size=16, color=C_GREEN)).arrange(RIGHT, buff=0.4).next_to(spec_t, DOWN, buff=0.1).align_to(base, LEFT)
        self.then(Create(base), FadeIn(spec_t), FadeIn(leg), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bt], lag_ratio=0.01), rt=1.4)
        self.then(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs], lag_ratio=0.01), bt.animate.set_opacity(0.45), rt=1.2, upto="Without all-to-all")
        last = EP[-1]
        rows = [("", "Transformer", "Self-organizing"),
                ("recall accuracy", f"{last['tf_acc']:.1%}", f"{last['so_acc']:.1%}"),
                ("epochs to 92.3%", f"{cross_ep}", "never"),
                ("effective rank", f"{last['tf_rank']:.1f}", f"{last['so_rank']:.1f}"),
                ("learning signal", "global backprop", "local Hebbian"),
                ("wall-clock (M3)", f"{RES['seconds']:.0f} s total", "")]
        tbl = VGroup()
        for r_i, r in enumerate(rows):
            cells_ = VGroup(*[T(c, size=17 if r_i else 18, color=(C_GREY if j == 0 else (C_BLUE if j == 1 else C_GREEN)) if r_i else (C_BLUE if j == 1 else C_GREEN),
                                font=MONO if (r_i and j) else FONT, weight=BOLD if r_i == 0 else NORMAL) for j, c in enumerate(r)])
            for j, c in enumerate(cells_):
                c.move_to(RIGHT * (0.5 + [0, 3.0, 5.2][j]) + DOWN * (0.0 + 0.48 * r_i) + UP * 1.4, aligned_edge=LEFT if j == 0 else ORIGIN)
            tbl.add(cells_)
        grid = VGroup(*[Line(RIGHT * 0.3, RIGHT * 6.8, color=C_DIM, stroke_width=1).move_to(UP * (1.4 - 0.48 * i + 0.24) + RIGHT * 3.6) for i in range(1, len(rows))])
        winner = SurroundingRectangle(VGroup(*[r[1] for r in tbl]), buff=0.12, color=C_BLUE, corner_radius=0.08)
        self.go("Without all-to-all", FadeIn(grid, lag_ratio=0.1), LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in tbl], lag_ratio=0.15), rt=2.0)
        self.go("cannot sustain", Indicate(tbl[1][2], color=C_GREEN), Indicate(tbl[2][2], color=C_GREEN), rt=1.2)
        self.go("dense matrix multiplications win", Create(winner), rt=1.0)
        self.finish()
