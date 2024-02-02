from game_qu.base.utility_functions import max_value
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.math.line_segment import LineSegment
from game_qu.math.point import Point
from game_qu.paths.followable_path import FollowablePath


class VelocityFollowablePath(FollowablePath):
    """A followable path that the user specifies the points to and this path does the rest of the calculations"""

    velocity = 0
    left_edge_lines = []
    top_edge_lines = []

    times = []  # Stores the times that the get_coordinates() function was called
    last_point = None

    def __init__(self, start_point, other_points, velocity, **kwargs):
        """ Initializes the object. Here are the kwargs options:

            Args:
                game_object (GameObject): the game object that is following this path
                attribute_modifying (str): the name of the attribute this path is modifying"""

        super().__init__(game_object=kwargs.get("game_object"), attribute_modifying=kwargs.get("attribute_modifying"))
        self.velocity = velocity
        self.path_lines = []
        self.left_edge_lines = []
        self.top_edge_lines = []
        self.times = []

        self.last_point = start_point

        for point in other_points:
            self.add_point(point)

    def add_point(self, point):
        """ Does some calculations to find the time from the start of the last point to the end of the parameter 'point'
            and then calls add_time_point() to add the point"""

        x_distance = abs(self.last_point.x_coordinate - point.x_coordinate)
        y_distance = abs(self.last_point.y_coordinate - point.y_coordinate)

        x_time = x_distance / self.velocity
        y_time = y_distance / self.velocity

        # Whichever one is greater is how long the object will take to travel that distance because it...
        # can't travel faster than one of its max velocities
        time_to_travel_distance = max_value(x_time, y_time)

        end_time = time_to_travel_distance + self.max_time

        self.add_time_point(point, end_time)

    def add_time_point(self, point, end_time):
        """Adds the point to the path using the end_time as the x_coordinate for the x and y coordinate lines"""

        left_edge_line = LineSegment(Point(self.max_time, self.last_point.x_coordinate),
                                     Point(end_time, point.x_coordinate))

        top_edge_line = LineSegment(Point(self.max_time, self.last_point.y_coordinate),
                                    Point(end_time, point.y_coordinate))

        self.left_edge_lines.append(left_edge_line)
        self.top_edge_lines.append(top_edge_line)
        self.max_time = end_time

        # The height for the path_line doesn't matter
        self.last_point = point

    def get_coordinates(self, should_increase_time=True):
        """
             Returns:
                list[float]: {left_edge, top_edge}; the coordinates at the current time - also updates the current time
                by calling 'self.update_time' if 'should_increase_time'"""

        if should_increase_time:
            self.update_time()

        return self.get_coordinates_at_time(self.current_time)

    def update_time(self):
        """Updates the time variables for this object by the time the last game tick took"""

        # The time should only be increased if it was not called that cycle
        if self.last_time != VelocityCalculator.time:
            self.current_time += VelocityCalculator.time
            self.last_time = VelocityCalculator.time

        max_time = self.max_time

        if self.current_time > max_time and self.has_max_time:
            self.current_time %= max_time

    def get_coordinates_at_time(self, time):
        """
             Returns:
                list[float]: {left_edge, top_edge}; the coordinates at that time"""

        index = self.get_index_of_line(time)
        left_edge_line = self.left_edge_lines[index]
        top_edge_line = self.top_edge_lines[index]

        return [left_edge_line.get_y_coordinate(time), top_edge_line.get_y_coordinate(time)]

    def get_index_of_line(self, time):
        """
             Returns:
                int: the index of the line that the path is currently on"""

        return_value = len(self.left_edge_lines) - 1

        for x in range(len(self.top_edge_lines)):
            top_edge_line: LineSegment = self.top_edge_lines[x]
            start_point = top_edge_line.start_point
            end_point = top_edge_line.end_point

            if time >= start_point.x_coordinate and time <= end_point.x_coordinate:
                return_value = x

        return return_value

    def set_time(self, time):
        """Sets the time to the provided 'time'- if it is greater than the max time it is reduced to a smaller time"""

        self.current_time = time % self.max_time

    def get_value_at_time(self, time):
        """
             Returns:
                object: the value of the attribute this path is modifying at 'time'"""

        return self.get_coordinates_at_time(time)[1]  # To get the y coordinate

    def get_delta_value(self, start_time, end_time):
        """
             Returns:
                object: the delta value of the attribute within the domain [start_time, end_time]"""

        return self.get_value_at_time(end_time) - self.get_value_at_time(start_time)

    def __str__(self):
        string = ""
        for x in range(len(self.top_edge_lines)):
            top_edge_line = self.top_edge_lines[x]
            left_edge_line = self.left_edge_lines[x]

            string += f"x {left_edge_line}, y {top_edge_line}\n"

        return string

    @property
    def last_end_time(self):
        return self.max_time

    @last_end_time.setter
    def last_end_time(self, value):
        self.max_time = value

    @property
    def total_time(self):
        return self.current_time

    @total_time.setter
    def total_time(self, value):
        self.current_time = value

    @property
    def previous_time(self):
        return self.last_time

    @previous_time.setter
    def previous_time(self, value):
        self.last_time = value

    @property
    def is_unending(self):
        return self.has_max_time

    @is_unending.setter
    def is_unending(self, value):
        self.has_max_time = value
