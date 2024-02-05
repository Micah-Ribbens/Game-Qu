class Fraction:
    """Has a numerator and a denominator along with utility functions that go along with fractions"""

    numerator = None
    denominator = None

    def __init__(self, numerator, denominator):
        """ Initializes the fraction

            Args:
                numerator (int): the top part of the fraction
                denominator (int): the bottom part of the fraction
     
            Returns:
                None"""

        self.numerator = numerator
        self.denominator = denominator

    def get_reciprocal(self):
        """ In math reciprocal is denominator/numerator
     
            Returns:
                Fraction: a new Fraction that is the recepricol of the current Fraction
                (the denominator and numerator switch places)"""

        return Fraction(self.denominator, self.numerator)

    def get_number(self):
        """ Turns the fraction into a number
     
            Returns:
                float: the fraction as a number"""

        return self.numerator / self.denominator

    def get_fraction_to_power(self, power):
        """ Uses the function pow() to get the fraction to the specified power

            Args:
                power (int): the power to which the fraction is raised
     
            Returns:
                Fraction: a new fraction where the numerator and denominator are raised to the power specified
        """

        return Fraction(pow(self.numerator, power), pow(self.denominator, power))

    def get_fraction_to_become_one(self):
        """ Gets the fraction that makes the current fraction + the new fraction equal to one
            for instance if the current fraction is 3/4 then 1 - 3/4 the new fraction would be 1/4
     
            Returns:
                Fraction: a new Fraction where the current fraction + the new fraction equals one
        """

        return Fraction(self.denominator - self.numerator, self.denominator)

    def __str__(self):
        """ Formats the Fraction in this form "numerator/denominator"
     
            Returns:
                str: "numerator/denominator"- looks like this when printed 1/4 (if numerator was 1 and denominator was 4)
        """

        return f"{self.numerator}/{self.denominator}"