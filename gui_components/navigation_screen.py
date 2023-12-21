from math import sqrt

from game_qu.base.colors import pleasing_green, white
from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.utility_functions import button_is_clicked, mouse_is_clicked
from game_qu.gui_components.grid import Grid
from game_qu.gui_components.screen import Screen
from game_qu.gui_components.text_box import TextBox
from game_qu.base.important_variables import *
from game_qu.base.utility_functions import game_button_is_clicked


class NavigationScreen(Screen):
    """ A screen that allows you to select different screens (navigate between different screens).
        By default, hitting escape brings you back to the main screen"""

    buttons = []
    screens = []
    selected_screen = None
    back_to_main_screen_game_button = KEY_ESCAPE
    button_color = pleasing_green
    screen_shortcut_game_buttons = {}

    def __init__(self, screen_names, screens, screen_shortcut_game_buttons={}, back_to_main_screen_game_button=KEY_ESCAPE, path_to_background_image="", button_color=button_color):
        """ Initializes the object with the values provided. It will create a grid with text boxes each containing a screen_name
            That will link to a specific screen (screen_names[0] -> screens[0])

            :parameter screen_names: str[]; the names of the screens that will be displayed
            :parameter screens: Screen[]; the screens, which the screen_names are referencing
            :parameter screen_shortcut_game_buttons: dict {game_button: Screen}. Game button can either be a key or
            button depending on whether IS_USING_CONTROLLER is true or not (if it is True game_button is a button otherwise it is a key)
            :parameter back_to_main_screen_game_button: game_button; the game_button that will bring the user back to the main screen
            :parameter path_to_background_image: str; the path to the background image of the navigation screen
            :parameter button_color: int[] {red, green, blue}; the rgb values of the buttons
        """

        super().__init__(path_to_background_image)
        self.screens = screens
        self.button_color = button_color
        self.screen_shortcut_game_buttons = screen_shortcut_game_buttons
        self.buttons = []

        for screen_name in screen_names:
            self.buttons.append(TextBox(screen_name, 18, pleasing_green, white, True))

        columns = int(sqrt(len(screen_names)))
        button_grid = Grid(Dimensions(0, 0, SCREEN_LENGTH, SCREEN_HEIGHT), columns, None)
        button_grid.turn_into_grid(self.buttons, None, None)

        self.components = self.buttons
        self.selected_screen = self
        self.back_to_main_screen_game_button = back_to_main_screen_game_button

    def run(self):
        """ Changes the currently displayed screen if the buttons were clicked, or the back_to_main_screen_game_button is clicked.
            It will also run the currently selected_screen's run method"""

        for x in range(len(self.buttons)):
            if self.buttons[x].got_clicked() and self.selected_screen == self:
                self.selected_screen = self.screens[x]

        for game_button in self.screen_shortcut_game_buttons.keys():
            if game_button_is_clicked(game_button):
                self.selected_screen = self.screen_shortcut_game_buttons.get(game_button)

        if game_button_is_clicked(self.back_to_main_screen_game_button):
            self.selected_screen = self

        if self.selected_screen != self:
            self.selected_screen.run()

    def render_background(self):
        """Renders the background of the currently selected screen"""

        if self.selected_screen != self:
            self.selected_screen.render_background()

        else:
            super().render_background()

    def get_components(self):
        """:returns: Component[]; the components of the currently selected_screen"""

        return self.components if self.selected_screen == self else self.selected_screen.get_components()

    def run_on_close(self):
        """Makes sure all the screen's run_on_close methods are called"""

        for screen in self.screens:
            screen.run_on_close()

    def modify_values(self, button_color=button_color, back_to_main_screen_game_button=back_to_main_screen_game_button):
        """Gives the ability to modify the values of the NavigationScreen"""

        self.button_color = button_color
        self.back_to_main_screen_game_button = back_to_main_screen_game_button

        for button in self.buttons:
            button.set_background_color(button_color)
