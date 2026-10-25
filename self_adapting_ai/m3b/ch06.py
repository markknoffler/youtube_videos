"""Chapter 06 — Theorem 2: Routing Expressivity & Graph Latency (Moore bound made physical)."""
from common import *
import networkx as nx


def sparse_graph(n=90, d=4, seed=3, w=11.0, h=5.6, center=ORIGIN):
    """Random geometric graph with degree ≤ d (nearest neighbours, capped), connected."""
    rng = np.random.default_rng(seed)
    pts = np.c_[rng.random(n) * w - w / 2, rng.random(n) * h - h / 2]
    G = nx.Graph(); G.add_nodes_from(range(n))
    order = np.argsort(pts[:, 0])
    for i in range(n):
        dists = np.linalg.norm(pts - pts[i], axis=1)
        for j in np.argsort(dists)[1:]:
            if G.degree(i) >= d:
                break
            if G.degree(j) < d and not G.has_edge(i, j) and dists[j] < 1.6:
                G.add_edge(i, j)
    comps = list(nx.connected_components(G))
    while len(comps) > 1:                      # stitch components with nearest pairs
        a, b = list(comps[0]), list(comps[1])
        D = np.linalg.norm(pts[a][:, None] - pts[b][None], axis=2)
        i, j = np.unravel_index(D.argmin(), D.shape)
        G.add_edge(a[i], b[j]); comps = list(nx.connected_components(G))
    P = [center + np.array([x, y, 0]) for x, y in pts]
    return G, P


