from game_qu.math.piecewise_function import PiecewiseFunction


def get_full_function(bounded_function):
    """
         Returns:
            PiecewiseFunction: the fully 'unbounded' function - x coordinates can now be less than the min x
            x coordinate"""

    start = bounded_function.get_min_x_coordinate() - bounded_function.bounds_size()
    end = bounded_function.get_max_x_coordinate() - bounded_function.bounds_size()
    bounds_size = bounded_function.bounds_size()  # This is the bounds size do not change if the original bounds size change!

    before_function = bounded_function.get_bounded_function_with_bounds(start, end)
    before_function.get_y_coordinate = lambda x: before_function.get_y_coordinate(x - bounds_size)

    return PiecewiseFunction([bounded_function.get_copy(), before_function])