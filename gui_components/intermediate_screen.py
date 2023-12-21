from game_qu.base.colors import white
from game_qu.base.utility_functions import get_index_of_range, get_ranges
from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.events import TimedEvent
from game_qu.base.important_variables import BACKGROUND_COLOR, SCREEN_LENGTH, SCREEN_HEIGHT
from game_qu.gui_components.screen import Screen
from game_qu.gui_components.text_box import TextBox

from game_qu.base.range import Range
from game_qu.base.velocity_calculator import VelocityCalculator


class IntermediateScreen(Screen):
    """A screen that displays text(s) for a period of time"""

    time_ranges = []
    current_time = 0
    max_time = 0
    screens = []
    texts = []
    set_screen_text_function = None
    is_being_displayed = False

    def __init__(self, number_of_screens=1, screens=None, texts=[""], times_displayed=[0], set_screen_text_function=None):
        """Initializes the object"""

        if screens is None:
            self.create_screens(number_of_screens, texts)

        else:
            self.screens = screens

        self.set_time_ranges(get_ranges(times_displayed))

        self.set_screen_text_function = self.set_screen_text if set_screen_text_function is None else set_screen_text_function

        Dimensions.__init__(self, 0, 0, SCREEN_LENGTH, SCREEN_HEIGHT)

    def create_screens(self, number_of_screens, texts):
        """Initializes all the screens (equal to the number_of_screens)"""

        for x in range(number_of_screens):
            screen = Screen()

            text_box = TextBox(texts[x], 30, BACKGROUND_COLOR, white, True)
            text_box.number_set_dimensions(0, 0, SCREEN_LENGTH, SCREEN_HEIGHT)
            screen.components = [text_box]
            self.screens.append(screen)

    def set_texts(self, texts):
        """Sets the texts of all the screens in 'self.screens.' It does this by using the method 'self.change_screen_method,' which is set in the __init__ method"""

        for x in range(len(texts)):
            self.set_screen_text_function(self.screens[x], texts[x])
    
    def set_screen_text(self, screen, text):
        """Sets the text the screen displays (or no text if that is wanted). Calls the 'set_text' method of the screen's first component"""

        # By default, the screen's first component is the TextBox containing the text
        screen.components[0].set_text(text)
        
    def display(self):
        """Displays all the intermediate screens and sets 'self.current_time' to 0 resetting the screen timers"""

        self.current_time = 0
        self.is_being_displayed = True

    def get_components(self):
        """:returns: Component[]; the components that should be displayed"""

        index = get_index_of_range(self.current_time, ranges=self.time_ranges)
        self.screens[index].render_background()
        return self.screens[index].get_components()

    def reset(self):
        """Resets the object back to the start"""

        self.current_time = 0
        self.is_being_displayed = False

    def set_time_ranges(self, time_ranges):
        """ Sets the time ranges that each screen is displayed (from 1 second to 3 seconds). If using range_lengths is wanted then
            it is reccommended to use the function get_ranges in base/utility_functions.py"""

        self.time_ranges = time_ranges
        self.max_time = 0

        for time_range in time_ranges:
            self.max_time += time_range.get_length()

    def has_finished(self):
        """:returns: bool; if the intermediate screens are done being displayed"""

        return self.current_time > self.max_time or not self.is_being_displayed

    def run(self):
        """Runs all the code necessary to make this object work properly"""

        if not self.has_finished():
            self.current_time += VelocityCalculator.time
            index = get_index_of_range(self.current_time, ranges=self.time_ranges)
            self.screens[index].run()

