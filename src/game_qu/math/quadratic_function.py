from game_qu.base.library_independant_utility_functions import rounded
from game_qu.math.function import Function
import math


class QuadraticFunction(Function):
    """A class that defines the necessary variables for a quadratic ax^2 + bx + c"""
    h = 0
    k = 0
    a = 0

    def set_variables(self, h, k, a):
        """ Sets the variables to the numbers to equation: a(x-h)^2 + k

            Args:
                h (float): the first number of the vertex
                k (float): the second number of the vertex
                a (float): the number that goes before (x-h)^2
     
            Returns:
                None
        """

        self.h = h
        self.k = k
        self.a = a

    def get_number(self, x):
        """ Finds the number by plugging x into the equation a(x-h)^2 + k

            Args:
                x (float): the variable x that will be used to get the number
     
            Returns:
                float: the number that is gotten when x is plugged into the equation
        """

        return self.a * pow((x - self.h), 2) + self.k

    def get_y_coordinate(self, x_coordinate):
        """
             Returns:
                float: the y coordinate associated with that specific x coordinate (calls 'get_number' but this function is
                here to keep the API the same throughout the library lifespan"""

        return self.get_number(x_coordinate)

    def points_set_variables(self, vertex, other_point):
        """ Sets the variables based on both points

            Args:
                vertex (Point): the vertex of the quadratic equation
                other_point (Point): another point besides the vertex
     
            Returns:
                None
        """

        self.h = vertex.x_coordinate
        self.k = vertex.y_coordinate

        # Figured this out using algebra
        self.a = (other_point.y_coordinate - self.k) / pow((other_point.x_coordinate - self.h), 2)

    def get_x_coordinate(self, y_coordinate):
        """
             Returns:
                float: the positive x coordinate associated with the y_coordinate (this is arbitrarily chosen, but
                all x coordinates can be found using 'get_x_coordinates'"""

        # Figured this out using algebra
        under_sqrt = (y_coordinate - self.k) / self.a
        return math.sqrt(under_sqrt) + self.h

    def get_x_coordinates(self, y_coordinate):
        """
             Returns:
                list[float]: the x coordinates associated with that y coordinate (calls 'solve_quadratic' internally)"""

        a, b, c = QuadraticFunction.get_a_b_and_c(self.h, self.k, self.a)
        return QuadraticFunction.solve_quadratic(a, b, c - y_coordinate)

    def get_inverted_function(self):
        """
             Returns:
                Function: the inverse function"""

        return Function.get_new_function(self.get_y_coordinate)

    def get_indefinite_integral(self):
        """
             Returns:
                Function: the indefinite integral"""

        return QuadraticFunction.get_indefinite_integral_using_vertex_form(self.h, self.k, self.a)

    def get_area_under_curve(self, lower_bound, upper_bound):
        """
             Returns:
                float: the area under the curve of the quadratic equation from the lower bound to the upper bound"""

        indefinite_integral = self.get_indefinite_integral()
        return indefinite_integral.get_y_coordinate(upper_bound) - indefinite_integral.get_y_coordinate(lower_bound)

    @staticmethod
    def get_a_b_and_c(h, k, a):
        """
             Returns:
                list[float]: {a, b, c}; the values of the equation in this form: ax^2 + bx + c"""

        b = -2 * a * h
        c = a * math.pow(h, 2) + k
        return [a, b, c]

    @staticmethod
    def get_indefinite_integral_using_quadratic_form(a, b, c):
        """ Finds and returns the indefinite integral to this equation: ax^2 + bx + c

            Args:
                a (float): the number in front of the x^2 term
                b (float): the number in front of the x term
                c (float): 'c' in the equation

            Returns:
                Function: the indefinite integral
        """

        # Some simple calculus to find the indefinite integral: ax^3/3 + bx^2/2 + cx
        equation = lambda x: 1 / 3 * a * math.pow(x, 3) + 1 / 2 * b * math.pow(x, 2) + c * x
        return Function.get_new_function(equation)

    @staticmethod
    def get_indefinite_integral_using_vertex_form(h, k, a):
        """ Finds and returns the indefinite integral to this equation: a(x-h)^2 + k

            Args:
                h (float): the first number of the vertex
                k (float): the second number of the vertex
                a (float): the number that goes before (x-h)^2

            Returns:
                Function: the indefinite integral
        """

        a, b, c = QuadraticFunction.get_a_b_and_c(h, k, a)
        return QuadraticFunction.get_indefinite_integral_using_quadratic_form(a, b, c)

    @staticmethod
    def solve_quadratic(a, b, c):
        """
             Returns:
                list[float]: [answer1, answer2] the answers to the quadratic (only one answer is returned if the
                answers are the same) and if the answer is an imaginary number it returns float('nan')"""

        number_under_square_root = pow(b, 2) - 4 * a * c
        number_under_square_root = rounded(number_under_square_root, 4)

        if number_under_square_root < 0:
            return None

        square_root = math.sqrt(number_under_square_root)

        answer1 = (-b + square_root) / (2 * a)
        answer2 = (-b - square_root) / (2 * a)

        answers = [answer2, answer1]

        # If the answers are the same, only one of them should be returned
        return answers if answers[0] != answers[1] else [answers[0]]
