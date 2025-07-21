from manim import *

class CenterPoint(ThreeDScene):
	def construct(self):
		# Set up the camera
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

		# Create a grid plane (XY plane)
		grid = NumberPlane(
			x_range=[-5, 5, 1],
			y_range=[-5, 5, 1],
			x_length=10,
			y_length=10,
			background_line_style={
				"stroke_color": GRAY,
				"stroke_width": 1,
				"stroke_opacity": 0.3,
			},
			axis_config={
				"stroke_width": 0,
			},
			faded_line_style={
				"stroke_color": GRAY,
				"stroke_width": 0.5,
				"stroke_opacity": 0.2,
			}
		)
		
		t_start = -0.3
		t_end = 0.5
		turn_axis_start = axes.c2p(0, -10*t_start, -10*t_start)
		turn_axis_end = axes.c2p(0, -10*t_end, -10*t_end)
		turn_axis = Line3D(
			start=turn_axis_start,
			end=turn_axis_end,
			color=WHITE
		)

		# Add label for turn axis
		turn_axis_label = Text("turn axis", font_size=24, color=WHITE)
		turn_axis_label.rotate(PI/2, axis=RIGHT)
		# Position the label near the middle of the line
		label_point = axes.c2p(0, -2, -2)
		turn_axis_label.move_to(label_point)
		turn_axis_label.shift(0.5 * UP + 0.5 * LEFT)
		turn_axis_label.rotate(PI, axis=np.array((0,0,1)))

		# Create points
		center_point = Dot3D(axes.c2p(0, 0, 0), color=GREEN, radius=0.08)
		center_label = Text("Center", font_size=20, color=GREEN, weight=BOLD)
		center_label.rotate(PI/2, axis=RIGHT)
		center_label.next_to(center_point, UP + RIGHT + OUT, buff=0.1)
		center_label.rotate(PI, axis=np.array((0,0,1)))

		turning_point = Dot3D(axes.c2p(2, 0, 0), color=BLUE, radius=0.08)
		turning_label = Text("Turning Point", font_size=20, color=BLUE, weight=BOLD)
		turning_label.rotate(PI/2, axis=RIGHT)
		turning_label.next_to(turning_point, UP + RIGHT + OUT, buff=0.1)
		turning_label.rotate(PI, axis=np.array((0,0,1)))

		new_center_point = Dot3D(axes.c2p(0.59, -1, 1), color=GOLD, radius=0.08)
		new_center_label = Text("New Center", font_size=20, color=GOLD, weight=BOLD)
		new_center_label.rotate(PI/2, axis=RIGHT)
		new_center_label.next_to(new_center_point, UP + RIGHT + OUT, buff=0.1)
		new_center_label.rotate(PI, axis=np.array((0,0,1)))


		# Add all elements to the scene
		self.play(Create(axes))
		self.play(Create(grid))
		self.play(GrowFromPoint(turn_axis, turn_axis_start))
		self.play(Create(turn_axis_label))
		self.play(Create(center_point), Create(center_label))
		
		# Create vector from Center to Turning Point
		
		# Create the full vector
		full_vector = Arrow3D(
			start=axes.c2p(0, 0, 0),
			end=turning_point.get_center(),
			color=PURPLE
		)
		
		self.play(GrowFromPoint(full_vector, full_vector.get_start()))
		
		# Create turning point after vector reaches destination
		self.play(Create(turning_point), Create(turning_label))
		
		# Copy the vector and move it to start at turning point
		vector_copy = Arrow3D(
			start=full_vector.get_start(),
			end=full_vector.get_end(),
			color=ORANGE,
		)
		
		self.add(vector_copy)
		self.play(
			Rotate(vector_copy, angle=135*DEGREES, axis=turn_axis.get_direction(), about_point=vector_copy.get_start()),
			run_time=2
		)
		self.play(
			vector_copy.animate.shift(full_vector.get_start() + full_vector.get_end()),
			run_time=1.5
		)
		
		# Create new center point after vector rotation
		self.play(Create(new_center_point), Create(new_center_label))
		
		# Add a mini rotation to enhance 3D effect
		self.begin_ambient_camera_rotation(rate=0.3)
		self.wait(10)
		self.stop_ambient_camera_rotation()
		
		# Wait 1 more second before ending the scene
		self.wait(5)

class TurningPoint(ThreeDScene):
	def construct(self):

		# Create a grid plane (XY plane)
		grid = NumberPlane(
			x_range=[-5, 5, 1],
			y_range=[-5, 5, 1],
			background_line_style={
				"stroke_color": GRAY,
				"stroke_width": 1,
				"stroke_opacity": 0.3,
			},
			axis_config={
				"stroke_width": 0,
			},
			faded_line_style={
				"stroke_color": GRAY,
				"stroke_width": 0.5,
				"stroke_opacity": 0.2,
			}
		)

		center = Dot(grid.c2p(-3, -1, 0), color=WHITE, radius=0.08)
		left_wheel = Dot(grid.c2p(-4, -1, 0), color=RED, radius=0.08)
		right_wheel = Dot(grid.c2p(-2, -1, 0), color=RED, radius=0.08)

		left_wheel_label = Text("Left Wheel", font_size=20, color=RED)
		right_wheel_label = Text("Right Wheel", font_size=20, color=RED)

		left_wheel_label.next_to(left_wheel, DOWN)
		right_wheel_label.next_to(right_wheel, DOWN)

		self.add(
			grid,
			center,
			left_wheel,
			left_wheel_label,
			right_wheel,
			right_wheel_label
		)

		self.wait(2)

		left_dist = Arrow(
			start=left_wheel.get_center(),
			end=left_wheel.get_center() + grid.c2p(0, 3, 0),
			buff=0,
			color=ORANGE
		)
		right_dist = Arrow(
			start=right_wheel.get_center(),
			end=right_wheel.get_center() + grid.c2p(0, 2, 0),
			buff=0,
			color=ORANGE
		)

		self.play(
			GrowArrow(left_dist),
			GrowArrow(right_dist)
		)

		wheel_line = Line(
			start=left_wheel.get_center()- grid.c2p(3, 0, 0),
			end=right_wheel.get_center() + grid.c2p(10, 0, 0),
			color=BLUE
		)
		dist_line = Line(
			start=left_dist.get_end() + (left_dist.get_end()-right_dist.get_end()),
			end=left_dist.get_end() + (left_dist.get_end()-right_dist.get_end()) * -7,
			color=BLUE
		)

		self.play(Create(wheel_line))
		self.play(Create(dist_line))

		# Create turn point
		turning_point = Dot(grid.c2p(2, -1, 0), color=GREEN, radius=0.08)
		turning_label = Text("Turning Point", font_size=20, color=GREEN, weight=BOLD)
		turning_label.next_to(turning_point, UP + RIGHT, buff=0.1)

		self.play(Create(turning_point), Write(turning_label))

		# wait 3 seconds
		self.wait(5)