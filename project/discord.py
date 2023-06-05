from manim import *


class Graph3D(ThreeDScene):
    def construct(self):
        self.next_section()
        axis_config = {
            "x_range": (-5.5, 5.5),
            "y_range": (-5.5, 5.5),
            "z_range": (-3.5, 3.5),
            "x_length": 11,
            "y_length": 11,
            "z_length": 7,
        }
        axes = ThreeDAxes(**axis_config)
        x_axis = axes.get_x_axis()
        x_label = axes.get_x_axis_label("x")
        y_axis = axes.get_y_axis()
        y_label = axes.get_y_axis_label("y")
        z_axis = axes.get_z_axis()
        z_label = axes.get_z_axis_label("z")

        self.add(x_axis, y_axis, z_axis, x_label, y_label, z_label)

        z_axis.rotate(90 * DEGREES, [0.0, 0.0, 1.0])
        # z_label.rotate(90 * DEGREES, [1.0, 0.0, 0.0])
        # z_label.rotate(180 * DEGREES, [0.0, 1.0, 0.0])
        x_label.move_to([6.0, 0.0, 0.0])
        y_label.move_to([0.0, 6.0, 0.0])
        z_label.move_to([0.0, 0.0, 2.0])
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)

        self.remove(z_label)

        surface1 = Surface(
            lambda u, v: axes.c2p(u, v, 0.5 * np.sin(u) * 0.5 * np.cos(v)),
            u_range=[-4, 4],
            v_range=[-4, 4],
            checkerboard_colors=[BLUE_C, RED_E],
            stroke_color=GOLD,
            stroke_width=2,
            fill_opacity=0.5,
        )

        surface2 = Surface(
            lambda u, v: axes.c2p(u, v, np.sin(u) * np.cos(v)),
            u_range=[-4, 4],
            v_range=[-4, 4],
            checkerboard_colors=[RED_E, BLUE_C],
            stroke_color=GOLD,
            stroke_width=2,
            fill_opacity=0.5,
        )

        self.set_camera_orientation(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            gamma=0 * DEGREES,
            frame_center=axes.get_center(),
            zoom=0.6,
        )

        self.wait()
        self.move_camera(
            phi=75 * DEGREES,
            theta=25 * DEGREES,
            zoom=0.6,
            added_anims=[
                Write(z_label),
                Rotate(y_axis, 90 * DEGREES, [0.0, 1.0, 0.0]),
            ],
        )
        self.wait()
        self.next_section(skip_animations=True)
        self.play(Write(surface1, run_time=2))
        self.wait()
        self.play(ReplacementTransform(surface1, surface2), run_time=2)
        self.wait()
        self.move_camera(
            phi=90 * DEGREES,
            theta=(-90 + 0) * DEGREES,
            gamma=0 * DEGREES,
            added_anims=[
                FadeOut(y_axis, y_label),
                Rotate(x_axis, 90 * DEGREES, [1.0, 0.0, 0.0]),
                Rotate(z_axis, 90 * DEGREES, [0.0, 0.0, 1.0]),
            ],
            zoom=0.6,
        )
        self.wait()
        self.begin_ambient_camera_rotation(rate=0.1, about="theta")
        self.wait(3)
        self.stop_ambient_camera_rotation(about="theta")
        self.wait(0.5)
        self.play(FadeOut(surface2, scale=0.5))
        self.wait()
