from manim import *

class TestTextMath(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        title = Text("Attention(Q, K, V) = softmax(Q·Kᵀ / √d) · V", font="Menlo", font_size=32, color="#58C4DD")
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
