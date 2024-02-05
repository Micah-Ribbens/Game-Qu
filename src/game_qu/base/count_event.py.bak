
class CountEvent:
    """ An event that keeps track how many times an action should be performed. Unless otherwise specified, the function
        calls have no impact on the value of 'times_needed_to_complete.' This guarantees that the event is revertable
        meaning that calling reset() will put the 'current_count' to 'times_needed_to_complete.' Also
        the event can be activated and disabled. If it is disabled, boolean method calls will always return False and
        the event is no longer mutable."""

    count_needed = 0
    current_count = 0
    is_infinite = False  # Whether this count event can be completed (is a finite number or an infinite number)
    is_active = True

    def __init__(self, count_needed):
        """ Initializes the object

            Args:
                count_needed (int): the number of times this event must happen to be done"""

        self.count_needed = count_needed
        self.current_count = count_needed

    def set_times_needed_to_complete(self, count_needed):
        """ Sets 'count needed' to the value provided. If you want the current count to update call 'reset()'

            Args:
                count_needed (int): the number of times this event must happen to be done"""

        if self.is_active:
            self.count_needed = count_needed

    def increase_times_needed_to_complete(self, amount):
        """Increases the count by amount"""

        if self.is_active:
            self.current_count += amount

    def decrease_times_needed_to_complete(self, amount):
        """Decreases the count by amount"""

        if self.is_active:
            self.current_count -= amount

    def mutate_times_needed_to_complete(self, amount):
        """ Increases the count by amount (if it is negative, then count is decreased). This is the same as calling
            'increase_times_needed_to_complete,' but adding a negative number to an increase method does not make
            logical sense as far as an API perspective."""

        if self.is_active:
            self.increase_times_needed_to_complete(amount)

    def increment(self):
        """Increments count by 1"""

        if self.is_active:
            self.current_count += 1

    def decrement(self):
        """Decrements count by 1"""

        if self.is_active:
            self.current_count -= 1

    def is_done(self):
        """Whether the amount of times this event must happen to be done is less than or equal to 0"""

        return (self.current_count <= 0 or self.is_infinite) and self.is_active

    def is_done_this_cycle(self):
        """Whether the count is equal to 0"""

        return self.current_count == 0 and self.is_active

    def reset(self):
        """ Resets the event, so the count is set to what the user specified in either
            the __init__ method or the 'set_times_needed_to_complete;' the most recent call is chosen"""

        if self.is_active:
            self.current_count = self.count_needed

    def set_is_active(self, is_active):
        """ Sets whether this Event is active. If it is not active, all functions that return a boolean will return False
            and the event cannot be mutated. If it is active, all operations behave 'normally'"""

        self.is_active = is_active

    def activate(self):
        """ Activates this function. If it is not active, all functions that return a boolean will return False and the
            event cannot be mutated. If it is active, all operations behave 'normally'"""

        self.set_is_active(True)

    def disable(self):
        """ Activates this function. If it is not active, all functions that return a boolean will return False and the
            event cannot be mutated. If it is active, all operations behave 'normally'"""

        self.set_is_active(False)

    def get_is_active(self):
        """
             Returns:
            boolean; whether the function is active. If it is not active, all functions that return a boolean
            will return False and the event cannot be mutated. If it is active, all operations behave 'normally'"""

        return self.is_active

    def set_is_infinite(self, is_infinite):
        """Sets whether this event is infinite (if it is infinite it cannot be completed)"""

        self.is_infinite = is_infinite

    def make_finite(self):
        """Makes this event finite (meaning it can be completed)"""

        self.set_is_infinite(False)

    def make_infinite(self):
        """Makes this event infinite (it cannot be completed)"""

        self.set_is_infinite(True)

    def get_is_infinite(self):
        """
             Returns:
            boolean; whether this event is infinite (if it is infinite it cannot be completed)"""

        return self.is_infinite

    def current_count_is_positive(self):
        """
             Returns:
                boolean: whether the positive (count > 0)"""

        return self.current_count > 0 and self.is_active

    def current_count_is_negative(self):
        """
             Returns:
                boolean: whether the count is negative (count < 0)"""

        return self.current_count < 0 and self.is_active
    
    def get_count_needed(self):
        """
             Returns:
                int: the number of times this event must happen to be done"""

        return self.count_needed

    def get_current_count(self):
        """
             Returns:
                int: the current count of this event"""

        return self.current_count
