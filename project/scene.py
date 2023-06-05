from manim import *
import math

CROSS_SEC_INT = 1.18 * math.sqrt(2) / 2.0
Z_INT = 1.02


# z = f(x) = f(y) ITO z is f(z) = 2sqrt(51-50z)/sqrt(293)
def fz(z):
    return 2.0 * math.sqrt(51.0 - 50.0 * z) / math.sqrt(293)


class MainView(ThreeDScene):
    def construct(self):
        self.next_section("Graph Setup", skip_animations=True)

        # graph setup
        axis_config = {
            "x_range": (-1, 1, 0.2),
            "y_range": (-1, 1, 0.2),
            "z_range": (0, 1.1, 0.1),
            "x_length": 11,
            "y_length": 11,
            "z_length": 7,
        }
        axes = ThreeDAxes(**axis_config)
        # ax = ThreeDAxes()
        # x_labels = range(-4, 5)
        # z_labels = range(-4, 4, 2)
        # ax.add_coordinates(x_labels, None, z_labels)  # default y labels, custom x & z labels
        # ax.add_coordinates(x_labels)  # only x labels
        x_axis = axes.get_x_axis()
        x_label = axes.get_x_axis_label("x")
        y_axis = axes.get_y_axis()
        y_label = axes.get_y_axis_label("y")
        z_axis = axes.get_z_axis()
        z_label = axes.get_z_axis_label("z")

        # axes.add_coordinates(
        #     np.linspace(-1, 1, 10, endpoint=False),
        #     np.linspace(-1, 1, 10, endpoint=False),
        #     range(0),
        # )
        graph = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        self.add(graph)

        # axes setup
        # make z-axis face camera
        z_axis.rotate(90 * DEGREES, [0.0, 0.0, 1.0])
        # needed since z begins on the XY plane
        z_label.rotate(90 * DEGREES, [1.0, 0.0, 0.0])
        z_label.rotate(180 * DEGREES, [0.0, 1.0, 0.0])

        # orient labels
        x_label.move_to([6.0, 0.0, 0.0])
        y_label.move_to([0.0, 6.0, 0.0])
        z_label.move_to([0.0, 0.0, 7.5])
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        # don't want z-label visible at the start
        self.remove(z_label)

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

        # initial cam orientation
        self.set_camera_orientation(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            gamma=0 * DEGREES,
            frame_center=axes.get_center(),
            zoom=0.6,
        )

        # shift to 3D view
        self.wait()
        self.move_camera(
            phi=75 * DEGREES,
            theta=25 * DEGREES,
            zoom=0.6,
            added_anims=[
                Write(z_label),
            ],
        )
        self.wait()

        self.next_section("Function Visualization", skip_animations=True)

        """
            Note that the base of the tent is a square. This square can be defined by two identical 
            parametric curves, with one in the XZ plane and the other in the YZ plane. If we were able
            to get every square cross section with respect to the z-axis, then we would be able to get
            the volume of the tent. In other words, we want to integrate some function A(z) from z=0
            to z=tent_height such that A(z) gets us the area of the square cross section at some 
            value z.
            
        """

        self.play(Create(x_graph), Create(y_graph))
        self.begin_ambient_camera_rotation(0.1)
        self.wait(5)

        self.next_section("Cross Section Visualization", skip_animations=True)

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

        self.play(Create(sqr_sec, lag_ratio=0.0))
        self.wait(2.0)
        self.play(z.animate.set_value(Z_INT), run_time=5.0)
        self.play(FadeOut(sqr_sec))
        self.wait(5)

        self.next_section("XY", skip_animations=True)

        """
            Well, how can we do that? Let's first look at each square cross section from the top down,
            such that we will be looking at the XY plane. Let's draw in a line r from the
            center of the square to one of its corners such that r is the square's radius. Now, let's
            play the animation from before, increasing z from 0 to the tent height. Notice the clear
            relationship between r and z: they are inversely proportional. Why is this useful? Well
            that's because we can directly relate the square's radius to its area! {go to TopView}
        """

        # showing radius in top view
        dot = always_redraw(
            lambda: Dot3D(
                point=axes.c2p(fz(z.get_value()), 0, z.get_value()),
                color=RED,
                radius=0.1,
            )
        )
        r_line = always_redraw(
            lambda: axes.get_horizontal_line(
                axes.c2p(fz(z.get_value()), 0, 0),
                color=ORANGE,
                stroke_width=5.0,
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
        self.add_fixed_orientation_mobjects(r_val_obj, z_val_obj)
        top_render = VGroup(dot, r_line, r_obj, r_val_obj, z_val_obj)

        self.stop_ambient_camera_rotation()
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            gamma=0 * DEGREES,
            added_anims=[
                FadeOut(z_axis, z_label),
                Rotate(y_label, -90 * DEGREES, [0.0, 0.0, 1.0]),
            ],
            zoom=0.6,
        )
        self.play(z.animate.set_value(0), run_time=0.1)
        self.wait(0.1)
        self.play(Write(sqr_sec), run_time=2.0)
        self.wait()
        self.play(Create(top_render))
        self.wait(5)

        self.next_section("XY change z", skip_animations=True)

        """
            {Transition to TopView}
        """

        self.play(z.animate.set_value(Z_INT), run_time=3.0)

        self.next_section("XZ", skip_animations=True)

        """
            Again, we want the relationship, or in other words, a function relating z and the area, 
            since we are basically integrating A(z) = 2 * r(z)^2. How can we find this function? Well 
            first, let's orient ourselves on the XZ plane, such that we are looking at parametric 
            function on the XZ plane. 
            {go to SideView}
        """

        # go to XZ plane
        self.move_camera(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            gamma=0 * DEGREES,
            added_anims=[
                FadeOut(y_axis, y_label),
                FadeOut(top_render, sqr_sec),
                FadeIn(z_axis, z_label),
                Rotate(x_axis, 90 * DEGREES, [1.0, 0.0, 0.0]),
                # Rotate(z_axis, 90 * DEGREES, [0.0, 0.0, 1.0]),
            ],
            zoom=0.6,
        )
        self.wait(5)

        self.next_section("Complete 3D Visualization")

        """
            If we go back into 3D, we can see all these components in play. Notice that as the value of
            z increases, r decreases and thus area decreases as well, which our new equation now models.
        """

        self.play(z.animate.set_value(0), run_time=0.1)
        self.wait(0.1)

        trace_lines = always_redraw(
            lambda: axes.get_lines_to_point(
                axes.c2p(fz(z.get_value()), 0, z.get_value())
            ),
        )
        # area_obj = always_redraw(
        #     lambda: MathTex(
        #         f"A({z.get_value()})={2 * fz(z.get_value() ** 2)}", color=GREEN
        #     ),
        # ).next_to(z_val_obj, DOWN, buff=0.5)

        # area_val, z val, r val
        # r_val_obj.move_to([0.0, 8.0, 4.0])
        # z_val_obj.move_to([])
        # r_val_obj.rotate(90 * DEGREES, [1.0, 0.0, 0.0])
        # z_val_obj.rotate(90 * DEGREES, [1.0, 0.0, 0.0])

        self.move_camera(
            phi=75 * DEGREES,
            theta=-25 * DEGREES,
            added_anims=[
                FadeIn(y_axis, y_label),
                Rotate(x_axis, -90 * DEGREES, [1.0, 0.0, 0.0]),
                # FadeIn(r_val_obj, z_val_obj),
                # Rotate(r_val_obj, 90 * DEGREES, [1.0, 0.0, 0.0]),
                # Rotate(z_val_obj, 90 * DEGREES, [1.0, 0.0, 0.0])
            ],
            zoom=0.6,
        )
        self.wait()
        self.play(FadeIn(dot, r_line, r_obj, trace_lines, sqr_sec))
        self.play(z.animate.set_value(Z_INT), run_time=3)
        self.wait()


class TopView(Scene):
    def construct(self):
        # scene setup
        sqr = Square(side_length=4.0).shift(UP * 0.5)
        sqr.rotate(45 * DEGREES)

        r_line = Line(start=sqr.get_center(), end=sqr.get_right(), color=BLUE)
        r_obj = MathTex("r", color=BLUE).next_to(r_line, DOWN, buff=0.2)
        d_line = Line(start=sqr.get_top(), end=sqr.get_bottom(), color=RED)
        d_obj = MathTex("2r", color=RED).next_to(d_line, LEFT, buff=0.2)

        sqr_eqn = MathTex(
            "A = \\frac{1}{2} r \\times 2r = 2r^{2}", color=PURPLE
        ).next_to(sqr, DOWN, buff=0.2)

        self.play(FadeIn(sqr))
        self.play(Create(r_line), FadeIn(r_obj))
        self.wait()
        self.play(Create(d_line), FadeIn(d_obj))
        self.wait()
        self.play(DrawBorderThenFill(sqr_eqn))


class SideView(Scene):
    def construct(self):
        """
        We didn't mention how the function was defined at first, but it is z = -1.465x^2 + 1.02.
        And in the YZ plane, it is z = -1.465y^2 + 1.02. We found this by finding the length of the
        tent, which was 1.18 m. This was the hypotenuse of a 45-45-90 triangle. We decided to make the
        corners of the tent's square base (or the legs of the triangle) our XY axes, so that meant
        that the intercepts were all at plus or minus 1.18/sqrt(2).

        Based on these intercepts, our equations could be found by doing
        f(x) = a * (x + 1.18/sqrt(2)) * (x - 1.18/sqrt(2)) and substituting the y-intercept (0, 1.02 m),
        which is the height. The a value of -1.465 is then substituted back into this equation. Upon rearranging,
        you get -1.465x^2 + 1.02.

        In other words, that means z = f(x) = f(y). Since the graph of f(x) and f(y) are basically the same,
        we'll only look at f(x). If we play the animation again, you can see that r = x, hence z is dependent on r.
        {video ends}
        Thus if we solve z = f(x) in terms of z, we'll get a function where r is dependent on z.
        With this new function r = x = f(z), we are able to create our area function A(z) = 2 * r(z)^2.
        {go to MainView}
        """
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


class AreaGraph(MovingCameraScene):
    def construct(self):
        """
        Here is the graph of A(z). If we take the integral of A(z),
        we get our area.
        """

        # scene setup
        axes = Axes(
            x_range=[0, 1.1, 0.1],
            x_length=12,
            y_range=[0, 1.5, 0.2],
            y_length=12,
        )
        axes.add_coordinates()

        # graph setup
        z_label = axes.get_x_axis_label("z")
        fz_label = axes.get_y_axis_label("f(z)")
        axes_labels = VGroup(z_label, fz_label)

        z_label.move_to([6.5, -6.0, 0.0])
        fz_label.move_to([-5.0, 5.5, 0.0])

        # function setup
        fz_graph = axes.plot(
            lambda x: 2.0 * math.sqrt(51.0 - 50.0 * x) / math.sqrt(293),
            x_range=[0, Z_INT],
            color=RED_A,
        )
        az_graph = axes.plot(
            lambda x: 2.0 * fz(float(x)) ** 2.0, x_range=[0, Z_INT], color=BLUE_A
        )

        fz_graph_label = (
            MathTex("r(z)", color=RED_A)
            .scale(1.5)
            .next_to(axes.c2p(0.8, 0.4, 0.0), RIGHT, buff=0.4)
        )
        az_graph_label = (
            MathTex("A(z)", color=BLUE_A).scale(1.5).next_to(axes.c2p(0.3, 1.0, 0.0))
        )
        az_integral_label = (
            MathTex("\int_0^{1.02} \! A(z) \, \mathrm{d}z \\approx 0.7102")
            .scale(1.2)
            .next_to(axes.c2p(0.4, 1.0, 0.0))
        )

        x_int = VGroup(
            Dot(point=axes.c2p(Z_INT, 0, 0), color=BLUE),
            MathTex("(1.02, 0)").next_to(axes.c2p(Z_INT, 0, 0), UP, buff=0.2),
        )

        area = axes.get_area(graph=az_graph, x_range=[0, Z_INT], color=[BLUE, YELLOW])

        self.camera.frame_center = axes.get_center()
        self.camera.frame.scale(2.0)

        self.play(DrawBorderThenFill(axes), run_time=2)
        self.play(DrawBorderThenFill(axes_labels))
        self.play(Create(fz_graph), run_time=2)
        self.play(Create(fz_graph_label))
        self.play(Create(az_graph), run_time=2)
        self.play(Create(az_graph_label))
        self.play(Write(x_int))
        self.play(FadeIn(area), run_time=2)
        self.play(TransformMatchingTex(az_graph_label, az_integral_label))
        self.wait()
