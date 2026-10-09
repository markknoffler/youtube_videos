from manim import *
import numpy as np
import os

# ==============================================================================
# MASTERCLASS COLOR PALETTE: PURPLE, HOT PINK & LAVENDER (NO BLUE!)
# ==============================================================================
COLOR_BG = "#0D021A"           # Deep Obsidian Violet
COLOR_HOT_PINK = "#FF2A85"     # Primary Vibrant Hot Pink
COLOR_LAVENDER = "#C77DFF"     # Secondary Electric Lavender
COLOR_LIGHT_LAVENDER = "#E0AAFF" # Soft Pale Lavender
COLOR_DEEP_PURPLE = "#7B2CBF"  # Deep Royal Purple
COLOR_NEON_MAGENTA = "#FF007F" # High-Energy Magenta
COLOR_ROSE = "#FF85A1"         # Warm Rose Pink
COLOR_DARK_CARD = "#1D0433"    # Card Fill Violet
COLOR_BORDER = "#9D4EDD"       # Bright Border Purple
COLOR_WHITE = "#FFFFFF"        # Crisp Text White
COLOR_MUTED = "#D8B4F8"        # Muted Subtitle Lavender

def create_card(title_text, body_text_list, width=6.2, height=3.6, stroke_color=COLOR_BORDER):
    """Creates a beautifully styled, padded card with zero text overflow."""
    card_bg = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        fill_color=COLOR_DARK_CARD,
        fill_opacity=0.88,
        stroke_color=stroke_color,
        stroke_width=2.5
    )
    title = Text(title_text, font_size=20, weight=BOLD, color=COLOR_HOT_PINK)
    title.next_to(card_bg.get_top(), DOWN, buff=0.25)
    line = Line(
        card_bg.get_left() + RIGHT * 0.3,
        card_bg.get_right() + LEFT * 0.3,
        color=stroke_color,
        stroke_width=1.5
    ).next_to(title, DOWN, buff=0.18)
    
    body_group = VGroup()
    for text_line in body_text_list:
        bullet = Dot(color=COLOR_LAVENDER, radius=0.045)
        txt = Text(text_line, font_size=15, color=COLOR_WHITE)
        row = VGroup(bullet, txt).arrange(RIGHT, buff=0.15)
        body_group.add(row)
    body_group.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    body_group.next_to(line, DOWN, buff=0.22)
    return VGroup(card_bg, title, line, body_group)


