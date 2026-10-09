from manim import *

class TestMath(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        eq = MathTex(r"\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V")
        self.play(Write(eq), run_time=1.5)
        self.wait(0.5)
