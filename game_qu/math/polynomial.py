import math
from copy import deepcopy

from game_qu.math.derivative import Derivative
from game_qu.math.function import Function
from game_qu.math.indefinite_integral import IndefiniteIntegral


class PolynomialTerm:
    """A class that represents a term of a polynomial"""

    coefficient = 0
    degree = 0

    def __init__(self, coefficient, degree):
        """Initializes the polynomial term with the given coefficient and degree"""

        self.set_values(coefficient, degree)

    def get_degree(self) -> float:
        """ Returns:
                float: the degree of the polynomail"""

        return self.degree

    def get_coefficient(self) -> float:
        """ Returns:
                float: the coefficient"""

        return self.coefficient

    def set_degree(self, degree):
        """ Sets the degree of the polynomial term to 'degree'

            Returns:
                PolynomialTerm: 'self'"""

        self.degree = degree
        return self

    def get_polynomial_term_with_degree(self, degree):
        """ Returns:
                PolynomialTerm: the polynomial term with that degree (does not modify the current polynomial term)"""

        self.get_copy().set_degree(degree)

    def set_coefficient(self, coefficient):
        """Sets the coefficient of the polynomial term to 'coefficient'

            Returns:
                PolynomialTerm: 'self'"""

        self.coefficient = coefficient
        return self

    def get_polynomial_term_with_coefficient(self, coefficient):
        """ Returns:
                PolynomialTerm: the polynomial term with that coefficient (does not modify the current polynomial term)"""

        self.get_copy().set_coefficient(coefficient)

    def set_values(self, coefficient, degree):
        """ Sets the degree and coefficient of the polynomial term

            Returns:
                PolynomialTerm: 'self'"""

        self.set_coefficient(coefficient)
        self.set_degree(degree)
        return self

    def get_polynomial_term_with_values(self, coefficient, degree):
        """ Returns:
                PolynomialTerm: the polynomial term with those values (does not modify the current polynomial term)"""

        self.get_copy().set_values(coefficient, degree)

    def get_copy(self):
        """ Returns:
                PolynomialTerm: a polynomial term copy"""

        return PolynomialTerm(self.coefficient, self.degree)

    def evaluate(self, x_value) -> float:
        """ Returns:
                float: the value associated with that polynomial term"""

        return self.coefficient * math.pow(x_value, self.degree)


class Polynomial(Function):
    """ Represents a polynomial function. The coefficients are in a matrix with the power being the length of the matrix
        - the index - 1. For instance, [1, 2, 3, 4] -> x^3 + 2x^2 + 3x + 4"""

    matrix = None

    def __init__(self, matrix):
        """Initializes the object with the matrix of terms. For instance, [1, 2, 3, 4] -> x^3 + 2x^2 + 3x + 4"""

        self.matrix = matrix

    def set_matrix(self, matrix):
        """ Sets the matrix of terms. For instance, [1, 2, 3, 4] -> x^3 + 2x^2 + 3x + 4

            Returns:
                Polynomial: 'self'"""

        self.matrix = matrix
        return self

    def get_polynomial_with_matrix(self, matrix):
        """ Returns:
                Polynomial: a polynomial with the given matrix (does not modify this polynomial)"""

        return self.get_copy().set_matrix(matrix)

    def set_terms(self, terms):
        """ Sets the terms of the polynomial

            Returns:
                Polynomial: 'self"""

        self.matrix.set_backing_list(terms)
        return self

    def get_terms(self):
        """ Returns:
                list[PolynomialTerm]: the terms of the polynomial"""

        return self.matrix.get_backing_list()

    def get_polynomial_with_terms(self, terms):
        """ Returns:
                Polynomial: the polynomial with the given terms (does not modify this polynomial)"""

        return self.get_copy().set_terms(terms)

    def get_copy(self):
        """ Returns:
                Polynomial: a copy of this polynomial"""

        matrix = deepcopy(self.matrix)
        return Polynomial(matrix)

    def get_y_coordinate(self, x_coordinate) -> float:
        """ Returns:
                float: y coordinate associated with that x coordinate"""

        y_coordinate = 0

        for term in self.matrix.get_backing_list():
            y_coordinate += term.evaluate(x_coordinate)

        return y_coordinate

    def get_indefinite_integral(self):
        """ Returns:
                IndefiniteIntegral: the indefinite integral of the polynomial"""

        return IndefiniteIntegral.get_polynomial_indefinite_integral(self)

    def evaluate_area(self, start, end):
        """ Returns:
                float: the value gotten from using the bounds for the indefinite integral"""

        return IndefiniteIntegral.evaluate_polynomial_area(self, start, end)

    def get_derivative(self):
        """ Returns:
                Derivative: the derivative of the function"""

        return Derivative.get_polynomial_derivative(self)

    def evaluate_derivative_at_point(self, x_coordinate):
        """ Returns:
                float: the value of the derivative evaluated at the 'x_coordinate'"""

        return Derivative.evaluate_polynomial_derivative_at_point(self, x_coordinate)