# ==============================================================================
# SCENE 01: THE MONOLITH OF MODERN AI
# ==============================================================================
class Scene01_TheMonolith(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        # Header Badge
        header = Text("THE MONOLITH OF MODERN AI", font_size=32, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Frozen Architectures in the Era of Frontier Models", font_size=17, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left side: AI Researcher Character
        char_path = "assets/characters/ai_researcher.jpg"
        if os.path.exists(char_path):
            char_img = ImageMobject(char_path).scale_to_fit_height(4.4)
            char_frame = RoundedRectangle(
                corner_radius=0.15,
                width=char_img.width + 0.1,
                height=char_img.height + 0.1,
                stroke_color=COLOR_HOT_PINK,
                stroke_width=2.5,
                fill_color=COLOR_DARK_CARD,
                fill_opacity=0.3
            )
            char_grp = Group(char_frame, char_img).to_edge(LEFT, buff=0.6).shift(DOWN*0.3)
            char_label = Text("AI Theorist / Architect", font_size=14, color=COLOR_LIGHT_LAVENDER, weight=BOLD)
            char_label.next_to(char_grp, DOWN, buff=0.12)
            self.play(FadeIn(char_grp, shift=RIGHT*0.4), FadeIn(char_label), run_time=1.5)
        
        # Right side: The Transformer Monolith Stack & Stats Card
        card = create_card(
            "THE FROZEN ARCHITECTURE",
            [
                "Trillions of Tokens Optimized Once",
                "Weights Etched into Silicon at Inference",
                "Zero Dynamic Rewiring at Test-Time",
                "Invariant Softmax Attention Graph"
            ],
            width=6.0,
            height=2.8,
            stroke_color=COLOR_HOT_PINK
        ).to_edge(RIGHT, buff=0.6).shift(UP*0.7)
        
        # Paper Screenshot
        paper_path = "assets/papers/attention_paper.png"
        if os.path.exists(paper_path):
            paper_img = ImageMobject(paper_path).scale_to_fit_height(2.0)
            paper_border = RoundedRectangle(
                corner_radius=0.1,
                width=paper_img.width + 0.08,
                height=paper_img.height + 0.08,
                stroke_color=COLOR_LAVENDER,
                stroke_width=2
            )
            paper_grp = Group(paper_border, paper_img).next_to(card, DOWN, buff=0.3).align_to(card, RIGHT)
            paper_tag = Text("Vaswani et al. (2017) Attention Is All You Need", font_size=13, color=COLOR_MUTED)
            paper_tag.next_to(paper_grp, DOWN, buff=0.1)
            self.play(FadeIn(card, shift=UP*0.3), FadeIn(paper_grp, shift=UP*0.3), FadeIn(paper_tag), run_time=1.8)
        else:
            self.play(FadeIn(card, shift=UP*0.3), run_time=1.5)
            
        # Animated pulsing highlight
        pulse = Circle(radius=0.4, color=COLOR_HOT_PINK, stroke_width=3).move_to(card.get_corner(UR))
        self.play(pulse.animate.scale(2.5).set_opacity(0), run_time=1.5)
        self.wait(1.0)


# ==============================================================================
# SCENE 02: THE BIOLOGICAL DREAM
# ==============================================================================
class Scene02_TheBiologicalDream(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("THE BIOLOGICAL DREAM", font_size=32, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Living Synapses (~20 Watts) vs Static GPU Megawatts", font_size=17, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Center-Left: Biological Mind Character
        char_path = "assets/characters/neural_mind.jpg"
        if os.path.exists(char_path):
            mind_img = ImageMobject(char_path).scale_to_fit_height(4.2)
            mind_frame = Circle(radius=2.2, color=COLOR_HOT_PINK, stroke_width=2.5)
            mind_grp = Group(mind_frame, mind_img).to_edge(LEFT, buff=0.8).shift(DOWN*0.3)
            mind_label = Text("Living Neural Mind", font_size=15, color=COLOR_LIGHT_LAVENDER, weight=BOLD)
            mind_label.next_to(mind_grp, DOWN, buff=0.15)
            self.play(FadeIn(mind_grp, shift=RIGHT*0.4), FadeIn(mind_label), run_time=1.5)
            
        # Right side: Comparison Matrix
        bio_card = create_card(
            "BIOLOGICAL BRAIN",
            [
                "86 Billion Living Neurons",
                "100 Trillion Dynamic Synapses",
                "20 Watts Metabolic Budget",
                "Continuous Structural Plasticity"
            ],
            width=5.8,
            height=2.3,
            stroke_color=COLOR_LAVENDER
        ).to_edge(RIGHT, buff=0.6).shift(UP*1.1)
        
        gpu_card = create_card(
            "MODERN GPU CLUSTER",
            [
                "Megawatts of Grid Power",
                "Frozen Parameter Weights",
                "Dense Systolic Tensor Engines",
                "Zero Runtime Synaptic Growth"
            ],
            width=5.8,
            height=2.3,
            stroke_color=COLOR_HOT_PINK
        ).next_to(bio_card, DOWN, buff=0.3)
        
        self.play(FadeIn(bio_card, shift=LEFT*0.3), run_time=1.2)
        self.play(FadeIn(gpu_card, shift=LEFT*0.3), run_time=1.2)
        self.wait(1.5)


# ==============================================================================
# SCENE 03: THE SELF-ORGANIZING HYPOTHESIS
# ==============================================================================
class Scene03_TheSelfOrganizingHypothesis(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("THE SELF-ORGANIZING HYPOTHESIS", font_size=32, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Local Plasticity & Bottom-Up Structural Rewiring", font_size=17, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left side: Dynamic Animated Graph
        nodes = []
        edges = []
        node_coords = [
            (-3.8, 0.8, 0), (-2.6, 1.6, 0), (-1.4, 0.9, 0),
            (-3.9, -0.6, 0), (-2.7, -1.4, 0), (-1.5, -0.7, 0),
            (-2.7, 0.1, 0)
        ]
        graph_grp = VGroup()
        for pos in node_coords:
            dot = Dot(point=pos, radius=0.15, color=COLOR_LIGHT_LAVENDER)
            glow = Circle(radius=0.25, color=COLOR_HOT_PINK, stroke_width=1.5).move_to(pos)
            nodes.append(dot)
            graph_grp.add(glow, dot)
            
        edge_pairs = [(0, 1), (1, 2), (0, 3), (3, 4), (4, 5), (2, 5), (6, 0), (6, 2), (6, 4)]
        for i, j in edge_pairs:
            line = Line(node_coords[i], node_coords[j], color=COLOR_DEEP_PURPLE, stroke_width=2.5)
            edges.append(line)
            graph_grp.add(line)
            
        graph_label = Text("Dynamic Synaptic Graph", font_size=14, color=COLOR_MUTED)
        graph_label.next_to(graph_grp, DOWN, buff=0.25)
        
        self.play(FadeIn(graph_grp), FadeIn(graph_label), run_time=1.5)
        
        # Right side: Mathematical Formulations
        hebb_card = create_card(
            "HEBB'S POSTULATE (1949)",
            [
                "\"Neurons that fire together, wire together\"",
                "Local Correlation: Delta w_ij = eta * x_i * x_j",
                "Spike-Timing Plasticity (STDP)"
            ],
            width=6.0,
            height=2.2,
            stroke_color=COLOR_HOT_PINK
        ).to_edge(RIGHT, buff=0.6).shift(UP*1.1)
        
        oja_card = create_card(
            "OJA'S NORMALIZED RULE (1982)",
            [
                "Delta w = eta * y * (x - y * w)",
                "Weight Normalization without Global Loss",
                "Unsupervised Principal Subspace Extraction"
            ],
            width=6.0,
            height=2.2,
            stroke_color=COLOR_LAVENDER
        ).next_to(hebb_card, DOWN, buff=0.3)
        
        self.play(FadeIn(hebb_card, shift=UP*0.2), run_time=1.2)
        self.play(FadeIn(oja_card, shift=UP*0.2), run_time=1.2)
        
        # Pulsing synaptic firing animation
        for i, j in [(0, 1), (6, 2), (4, 5)]:
            pulse = Dot(color=COLOR_HOT_PINK, radius=0.08).move_to(node_coords[i])
            self.play(pulse.animate.move_to(node_coords[j]), run_time=0.6)
            self.remove(pulse)
        self.wait(1.0)


# ==============================================================================
# SCENE 04: THE MODULAR EMERGENCE PARADOX
# ==============================================================================
class Scene04_TheParadox(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("THE MODULAR EMERGENCE PARADOX", font_size=32, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Why Did Organic Graphs Fail While Brute Tensors Won?", font_size=17, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left: Self-Organizing Failure Card
        left_card = create_card(
            "SELF-ORGANIZING PROMISE",
            [
                "Promised: Organic emergent modularity",
                "Promised: Dynamic continuous adaptation",
                "Reality: Representational chaos & collapse",
                "Reality: Catastrophic interference at scale"
            ],
            width=5.8,
            height=3.4,
            stroke_color=COLOR_LAVENDER
        ).to_edge(LEFT, buff=0.7).shift(DOWN*0.2)
        
        # Right: Transformer Sentinel Character
        char_path = "assets/characters/transformer_monolith.jpg"
        if os.path.exists(char_path):
            trans_img = ImageMobject(char_path).scale_to_fit_height(3.8)
            trans_frame = RoundedRectangle(
                corner_radius=0.15,
                width=trans_img.width + 0.1,
                height=trans_img.height + 0.1,
                stroke_color=COLOR_HOT_PINK,
                stroke_width=2.5,
                fill_color=COLOR_DARK_CARD,
                fill_opacity=0.3
            )
            trans_grp = Group(trans_frame, trans_img).to_edge(RIGHT, buff=0.7).shift(DOWN*0.1)
            trans_label = Text("Transformer Sentinel (Emergent Circuits)", font_size=13, color=COLOR_LIGHT_LAVENDER, weight=BOLD)
            trans_label.next_to(trans_grp, DOWN, buff=0.12)
            self.play(FadeIn(left_card, shift=RIGHT*0.3), FadeIn(trans_grp, shift=LEFT*0.3), FadeIn(trans_label), run_time=1.5)
        else:
            self.play(FadeIn(left_card, shift=RIGHT*0.3), run_time=1.2)
            
        # Center Paradox Glyph
        paradox_box = RoundedRectangle(
            corner_radius=0.15,
            width=1.6,
            height=1.6,
            stroke_color=COLOR_NEON_MAGENTA,
            stroke_width=3,
            fill_color=COLOR_DARK_CARD,
            fill_opacity=0.95
        ).move_to(ORIGIN).shift(DOWN*0.2)
        q_mark = Text("?", font_size=60, weight=BOLD, color=COLOR_HOT_PINK).move_to(paradox_box.get_center())
        self.play(SpinInFromNothing(paradox_box), FadeIn(q_mark), run_time=1.2)
        self.wait(1.5)


# ==============================================================================
# SCENE 05: THEOREM 1: RANK COLLAPSE & THE OJA TRAP
# ==============================================================================
class Scene05_Theorem1_RankCollapse(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("THEOREM 1: RANK COLLAPSE & THE OJA TRAP", font_size=30, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Homogeneous Local Plasticity Collapses Dimensionality", font_size=16, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left side: Formal Mathematical Derivation Card
        math_card = create_card(
            "SPECTRAL COLLAPSE PROOF",
            [
                "dW/dt = eta * (y*x^T - alpha * y*y^T * W)",
                "Stationary Input Covariance: C = E[x * x^T]",
                "Asymptotic Attractor: lim W(t) -> v_1",
                "Effective Rank: Rank(W) -> 1 (Oja's Trap)",
                "Forfeits high-rank associative attention"
            ],
            width=6.2,
            height=3.6,
            stroke_color=COLOR_HOT_PINK
        ).to_edge(LEFT, buff=0.6).shift(DOWN*0.2)
        
        # Right side: Rank Decay Plot
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 16, 4],
            x_length=4.8,
            y_length=3.0,
            axis_config={"color": COLOR_LAVENDER, "stroke_width": 2}
        ).to_edge(RIGHT, buff=0.8).shift(UP*0.2)
        
        labels = axes.get_axis_labels(x_label=Text("Epochs", font_size=14, color=COLOR_MUTED), y_label=Text("Rank", font_size=14, color=COLOR_MUTED))
        
        # Rank curves: Transformer (stays high) vs SO-DRN (collapses)
        so_curve = axes.plot(lambda x: 15.0 / (1.0 + 1.2 * x) + 1.5, color=COLOR_HOT_PINK, stroke_width=3.5)
        tf_curve = axes.plot(lambda x: 14.5 - 0.05 * x, color=COLOR_LAVENDER, stroke_width=3.5)
        
        so_tag = Text("SO-DRN (Rank -> 2.1)", font_size=13, color=COLOR_HOT_PINK).next_to(so_curve.get_end(), RIGHT, buff=0.15)
        tf_tag = Text("Transformer (Rank = 14.6)", font_size=13, color=COLOR_LAVENDER).next_to(tf_curve.get_end(), UP, buff=0.1)
        
        self.play(FadeIn(math_card, shift=RIGHT*0.3), run_time=1.2)
        self.play(Create(axes), FadeIn(labels), run_time=1.2)
        self.play(Create(so_curve), Create(tf_curve), FadeIn(so_tag), FadeIn(tf_tag), run_time=1.8)
        self.wait(1.5)


# ==============================================================================
# SCENE 06: THEOREM 2: ROUTING BOUNDS & GRAPH LATENCY
# ==============================================================================
class Scene06_Theorem2_RoutingBounds(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("THEOREM 2: ROUTING EXPRESSIVITY & LATENCY", font_size=30, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Extremal Graph Diameter vs O(1) Attention Depth", font_size=16, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left side: Moore Bound Card
        moore_card = create_card(
            "THE MOORE BOUND",
            [
                "N Neurons with Maximum Degree d",
                "Diameter(G) >= Omega(log N / log d)",
                "Token routing requires O(log N) sequential hops",
                "Vanishing gradients across multi-hop paths",
                "Exponential signal latency & distortion"
            ],
            width=6.0,
            height=3.4,
            stroke_color=COLOR_LAVENDER
        ).to_edge(LEFT, buff=0.6).shift(DOWN*0.2)
        
        # Right side: Comparison Cards (Sparse Hops vs Attention Crossbar)
        sparse_card = create_card(
            "LOCAL GRAPH ROUTING",
            [
                "Diameter: Omega(log N)",
                "Latency: 20+ Sequential Recurrent Steps",
                "Signal: Attenuates exponentially per hop"
            ],
            width=5.8,
            height=2.0,
            stroke_color=COLOR_HOT_PINK
        ).to_edge(RIGHT, buff=0.6).shift(UP*0.8)
        
        attn_card = create_card(
            "TRANSFORMER SOFT ATTENTION",
            [
                "Diameter: Exactly 1 (All-to-All Crossbar)",
                "Latency: Single Parallelized Matrix Product",
                "Signal: Zero intermediate hop attenuation"
            ],
            width=5.8,
            height=2.0,
            stroke_color=COLOR_LIGHT_LAVENDER
        ).next_to(sparse_card, DOWN, buff=0.3)
        
        self.play(FadeIn(moore_card, shift=RIGHT*0.3), run_time=1.2)
        self.play(FadeIn(sparse_card, shift=UP*0.2), run_time=1.0)
        self.play(FadeIn(attn_card, shift=UP*0.2), run_time=1.0)
        self.wait(1.5)


# ==============================================================================
# SCENE 07: THEOREM 3: HARDWARE LOTTERY & CREDIT ASSIGNMENT
# ==============================================================================
class Scene07_Theorem3_HardwareBarrier(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("THEOREM 3: HARDWARE LOTTERY & CREDIT ASSIGNMENT", font_size=28, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Systolic Utilization vs Exponential Local Variance", font_size=16, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left side: The Bitter Lesson Screenshot
        bitter_path = "assets/papers/bitter_lesson.png"
        if os.path.exists(bitter_path):
            bitter_img = ImageMobject(bitter_path).scale_to_fit_height(3.2)
            bitter_border = RoundedRectangle(
                corner_radius=0.12,
                width=bitter_img.width + 0.1,
                height=bitter_img.height + 0.1,
                stroke_color=COLOR_HOT_PINK,
                stroke_width=2.5
            )
            bitter_grp = Group(bitter_border, bitter_img).to_edge(LEFT, buff=0.6).shift(DOWN*0.2)
            bitter_label = Text("Rich Sutton (2019) The Bitter Lesson", font_size=13, color=COLOR_MUTED)
            bitter_label.next_to(bitter_grp, DOWN, buff=0.12)
            self.play(FadeIn(bitter_grp, shift=RIGHT*0.3), FadeIn(bitter_label), run_time=1.5)
            
        # Right side: Hardware & Variance Breakdown
        hw_card = create_card(
            "THE HARDWARE LOTTERY",
            [
                "Dense Tensor Cores: >90% Compute FLOPS",
                "Dynamic Sparse Graphs: <8% Cache Thrashing",
                "Pointer indirection destroys memory bandwidth"
            ],
            width=6.0,
            height=2.0,
            stroke_color=COLOR_LAVENDER
        ).to_edge(RIGHT, buff=0.6).shift(UP*0.8)
        
        var_card = create_card(
            "CREDIT ASSIGNMENT BARRIER",
            [
                "Backprop: Analytical gradient in 1 reverse pass",
                "Local Plasticity: Node perturbation variance",
                "Variance Explosion: Var(g) proportional to T * sigma^2"
            ],
            width=6.0,
            height=2.0,
            stroke_color=COLOR_HOT_PINK
        ).next_to(hw_card, DOWN, buff=0.3)
        
        self.play(FadeIn(hw_card, shift=UP*0.2), run_time=1.2)
        self.play(FadeIn(var_card, shift=UP*0.2), run_time=1.2)
        self.wait(1.5)


# ==============================================================================
# SCENE 08: EMPIRICAL DIAGNOSTIC BENCHMARK
# ==============================================================================
class Scene08_EmpiricalBenchmarks(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("EMPIRICAL BENCHMARK: THE MOMENT OF TRUTH", font_size=28, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("In-Context Associative Recall: SO-DRN vs Transformer", font_size=16, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left side: Benchmark Plot Image
        plot_path = "benchmarks/benchmark_comparison.png"
        if os.path.exists(plot_path):
            plot_img = ImageMobject(plot_path).scale_to_fit_height(3.4)
            plot_border = RoundedRectangle(
                corner_radius=0.12,
                width=plot_img.width + 0.1,
                height=plot_img.height + 0.1,
                stroke_color=COLOR_LAVENDER,
                stroke_width=2.5
            )
            plot_grp = Group(plot_border, plot_img).to_edge(LEFT, buff=0.6).shift(DOWN*0.2)
            plot_label = Text("Empirical Training Trajectory (100 Epochs)", font_size=13, color=COLOR_MUTED)
            plot_label.next_to(plot_grp, DOWN, buff=0.12)
            self.play(FadeIn(plot_grp, shift=RIGHT*0.3), FadeIn(plot_label), run_time=1.5)
            
        # Right side: Results HUD
        hud_card = create_card(
            "DIAGNOSTIC TEST METRICS",
            [
                "TASK: In-Context Associative Key-Value Recall",
                "SO-DRN Effective Rank: 2.1 / 64 (Collapsed)",
                "SO-DRN Accuracy: 7.7% (Flatlined)",
                "Transformer Effective Rank: 14.56 / 64 (Full)",
                "Transformer Accuracy: 92.3% (Solved)"
            ],
            width=6.0,
            height=3.4,
            stroke_color=COLOR_HOT_PINK
        ).to_edge(RIGHT, buff=0.6).shift(DOWN*0.2)
        
        self.play(FadeIn(hud_card, shift=LEFT*0.3), run_time=1.5)
        self.wait(1.5)


# ==============================================================================
# SCENE 09: WHAT FRONTIER LABS DISCOVERED
# ==============================================================================
class Scene09_FrontierLabs(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("WHAT FRONTIER LABS DISCOVERED", font_size=30, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Hardware-Aligned Adaptability: DeepSeek-V3 & MoE Routing", font_size=16, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left side: DeepSeek-V3 Paper Screenshot
        deepseek_path = "assets/papers/deepseek_paper.png"
        if os.path.exists(deepseek_path):
            ds_img = ImageMobject(deepseek_path).scale_to_fit_height(3.2)
            ds_border = RoundedRectangle(
                corner_radius=0.12,
                width=ds_img.width + 0.1,
                height=ds_img.height + 0.1,
                stroke_color=COLOR_HOT_PINK,
                stroke_width=2.5
            )
            ds_grp = Group(ds_border, ds_img).to_edge(LEFT, buff=0.6).shift(DOWN*0.2)
            ds_label = Text("DeepSeek-AI (2024) DeepSeek-V3 Technical Report", font_size=13, color=COLOR_MUTED)
            ds_label.next_to(ds_grp, DOWN, buff=0.12)
            self.play(FadeIn(ds_grp, shift=RIGHT*0.3), FadeIn(ds_label), run_time=1.5)
            
        # Right side: Architectural Breakthrough Cards
        moe_card = create_card(
            "FINE-GRAINED MOE ROUTING",
            [
                "256 Routing Experts + 2 Shared Experts",
                "Dynamic Top-8 Expert Dispatch per Token",
                "Conditional Compute without Matrix Thrashing"
            ],
            width=6.0,
            height=2.0,
            stroke_color=COLOR_LAVENDER
        ).to_edge(RIGHT, buff=0.6).shift(UP*0.8)
        
        mla_card = create_card(
            "MULTI-HEAD LATENT ATTENTION",
            [
                "Low-Rank Key-Value Latent Compression",
                "Dynamic Runtime Decompression Vector",
                "Preserves Full-Rank Attention Expressivity"
            ],
            width=6.0,
            height=2.0,
            stroke_color=COLOR_HOT_PINK
        ).next_to(moe_card, DOWN, buff=0.3)
        
        self.play(FadeIn(moe_card, shift=UP*0.2), run_time=1.2)
        self.play(FadeIn(mla_card, shift=UP*0.2), run_time=1.2)
        self.wait(1.5)


# ==============================================================================
# SCENE 10: THE 10-YEAR FRONTIER
# ==============================================================================
class Scene10_The10YearFrontier(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        
        header = Text("THE 10-YEAR FRONTIER: HYBRID INTELLIGENCE", font_size=28, weight=BOLD, color=COLOR_HOT_PINK)
        sub = Text("Unifying Global Attention with Continuous Structural Plasticity", font_size=16, color=COLOR_LAVENDER)
        title_grp = VGroup(header, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        self.play(FadeIn(title_grp, shift=DOWN*0.3), run_time=1.2)
        
        # Left side: Character Triad Assembly
        chars_grp = Group()
        c1 = "assets/characters/ai_researcher.jpg"
        c2 = "assets/characters/neural_mind.jpg"
        c3 = "assets/characters/transformer_monolith.jpg"
        if os.path.exists(c1) and os.path.exists(c2) and os.path.exists(c3):
            im1 = ImageMobject(c1).scale_to_fit_height(1.8)
            im2 = ImageMobject(c2).scale_to_fit_height(1.8)
            im3 = ImageMobject(c3).scale_to_fit_height(1.8)
            
            f1 = RoundedRectangle(corner_radius=0.1, width=im1.width+0.05, height=im1.height+0.05, stroke_color=COLOR_HOT_PINK, stroke_width=2)
            f2 = RoundedRectangle(corner_radius=0.1, width=im2.width+0.05, height=im2.height+0.05, stroke_color=COLOR_LAVENDER, stroke_width=2)
            f3 = RoundedRectangle(corner_radius=0.1, width=im3.width+0.05, height=im3.height+0.05, stroke_color=COLOR_LIGHT_LAVENDER, stroke_width=2)
            
            g1 = Group(f1, im1)
            g2 = Group(f2, im2)
            g3 = Group(f3, im3)
            
            chars_col = Group(g1, g2, g3).arrange(DOWN, buff=0.18).to_edge(LEFT, buff=0.8).shift(DOWN*0.3)
            triad_label = Text("The Grand Synthesis", font_size=13, color=COLOR_MUTED, weight=BOLD)
            triad_label.next_to(chars_col, DOWN, buff=0.12)
            self.play(FadeIn(chars_col, shift=RIGHT*0.3), FadeIn(triad_label), run_time=1.8)
            
        # Right side: 4 Future Pillars Card
        pillars_card = create_card(
            "THE FOUR FUTURE PILLARS",
            [
                "1. Neuromorphic Silicon: In-memory analog crossbars",
                "2. Fast-Weights & TTT: Runtime localized meta-gradients",
                "3. Liquid State Networks: Continuous-time adaptive ODEs",
                "4. Self-Compiling Graphs: Autonomous cognitive agents"
            ],
            width=6.4,
            height=3.4,
            stroke_color=COLOR_HOT_PINK
        ).to_edge(RIGHT, buff=0.6).shift(DOWN*0.2)
        
        self.play(FadeIn(pillars_card, shift=LEFT*0.3), run_time=1.5)
        
        # Outro Badge
        outro_badge = Text("The future belongs to living, self-adapting cognitive architectures.", font_size=15, color=COLOR_ROSE, slant=ITALIC)
        outro_badge.next_to(pillars_card, DOWN, buff=0.25)
        self.play(FadeIn(outro_badge), run_time=1.2)
        self.wait(1.5)
