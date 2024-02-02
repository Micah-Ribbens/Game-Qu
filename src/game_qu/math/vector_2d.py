import math

from game_qu.base.utility_functions import modified_mod


class Vector2D:
    """A class that represent a vector in 2D space"""

    angle = 0
    magnitude = 0
    x_magnitude = 0
    y_magnitude = 0

    def __init__(self, angle, magnitude):
        """Initializes a Vector2D with these values"""

        self.set_magnitude_and_angle(angle, magnitude)

    def get_x_magnitude(self):
        return self.x_magnitude

    def get_y_magnitude(self):
        return self.y_magnitude

    def get_magnitude(self):
        return self.magnitude

    def set_x_and_y_magnitude(self, x_magnitude, y_magnitude):
        """ Finds the angle and magnitude of the vector from the parameters and then calls 'self.set_values()' with those values

            Returns:
                Vector2D: 'self'"""

        magnitude = math.sqrt(math.pow(x_magnitude, 2) + math.pow(y_magnitude, 2))  # Pythagorean theorem
        angle = math.atan2(y_magnitude, x_magnitude)
        self.set_magnitude_and_angle(angle, magnitude)  # This will set the x and y magnitude

        return self

    def get_vector_with_x_and_y_magnitude(self, x_magnitude, y_magnitude):
        """
             Returns:
                Vector2D: the vector with that specific x and y magnitude (this does not modify the current vector) """

        return self.get_copy().set_x_and_y_magnitude(x_magnitude, y_magnitude)

    def set_magnitude_and_angle(self, angle, magnitude):
        """ Sets the values of the 'angle' and 'magnitude' attributes of this instance

            Returns:
                Vector2D: 'self'"""

        self.angle = angle
        self.magnitude = magnitude
        self.x_magnitude = math.cos(angle) * magnitude
        self.y_magnitude = math.sin(angle) * magnitude

        return self

    def get_vector_with_magnitude_and_angle(self, angle, magnitude):
        """ 
            Returns:
                Vector2D: the vector with that specific magnitude and angle (this does not modify the current vector) """

        return self.get_copy().set_magnitude_and_angle(angle, magnitude)

    def set_angle(self, angle):
        """ Sets the angle of the vector

            Returns:
                Vector2D: 'self'"""

        return self.set_magnitude_and_angle(angle, self.magnitude)

    def get_vector_with_angle(self, angle):
        """
             Returns:
                Vector2D: the vector with that specific angle (this does not modify the current vector) """

        return self.get_copy().set_angle(angle)

    def set_magnitude(self, magnitude):
        """ Sets the magnitude of the vector

            Returns:
                Vector2D: 'self'"""

        return self.set_magnitude_and_angle(self.angle, magnitude)

    def get_vector_with_magnitude(self, magnitude):
        """
             Returns:
                Vector2D: the vector with that specific magnitude (this does not modify the current vector) """

        return self.get_copy().set_magnitude(magnitude)

    def set_x_magnitude(self, x_magnitude):
        """ Sets the x magnitude of the vector

            Returns:
                Vector2D: 'self'"""

        return self.set_x_and_y_magnitude(x_magnitude, self.y_magnitude)

    def get_vector_with_x_magnitude(self, x_magnitude):
        """
             Returns:
                Vector2D: the vector with that specific x magnitude (this does not modify the current vector) """

        return self.get_copy().set_x_magnitude(x_magnitude)

    def set_y_magnitude(self, y_magnitude):
        """ Sets the y magnitude of the vector

            Returns:
                Vector2D: 'self'"""

        return self.set_x_and_y_magnitude(self.x_magnitude, y_magnitude)

    def get_vector_with_y_magnitude(self, y_magnitude):
        """
             Returns:
                Vector2D: the vector with that specific y magnitude (this does not modify the current vector) """

        return self.get_copy().set_y_magnitude(y_magnitude)

    def normalize(self):
        """ Normalizes the vector

            Returns:
                Vector2D: 'self'"""

        new_x_magnitude = self.x_magnitude / self.magnitude
        new_y_magnitude = self.y_magnitude / self.magnitude

        self.set_x_and_y_magnitude(new_x_magnitude, new_y_magnitude)
        return self

    def get_normalized(self):
        """
             Returns:
                Vector2D: the normalized version of this vector"""

        return self.get_copy().normalize()

    def get_copy(self):
        """
             Returns:
                Vector2D: the copy of the current vector"""

        return Vector2D(self.angle, self.magnitude)

    def add(self, other_vector):
        """ Adds the other_vector (Vector2D) to this current vector

            Returns:
                Vector2D: 'self'"""

        new_x_magnitude = other_vector.get_x_magnitude() + self.x_magnitude
        new_y_magnitude = other_vector.get_y_magnitude() + self.y_magnitude
        self.set_x_and_y_magnitude(new_x_magnitude, new_y_magnitude)
        return self

    def get_added_vector(self, other_vector):
        """
             Returns:
                Vector2D: a new vector that is the result of adding another vector to this vector (does not modify the current vector)"""

        return self.get_copy().add(other_vector)

    def subtract(self, other_vector):
        """ Subtracts the other_vector (Vector2D) from this current vector

            Returns:
                Vector2D: 'self'"""

        new_x_magnitude = other_vector.get_x_magnitude() - self.x_magnitude
        new_y_magnitude = other_vector.get_y_magnitude() - self.y_magnitude
        self.set_x_and_y_magnitude(new_x_magnitude, new_y_magnitude)
        return self

    def get_subtracted_vector(self, other_vector):
        """
             Returns:
                Vector2D: the vector that results from subtracting the other vector from this vector (does not modify the current vector)"""

        return self.get_copy().subtract(other_vector)

    def multiply_by_scalar(self, scalar):
        """ Multiplies the magnitude of the vector by the scalar

            Returns:
                Vector2D: self"""

        self.magnitude *= scalar
        self.set_magnitude_and_angle(self.angle, self.magnitude)
        return self

    def get_vector_multiplied_by_scalar(self, scalar):
        """
             Returns:
                Vector2D: a new vector that is the result of multiplying this vector by a scalar (does not modify the current vector)"""

        return self.get_copy().multiply_by_scalar(scalar)

    def hadamard_product(self, other_vector):
        """ Performs a hadamard product on this vector ([x1, y1] * [x2, y2] = [x1 * x2, y1 * y2])

            Returns:
                Vector2D: 'self'"""

        new_x_magnitude = other_vector.get_x_magnitude() * self.x_magnitude
        new_y_magnitude = other_vector.get_y_magnitude() * self.y_magnitude
        self.set_x_and_y_magnitude(new_x_magnitude, new_y_magnitude)
        return self

    def get_hadamard_product(self, other_vector):
        """
             Returns:
                Vector2D: a new vector that is the result of performing a hadamard product on this vector (does not modify the current vector)"""

        return self.get_copy().hadamard_product(other_vector)

    def rotate_vector(self, angle):
        """ Rotates the vector counter-clockwise by 'angle'

            Returns:
                Vector2D: 'self'"""

        new_angle = modified_mod(self.angle + angle, math.pi * 2)
        self.set_angle(new_angle)
        return self

    def get_rotated_vector(self, angle):
        """
             Returns:
                Vector2D: the vector that results from rotating the current vector counter-clockwise by 'angle' (does not modify the current vector)"""

        return self.get_copy().rotate_vector(angle)

    def invert_vector_direction(self):
        """ Rotates the vector by pi degrees

            Returns:
                Vector2D: self"""

        self.rotate_vector(math.pi)
        return self

    def get_inverted_direction_vector(self):
        """
             Returns:
                Vector2D: the vector that results from rotating the current vector clockwise by pi degrees (does not modify the current vector)"""

        return self.get_copy().invert_vector_direction()

    def dot_product(self, other_vector):
        """
             Returns:
                float: the dot product of these two vectors"""

        return (other_vector.get_x_magnitude() * self.x_magnitude +
                other_vector.get_y_magnitude() * self.y_magnitude)

    def equals(self, other_vector):
        """
             Returns:
                boolean: whether the other vector equals this vector"""

        return other_vector.get_angle() == self.angle and other_vector.get_magnitude() == self.magnitude

    def __add__(self, other_vector):
        """
             Returns:
                Vector2D: The resulting vector from adding 'self' to 'other_vector'"""

        return self.get_added_vector(other_vector)

    def __sub__(self, other_vector):
        """
             Returns:
                Vector2D: The resulting vector from subtracting 'other_vector' from 'self'"""

        return self.get_subtracted_vector(other_vector)

    def __mul__(self, other_vector):
        """
             Returns:
                Vector2D: The resulting vector from adding 'self' to 'other_vector'"""

        return self.get_hadamard_product(other_vector)

    def __str__(self):
        return f"angle: {self.angle} ; magnitude: {self.magnitude} ; x_magnitude: {self.x_magnitude} ; y_magnitude: {self.y_magnitude}"
