from abc import ABC, abstractmethod

from game_qu.base.library_independant_utility_functions import get_kwarg_item
from game_qu.base.velocity_calculator import VelocityCalculator


class FollowablePath(ABC):
    """An interface that defines the behavior of a path that is followable"""

    game_object = None
    current_time = 0
    is_started = False
    attribute_modifying = None
    max_time = 0
    last_time = 0
    last_delta_time = 0
    has_max_time = False

    def __init__(self, **kwargs):
        """ Initializes the object

            Args:
                game_object (GameObject): the game object that is following this path
                attribute_modifying (str): the name of the attribute this path is modifying
                max_time (float): the max time of the path - the time the path should end (None if the path should not end)
     
            Returns:
                None
        """

        self.game_object = get_kwarg_item(kwargs, "game_object", None)
        self.attribute_modifying = get_kwarg_item(kwargs, "attribute_modifying", "")
        self.max_time = get_kwarg_item(kwargs, "max_time", 0)
        self.has_max_time = kwargs.get("max_time") is not None

    def run(self, is_reset_event=False, is_start_event=False, is_changing_attribute=False):
        """Updates the time of the followable path and the player's attribute if it was told to"""

        self.last_time = self.current_time

        # It should not be started again if it has already been started because starting puts the current_time back to 0
        if is_start_event and not self.is_started:
            self.start()

        if is_reset_event:
            self.reset()

        if self.is_started:
            self.current_time += VelocityCalculator.time

        can_change_attribute = self.is_started and self.game_object is not None

        should_change_attribute = can_change_attribute and is_changing_attribute

        self.last_delta_time = self.current_time - self.last_time

        # If the attribute should be changed, then this will change it
        if should_change_attribute:
            self.game_object.__dict__[self.attribute_modifying] += self.get_delta_value(self.last_time, self.current_time)

    def reset(self):
        """Ends and resets the path"""

        self.is_started = False
        self.current_time = 0
        self.last_time = 0

    def is_done(self, should_reset=False):
        """
             Returns:
                bool: if the path is finished (and if 'should_reset' it will reset it)"""

        return_value = self.current_time >= self.max_time and self.has_max_time

        if should_reset and return_value:
            self.reset()

        return return_value

    def has_finished(self):
        """
             Returns:
                bool: if the path has either not started or is done"""

        return not self.is_started or self.is_done()

    def start(self):
        """Starts the followable path"""

        self.is_started = True
        self.current_time = 0
        self.last_time = 0

    def restart(self):
        """Restarts the path (same as start, but sounds more clear)"""

        self.start()

    @abstractmethod
    def get_value_at_time(self, time):
        """
             Returns:
                object: the value of the attribute this path is modifying at 'time'"""
        pass

    @abstractmethod
    def get_delta_value(self, start_time, end_time):
        """
             Returns:
                object: the delta value of the attribute within the domain [start_time, end_time]"""
        pass

    def get_current_value(self):
        return self.get_value_at_time(self.current_time)

    def get_current_time(self):
        return self.current_time

    def set_has_max_time(self, has_max_time):
        self.has_max_time = has_max_time
