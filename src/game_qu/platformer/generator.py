import random

from game_qu.base.important_variables import SCREEN_HEIGHT, SCREEN_LENGTH
from game_qu.base.paths import Path
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.math.point import Point
from game_qu.platformer.player import Player
from game_qu.platformer.platform import Platform


class Generator:
    """Generates platforms, enemies, and other things semi-randomly (as long as it is playable for the player and mantains a good difficulty)"""

    player = None
    
    # Modifiable Constants
    margins_of_error = Path(Point(0, 20), [Point(20, 15), Point(40, 10), Point(60, 8), Point(70, 7),
                                           Point(80, 4), Point(90, 3), Point(100, 0)])
    max_vertical_change = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 50)
    side_scrolling_start_distance = VelocityCalculator.get_dimension(SCREEN_LENGTH, 33)
    minimum_platform_length_visible = VelocityCalculator.get_dimension(SCREEN_LENGTH, 20)
    minimum_generator_accuracy_decrease = 0.05
    minimum_platform_height = int(VelocityCalculator.get_dimension(SCREEN_HEIGHT, 10))
    maximum_platform_height = int(VelocityCalculator.get_dimension(SCREEN_HEIGHT, 20))
    minimum_platform_length = int(VelocityCalculator.get_dimension(SCREEN_LENGTH, 45))
    maximum_platform_length = int(VelocityCalculator.get_dimension(SCREEN_LENGTH, 55))

    def __init__(self, player: Player):
        self.player = player

    # Functions that game uses (aren't just for tests)
    def _get_accuracy(self, difficulty):
        """
            Returns:
                double: how accurate the player has to be (1 - margin_of_error)"""

        # self.margins_of_error are in percentages
        return 1 - ( self.margins_of_error.get_y_coordinate(difficulty) / 100 )

    def _get_bottommost_top_edge(self, last_platform, platform_height):
        """
            Returns:
                double: the generated platform's bottommost top_edge (must stay within the screen)"""

        return_value = last_platform.top_edge + self.max_vertical_change

        # The platform's bottom must be visible
        if return_value + platform_height >= SCREEN_HEIGHT:
            return_value = SCREEN_HEIGHT - platform_height

        return return_value

    def get_platform_within_screen(self, last_platform: Platform, next_platform: Platform):
        """
            Returns: 
                Platform: the updated 'platform' that is within the screen meaning when the player gets to the edge
                of 'last_platform' they can see a good amount of the next platform"""

        last_platform_length_left = last_platform.right_edge - self.side_scrolling_start_distance

        next_platform_length_visible = SCREEN_LENGTH - next_platform.left_edge
        # Have to add that because side scrolling will increase how much of the platform is visible
        next_platform_length_visible += last_platform_length_left

        if next_platform_length_visible < self.minimum_platform_length_visible:
            difference = self.minimum_platform_length_visible - next_platform_length_visible
            next_platform.left_edge -= difference

        return next_platform

    def generate_platform(self, last_platform, difficulty):
        """
            Returns:
                Platform: the next platform, which would be after 'last_platform;' uses the difficulty to decide how hard of a jump it should be"""

        accuracy = self._get_accuracy(difficulty)
        new_platform_height = random.randint(self.minimum_platform_height, self.maximum_platform_height)

        topmost_top_edge = self.player.get_topmost_top_edge(last_platform, accuracy, self._get_accuracy(1))
        bottommost_top_edge = self._get_bottommost_top_edge(last_platform, new_platform_height)
        new_platform_top_edge = random.randint(int(topmost_top_edge), int(bottommost_top_edge))

        new_platform_length = random.randint(self.minimum_platform_length, self.maximum_platform_length)

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, new_platform_top_edge)

        max_distance = self.get_horizontal_distance(max_vertical_time, accuracy)
        min_distance = self.get_horizontal_distance(max_vertical_time, accuracy - self.minimum_generator_accuracy_decrease)
        distance = random.randint(int(min_distance), int(max_distance))

        new_platform_left_edge = last_platform.right_edge + distance
        platform = Platform(new_platform_left_edge, new_platform_top_edge, new_platform_length, new_platform_height)

        return self.get_platform_within_screen(last_platform, platform)

    def get_horizontal_distance(self, vertical_time, accuracy):
        """
            Returns:
                double: the horizontal distance apart the old platform and the new one should be"""

        # 2 * player's length because one of them comes from the player not being affected by gravity until its
        # left_edge > the last platform's right edge and other one because they can land on the new platform when
        # the right_edge is > the new platform's left_edge
        return vertical_time * self.player.max_horizontal_velocity * accuracy + self.player.length * 2

    # Just for tests
    def get_hardest_platform(self, last_platform, difficulty):
        """
            Returns:
                Platform: the hardest platform possible at this difficulty"""

        accuracy = self._get_accuracy(difficulty)
        platform_height = random.randint(self.minimum_platform_height, self.maximum_platform_height)

        platform_top_edge = self.player.get_topmost_top_edge(last_platform, accuracy, self._get_accuracy(1))

        platform_length = random.randint(self.minimum_platform_length, self.maximum_platform_length)

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, platform_top_edge)

        platform_left_edge = last_platform.right_edge + self.get_horizontal_distance(max_vertical_time, accuracy)

        platform = Platform(platform_left_edge, platform_top_edge, platform_length, platform_height)

        return self.get_platform_within_screen(last_platform, platform)

    def get_easiest_platform(self, last_platform, difficulty):
        """
            Returns:
                Platform: the easiest platform possible at this difficulty"""

        accuracy = self._get_accuracy(difficulty)
        platform_height = random.randint(self.minimum_platform_height, self.maximum_platform_height)
        platform_top_edge = self._get_bottommost_top_edge(last_platform, platform_height)

        platform_length = random.randint(self.minimum_platform_length, self.maximum_platform_length)

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, platform_top_edge)
        platform_left_edge = last_platform.right_edge + self.get_horizontal_distance(max_vertical_time, accuracy)

        if platform_left_edge + platform_length > SCREEN_LENGTH:
            platform_left_edge = SCREEN_LENGTH - platform_length

        return Platform(platform_left_edge, platform_top_edge, platform_length, platform_height)




