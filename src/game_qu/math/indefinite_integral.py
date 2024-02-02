from game_qu.math.function import Function
import sys


class IndefiniteIntegral:
    """Essentially a wrapper class for a function that makes finding the bounded value from the integral easy"""

    indefinite_integral = None

    def __init__(self, indefinite_integral: Function) -> None:
        """Initializes the object"""

        self.indefinite_integral = indefinite_integral

    def evaluate(self, start, end) -> float:
        """
             Returns:
                float: the value gotten from using the bounds for the indefinite integral"""

        return self.indefinite_integral.get_y_coordinate(end) - self.indefinite_integral.get_y_coordinate(start)

    def set_indefinite_integral(self, indefinite_integral) -> None:
        """Sets the indefinite integral of the function"""

        self.indefinite_integral = indefinite_integral

    @staticmethod
    def get_polynomial_indefinite_integral(polynomial):
        """
             Returns:
                Function: the indefinite integral of the polynomial (does not modify the passed in polynomial)"""

        new_terms = []
        for term in polynomial.get_terms():
            # Using the reverse power rule of indefinite integrals
            new_coefficient = term.get_coefficient() * 1/(term.get_degree() + 1)
            new_degree = term.get_degree() + 1

            new_term = term.get_polynomial_term_with_values(new_coefficient, new_degree)
            new_terms.append(new_term)

        return polynomial.get_polynomial_with_terms(new_terms)

    @staticmethod
    def evaluate_polynomial_area(polynomial, start, end) -> float:
        """
             Returns:
                float: the area of the polynomial within the bounds of start and end"""

        integral_function = IndefiniteIntegral.get_polynomial_indefinite_integral(polynomial)
        return IndefiniteIntegral(integral_function).evaluate(start, end)
