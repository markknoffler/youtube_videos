"""Chapter 04 — The Modular Emergence Paradox: a static wire vs. a recomputed attention affinity."""
from common import *


class Ch04(Chapter):
    CH = 4

    def construct(self):
        C = self.times(
            "This brings us", "Modular Emergence Paradox", "If self-organization", "local plasticity", "continuous topological",
            "why did decades", "And conversely", "violently rejects", "all-to-all attention", "uniform backpropagation",
            "conquer every", "Examine the stark", "Self-organizing networks promised", "Yet in practice", "representational chaos",
            "destructive interference", "catastrophic forgetting", "Meanwhile, the Transformer", "spontaneously discovers",
            "Inside a trained", "induction heads", "modular routing", "arithmetic units", "associative recall",
            "These functional circuits", "without any dynamic", "The weights remain", "yet the activation flow",
            "multi-step algorithmic", "In seminal work", "coordinate across layers", "implicit gradient descent",
            "When an induction head", "copies previous", "bilinear query-key", "retrieving arbitrary", "Biologically-inspired",
            "token-specific lookup", "catastrophic interference", "How could a rigid", "This paradox cannot",
            "engineering patience", "To understand why", "three foundational")
        frame = self.camera.frame
        tag = T("04 · THE MODULAR EMERGENCE PARADOX", size=16, color=C_GREY).to_corner(UL, buff=0.35)

        # ── bridge: the collapsed grey cloud of ch03 on the left, the monolith on the right ─
        rng = np.random.default_rng(3)
        blob = VGroup(*[Dot(LEFT * 3.6 + 0.35 * np.array([*rng.normal(size=2), 0]), radius=0.05, color=C_GREY) for _ in range(60)])
        mono = monolith(6, w=2.0, h=0.36, color=C_ICE).move_to(RIGHT * 3.6)
        self.add(tag, blob)
        title = T("The Modular Emergence Paradox", size=44, weight=BOLD).to_edge(UP, buff=0.7)
        self.go("This brings us", FadeIn(mono, shift=LEFT), rt=1.0)
        self.go("Modular Emergence Paradox", Write(title), rt=1.4)

        # left column: the biological recipe, ticked off as named
        recipe = VGroup(*[VGroup(T(s, size=22, color=C_GREEN), check().scale(0.6)).arrange(RIGHT, buff=0.2)
                          for s in ["self-organization", "local plasticity", "topological rewiring"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        recipe.move_to(LEFT * 3.6 + UP * 0.9)
        for i, k in enumerate(["If self-organization", "local plasticity", "continuous topological"]):
            self.go(k, FadeIn(recipe[i][0], shift=RIGHT * 0.2), Create(recipe[i][1]), rt=0.6)
        fm = VGroup(T("foundation models?", size=24), cross()).arrange(RIGHT, buff=0.25).move_to(LEFT * 3.6 + DOWN * 2.3)
        arr = Arrow(recipe.get_bottom(), fm.get_top(), color=C_GREY, buff=0.5)
        self.go("why did decades", blob.animate.move_to(LEFT * 3.6 + DOWN * 0.7), GrowArrow(arr), rt=0.9)
        self.then(FadeIn(fm[0]), Create(fm[1]), rt=0.8, upto="And conversely")

        # right column: the monolith opens into brute-force all-to-all attention
        toks = VGroup(*[Dot(radius=0.09, color=C_BLUE) for _ in range(7)]).arrange(RIGHT, buff=0.42).move_to(RIGHT * 3.6 + DOWN * 1.1)
        toks2 = toks.copy().move_to(RIGHT * 3.6 + UP * 0.9)
        dense = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=1.2, color=C_BLUE, stroke_opacity=0.5) for a in toks for b in toks2])
        self.go("And conversely", Indicate(mono, color=WHITE), rt=0.8)
        self.go("violently rejects", ReplacementTransform(mono, VGroup(toks, toks2)), rt=1.0)
        self.go("all-to-all attention", Create(dense, lag_ratio=0.01), rt=1.3)
        bp = VGroup(*[Arrow(toks2[i].get_top() + UP * 0.6, toks2[i].get_top() + UP * 0.1, buff=0, color=C_RED, stroke_width=3, max_tip_length_to_length_ratio=0.4) for i in range(7)])
        bpl = M(r"\nabla \mathcal{L}", size=28, color=C_RED).next_to(bp, RIGHT, buff=0.1)
        self.go("uniform backpropagation", LaggedStart(*[GrowArrow(b) for b in bp], lag_ratio=0.08), FadeIn(bpl), rt=1.1)
        doms = VGroup(*[label_box(s, c, size=16) for s, c in [("language", C_BLUE), ("code", C_TEAL), ("vision", C_YELLOW), ("audio", C_PINK), ("proteins", C_GREEN)]])
        doms.arrange(RIGHT, buff=0.15).move_to(RIGHT * 3.6 + DOWN * 2.4).scale_to_fit_width(6)
        self.go("conquer every", LaggedStart(*[FadeIn(d, shift=UP * 0.2) for d in doms], lag_ratio=0.15), rt=1.4, upto="Examine the stark")

        # ── the contradiction, measured: what each promised vs. what each did ───────
        self.go("Examine the stark", FadeOut(VGroup(recipe, arr, fm, bp, bpl, doms)), title.animate.scale(0.5).to_corner(UR, buff=0.35), rt=1.0)
        div = DashedLine(UP * 2.8, DOWN * 3.4, color=C_DIM)
        hl = T("self-organizing", size=24, color=C_GREEN).move_to(LEFT * 3.6 + UP * 2.6)
        hr = T("Transformer", size=24, color=C_BLUE).move_to(RIGHT * 3.6 + UP * 2.6)
        self.then(Create(div), FadeIn(hl), FadeIn(hr), dense.animate.set_opacity(0.25), rt=0.8)
        # catastrophic forgetting, live: task A accuracy decays as task B is learned locally
        acc = LiveAxes([0, 10, 5], [0, 1, 0.5], width=4.6, height=2.0, x_label="training on task B →").move_to(LEFT * 3.6 + DOWN * 2.0)
        xs = np.linspace(0, 10, 120)
        tr = ValueTracker(0)
        ca = acc.live_curve(xs, 0.92 * np.exp(-0.35 * xs) + 0.05, tr, color=C_YELLOW)
        cb = acc.live_curve(xs, 0.9 * (1 - np.exp(-0.5 * xs)), tr, color=C_PINK)
        la = VGroup(T("task A", size=16, color=C_YELLOW), T("task B", size=16, color=C_PINK)).arrange(DOWN, aligned_edge=LEFT).next_to(acc, RIGHT, buff=0.1)
        self.go("Self-organizing networks promised", blob.animate.move_to(LEFT * 3.6 + UP * 0.9).scale(1.6).set_color(C_GREEN), rt=1.2)
        self.go("Yet in practice", FadeIn(acc), FadeIn(la), rt=0.6)
        self.add(ca, cb)
        rngb = np.random.default_rng(5)
        self.go("representational chaos", *[d.animate.shift(0.6 * np.array([*rngb.normal(size=2), 0])).set_color(C_GREY) for d in blob],
                tr.animate.set_value(3), rt=1.0)
        self.go("destructive interference", tr.animate.set_value(6.5), Wiggle(blob), rt=1.2)
        self.go("catastrophic forgetting", tr.animate.set_value(10), rt=1.2, upto="Meanwhile, the Transformer")

        # attention-head grid: circuits light up as they are named
        heads = VGroup(*[RoundedRectangle(width=0.5, height=0.36, corner_radius=0.05, stroke_color=C_DIM, stroke_width=1.2).set_fill(C_DIM, 0.25)
                         for _ in range(6 * 8)]).arrange_in_grid(6, 8, buff=0.08).move_to(RIGHT * 2.6 + DOWN * 0.3)
        hlab = VGroup(T("layer", size=14, color=C_GREY).rotate(PI / 2).next_to(heads, LEFT, buff=0.1),
                      T("attention heads", size=14, color=C_GREY).next_to(heads, DOWN, buff=0.1))
        self.go("Meanwhile, the Transformer", FadeOut(VGroup(toks, toks2, dense)), FadeIn(heads, lag_ratio=0.01), FadeIn(hlab), rt=1.2)
        self.go("spontaneously discovers", LaggedStart(*[h.animate.set_fill(C_BLUE, 0.3 + 0.5 * rngb.random()) for h in heads], lag_ratio=0.01), rt=1.4,
                upto="Inside a trained")
        circuits = [("induction heads", C_YELLOW, [9, 18]), ("routing circuits", C_TEAL, [3, 12, 21, 30]),
                    ("arithmetic units", C_ORANGE, [34, 35, 42]), ("associative recall", C_PINK, [25, 38])]
        clabs = VGroup()
        for k, (nm, col, idx) in enumerate(circuits):
            lab = T(nm, size=17, color=col)
            clabs.add(lab)
        clabs.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(heads, RIGHT, buff=0.25)
        self.go("Inside a trained", heads.animate.set_fill(C_DIM, 0.25), rt=0.8)
        for (nm, col, idx), key, lab in zip(circuits, ["induction heads", "modular routing", "arithmetic units", "associative recall"], clabs):
            self.go(key, *[heads[i].animate.set_fill(col, 0.95).set_stroke(col, 2) for i in idx], FadeIn(lab, shift=LEFT * 0.2),
                    *[ShowPassingFlash(Line(heads[a].get_center(), heads[b].get_center()).set_stroke(col, 4)) for a, b in zip(idx, idx[1:])], rt=0.8)

        # ── THE CENTERPIECE: a fixed wire vs. an affinity recomputed from content ─────
        self.go("These functional circuits", FadeOut(VGroup(blob, acc, la, hl, hr, div, heads, hlab, clabs, title)), rt=0.9)
        self.remove(ca, cb)
        n1 = Circle(0.3, color=WHITE, stroke_width=2.5).set_fill(BLACK, 1).move_to(LEFT * 5.6 + UP * 2.2)
        n2 = n1.copy().move_to(LEFT * 1.6 + UP * 2.2)
        wire = Line(n1.get_right(), n2.get_left(), color=C_GREY, stroke_width=4)
        wl = M(r"w_{12}=0.7", size=28, color=C_GREY).next_to(wire, UP, buff=0.12)
        wst = Stream(wire, n=5, speed=0.6, color=C_GREY, radius=0.05)
        wtag = T("a physical wire: fixed, whatever the input", size=18, color=C_GREY).next_to(wire, DOWN, buff=0.35)
        self.go("without any dynamic", FadeIn(n1), FadeIn(n2), Create(wire), Write(wl), rt=0.9)
        self.add(wst)
        self.then(FadeIn(wtag), rt=0.5)

        # the sentence, the query token "it", and Q/K geometry on the right
        words = ["The", "cat", "chased", "the", "mouse", "because", "it", "was", "hungry"]
        row = token_row(words, color=C_GREY, size=22).move_to(LEFT * 2.6 + DOWN * 1.7)
        qi = 6
        row[qi][0].set_color(Q_COL).set_fill(Q_COL, 0.25)
        plane = NumberPlane(x_range=[-2.2, 2.2, 1], y_range=[-2.2, 2.2, 1], x_length=4.6, y_length=4.6,
                            background_line_style=dict(stroke_color=C_BLUE, stroke_opacity=0.18, stroke_width=1),
                            axis_config=dict(stroke_color=C_GREY, stroke_opacity=0.5)).move_to(RIGHT * 4.2 + UP * 0.3)
        kv = {1: (1.6, 0.9), 4: (-0.9, 1.6), 2: (0.2, -1.2), 0: (-1.3, -0.5), 3: (-1.2, -0.7), 5: (0.9, -0.8), 7: (0.3, -0.4), 8: (1.2, -1.1)}
        kvec = {j: np.array(v) for j, v in kv.items()}
        ang = ValueTracker(np.arctan2(0.9, 1.6) + 0.05)

        def qv():
            return 1.9 * np.array([np.cos(ang.get_value()), np.sin(ang.get_value())])

        def scores():
            s = np.array([qv() @ kvec[j] for j in sorted(kvec)])
            e = np.exp(2.2 * s - (2.2 * s).max())
            return dict(zip(sorted(kvec), e / e.sum())), dict(zip(sorted(kvec), s))
        karr = VGroup()
        for j in (1, 4, 2, 5):
            a = Arrow(plane.c2p(0, 0), plane.c2p(*kvec[j]), buff=0, color=K_COL, stroke_width=4, max_tip_length_to_length_ratio=0.12)
            karr.add(VGroup(a, M(r"k_{\text{" + words[j] + "}}", size=22, color=K_COL).next_to(a.get_end(), normalize(np.array([*kvec[j], 0])) * 0.6, buff=0.05)))
        qarr = always_redraw(lambda: Arrow(plane.c2p(0, 0), plane.c2p(*qv()), buff=0, color=Q_COL, stroke_width=6, max_tip_length_to_length_ratio=0.12))
        qlab = always_redraw(lambda: M(r"q_{\text{it}}", size=26, color=Q_COL).next_to(plane.c2p(*qv()), UP, buff=0.08))
        # affinity edges from "it" to every token, recomputed every frame
        def att_edges():
            w, _ = scores()
            g = VGroup()
            src = row[qi].get_top()
            for j, a in w.items():
                tgt = row[j].get_top()
                arc = ArcBetweenPoints(src, tgt, angle=-0.9 if j < qi else 0.9)
                g.add(arc.set_stroke(Q_COL, width=0.5 + 12 * a, opacity=0.25 + 0.75 * a))
            return g
        edges = always_redraw(att_edges)

        def dot_labels():
            _, s = scores()
            g = VGroup()
            for j in (1, 4):
                d = DecimalNumber(s[j], num_decimal_places=2, font_size=22, color=WHITE, include_sign=True)
                d.next_to(plane.c2p(*kvec[j]), DOWN if j == 1 else LEFT, buff=0.25)
                g.add(d)
            return g
        dls = always_redraw(dot_labels)
        eq = M(r"\alpha_{j}", "=", r"\mathrm{softmax}_j", r"\Big(", r"q_{\text{it}}", r"\cdot", r"k_j", r"/\sqrt{d}", r"\Big)", size=34).to_edge(UP, buff=0.4).shift(RIGHT * 2.6)
        eq[4].set_color(Q_COL); eq[6].set_color(K_COL)
        self.go("The weights remain", FadeIn(row, lag_ratio=0.05), Create(plane), rt=1.2)
        locks = VGroup(*[label_box(s, c, size=16) for s, c in [("W_Q  fixed", Q_COL), ("W_K  fixed", K_COL)]]).arrange(RIGHT, buff=0.2).next_to(plane, DOWN, buff=0.2)
        self.then(FadeIn(karr, lag_ratio=0.2), FadeIn(locks), rt=1.0, upto="yet the activation flow")
        self.add(qarr, qlab)
        self.go("yet the activation flow", Write(eq), FadeIn(edges), rt=1.0)
        self.add(dls)
        # change ONE input word: hungry → scared ; the query rotates, the affinity moves to "mouse"
        new = token_row(["scared"], color=C_PINK, size=22)[0].move_to(row[8])
        self.then(ang.animate.set_value(ang.get_value() + 0.12), rt=0.8)
        self.go("multi-step algorithmic", Transform(row[8], new), rt=0.5)
        self.then(ang.animate.set_value(np.arctan2(1.6, -0.9) - 0.05), wst.speed.animate.set_value(0.6), rt=1.8, upto="In seminal work")
        self.then(Indicate(wire, color=C_GREY), Indicate(locks), rt=0.6, upto="In seminal work")
        back = token_row(["hungry"], color=C_GREY, size=22)[0].move_to(row[8])
        self.then(Transform(row[8], back), ang.animate.set_value(np.arctan2(0.9, 1.6) + 0.05), rt=1.2, upto="In seminal work")

        # ── Olsson et al.: the real paper, the exact line ───────────────────────────────
        self.remove(edges, dls, qarr, qlab)
        page = PaperPage("induction", 0, height=7.2).move_to(RIGHT * 3.4 + DOWN * 2.2)
        hlr = page.hl("are attention heads that implement a simple algorithm to complete token sequences like")
        self.go("In seminal work", FadeOut(VGroup(row, plane, karr, eq, locks, n1, n2, wire, wl, wst, wtag)), FadeIn(page, shift=UP), rt=1.2)
        self.then(frame.animate.scale(0.55).move_to(hlr.get_center() + DOWN * 0.2), rt=1.2, upto="coordinate across layers")
        self.go("coordinate across layers", FadeIn(hlr, lag_ratio=0.3), rt=1.2)
        self.go("implicit gradient descent", frame.animate.scale(1 / 0.55).move_to(ORIGIN), Group(page, hlr).animate.scale(0.5).to_corner(UR, buff=0.4), rt=1.4,
                upto="When an induction head")

        # ── an induction head at work: [A][B] … [A] → [B] ─────────────────────────────
        seq = ["Mr", "Durs", "ley", "was", "proud", "…", "said", "Mr", "?"]
        srow = token_row(seq, color=C_GREY, size=26).move_to(DOWN * 0.6 + LEFT * 0.8)
        self.go("When an induction head", FadeIn(srow, lag_ratio=0.08), rt=1.0)
        cur = srow[7]
        self.then(cur[0].animate.set_color(Q_COL).set_fill(Q_COL, 0.3), rt=0.4)
        scan = Dot(cur.get_top() + UP * 0.25, radius=0.08, color=Q_COL)
        self.go("copies previous", FadeIn(scan), rt=0.2)
        for j in range(6, -1, -1):
            self.play(scan.animate.move_to(srow[j].get_top() + UP * 0.25), srow[j][0].animate.set_stroke(Q_COL, 2.5), run_time=0.16)
            if j != 0:
                self.play(srow[j][0].animate.set_stroke(C_GREY, 1.4), run_time=0.04)
        qk = ArcBetweenPoints(cur.get_top() + UP * 0.1, srow[0].get_top() + UP * 0.1, angle=-0.8).set_stroke(Q_COL, 5)
        qkl = M(r"q_{\text{Mr}}\cdot k_{\text{Mr}} \gg 0", size=28, color=Q_COL).next_to(qk, UP, buff=0.1)
        self.go("bilinear query-key", Create(qk), Write(qkl), srow[0][0].animate.set_fill(Q_COL, 0.4), rt=1.2)
        nxt = ArcBetweenPoints(srow[1].get_bottom() + DOWN * 0.1, srow[8].get_bottom() + DOWN * 0.1, angle=0.7).set_stroke(V_COL, 5)
        cp = srow[1][1].copy()
        self.go("retrieving arbitrary", Create(nxt), srow[1][0].animate.set_fill(V_COL, 0.4), rt=0.8)
        self.then(cp.animate.move_to(srow[8][1]).set_color(V_COL), FadeOut(srow[8][1]), rt=0.8, upto="Biologically-inspired")
        pat = M(r"[A][B]\ \dots\ [A]\ \rightarrow\ [B]", size=36, color=C_YELLOW).next_to(srow, DOWN, buff=1.0)
        self.then(Write(pat), rt=0.6, upto="Biologically-inspired")

        # ── a Hebbian associative memory tries the same lookup: crosstalk ───────────────
        ind = VGroup(srow, qk, qkl, nxt, cp, scan, pat)
        self.go("Biologically-inspired", ind.animate.scale(0.6).to_edge(UP, buff=0.9).shift(LEFT * 2), rt=1.0)
        rngh = np.random.default_rng(8)
        d = 8
        keys = rngh.normal(size=(5, d)); keys[1] = keys[0] * 0.85 + 0.5 * rngh.normal(size=d)
        keys /= np.linalg.norm(keys, axis=1, keepdims=True)
        vals = np.eye(5)
        Mh = sum(np.outer(vals[i], keys[i]) for i in range(5))
        mhm = heatmap((Mh - Mh.min()) / (Mh.max() - Mh.min()), cell=0.32, cmap=(BLACK, C_GREEN, WHITE)).move_to(LEFT * 3.0 + DOWN * 1.3)
        mhl = M(r"M=\sum_i v_i k_i^{\top}", size=30, color=C_GREEN).next_to(mhm, UP, buff=0.2)
        self.go("token-specific lookup", FadeIn(mhm, lag_ratio=0.01), Write(mhl), rt=1.0)
        out = Mh @ keys[0]
        out = np.clip(out / out.max(), 0, 1)
        bars = VGroup(*[Rectangle(width=0.4, height=0.05 + 1.8 * v).set_stroke(width=0).set_fill(C_PINK if i != 0 else C_GREEN, 0.9) for i, v in enumerate(out)])
        bars.arrange(RIGHT, buff=0.1, aligned_edge=DOWN).move_to(RIGHT * 2.4 + DOWN * 1.6)
        bl = VGroup(M(r"M k_{\text{Mr}}", size=28).next_to(bars, UP, buff=0.2),
                    T("wanted value 1 only · got crosstalk", size=18, color=C_PINK).next_to(bars, DOWN, buff=0.2))
        self.go("catastrophic interference", FadeIn(bl[0]), *[GrowFromEdge(b, DOWN) for b in bars], rt=1.0)
        self.then(FadeIn(bl[1]), Indicate(bars[1], color=C_RED), rt=0.8, upto="How could a rigid")

        # ── the physical graph tries to imitate attention by adding wires ─────────────
        self.go("How could a rigid", FadeOut(VGroup(ind, mhm, mhl, bars, bl)), FadeOut(Group(page, hlr)), rt=0.8)
        nN = ValueTracker(4)

        def wiring():
            n = int(nN.get_value())
            pts = [np.array([np.cos(a) * 2.2, np.sin(a) * 2.2, 0]) + LEFT * 3.2 for a in np.linspace(0, TAU, n, endpoint=False)]
            g = VGroup(*[Line(pts[i], pts[j], stroke_width=0.8, color=C_GREEN, stroke_opacity=0.6) for i in range(n) for j in range(i + 1, n)])
            g.add(*[Dot(p, radius=0.06, color=C_GREEN) for p in pts])
            return g
        wg = always_redraw(wiring)
        wc = always_redraw(lambda: M(r"\text{wires} = %d" % (int(nN.get_value()) * (int(nN.get_value()) - 1) // 2), size=30, color=C_GREEN).next_to(LEFT * 3.2 + DOWN * 2.6, DOWN, buff=0.1))
        self.add(wg, wc)
        att = VGroup(M(r"A = \mathrm{softmax}(QK^\top/\sqrt d)", size=32, color=C_BLUE),
                     T("same W_Q, W_K for any N — recomputed per input", size=18, color=C_BLUE)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.2 + UP * 0.6)
        self.then(FadeIn(att), nN.animate.set_value(10), rt=2.0, upto="This paradox cannot")
        topo = VGroup(T("topology", size=26, color=C_GREEN), M(r"\neq", size=40), T("metric routing", size=26, color=C_BLUE)).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.2 + DOWN * 1.4)
        self.go("This paradox cannot", nN.animate(rate_func=linear).set_value(28), Write(topo), rt=2.2)
        self.go("engineering patience", Indicate(topo), rt=1.0, upto="To understand why")

        # ── three theorems ─────────────────────────────────────────────────────────────
        cards = VGroup(*[VGroup(RoundedRectangle(width=3.8, height=2.2, corner_radius=0.15, color=c, stroke_width=2).set_fill(c, 0.08),
                                VGroup(T(f"Theorem {i + 1}", size=26, color=c, weight=BOLD), T(s, size=18, color=WHITE)).arrange(DOWN, buff=0.15))
                         for i, (s, c) in enumerate([("rank collapse", C_YELLOW), ("routing latency", C_GREEN), ("hardware lottery", C_ORANGE)])])
        for c_ in cards:
            c_[1].move_to(c_[0])
        cards.arrange(RIGHT, buff=0.4).move_to(UP * 0.0)
        self.remove(wg, wc)
        self.go("To understand why", FadeOut(VGroup(att, topo)), rt=0.6)
        self.go("three foundational", LaggedStart(*[FadeIn(c_, shift=UP * 0.3) for c_ in cards], lag_ratio=0.35), rt=2.0)
        self.then(cards[1:].animate.set_opacity(0.25), cards[0].animate.scale(1.15), rt=1.0)
        self.finish()
