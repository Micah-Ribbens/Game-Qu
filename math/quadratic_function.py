from game_qu.math.function import Function


class QuadraticFunction(Function):
    """A class that defines the necessary variables for a quadratic ax^2 + bx + c"""
    h = 0
    k = 0
    a = 0

    def set_variables(self, h, k, a):
        """ Sets the variables to the numbers to equation: a(x-h)^2 + k

            :parameter h: float; the first number of the vertex
            :parameter k: float; the second number of the vertex
            :parameter a: float; the number that goes before (x-h)^2

            :returns: None
        """

        self.h = h
        self.k = k
        self.a = a

    def get_number(self, x):
        """ Finds the number by plugging x into the equation a(x-h)^2 + k

            :parameter x: float; the variable x that will be used to get the number

            :returns: float; the number that is gotten when x is plugged into the equation
        """

        return self.a * pow((x - self.h), 2) + self.k

    def get_y_coordinate(self, x_coordinate):
        """ :returns: the y coordinate associated with that specific x coordinate (calls 'get_number' but this function is
            here to keep the API the same throughout the library lifespan"""

        return self.get_number(x_coordinate)

    def points_set_variables(self, vertex, other_point):
        """ Sets the variables based on both points

            :parameter vertex: Point; the vertex of the quadratic equation
            :parameter other_point: Point; another point besides the vertex

            :returns: None
        """

        self.h = vertex.x_coordinate
        self.k = vertex.y_coordinate

        # Figured this out using algebra
        self.a = (other_point.y_coordinate - self.k) / pow((other_point.x_coordinate - self.h), 2)

    def get_x_coordinate(self, y_coordinate):
        """ :returns: float; the positive x coordinate associated with the y_coordinate (this is arbitrarily chosen, but
            all x coordinates can be found using 'get_x_coordinates'"""

        # Figured this out using algebra
        under_sqrt = (y_coordinate - self.k) / self.a
        return math.sqrt(under_sqrt) + self.h

    def get_x_coordinates(self, y_coordinate):
        """:returns: float[]; the x coordinates associated with that y coordinate (calls 'solve_quadratic' internally)"""

        a, b, c = QuadraticFunction.get_a_b_and_c(self.h, self.k, self.a)
        return solve_quadratic(a, b, c)

    def get_inverted_function(self):
        """:returns: Function; the inverse function"""

        return Function.get_new_function(self.get_y_coordinate)

    @staticmethod
    def get_a_b_and_c(h, k, a):
        """:returns: float[3] {a, b, c}; the values of the equation in this form: ax^2 + bx + c"""

        b = -2 * a * h
        c = a * math.pow(h, 2) + k
        return [a, b, c]

    @staticmethod
    def get_indefinite_integral_using_quadratic_form(a, b, c):
        """ Finds and returns the indefinite integral to this equation: ax^2 + bx + c

            :parameter a: float; the number in front of the x^2 term
            :parameter b: float; the number in front of the x term
            :parameter c: float; 'c' in the equation

            :returns: Function; the indefinite integral
        """

        # Some simple calculus to find the indefinite integral: ax^3/3 + bx^2/2 + cx
        equation = lambda x: 1 / 3 * a * math.pow(x, 3) + 1 / 2 * b * math.pow(x, 2) + c * x
        return Function.get_new_function(equation)

    @staticmethod
    def get_indefinite_integral_using_vertex_form(h, k, a):
        """ Finds and returns the indefinite integral to this equation: a(x-h)^2 + k

            :parameter h: float; the first number of the vertex
            :parameter k: float; the second number of the vertex
            :parameter a: float; the number that goes before (x-h)^2

            :returns: Function; the indefinite integral
        """

        a, b, c = QuadraticFunction.get_a_b_and_c(h, k, a)
        return QuadraticFunction.get_indefinite_integral_using_quadratic_form(a, b, c)

    def get_indefinite_integral(self):
        """:returns: Function; the indefinite integral"""

        return QuadraticFunction.get_indefinite_integral_using_vertex_form(self.h, self.k, self.a)

    def get_area_under_curve(self, lower_bound, upper_bound):
        """:returns: float; the area under the curve of the quadratic equation from the lower bound to the upper bound"""

        indefinite_integral = self.get_indefinite_integral()
        return indefinite_integral.get_y_coordinate(upper_bound) - indefinite_integral.get_y_coordinate(lower_bound)