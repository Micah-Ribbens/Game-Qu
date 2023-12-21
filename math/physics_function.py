import math

from game_qu.base.utility_functions import get_kwarg_item, solve_quadratic
from game_qu.math.quadratic_function import QuadraticFunction


class PhysicsFunction:
    """A class that uses common physics equations for initial_velocity, acceleration, and initial_distance"""

    acceleration = 0
    initial_velocity = 0
    initial_distance = 0

    def get_time_to_vertex(self):
        """ Gets the time it takes to reach the vertex knowing that the final initial_velocity is 0, so the time is -initial_velocity / acceleration

            :returns: float; the time to reach the vertex
        """

        return -self.initial_velocity / self.acceleration

    def set_acceleration_with_displacement(self, time, displacement):
        """ Sets the acceleration knowing that d = 1/2 * a * t^2 where d is displacement, a is acceleration, and t is time.
            This is assuming initial_velocity is 0

            :parameter time: float; the amount of time that it should take to go that amount (displacement)
            :parameter displacement: float; the distance (up being positive and down being negative) that it should travel

            :returns: None
        """

        self.acceleration = (2 * displacement) / pow(time, 2)

    def set_velocity_with_displacement(self, displacement):
        """ Sets the initial velocity of the function knowing that vf^2 = vi^2 + 2ad and we know that vf is 0
            a is acceleration, t is time, and v is initial_velocity

            :parameter displacement: float; the distance (up being positive and down being negative) that it should travel

            :returns: None
        """

        # Solved for vi knowing vf = 0 in vf^2 = vi^2 + 2ad
        self.initial_velocity = math.sqrt(2 * self.acceleration * displacement)


    def set_acceleration_with_velocity(self, time, velocity_change):
        """Sets the acceleration knowing that vf = vi + at"""

        self.acceleration = velocity_change / time

    def set_all_variables(self, vertex, time, initial_distance):
        """ Sets all the variables; calls set_velocity and set_gravity_acceleration

            :parameter vertex: float; the highest/lowest point of the parabola
            :parameter time: float; the time it takes to get to the vertex/go the acceleration_distance
            :parameter acceleration_displacement: float; the distance (up being positive and down being negative) that the acceleration in that time
            :parameter initial_distance: float; the initial distance

            :returns: None
        """

        self.initial_distance = initial_distance

        # Gotten using math
        self.initial_velocity = (-2 * initial_distance + 2 * vertex) / time
        self.acceleration = 2 * (initial_distance - vertex) / pow(time, 2)

    def set_variables(self, **kwargs):
        """ Sets the variables to the number provided

            possible parameters:
                acceleration: float; the acceleration (can be positive or negative) | a in 1/2 * ax^2 + bx + c
                initial_velocity: float; the initial_velocity (can be positive or negative) | b in 1/2 * ax^2 + bx + c
                initial_distance: float; the starting point (can be positive or negative) | c in 1/2 * ax^2 + bx + c

            :returns: None
        """

        self.acceleration = get_kwarg_item(kwargs, "acceleration", self.acceleration)
        self.initial_velocity = get_kwarg_item(kwargs, "initial_velocity", self.initial_velocity)
        self.initial_distance = get_kwarg_item(kwargs, "initial_distance", self.initial_distance)

    def get_distance(self, time):
        """ Finds the number by plugging x into the equation 1/2 * at^2 + vt + d
            where a is acceleration, t is time, v is initial_velocity, and d is initial_distance

            :parameter time: float; the amount of time that has passed

            :returns: float; the number that is gotten when time is plugged into the equation
        """
        return 1 / 2 * self.acceleration * pow(time, 2) + self.initial_velocity * time + self.initial_distance

    def get_velocity_using_time(self, time):
        """ Uses the fact that the initial_velocity is equal to vi - at^2 where vi is the initial initial_velocity, a is acceleration, and t is time
            to find the initial_velocity

            :parameter time: float; the amount of time that the initial_velocity has been affected by acceleration

            :returns: float; the initial_velocity after affected by acceleration
        """

        return self.initial_velocity + self.acceleration * time

    def get_velocity_using_displacement(self, displacement):
        """ Uses the formula vf^2 = vi^2 + 2ax to find the initial_velocity
            where vf is final initial_velocity, vi is initial initial_velocity, a is acceleration, and x is displacement

            :parameter displacement: float; the amount that the ball has traveled (upwards is positive and downwards is negative)

            :returns: float; the final initial_velocity
        """

        final_velocity_squared = pow(self.initial_velocity, 2) + 2 * self.acceleration * displacement
        # Reduces the risk of a rounding error like -1*e^-15 would cause an imaginary number exception
        return pow(int(final_velocity_squared), 1 / 2)

    def get_vertex(self):
        """:returns: float; the vertex of this physics equation"""

        return self.get_distance(self.get_time_to_vertex())

    def get_times_to_point(self, distance):
        """ Finds the number by plugging in 'distance' into the equation 1/2 * at^2 + vt + d
            where a is acceleration, t is time, v is initial_velocity, and d is initial_distance

            :parameter distance: float; the distance that is wanted

            :returns: float[]; the times that the parabola is at that y coordinate
        """
        return solve_quadratic(1 / 2 * self.acceleration, self.initial_velocity, self.initial_distance - distance)

    def get_full_cycle_time(self):
        """:returns: float; the amount of time it takes the parabola to go from start_location -> start_location"""

        return self.get_time_to_vertex() * 2

    def get_indefinite_integral_of_position_equation(self):
        """:returns: Function; the indefinite integral of the position equation: x = 1/2at^2 + vt + xi"""

        a, b, c = self.get_a_b_and_c()
        return QuadraticFunction.get_indefinite_integral_using_quadratic_form(a, b, c)

    def get_a_b_and_c(self):
        """:returns: {a, b, c}; the a, b, and c values of this equation if it was in quadratic form: ax^2 + bx + c"""

        a = 1/2 * self.acceleration
        b = self.initial_velocity
        c = self.initial_distance

        return [a, b, c]

    def get_displacement(self, start_time, end_time):
        """:returns: float; the displacement of the object from start_time -> end_time (the integral from start_time to end_time)"""

        indefinite_integral = self.get_indefinite_integral_of_position_equation()
        return indefinite_integral.get_y_coordinate(end_time) - indefinite_integral.get_y_coordinate(start_time)

    def get_indefinite_integral_of_velocity_equation(self):
        """:returns: Function; the indefinite integral of the velocity equation: vt -> vt^2/2"""

        return QuadraticFunction.get_indefinite_integral_using_quadratic_form(0, self.initial_velocity, 0)

    def get_displacement_due_to_velocity(self, start_time, end_time):
        """:returns: float; the displacement of the object from start_time -> end_time (the integral from start_time to end_time)"""

        indefinite_integral = self.get_indefinite_integral_of_velocity_equation()
        return indefinite_integral.get(end_time) - indefinite_integral.get(start_time)

    def get_indefinite_integral_of_acceleration_equation(self):
        """:returns; Function; the indefinite integral of the acceleration equation: 1/2at^2 -> 1/6at^3"""

        return QuadraticFunction.get_indefinite_integral_using_quadratic_form(1/2 * self.acceleration, 0, 0)

    def get_displacement_due_to_acceleration(self, start_time, end_time):
        """:returns"""


    def __str__(self):
        return f"[{self.acceleration},{self.initial_velocity},{self.initial_distance},]"

    def __eq__(self, other):
        return (self.acceleration == other.acceleration and self.initial_velocity == other.initial_velocity and
                self.initial_distance == other.initial_distance)