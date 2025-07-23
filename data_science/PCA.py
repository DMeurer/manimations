from manim import *


class PCAAnimation(ThreeDScene):
	def construct(self):
		# camera setup
		# self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
		# self.begin_3dillusion_camera_rotation(rate=0.3)

		self.wait(1)

		# 3D Axes
		axes = Axes(
			x_range=[0, 5],
			y_range=[0, 5],
			x_length=5,
			y_length=5,
		)
		axes.shift(IN * 2)

		self.play(Create(axes))

		# create random points between (0, 0, 0) and (5, 5, 5)
		points = [
			axes.c2p(1.1, 1.2, 2.3),
			axes.c2p(1.6, 1.0, -0.8),
			axes.c2p(1.0, 1.7, 2.8),
			axes.c2p(1.8, 1.1, -0.2),
			axes.c2p(1.3, 1.9, 2.1),
			axes.c2p(1.9, 1.3, -0.9),
			axes.c2p(1.2, 1.5, 2.9),
			axes.c2p(3.2, 3.1, -0.3),
			axes.c2p(3.9, 3.8, 2.2),
			axes.c2p(3.1, 3.9, -0.7),
			axes.c2p(3.8, 3.2, 2.7),
			axes.c2p(3.3, 3.7, -0.1),
			axes.c2p(3.9, 3.1, 2.4),
			axes.c2p(3.2, 3.8, -0.8),
			axes.c2p(3.7, 3.3, 2.6)
		]
		dots = [Dot3D(point, color=BLUE) for point in points]

		# add points to the scene, animate their creation at the same time, but with a delay
		self.play(LaggedStart(*[Create(dot) for dot in dots], lag_ratio=0.1), run_time=2)
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
		
		# draw horizontal line from through the centroid
		horizontal_line = Line3D(
			start=centroid_dot.get_center() - np.array((3, 0, 0)),
			end=centroid_dot.get_center() + np.array((3, 0, 0)),
			color=RED
		)
		self.play(GrowFromPoint(horizontal_line, centroid_dot.get_center()))
		self.wait(1)
		
		# draw thin dotted lines from each point to the horizontal line, indicating the distance
		lines = []
		for dot in dots:
			line = DashedLine(
				start=dot.get_center(),
				end=np.array((dot.get_x(), centroid_dot.get_y(), dot.get_z())),
				color=GRAY,
				dash_length=0.2
			)
			lines.append(line)
		self.play(LaggedStart(*[GrowFromPoint(line, dot.get_center()) for line, dot in zip(lines, dots)], lag_ratio=0.1))
		
