import numpy as np
from manim import *


class PCAAnimation(ThreeDScene):
    def get_perpendicular_projection(self, dot_pos, centroid_pos, angle):
        regression_direction = np.array([np.cos(angle), np.sin(angle), 0])
        centroid_to_dot = dot_pos - centroid_pos
        projection_length = np.dot(centroid_to_dot, regression_direction)
        return centroid_pos + projection_length * regression_direction

    def calculate_total_distance(self, dots, centroid_pos, angle):
        total_distance = 0
        for dot in dots:
            dot_pos = dot.get_center()
            projection_point = self.get_perpendicular_projection(
                dot_pos, centroid_pos, angle
            )
            distance = np.linalg.norm(dot_pos - projection_point)
            total_distance += distance
        return total_distance

    def construct(self):
        # camera setup
        # self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        # self.begin_3dillusion_camera_rotation(rate=0.3)
        # set camera to an orthographic view
        self.set_camera_orientation(focal_distance=9999999999)

        self.wait(1)

        axes_2d = ThreeDAxes(
            x_range=[0, 5],
            y_range=[0, 5],
            z_range=[-1, 1],
            x_length=5,
            y_length=5,
            z_length=2,
        )
        axes_2d.shift(IN * 2)

        self.play(Create(axes_2d))

        # create random points between (0, 0, 0) and (5, 5, 5)
        points = [
            axes_2d.c2p(1.1, 1.2, 2.3),
            axes_2d.c2p(1.6, 1.0, -0.8),
            axes_2d.c2p(1.0, 1.7, 2.8),
            axes_2d.c2p(1.8, 1.1, -0.2),
            axes_2d.c2p(1.3, 1.9, 2.1),
            axes_2d.c2p(1.9, 1.3, -0.9),
            axes_2d.c2p(1.2, 1.5, 2.9),
            axes_2d.c2p(3.2, 3.1, -0.3),
            axes_2d.c2p(3.9, 3.8, 2.2),
            axes_2d.c2p(3.1, 3.9, -0.7),
            axes_2d.c2p(3.8, 3.2, 2.7),
            axes_2d.c2p(3.3, 3.7, -0.1),
            axes_2d.c2p(3.9, 3.1, 2.4),
            axes_2d.c2p(3.2, 3.8, -0.8),
            axes_2d.c2p(3.7, 3.3, 2.6),
        ]
        dots = [Dot3D(point, color=BLUE) for point in points]

        # add points to the scene, animate their creation at the same time, but with a delay
        self.play(
            LaggedStart(*[Create(dot) for dot in dots], lag_ratio=0.1), run_time=2
        )
        self.wait(1)

        # calculate the center
        centroid = np.ndarray(shape=(3,), dtype=float)
        for point in points:
            centroid += np.array(point)
        centroid /= len(points)
        centroid_dot = Dot3D(centroid, color=YELLOW, radius=0.1)
        centroid_label = Text("Center", font_size=24, color=YELLOW)
        centroid_label.next_to(centroid_dot, UP + LEFT)
        self.play(Create(centroid_dot), Write(centroid_label))
        self.wait(1)

        # draw horizontal line through the centroid
        regression_line = Line3D(
            start=centroid_dot.get_center() - np.array((3, 0, 0)),
            end=centroid_dot.get_center() + np.array((3, 0, 0)),
            color=RED,
        )
        self.play(GrowFromPoint(regression_line, centroid_dot.get_center()))
        self.wait(1)

        # Create ValueTracker for the regression line angle
        angle_tracker = ValueTracker(0)

        # calculate the actual regression line angle
        # calculate the slope
        slope = (centroid_dot.get_y() - points[0][1]) / (
            centroid_dot.get_x() - points[0][0]
        )
        # calculate the angle in radians
        target_angle = np.arctan(slope)

        # draw thin dotted lines from each point to the horizontal line, indicating the distance
        lines = []
        for i, dot in enumerate(dots):
            line = DashedLine(
                start=dot.get_center(),
                end=np.array((dot.get_x(), centroid_dot.get_y(), dot.get_z())),
                color=GRAY,
                dash_length=0.2,
            )
            lines.append(line)

        self.play(
            LaggedStart(
                *[
                    GrowFromPoint(line, dot.get_center())
                    for line, dot in zip(lines, dots)
                ],
                lag_ratio=0.1,
            )
        )

        # Create sum of distances text in top left corner
        sum_text = Text("Sum of distances:", font_size=21, color=WHITE)
        sum_text.to_corner(UL)
        self.play(Write(sum_text))

        # Add updater to sum text to calculate current distances
        def update_sum_text(mob):
            current_distance = self.calculate_total_distance(
                dots, centroid_dot.get_center(), angle_tracker.get_value()
            )
            new_text = Text(
                f"Sum of distances: {current_distance:.2f}", font_size=21, color=WHITE
            )
            new_text.to_corner(UL)
            mob.become(new_text)

        sum_text.add_updater(update_sum_text)

        # Add updaters to each line to stay perpendicular to regression line
        for i, (line, dot) in enumerate(zip(lines, dots)):
            line.add_updater(
                lambda mob, dot=dot: mob.put_start_and_end_on(
                    dot.get_center(),
                    self.get_perpendicular_projection(
                        dot.get_center(),
                        centroid_dot.get_center(),
                        angle_tracker.get_value(),
                    ),
                )
            )

        self.wait(1)

        # rotate the regression line and update angle tracker
        self.play(
            Rotate(
                regression_line,
                angle=target_angle,
                axis=OUT,
                about_point=centroid_dot.get_center(),
            ),
            angle_tracker.animate.set_value(target_angle),
            run_time=4,
        )
        self.wait(1)

        # Remove the sum text
        sum_text.clear_updaters()
        self.remove(sum_text)
        self.wait(1)

        # create a new coordinate system with the regression line as the x-axis, this time 3D
        axes_3d = axes_2d.copy()

        # Doesnt work, using updaters instead
        # axes_3d.set(x_range=[-4, 4])
        # axes_3d.set(y_range=[-4, 4])
        # axes_3d.set(z_range=[-4, 4])
        # axes_3d.set(x_length=8)
        # axes_3d.set(y_length=8)
        # axes_3d.set(z_length=8)

        axes_3d.add_updater(
            lambda mob: mob.set(
                x_range=[-4, 4],
                y_range=[-4, 4],
                z_range=[-4, 4],
                x_length=8,
                y_length=8,
                z_length=8,
            )
        )

        axes_3d.update()

        # center of the axes to the centroid
        axes_3d.move_to(
            centroid_dot.get_center() - (axes_3d.c2p(0, 0, 0) - axes_3d.get_center())
        )
        axes_3d.rotate(
            angle_tracker.get_value(), axis=OUT, about_point=centroid_dot.get_center()
        )

        for line in lines:
            line.clear_updaters()
        self.play(Create(axes_3d), FadeOut(regression_line), run_time=2)
        self.play(FadeOut(axes_2d))

        # move to make the centroid the center of the camera
        self.move_camera(
            theta=angle_tracker.get_value() - 0.5 * PI,
            frame_center=centroid_dot.get_center(),
            run_time=1.5,
        )
        self.wait(1)

        # move Dots XY to the regression line, where the dotted lines end
        moves = []
        for i, (line, dot) in enumerate(zip(lines, dots)):
            intersection_point = self.get_perpendicular_projection(
                dot.get_center(), centroid_dot.get_center(), angle_tracker.get_value()
            )
            projection_point = np.array(
                (intersection_point[0], intersection_point[1], points[i][2])
            )
            moves.append(dot.animate.move_to(projection_point))
        self.play(
            LaggedStart(*moves, lag_ratio=0.2),
            LaggedStart(FadeOut(*lines), lag_ratio=0.2),
        )

        self.wait(1)

        self.move_camera(
            phi=PI * 0.5,
            theta=angle_tracker.get_value() - 0.5 * PI,
            frame_center=centroid_dot.get_center(),
            run_time=4,
        )

        self.wait(3)

