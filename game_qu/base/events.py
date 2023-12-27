from game_qu.base.history_keeper import HistoryKeeper
from game_qu.base.id_creator import id_creator
from game_qu.base.timed_event import TimedEvent
from game_qu.base.count_event import CountEvent


class Event:
    """Used to store an event from the current cycle and past cycles (event being anything that is a bool)"""

    happened_this_cycle = False
    name = ""
    is_active = True

    def __init__(self):
        """Initializes the object"""

        self.name = id_creator.get_unique_id()

    def run(self, happened_this_cycle):
        """ Uses HistoryKeeper.add() to store the event for the current cycle, which will be accessed by is_continuous()

            Args:
                happened_this_cycle (bool): the event from the current cycle
     
            Returns:
                None"""

        if self.is_active:
            self.happened_this_cycle = happened_this_cycle
            HistoryKeeper.add(happened_this_cycle, self.name, False)

    def happened_last_cycle(self):
        """ Uses HistoryKeeper.get_last() to get the event from the last cycle and see if it is True
     
            Returns:
                bool: if the event was True last cycle
        """

        return HistoryKeeper.get_last(self.name) and self.is_active

    def is_click(self):
        """
             Returns:
                bool: if the event is True this cycle and was not last cycle"""

        return not self.happened_last_cycle() and self.happened_this_cycle and self.is_active

    def has_stopped(self):
        """
             Returns:
                bool: if the event was True last cycle and is not True this cycle"""

        return self.happened_last_cycle() and not self.happened_this_cycle and self.is_active

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
                boolean: whether the function is active. If it is not active, all functions that return a boolean
                will return False and the event cannot be mutated. If it is active, all operations behave 'normally'"""

        return self.is_active
