from game_qu.math.function import Function


class Derivative:
    """Essentially a wrapper class for a function that makes working with derivatives easier"""

    derivative = None

    def __init__(self, derivative: Function) -> None:
        """Initializes the object"""

        self.derivative = derivative

    def evaluate(self, x_coordinate) -> float:
        """
             Returns:
                float: the evaluating the derivative at 'x_coordinate'"""

        return self.derivative.get_y_coordinate(x_coordinate)

    def set_derivative(self, derivative) -> None:
        """Sets the derivative of the function"""

        self.derivative = derivative

    @staticmethod
    def get_polynomial_derivative(polynomial):
        """
             Returns:
                Polynomial: the derivative of the polynomial (does not modify the passed in polynomial)"""

        new_terms = []
        for term in polynomial.get_terms():
            # Using the reverse power rule of indefinite integrals
            new_coefficient = term.get_coefficient() * term.get_degree()
            new_degree = term.get_degree() - 1

            new_term = term.get_polynomial_term_with_values(new_coefficient, new_degree)
            new_terms.append(new_term)

        return polynomial.get_polynomial_with_terms(new_terms)

    @staticmethod
    def evaluate_polynomial_derivative_at_point(polynomial, x_coordinate) -> float:
        """
             Returns:
                float: the area of the polynomial within the bounds of start and end"""

        return Derivative.get_polynomial_derivative(polynomial).get_y_coordinate(x_coordinate)
