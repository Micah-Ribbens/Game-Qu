from game_qu.base.velocity_calculator import VelocityCalculator


class TimedEvent:
    """Used for events that are completed within a certain time frame"""

    current_time = 0
    is_started = False
    time_needed = 0
    restarts_upon_completion = False

    # Stores if the TimedEvent is done for that cycle since it should be known for at least one cycle
    variable_is_done = False

    def __init__(self, time_needed: int, restarts_upon_completion: bool = False) -> None:
        """ Initializes the object by modifying the attributes with the values provided

            Args:
                time_needed (int): the time it takes for the TimedEvent to end
                restarts_upon_completion (bool): whether the TimedEvent restarts when it has finished (if it does not
                restart it will stay paused until 'self.start()' is called)
     
            Returns:
                None
        """

        self.time_needed = time_needed
        self.restarts_upon_completion = restarts_upon_completion


    def run(self, should_reset=False, should_start=False) -> None:
        """ If the TimedEvent is_started then the current_time increases by the time it took the current cycle to run.
            Then it does various things depending on the values provided (see params)

            Args:
                should_reset (bool): the event that if True resets the current_time to 0 and stops the TimedEvent
                should_start (bool): the event that if True starts the TimedEvent
     
            Returns:
                None
        """

        # The variable is done was True last cycle meaning it should be False again (enough time was given to get the value)
        if self.variable_is_done:
            self.variable_is_done = False

        if should_reset:
            self.reset()

        if should_start and not self.is_started:
            self.start()

        if self.is_started:
            self.current_time += VelocityCalculator.time

        if self.current_time >= self.time_needed and self.is_started:
            self.variable_is_done = True

        if self.current_time >= self.time_needed and self.restarts_upon_completion:
            self.start()
            self.current_time = 0

    def start(self):
        """Starts the TimedEvent (sets is_started to True and sets the current_time to 0)"""

        self.current_time = 0
        self.is_started = True
        self.variable_is_done = False

    def reset(self):
        """Resets the TimedEvent (sets is_started to False and the current_time to 0)"""

        self.current_time = 0
        self.is_started = False
        self.variable_is_done = False

    def is_done(self) -> bool:
        """ Returns:
                bool: if the event has started and the current time is greater than the time needed"""

        return self.variable_is_done

    def has_finished(self) -> bool:
        """ Returns:
                bool: if the event has either not started or is done"""

        return not self.is_started or self.is_done()

    def set_time_needed(self, time_needed):
        """Sets how much time is needed for this timed event to be completed"""

        self.time_needed = time_needed

    def set_restarts_upon_completion(self, restarts_upon_completion):
        """Sets whether the timed event restarts after the time limit is reached"""

        self.restarts_upon_completion = restarts_upon_completion
