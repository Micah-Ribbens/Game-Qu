from game_qu.base.utility_functions import is_within_bounds
from game_qu.math.function import Function
from game_qu.math.piecewise_function import PiecewiseFunction


class BoundedFunction(Function):
    x_coordinates_can_be_less_than_min = False
    is_repeating = False
    min_x_coordinate = 0
    max_x_coordinate = 0
    unmodified_function = None
    current_function = None

    def __init__(self, function, min_x_coordinate, max_x_coordinate):
        """Initializes the object with the specified bounds"""

        self.set_bounds(min_x_coordinate, max_x_coordinate)
        self.set_function(function)

    def get_min_x_coordinate(self) -> float:
        """:returns: float; the minimum x coordinate"""

        return self.min_x_coordinate

    def get_max_x_coordinate(self) -> float:
        """:returns: float; the maximum x coordinate"""

        return self.max_x_coordinate

    def set_min_x_coordinate(self, min_x_coordinate):
        """Sets the minimum x-coordinate to 'min_x_coordinate'
            returns: BoundedFunction; 'self'"""

        self.min_x_coordinate = min_x_coordinate
        return self

    def get_bounded_function_with_min_x_coordinate(self, min_x_coordinate):
        """:returns: BoundedFunction; a bounded function with the specified min_x_coordinate (does not modify the current bounded function)"""

        return self.get_copy().set_min_x_coordinate(min_x_coordinate)

    def set_max_x_coordinate(self, max_x_coordinate):
        """Sets the maximum x-coordinate to 'max_x_coordinate'
            returns: BoundedFunction; 'self'"""

        self.max_x_coordinate = max_x_coordinate
        return self

    def get_bounded_function_with_max_x_coordinate(self, max_x_coordinate):
        """:returns: BoundedFunction; a bounded function with the specified max_x_coordinate (does not modify the current bounded function)"""

        return self.get_copy().set_max_x_coordinate(max_x_coordinate)

    def set_bounds(self, min_x_coordinate, max_x_coordinate):
        """Sets both minimum and maximum x coordinates (bounds)
            returns: BoundedFunction; 'self'"""

        self.set_min_x_coordinate(min_x_coordinate)
        self.set_max_x_coordinate(max_x_coordinate)
        self.update_current_function()
        return self

    def get_bounded_function_with_bounds(self, min_x_coordinate, max_x_coordinate):
        """:returns: BoundedFunction; a bounded function with the specified bounds (does not modify the current bounded function)"""

        return self.get_copy().set_bounds(min_x_coordinate, max_x_coordinate)

    def get_coordinates(self) -> tuple:
        """:returns: tuple; (min_x_coordinate, max_x_coordinate)"""

        return self.min_x_coordinate, self.max_x_coordinate

    def get_copy(self):
        """:returns: BoundedFunction; a copy of the bounded function"""

        return BoundedFunction(self.min_x_coordinate, self.max_x_coordinate)

    def get_function(self):
        """:returns: function; the stored function"""

        return self.current_function

    def set_function(self, function):
        """ Sets the underlying function to 'function'
            returns: BoundedFunction; 'self"""

        self.unmodified_function = function
        self.update_current_function()
        return self

    def get_bounded_function_with_function(self, function):
        """:returns: BoundedFunction; a bounded function with the underlying function being 'function' (does not modify the current bounded function)"""

        return self.get_copy().set_function(function)

    def get_is_repeating(self):
        """:returns: boolean; whether the function repeats"""

        return self.is_repeating

    def set_is_repeating(self, is_repeating):
        """Sets the is_repeating attribute to 'is_repeating'
            returns: BoundedFunction; 'self'"""

        self.is_repeating = is_repeating
        return self

    def get_bounded_function_with_is_repeating(self, is_repeating):
        """:returns: BoundedFunction; a bounded function with the is repeating attribute set to 'is_repeating' (does not modify the current bounded function)"""

        return self.get_copy().set_is_repeating(is_repeating)

    def get_x_coordinates_can_be_less_than_min(self):
        """:returns: bool; whether the x coordinates this function accepts can be less than the min x coordinate"""

        return self.x_coordinates_can_be_less_than_min

    def set_x_coordinates_can_be_less_than_min(self, x_coordinates_can_be_less_than_min):
        """:returns: bool; sets whether the x coordinates this function accepts can be less than the min x coordinate
            returns: BoundedFunction; 'self'"""

        value_has_changed = self.x_coordinates_can_be_less_than_min != x_coordinates_can_be_less_than_min
        if value_has_changed and x_coordinates_can_be_less_than_min:
            self.update_current_function()

        if x_coordinates_can_be_less_than_min:
            self.current_function = self.unmodified_function

        self.x_coordinates_can_be_less_than_min = x_coordinates_can_be_less_than_min
        return self

    def get_full_function(self):
        """ :returns: PiecewiseFunction; the fully 'unbounded' function - x coordinates can now be less than the min x
            x coordinate"""

        start = self.get_min_x_coordinate() - self.bounds_size()
        end = self.get_max_x_coordinate() - self.bounds_size()
        bounds_size = self.bounds_size()  # This is the bounds size do not change if the original bounds size change!

        before_function = self.get_bounded_function_with_bounds(start, end)
        before_function.get_y_coordinate = lambda x: before_function.get_y_coordinate(x - bounds_size)

        return PiecewiseFunction([self.get_copy(), before_function])

    def update_current_function(self):
        """Updates the current function after the bounded function is updated"""

        if self.x_coordinates_can_be_less_than_min:
            self.current_function = self.get_full_function()

        else:
            self.current_function = self.unmodified_function

    def get_bounded_function_with_x_coordinates_less_than_min(self, x_coordinates_can_be_less_than_min):
        """:returns: BoundedFunction; a bounded function with the is repeating attribute set to 'x_coordinates_can_be_less_than_min' (does not modify the current bounded function)"""

        return self.get_copy().set_x_coordinates_can_be_less_than_min(x_coordinates_can_be_less_than_min)

    def get_y_coordinate(self, x_coordinate):
        """:returns: float; the y_coordinate associated with that value"""

        if not self.is_repeating and not is_within_bounds(x_coordinate, self.min_x_coordinate, self.max_x_coordinate):
            raise ValueError("The x coordinate must be within the bounds specified because this function has strict bounds")

        return self.current_function.get_y_coordinate(x_coordinate)

    def get_x_coordinate(self, y_coordinate):
        """ :returns: float; the x coordinate associated with that y coordinate (raises a ValueError if the function does
            not implement the get_inverse_function() method"""

        return self.current_function.get_x_coordinate(y_coordinate)

    def get_bounds(self):
        """:returns: {min_x_coordinate, max_x_coordinate}; the bounds of the function"""

        return [self.min_x_coordinate, self.max_x_coordinate]

    def bounds_size(self):
        """:returns: float; the size of the bounds (max - min)"""

        return self.max_x_coordinate - self.min_x_coordinate

    def get_min(self):
        """:returns: float; the value of the function at the min x coordinate"""

        return self.current_function.get_y_coordinate(self.min_x_coordinate)

    def get_max(self):
        """:returns: float; the value of the function at the max x coordinate"""

        return self.current_function.get_y_coordinate(self.max_x_coordinate)

    def get_indefinite_integral(self):
        """ Finds and returns the indefinite integral. Raises an AttributeError if the underlying function does not have the
            method: 'get_indefinite_integral'

            :returns: IndefiniteIntegral; the indefinite integral of the polynomial"""

        return self.current_function.get_indefinite_integral()

    def evaluate_area(self, start, end):
        """:returns: float; the value gotten from using the bounds for the indefinite integral"""

        return self.get_indefinite_integral().evaluate(start, end)

    def get_derivative(self):
        """ Finds and returns the derivative. Raises an AttributeError if the underlying function do not have the
            method: 'get_derivative'

            :returns: Derivative; the derivative of the polynomial"""

        return self.current_function.get_derivative()

    def evaluate_derivative_at_point(self, x_coordinate):
        """:returns: float; the value of the derivative evaluated at the 'x_coordinate'"""

        return self.get_derivative().evaluate(x_coordinate)
