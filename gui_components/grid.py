from math import ceil, floor

from game_qu.base.important_variables import SCREEN_LENGTH, SCREEN_HEIGHT
from game_qu.base.velocity_calculator import VelocityCalculator


class Grid:
    """Provides an easy way to put components into a grid"""

    rows = None
    columns = None
    dimensions = None
    length_buffer = VelocityCalculator.get_dimension(SCREEN_LENGTH, 1)
    height_buffer = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 1)
    goes_top_to_bottom = True
    goes_left_to_right = True

    def __init__(self, dimensions, rows, columns, goes_top_to_bottom=True, goes_left_to_right=True):
        """ Initializes the object | IMPORTANT - columns and rows can't both be None

            :parameter dimensions: Dimensions; the left_edge, top_edge, length, and height of the grid
            :parameter rows: int; the max amount of rows the grid can have (can be None)
            :parameter columns: int; the max amount of columns the grid can have (can be None)
            :parameter goes_top_to_bottom: bool; if the components of the grid start at the top and go down (start at bottom if False)
            :parameter goes_left_to_right: bool; if the components of the grid start at the left and go right (start at right if False)

            :returns: None
        """

        self.dimensions = dimensions
        self.rows, self.columns = rows, columns
        self.goes_top_to_bottom, self.goes_left_to_right = goes_top_to_bottom, goes_left_to_right

    def turn_into_grid(self, items, item_max_length=None, item_max_height=None, component_stretching_is_allowed=True):
        """ Turns all the items into a grid format

            :parameter items: Component[]; the items that will be converted into a grid
            :parameter item_max_length: int; the max length that an item can be (None means there is no max length)
            :parameter item_max_height: int; the max height than an item can be (None means there is no max height)
            :parameter component_stretching_is_allowed: bool; whether the component has to be scaled by a specific value
             before it is rendered (instead of having uneven scales causing stretching)

            :returns: None
        """

        rows, columns = self.rows, self.columns
        number_of_items = len(items)

        if rows is None:
            rows = self.get_grid_dimension(columns, number_of_items)

        if columns is None:
            columns = self.get_grid_dimension(rows, number_of_items)

        item_height = self.get_item_dimension(self.dimensions.height, rows, item_max_height, self.height_buffer)
        item_length = self.get_item_dimension(self.dimensions.length, columns, item_max_length, self.length_buffer)

        base_left_edge = self.dimensions.left_edge if self.goes_left_to_right else self.dimensions.right_edge - item_length
        base_top_edge = self.dimensions.top_edge if self.goes_top_to_bottom else self.dimensions.bottom_edge - item_height

        for x in range(number_of_items):
            column_number = x % columns
            row_number = floor(x / columns)

            left_edge = base_left_edge + self.get_dimension_change(column_number, item_length, self.length_buffer)
            top_edge = base_top_edge + self.get_dimension_change(row_number, item_height, self.height_buffer)

            current_item_length = item_length
            current_item_height = item_height
            
            if not component_stretching_is_allowed:
                current_item_length, current_item_height = items[x].get_scaled_dimensions(item_length, item_height)

            items[x].number_set_dimensions(left_edge, top_edge, current_item_length, current_item_height)

    def get_grid_dimension(self, other_dimension, number_of_items):
        """ Finds the number of either rows or columns there should be depending on the value of 'other_dimension' (ceil(number_of_items / other_dimension)

            :parameter other_dimension: float; the grid dimension (number of rows or columns) other than the one that will be returned
            :parameter number_of_items: int; The number of items in the grid

            :returns: float; either the number of rows or columns depending on the value of 'other_dimension'"""

        return ceil(number_of_items / other_dimension)

    def get_item_dimension(self, grid_dimension_size, grid_dimension, item_dimension_max, buffer_between_items):
        """ Finds the size of the item that is in 'grid_dimension'- height for rows and length for columns

            :parameter grid_dimension_size: float; the grid's height if the grid item height is wanted and grid's length if the grid item length is wanted
            :parameter grid_dimension: int; the grid's number of rows if the grid item height is wanted and grid's number of columns if the grid item length is wanted
            :parameter item_dimension_max: float; the max value this function can return
            :parameter buffer_between_items: float; the number of pixels between adjacent items

            :returns: float; the size of the item that is in 'grid_dimension'- height for rows and length for columns"""

        remaining_dimension = grid_dimension_size - buffer_between_items * (grid_dimension - 1)

        item_dimension = remaining_dimension / grid_dimension

        if item_dimension_max is not None and item_dimension > item_dimension_max:
            item_dimension = item_dimension_max

        return item_dimension

    def get_dimension_change(self, grid_dimension, item_dimension, buffer_between_items):
        """ The amount of pixels that are after the first grid item in the 'grid_dimension'

            :parameter grid_dimension: int; rows if the grid item delta top_edge is wanted and columns if grid item delta left_edge is wanted
            :parameter item_dimension: float; the height of the grid item if delta top_edge is wanted and length of the grid item if delta left_edge is wanted
            :parameter buffer_between_items: float; the number of pixels between adjacent items

            :returns: float; the amount of pixels that are after the first grid item in the 'grid_dimension'"""

        dimension_change_amount = grid_dimension * (item_dimension + buffer_between_items)

        # If it starts at the top then the top_edge increases, but if it doesn't then the top_edge decreases
        return dimension_change_amount if self.goes_top_to_bottom else -dimension_change_amount
