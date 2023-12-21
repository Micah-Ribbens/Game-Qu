from game_qu.base.events import Event, TimedEvent
from game_qu.library_abstraction import keys
from game_qu.library_abstraction import utility_functions
from game_qu.library_abstraction import variables
from game_qu.base.important_constants import IS_USING_CONTROLLER
from game_qu.base.library_changer import LibraryChanger


class Keyboard:
    """ A class that has key_events and key_timed_events that are used to find key states like how long a key was held in,
        if a key was released, etc. Generally it is recommended to use the functions from game_qu.base/utility_functions.py
        but the key_events and key_timed_events from this class can also be used."""

    key_events = []
    key_timed_events = []
    button_timed_events = {}
    button_events = {}
    mouse_clicked_event = Event()

    def __init__(self):
        """Initializes all the key events"""

        for x in range(len(keys.keys)):
            self.key_events.append(Event())
            self.key_timed_events.append(TimedEvent(0))

        # Currently this game engine does not support controllers for pyglet
        if LibraryChanger.current_library_name == "pygame":
            self.create_button_events()

    def create_button_events(self):
        """Creates all the button Events and TimedEvents"""

        for button in keys.buttons:
            self.button_events[button] = Event()
            self.button_timed_events[button] = TimedEvent(0)

    def get_key_timed_event(self, key):
        """:returns: TimedEvent; the TimedEvent associated with that key"""

        return_value = None

        if self.button_timed_events.get(key) is None:
            return_value = self.key_timed_events[key]

        else:
            return_value = self.get_button_timed_event(key)

        return return_value

    def get_key_event(self, key):
        """:returns: Event; the Event associated with that key"""

        return_value = None

        if self.button_events.get(key) is None:
            return_value = self.key_events[key]

        else:
            return_value = self.get_button_event(key)

        return return_value

    def get_button_event(self, button):
        """:returns: Event; the Event associated with that button"""

        return self.button_events[button]

    def get_button_timed_event(self, button):
        """:returns: TimedEvent; the TimedEvent associated with that button"""

        return self.button_timed_events[button]

    def run(self):
        """ Runs all the events in key_events and key_timed_events, so attributes about the keys can be viewed. This function
            SHOULD NOT be called by the user and this library automatically calls it"""

        self.mouse_clicked_event.run(utility_functions.mouse_was_pressed())

        for key in keys.keys:
            key_was_pressed = utility_functions.key_is_pressed(key)

            self.get_key_event(key).run(key_was_pressed)

            should_reset = not self.get_key_event(key).happened_last_cycle() and not key_was_pressed

            self.get_key_timed_event(key).run(should_reset, key_was_pressed)
        
        # If no controller is hooked up, then the buttons should not be run
        # Currently this game engine does not support controllers for pyglet
        # TODO make this more general purpose- have it work for multiple controllers
        if LibraryChanger.current_library_name == "pygame" and variables.joystick is not None and IS_USING_CONTROLLER:
            self.run_buttons()

    def run_buttons(self):
        """Runs all the button events, so important information can be gotten from them"""

        for button in keys.buttons:

            button_was_pressed = utility_functions.button_is_pressed(button)

            self.get_button_event(button).run(button_was_pressed)

            should_reset = not self.get_button_event(button).happened_last_cycle() and not button_was_pressed

            self.get_button_timed_event(button).run(should_reset, button_was_pressed)

