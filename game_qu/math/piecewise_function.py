from copy import deepcopy

from game_qu.math.derivative import Derivative
from game_qu.math.function import Function
from game_qu.base.utility_functions import modified_mod, is_within_bounds, min_value
from game_qu.math.indefinite_integral import IndefiniteIntegral


class PiecewiseFunction(Function):
    """ A function that is made up of multiple functions. The function uses different functions depending on what the x
        coordinate is and if it falls within the other function"""

    functions = []
    is_repeating = False
    x_coordinates_can_be_less_than_min = True
    min_x_coordinate = 0
    max_x_coordinate = 0

    def __init__(self, functions):
        """Initializes the object with the functions"""

        self.set_functions(functions)

    def get_functions(self):
        """ Returns:
                BoundedFunction: all the functions of the piecewise function"""

        return self.functions

    def set_functions(self, functions):
        """Sets the functions of the piecewise function

             Returns:
                PiecewiseFunction: 'self'"""

        self.functions = functions
        self.update_function_bounds_fully()
        return self

    def get_piecewise_function_with_functions(self, functions):
        """ Returns:
                PiecewiseFunction: a piecewise function with functions attribute being set to 'functions' (does not modify the current piecewise function)"""

        return self.get_copy().set_functions(functions)

    def get_copy(self):
        """ Returns:
                PiecewiseFunction: a copy of the current piecewise_function"""

        # return deepcopy(self)
        new_functions = []
        copy = PiecewiseFunction(new_functions)
        for val in self.get_functions():
            new_functions.append(val)

        copy.set_is_repeating(self.is_repeating)
        copy.set_x_coordinates_can_be_less_than_min(self.x_coordinates_can_be_less_than_min)
        return copy


    def get_x_coordinates_can_be_less_than_min(self):
        """ Returns:
                bool: whether the x coordinates this function accepts can be less than the min x coordinate"""

        return self.x_coordinates_can_be_less_than_min

    def set_x_coordinates_can_be_less_than_min(self, x_coordinates_can_be_less_than_min):
        """ Sets whether the x coordinates this function accepts can be less than the min x coordinate

             Returns:
                BoundedFunction: 'self'"""

        self.x_coordinates_can_be_less_than_min = x_coordinates_can_be_less_than_min
        return self

    def get_bounded_function_with_x_coordinates_less_than_min(self, x_coordinates_can_be_less_than_min):
        """ Returns:
                PiecewiseFunction: a piecewise function with the is repeating attribute set to 'x_coordinates_can_be_less_than_min' (does not modify the current piecewise function)"""

        return self.get_copy().set_x_coordinates_can_be_less_than_min(x_coordinates_can_be_less_than_min)

    def get_is_repeating(self):
        """ Returns:
                boolean: whether the piecewise function repeats"""

        return self.is_repeating

    def set_is_repeating(self, is_repeating):
        """Sets the is_repeating attribute to 'is_repeating'

             Returns:
                PiecewiseFunction: 'self'"""

        self.is_repeating = is_repeating
        return self

    def get_piecewise_function_with_is_repeating(self, is_repeating):
        """ Returns:
                PiecewiseFunction: a piecewise function with the is repeating attribute set to 'is_repeating' (does not modify the current piecewise function)"""

        return self.get_copy().set_is_repeating(is_repeating)

    def update_function_bounds_fully(self):
        """Updates the function bounds for operations like remove (has to check every function in the list)"""

        if len(self.functions) == 0:
            return

        self.functions = sorted(self.functions, key=lambda x: x.get_min_x_coordinate())
        self.min_x_coordinate = self.functions[0].get_min_x_coordinate()

        max_index = len(self.functions) - 1
        self.max_x_coordinate = self.functions[max_index].get_max_x_coordinate()

    def update_function_bounds_for_added_function(self, function):
        """Updates the function bounds when a function is added (do not have to check every function in list)"""

        self.min_x_coordinate = min(self.min_x_coordinate, function.get_min_x_coordinate())
        self.max_x_coordinate = max(self.max_x_coordinate, function.get_max_x_coordinate())

    def validate_function_bounds_do_not_overlap(self):
        """Raises a ValueError if the function bounds overlap (if there are overlapping bounds the piecewise function is invalidated)"""

        for i in range(len(self.functions)):
            for j in range(len(self.functions)):
                function1 = self.functions[i]
                function2 = self.functions[j]

                a, b = function1.get_bounds()
                c, d = function2.get_bounds()

                # If the function1's bounds fall within function2's bounds (case 1) or it crosses the bounds of
                # function2 (case 2) then this is no longer a valid piecewise function.
                is_invalid = a <= c <= b
                distance_between_c_and_a = a - c
                function1_bound_size = b - a
                is_invalid |= distance_between_c_and_a >= function1_bound_size

                if is_invalid:
                        raise ValueError("The bounds of each function within the piecewise function must not overlap")

    def clear_functions(self):
        """ Clears all functions from the piecewise function

            Returns:
                PiecewiseFunction: 'self'"""

        self.functions.clear()
        self.min_x_coordinate = 0
        self.max_x_coordinate = 0
        return self

    def get_piecewise_function_with_cleared_functions(self):
        """Returns a new PiecewiseFunction with cleared functions (does not modify the current piecewise function)

             Returns:
                PiecewiseFunction: new piecewise function with cleared functions"""

        return self.get_copy().clear_functions()

    def add_function(self, new_function):
        """ Adds a new function to the piecewise function

            Args:
                new_function (Function): function to be added

            Returns:
                PiecewiseFunction: 'self'"""

        self.functions.append(new_function)
        self.validate_function_bounds_do_not_overlap()
        self.update_function_bounds_fully()
        return self

    def get_piecewise_function_with_added_function(self, new_function):
        """ Returns a new PiecewiseFunction with the added function (does not modify the current piecewise function)
            
            Args:
                new_function (Function): function to be added
            
             Returns:
                PiecewiseFunction: new piecewise function with the added function"""

        return self.get_copy().add_function(new_function)

    def remove_function_at_index(self, index):
        """ Removes a function at the specified index from the piecewise function
            
            Args:
                index (int): index of the function to be removed
            
            Returns:
                PiecewiseFunction: 'self'"""

        if 0 <= index < len(self.functions):
            del self.functions[index]

        self.update_function_bounds_fully()
        return self

    def get_piecewise_function_with_function_removed_at_index(self, index):
        """ Returns a new PiecewiseFunction with a function removed at the specified index (does not modify the current piecewise function)
            Args:
                index (int): index of the function to be removed

             Returns:
               PiecewiseFunction: new piecewise function with the function removed at the specified index"""

        return self.get_copy().remove_function_at_index(index)

    def remove_function(self, function):
        """ Removes the specified function from the piecewise function

            Args:
                function (Function): function to be removed

            Returns:
                PiecewiseFunction: 'self'"""

        self.functions.remove(function)
        self.update_function_bounds_fully()
        return self

    def get_piecewise_function_with_function_removed(self, function):
        """ Returns a new PiecewiseFunction with the specified function removed (does not modify the current piecewise function)
            Args:
                function (Function): function to be removed

             Returns:
                PiecewiseFunction: new piecewise function with the specified function removed"""

        return self.get_copy().remove_function(function)

    def get_y_coordinate(self, x_coordinate):
        """ Returns:
                float: the y coordinate associated with that x coordinate"""

        return self.get_function(x_coordinate).get_y_coordinate(x_coordinate)

    def get_function(self, x_coordinate):
        """ Returns:
                BoundedFunction: the function that controls the piecewise function at the x coordinate"""

        if len(self.functions) == 0:
            raise ValueError("There must be a function in functions in order for the piecewise function to operate")

        if self.is_repeating:
            x_coordinate = modified_mod(x_coordinate, self.bounds_size())

        if not is_within_bounds(x_coordinate, self.min_x_coordinate, self.max_x_coordinate):
            if not self.x_coordinates_can_be_less_than_min:
                raise ValueError("The x coordinate must be greater")

            else:
                return self.get_before_piecewise_function().get_function(x_coordinate)

        for function in self.functions:
            if is_within_bounds(x_coordinate, *function.get_bounds()):
                return function

        raise ValueError("You should not get this value error! This is an implementation error in the code")



    def get_before_piecewise_function(self):
        """ Returns:
                PiecewiseFunction: a piecewise function that 'comes before' the original"""

        before_piecewise_function = self.get_copy()
        new_x_start = self.min_x_coordinate - self.bounds_size()
        # The relative positions of functions stay the same, so I am just performing a 'domain shift'
        x_position_in_original_function = lambda x: self.get_x_relative_position(new_x_start, x) + self.min_x_coordinate
        before_piecewise_function.get_y_coordinate = lambda x: self.get_y_coordinate(x_position_in_original_function(x))

        return before_piecewise_function

    def get_x_relative_position(self, start, x_coordinate):
        """ Returns:
                float: the distance x is from start (the relative position within the interval [start, end])"""

        return start - x_coordinate


    def get_min_x_coordinate(self):
        """ Returns:
                float: the min x coordinate of the piecewise function (min x coordinate of min bounded function)"""

        return self.min_x_coordinate

    def get_max_x_coordinate(self):
        """ Returns:
                float: the max x coordinate of the piecewise function (max x coordinate of max bounded function)"""

        return self.max_x_coordinate

    def get_bounds(self):
        """ Returns:
                list[float]: {min_x_coordinate, max_x_coordinate}; the bounds of the peicewise function"""

        return [self.min_x_coordinate, self.max_x_coordinate]

    def bounds_size(self):
        """ Returns:
                float: the size of the bounds (max - min)"""

        return self.max_x_coordinate - self.min_x_coordinate

    def get_indefinite_integral(self):
        """ Finds and returns the indefinite integral. Raises an AttributeError if any of the functions do not have the
            method: 'get_indefinite_integral'
     
            Returns:
                PiecewiseFunction: the indefinite integral of the polynomial"""

        new_functions = []
        for function in self.functions:
            new_functions.append(function.get_indefinite_integral())

        indefinite_integral = self.get_copy().get_piecewise_function_with_functions(new_functions)
        return indefinite_integral

    def evaluate_area(self, start, end):
        """ Returns:
                float: the value gotten from using the bounds for the indefinite integral"""

        indefinite_integral = self.get_indefinite_integral()
        area = 0
        current_start = start

        for x in range(len(indefinite_integral.get_functions())):
            bounded_function = indefinite_integral.get_functions()[x]
            min_x, max_x = bounded_function.get_bounds()

            if is_within_bounds(current_start, min_x, max_x):
                end_x = min_value(max_x, end)
                new_area = bounded_function.get_y_coordinate(end_x) - bounded_function.get_y_coordinate(current_start)
                area += new_area
                current_start = end_x

            if current_start == end:
                break

        return area

    def get_derivative(self):
        """ Finds and returns the derivative. Raises an AttributeError if any of the functions do not have the
            method: 'get_derivative'
     
            Returns:
                PiecewiseFunction: the derivative of the polynomial"""

        new_functions = []
        for function in self.functions:
            new_functions.append(function.get_derivative())

        return self.get_piecewise_function_with_functions(new_functions)

    def evaluate_derivative_at_point(self, x_coordinate):
        """ Returns:
                float: the value of the derivative evaluated at the 'x_coordinate'"""

        return self.get_derivative().get_y_coordinate(x_coordinate)