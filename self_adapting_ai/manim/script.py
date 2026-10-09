from manim import *
import numpy as np

# ==============================================================================
# GLOBAL CREATIVE CONSTANTS (Classic 3Blue1Brown Aesthetic)
# ==============================================================================
BG = "#1C1C1C"
PRIMARY = "#58C4DD"     # Blue
SECONDARY = "#83C167"   # Green
ACCENT = "#FFFF00"      # Yellow
CORAL = "#FF6B6B"       # Red / Coral
PURPLE = "#C792EA"      # Soft Purple
WHITE = "#FFFFFF"
GRAY_A = "#EAEAEA"
GRAY_B = "#888888"
GRAY_C = "#2A2A2A"

MONO = "Menlo"

def create_card(text_mobj, color=PRIMARY, fill_color=GRAY_C, fill_opacity=0.6, buff=0.25):
    """Creates a card mathematically fitted to text with guaranteed padding so it NEVER overflows."""
    box = RoundedRectangle(
        corner_radius=0.15,
        width=max(text_mobj.width + buff * 2, 2.0),
        height=text_mobj.height + buff * 2,
        color=color,
        fill_color=fill_color,
        fill_opacity=fill_opacity
    )
    box.move_to(text_mobj.get_center())
    return VGroup(box, text_mobj)

# ==============================================================================
# CHAPTER 1: THE MONOLITH OF DEEP LEARNING
# ==============================================================================
class Scene1_TheMonolith(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Title
        t = Text("THE MONOLITH OF MODERN AI", font=MONO, font_size=30, color=PRIMARY, weight=BOLD)
        st = Text("Frozen Architectures & The Transformer Monopoly", font=MONO, font_size=18, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # Token Sequence
        toks = VGroup(*[
            VGroup(
                RoundedRectangle(corner_radius=0.1, height=0.7, width=1.0, color=PRIMARY, fill_color=GRAY_C, fill_opacity=0.7),
                Text(lbl, font=MONO, font_size=17, color=WHITE)
            ) for lbl in ["[x₁]", "[x₂]", "[x₃]", "[x₄]"]
        ]).arrange(RIGHT, buff=0.35).shift(UP * 0.9)
        self.play(LaggedStart(*[FadeIn(tok, shift=DOWN*0.2) for tok in toks], lag_ratio=0.15), run_time=1.0)
        self.wait(0.5)

        # Projection Blocks
        projs = VGroup(*[
            create_card(Text(lbl, font=MONO, font_size=15, color=SECONDARY), color=SECONDARY, buff=0.18)
            for lbl in ["W_Q  (Query)", "W_K  (Key)", "W_V  (Value)"]
        ]).arrange(RIGHT, buff=0.4).shift(DOWN * 0.3)
        arrows1 = VGroup(*[
            Arrow(toks[i].get_bottom(), projs[min(i, 2)].get_top(), buff=0.12, color=GRAY_B, stroke_width=2.0)
            for i in range(4)
        ])
        self.play(Create(arrows1), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(p) for p in projs], lag_ratio=0.2), run_time=1.0)
        self.wait(0.6)

        # Bilinear Attention Formula Box
        attn_txt = Text("Attention(Q, K, V) = softmax( Q·Kᵀ / √d ) · V", font=MONO, font_size=17, color=ACCENT, weight=BOLD)
        attn_card = create_card(attn_txt, color=ACCENT, buff=0.22).shift(DOWN * 1.6)
        self.play(FadeIn(attn_card, shift=UP*0.2), run_time=0.9)
        self.wait(0.8)

        # Residual Stream Highway
        res_txt = Text("x_out = LayerNorm( x + Attention(x) )", font=MONO, font_size=15, color=PRIMARY)
        res_card = create_card(res_txt, color=PRIMARY, buff=0.18).shift(DOWN * 2.5)
        self.play(FadeIn(res_card, shift=UP*0.2), run_time=0.8)
        self.wait(0.8)

        # Clear lower elements for stamp
        self.play(FadeOut(attn_card), FadeOut(res_card), FadeOut(arrows1), FadeOut(projs), run_time=0.6)
        
        # Frozen Weights Stamp
        stamp_txt = Text("SYNAPTIC WEIGHTS: PERMANENTLY FROZEN IN SILICON", font=MONO, font_size=16, color=CORAL, weight=BOLD)
        stamp_card = create_card(stamp_txt, color=CORAL, fill_color="#301010", buff=0.25).shift(DOWN * 0.5)
        self.play(GrowFromCenter(stamp_card), run_time=0.9)
        self.wait(0.8)

        q_txt = Text("Why can't our models rewire their own computational anatomy?", font=MONO, font_size=17, color=WHITE, weight=BOLD)
        q_card = create_card(q_txt, color=WHITE, buff=0.2).next_to(stamp_card, DOWN, buff=0.4)
        self.play(Write(q_txt), Create(q_card[0]), run_time=1.1)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 2: THE BIOLOGICAL ARCHITECTURE & NEUROMORPHIC PRINCIPLES
