from game_qu.base.library_independant_utility_functions import min_value, max_value
from game_qu.math.function import Function
from game_qu.math.matrix import Matrix
from game_qu.math.point import Point
from game_qu.math.polynomial import Polynomial, PolynomialTerm


class LineSegment(Polynomial):
    """Uses the equation y = mx + b where m is slope and b is y_intercept"""

    start_point = None
    end_point = None
    slope = None
    y_intercept = None

    def __init__(self, start_point, end_point):
        """ Sets the start and end point of the lines. It creates a very similar line if the x_coordinate of the start and end
            point have the same x_coordinate by adding a very small number to the end_point's x_coordinate. This makes
            finding where two lines collide alot easier. This function will call set_points()

            Args:
                start_point (Point): a point on the line (different than end_point)
                end_point (Point): a point on the line (different than start_point)
     
            Returns:
                None
        """

        super().__init__(Matrix([]))
        self.set_points(start_point, end_point)

    def set_points(self, start_point, end_point):
        """ Sets the start and end point of the lines. It creates a very similar line if the x_coordinate of the start and end
            point have the same x_coordinate by adding a very small number to the end_point's x_coordinate. This makes
            finding where two lines collide alot easier.

            Args:
                start_point (Point): a point on the line (different than end_point)
                end_point (Point): a point on the line (different than start_point)
     
            Returns:
                None
        """

        self.start_point, self.end_point = start_point, end_point
        self.update_line_values()

    def set_end_point(self, end_point):
        """Sets the end point of the line"""

        self.set_points(self.start_point, end_point)

    def set_start_point(self, start_point):
        """Sets the start point of the line"""

        self.set_points(start_point, self.end_point)

    def update_line_values(self):
        """Updates the slope (m) and y_intercept (b) of the line through calculation. Uses the equation y = mx + b"""

        if self.start_point.x_coordinate == self.end_point.x_coordinate:
            self.end_point.x_coordinate += pow(10, -9)

        slope = ((self.end_point.y_coordinate - self.start_point.y_coordinate) /
                 (self.end_point.x_coordinate - self.start_point.x_coordinate))

        y_intercept = self.start_point.y_coordinate - slope * self.start_point.x_coordinate
        self.set_line_values(slope, y_intercept, self.get_min_x_coordinate(), self.get_max_x_coordinate())

    def set_line_values(self, slope, y_intercept, minimum_x, maximum_x):
        """Sets the slope and y intercept of the line"""

        self.slope = slope
        self.y_intercept = y_intercept
        self.start_point = Point(minimum_x, self.get_y_coordinate(minimum_x))
        self.end_point = Point(maximum_x, self.get_y_coordinate(maximum_x))

        self.set_terms([PolynomialTerm(self.slope, 1), PolynomialTerm(self.y_intercept, 0)])

    def set_slope(self, slope, minimum_x, maximum_x):
        """Sets the slope of the line"""

        self.set_line_values(slope, self.y_intercept, minimum_x, maximum_x)

    def set_y_intercept(self, y_intercept, minimum_x, maximum_x):
        """Sets the y intercept of the line"""

        self.set_line_values(self.slope, y_intercept, minimum_x, maximum_x)

    def get_y_coordinate(self, x_coordinate):
        """
             Returns:
                float: the y_coordinate at the x_coordinate"""

        return x_coordinate * self.slope + self.y_intercept

    def get_x_coordinate(self, y_coordinate):
        """
             Returns:
                float: the x_coordinate at the y_coordinate"""

        return (y_coordinate - self.y_intercept) / self.slope

    def contains_x_coordinate(self, x_coordinate):
        """
             Returns:
                bool: if the LineSegment contains the x_coordinate"""

        return x_coordinate >= self.get_min_x_coordinate() and x_coordinate <= self.get_max_x_coordinate()

    def contains_y_coordinate(self, y_coordinate):
        """
             Returns:
                bool: if the LineSegment contains the y_coordinate"""

        return y_coordinate >= self.get_min_y_coordinate() and y_coordinate <= self.get_max_y_coordinate()

    def contains_point(self, point):
        """
             Returns:
                bool: if the LineSegment contains the x_coordinate, y_coordinate, and point"""

        contains_coordinates = self.contains_x_coordinate(point.x_coordinate) and self.contains_y_coordinate(point.y_coordinate)
        correct_y_coordinate = point.y_coordinate == self.get_y_coordinate(point.x_coordinate)

        return contains_coordinates and correct_y_coordinate

    def slope_is_positive(self):
        """
             Returns:
                bool: if the slope is >= 0"""

        return self.slope >= 0

    def get_copy(self):
        """
             Returns:
                LineSegment: a copy of this LineSegment"""

        return LineSegment(self.start_point.get_copy(), self.end_point.get_copy())

    def get_inverted_function(self):
        """
             Returns:
                LineSegment: the line segment that is the inverse of this function (the y coordinates map to the x coordinate)"""

        start_point = Point(self.start_point.y_coordinate, self.start_point.x_coordinate)
        end_point = Point(self.end_point.y_coordinate, self.end_point.y_coordinate)

        return LineSegment(start_point, end_point)

    def get_bounds(self):
        """
             Returns:
                list[float]: {min_x_coordinate, max_x_coordinate} of this function"""

        return [self.get_min_x_coordinate(), self.get_max_x_coordinate()]

    def get_min_x_coordinate(self):
        return min_value(self.start_point.x_coordinate, self.end_point.x_coordinate)

    def get_max_x_coordinate(self):
        return max_value(self.start_point.x_coordinate, self.end_point.x_coordinate)

    def get_min_y_coordinate(self):
        return min_value(self.start_point.y_coordinate, self.end_point.y_coordinate)

    def get_max_y_coordinate(self):
        return max_value(self.start_point.y_coordinate, self.end_point.y_coordinate)

    def get_slope(self):
        return self.slope

    def get_y_intercept(self):
        return self.y_intercept
