from game_qu.math.piecewise_function import PiecewiseFunction
from game_qu.paths.followable_path import FollowablePath


class PiecewiseFollowablePath(FollowablePath):
    """A followable path that is defined by a piecewise function"""

    piecewise_function: PiecewiseFunction = None

    def __init__(self, piecewise_function, **kwargs):
        """ Initializes the object

            :parameter game_object: GameObject; the game object that is following this path
            :parameter attribute_modifying: String; the name of the attribute this path is modifying
            :parameter max_time: float; the max time of the path - the time the path should end

            :returns: None
        """

        super().__init__(**kwargs)
        self.set_piecewise_function(piecewise_function)

    def set_piecewise_function(self, piecewise_function):
        """Sets the piecewise function that defines this path"""

        self.piecewise_function = piecewise_function
        self.piecewise_function.set_is_repeating(True)
        self.piecewise_function.set_x_coordinates_can_be_less_than_min(True)

    def get_piecewise_function(self):
        """:returns: PiecewiseFunction; the piecewise function that defines the path"""

        return self.piecewise_function

    def get_value_at_time(self, time):
        """:returns: Object; the value of the attribute this path is modifying at 'time'"""

        return self.piecewise_function.get_y_coordinate(time)

    def get_delta_value(self, start_time, end_time):
        """:returns: Object; the delta value of the attribute within the domain [start_time, end_time]"""

        return self.piecewise_function.evaluate_area(start_time, end_time)