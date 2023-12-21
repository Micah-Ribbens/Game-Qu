class Range:
    """Stores the information for a start and end of a range (1-5)"""

    start = 0
    end = 0

    def __init__(self, start, end):
        """Initializes the object"""

        self.start = start
        self.end = end

    def is_less_than(self, other_range):
        """:returns: bool; if this range's start is less than the other range's start"""

        starts_are_equal = self.start == other_range.start
        return_value = None

        if starts_are_equal:
            return_value = self.end < other_range.end

        else:
            return_value = self.start < other_range.start

        return return_value

    def get_length(self):
        """:returns: float; the length of the range (end - start)"""

        return self.end - self.start

    def __str__(self):
        """Gives the string representation of the range"""

        return f"{self.start} -> {self.end}"

    def __contains__(self, number):
        """:returns: bool; if the number is within the range- greater than start and less than end"""

        return number >= self.start and number <= self.end