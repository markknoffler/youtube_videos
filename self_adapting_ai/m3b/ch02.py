"""Chapter 02 — The Biological Dream: Brains vs Static Silos."""
from common import *


def dendrite_tree(root, depth=5, angle=PI / 2, length=0.9, rng=None, color=C_GREEN):
    """Recursive branching arbor; returned in growth order so Create(lag) grows it outward."""
    rng = rng or np.random.default_rng(0)
    out = []

    def rec(p, a, L, d):
        if d == 0:
            return
        q = p + L * np.array([np.cos(a), np.sin(a), 0])
        out.append((d, Line(p, q, stroke_width=0.8 + 0.7 * d, color=color)))
        for s in (-1, 1):
            rec(q, a + s * (0.35 + 0.25 * rng.random()), L * (0.62 + 0.12 * rng.random()), d - 1)
    rec(root, angle, length, depth)
    out.sort(key=lambda t: -t[0])
    return VGroup(*[l for _, l in out])


class Ch02(Chapter):
    CH = 2

    def construct(self):
        C = self.times(
            "To understand", "biological brain", "twenty watts", "refrigerator light", "Yet within", "eighty-six billion",
            "one hundred trillion", "breathtaking", "Crucially", "perpetual topological", "neurogenesis", "dendritic arborization",
            "spine pruning", "real time based", "Under the governing", "fire in temporal synchrony", "physically thickens",
            "AMPA and NMDA", "reinforce", "Conversely", "microglia", "conserve precious", "does not separate", "Every single percept",
            "every sentence", "every thought", "physically alters", "event-driven and asynchronous", "sparse millisecond",
            "one to ten hertz", "continuous synchronization", "Now compare", "frontier GPU cluster", "liquid cooling",
            "Inside, millions", "systolic arrays", "Why couldn't", "Why did computer science", "frozen tensors")
        frame = self.camera.frame
        tag = T("02 · THE BIOLOGICAL DREAM", size=16, color=C_GREY).to_corner(UL, buff=0.35)

        # ── bridge: the frozen lattice from chapter 1 melts into living tissue ─────────
        lattice = VGroup(*[Square(0.28).set_stroke(C_ICE, 1).set_fill(C_ICE, 0.18) for _ in range(15 * 9)]).arrange_in_grid(9, 15, buff=0.12)
        self.add(lattice, tag)
        field = SpikeField(n=46, width=12.5, height=6.6, rate=0.0, seed=4)
        self.go("To understand", frame.animate.scale(0.55), lattice.animate.set_opacity(0.35), rt=2.5, upto="biological brain")
        self.go("biological brain", frame.animate.scale(1 / 0.55), FadeOut(lattice, scale=1.6), FadeIn(field, scale=0.8),
                field.rate.animate.set_value(2.5), rt=2.2, upto="twenty watts")

        # ── 20 W: a power gauge and a dim bulb ────────────────────────────────────────
        panel = RoundedRectangle(width=4.6, height=3.4, corner_radius=0.2, stroke_color=C_DIM, stroke_width=1.5).set_fill(BG, 0.92)
        panel.to_corner(UR, buff=0.5).shift(DOWN * 0.4)
        dial = Arc(1.1, PI, -PI, color=C_GREY, stroke_width=3).move_to(panel.get_center() + UP * 0.3)
        ticks = VGroup()
        for k, lab in enumerate(["0", "10", "20", "30", "40"]):
            a = PI - k * PI / 4
            p = dial.get_arc_center() + 1.1 * np.array([np.cos(a), np.sin(a), 0])
            ticks.add(Line(p, p * 0 + dial.get_arc_center() + 0.95 * np.array([np.cos(a), np.sin(a), 0]), color=C_GREY),
                      T(lab, size=14, color=C_GREY).move_to(dial.get_arc_center() + 1.35 * np.array([np.cos(a), np.sin(a), 0])))
        watts = ValueTracker(0)
        needle = always_redraw(lambda: Line(dial.get_arc_center(), dial.get_arc_center() + 0.95 * np.array(
            [np.cos(PI - PI * watts.get_value() / 40), np.sin(PI - PI * watts.get_value() / 40), 0]), color=C_YELLOW, stroke_width=4))
        wl = counter(0, fmt=0, unit="W", size=34, color=C_YELLOW, tracker=watts).next_to(dial.get_arc_center(), DOWN, buff=0.25)
        self.go("twenty watts", FadeIn(panel), Create(dial), FadeIn(ticks), rt=0.6)
        self.add(needle, wl)
        self.then(watts.animate.set_value(20), rt=1.4, upto="refrigerator light")
        b = bulb(scale=0.9).next_to(panel, DOWN, buff=0.35)
        bl = T("≈ a dim fridge bulb", size=18, color=C_YELLOW).next_to(b, LEFT, buff=0.2)
        self.go("refrigerator light", FadeIn(b, scale=0.6), Write(bl), rt=1.0, upto="Yet within")

        # ── 86 billion neurons, 100 trillion synapses — counted while the field fires ──
        neur = counter(0, unit="neurons", size=36, color=C_GREEN)
        syn = counter(0, unit="synapses", size=36, color=C_TEAL)
        cnt = VGroup(neur, syn).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(DL, buff=0.6)
        bg_c = SurroundingRectangle(cnt, buff=0.25, color=C_DIM, corner_radius=0.15).set_fill(BG, 0.9)
        self.go("Yet within", field.rate.animate.set_value(4), FadeIn(bg_c), FadeIn(cnt), rt=0.6)
        self.go("eighty-six billion", neur.tracker.animate.set_value(86_000_000_000), Indicate(field.somata, color=WHITE, scale_factor=1.2), rt=1.6)
        self.go("one hundred trillion", syn.tracker.animate.set_value(100_000_000_000_000), field.synapses.animate.set_stroke(opacity=0.55), rt=1.6)
        self.go("breathtaking", field.rate.animate.set_value(6), rt=1.0, upto="Crucially")

        # ── perpetual topological motion: neurogenesis, arbors, pruning ────────────────
        self.go("Crucially", FadeOut(VGroup(panel, dial, ticks, wl, b, bl, bg_c, cnt)), field.alpha.animate.set_value(0.25), rt=1.0)
        self.remove(needle)
        lg = living_graph(30, center=LEFT * 3.2, radius=2.2, seed=8)
        thr0 = lg.thr.get_value(); lg.thr.set_value(0.01)
        self.add(lg[0])
        self.go("perpetual topological", FadeIn(lg.nodes), lg.thr.animate.set_value(thr0), lg.nodes.amp.animate.set_value(0.5), rt=1.6)
        ng = VGroup(*[Dot(LEFT * 3.2 + 2 * np.array([np.cos(a), np.sin(a), 0]) * 0.7, radius=0.07, color=C_YELLOW) for a in np.linspace(0, TAU, 5, endpoint=False)])
        ng_l = T("neurogenesis", size=22, color=C_YELLOW).move_to(LEFT * 3.2 + UP * 3.0)
        self.go("neurogenesis", LaggedStart(*[GrowFromCenter(d) for d in ng], lag_ratio=0.2), FadeIn(ng_l), rt=1.0)
        tree = dendrite_tree(RIGHT * 3.0 + DOWN * 2.6, depth=6, length=1.2)
        soma = Dot(RIGHT * 3.0 + DOWN * 2.6, radius=0.16, color=C_GREEN)
        tr_l = T("dendritic arborization", size=22, color=C_GREEN).move_to(RIGHT * 3.0 + UP * 3.0)
        self.go("dendritic arborization", FadeIn(soma), Create(tree, lag_ratio=0.05), FadeIn(tr_l), rt=2.0, upto="spine pruning")
        leaves = VGroup(*tree[-12:])
        pr_l = T("spine pruning", size=22, color=C_RED).next_to(tr_l, DOWN, buff=0.15)
        self.go("spine pruning", leaves.animate.set_color(C_RED), FadeIn(pr_l), rt=0.6)
        self.then(*[Uncreate(l) for l in leaves], lg.thr.animate.set_value(thr0 * 0.75), rt=1.0, upto="real time based")
        self.go("real time based", Create(VGroup(*[l.copy().set_color(C_TEAL).rotate(0.3, about_point=l.get_start()) for l in leaves[:8]]), lag_ratio=0.1),
                rt=1.4, upto="Under the governing")

        # ── STDP: Δw follows Δt ─────────────────────────────────────────────────────────
        self.go("Under the governing", FadeOut(VGroup(lg.nodes, ng, ng_l, tree, soma, tr_l, pr_l)), rt=0.8)
        self.remove(lg[0])
        self.clear_ghosts = [m for m in self.mobjects if m not in (field, tag)]
        for m in self.clear_ghosts:
            self.remove(m)
        pre = Circle(0.4, color=C_BLUE, stroke_width=3).set_fill(C_BLUE, 0.2).move_to(LEFT * 5.2 + UP * 1.6)
        post = Circle(0.4, color=C_PINK, stroke_width=3).set_fill(C_PINK, 0.2).move_to(LEFT * 1.6 + UP * 1.6)
        prel, postl = T("pre", size=18, color=C_BLUE).next_to(pre, DOWN), T("post", size=18, color=C_PINK).next_to(post, DOWN)
        wv = ValueTracker(2.0)
        syn_ln = always_redraw(lambda: Line(pre.get_right(), post.get_left(), color=C_YELLOW, stroke_width=wv.get_value()))
        # spike trains
        ax_pre = Line(LEFT * 6.2, LEFT * 0.6, color=C_DIM).move_to(LEFT * 3.4 + DOWN * 0.4)
        ax_post = ax_pre.copy().shift(DOWN * 0.8)
        trains = VGroup(ax_pre, ax_post, T("pre", size=14, color=C_BLUE).next_to(ax_pre, LEFT, buff=0.1),
                        T("post", size=14, color=C_PINK).next_to(ax_post, LEFT, buff=0.1))
        self.go("Under the governing", FadeIn(VGroup(pre, post, prel, postl)), field.alpha.animate.set_value(0.12), FadeIn(trains), rt=1.0)
        self.add(syn_ln)
        # STDP window on the right
        ax = Axes(x_range=[-50, 50, 25], y_range=[-1.2, 1.2, 1], x_length=5.4, y_length=3.4,
                  axis_config=dict(color=C_GREY, include_tip=False, font_size=16)).move_to(RIGHT * 3.4 + UP * 0.3)
        axl = VGroup(M(r"\Delta t = t_{post}-t_{pre}\ \ (\mathrm{ms})", size=22, color=C_GREY).next_to(ax, DOWN, buff=0.2),
                     M(r"\Delta w", size=28).next_to(ax.y_axis, UP, buff=0.1))
        ltp = ax.plot(lambda x: np.exp(-x / 15), x_range=[0.5, 50], color=C_GREEN, stroke_width=3)
        ltd = ax.plot(lambda x: -0.8 * np.exp(x / 15), x_range=[-50, -0.5], color=C_RED, stroke_width=3)
        eq = M(r"\Delta w=", r"\begin{cases} A_+ e^{-\Delta t/\tau_+} & \Delta t>0\\ -A_- e^{\Delta t/\tau_-} & \Delta t<0\end{cases}", size=28).next_to(ax, UP, buff=0.25)
        self.go("fire in temporal synchrony", Create(ax), FadeIn(axl), rt=0.8)
        # paired spikes: pre at t, post at t+Δt
        dts = [12, 8, 15, 5]
        for k, d in enumerate(dts):
            x0 = -5.6 + 1.3 * k
            sp1 = Line(UP * 0.25, DOWN * 0.0, color=C_BLUE, stroke_width=3).move_to(ax_pre.get_center() * [0, 1, 0] + RIGHT * x0 + UP * 0.12)
            sp2 = Line(UP * 0.25, DOWN * 0.0, color=C_PINK, stroke_width=3).move_to(ax_post.get_center() * [0, 1, 0] + RIGHT * (x0 + d / 30) + UP * 0.12)
            dot = Dot(ax.c2p(d, np.exp(-d / 15)), color=C_GREEN, radius=0.07)
            self.play(FadeIn(sp1), Flash(pre, color=C_BLUE, line_length=0.2), run_time=0.25)
            self.play(FadeIn(sp2), Flash(post, color=C_PINK, line_length=0.2), FadeIn(dot, scale=2), wv.animate.increment_value(1.0), run_time=0.35)
        self.go("physically thickens", Create(ltp), Write(eq[0]), Write(eq[1]), wv.animate.set_value(8), rt=1.6, upto="AMPA and NMDA")
        rec = VGroup(*[Dot(radius=0.05, color=c).move_to(post.get_left() + UP * (0.25 - 0.1 * i) + LEFT * 0.05)
                       for i, c in enumerate([C_TEAL, C_ORANGE, C_TEAL, C_ORANGE, C_TEAL, C_ORANGE])])
        recl = VGroup(T("AMPA", size=16, color=C_TEAL), T("NMDA", size=16, color=C_ORANGE)).arrange(RIGHT, buff=0.3).next_to(post, UP, buff=0.2)
        self.go("AMPA and NMDA", LaggedStart(*[FadeIn(r, scale=3) for r in rec], lag_ratio=0.15), FadeIn(recl), rt=1.2, upto="reinforce")
        self.go("reinforce", Indicate(syn_ln, color=WHITE), rt=0.8, upto="Conversely")
        # anti-causal pairs and disuse → depression + pruning
        self.go("Conversely", Create(ltd), *[FadeIn(Dot(ax.c2p(-d, -0.8 * np.exp(-d / 15)), color=C_RED, radius=0.07), scale=2) for d in (6, 14, 25)],
                wv.animate.set_value(2.0), rt=1.4, upto="microglia")
        glia = VGroup(*[Circle(0.12 + 0.06 * i, color=C_PURPLE, stroke_width=0).set_fill(C_PURPLE, 0.35).shift(0.1 * np.array([np.cos(i), np.sin(i * 1.7), 0])) for i in range(4)])
        glia.move_to(LEFT * 3.4 + UP * 3.0)
        gl = T("microglia", size=18, color=C_PURPLE).next_to(glia, UP, buff=0.1)
        self.go("microglia", FadeIn(glia), FadeIn(gl), rt=0.5)
        self.then(glia.animate.move_to(syn_ln.get_center()), gl.animate.move_to(syn_ln.get_center() + UP * 0.5), rt=1.0, upto="conserve precious")
        self.go("conserve precious", wv.animate.set_value(0.05), glia.animate.scale(1.4).set_opacity(0.2), FadeOut(rec), FadeOut(recl), rt=1.4,
                upto="does not separate")

        # ── no train / inference split: one continuous line of learning ───────────────
        stdp = VGroup(ax, axl, ltp, ltd, eq, pre, post, prel, postl, trains, glia, gl)
        dots = [m for m in self.mobjects if isinstance(m, (Dot, Line)) and m not in (field,) and m not in stdp]
        self.go("does not separate", FadeOut(stdp), *[FadeOut(d) for d in dots], rt=0.8)
        self.remove(syn_ln)
        art = VGroup(Line(LEFT * 6, LEFT * 1.4, color=C_ORANGE, stroke_width=6), Line(LEFT * 1.4, RIGHT * 0.2, color=C_ICE, stroke_width=6)).move_to(UP * 2.4)
        art_l = VGroup(T("silicon:  train  |  then freeze", size=20, color=C_ICE)).next_to(art, UP, buff=0.15)
        bio_x = np.linspace(-6, 0.2, 200)
        bio = VMobject(stroke_color=C_GREEN, stroke_width=5).set_points_smoothly([np.array([x, 1.2 + 0.18 * np.sin(4 * x) * np.cos(1.3 * x), 0]) for x in bio_x])
        bio_l = T("brain:  learning ≡ inference, always", size=20, color=C_GREEN).next_to(bio, DOWN, buff=0.2)
        self.then(Create(art), FadeIn(art_l), rt=0.9)
        self.then(Create(bio), FadeIn(bio_l), rt=1.2, upto="Every single percept")
        # percepts arrive and every one rewires a small net
        net = NeuralNet((4, 5, 4), width=3.4, height=2.4, seed=3, edge_op=0.8).move_to(RIGHT * 4.0 + DOWN * 1.4)
        self.add(net)
        rngw = np.random.default_rng(6)
        def rewire():
            return AnimationGroup(*[e.animate.set_stroke(color=C_BLUE if rngw.random() > 0.4 else C_RED, width=0.5 + 3 * rngw.random())
                                    for g in net.edges for e in g])
        for key, word in [("Every single percept", "a percept"), ("every sentence", "a sentence"), ("every thought", "a thought")]:
            chip = label_box(word, C_GREEN, size=18).move_to(LEFT * 3 + DOWN * 2.2)
            self.go(key, FadeIn(chip, shift=RIGHT), rt=0.4)
            self.then(chip.animate.move_to(net.layers[0]).scale(0.3).set_opacity(0), net.flow(0, C_GREEN), rewire(), rt=1.0, upto="physically alters")
        self.go("physically alters", Indicate(net.edges, color=C_GREEN), rt=0.8, upto="event-driven and asynchronous")

        # ── event-driven & asynchronous: sparse raster vs. global clock ───────────────
        self.go("event-driven and asynchronous", FadeOut(VGroup(art, art_l, bio, bio_l, net)), field.alpha.animate.set_value(0.18), rt=0.8)
        rast_ax = VGroup(*[Line(LEFT * 6, RIGHT * 0.5, color=C_DIM, stroke_width=1).shift(UP * (2.6 - 0.28 * i)) for i in range(16)])
        rast_l = T("16 neurons · spikes over time", size=16, color=C_GREY).next_to(rast_ax, UP, buff=0.1).align_to(rast_ax, LEFT)
        scroll = ValueTracker(0)
        rngs = np.random.default_rng(3)
        spikes_t = [np.sort(rngs.random(int(4 + 8 * rngs.random())) * 12) for _ in range(16)]

        def raster():
            g = VGroup()
            s = scroll.get_value()
            for i, ts in enumerate(spikes_t):
                for t0 in ts:
                    x = -6 + (t0 - s) % 12 * (6.5 / 12)
                    g.add(Line(UP * 0.1, DOWN * 0.1, color=C_GREEN, stroke_width=3).move_to([x, 2.6 - 0.28 * i, 0]))
            return g
        rast = always_redraw(raster)
        self.go("event-driven and asynchronous", Create(rast_ax, lag_ratio=0.05), FadeIn(rast_l), rt=0.8)
        self.add(rast)
        self.then(scroll.animate(rate_func=linear).set_value(3), rt=2.0, upto="sparse millisecond")
        hz = M(r"1\text{–}10\ \mathrm{Hz}", size=40, color=C_GREEN).move_to(RIGHT * 3.6 + UP * 1.6)
        self.go("sparse millisecond", scroll.animate(rate_func=linear).set_value(5), rt=1.6)
        self.go("one to ten hertz", Write(hz), scroll.animate(rate_func=linear).set_value(7), rt=1.6)
        clk_x = np.linspace(-6, 0.5, 400)
        clk = VMobject(stroke_color=C_ORANGE, stroke_width=3).set_points_as_corners(
            [np.array([x, -1.4 + 0.35 * np.sign(np.sin(x * 9)), 0]) for x in clk_x])
        clk_l = T("GPU: global clock, every cycle, every unit", size=18, color=C_ORANGE).next_to(clk, DOWN, buff=0.2).align_to(clk, LEFT)
        ghz = M(r"\sim 2\ \mathrm{GHz}", size=40, color=C_ORANGE).move_to(RIGHT * 3.6 + DOWN * 1.4)
        self.go("continuous synchronization", Create(clk), FadeIn(clk_l), Write(ghz), scroll.animate(rate_func=linear).set_value(9), rt=1.8,
                upto="Now compare")

        # ── the data center ─────────────────────────────────────────────────────────────
        self.go("Now compare", FadeOut(VGroup(rast_ax, rast_l, hz, clk, clk_l, ghz)), field.animate.scale(0.48).to_edge(LEFT, buff=0.3), field.alpha.animate.set_value(1.0),
                rt=1.4)
        self.remove(rast)
        brain_l = T("brain  ·  20 W", size=22, color=C_GREEN).next_to(field, UP, buff=0.2)
        photo = framed_image(os.path.join(PROJECT, "remotion_studio/public/assets/real_world/datacenters/gpu_cluster_racks.jpg"), height=2.6)
        photo.to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        photo.add(T("hyperscale AI data center", size=16, color=C_GREY).next_to(photo, UP, buff=0.1))
        mw = counter(0, unit="MW", size=36, color=C_ORANGE).next_to(photo, DOWN, buff=0.25)
        self.then(FadeIn(brain_l), rt=0.4)
        self.go("frontier GPU cluster", FadeIn(photo, shift=LEFT), FadeIn(mw), rt=0.8)
        self.then(mw.tracker.animate.set_value(150), rt=1.2, upto="liquid cooling")
        photo2 = framed_image(os.path.join(PROJECT, "remotion_studio/public/assets/real_world/datacenters/datacenter_supercomputer.jpg"), height=2.0)
        photo2.next_to(photo, LEFT, buff=0.3).shift(DOWN * 0.3)
        cool = VGroup(*[Line(DOWN * 0.3, UP * 0.3, color=C_BLUE, stroke_width=3).shift(RIGHT * 0.2 * k) for k in range(8)]).next_to(photo2, DOWN, buff=0.15)
        self.go("liquid cooling", FadeIn(photo2, shift=UP), LaggedStart(*[ShowPassingFlash(l.copy().set_stroke(C_ICE, 4)) for l in cool], lag_ratio=0.1), rt=1.4)
        arr = systolic(8, 8, cell=0.3).move_to(RIGHT * 3.6 + DOWN * 1.9)
        wf = ValueTracker(-3)
        wavefront(arr, wf)
        self.go("Inside, millions", FadeOut(photo2), mw.animate.next_to(photo, LEFT, buff=0.3), FadeIn(arr, lag_ratio=0.01), rt=0.9)
        self.then(wf.animate(rate_func=linear).set_value(16), rt=1.6, upto="systolic arrays")
        mm = M(r"Y = WX", size=34, color=C_ORANGE).next_to(arr, LEFT, buff=0.4)
        self.go("systolic arrays", Write(mm), wf.animate(rate_func=linear).set_value(-3), rt=1.6, upto="Why couldn't")

        # ── the question, spatially: living field vs. frozen grid ──────────────────────
        qm = T("?", size=110, color=WHITE, weight=BOLD).move_to(ORIGIN + DOWN * 0.3)
        dwb = M(r"\Delta w \neq 0", size=36, color=C_GREEN).next_to(field, DOWN, buff=0.3)
        dwg = M(r"\Delta w = 0", size=36, color=C_ICE).next_to(arr, UP, buff=0.3)
        self.go("Why couldn't", FadeOut(photo), FadeOut(mw), Write(qm), FadeIn(dwb), FadeIn(dwg), field.rate.animate.set_value(8), rt=1.4)
        self.go("Why did computer science", wf.animate(rate_func=linear).set_value(16), Indicate(qm), rt=2.0, upto="frozen tensors")
        self.go("frozen tensors", arr.animate.set_color(C_ICE), rt=1.0)
        self.finish()
