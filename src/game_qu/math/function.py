from abc import ABC, abstractmethod


class Function(ABC):
    """ Anything that maps an x value to a y value. This is an abstract class with two methods.
        Only 'get_y_coordinate' must be implemented"""

    @abstractmethod
    def get_y_coordinate(self, x_coordinate):
        """
             Returns:
                float: the y coordinate associated with that x coordinate"""

        pass

    def get_x_coordinate(self, y_coordinate):
        """
             Returns:
                float: the x coordinate associated with that y coordinate (only works if the function is invertible)"""

        return self.get_inverted_function().get_x_coordinate(y_coordinate)

    def get_inverted_function(self):
        """
             Returns:
                Function: the inversion function of this current function. By default it raises a ValueError because not all functions will have an inverse"""

        raise ValueError("This function either has no inverse, or an inverse of this function was never calculated")


    @staticmethod
    def get_new_function(get_y_coordinate_method):
        """
             Returns:
                Function: a function with the get_y_coordinate method being the provided 'get_y_coordinate_method'"""

        # Creating an inner class that implements 'Function' and uses the 'get_y_coordinate_method'
        class InnerFunction(Function):
            def get_y_coordinate(self, x_coordinate):
                return get_y_coordinate_method(x_coordinate)

        return InnerFunction()  # returning an instance here