# ==============================================================================
class Scene2_TheBiologicalDream(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("THE BIOLOGICAL ARCHITECTURE", font=MONO, font_size=30, color=SECONDARY, weight=BOLD)
        st = Text("Spike Dynamics, Dendritic Plasticity & Self-Organization", font=MONO, font_size=18, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # Organic Neural Graph
        node_pts = [
            [-3.2, 0.4, 0], [-2.0, 1.5, 0], [-1.0, 0.1, 0], [-2.2, -1.2, 0],
            [0.8, 1.4, 0], [2.2, 0.3, 0], [1.2, -1.4, 0], [3.2, -1.0, 0],
            [-0.1, -0.6, 0], [0.1, 0.7, 0]
        ]
        nodes = VGroup(*[
            Circle(radius=0.2, color=SECONDARY, fill_color="#103010", fill_opacity=0.8).move_to(pt)
            for pt in node_pts
        ])
        edge_pairs = [(0,1), (1,2), (0,3), (2,3), (1,9), (9,4), (4,5), (5,7), (6,7), (2,8), (8,6), (9,8)]
        edges = VGroup(*[
            Line(nodes[i].get_center(), nodes[j].get_center(), color=GRAY_B, stroke_width=1.8)
            for i, j in edge_pairs
        ])
        self.play(Create(edges), LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.08), run_time=1.2)
        self.wait(0.5)

        # Action Potential Spikes firing
        pulse_anims = [n.animate.set_color(ACCENT).set_fill(ACCENT, opacity=0.9) for n in [nodes[0], nodes[1], nodes[9], nodes[4], nodes[5]]]
        self.play(*pulse_anims, run_time=0.6)
        self.wait(0.4)

        # Structural Rewiring: Sprouting & Pruning
        new_edge1 = DashedLine(nodes[0].get_center(), nodes[9].get_center(), color=SECONDARY, stroke_width=2.5)
        new_edge2 = DashedLine(nodes[2].get_center(), nodes[7].get_center(), color=SECONDARY, stroke_width=2.5)
        prune_edge = edges[2]
        self.play(Create(new_edge1), Create(new_edge2), prune_edge.animate.set_color(CORAL).set_stroke(width=1), run_time=0.9)
        self.play(FadeOut(prune_edge), run_time=0.5)

        # Restore nodes
        self.play(*[n.animate.set_color(SECONDARY).set_fill("#103010", opacity=0.8) for n in nodes], run_time=0.5)

        # Local Plasticity Cards
        hebb_txt = Text("Hebbian STDP: Neurons that fire together, wire together\nΔW_ij = η · (Pre_i · Post_j) - γ · W_ij", font=MONO, font_size=14, color=WHITE)
        hebb_card = create_card(hebb_txt, color=SECONDARY, buff=0.22).shift(DOWN * 2.2)
        self.play(FadeIn(hebb_card, shift=UP*0.2), run_time=0.9)
        self.wait(0.8)

        # Question Card
        q_txt = Text("Can complex modularity naturally emerge from unconstrained plasticity?", font=MONO, font_size=15, color=ACCENT, weight=BOLD)
        q_card = create_card(q_txt, color=ACCENT, buff=0.2).next_to(hebb_card, UP, buff=0.3)
        self.play(FadeIn(q_card, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 3: THE SELF-ORGANIZING HYPOTHESIS & NEUROEVOLUTION
# ==============================================================================
class Scene3_SelfOrganizingHypothesis(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("THE NEUROEVOLUTION HYPOTHESIS", font=MONO, font_size=30, color=ACCENT, weight=BOLD)
        st = Text("Topology Search, Weight Agnosticism & Spiking Networks", font=MONO, font_size=18, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # WANN & NEAT Concept Cards
        c1_txt = Text("Weight Agnostic Neural Networks (Gaier & Ha, 2019)\nTopology alone encodes intelligence without weight training.", font=MONO, font_size=14, color=WHITE)
        c1 = create_card(c1_txt, color=PRIMARY, buff=0.22).shift(UP * 0.8)

        c2_txt = Text("Evolutionary Topology Search (NEAT / HyperNEAT)\nMutate edges, sprout nodes, evaluate fitness iteratively.", font=MONO, font_size=14, color=WHITE)
        c2 = create_card(c2_txt, color=SECONDARY, buff=0.22).next_to(c1, DOWN, buff=0.3)

        c3_txt = Text("The Grand Premise:\nGiven enough compute, networks self-organize optimal schemas.", font=MONO, font_size=14, color=ACCENT, weight=BOLD)
        c3 = create_card(c3_txt, color=ACCENT, buff=0.22).next_to(c2, DOWN, buff=0.3)

        self.play(FadeIn(c1, shift=DOWN*0.15), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(c2, shift=DOWN*0.15), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(c3, shift=UP*0.15), run_time=0.8)
        self.wait(0.8)

        # The Wall of Scale Warning
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3), run_time=0.6)
        wall_txt = Text("THE WALL OF SCALE:\nSelf-organizing networks catastrophically hit a ceiling\nwhen attempting linguistic associative reasoning.", font=MONO, font_size=16, color=CORAL, weight=BOLD)
        wall_card = create_card(wall_txt, color=CORAL, fill_color="#301010", buff=0.25).shift(DOWN * 0.2)
        self.play(GrowFromCenter(wall_card), run_time=0.9)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 4: THE MODULAR EMERGENCE PARADOX
# ==============================================================================
class Scene4_TheParadox(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("THE MODULAR EMERGENCE PARADOX", font=MONO, font_size=30, color=CORAL, weight=BOLD)
        st = Text("Why Dynamic Rewiring Cannot Discover Bilinear Attention", font=MONO, font_size=18, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # Split Screen Comparison
        # Left: Graph Rewiring
        l_title = Text("STATIC GRAPH REWIRING", font=MONO, font_size=15, color=CORAL, weight=BOLD)
        l_body = Text("• Modifies scalar weight W_ij ∈ ℝ\n• Dictates WHO connects to whom\n• Fixed physical wire\n• Linear mixture of features", font=MONO, font_size=13, color=WHITE)
        l_grp = VGroup(l_title, l_body).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        l_card = create_card(l_grp, color=CORAL, buff=0.25).shift(LEFT * 3.4 + DOWN * 0.3)

        # Right: Bilinear Attention
        r_title = Text("BILINEAR ATTENTION", font=MONO, font_size=15, color=PRIMARY, weight=BOLD)
        r_body = Text("• Dynamic Metric Space: ⟨q_i, k_j⟩\n• Coordinate projections: W_Q, W_K\n• No fixed physical wire\n• Recomputed per query at runtime", font=MONO, font_size=13, color=WHITE)
        r_grp = VGroup(r_title, r_body).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        r_card = create_card(r_grp, color=PRIMARY, buff=0.25).shift(RIGHT * 3.4 + DOWN * 0.3)

        self.play(FadeIn(l_card, shift=RIGHT*0.2), FadeIn(r_card, shift=LEFT*0.2), run_time=1.1)
        self.wait(0.8)

        # Summary Callout
        call_txt = Text("Graph edges decide WHO connects.\nAttention decides HOW to measure distance in latent space.", font=MONO, font_size=15, color=ACCENT, weight=BOLD)
        call_card = create_card(call_txt, color=ACCENT, buff=0.22).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(call_card, shift=UP*0.2), run_time=0.9)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 5: THEOREM 1 — RANK COLLAPSE IN LOCAL PLASTICITY
# ==============================================================================
class Scene5_Theorem1_RankCollapse(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("THEOREM 1: RANK COLLAPSE", font=MONO, font_size=30, color=CORAL, weight=BOLD)
        st = Text("Mathematical Proof of Representation Death in Hebbian Plasticity", font=MONO, font_size=17, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # Equation Card
        eq_txt = Text("Oja's Subspace Plasticity Rule:\ndW/dt = α·(HᵀH) - β·W(HᵀH)W", font=MONO, font_size=15, color=WHITE)
        eq_card = create_card(eq_txt, color=PRIMARY, buff=0.2).shift(UP * 1.2)
        self.play(FadeIn(eq_card, shift=DOWN*0.15), run_time=0.8)
        self.wait(0.6)

        # Spectral Eigenvalue Spectrum
        axes = Axes(x_range=[0, 5, 1], y_range=[0, 8, 2], x_length=4.2, y_length=2.0, axis_config={"color": GRAY_B}).shift(DOWN * 0.7 + LEFT * 2.8)
        bar_lbl = Text("Eigenvalue Spectrum", font=MONO, font_size=13, color=GRAY_A).next_to(axes, UP, buff=0.1)
        b1 = Rectangle(height=1.8, width=0.35, color=CORAL, fill_color=CORAL, fill_opacity=0.9).move_to(axes.c2p(1, 4.0), aligned_edge=DOWN)
        b2 = Rectangle(height=0.12, width=0.35, color=GRAY_B, fill_color=GRAY_B, fill_opacity=0.5).move_to(axes.c2p(2, 0.25), aligned_edge=DOWN)
        b3 = Rectangle(height=0.06, width=0.35, color=GRAY_B, fill_color=GRAY_B, fill_opacity=0.5).move_to(axes.c2p(3, 0.12), aligned_edge=DOWN)
        b4 = Rectangle(height=0.03, width=0.35, color=GRAY_B, fill_color=GRAY_B, fill_opacity=0.5).move_to(axes.c2p(4, 0.06), aligned_edge=DOWN)

        t_note = Text("Dominant Mode λ₁ exponentially\nsuppresses all subordinate modes:\nd/dt ln(||w₁||/||w_k||) = 2α(λ₁ - λ_k) > 0\n⟹ Effective Rank collapses to 1!", font=MONO, font_size=13, color=CORAL).next_to(axes, RIGHT, buff=0.5)

        self.play(Create(axes), FadeIn(bar_lbl), run_time=0.8)
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), GrowFromEdge(b3, DOWN), GrowFromEdge(b4, DOWN), FadeIn(t_note), run_time=1.1)
        self.wait(0.8)

        # Conclusion Card
        c_txt = Text("Without global orthogonalization, local plasticity suffers representation death.", font=MONO, font_size=14, color=ACCENT, weight=BOLD)
        c_card = create_card(c_txt, color=ACCENT, buff=0.2).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(c_card, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 6: THEOREM 2 — ROUTING EXPRESSIVITY LOWER BOUND
# ==============================================================================
class Scene6_Theorem2_RoutingBounds(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("THEOREM 2: ROUTING EXPRESSIVITY", font=MONO, font_size=30, color=PRIMARY, weight=BOLD)
        st = Text("The Graph Moore Bound vs. Constant-Depth Attention", font=MONO, font_size=18, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # Transformer Scaling Card
        tf_title = Text("TRANSFORMER ATTENTION SCALING", font=MONO, font_size=15, color=PRIMARY, weight=BOLD)
        tf_body = Text("• Realizes arbitrary token permutations\n• Parameter complexity: O(d²) independent of length N\n• Layer Latency: O(1) constant depth", font=MONO, font_size=13, color=WHITE)
        tf_grp = VGroup(tf_title, tf_body).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        tf_card = create_card(tf_grp, color=PRIMARY, buff=0.25).shift(UP * 0.9)

        # Graph Bound Card
        g_title = Text("PHYSICAL GRAPH DEGREE BOTTLENECK", font=MONO, font_size=15, color=CORAL, weight=BOLD)
        g_body = Text("• Bounded maximum neuron degree Δ\n• Moore Bound: Diameter D ≥ log(N) / log(Δ - 1)\n• Latency penalty: Ω(log N) multi-hop delays\n• Zero-delay routing requires Ω(N²) physical connections!", font=MONO, font_size=13, color=WHITE)
        g_grp = VGroup(g_title, g_body).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        g_card = create_card(g_grp, color=CORAL, buff=0.25).next_to(tf_card, DOWN, buff=0.35)

        self.play(FadeIn(tf_card, shift=DOWN*0.15), run_time=0.9)
        self.wait(0.6)
        self.play(FadeIn(g_card, shift=UP*0.15), run_time=0.9)
        self.wait(0.8)

        # Core Takeaway
        bot_txt = Text("Transformers decouple routing expressivity from physical connection density.", font=MONO, font_size=14, color=ACCENT, weight=BOLD)
        bot_card = create_card(bot_txt, color=ACCENT, buff=0.2).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(bot_card, shift=UP*0.15), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 7: THEOREM 3 — THE HARDWARE & CREDIT ASSIGNMENT BARRIER
# ==============================================================================
class Scene7_Theorem3_HardwareBarrier(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("THEOREM 3: HARDWARE & CREDIT ASSIGNMENT", font=MONO, font_size=28, color=ACCENT, weight=BOLD)
        st = Text("The Hardware Lottery & Exponential Gradient Variance", font=MONO, font_size=17, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # Hardware Lottery Card
        hw_title = Text("1. THE HARDWARE LOTTERY (Sara Hooker, 2020)", font=MONO, font_size=14, color=ACCENT, weight=BOLD)
        hw_body = Text("• Systolic Tensor Cores (GPUs) require dense arithmetic:\n  Intensity = 2NBd² FLOPs / (2NBd + 2d²) Bytes ≈ O(d) >> 1\n• Sparse Graphs: Pointer chasing throttles memory bandwidth (O(1))", font=MONO, font_size=12, color=WHITE)
        hw_grp = VGroup(hw_title, hw_body).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        hw_card = create_card(hw_grp, color=ACCENT, buff=0.22).shift(UP * 0.9)

        # Variance Card
        var_title = Text("2. TEMPORAL CREDIT ASSIGNMENT EXPLOSION", font=MONO, font_size=14, color=CORAL, weight=BOLD)
        var_body = Text("• Backpropagation: Exact deterministic gradient (Var = 0)\n• Local Hebbian Updates: Driven by global neuromodulatory noise\n• Variance: Var(ĝ) ∝ T · σ² ⟹ Sample Complexity gap K_local >> K_backprop", font=MONO, font_size=12, color=WHITE)
        var_grp = VGroup(var_title, var_body).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        var_card = create_card(var_grp, color=CORAL, buff=0.22).next_to(hw_card, DOWN, buff=0.3)

        self.play(FadeIn(hw_card, shift=DOWN*0.15), run_time=0.9)
        self.wait(0.6)
        self.play(FadeIn(var_card, shift=UP*0.15), run_time=0.9)
        self.wait(0.8)

        take_txt = Text("Local self-organizing learning requires millions of times more data on long sequences.", font=MONO, font_size=13, color=PRIMARY, weight=BOLD)
        take_card = create_card(take_txt, color=PRIMARY, buff=0.2).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(take_card, shift=UP*0.15), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 8: EMPIRICAL BENCHMARKS & LAB EVIDENCE
# ==============================================================================
class Scene8_EmpiricalBenchmarks(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("EMPIRICAL LAB BENCHMARKS", font=MONO, font_size=30, color=SECONDARY, weight=BOLD)
        st = Text("Associative In-Context Retrieval Challenge", font=MONO, font_size=18, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # Dual Axes
        ax1 = Axes(x_range=[0, 40, 10], y_range=[1.0, 3.8, 1.0], x_length=4.5, y_length=2.4, axis_config={"color": GRAY_B}).shift(LEFT * 3.3 + DOWN * 0.3)
        ax1_t = Text("Loss Dynamics", font=MONO, font_size=14, color=WHITE, weight=BOLD).next_to(ax1, UP, buff=0.1)
        c_so_loss = ax1.plot(lambda x: 1.5 + 2.0 * np.exp(-x * 0.03), color=CORAL, stroke_width=2.5)
        c_tf_loss = ax1.plot(lambda x: 1.4 + 2.1 * np.exp(-x * 0.08), color=PRIMARY, stroke_width=2.5)

        ax2 = Axes(x_range=[0, 40, 10], y_range=[0, 100, 25], x_length=4.5, y_length=2.4, axis_config={"color": GRAY_B}).shift(RIGHT * 3.3 + DOWN * 0.3)
        ax2_t = Text("Retrieval Accuracy (%)", font=MONO, font_size=14, color=WHITE, weight=BOLD).next_to(ax2, UP, buff=0.1)
        c_so_acc = ax2.plot(lambda x: 3.1 + 5.0 * (1.0 - np.exp(-x * 0.05)), color=CORAL, stroke_width=2.5)
        c_tf_acc = ax2.plot(lambda x: 3.1 + 88.0 * (1.0 - np.exp(-x * 0.1)), color=SECONDARY, stroke_width=2.5)
        c_chance = ax2.plot(lambda x: 3.1, color=ACCENT, stroke_width=1.5)

        self.play(Create(ax1), Create(ax2), FadeIn(ax1_t), FadeIn(ax2_t), run_time=0.9)
        self.play(Create(c_so_loss), Create(c_tf_loss), Create(c_so_acc), Create(c_tf_acc), Create(c_chance), run_time=1.5)
        self.wait(0.8)

        # Benchmark Metrics Box
        m_txt = Text("Transformer: 92.3% Accuracy (Spectral Rank: 14.56 Preserved)\nSO-DRN Rewiring: 7.7% Accuracy (Severe Rank Collapse: ~2.1 Modes)", font=MONO, font_size=14, color=ACCENT, weight=BOLD)
        m_card = create_card(m_txt, color=ACCENT, buff=0.22).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(m_card, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 9: FRONTIER RESEARCH IN TOP AI LABS
# ==============================================================================
class Scene9_FrontierLabs(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("FRONTIER LAB RESEARCH", font=MONO, font_size=30, color=PRIMARY, weight=BOLD)
        st = Text("DeepMind, Anthropic & OpenAI: Why Transformers Persist", font=MONO, font_size=18, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        c1_txt = Text("1. In-Context Learning is Implicit Gradient Descent (von Oswald et al., 2022)\nAttention layers simulate a meta-optimizer in the forward pass.\nNo synaptic rewiring needed: learning occurs in activation space!", font=MONO, font_size=13, color=WHITE)
        c1 = create_card(c1_txt, color=PRIMARY, buff=0.22).shift(UP * 0.9)

        c2_txt = Text("2. Mechanistic Circuits & Induction Heads (Anthropic, 2021)\nAttention acts as a soft routing bus where induction heads\nspontaneously emerge to copy, bind, and translate token relationships.", font=MONO, font_size=13, color=WHITE)
        c2 = create_card(c2_txt, color=SECONDARY, buff=0.22).next_to(c1, DOWN, buff=0.3)

        c3_txt = Text("3. Meta-Plasticity (Kirsch & Schmidhuber, DeepMind)\nTrain secondary neural networks to discover new plasticity rules,\nescaping rigid hand-engineered Hebbian formulas.", font=MONO, font_size=13, color=ACCENT, weight=BOLD)
        c3 = create_card(c3_txt, color=ACCENT, buff=0.22).next_to(c2, DOWN, buff=0.3)

        self.play(FadeIn(c1, shift=DOWN*0.15), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(c2, shift=DOWN*0.15), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(c3, shift=UP*0.15), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)


# ==============================================================================
# CHAPTER 10: THE 10-YEAR HORIZON & LIVING SYNTHETIC MINDS
# ==============================================================================
class Scene10_The10YearFrontier(Scene):
    def construct(self):
        self.camera.background_color = BG

        t = Text("THE 10-YEAR FRONTIER: 2026–2035", font=MONO, font_size=30, color=ACCENT, weight=BOLD)
        st = Text("How Self-Adapting Artificial Intelligence Can Truly Work", font=MONO, font_size=18, color=GRAY_A)
        hdr = VGroup(t, st).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(Write(t), run_time=1.0)
        self.play(FadeIn(st, shift=UP*0.15), run_time=0.6)
        self.wait(0.6)

        # 4 Pillars
        p_data = [
            ("1. META-PLASTICITY", "Learn the learning rule\nvia meta-gradient descent.", PRIMARY),
            ("2. CONTINUOUS NEURAL ODEs", "Liquid time-constants\nDynamic temporal routing.", SECONDARY),
            ("3. KOLMOGOROV-ARNOLD NETS", "Nonlinear splines embedded\ndirectly within synapses.", PURPLE),
            ("4. IN-MEMORY CROSSBARS", "Neuromorphic hardware\nCompute co-located with memory.", CORAL)
        ]
        pos = [LEFT * 3.3 + UP * 0.8, RIGHT * 3.3 + UP * 0.8, LEFT * 3.3 + DOWN * 1.3, RIGHT * 3.3 + DOWN * 1.3]

        cards = VGroup()
        for i, (p_t, p_d, col) in enumerate(p_data):
            p_txt = Text(f"{p_t}\n{p_d}", font=MONO, font_size=13, color=WHITE)
            p_card = create_card(p_txt, color=col, buff=0.22)
            p_card.move_to(pos[i])
            cards.add(p_card)

        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.2) for c in cards], lag_ratio=0.2), run_time=1.4)
        self.wait(1.0)
        self.play(FadeOut(cards), run_time=0.6)

        # Final Philosophical Statement
        fin_txt = Text("THE FUTURE OF INTELLIGENCE:\nNot a static frozen monolith. Nor a blind copy of biology.\nA self-adapting mathematical organism: fluid, continuous, and alive.", font=MONO, font_size=16, color=WHITE, weight=BOLD)
        fin_card = create_card(fin_txt, color=PRIMARY, fill_color="#0D1B2A", buff=0.3).shift(DOWN * 0.3)
        self.play(FadeIn(fin_card, scale=0.9), run_time=1.1)
        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
