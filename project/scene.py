from manim import *
import math

CROSS_SEC_INT = 1.18 * math.sqrt(2) / 2.0
Z_INT = 1.02


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


# z = f(x) = f(y) ITO z is f(z) = 2sqrt(51-50z)/sqrt(293)
def fz(z):
    return 2.0 * math.sqrt(51.0 - 50.0 * z) / math.sqrt(293)


class Intro(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-1, 1, 0.2],
            y_range=[-1, 1, 0.2],
            z_range=[0, 1.1, 0.1],
            x_length=12,
            y_length=12,
            z_length=5,
        )
        axes.add_coordinates()

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y").shift(UP * 1.8)
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)

        # setup for z = f(x) = f(y)
        x_graph = axes.plot_parametric_curve(
            lambda t: np.array(
                [
                    t,
                    0,
                    -1.465 * t**2 + 1.02,
                ]
            ),
            t_range=np.array([-CROSS_SEC_INT, CROSS_SEC_INT]),
            color=GREEN_B,
        )
        y_graph = axes.plot_parametric_curve(
            lambda t: np.array(
                [
                    0,
                    t,
                    -1.465 * t**2 + 1.02,
                ]
            ),
            t_range=np.array([-CROSS_SEC_INT, CROSS_SEC_INT]),
            color=GREEN_B,
        )

        z = ValueTracker(0)

        # square cross section
        quad_one = always_redraw(
            lambda: Line3D(
                start=axes.c2p(fz(z.get_value()), 0, z.get_value()),
                end=axes.c2p(0, fz(z.get_value()), z.get_value()),
                color=PURPLE_A,
            )
        )
        quad_two = always_redraw(
            lambda: Line3D(
                start=axes.c2p(-fz(z.get_value()), 0, z.get_value()),
                end=axes.c2p(0, fz(z.get_value()), z.get_value()),
                color=PURPLE_A,
            )
        )
        quad_three = always_redraw(
            lambda: Line3D(
                start=axes.c2p(-fz(z.get_value()), 0, z.get_value()),
                end=axes.c2p(0, -fz(z.get_value()), z.get_value()),
                color=PURPLE_A,
            )
        )
        quad_four = always_redraw(
            lambda: Line3D(
                start=axes.c2p(fz(z.get_value()), 0, z.get_value()),
                end=axes.c2p(0, -fz(z.get_value()), z.get_value()),
                color=PURPLE_A,
            )
        )
        sqr_sec = VGroup(quad_one, quad_two, quad_three, quad_four)

        dot = always_redraw(
            lambda: Dot(
                point=axes.c2p(fz(z.get_value()), 0, 0),
                color=RED,
            )
        )
        r_line = always_redraw(
            lambda: axes.get_horizontal_line(
                axes.c2p(fz(z.get_value()), 0, 0),
                color=ORANGE,
                stroke_width=10.0,
                line_func=Line,
            ),
        )
        r_obj = always_redraw(
            lambda: MathTex("r", color=ORANGE).next_to(r_line, DOWN, buff=0.8)
        )
        r_val_obj = always_redraw(
            lambda: MathTex(f"r={round(fz(z.get_value()), 4)}", color=ORANGE).to_edge(
                UR, buff=0.5
            )
        )
        z_val_obj = always_redraw(
            lambda: MathTex(
                f"z={round(z.get_value(), 4)}",
                color=BLUE,
            ).next_to(r_val_obj, DOWN, buff=0.5)
        )

        self.next_section("Intro", skip_animations=True)
        self.set_camera_orientation(zoom=0.5)
        self.play(FadeIn(axes), FadeIn(labels))
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=0.75, run_time=1.5)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(Create(x_graph), Create(y_graph))
        self.play(Create(sqr_sec))
        self.wait(0.5)
        self.play(z.animate.set_value(Z_INT))
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.5, run_time=0.5)
        self.play(z.animate.set_value(0))
        self.wait(0.5)
        self.next_section("Cross Section")
        self.play(Create(dot), Create(r_line), Create(r_obj))
        self.play(Create(r_val_obj), Create(z_val_obj))
        self.wait(0.5)
        self.play(z.animate.set_value(Z_INT), run_time=0.5)
        # self.play(FadeOut(rendered, lag_ratio=0.0), run_time=0.5)


class TopView(Scene):
    def construct(self):
        # scene setup
        sqr = Square(side_length=4.0)
        sqr.rotate(45 * DEGREES)

        line = Line(start=sqr.get_center(), end=sqr.get_right(), color=ORANGE)
        r_obj = MathTex("r", color=ORANGE).next_to(line, DOWN, buff=0.2)

        self.play(FadeIn(sqr))
        self.play(Create(line), FadeIn(r_obj))
