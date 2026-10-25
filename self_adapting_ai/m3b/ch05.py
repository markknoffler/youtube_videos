"""Chapter 05 — Theorem 1: Rank Collapse & the Oja Trap (live 16-neuron simulations)."""
from common import *

D = 16


def make_data(n=4000, seed=0):
    rng = np.random.default_rng(seed)
    lam = 0.68 ** np.arange(D) * 3.0
    Q, _ = np.linalg.qr(rng.normal(size=(D, D)))
    X = rng.normal(size=(n, D)) * np.sqrt(lam) @ Q.T
    C = np.cov(X.T)
    ev, V = np.linalg.eigh(C)
    return X, C, ev[::-1], V[:, ::-1]


def simulate(X, rule="oja", k=4, eta=0.004, snaps=150, seed=1):
    """Returns per-snapshot weight matrices (neurons × D)."""
    rng = np.random.default_rng(seed)
    W = rng.normal(size=(D, D)) * 0.3
    out = [W.copy()]
    every = len(X) // snaps
    for t, x in enumerate(X):
        y = W @ x
        if rule == "oja":                      # each neuron: independent Oja → all → ±v1
            W += eta * (np.outer(y, x) - (y ** 2)[:, None] * W)
        else:                                  # Sanger GHA on the first k neurons
            Wk = W[:k]; yk = y[:k]
            W[:k] += eta * (np.outer(yk, x) - np.tril(np.outer(yk, yk)) @ Wk)
            W[k:] *= 0.995
        if (t + 1) % every == 0:
            out.append(W.copy())
    return np.array(out)


def eff_rank(W):
    s = np.linalg.svd(W, compute_uv=False)
    p = s / s.sum()
    return float(np.exp(-(p * np.log(p + 1e-12)).sum())), s