class Ch06(Chapter):
    CH = 6

    def construct(self):
        C = self.times(
            "second fundamental", "Theorem 2", "Advocates", "highly sparse", "six layers", "Let us subject", "Consider a dynamic",
            "at most d synaptic", "immediate neighbors", "From extremal", "Moore Bound", "diameter of any graph", "bounded below",
            "log N divided", "What does this lower", "If token A", "opposite side", "cannot travel", "multi-hop relay",
            "Each intermediate hop", "nonlinear distortion", "attenuates gradient", "If an architecture", "degree sixteen",
            "five to six", "In recurrent execution", "decay exponentially", "spectral norms", "vanishing or exploding",
            "In stark contrast", "geometric topology", "multi-head attention layer", "dynamic bipartite", "diameter of exactly one",
            "Every single token", "single, parallelized", "depth", "Sparse self-organizing", "insurmountable", "global context")
        frame = self.camera.frame
        tag = T("06 · THEOREM 2 — ROUTING LATENCY", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        card = VGroup(RoundedRectangle(width=4.4, height=2.5, corner_radius=0.15, color=C_GREEN, stroke_width=2).set_fill(C_GREEN, 0.08),
                      VGroup(T("Theorem 2", size=30, color=C_GREEN, weight=BOLD), T("routing latency", size=20)).arrange(DOWN, buff=0.15))
        self.add(card, tag)
        head = VGroup(T("Theorem 2", size=26, color=C_GREEN, weight=BOLD), T("Routing expressivity & graph latency bounds", size=22)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.75)
        self.go("second fundamental", Indicate(card, color=C_GREEN), rt=1.0)
        self.go("Theorem 2", ReplacementTransform(card, head), rt=1.4)

        # ── the cortex: six layers, local wiring only ─────────────────────────────────
        rng = np.random.default_rng(1)
        bands = VGroup(*[Rectangle(width=11, height=0.7, stroke_width=0).set_fill(interpolate_color(ManimColor(C_DIM), ManimColor(C_GREEN), 0.1 + 0.08 * i), 0.5)
                         for i in range(6)]).arrange(DOWN, buff=0.06).move_to(DOWN * 0.4)
        roman = VGroup(*[T(r, size=18, color=C_GREY).next_to(b, LEFT, buff=0.2) for r, b in zip(["I", "II", "III", "IV", "V", "VI"], bands)])
        cells = VGroup(*[Dot(b.get_center() + RIGHT * (rng.random() - 0.5) * 10.6 + UP * (rng.random() - 0.5) * 0.5, radius=0.05, color=C_GREEN)
                         for b in bands for _ in range(14)])
        loc = VGroup()
        for a in cells:
            for b in cells:
                if a is not b and np.linalg.norm(a.get_center() - b.get_center()) < 0.75 and rng.random() < 0.5:
                    loc.add(Line(a.get_center(), b.get_center(), stroke_width=1, color=C_GREEN, stroke_opacity=0.5))
        self.go("Advocates", FadeIn(bands, lag_ratio=0.1), rt=1.0)
        self.go("highly sparse", FadeIn(cells, lag_ratio=0.01), Create(loc, lag_ratio=0.01), rt=1.6)
        self.go("six layers", LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in roman], lag_ratio=0.12), rt=1.0, upto="Let us subject")

        # ── abstraction: N nodes, degree ≤ d ─────────────────────────────────────────
        G, P = sparse_graph(n=90, d=4, center=DOWN * 0.4)
        nodes = VGroup(*[Dot(p, radius=0.07, color=C_GREEN) for p in P])
        edges = {e: Line(P[e[0]], P[e[1]], stroke_width=1.6, color=C_GREEN, stroke_opacity=0.55) for e in G.edges}
        evg = VGroup(*edges.values())
        self.go("Let us subject", FadeOut(VGroup(bands, roman, loc)), *[c.animate.move_to(P[i % len(P)]) for i, c in enumerate(cells[:90])],
                FadeOut(cells[90:]), rt=1.6)
        self.remove(*cells[:90]); self.add(nodes)
        self.go("Consider a dynamic", Create(evg, lag_ratio=0.005), rt=1.4)
        Nl = M("N = 90", size=32, color=C_GREEN).to_corner(UR, buff=0.5).shift(DOWN * 0.6)
        self.then(Write(Nl), rt=0.6)
        hub = 45
        nb = list(G.neighbors(hub))
        dl = M(r"\deg \le d = 4", size=32, color=C_YELLOW).next_to(Nl, DOWN, buff=0.2)
        self.go("at most d synaptic", nodes[hub].animate.set_color(C_YELLOW).scale(1.8), Write(dl), rt=0.8)
        self.go("immediate neighbors", *[edges[tuple(sorted((hub, j)))].animate.set_stroke(C_YELLOW, 3.5, 1) if tuple(sorted((hub, j))) in edges else
                                         edges[(j, hub)].animate.set_stroke(C_YELLOW, 3.5, 1) for j in nb],
                *[nodes[j].animate.set_color(C_YELLOW) for j in nb], rt=1.0, upto="From extremal")

        # ── Moore bound: BFS balls grow by at most ×(d−1) per hop ────────────────────
        layers = nx.single_source_shortest_path_length(G, hub)
        maxh = max(layers.values())
        hopc = [C_YELLOW, C_ORANGE, C_PINK, C_PURPLE, C_BLUE, C_TEAL, C_GREEN, C_ICE] + [C_GREY] * 30
        moore = M(r"\mathrm{diam}(G)", r"\;\ge\;", r"\Omega\!\left(", r"\frac{\log N}{\log d}", r"\right)", size=42).to_edge(DOWN, buff=0.35)
        self.go("From extremal", nodes.animate.set_opacity(0.5), rt=0.6)
        self.go("Moore Bound", Write(moore[0]), rt=0.8)
        counts = VGroup()
        for h in range(1, maxh + 1):
            ring = [v for v, k in layers.items() if k == h]
            if not ring:
                continue
            anim = [nodes[v].animate.set_color(hopc[h]).set_opacity(1) for v in ring]
            cnt = T(f"hop {h}: {len(ring)}   (≤ {4 * 3 ** (h - 1)})", size=16, color=hopc[h])
            counts.add(cnt)
            cnt.next_to(dl, DOWN, buff=0.15 + 0.3 * (len(counts) - 1)).align_to(dl, RIGHT)
            if h == 3:
                self.go("diameter of any graph", rt=0.1)
            self.play(*anim, FadeIn(cnt, shift=LEFT * 0.1), run_time=0.35)
            if h >= 9:
                break
        self.go("bounded below", Write(moore[1:3]), Write(moore[4]), rt=1.0)
        self.go("log N divided", Write(moore[3]), rt=1.2, upto="What does this lower")

        # ── A → B: a pulse hops, distorts and fades ───────────────────────────────────
        src = min(range(len(P)), key=lambda v: P[v][0])
        from_src = nx.single_source_shortest_path_length(G, src)
        far = max(from_src, key=lambda v: (from_src[v], P[v][0]))
        path = nx.shortest_path(G, src, far)
        self.go("What does this lower", FadeOut(counts), nodes.animate.set_color(C_GREEN).set_opacity(0.6), evg.animate.set_stroke(C_GREEN, 1.6, 0.4), rt=1.0)
        A = VGroup(Circle(0.22, color=C_BLUE, stroke_width=3).move_to(P[src]), T("A", size=20, color=C_BLUE).next_to(P[src], LEFT, buff=0.3))
        B = VGroup(Circle(0.22, color=C_PINK, stroke_width=3).move_to(P[far]), T("B", size=20, color=C_PINK).next_to(P[far], RIGHT, buff=0.3))
        self.go("If token A", Create(A), rt=0.6)
        self.go("opposite side", Create(B), rt=0.6)
        straight = DashedLine(P[src], P[far], color=C_GREY)
        self.go("cannot travel", Create(straight), rt=0.6)
        self.then(straight.animate.set_color(C_RED).set_opacity(0.2), rt=0.5)
        # signal-quality panel (top-right): a waveform that degrades at every hop
        panel = RoundedRectangle(width=3.6, height=2.0, corner_radius=0.12, stroke_color=C_DIM).set_fill(BG, 0.92).to_corner(UR, buff=0.4).shift(DOWN * 0.9)
        amp, dist = ValueTracker(1.0), ValueTracker(0.0)
        xs = np.linspace(-1.5, 1.5, 120)

        def wave():
            a, d = amp.get_value(), dist.get_value()
            ys = a * np.exp(-xs ** 2 * 3) * np.cos(xs * 9)
            ys = np.tanh(ys * (1 + 3 * d)) / (1 + 2 * d) * a + d * 0.12 * np.sin(xs * 37)
            return VMobject(stroke_color=C_YELLOW, stroke_width=2.5).set_points_smoothly([panel.get_center() + np.array([x, 0.65 * y, 0]) for x, y in zip(xs, ys)])
        wv = always_redraw(wave)
        hops = ValueTracker(0)
        hopl = always_redraw(lambda: VGroup(T("hops", size=16, color=C_GREY), Integer(int(hops.get_value()), font_size=30, color=C_YELLOW)).arrange(RIGHT, buff=0.15).next_to(panel, DOWN, buff=0.15))
        self.go("multi-hop relay", FadeOut(VGroup(Nl, dl)), FadeIn(panel), rt=0.4)
        self.add(wv, hopl)
        pulse = Dot(P[src], radius=0.1, color=C_YELLOW)
        self.add(pulse)
        hop_t = max(0.3, (self.t("If an architecture") - self.now - 0.5) / max(1, len(path) - 1))
        keys_at = {1: "Each intermediate hop", 3: "nonlinear distortion", 5: "attenuates gradient"}
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            e = edges.get((a, b)) or edges.get((b, a))
            self.play(pulse.animate.move_to(P[b]), e.animate.set_stroke(C_YELLOW, 3.5, 1), nodes[b].animate.set_color(C_YELLOW).set_opacity(1),
                      hops.animate.set_value(i + 1), amp.animate.set_value(0.82 ** (i + 1)), dist.animate.set_value(min(1, 0.12 * (i + 1))),
                      run_time=min(hop_t, 1.0), rate_func=smooth)
        self.go("If an architecture", Flash(B[0], color=C_PINK), rt=0.6)

        # ── numbers: N = 10^6, d = 16 → ≥ 5 hops ; gradients ∏‖J‖ ──────────────────
        self.go(None, FadeOut(VGroup(nodes, evg, A, B, straight, pulse, panel)), moore.animate.move_to(UP * 2.0 + LEFT * 2.8), rt=0.8)
        self.remove(wv, hopl)
        plug = M(r"\frac{\log 10^{6}}{\log 16}", "=", r"\frac{13.8}{2.77}", r"\approx 4.98", size=40).next_to(moore, DOWN, buff=0.5)
        self.go("degree sixteen", Write(plug[0]), rt=1.0)
        self.go("five to six", Write(plug[1:]), rt=1.4)
        lax = Axes(x_range=[1, 9, 2], y_range=[0, 8, 2], x_length=4.6, y_length=2.6, axis_config=dict(color=C_GREY, include_tip=False, font_size=16),
                   x_axis_config=dict(include_numbers=True), y_axis_config=dict(include_numbers=True)).move_to(RIGHT * 3.6 + UP * 1.4)
        ll = VGroup(M(r"\log_{10} N", size=22, color=C_GREY).next_to(lax.x_axis, DOWN, buff=0.35), T("min hops", size=16, color=C_GREY).next_to(lax.y_axis, UP, buff=0.1))
        curve = lax.plot(lambda x: x * np.log(10) / np.log(16), x_range=[1, 9], color=C_GREEN)
        dot = Dot(lax.c2p(6, 6 * np.log(10) / np.log(16)), color=C_YELLOW)
        self.then(Create(lax), FadeIn(ll), Create(curve), FadeIn(dot, scale=2), rt=1.4, upto="In recurrent execution")
        gax = Axes(x_range=[0, 12, 3], y_range=[-6, 3, 3], x_length=4.6, y_length=2.6, axis_config=dict(color=C_GREY, include_tip=False, font_size=16),
                   x_axis_config=dict(include_numbers=True)).move_to(RIGHT * 3.6 + DOWN * 1.9)
        gl = VGroup(T("hops k", size=16, color=C_GREY).next_to(gax.x_axis, DOWN, buff=0.35),
                    M(r"\log_{10}\prod_{i=1}^{k}\|J_i\|", size=22, color=C_GREY).next_to(gax, LEFT, buff=0.1))
        geq = M(r"\Big\|\frac{\partial \mathcal{L}}{\partial h_0}\Big\| \le \prod_{i=1}^{k}\|J_i\|\,\Big\|\frac{\partial\mathcal{L}}{\partial h_k}\Big\|", size=34).next_to(plug, DOWN, buff=0.5)
        self.go("In recurrent execution", Write(geq), Create(gax), FadeIn(gl), rt=1.6)
        van = gax.plot(lambda k: k * np.log10(0.5), x_range=[0, 12], color=C_BLUE)
        exp_ = gax.plot(lambda k: min(3, k * np.log10(1.8)), x_range=[0, 12], color=C_RED)
        self.go("decay exponentially", Create(van), FadeIn(T("‖J‖=0.5 vanishes", size=16, color=C_BLUE).next_to(gax.c2p(12, -3.6), RIGHT, buff=0.05)), rt=1.4)
        self.go("spectral norms", Indicate(geq), rt=0.8)
        self.go("vanishing or exploding", Create(exp_), FadeIn(T("‖J‖=1.8 explodes", size=16, color=C_RED).next_to(gax.c2p(12, 3), RIGHT, buff=0.05)), rt=1.2,
                upto="In stark contrast")

        # ── the Transformer: one hop, everybody, at once ───────────────────────────────
        self.go("In stark contrast", FadeOut(self.stage(tag, head)), rt=0.8)
        n = 10
        top = VGroup(*[Dot(radius=0.1, color=C_BLUE) for _ in range(n)]).arrange(RIGHT, buff=0.75).move_to(UP * 1.4)
        bot = VGroup(*[Dot(radius=0.1, color=C_BLUE) for _ in range(n)]).arrange(RIGHT, buff=0.75).move_to(DOWN * 1.4)
        bip = VGroup(*[Line(b.get_center(), t.get_center(), stroke_width=1, color=C_BLUE, stroke_opacity=0.35) for b in bot for t in top])
        self.go("geometric topology", FadeIn(bot, lag_ratio=0.05), FadeIn(top, lag_ratio=0.05), rt=0.9)
        self.go("multi-head attention layer", Create(bip, lag_ratio=0.003), rt=1.2)
        tA = VGroup(Circle(0.22, color=C_BLUE, stroke_width=3).move_to(bot[0]), T("A", size=20, color=C_BLUE).next_to(bot[0], DOWN))
        tB = VGroup(Circle(0.22, color=C_PINK, stroke_width=3).move_to(top[-1]), T("B", size=20, color=C_PINK).next_to(top[-1], UP))
        ab = Line(bot[0].get_center(), top[-1].get_center(), color=C_YELLOW, stroke_width=5)
        self.go("dynamic bipartite", Create(tA), Create(tB), rt=0.8)
        d1 = M(r"\mathrm{diam} = 1", size=44, color=C_YELLOW).to_edge(DOWN, buff=0.5)
        self.go("diameter of exactly one", Create(ab), Write(d1), rt=1.0)
        self.go("Every single token", LaggedStart(*[ShowPassingFlash(l.copy().set_stroke(C_YELLOW, 3), time_width=0.6) for l in bip], lag_ratio=0.0), rt=1.2)
        step = VGroup(T("steps", size=18, color=C_GREY), Integer(1, font_size=36, color=C_YELLOW)).arrange(RIGHT).to_corner(UR, buff=0.6).shift(DOWN * 0.6)
        self.go("single, parallelized", FadeIn(step), AnimationGroup(*[ShowPassingFlash(l.copy().set_stroke(WHITE, 3), time_width=1) for l in bip]), rt=1.0)
        o1 = M(r"O(1)\ \text{depth}", size=36, color=C_YELLOW).next_to(d1, RIGHT, buff=0.6)
        self.go("depth", Write(o1), rt=0.8)

        # ── scale N: sparse hops climb, attention stays at one; sparse tries more wires ─
        self.go("Sparse self-organizing", VGroup(top, bot, bip, tA, tB, ab, d1, o1, step).animate.scale(0.5).move_to(RIGHT * 3.6 + UP * 0.3), rt=1.0)
        cmp = Axes(x_range=[2, 12, 2], y_range=[0, 10, 2], x_length=5.2, y_length=3.2, axis_config=dict(color=C_GREY, include_tip=False, font_size=16),
                   x_axis_config=dict(include_numbers=True), y_axis_config=dict(include_numbers=True)).move_to(LEFT * 3.4 + UP * 0.2)
        cl = VGroup(M(r"\log_{10} N", size=22, color=C_GREY).next_to(cmp.x_axis, DOWN, buff=0.35), T("sequential steps", size=16, color=C_GREY).next_to(cmp, UP, buff=0.1))
        tN = ValueTracker(2)
        sp = always_redraw(lambda: cmp.plot(lambda x: x * np.log(10) / np.log(16), x_range=[2, max(2.01, tN.get_value())], color=C_GREEN))
        at = always_redraw(lambda: cmp.plot(lambda x: 1, x_range=[2, max(2.01, tN.get_value())], color=C_YELLOW))
        self.then(Create(cmp), FadeIn(cl), rt=0.6)
        self.add(sp, at)
        self.then(tN.animate(rate_func=linear).set_value(12), rt=1.8, upto="insurmountable")
        boom = VGroup(T("sparse graph adds shortcut edges to cut diameter →", size=18, color=C_RED),
                      M(r"|E| \to O(N^2)", size=34, color=C_RED)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        ecount = counter(4 * 90, size=34, color=C_RED).next_to(boom, UP, buff=0.2)
        self.go("insurmountable", FadeIn(boom[0]), FadeIn(ecount), rt=0.4)
        self.then(ecount.tracker.animate(rate_func=rate_functions.ease_in_expo).set_value(4_005_000_000), Write(boom[1]), rt=1.6, upto="global context")
        self.go("global context", Indicate(VGroup(top, bot, bip), color=C_YELLOW), rt=1.2)
        self.finish()
