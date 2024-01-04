"""This is an example of a simple platformer made using the game engine. Click the see 'Expand Source Code' button below
to see the code."""

# This must be before the other imports, so we can actually modify the constants. Otherwise, the constants will remain the
# same as the default values.
from game_qu.base.library_changer import LibraryChanger
from game_qu.base.colors import *

LibraryChanger.set_game_library("pygame")
LibraryChanger.set_screen_dimensions(1000, 600)
LibraryChanger.set_background_color(black)

# The rest of the imports
from game_qu.base.important_variables import *
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.base.game_runner_function import run_game
from game_qu.base.paths import Path
from game_qu.math.point import Point
from game_qu.platformer.enemy import Enemy
from game_qu.platformer.platform import Platform
from game_qu.platformer.platformer_screen import PlatformerScreen
from game_qu.platformer.player import Player
from game_qu.gui_components.component import Component


class SimplePlayer(Player):
    """A simple player"""

    eye1 = None
    eye2 = None
    mouth = None

    def __init__(self, left_key, right_key, jump_key, down_key, attack_key):
        """Initializes the object"""

        super().__init__(left_key, right_key, jump_key, down_key, attack_key)
        self.set_color(gray)

        self.eye1 = Component("")
        self.eye2 = Component("")
        self.mouth = Component("")

        self.eye1.set_color(blue)
        self.eye2.set_color(blue)
        self.mouth.set_color(red)

    def render(self):
        """Renders this object onto the screen"""

        super().render()

        # Settings all the dimensions of the subcomponents for rendering (eyes and mouth)
        self.eye1.set_dimensions_within_component(25, 20, 20, 20, self)
        self.eye2.set_dimensions_within_component(55, 20, 20, 20, self)
        self.mouth.set_dimensions_within_component(10, 70, 80, 10, self)

        # Rendering the subcomponents
        self.eye1.render()
        self.eye2.render()
        self.mouth.render()


class SimpleEnemy(Enemy):
    """A simple enemy that moves back and forth across the platform"""

    eye = None

    def __init__(self, platform):
        """Initializes the object"""

        super().__init__(30, 20, platform, "")
        self.set_color(black)

        self.eye = Component("")
        self.eye.set_color(red)

    def get_point_value(self):
        return 100

    def render(self):
        """Renders this component onto the game"""

        super().render()
        self.eye.set_dimensions_within_component(0, 30, 100, 10, self)
        self.eye.render()


class SimplePlatform(Platform):
    """A simple platform"""

    grass = None

    def __init__(self):
        """Initializes the object"""

        super().__init__()
        self.set_color(brown)

        self.grass = Component("")
        self.grass.set_color(green)

    def render(self):
        """Renders this component onto the game"""

        super().render()
        self.grass.set_dimensions_within_component(0, 0, 100, 20, self)
        self.grass.render()


class MainScreen(PlatformerScreen):
    """The main screen of the game"""

    score_to_game_difficulty = Path(Point(0, 50), [Point(1000, 70), Point(1650, 95), Point(5000, 100),
                                    Point(float("inf"), 100)])

    # Here we will be implementing the abstract methods and modifying some methods to get what we want
    def get_enemy_types(self):
        """
            Returns:
                list[Enemy]: all the types of enemies that can be generated
        """

        return [SimpleEnemy]

    def get_game_difficulty(self):
        """
            Returns:
                float: the difficulty of the game based on the score of the player (from 0 to 100 with 100 being the hardest)
        """

        return self.score_to_game_difficulty.get_y_coordinate(self.player_score)

    def get_score_from_passing_platform(self):
        """
            Returns:
                int: the score from passing a platform
        """

        return 100

    def get_start_platform_coordinates(self):
        """
            Returns:
                list[float]: {left_edge, top_edge, length, height} of the start platform
        """

        return [0,
                VelocityCalculator.get_dimension(SCREEN_HEIGHT, 85),
                VelocityCalculator.get_dimension(SCREEN_LENGTH, 50),
                VelocityCalculator.get_dimension(SCREEN_HEIGHT, 15)]

    def get_players(self):
        """
            Returns:
                list[Player]: the players of the game
        """

        return [SimplePlayer(KEY_A, KEY_D, KEY_W, KEY_S, KEY_F)]


if __name__ == "__main__":
    # Finally running the game
    run_game(MainScreen())
