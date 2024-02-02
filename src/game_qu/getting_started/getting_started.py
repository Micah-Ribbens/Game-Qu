""" # Summary
This game engine is compartmentalized. There is almost total freedom for making games with this engine.
Components like collision detection, rendering, etc. can be used as is, replaced, or modified. There is
physics, a simple GUI structure, math representation for calculus, vectors, and more. The most important thing to
understand is how the GUI structure works. There are three main classes that every GUI component uses or inherits from:
Component, Screen, and game_window. The main idea behind having components and screens is that a component has behavior
that is independent of the screen (the player's movement as one example). The screen, on the other hand, defines the interactions
among the components. For instance, when an enemy hits the player, the player gets damaged. Below they will be described in detail:

## Component
This is the base class for all GUI components. The goal of a component is for it to be a part of a screen. For
instance, in pong, the paddles and ball would be components of the screen.
- Dimensions of the component: 'left_edge,' 'top_edge,' 'length,' and 'height'
- 'color' - the color of the rectangle that is rendered onto the screen for the component. This only matters if 'path_to_image' is set to
''. Otherwise, the image will be rendered onto the screen.
- 'path_to_image' - the path to the image that will be rendered onto the screen for the component.
- run() method - this method is called every game cycle and it is where the game logic is put. The method is called before render()
- render() method - this method is called every game cycle and is where the rendering logic is put. The method is called after run()

## Screen
This is the base class for all screens. Each screen has a list of components that are on it. The screen's run() and
render() methods are called and then each run and render() method of each component is called.
- 'components' - the list of components that are on the screen
- get_components() method - returns the list of components that are on the screen (by default, it returns the 'components' attribute)
- run() method - this method is called every game cycle and it is where the game logic is put. The method is called before render()
- render()/render_background() - renders the screen (usually the background)
- 'path_to_image' - the path to the image that will be rendered onto the screen for the component.
- 'color' - the color of background. This only matters if 'path_to_image' is set to ''. Otherwise, the image will be rendered onto the screen.

## game_window (Instance of the Window class)
This variable holds all the screens. It can display multiple screens every game cycle, but it usually makes sense to only
display one.
- display_screen() method - displays the screen that is passed in as an argument
- add_screen() method - adds the screen that is passed as an argument to the list of screens that the game_window holds
- stop_rendering() method - stops rendering the game (helpful if the game stays the same over multiple game cycles - a pause menu).
- continue_rendering() method - continues rendering the game

Click 'Expand Source Code' to see an example of how to use the methods simply. The code below will be two simple 'games'"""

# All the import statements we need for this "simple" game
from game_qu.base.game_runner_function import run_game
from game_qu.base.important_constants import SCREEN_LENGTH
from game_qu.base.important_variables import KEY_D, KEY_A, KEY_W, KEY_S, game_window, KEY_ESCAPE
from game_qu.base.utility_functions import key_is_clicked, key_is_pressed
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.component import Component
from game_qu.gui_components.screen import Screen
from game_qu.base.colors import *
from game_qu.gui_components.text_box import TextBox


# Now onto game number one (the player can move horizontally)
class Game1Screen(Screen):
    player = Component()
    player_velocity = VelocityCalculator.get_velocity(SCREEN_LENGTH, 800)

    def __init__(self):
        super().__init__("", light_gray)
        self.player.set_color(magenta)
        self.player.percentage_set_dimensions(50, 50, 30, 30)
        self.components = [self.player]

    def run(self):
        if key_is_pressed(KEY_D):
            self.player.left_edge += VelocityCalculator.get_distance(self.player_velocity)

        if key_is_pressed(KEY_A):
            self.player.left_edge -= VelocityCalculator.get_distance(self.player_velocity)


# Now onto game number two (the player can move vertically)
class Game2Screen(Screen):
    player = Component()
    player_velocity = VelocityCalculator.get_velocity(SCREEN_LENGTH, 800)

    def __init__(self):
        super().__init__("", light_gray)
        self.player.percentage_set_dimensions(50, 50, 30, 30)
        self.player.set_color(purple)
        self.components = [self.player]

    def run(self):
        if key_is_pressed(KEY_W):
            self.player.top_edge += VelocityCalculator.get_distance(self.player_velocity)

        if key_is_pressed(KEY_S):
            self.player.top_edge -= VelocityCalculator.get_distance(self.player_velocity)

# The main screen would be the way to get to the two other screens
class MainScreen(Screen):
    game1_text_box = TextBox("Game1", 25, white, black, True)
    game2_text_box = TextBox("Game2", 25, white, black, True)
    is_currently_visible = True
    game1_screen = None
    game2_screen = None

    def __init__(self, game1_screen, game2_screen):
        super().__init__("", light_gray)
        self.components = [self.game1_text_box, self.game2_text_box]
        self.game1_text_box.percentage_set_dimensions(20, 20, 28, 30)
        self.game2_text_box.percentage_set_dimensions(52, 20, 28, 30)

        self.game1_screen = game1_screen
        self.game2_screen = game2_screen

    def run(self):
        # You can go to the other screens from this screen, so that is what we are doing here
        if self.game1_text_box.got_clicked():
            game_window.display_screen(self.game1_screen)
            self.is_currently_visible = False

        if self.game2_text_box.got_clicked():
            game_window.display_screen(self.game2_screen)
            self.is_currently_visible = False

        if key_is_clicked(KEY_ESCAPE):
            game_window.display_screen(self)
            self.is_currently_visible = True

        # So this screen's run method code is always called
        self.show()

    def render_background(self):
        # Only if this is the screen that should be rendered should the background be rendered
        if self.is_currently_visible:
            super().render_background()

    def get_components(self):
        # Only if this is the screen that should be rendered should the components be returned (and those rendered)
        if self.is_currently_visible:
            return self.components

        return []


if __name__ == "__main__":
    # Initializing the screens
    game1_screen = Game1Screen()
    game2_screen = Game2Screen()
    main_screen = MainScreen(game1_screen, game2_screen)

    # Making sure the window has all the screens
    game_window.add_screen(game1_screen)
    game_window.add_screen(game2_screen)
    game_window.add_screen(main_screen)
    game_window.display_screen(main_screen)

    # Running the game
    run_game(main_screen)