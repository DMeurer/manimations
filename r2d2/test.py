from manim import *

class LineAndVector(Scene):
	def construct(self):
		# Create a line
		line = Line(start=LEFT, end=RIGHT)
		# Create a vector
		vector = Vector(RIGHT + UP)

		# Animate the creation of the line and vector
		self.play(GrowFromPoint(line, line.get_start()))
		self.wait() # Wait a bit to see the line
		self.play(GrowFromPoint(vector, vector.get_start()))
		self.wait()

		# Example of transforming the line
		self.play(line.animate.shift(UP * 2))
		self.wait()

		# Example of transforming the vector
		self.play(vector.animate.shift(DOWN * 2))
		self.wait()


class Axis(ThreeDScene):
	def construct(self):
		# Set up the camera
		# self.set_camera_orientation(phi=45 * DEGREES, theta=10 * DEGREES)
		self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

		# Create 3D axes with colors matching the image
		axes = ThreeDAxes(
			x_range=[-5, 5, 1],
			y_range=[-5, 5, 1],
			z_range=[-2, 4, 1],
			x_length=10,
			y_length=10,
			z_length=6,
		)
		
		# Points for each axis
		x_point = Dot3D(axes.c2p(2, 0, 0), color=RED)
		y_point = Dot3D(axes.c2p(0, 2, 0), color=BLUE)
		z_point = Dot3D(axes.c2p(0, 0, 2), color=GREEN)
		
		self.play(Create(axes))
		self.play(
			Create(x_point),
			Create(y_point),
			Create(z_point)
		)
		self.wait(5)


class ElbowTest(ThreeDScene):
	def construct(self):
		# Set up the camera
		# self.set_camera_orientation(phi=45 * DEGREES, theta=10 * DEGREES)
		self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

		# Create 3D axes with colors matching the image
		axes = ThreeDAxes(
			x_range=[-5, 5, 1],
			y_range=[-5, 5, 1],
			z_range=[-2, 4, 1],
			x_length=10,
			y_length=10,
			z_length=6,
		)
		self.play(Create(axes))
		
		elbow = Elbow(
			color=YELLOW,
			width=0.1
		)
		
		elbow.set_points_as_corners([RIGHT, RIGHT+UP, UP])

		self.play(
			Create(elbow),
			run_time=2
		)
		
		self.play(
			Rotate(elbow, angle=135*DEGREES, axis=np.array((0, 5, 10)), about_point=ORIGIN),
		)
		
		self.wait(5)