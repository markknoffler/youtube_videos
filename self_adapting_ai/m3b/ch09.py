"""Chapter 09 — What frontier labs discovered: structured routing on dense tensors (MoE + MLA)."""
from common import *


class Ch09(Chapter):
    CH = 9

    def construct(self):
        C = self.times(
            "Recognizing these", "frontier industrial", "brilliant architectural", "Consider the breakthrough", "late 2024",
            "did not abandon", "unstructured biological", "Instead, they engineered", "dense tensor matrices", "two revolutionary",
            "First, through fine-grained", "distinct feed", "For any given token", "only eight experts", "keeping two shared",
            "extreme conditional", "sparse execution", "ninety-percent hardware", "all-to-all communication", "Second, through",
            "Instead of incurring", "raw key-value caches", "dynamically compresses", "low-dimensional latent", "decompressing",
            "Notice how this", "do not come from abolishing", "They come from designing", "on top of dense", "You gain the efficiency",
            "catastrophic cache penalty", "By combining", "sparse parameter activation", "zero loss", "Rather than letting",
            "learned soft routing", "statically defined", "Modularity is alive", "unruly biological", "disciplined mathematical")
        frame = self.camera.frame
        tag = T("09 · WHAT FRONTIER LABS DISCOVERED", size=16, color=C_GREY).to_corner(UL, buff=0.35)
        self.add(tag)

        # ── evidence wall: real papers connected by the mechanisms they share ─────────
        ds = framed_image(os.path.join(ASSETS, "shots", "arxiv_deepseek_v3.png"), height=2.2)
        pages = Group(PaperPage("attention", 0, height=2.6), PaperPage("induction", 0, height=2.6), PaperPage("oswald", 0, height=2.6),
                      PaperPage("deepseek2", 0, height=2.6))
        caps = ["Vaswani 2017 · attention", "Olsson 2022 · induction heads", "von Oswald 2023 · ICL ≈ GD", "DeepSeek-V2 2024 · MLA"]
        pos = [LEFT * 5.0 + UP * 1.3, LEFT * 1.7 + UP * 1.3, RIGHT * 1.6 + UP * 1.3, RIGHT * 4.9 + UP * 1.3]
        wall = Group()
        for p, c, xy in zip(pages, caps, pos):
            p.move_to(xy)
            wall.add(Group(p, T(c, size=14, color=C_GREY).next_to(p, DOWN, buff=0.1)))
        ds.move_to(DOWN * 2.0)
        links = VGroup(*[Line(w[0].get_bottom(), ds.get_top(), color=C_BLUE, stroke_width=1.5, stroke_opacity=0.6) for w in wall])
        self.go("Recognizing these", LaggedStart(*[FadeIn(w, shift=DOWN * 0.3) for w in wall], lag_ratio=0.2), rt=2.0)
        self.go("frontier industrial", FadeIn(ds, shift=UP * 0.3), rt=0.8)
        self.go("brilliant architectural", Create(links, lag_ratio=0.2), *[ShowPassingFlash(l.copy().set_stroke(C_YELLOW, 4)) for l in links], rt=1.4)

        # ── DeepSeek-V3: the technical report, the exact numbers ──────────────────────
        rep = PaperPage("deepseek", 0, height=7.0).move_to(RIGHT * 0.0 + DOWN * 0.3)
        h671 = rep.hl("language model with 671B total")
        h37 = rep.hl("parameters with 37B activated for each token")
        self.go("Consider the breakthrough", FadeOut(Group(wall, links)), FadeOut(ds, shift=UP), FadeIn(rep, shift=UP), rt=1.2)
        self.go("late 2024", frame.animate.scale(0.45).move_to(h671.get_center() + DOWN * 0.15), rt=1.2)
        self.then(FadeIn(h671), rt=0.5)
        self.then(FadeIn(h37), rt=0.5, upto="did not abandon")
        self.go("did not abandon", frame.animate.scale(1 / 0.45).move_to(ORIGIN), FadeOut(Group(rep, h671, h37)), rt=1.2)
        mono = monolith(6, w=2.6, h=0.42, color=C_BLUE).move_to(RIGHT * 2.6)
        bio = living_graph(20, center=LEFT * 3.4, radius=1.4, seed=5)
        self.then(FadeIn(mono, shift=UP * 0.2), rt=0.6)
        self.add(bio[0])
        self.go("unstructured biological", FadeIn(bio.nodes), rt=0.6)
        xx = cross(s=0.6).move_to(LEFT * 3.4)
        self.then(Create(xx), bio.nodes.amp.animate.set_value(0.05), rt=0.8, upto="Instead, they engineered")
        self.go("Instead, they engineered", FadeOut(VGroup(bio.nodes, xx)), mono.animate.move_to(ORIGIN).scale(1.2), rt=1.0)
        self.remove(bio[0])
        # the MLP layer opens into a bank of experts
        mlp = mono[3]
        self.go("dense tensor matrices", mlp.animate.set_color(C_YELLOW).scale(1.1), Indicate(mlp, color=C_YELLOW), rt=1.2, upto="two revolutionary")
        inn = VGroup(label_box("① fine-grained Mixture of Experts", C_YELLOW, size=20), label_box("② Multi-head Latent Attention", C_TEAL, size=20)).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5)
        self.go("two revolutionary", LaggedStart(*[FadeIn(i, shift=LEFT * 0.2) for i in inn], lag_ratio=0.4), rt=1.4)

        # ── MoE: 256 experts, a gate picks 8 per token ─────────────────────────────────
        grid = VGroup(*[RoundedRectangle(width=0.27, height=0.27, corner_radius=0.04, stroke_color=C_GREY, stroke_width=1).set_fill(C_GREY, 0.3)
                        for _ in range(256)]).arrange_in_grid(16, 16, buff=0.05).move_to(RIGHT * 2.6 + DOWN * 0.2)
        shared = RoundedRectangle(width=0.9, height=4.9, corner_radius=0.08, color=C_ORANGE, stroke_width=2).set_fill(C_ORANGE, 0.25).next_to(grid, RIGHT, buff=0.3)
        shared_l = T("shared\nexpert", size=14, color=C_ORANGE).move_to(shared)
        gl = T("256 routed experts", size=18, color=C_YELLOW).next_to(grid, UP, buff=0.15)
        self.go("First, through fine-grained", FadeOut(inn[1]), inn[0].animate.scale(0.8).to_corner(UL, buff=0.4).shift(DOWN * 0.45),
                ReplacementTransform(mono, VGroup(*[grid[i] for i in range(0, 256, 32)])), rt=1.2)
        self.go("distinct feed", LaggedStart(*[FadeIn(g, scale=0.5) for g in grid], lag_ratio=0.002), FadeIn(gl), rt=1.6)
        # gate bars on the left
        gate_ax = Line(LEFT * 6.2, LEFT * 1.6, color=C_GREY).move_to(LEFT * 3.9 + DOWN * 2.6)
        gate_l = M(r"s_{t,i}=\sigma(u_t^{\top} e_i)", size=28, color=C_YELLOW).move_to(LEFT * 3.9 + UP * 0.3)
        topk = M(r"g_{t,i}= s_{t,i}\ \text{if}\ i\in\mathrm{TopK}_8(s_t)", size=26, color=C_YELLOW).next_to(gate_l, DOWN, buff=0.2)
        rng = np.random.default_rng(3)
        toks = ["The", "proof", "of", "Fermat"]
        routes = VGroup()
        self.go("For any given token", FadeIn(shared), FadeIn(shared_l), Write(gate_l), Create(gate_ax), rt=1.0)
        keys = ["only eight experts", "keeping two shared", "extreme conditional", "sparse execution"]
        for k, w in enumerate(toks):
            tb = label_box(w, C_BLUE, size=22).move_to(LEFT * 3.9 + UP * 2.0)
            s = rng.random(256) ** 3
            top = np.argsort(-s)[:8]
            bars = VGroup(*[Rectangle(width=0.016, height=1.6 * v + 0.005).set_stroke(width=0).set_fill(C_YELLOW if i in top else C_GREY, 0.9)
                            .move_to(gate_ax.get_left() + RIGHT * (0.01 + i * 0.0176), aligned_edge=DOWN) for i, v in enumerate(s)])
            lines = VGroup(*[Line(tb.get_right(), grid[i].get_center(), color=C_YELLOW, stroke_width=1.6, stroke_opacity=0.8) for i in top])
            lines.add(Line(tb.get_right(), shared.get_left(), color=C_ORANGE, stroke_width=2.5))
            self.go(keys[k], FadeIn(tb, shift=DOWN * 0.2), FadeIn(bars, lag_ratio=0.002), *([Write(topk)] if k == 0 else []), rt=0.6)
            self.then(Create(lines, lag_ratio=0.05), *[grid[i].animate.set_fill(C_YELLOW, 0.95) for i in top], shared.animate.set_fill(C_ORANGE, 0.6), rt=0.7)
            self.then(FadeOut(lines), FadeOut(bars), FadeOut(tb), *[grid[i].animate.set_fill(C_YELLOW, 0.35) for i in top], rt=0.4)
        act = T("8 of 256 active per token  ·  37B of 671B parameters", size=18, color=C_YELLOW).next_to(grid, DOWN, buff=0.2)
        self.then(FadeIn(act), rt=0.5)
        # experts sharded over GPUs, tokens dispatched all-to-all
        self.go("ninety-percent hardware", FadeOut(VGroup(gate_l, topk, gate_ax)), rt=0.5)
        gpus = VGroup(*[RoundedRectangle(width=1.6, height=1.0, corner_radius=0.1, color=C_ORANGE, stroke_width=2).set_fill(C_ORANGE, 0.1) for _ in range(4)])
        gpus.arrange_in_grid(2, 2, buff=0.6).move_to(LEFT * 3.9 + UP * 0.3)
        gl2 = VGroup(*[T(f"GPU {i}\n64 experts", size=13, color=C_ORANGE).move_to(g) for i, g in enumerate(gpus)])
        self.then(FadeIn(gpus, lag_ratio=0.1), FadeIn(gl2), rt=0.8)
        a2a = VGroup(*[Line(a.get_center(), b.get_center(), color=C_YELLOW, stroke_width=2) for a in gpus for b in gpus if a is not b])
        self.go("all-to-all communication", LaggedStart(*[ShowPassingFlash(l, time_width=0.6) for l in a2a], lag_ratio=0.05), rt=1.6)
        self.then(LaggedStart(*[ShowPassingFlash(l.copy(), time_width=0.6) for l in a2a], lag_ratio=0.05), rt=1.2, upto="Second, through")

        # ── MLA: the KV cache grows, then compresses into a latent ─────────────────────
        self.go("Second, through", FadeOut(VGroup(grid, shared, shared_l, gl, act, gpus, gl2, inn[0])), rt=0.8)
        title = label_box("② Multi-head Latent Attention (MLA)", C_TEAL, size=20).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        self.then(FadeIn(title), rt=0.4)
        n = 12
        kcols = VGroup(*[VGroup(heatmap(rng.random((8, 1)), cell=0.17, cmap=(BLACK, K_COL, WHITE)), heatmap(rng.random((8, 1)), cell=0.17, cmap=(BLACK, V_COL, WHITE))).arrange(RIGHT, buff=0.02)
                         for _ in range(n)]).arrange(RIGHT, buff=0.12).move_to(LEFT * 2.6 + UP * 1.0)
        cache_l = T("KV cache: 2 × d_h × heads per token", size=16, color=C_GREY).next_to(kcols, UP, buff=0.2)
        mem = ValueTracker(0)
        mbar_bg = Rectangle(width=6, height=0.35, color=C_DIM).set_fill(C_DIM, 0.3).move_to(LEFT * 2.6 + DOWN * 2.6)
        mbar = always_redraw(lambda: Rectangle(width=max(0.01, 6 * mem.get_value()), height=0.35).set_stroke(width=0)
                             .set_fill(interpolate_color(ManimColor(C_GREEN), ManimColor(C_RED), mem.get_value()), 0.9).move_to(mbar_bg.get_left(), aligned_edge=LEFT))
        mbl = T("memory per sequence", size=14, color=C_GREY).next_to(mbar_bg, UP, buff=0.1).align_to(mbar_bg, LEFT)
        self.go("Instead of incurring", FadeIn(cache_l), FadeIn(mbar_bg), FadeIn(mbl), rt=0.5)
        self.add(mbar)
        self.go("raw key-value caches", LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in kcols], lag_ratio=0.12), mem.animate.set_value(0.95), rt=2.0)
        # down-projection to a latent c_t
        lat = VGroup(*[heatmap(rng.random((2, 1)), cell=0.17, cmap=(BLACK, C_TEAL, WHITE)) for _ in range(n)])
        for l_, c in zip(lat, kcols):
            l_.move_to(c.get_center() + DOWN * 1.6)
        eqd = M(r"c_t = W^{DKV} h_t", size=32, color=C_TEAL).move_to(RIGHT * 3.6 + UP * 0.8)
        self.go("dynamically compresses", Write(eqd), *[ReplacementTransform(c.copy(), l_) for c, l_ in zip(kcols, lat)], rt=1.6)
        self.go("low-dimensional latent", FadeOut(kcols), mem.animate.set_value(0.07), FadeOut(cache_l),
                FadeIn(T("latent cache c_t", size=16, color=C_TEAL).next_to(lat, UP, buff=0.15)), rt=1.4)
        equ = M(r"k_t = W^{UK} c_t,\quad v_t = W^{UV} c_t", size=30, color=C_TEAL).next_to(eqd, DOWN, buff=0.3)
        rec = VGroup(heatmap(rng.random((8, 1)), cell=0.17, cmap=(BLACK, K_COL, WHITE)), heatmap(rng.random((8, 1)), cell=0.17, cmap=(BLACK, V_COL, WHITE))).arrange(RIGHT, buff=0.02)
        rec.move_to(RIGHT * 3.6 + DOWN * 1.4)
        self.go("decompressing", Write(equ), TransformFromCopy(lat[-1], rec), rt=1.4, upto="Notice how this")

        # ── resolution: modularity on top of dense matmul ─────────────────────────────
        self.go("Notice how this", FadeOut(self.stage(tag)), rt=0.8)
        self.remove(mbar)
        mono2 = monolith(6, w=2.4, h=0.4, color=C_BLUE).move_to(LEFT * 3.6)
        self.then(FadeIn(mono2), rt=0.5)
        self.go("do not come from abolishing", Indicate(mono2, color=C_ICE), rt=1.0)
        experts = VGroup(*[heatmap(rng.random((5, 5)), cell=0.18, cmap=(BLACK, C_YELLOW, WHITE)) for _ in range(6)]).arrange_in_grid(2, 3, buff=0.35).move_to(RIGHT * 2.6 + UP * 0.6)
        exl = T("each expert = a dense matrix (systolic-friendly)", size=16, color=C_YELLOW).next_to(experts, UP, buff=0.2)
        self.go("They come from designing", TransformFromCopy(mono2[3], experts), FadeIn(exl), rt=1.4)
        wfs = []
        for e in experts:
            tr = ValueTracker(-3)
            e.rows, e.cols = 5, 5
            wavefront(e, tr, color=C_YELLOW, width=1.5)
            wfs.append(tr)
        self.go("on top of dense", *[t_.animate(rate_func=linear).set_value(10) for t_ in wfs], rt=1.8)
        # contiguous expert gather vs pointer chasing
        cmp_l = VGroup(T("MoE dispatch: contiguous blocks", size=16, color=C_YELLOW), T("graph rewiring: pointer chasing", size=16, color=C_RED)).arrange(DOWN, aligned_edge=LEFT, buff=1.0).move_to(RIGHT * 2.6 + DOWN * 1.9)
        blk = VGroup(*[Rectangle(width=0.5, height=0.25).set_stroke(C_YELLOW, 1).set_fill(C_YELLOW, 0.5) for _ in range(8)]).arrange(RIGHT, buff=0.03).next_to(cmp_l[0], DOWN, buff=0.1).align_to(cmp_l[0], LEFT)
        ptr = VGroup(*[CurvedArrow(LEFT * 0.0, RIGHT * 0.6, angle=1.2, color=C_RED, stroke_width=2, tip_length=0.08) for _ in range(6)]).arrange(RIGHT, buff=0.05).next_to(cmp_l[1], DOWN, buff=0.1).align_to(cmp_l[1], LEFT)
        self.go("You gain the efficiency", FadeIn(cmp_l[0]), FadeIn(blk, lag_ratio=0.1), *[t_.animate(rate_func=linear).set_value(-3) for t_ in wfs], rt=1.4)
        self.go("catastrophic cache penalty", FadeIn(cmp_l[1]), LaggedStart(*[Create(p) for p in ptr], lag_ratio=0.2), rt=1.4, upto="By combining")
        for e in experts:
            e.clear_updaters()
        self.then(*[sq.animate.set_fill(C_YELLOW, 0.3 + 0.6 * rng.random()) for e in experts for sq in e], rt=0.5, upto="By combining")
        # combined system stats: sparse activation, smooth training
        self.go("By combining", FadeOut(VGroup(cmp_l, blk, ptr, exl)), experts.animate.scale(0.7).move_to(RIGHT * 2.6 + UP * 1.9), rt=1.0)
        frac = 37 / 671
        pie_bg = Circle(1.0, color=C_DIM, stroke_width=0).set_fill(C_DIM, 0.6).move_to(RIGHT * 0.9 + DOWN * 1.3)
        pie = AnnularSector(inner_radius=0, outer_radius=1.0, angle=TAU * frac, start_angle=PI / 2, color=C_YELLOW).set_fill(C_YELLOW, 0.9).move_arc_center_to(pie_bg.get_center())
        pl = VGroup(T("37B active", size=16, color=C_YELLOW), T("of 671B", size=14, color=C_GREY)).arrange(DOWN, buff=0.05).next_to(pie_bg, DOWN, buff=0.15)
        self.go("sparse parameter activation", FadeIn(pie_bg), Create(pie), FadeIn(pl), rt=1.2)
        lax = LiveAxes([0, 10, 5], [0, 4, 2], width=3.6, height=2.2, x_label="training tokens →").move_to(RIGHT * 4.4 + DOWN * 1.3)
        lt_ = ValueTracker(0)
        xs = np.linspace(0, 10, 200)
        rngl = np.random.default_rng(1)
        lc = lax.live_curve(xs, 3.6 * np.exp(-0.35 * xs) + 0.6 + 0.03 * rngl.normal(size=200), lt_, color=C_TEAL)
        ll = T("no irrecoverable loss spikes (tech. report)", size=14, color=C_TEAL).next_to(lax, UP, buff=0.05)
        self.go("zero loss", FadeIn(lax), FadeIn(ll), rt=0.5)
        self.add(lc)
        self.then(lt_.animate(rate_func=linear).set_value(10), rt=1.6, upto="Rather than letting")

        # ── learned soft routing over static expert banks; routes keep flowing ────────
        self.remove(lc)
        self.go("Rather than letting", FadeOut(VGroup(pie_bg, pie, pl, lax, ll)), rt=0.6)
        gate = Circle(0.4, color=C_YELLOW, stroke_width=3).set_fill(C_YELLOW, 0.2).move_to(LEFT * 0.4 + DOWN * 0.8)
        gate_l2 = M(r"\mathrm{TopK}\,\sigma(u^{\top}e)", size=24, color=C_YELLOW).next_to(gate, DOWN, buff=0.15)
        self.go("learned soft routing", ReplacementTransform(mono2, gate), FadeIn(gate_l2), rt=1.0)
        banks = experts
        self.go("statically defined", banks.animate.move_to(RIGHT * 3.2 + DOWN * 0.8).scale(1.3), rt=0.8)
        rs = []
        for i, e in enumerate(banks):
            p = VMobject().set_points_smoothly([LEFT * 6.5 + UP * (1.6 - 0.5 * i) + DOWN * 0.8, gate.get_center(), e.get_left()])
            rs.append(Stream(p, n=5, speed=0.35 + 0.06 * i, color=[C_YELLOW, C_TEAL, C_PINK, C_BLUE, C_ORANGE, C_GREEN][i], radius=0.05, square=True))
        self.go("Modularity is alive", *[FadeIn(r) for r in rs], rt=1.0)
        self.go("unruly biological", Indicate(banks, color=WHITE), rt=1.2)
        motto = T("modularity as disciplined routing over dense matrices", size=26, color=C_YELLOW).to_edge(DOWN, buff=0.6)
        self.go("disciplined mathematical", Write(motto), rt=1.4)
        self.finish()
