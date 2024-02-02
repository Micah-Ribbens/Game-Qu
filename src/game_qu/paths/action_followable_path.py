from game_qu.paths.velocity_followable_path import VelocityFollowablePath


class ActionFollowablePath(VelocityFollowablePath):
    """ A path that performs an action at each of the points. This does not work the FollowablePath methods. This will have
        to change in the future."""

    actions = []
    is_unending = True
    index_of_last_line = None
    object_on_path = None

    def __init__(self, start_point, object_on_path, velocity):
        """Initializes the object"""

        super().__init__(start_point, [], velocity)
        self.object_on_path = object_on_path
        self.actions = []

    def add_point(self, point, action, additional_time=None):
        """Adds the point to the action path"""

        if additional_time is None:
            super().add_point(point)

        if additional_time is not None:
            super().add_time_point(point, self.last_end_time + additional_time)

        self.actions.append(action)

    def run(self):
        """Runs all the code for the action path"""

        new_index = self.get_index_of_line(self.total_time % self.max_time)

        if new_index != self.index_of_last_line:
            self.index_of_last_line = new_index
            self.actions[new_index]()

        self.object_on_path.left_edge, self.object_on_path.top_edge = self.get_coordinates()

    def update_for_side_scrolling(self, amount):
        """Updates the Path, so side scrolling doesn't cause any issues"""

        for left_edge_line in self.left_edge_lines:
            # The y_coordinate for the left_edge_line is the 'left_edge' and the x_coordinate is 'time'
            left_edge_line.start_point.y_coordinate -= amount
            left_edge_line.end_point.y_coordinate -= amount

            left_edge_line.update_line_values()

    def reset(self):
        """As of now action followable paths do not support this operation"""

        pass

    def is_done(self, should_reset=False):
        """As of now action followable paths do not support this operation"""

        pass

    def has_finished(self):
        """As of now action followable paths do not support this operation"""

        pass

    def start(self):
        """As of now action followable paths do not support this operation"""

        pass

    def get_value_at_time(self, time):
        """As of now action followable paths do not support this operation"""

        pass

    def get_delta_value(self, start_time, end_time):
        """As of now action followable paths do not support this operation"""

        pass