class Ch05(Chapter):
    CH = 5

    def construct(self):
        C_ = self.times(
            "Our first theoretical", "Rank Collapse in Homogeneous", "Let us mathematically", "Consider a layer",
            "synaptic weight matrix W", "The continuous-time update", "dW over dt", "eta times the expectation", "minus alpha",
            "When we analyze", "stationary input", "fatal spectral", "By Lyapunov", "dominant eigenvector", "covariance matrix C",
            "In formal terms", "collapses to one", "Every neuron in the layer", "largest principal", "Even when researchers",
            "lateral inhibition", "Sanger's Generalized", "top k orthogonal", "It acts as a linear", "fixed subspace",
            "Now look at what", "dynamic in-context", "In a Transformer", "softmax of Q", "square root of d",
            "dynamic, input-dependent", "full-rank associative", "arbitrary token pairs", "Local Hebbian rewiring",
            "static statistics", "squanders", "dominant eigenvalues", "permanently barring", "context-sensitive")
        frame = self.camera.frame
        tag = T("05 · THEOREM 1 — RANK COLLAPSE", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        X, Cm, ev, V = make_data()
        oja = simulate(X, "oja")
        gha = simulate(X, "gha")

        # ── bridge: theorem card from ch04 becomes the header ─────────────────────────
        card = VGroup(RoundedRectangle(width=4.4, height=2.5, corner_radius=0.15, color=C_YELLOW, stroke_width=2).set_fill(C_YELLOW, 0.08),
                      VGroup(T("Theorem 1", size=30, color=C_YELLOW, weight=BOLD), T("rank collapse", size=20)).arrange(DOWN, buff=0.15))
        self.add(card, tag)
        head = VGroup(T("Theorem 1", size=26, color=C_YELLOW, weight=BOLD), T("Rank collapse in homogeneous local plasticity", size=22)).arrange(RIGHT, buff=0.3)
        head.to_edge(UP, buff=0.75)
        self.go("Our first theoretical", Indicate(card, color=C_YELLOW), rt=1.0)
        self.go("Rank Collapse in Homogeneous", ReplacementTransform(card, head), rt=1.4)

        # ── a layer: x → W → y ──────────────────────────────────────────────────────────
        net = NeuralNet((8, 8), width=3.0, height=4.0, seed=2, edge_op=0.6).move_to(LEFT * 4.6 + DOWN * 0.3)
        xl = M("x", size=32, color=C_BLUE).next_to(net.layers[0], DOWN)
        yl = M("y", size=32, color=C_PINK).next_to(net.layers[1], DOWN)
        self.go("Let us mathematically", FadeIn(net, lag_ratio=0.01), rt=1.2)
        self.go("Consider a layer", FadeIn(xl), FadeIn(yl), net.forward([np.random.rand(8), np.random.rand(8)], color=C_YELLOW), rt=1.4)
        Wh = heatmap(np.abs(oja[0][:8, :8]) / np.abs(oja[0]).max(), cell=0.3, cmap=(BLACK, C_BLUE, C_YELLOW)).move_to(LEFT * 1.6 + DOWN * 0.3)
        Wl = M("W", size=36).next_to(Wh, UP, buff=0.15)
        self.go("synaptic weight matrix W", TransformFromCopy(net.edges, Wh), Write(Wl), rt=1.2)

        # equation built term by term, each term attached to an object
        eq = M(r"\frac{dW}{dt}", "=", r"\eta\,", r"\mathbb{E}[\,y\,x^{\top}]", r"\;-\;", r"\alpha\,", r"y\,y^{\top}W", size=44).move_to(RIGHT * 3.2 + UP * 1.6)
        self.go("The continuous-time update", FadeIn(eq[0]), rt=0.6)
        self.go("dW over dt", Write(eq[1]), Indicate(Wh, color=WHITE), rt=0.8)
        xv = heatmap(np.random.rand(1, 8), cell=0.28, cmap=(BLACK, C_BLUE, WHITE)).move_to(RIGHT * 3.2 + DOWN * 0.2)
        yv = heatmap(np.random.rand(8, 1), cell=0.28, cmap=(BLACK, C_PINK, WHITE)).next_to(xv, LEFT, buff=0.25).shift(DOWN * 1.1)
        outer = heatmap(np.outer(np.random.rand(8), np.random.rand(8)), cell=0.28, cmap=(BLACK, C_YELLOW, WHITE)).next_to(xv, DOWN, buff=0.15)
        self.go("eta times the expectation", Write(eq[2:4]), FadeIn(xv), FadeIn(yv), rt=0.9)
        self.then(TransformFromCopy(VGroup(xv, yv), outer), rt=1.0, upto="minus alpha")
        self.go("minus alpha", Write(eq[4:]), eq[3].animate.set_color(C_YELLOW), outer.animate.scale(0.6).next_to(eq[3], DOWN, buff=0.2), FadeOut(xv), FadeOut(yv), rt=1.2)
        decay = Arrow(Wh.get_right() + RIGHT * 0.1, Wh.get_right() + RIGHT * 0.9, color=C_RED, buff=0).rotate(PI)
        self.then(eq[6].animate.set_color(C_RED), GrowArrow(decay), rt=0.8, upto="When we analyze")

        # ── stationary inputs: a 3-D cloud and its covariance ──────────────────────────
        yaw = ValueTracker(0.2)
        P3 = X[:220] @ V[:, :3]
        cloud = Cloud3D(P3 * 0.42, [C_BLUE] * len(P3), radius=0.03, yaw=yaw)
        cloud.anchor = LEFT * 3.6 + DOWN * 0.4
        cloud.add_updater(lambda m, dt: yaw.increment_value(dt * 0.25))
        self.go("When we analyze", FadeOut(VGroup(net, xl, yl, decay)), Wh.animate.scale(0.7).move_to(RIGHT * 5.6 + DOWN * 2.4),
                Wl.animate.scale(0.7).move_to(RIGHT * 5.6 + DOWN * 1.2), eq.animate.scale(0.75).to_corner(UR, buff=0.5).shift(DOWN * 0.6),
                FadeOut(outer), rt=1.2)
        self.add(cloud)
        self.go("stationary input", FadeIn(cloud), rt=1.0)
        Ch = heatmap(np.abs(Cm[:10, :10]) / np.abs(Cm).max(), cell=0.24, cmap=(BLACK, C_GREEN, WHITE)).move_to(RIGHT * 1.6 + DOWN * 0.6)
        Chl = M(r"C=\mathbb{E}[xx^{\top}]", size=30, color=C_GREEN).next_to(Ch, UP, buff=0.15)
        self.go("fatal spectral", FadeIn(Ch, lag_ratio=0.01), Write(Chl), rt=1.2)

        # eigen-decomposition: eigenvalue bars (one per mode)
        bars_ax = Line(RIGHT * 0.2, RIGHT * 6.4, color=C_GREY).move_to(RIGHT * 3.3 + DOWN * 2.9)
        bw = 0.3

        def spectrum(s, color, scale=1.0):
            g = VGroup()
            s = np.asarray(s)
            for i, v in enumerate(s[:D]):
                h = max(0.01, 2.2 * v / scale)
                g.add(Rectangle(width=bw, height=h).set_stroke(width=0).set_fill(color, 0.9).move_to(bars_ax.get_left() + RIGHT * (0.25 + i * 0.38), aligned_edge=DOWN).shift(UP * 0.0))
            return g
        evb = spectrum(ev, C_GREEN, ev[0])
        evl = M(r"\lambda_1 > \lambda_2 > \dots > \lambda_{16}", size=26, color=C_GREEN).next_to(evb, UP, buff=0.15).align_to(evb, LEFT)
        v1 = Arrow(ORIGIN, RIGHT, color=C_GREEN)

        def v1_arrow():
            a, b = yaw.get_value(), cloud.pitch
            Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
            Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
            q = (Rx @ Ry) @ np.array([2.6, 0, 0])
            return DashedLine(cloud.anchor - q * [1, 1, 0], cloud.anchor + q * [1, 1, 0], color=C_GREEN, stroke_width=3, dashed_ratio=0.5).set_points(DashedVMobject(Line(cloud.anchor - q * [1, 1, 0], cloud.anchor + q * [1, 1, 0]), num_dashes=30).get_all_points()) if False else DashedVMobject(Line(cloud.anchor - q * [1, 1, 0], cloud.anchor + q * [1, 1, 0], color=C_GREEN, stroke_width=3), num_dashes=30)
        v1l = always_redraw(v1_arrow)
        self.go("By Lyapunov", Ch.animate.scale(0.75).next_to(Chl, DOWN, buff=0.1), rt=0.6)
        self.then(LaggedStart(*[GrowFromEdge(b, DOWN) for b in evb], lag_ratio=0.06), FadeIn(evl), Create(bars_ax), rt=1.6, upto="dominant eigenvector")
        self.go("dominant eigenvector", FadeIn(v1l), Indicate(evb[0], color=WHITE, scale_factor=1.3), rt=1.0)
        vlab = M("v_1", size=30, color=C_GREEN).move_to(LEFT * 0.7 + UP * 1.2)
        self.go("covariance matrix C", FadeIn(vlab), Indicate(Chl), rt=1.0, upto="In formal terms")

        # ── live: 16 neurons under Oja's rule — watch the modes disappear ─────────────
        k = ValueTracker(0)
        s0 = np.linalg.svd(oja[0], compute_uv=False)[0]
        neur3 = lambda i: (oja[int(k.get_value())] @ V[:, :3]) * 1.0

        def neurons():
            W3 = neur3(0)
            a, b = yaw.get_value(), cloud.pitch
            Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
            Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
            Q = W3 @ (Rx @ Ry).T
            g = VGroup()
            for i, q in enumerate(Q):
                tip = cloud.anchor + 2.3 * np.array([q[0], q[1], 0])
                g.add(Line(cloud.anchor, tip, color=C_PINK, stroke_width=2.2, stroke_opacity=0.8), Dot(tip, radius=0.05, color=C_PINK))
            return g
        nv = always_redraw(neurons)

        def wspec():
            W = oja[int(k.get_value())]
            s = np.linalg.svd(W, compute_uv=False)
            return spectrum(s, C_PINK, s0 * 1.2)
        ws = always_redraw(wspec)
        rk = always_redraw(lambda: VGroup(T("effective rank", size=18, color=C_GREY),
                                          DecimalNumber(eff_rank(oja[int(k.get_value())])[0], num_decimal_places=2, font_size=40, color=C_PINK)).arrange(DOWN, buff=0.1).move_to(RIGHT * 5.5 + UP * 0.2))
        Wlive = always_redraw(lambda: heatmap(np.abs(oja[int(k.get_value())][:8, :8]) / (np.abs(oja[int(k.get_value())]).max() + 1e-9), cell=0.21,
                                               cmap=(BLACK, C_BLUE, C_YELLOW)).move_to(RIGHT * 5.6 + DOWN * 2.4))
        lim = M(r"\lim_{t\to\infty}\ \mathrm{rank}(W) = 1", size=36, color=C_PINK).move_to(LEFT * 3.6 + UP * 2.4)
        self.go("In formal terms", FadeOut(VGroup(Ch, Chl, evl)), evb.animate.set_opacity(0.25), FadeOut(Wh), rt=0.8)
        self.add(nv, ws, rk, Wlive)
        self.then(k.animate(rate_func=linear).set_value(30), rt=2.0, upto="collapses to one")
        self.go("collapses to one", Write(lim), k.animate(rate_func=linear).set_value(70), rt=2.4)
        self.go("Every neuron in the layer", k.animate(rate_func=linear).set_value(115), rt=2.6)
        self.go("largest principal", k.animate(rate_func=smooth).set_value(150), Indicate(v1l, color=C_GREEN), rt=2.0, upto="Even when researchers")
        self.remove(nv, ws, rk, Wlive)
        frozen = VGroup(neurons(), wspec(), rk.copy(), Wlive.copy())
        self.add(frozen)

        # ── Sanger's GHA: lateral inhibition buys k orthogonal components, no more ─────
        kg = ValueTracker(0)
        sg0 = np.linalg.svd(gha[0], compute_uv=False)[0]

        def gneurons():
            W3 = gha[int(kg.get_value())][:4] @ V[:, :3]
            a, b = yaw.get_value(), cloud.pitch
            Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
            Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
            Q = W3 @ (Rx @ Ry).T
            cols = [C_YELLOW, C_ORANGE, C_TEAL, C_PURPLE]
            return VGroup(*[Arrow(cloud.anchor, cloud.anchor + 2.3 * np.array([q[0], q[1], 0]), buff=0, color=c, stroke_width=5,
                                  max_tip_length_to_length_ratio=0.12) for q, c in zip(Q, cols)])
        gv = always_redraw(gneurons)
        gs = always_redraw(lambda: spectrum(np.linalg.svd(gha[int(kg.get_value())], compute_uv=False), C_YELLOW, sg0 * 1.4))
        inh = VGroup(*[CurvedArrow(LEFT * 6 + UP * (1.8 - 0.5 * i), LEFT * 6 + UP * (1.3 - 0.5 * i), angle=-1.6, color=C_RED, tip_length=0.12) for i in range(3)])
        inh_l = T("anti-Hebbian lateral inhibition", size=18, color=C_RED).next_to(inh, RIGHT, buff=0.15)
        self.go("Even when researchers", FadeOut(frozen), FadeOut(lim), FadeOut(Wl), rt=0.7)
        self.add(gv, gs)
        self.go("lateral inhibition", FadeIn(inh), FadeIn(inh_l), kg.animate(rate_func=linear).set_value(40), rt=1.6)
        gha_eq = M(r"\Delta W = \eta\,\big(yx^{\top} - \mathrm{LT}[yy^{\top}]\,W\big)", size=30, color=C_YELLOW).move_to(LEFT * 3.6 + UP * 2.4)
        self.go("Sanger's Generalized", Write(gha_eq), kg.animate(rate_func=linear).set_value(100), rt=2.2)
        topk = Brace(evb[:4], UP, buff=0.1, color=C_YELLOW)
        topk_l = T("top k = 4, then nothing", size=18, color=C_YELLOW).next_to(topk, UP, buff=0.05)
        self.go("top k orthogonal", kg.animate(rate_func=smooth).set_value(150), GrowFromCenter(topk), FadeIn(topk_l), rt=1.8, upto="It acts as a linear")
        # projection onto a fixed subspace: every data point slides onto the plane of v1, v2
        self.remove(gv, gs)
        gfro = VGroup(gneurons(), spectrum(np.linalg.svd(gha[-1], compute_uv=False), C_YELLOW, sg0 * 1.4))
        self.add(gfro)
        proj = P3.copy(); proj[:, 2] = 0
        pt = ValueTracker(0)
        cloud.add_updater(lambda m, dt: setattr(m, "P", (1 - pt.get_value()) * P3 * 0.42 + pt.get_value() * proj * 0.42))
        Pop = M(r"P = V_k V_k^{\top}", size=34, color=C_YELLOW).next_to(gha_eq, DOWN, buff=0.3)
        self.go("It acts as a linear", Write(Pop), pt.animate.set_value(1.0), rt=2.2)
        self.go("fixed subspace", Indicate(Pop), rt=1.0, upto="Now look at what")

        # ── what intelligence needs: a map that changes with the input ─────────────────
        self.go("Now look at what", FadeOut(VGroup(gha_eq, Pop, inh, inh_l, topk, topk_l, gfro, cloud, v1l, vlab, evb, bars_ax, eq)), rt=1.0)
        self.remove(cloud, v1l)
        words = ["Alice", "met", "Bob", ".", "Bob", "thanked", "her", "and", "Alice"]
        row = token_row(words, color=C_GREY, size=22).move_to(UP * 1.9)
        self.go("dynamic in-context", FadeIn(row, lag_ratio=0.08), rt=1.0)
        rngt = np.random.default_rng(3)
        E = rngt.normal(size=(9, 16))
        E[4] = E[2]; E[8] = E[0]                        # repeated names share embeddings
        WQ, WK = rngt.normal(size=(16, 16)) / 4, rngt.normal(size=(16, 16)) / 4

        def attn(Emb):
            S = (Emb @ WQ) @ (Emb @ WK).T / 4
            S = S - S.max(1, keepdims=True)
            A = np.exp(S); A /= A.sum(1, keepdims=True)
            return A
        A0 = attn(E)
        am = heatmap(A0 / A0.max(), cell=0.36, cmap=(BLACK, C_BLUE, C_YELLOW)).move_to(LEFT * 2.6 + DOWN * 1.0)
        aeq = M(r"A=\mathrm{softmax}\!\Big(", r"\frac{QK^{\top}}{\sqrt{d}}", r"\Big)", size=40).move_to(RIGHT * 3.0 + UP * 0.4)
        self.go("In a Transformer", FadeIn(am, lag_ratio=0.005), rt=0.9)
        self.go("softmax of Q", Write(aeq[:2]), rt=1.2)
        self.go("square root of d", Write(aeq[2:]), rt=0.8)
        # input-dependent: change two tokens, the whole map recomputes with W fixed
        E2 = E.copy(); E2[6] = rngt.normal(size=16); E2[1] = rngt.normal(size=16)
        A1 = attn(E2)
        new = token_row(["him"], color=C_PINK, size=22)[0].move_to(row[6])
        self.go("dynamic, input-dependent", Transform(row[6], new), rt=0.5)
        self.then(*[sq.animate.set_fill(heat_color(v)) for sq, v in zip(am, (A1 / A1.max()).flatten())], rt=1.2)
        sA = np.linalg.svd(E2 @ WQ @ WK.T @ E2.T, compute_uv=False)
        bars_ax2 = Line(RIGHT * 0.6, RIGHT * 6.4, color=C_GREY).move_to(RIGHT * 3.4 + DOWN * 2.8)
        tb = VGroup(*[Rectangle(width=0.4, height=max(0.02, 2.0 * v / sA[0])).set_stroke(width=0).set_fill(C_BLUE, 0.9) for v in sA])
        tb.arrange(RIGHT, buff=0.12, aligned_edge=DOWN).next_to(bars_ax2, UP, buff=0).align_to(bars_ax2, LEFT).shift(RIGHT * 0.2)
        tbl = T("bilinear form QKᵀ: many live modes", size=18, color=C_BLUE).next_to(tb, UP, buff=0.15)
        self.go("full-rank associative", Create(bars_ax2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in tb], lag_ratio=0.08), FadeIn(tbl), rt=1.6)
        pairs = VGroup(*[ArcBetweenPoints(row[a].get_top(), row[b].get_top(), angle=-1.0).set_stroke(C_YELLOW, 3) for a, b in [(8, 0), (4, 2), (6, 0)]])
        self.go("arbitrary token pairs", LaggedStart(*[Create(p) for p in pairs], lag_ratio=0.3), rt=1.4, upto="Local Hebbian rewiring")

        # ── verdict: collapsed spectrum vs. living spectrum ─────────────────────────────
        hs = np.linalg.svd(oja[-1], compute_uv=False)
        hb = VGroup(*[Rectangle(width=0.4, height=max(0.02, 2.0 * v / hs[0])).set_stroke(width=0).set_fill(C_PINK, 0.9) for v in hs[:9]])
        hb.arrange(RIGHT, buff=0.12, aligned_edge=DOWN).move_to(LEFT * 3.4 + DOWN * 1.8)
        hax = Line(LEFT * 0.0, RIGHT * 5.8, color=C_GREY).next_to(hb, DOWN, buff=0).align_to(hb, LEFT).shift(LEFT * 0.2)
        hbl = T("local Hebbian W: one mode left", size=18, color=C_PINK).next_to(hb, UP, buff=0.15)
        self.go("Local Hebbian rewiring", FadeOut(am), FadeOut(pairs), FadeOut(aeq), rt=0.6)
        self.then(Create(hax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb], lag_ratio=0.08), FadeIn(hbl), rt=1.2, upto="static statistics")
        self.go("static statistics", Indicate(hb[0], color=WHITE), rt=1.0)
        r1 = VGroup(T("rank", size=18, color=C_GREY), DecimalNumber(eff_rank(oja[-1])[0], num_decimal_places=2, font_size=40, color=C_PINK)).arrange(DOWN).next_to(hbl, UP, buff=0.3)
        r2 = VGroup(T("rank", size=18, color=C_GREY), DecimalNumber(eff_rank(E2 @ WQ @ WK.T @ E2.T)[0], num_decimal_places=2, font_size=40, color=C_BLUE)).arrange(DOWN).next_to(tbl, UP, buff=0.3)
        self.go("squanders", FadeIn(r1), FadeIn(r2), rt=0.8)
        self.go("dominant eigenvalues", hb[1:].animate.set_opacity(0.1), rt=1.0)
        lockx = cross(s=0.4).next_to(hbl, RIGHT, buff=0.3) if False else VGroup(Line(UL * 0.3, DR * 0.3, color=C_RED, stroke_width=6), Line(UR * 0.3, DL * 0.3, color=C_RED, stroke_width=6)).next_to(row, DOWN, buff=0.3).shift(LEFT * 3)
        self.go("permanently barring", Create(lockx), row.animate.set_opacity(0.5), rt=1.0)
        self.go("context-sensitive", Indicate(tb, color=C_BLUE), rt=1.0)
        self.finish()
