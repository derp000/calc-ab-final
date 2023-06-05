from manim import *
import math

CROSS_SEC_INT = 1.18 * math.sqrt(2) / 2.0


class SideView(Scene):
    def construct(self):
        # scene setup
        axes = Axes(
            x_range=[-1, 1, 0.2], x_length=12, y_range=[0, 1.1, 0.1], y_length=5
        )
        axes.add_coordinates()

        # graph setup
        x_label = axes.get_x_axis_label("x")
        z_label = axes.get_y_axis_label("z")
        axes_labels = VGroup(x_label, z_label)

        # function setup
        cross_sec_graph = axes.plot(
            lambda x: -1.465 * x**2 + 1.02,
            x_range=[-CROSS_SEC_INT, CROSS_SEC_INT],
            color=GREEN_B,
        )
        x_r_int = VGroup(
            Dot(point=axes.c2p(CROSS_SEC_INT, 0, 0), color=BLUE),
            MathTex("(1.18 \\frac{ \sqrt{2} }{2}, 0)")
            .scale(0.75)
            .next_to(axes.c2p(CROSS_SEC_INT, 0, 0), UP, buff=0.2),
        )
        x_l_int = VGroup(
            Dot(point=axes.c2p(-CROSS_SEC_INT, 0, 0), color=BLUE),
            MathTex("(-1.18 \\frac{ \sqrt{2} }{2}, 0)")
            .scale(0.75)
            .next_to(axes.c2p(-CROSS_SEC_INT, 0, 0), UP, buff=0.2),
        )
        y_int = VGroup(
            Dot(point=axes.c2p(0, 1.02, 0), color=BLUE),
            MathTex("(0, 1.02)")
            .scale(0.75)
            .next_to(axes.c2p(0, 1.02, 0), RIGHT, buff=0.2),
        )
        points = VGroup(x_r_int, x_l_int, y_int)
        func = MathTex("f(x) = -1.465x^{2} + 1.02").next_to(axes, UP, buff=0.4)

        # dot and liens tracing the function
        x = ValueTracker(CROSS_SEC_INT)
        dot = always_redraw(
            lambda: Dot(
                point=axes.c2p(
                    x.get_value(), cross_sec_graph.underlying_function(x.get_value()), 0
                ),
                color=RED,
            )
        )
        lines = always_redraw(
            lambda: axes.get_lines_to_point(
                axes.c2p(
                    x.get_value(), cross_sec_graph.underlying_function(x.get_value()), 0
                )
            ),
        )
        r_line = always_redraw(
            lambda: axes.get_horizontal_line(
                axes.c2p(x.get_value(), 0, 0),
                color=ORANGE,
                stroke_width=10.0,
                line_func=Line,
            ),
        )
        r_tex = always_redraw(
            lambda: MathTex("r", color=ORANGE).next_to(r_line, DOWN, buff=0.8)
        )
        r = always_redraw(
            lambda: MathTex(f"r={round(x.get_value(), 4)}", color=ORANGE).to_edge(
                UR, buff=2.0
            )
        )
        z = always_redraw(
            lambda: MathTex(
                f"z={round(cross_sec_graph.underlying_function(x.get_value()), 4)}",
                color=BLUE,
            ).next_to(r, DOWN, buff=0.5)
        )

        self.play(DrawBorderThenFill(axes), run_time=2)
        self.play(DrawBorderThenFill(axes_labels))
        self.play(Create(cross_sec_graph), Write(func), run_time=2)
        self.play(Create(points, lag_ratio=0), run_time=3)
        self.wait()
        self.play(Create(dot), Create(lines), Create(r_line), Create(r_tex))
        self.play(Create(r), Create(z))
        self.wait()
        self.play(x.animate.set_value(0), run_time=10)
