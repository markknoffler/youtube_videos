from manim import *

class HelloScene(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        title = Text("Self-Adapting AI", font="Menlo", font_size=40, color="#58C4DD")
        self.play(FadeIn(title), run_time=1)
        self.wait(0.5)
