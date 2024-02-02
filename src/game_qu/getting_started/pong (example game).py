"""This is an example of a simple game of pong made using the game engine. Click the see 'Expand Source Code' button below
to see the code."""

from game_qu.base.library_changer import LibraryChanger
from game_qu.base.colors import *

# This must be before the other imports, so we can actually modify the constants. Otherwise, the constants will remain the
# same as the default values.
LibraryChanger.set_game_library("pygame")
LibraryChanger.set_screen_dimensions(800, 600)
LibraryChanger.set_background_color(black)

# The rest of the imports
from game_qu.gui_components.screen import Screen
from game_qu.gui_components.component import Component
from game_qu.gui_components.text_box import TextBox
from game_qu.base.important_variables import *
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.base.utility_functions import key_is_pressed, render_ellipse
from game_qu.math.vector_2d import Vector2D
from game_qu.base.engines import CollisionsEngine
from game_qu.base.game_runner_function import run_game
import math


class Player(Component):
    """The paddles of the game of Pong"""

    up_key = None
    down_key = None
    velocity = VelocityCalculator.get_velocity(SCREEN_HEIGHT, 2000)
    length = VelocityCalculator.get_dimension(SCREEN_LENGTH, 3.5)
    height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 33)

    def __init__(self, up_key, down_key, base_left_edge, color):
        """Initializes the object"""

        super().__init__()
        self.set_color(color)

        self.up_key = up_key
        self.down_key = down_key
        self.left_edge = base_left_edge

        self.reset()

    def run(self):
        """Runs the movement of the player"""

        if key_is_pressed(self.up_key):
            self.top_edge -= VelocityCalculator.get_distance(self.velocity)

        if key_is_pressed(self.down_key):
            self.top_edge += VelocityCalculator.get_distance(self.velocity)

        self.top_edge = max(0, self.top_edge)
        self.top_edge = min(SCREEN_HEIGHT - self.height, self.top_edge)

    def reset(self):
        """Resets all the variables to the start of the game"""

        middle_of_screen = (SCREEN_HEIGHT - self.height) / 2
        self.top_edge = middle_of_screen


class Ball(Component):
    """The ball of the game pong"""

    base_velocity = VelocityCalculator.get_velocity(SCREEN_LENGTH, 700)
    velocity = base_velocity

    # The velocity increases by 5% every time it hits the ball
    velocity_multiplier = 1.05

    length = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 6)
    height = length
    vector = None

    def __init__(self):
        """Initializes the object"""

        super().__init__()
        self.reset()  # Sets the variables to the start of the game

    def reset(self):
        """Resets all the variables so they are the same as the start of the game"""

        self.left_edge = SCREEN_LENGTH / 2
        self.top_edge = SCREEN_HEIGHT / 2
        self.velocity = self.base_velocity
        self.vector = Vector2D(math.pi / 4, 1).normalize()  # A 45-degree angle upwards

        self.set_color(white)

    def run(self):
        """Moves the ball across the screen"""

        # First move the ball
        displacement_vector = self.vector.get_vector_multiplied_by_scalar(VelocityCalculator.delta_time * self.velocity)
        self.left_edge += displacement_vector.get_x_magnitude()
        self.top_edge += displacement_vector.get_y_magnitude()

        # Then check if the ball has hit the top or bottom of the screen. This should be after movement, so the ball is
        # always rendered within the screen (rendering is called after the run method)
        if self.top_edge < 0:
            self.vector.set_y_magnitude(-self.vector.get_y_magnitude())
            self.top_edge = 0

        if self.bottom_edge > SCREEN_HEIGHT:
            self.vector.set_y_magnitude(-self.vector.get_y_magnitude())
            self.set_bottom_edge(SCREEN_HEIGHT)

    def change_horizontal_direction(self):
        """Changes the horizontal direction of the ball"""

        self.vector.set_x_magnitude(-self.vector.get_x_magnitude())
        self.velocity *= self.velocity_multiplier

    def render(self):
        """Renders the ball onto the screen (renders a circle instead of the default rectangle)"""

        render_ellipse(self.left_edge, self.top_edge, self.length, self.height, self.color)


class MainScreen(Screen):
    """The main screen of the game. This is where the game is played"""

    # The game objects
    player1 = Player(KEY_W, KEY_S, 0, blue)
    player2 = Player(KEY_UP, KEY_DOWN, SCREEN_LENGTH - Player.length, red)
    ball = Ball()

    # Keeping track of the score
    player1_score = 0
    player2_score = 0
    score_text_box = TextBox("", 35, light_gray, black, True)

    def __init__(self):
        """Initializes the object"""

        super().__init__("", light_gray)
        self.update_score_text_box()
        self.score_text_box.set_is_rendering_background(False)  # So the text does not have a background color under it
        self.score_text_box.percentage_set_dimensions(20, 0, 60, 10)

        # The order of the items in the list affects the order that their run method and render methods are called. The
        # text box should be run and rendered first so the ball and players can be rendered on top of it.
        self.components = [self.score_text_box, self.player1, self.player2, self.ball]

    def run(self):
        """Runs all the collision logic"""

        if CollisionsEngine.is_collision(self.ball, self.player1):
            self.ball.change_horizontal_direction()
            self.ball.set_color(self.player1.get_color())
            self.ball.set_left_edge(self.player1.right_edge)

        if CollisionsEngine.is_collision(self.ball, self.player2):
            self.ball.change_horizontal_direction()
            self.ball.set_color(self.player2.get_color())
            self.ball.set_right_edge(self.player2.left_edge)

        if self.ball.right_edge < 0:
            self.player2_score += 1
            self.update_score_text_box()

        if self.ball.left_edge > SCREEN_LENGTH:
            self.player1_score += 1
            self.update_score_text_box()

    def update_score_text_box(self):
        """Updates the score of the score that the game displays"""

        score_text = f"Player1: {self.player1_score}     Player2: {self.player2_score}"
        self.score_text_box.set_text(score_text)

        self.player1.reset()
        self.player2.reset()
        self.ball.reset()


if __name__ == "__main__":
    # Finally running the game
    run_game(MainScreen())
