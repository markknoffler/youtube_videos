"""Chapter 03 — The Self-Organizing Hypothesis (Hebb → Oja → Kohonen → rewiring → collapse)."""
from common import *


def oja_run(steps=400, eta=0.02, seed=0):
    """Real Oja's-rule simulation on anisotropic 2-D data: returns data and the weight trajectory."""
    rng = np.random.default_rng(seed)
    ang = 0.55
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    X = (rng.normal(size=(steps, 2)) * [1.5, 0.45]) @ R.T
    w = np.array([-0.3, 0.9]); traj = [w.copy()]
    for x in X:
        y = w @ x
        w = w + eta * y * (x - y * w)
        traj.append(w.copy())
    evals, evecs = np.linalg.eigh(np.cov(X.T))
    return X, np.array(traj), evecs[:, -1]


def som_run(n=9, steps=2400, seed=1, snaps=120):
    """Kohonen SOM: an n×n lattice learning the unit square. Returns lattice snapshots."""
    rng = np.random.default_rng(seed)
    W = 0.5 + 0.12 * rng.normal(size=(n, n, 2))
    gi, gj = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    out = [W.copy()]
    for t in range(steps):
        x = rng.random(2)
        d = ((W - x) ** 2).sum(-1)
        bi, bj = np.unravel_index(d.argmin(), d.shape)
        frac = t / steps
        sigma = 3.0 * (0.08 / 3.0) ** frac * n / 9
        lr = 0.5 * (0.02 / 0.5) ** frac
        h = np.exp(-((gi - bi) ** 2 + (gj - bj) ** 2) / (2 * sigma ** 2))[..., None]
        W += lr * h * (x - W)
        if (t + 1) % (steps // snaps) == 0:
            out.append(W.copy())
    return np.array(out)


class Ch03(Chapter):
    CH = 3

    def construct(self):
        C = self.times(
            "The dream of self", "older than backpropagation", "In 1949", "Organization of Behavior", "foundational postulate",
            "when an axon", "near enough", "repeatedly takes part", "some growth process", "In popular culture", "fire together",
            "wire together", "In the decades", "rigorous computational", "In 1982", "normalized Hebbian", "local weight decay",
            "principal eigenvector", "without any external", "Concurrently", "Self-Organizing Maps", "uncoordinated",
            "neighboring units", "spontaneously fold", "ordered topological", "Later, researchers", "BCM theory",
            "Dynamic Rewiring", "weak connections", "randomly sprouted", "local activity levels", "breathtakingly elegant",
            "freedom to sculpt", "general intelligence", "modular specialization", "dynamic routing", "bottom up",
            "For decades", "holy grail", "catastrophic forgetting", "growing new modules", "Yet when these ideas",
            "modern deep learning", "unexpected crisis", "failed to materialize", "chaotic representational")
        tag = T("03 · THE SELF-ORGANIZING HYPOTHESIS", size=16, color=C_GREY).to_corner(UL, buff=0.35)

        # ── bridge: the living field from ch02 shrinks onto a history axis ───────────
        field = SpikeField(n=30, width=12, height=6, rate=3, seed=4)
        self.add(field, tag)
        axis = NumberLine(x_range=[1940, 2030, 10], length=12, color=C_GREY, include_numbers=True, font_size=18,
                          decimal_number_config=dict(group_with_commas=False, num_decimal_places=0)).to_edge(DOWN, buff=0.55)
        self.go("The dream of self", field.animate.scale(0.35).move_to(UP * 1.8), Create(axis), rt=2.0)
        bp = VGroup(Dot(axis.n2p(1986), color=C_RED), T("backprop 1986", size=16, color=C_RED).next_to(axis.n2p(1986), UP, buff=0.25))
        hb = VGroup(Dot(axis.n2p(1949), color=C_GREEN), T("Hebb 1949", size=16, color=C_GREEN).next_to(axis.n2p(1949), UP, buff=0.25))
        self.go("older than backpropagation", FadeIn(bp, shift=DOWN * 0.2), rt=0.6)
        self.then(FadeIn(hb, shift=DOWN * 0.2), Create(CurvedArrow(axis.n2p(1986) + UP * 0.55, axis.n2p(1949) + UP * 0.55, angle=0.6, color=C_GREY, tip_length=0.15)),
                  rt=1.2, upto="In 1949")

        # ── Hebb: photo, book, and the postulate spoken word-by-word ─────────────────
        hebb = framed_image(os.path.join(PROJECT, "remotion_studio/public/assets/real_world/researchers/donald_hebb.jpg"), height=2.2,
                            caption="Hebb's cell assemblies (1949)").to_corner(UL, buff=0.7).shift(DOWN * 0.3)
        self.go("In 1949", field.alpha.animate.set_value(0.0), FadeIn(hebb, shift=RIGHT), Indicate(hb), rt=1.0)
        self.remove(field)
        book = VGroup(RoundedRectangle(width=1.5, height=2.0, corner_radius=0.06, color=C_GOLD, stroke_width=2).set_fill(C_GOLD, 0.15),
                      T("The\nOrganization\nof Behavior", size=15, color=C_GOLD, line_spacing=0.8)).next_to(hebb, RIGHT, buff=0.4)
        book[1].move_to(book[0])
        self.go("Organization of Behavior", FadeIn(book, shift=UP * 0.3), rt=0.8)
        quote_txt = ("when an axon of cell A is near enough to excite cell B and repeatedly takes part in firing it, "
                     "some growth process or metabolic change takes place")
        quote = wrap_words(quote_txt, width=6.2, size=26, slant=ITALIC).move_to(RIGHT * 2.6 + UP * 2.0)
        self.go("foundational postulate", FadeIn(quote, lag_ratio=0.02), rt=1.0, upto="when an axon")
        self.karaoke(quote, self.word_times(quote_txt, self.t("when an axon")))
        # the mechanism, built as the words arrive
        A = Circle(0.38, color=C_BLUE, stroke_width=3).set_fill(C_BLUE, 0.2).move_to(LEFT * 1.0 + DOWN * 1.1)
        B = Circle(0.38, color=C_PINK, stroke_width=3).set_fill(C_PINK, 0.2).move_to(RIGHT * 4.4 + DOWN * 1.1)
        Al, Bl = T("A", size=24, color=C_BLUE).move_to(A), T("B", size=24, color=C_PINK).move_to(B)
        axon = VMobject(stroke_color=C_BLUE, stroke_width=3).set_points_smoothly(
            [A.get_right(), LEFT * 0.0 + DOWN * 0.8, RIGHT * 1.6 + DOWN * 1.4, RIGHT * 3.0 + DOWN * 1.0, B.get_left() + LEFT * 0.12])
        self.go("when an axon", FadeIn(VGroup(A, Al)), Create(axon), rt=1.4, upto="near enough")
        wsyn = ValueTracker(0.6)
        knob = always_redraw(lambda: Dot(B.get_left() + LEFT * 0.12, radius=0.04 + 0.05 * wsyn.get_value(), color=C_YELLOW))
        self.go("near enough", FadeIn(VGroup(B, Bl)), rt=0.6)
        self.add(knob)
        for k in range(3):
            self.play(ShowPassingFlash(axon.copy().set_stroke(C_YELLOW, 6), time_width=0.4), Flash(A, color=C_BLUE, line_length=0.2), run_time=0.45)
            self.play(Flash(B, color=C_PINK, line_length=0.25), run_time=0.3)
        self.go("some growth process", wsyn.animate.set_value(3.0), Flash(knob.get_center(), color=C_YELLOW), rt=1.6, upto="In popular culture")

        # ── "fire together, wire together": a population and Δw = η x y ───────────────
        quote.clear_updaters()
        self.go("In popular culture", FadeOut(Group(hebb, book, quote, A, B, Al, Bl, axon)), rt=0.8)
        self.remove(knob)
        rng = np.random.default_rng(2)
        P = [np.array([np.cos(a) * 2.4, np.sin(a) * 1.6, 0]) + LEFT * 2.6 + UP * 0.6 for a in np.linspace(0, TAU, 9, endpoint=False)]
        pop = VGroup(*[Circle(0.22, color=WHITE, stroke_width=2).set_fill(BLACK, 1).move_to(p) for p in P])
        pairs = [(i, j) for i in range(9) for j in range(i + 1, 9)]
        wts = {pq: 0.3 for pq in pairs}
        eds = {pq: Line(P[pq[0]], P[pq[1]], stroke_width=0.6, color=C_GREY, stroke_opacity=0.35) for pq in pairs}
        edg = VGroup(*eds.values())
        motto = VGroup(T("neurons that ", size=30), T("fire together", size=30, color=C_YELLOW), T(", ", size=30),
                       T("wire together", size=30, color=C_GREEN)).arrange(RIGHT, buff=0.08, aligned_edge=DOWN).move_to(UP * 3.1)
        self.then(FadeIn(edg), FadeIn(pop, lag_ratio=0.1), rt=1.0)
        eqh = M(r"\Delta w_{ij}", "=", r"\eta", r"\, x_i", r"\, y_j", size=46).move_to(RIGHT * 3.6 + UP * 0.6)
        eqh[3].set_color(C_BLUE); eqh[4].set_color(C_PINK)
        assemblies = [(0, 1, 2), (4, 5, 6), (2, 3)]
        self.go("fire together", FadeIn(motto[:3]), rt=0.4)
        for asm in assemblies:
            self.play(*[pop[i].animate.set_fill(C_YELLOW, 1) for i in asm], run_time=0.25)
            anims = []
            for a in asm:
                for b in asm:
                    if a < b:
                        wts[(a, b)] += 0.9
                        anims.append(eds[(a, b)].animate.set_stroke(C_GREEN, width=1 + 3 * wts[(a, b)], opacity=0.9))
            self.play(*anims, *[pop[i].animate.set_fill(BLACK, 1) for i in asm], run_time=0.35)
        self.go("wire together", FadeIn(motto[3]), rt=0.5)
        self.go("In the decades", Write(eqh[0:3]), rt=0.9)
        self.go("rigorous computational", Write(eqh[3:]), rt=1.0, upto="In 1982")
        # Hebb alone diverges: plot |w| exploding
        grow = LiveAxes([0, 10, 5], [0, 10, 5], width=3.0, height=1.6).next_to(eqh, DOWN, buff=0.5)
        tgw = ValueTracker(0)
        xs = np.linspace(0, 10, 100)
        gc = grow.live_curve(xs, np.minimum(10, 0.3 * np.exp(0.38 * xs)), tgw, color=C_RED)
        gl = M(r"\|w\|\to\infty", size=26, color=C_RED).next_to(grow, RIGHT, buff=0.1)
        self.then(FadeIn(grow), rt=0.4)
        self.add(gc)
        self.then(tgw.animate.set_value(10), FadeIn(gl), rt=1.2, upto="In 1982")

        # ── Oja 1982: a single neuron finds the principal eigenvector (live simulation) ─
        X, traj, pc = oja_run()
        ax = Axes(x_range=[-4, 4], y_range=[-3, 3], x_length=6.4, y_length=4.8, axis_config=dict(color=C_DIM, include_tip=False)).move_to(LEFT * 2.6 + UP * 0.2)
        cloud = VGroup(*[Dot(ax.c2p(*x), radius=0.025, color=C_BLUE).set_opacity(0.6) for x in X[:260]])
        self.remove(gc)
        self.go("In 1982", FadeOut(VGroup(pop, edg, motto, grow, gl)), FadeIn(VGroup(Dot(axis.n2p(1982), color=C_YELLOW),
                T("Oja 1982", size=16, color=C_YELLOW).next_to(axis.n2p(1982), UP, buff=0.6))), rt=0.8)
        eqo = M(r"\Delta w", "=", r"\eta\, y", r"\,(x", r"- y\,w", ")", size=46).move_to(RIGHT * 3.6 + UP * 0.6)
        self.go("normalized Hebbian", Create(ax), LaggedStart(*[FadeIn(d, scale=0.3) for d in cloud], lag_ratio=0.004),
                TransformMatchingTex(eqh, eqo), rt=1.6)
        self.go("local weight decay", Indicate(eqo[4], color=C_YELLOW, scale_factor=1.3), rt=0.8)
        k = ValueTracker(0)
        warr = always_redraw(lambda: Arrow(ax.c2p(0, 0), ax.c2p(*(2.2 * traj[int(k.get_value())])), buff=0, color=C_YELLOW, stroke_width=6,
                                           max_tip_length_to_length_ratio=0.15))
        wlab = always_redraw(lambda: M("w", size=34, color=C_YELLOW).next_to(warr.get_end(), UR, buff=0.05))
        unit = DashedVMobject(Circle(radius=ax.c2p(2.2, 0)[0] - ax.c2p(0, 0)[0], color=C_GREY, stroke_width=1.5).move_to(ax.c2p(0, 0)), num_dashes=40)
        self.add(warr, wlab)
        sample = Dot(radius=0.07, color=WHITE)
        self.then(Create(unit), k.animate(rate_func=linear).set_value(120), rt=1.6, upto="principal eigenvector")
        norm_l = M(r"\|w\| \to 1", size=30, color=C_GREY).next_to(eqo, DOWN, buff=0.4)
        self.then(FadeIn(norm_l), rt=0.4)
        pcl = DashedLine(ax.c2p(*(-3.6 * pc)), ax.c2p(*(3.6 * pc)), color=C_GREEN, stroke_width=3)
        pcn = M(r"v_1 \text{ of } C=\mathbb{E}[xx^\top]", size=28, color=C_GREEN).next_to(eqo, DOWN, buff=1.1)
        self.go("principal eigenvector", k.animate(rate_func=linear).set_value(400), Create(pcl), Write(pcn), rt=2.2, upto="without any external")
        noteach = T("no teacher · no global loss · purely local", size=20, color=C_GREY).next_to(pcn, DOWN, buff=0.4)
        self.go("without any external", FadeIn(noteach, shift=UP * 0.2), rt=0.8, upto="Concurrently")

        # ── Kohonen SOM: a crumpled lattice unfolds into an ordered map ───────────────
        snaps = som_run()
        som_ax = Square(4.6, color=C_DIM, stroke_width=1.5).move_to(LEFT * 2.6 + UP * 0.2)
        o = som_ax.get_corner(DL)
        sk = ValueTracker(0)

        def lattice():
            Wt = snaps[int(np.clip(sk.get_value(), 0, len(snaps) - 1))]
            g = VGroup()
            n = Wt.shape[0]
            for i in range(n):
                g.add(VMobject(stroke_color=C_TEAL, stroke_width=1.8).set_points_as_corners([o + 4.6 * np.array([*Wt[i, j], 0]) for j in range(n)]))
                g.add(VMobject(stroke_color=C_TEAL, stroke_width=1.8).set_points_as_corners([o + 4.6 * np.array([*Wt[j, i], 0]) for j in range(n)]))
            for i in range(n):
                for j in range(n):
                    g.add(Dot(o + 4.6 * np.array([*Wt[i, j], 0]), radius=0.045, color=interpolate_color(ManimColor(C_TEAL), ManimColor(C_YELLOW), (i + j) / (2 * n - 2))))
            return g
        lat = always_redraw(lattice)
        self.remove(warr, wlab)
        self.go("Concurrently", FadeOut(VGroup(ax, cloud, unit, pcl, norm_l, noteach, pcn)), FadeOut(eqo), rt=0.8)
        soml = T("Kohonen · Self-Organizing Map", size=22, color=C_TEAL).next_to(som_ax, UP, buff=0.15)
        self.go("Self-Organizing Maps", Create(som_ax), FadeIn(soml), FadeIn(VGroup(Dot(axis.n2p(1982), color=C_TEAL))), rt=0.8)
        self.add(lat)
        eqs = M(r"w_j \leftarrow w_j + \eta\, h_{j,b}(t)\,(x - w_j)", size=34).move_to(RIGHT * 3.6 + UP * 1.4)
        hb_l = M(r"b=\arg\min_j\|x-w_j\|", size=30, color=C_YELLOW).next_to(eqs, DOWN, buff=0.3)
        self.go("uncoordinated", Write(eqs), sk.animate(rate_func=linear).set_value(10), rt=1.4)
        self.go("neighboring units", Write(hb_l), sk.animate(rate_func=linear).set_value(30), rt=1.6)
        self.go("spontaneously fold", sk.animate(rate_func=linear).set_value(85), rt=2.4, upto="ordered topological")
        self.go("ordered topological", sk.animate(rate_func=smooth).set_value(120), rt=1.4, upto="Later, researchers")

        # ── BCM & dynamic rewiring: the lattice becomes a graph that prunes & sprouts ──
        Wf = snaps[-1]
        nn_ = Wf.shape[0]
        gp = [o + 4.6 * np.array([*Wf[i, j], 0]) for i in range(nn_) for j in range(nn_)]
        gnodes = VGroup(*[Dot(p, radius=0.06, color=C_TEAL) for p in gp])
        el = []
        for a in range(len(gp)):
            for b in range(a + 1, len(gp)):
                if np.linalg.norm(gp[a] - gp[b]) < 0.75:
                    el.append((a, b, Line(gp[a], gp[b], color=C_TEAL, stroke_width=1.6)))
        gedges = VGroup(*[e for _, _, e in el])
        self.go("Later, researchers", FadeOut(lat), FadeIn(gedges), FadeIn(gnodes), FadeOut(soml), rt=0.8)
        bcm = Axes(x_range=[0, 2, 1], y_range=[-0.6, 1, 1], x_length=3.0, y_length=1.8, axis_config=dict(color=C_GREY, include_tip=False)).move_to(RIGHT * 3.6 + DOWN * 1.2)
        th = ValueTracker(0.8)
        phi = always_redraw(lambda: bcm.plot(lambda y: y * (y - th.get_value()), x_range=[0, 2], color=C_ORANGE))
        bcm_l = VGroup(M(r"\phi(y,\theta_M)", size=24, color=C_ORANGE).next_to(bcm, UP, buff=0.1),
                       M(r"\theta_M = \mathbb{E}[y^2]", size=22, color=C_GREY).next_to(bcm, DOWN, buff=0.1))
        self.go("BCM theory", FadeOut(eqs), FadeOut(hb_l), FadeIn(bcm), FadeIn(bcm_l), rt=0.8)
        self.add(phi)
        self.then(th.animate.set_value(1.4), rt=1.0, upto="Dynamic Rewiring")
        rngw = np.random.default_rng(4)
        weights = rngw.random(len(el))
        self.go("Dynamic Rewiring", *[e.animate.set_stroke(C_TEAL if w > 0.35 else C_RED, width=0.6 + 3 * w) for (_, _, e), w in zip(el, weights)], rt=1.2)
        weak = VGroup(*[e for (_, _, e), w in zip(el, weights) if w <= 0.35])
        self.go("weak connections", *[Uncreate(e) for e in weak], rt=1.2)
        sprouts = VGroup()
        for _ in range(14):
            a, b = rngw.integers(len(gp), size=2)
            if a != b:
                sprouts.add(DashedLine(gp[a], gp[b], color=C_GREEN, stroke_width=2))
        self.go("randomly sprouted", LaggedStart(*[Create(s) for s in sprouts], lag_ratio=0.1), rt=1.4)
        self.go("local activity levels", LaggedStart(*[Flash(gnodes[i], color=C_YELLOW, line_length=0.15) for i in rngw.integers(len(gp), size=10)], lag_ratio=0.1),
                th.animate.set_value(0.6), rt=1.6, upto="breathtakingly elegant")

        # ── the elegant hypothesis: local rules → modules emerge (the graph organizes) ─
        keep = [(a, b) for (a, b, e), w in zip(el, weights) if w > 0.35]
        self.remove(phi)
        self.go("breathtakingly elegant", FadeOut(VGroup(bcm, bcm_l, sprouts)), FadeOut(VGroup(*[m for m in self.mobjects if m is axis or (isinstance(m, VMobject) and m.get_center()[1] < -2.6 and m not in gnodes and m not in gedges and m is not getattr(self, 'captions', None))])), VGroup(gnodes, gedges).animate.move_to(ORIGIN + UP * 0.3), rt=1.2)
        surv = VGroup(*[e for (a, b, e), w in zip(el, weights) if w > 0.35])
        centers = [LEFT * 3.4 + UP * 1.2, RIGHT * 3.4 + UP * 1.2, DOWN * 1.6]
        cols = [C_YELLOW, C_PINK, C_BLUE]
        assign = [((i // nn_) * 3 // nn_ if (j < nn_ // 2) else 1 + ((i // nn_) > nn_ // 2)) % 3 for i, j in [(k, k % nn_) for k in range(len(gp))]]
        rngm = np.random.default_rng(7)
        targ = [centers[assign[k]] + 1.1 * np.array([*rngm.normal(size=2) * [1, 0.7], 0]) for k in range(len(gp))]
        new_edges = VGroup()
        for (a, b) in keep:
            if assign[a] == assign[b]:
                new_edges.add(Line(targ[a], targ[b], color=cols[assign[a]], stroke_width=1.8, stroke_opacity=0.8))
        bridges = VGroup(*[Line(centers[i], centers[j], color=C_GREY, stroke_width=2, stroke_opacity=0.5) for i, j in [(0, 1), (1, 2), (0, 2)]])
        self.go("freedom to sculpt", *[d.animate.move_to(targ[k]).set_color(cols[assign[k]]) for k, d in enumerate(gnodes)],
                ReplacementTransform(surv, new_edges), rt=2.4, upto="general intelligence")
        mods = VGroup(*[T(s, size=20, color=c) for s, c in [("module A", C_YELLOW), ("module B", C_PINK), ("module C", C_BLUE)]])
        for m, c in zip(mods, centers):
            m.move_to(c + UP * 1.5 + (DOWN * 3.0 if c[1] < 0 else 0))
        self.go("general intelligence", Create(bridges), rt=0.8)
        self.go("modular specialization", LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in mods], lag_ratio=0.25), rt=1.0)
        route = VMobject().set_points_smoothly([centers[0], centers[2] + LEFT * 0.4, centers[1]])
        rs = Stream(route, n=10, speed=0.5, color=WHITE, radius=0.05)
        self.go("dynamic routing", FadeIn(rs), rt=0.6)
        hyp = T("local rules  →  emergent modular intelligence", size=26, color=C_GREEN).to_edge(DOWN, buff=1.5)
        self.go("bottom up", Write(hyp), rt=1.2, upto="For decades")
        grail = VGroup(Star(5, outer_radius=0.25, color=C_GOLD).set_fill(C_GOLD, 0.6), T("the holy grail", size=24, color=C_GOLD)).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.6)
        self.go("holy grail", FadeIn(grail, scale=0.6), rt=0.8)
        self.go("catastrophic forgetting", Indicate(new_edges, color=WHITE), rt=1.0)
        nm_c = RIGHT * 0.2 + UP * 2.6
        newmod = VGroup(*[Dot(nm_c + 0.5 * np.array([*rngm.normal(size=2) * [1, 0.5], 0]), radius=0.06, color=C_GREEN) for _ in range(7)])
        newb = VGroup(Line(nm_c, centers[0], color=C_GREY, stroke_width=1.5), Line(nm_c, centers[1], color=C_GREY, stroke_width=1.5))
        self.go("growing new modules", LaggedStart(*[GrowFromCenter(d) for d in newmod], lag_ratio=0.1), Create(newb), rt=1.4, upto="Yet when these ideas")

        # ── scale it up: dense token interactions flood the routing → collapse ────────
        rs.clear_updaters()
        self.go("Yet when these ideas", FadeOut(rs), FadeOut(hyp), FadeOut(grail), rt=0.6)
        streams = []
        for k in range(10):
            a = TAU * k / 10
            pth = Line(7.5 * np.array([np.cos(a), np.sin(a) * 0.6, 0]), centers[k % 3])
            st = Stream(pth, n=6, speed=0.9, color=C_ORANGE, radius=0.04, square=True)
            streams.append(st)
        tok_l = T("tokens · long contexts · billions of parameters", size=20, color=C_ORANGE).to_edge(DOWN, buff=1.2)
        self.go("modern deep learning", *[FadeIn(s) for s in streams], FadeIn(tok_l), rt=1.0)
        rng5 = np.random.default_rng(11)
        dense = VGroup(*[Line(gnodes[a].get_center(), gnodes[b].get_center(), color=C_GREY, stroke_width=0.8, stroke_opacity=0.5)
                         for a, b in rng5.integers(len(gp), size=(90, 2)) if a != b])
        self.go("unexpected crisis", LaggedStart(*[Create(d) for d in dense], lag_ratio=0.01), *[s.speed.animate.set_value(2.0) for s in streams], rt=2.0)
        rank = counter(64, fmt=1, size=36, color=C_RED).to_corner(DR, buff=0.8).shift(UP * 0.6)
        rank_l = T("effective rank", size=18, color=C_GREY).next_to(rank, UP, buff=0.1)
        self.go("failed to materialize", FadeOut(mods), *[d.animate.set_color(C_GREY) for d in gnodes], new_edges.animate.set_color(C_GREY),
                bridges.animate.set_opacity(0.1), FadeIn(rank), FadeIn(rank_l), rt=1.6, upto="chaotic representational")
        self.go("chaotic representational", *[d.animate.move_to(UP * 0.3 + 0.25 * np.array([*rng5.normal(size=2), 0])) for d in gnodes],
                *[d.animate.move_to(UP * 0.3) for d in newmod], FadeOut(new_edges), FadeOut(bridges), FadeOut(newb), dense.animate.set_opacity(0.05),
                rank.tracker.animate.set_value(1.8), rt=2.6)
        self.finish()
