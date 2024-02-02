from game_qu.math.function import Function
from game_qu.math.line_segment import LineSegment


class LinearInterpolation(Function):
    """ Made up of multiple lines that are all connected. The previous point and the next point are connected by a line.
        For instance, a line looks like: LineSegment(points[0], points[1]). IMPORTANT: no LineSegments can share the same
        x_coordinate (besides the first x_coordinate between adjacent lines) otherwise the code won't work"""

    lines = []
    points = []
    last_point = None

    def __init__(self, start_point, other_points):
        """Initializes the object with the start_point and other_points. This method calls add_point() for each point in other_points"""

        self.lines = []
        self.points = [start_point]
        self.last_point = start_point

        for other_point in other_points:
            self.add_point(other_point)

    def add_point(self, point):
        """Adds the point to this path by adding a new line to the path: LineSegment('last_point', 'point')"""

        self.lines.append(LineSegment(self.last_point, point))
        self.last_point = point
        self.points.append(point)

    def get_y_coordinate(self, x_coordinate):
        """
             Returns:
                float: the y_coordinate at that x_coordinate. Or in other words, what the LineSegment that contains
                the x_coordinate get_y_coordinate() method returns"""

        y_coordinate = 0

        for line in self.lines:
            if line.contains_x_coordinate(x_coordinate):
                y_coordinate = line.get_y_coordinate(x_coordinate)
                break

        return y_coordinate

    def get_lines(self):
        """
             Returns:
                list[LineSegment]: the lines of this simple path"""

        return self.lines

    def get_first_line(self):
        """
             Returns:
                LineSegment: the last LineSegment of the Path"""

        return self.lines[0]

    def get_last_line(self):
        """
             Returns:
                LineSegment: the last LineSegment of the Path"""

        last_index = len(self.lines) - 1
        return self.lines[last_index]

    def __str__(self):
        """
             Returns:
                str: the string representation of the Path"""

        string = ""
        for x in range(len(self.lines)):
            string += f"{self.lines[x]} || "

        return string

    def is_moving_down(self, x_coordinate):
        """
             Returns:
                bool: if the slope is negative for the last line that contains this specific 'x_coordinate'"""

        return_value = None

        for line in self.lines:
            if line.contains_x_coordinate(x_coordinate):
                return_value = not line.slope_is_positive()

        return return_value
