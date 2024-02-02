from game_qu.base.important_constants import SCREEN_LENGTH, SCREEN_HEIGHT


class Dimensions:
    """ Gives left_edge, top_edge, height, length and then using those number it provides
        right_edge, bottom_edge, horizontal_midpoint, and vertical_midpoint"""

    left_edge = 0
    top_edge = 0
    length = 0
    height = 0

    def __init__(self, left_edge, top_edge, length, height):
        """Initializes all the attributes of the class with the numbers provided (calls self.number_set_dimensions())"""

        self.number_set_dimensions(left_edge, top_edge, length, height)

    @property
    def right_edge(self):
        """The left_edge + length is what constitutes the object's right_edge"""

        return self.left_edge + self.length

    @property
    def bottom_edge(self):
        """The top_edge + height is what constitutes the object's bottom_edge"""

        return self.top_edge + self.height

    @property
    def horizontal_midpoint(self):
        """The left_edge + length / 2 is what constitutes the object's horizontal_midpoint"""

        return self.left_edge + self.length / 2

    @property
    def vertical_midpoint(self):
        """The top_edge + height / 2 is what constitutes the object's vertical_midpoint"""

        return self.top_edge + self.height / 2

    def number_set_dimensions(self, left_edge, top_edge, length, height):
        """Sets the dimensions of this object (does the same thing as __init__)"""

        self.left_edge, self.top_edge, self.length, self.height = left_edge, top_edge, length, height

    def percentage_set_dimensions(self, percent_right, percent_down, percent_length, percent_height,
                                  horizontal_number=SCREEN_LENGTH, vertical_number=SCREEN_HEIGHT):
        """ Sets the dimensions based on the values passed into this function

            Args:
                percent_right (int): the percent it is to right (percentage of horizontal_number)
                percent_down (int): the percent it is down (percentage of horizontal_number)
                percent_length (int): the length (percentage of vertical_number)
                percent_height (int): the height (percentage of vertical_number)
                horizontal_number (int): what percent_right and percent_length are percentages of
                vertical_number (int): what percent_down and percent_height are percentages of
     
            Returns:
                None
        """

        self.left_edge = horizontal_number * percent_right / 100
        self.length = horizontal_number * percent_length / 100
        self.top_edge = vertical_number * percent_down / 100
        self.height = vertical_number * percent_height / 100

    def set_dimensions_within_component(self, percent_right, percent_down, percent_length, percent_height, component):
        """ Sets the dimensions of this component, so it fits within the other 'component.' The percentages are relative
            to the provided 'component.' For instance, percent_length is a percentage of component.length."""

        self.left_edge = component.length * percent_right / 100 + component.left_edge
        self.length = component.length * percent_length / 100
        self.top_edge = component.height * percent_down / 100 + component.top_edge
        self.height = component.height * percent_height / 100

    def set_left_edge(self, value):
        self.left_edge = value

    def set_top_edge(self, value):
        self.top_edge = value

    def set_right_edge(self, value):
        self.left_edge = value - self.length

    def set_bottom_edge(self, value):
        self.top_edge = value - self.height

    def set_height(self, value):
        self.height = value

    def set_length(self, value):
        self.length = value
