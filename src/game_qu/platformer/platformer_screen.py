import abc

from game_qu.base.id_creator import id_creator
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.engines import CollisionsEngine
from game_qu.base.history_keeper import HistoryKeeper
from game_qu.platformer.generator import Generator
from game_qu.platformer.gravity_engine import GravityEngine
from game_qu.platformer.platform import Platform
from game_qu.platformer.player import Player
from game_qu.gui_components.grid import Grid
from game_qu.platformer.health_bar import HealthBar
from game_qu.gui_components.hud import HUD
from game_qu.gui_components.intermediate_screen import IntermediateScreen
from game_qu.gui_components.screen import Screen
from game_qu.base.utility_functions import *
from game_qu.base.important_variables import *


class PlatformerScreen(Screen):
    """An endless platformer game"""

    players = []
    player_health_bars = []
    platforms = []
    game_objects = []
    collidable_objects = []  # All components that are not a player or a platform, but are collidable (powerups, enemies, etc.)
    other_game_objects = []  # All components that are not a player or a platform, but are not collidable (visuals like grass)
    gravity_engine = None
    rightmost_platform = None
    generator = None
    intermediate_screen = IntermediateScreen()

    # Modifiable Numbers
    health_grid_length = VelocityCalculator.get_dimension(SCREEN_LENGTH, 25)
    health_grid_height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 10)
    side_scrolling_start_distance = VelocityCalculator.get_dimension(SCREEN_LENGTH, 33)
    death_message_time = 0.6
    hud_length = SCREEN_LENGTH - health_grid_length
    hud_height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 6)
    player_keys = [KEY_A, KEY_D, KEY_W, KEY_S, KEY_F]

    hud = None

    # Scoring
    player_score = 0
    high_score = 0
    is_high_score = False
    has_respawned = False

    def __init__(self):
        """Initializes the object"""

        super().__init__("")

        self.setup_platforms()
        self.setup_players()
        self.hud = HUD(1, [], self.hud_length, self.hud_height, 1, None, high_score_is_needed=True)

    def setup_players(self):
        """Creates all the player's and all the necessary stuff associated with them (GravityEngine, HealthGrid, Generator, HUD)"""

        self.players = self.get_players()
        self.gravity_engine = GravityEngine([], self.players[0].get_vertical_acceleration())

        for player in self.players:
            player.gravity_engine = self.gravity_engine
            player.left_edge = self.platforms[0].left_edge + 10
            player.base_top_edge = self.platforms[0].top_edge - player.height
            player.set_top_edge(player.base_top_edge)

            self.player_health_bars.append(HealthBar(player, lambda: False))

        health_grid = Grid(Dimensions(0, 0, self.health_grid_length, self.health_grid_height), 2, 2)
        health_grid.turn_into_grid(self.player_health_bars, None, None)

        self.generator = Generator(self.players[0])
        self.hud.set_dimensions(health_grid.dimensions.right_edge, 0, self.hud_length, self.hud_height)

    def setup_platforms(self):
        """Creates the platforms of the game for starting out"""

        # One Long Platform
        self.platforms = [Platform(*self.get_start_platform_coordinates())]
        self.update_rightmost_platform()

    def run(self):
        """Runs all the code necessary in order for the platformer to work"""

        if self.intermediate_screen.has_finished():
            self.run_game_code()

        else:
            self.intermediate_screen.run()

    def run_game_code(self):
        """Runs all the code for running the game that runs when the intermediate screen is not being displayed"""

        self.run_players()
        self.run_all_collisions()

        for game_object in self.game_objects:
            game_object.run_collisions()

        self.add_game_objects_to_history_keeper()
        self.run_side_scrolling()
        self.run_platform_generation()

    def run_players(self):
        """Runs all the code associated with the player's that is not collisions"""

        self.update_score()
        self.gravity_engine.run()

        for player in self.players:
            if player.platform_is_on is not None and not CollisionsEngine.is_collision(player, player.platform_is_on):
                player.set_is_on_platform(False, None)

            if player.hit_points_left <= 0 or not is_within_screen(player):
                self.reset_game()

            # So the player is moving before side scrolling happens
            player.run()

    def update_score(self):
        """Updates the HUD and the high score of the player"""

        if self.player_score > self.high_score:
            self.is_high_score = True
            self.high_score = self.player_score

        self.hud.update([self.player_score], self.high_score)

    def run_platform_generation(self):
        """Runs all the code for generating platforms"""

        if self.rightmost_platform.right_edge <= SCREEN_LENGTH:
            difficulty = self.get_game_difficulty()
            new_platform = self.generator.generate_platform(self.rightmost_platform, difficulty)
            self.platforms.append(new_platform)
            self.update_rightmost_platform()

    def run_side_scrolling(self):
        """Makes the screen side scroll based off the player who is the farthest behind"""

        # First the players are sorted by the smallest left_edge and then the smallest player is taken
        farthest_back_player = list(sorted(self.players, key=lambda player: player.right_edge))[0]
        shortest_distance = farthest_back_player.right_edge

        # If the distance of the farthest back player is greater than the distance needed for sidescrolling then
        # All the objects in the game should be side scrolled
        if shortest_distance > self.side_scrolling_start_distance:
            side_scrolling_distance = shortest_distance - self.side_scrolling_start_distance
            self.side_scroll_all_objects(side_scrolling_distance)
    def side_scroll_objects(self, distance, game_objects):
        """Moves all the objects leftwards by the distance specified (side scrolling)"""

        for game_object in game_objects:
            game_object.update_for_side_scrolling(distance)

    def side_scroll_all_objects(self, side_scrolling_distance):
        """Side scrolls all the game objects by 'side_scrolling_distance'"""

        self.side_scroll_objects(side_scrolling_distance, self.players)
        self.side_scroll_objects(side_scrolling_distance, self.platforms)

    def get_code_ready_for_collisions(self):
        """Runs the necessary code to prepare for collisions: makes """

        player_components = []
        for player in self.players:
            player_components += player.get_collidable_components()
            player.reset_collision_data()

        self.remove_platforms_not_within_screen()
        self.game_objects = player_components + self.platforms + self.other_game_objects + self.collidable_objects

    def remove_platforms_not_within_screen(self):
        """Removes all the platforms that are not within the screen"""

        updated_platforms = []
        for platform in self.platforms:
            if platform.right_edge >= 0:
                updated_platforms.append(platform)

            else:
                self.player_score += self.get_score_from_passing_platform()
        self.platforms = updated_platforms

    def update_rightmost_platform(self):
        """Updates the attribute 'rightmost_platform' so it is actually the rightmost_platform"""

        # First the platforms are sorted with right_edge's decreasing, then the index of 0 is taken giving the rightmost platform
        self.rightmost_platform = list(sorted(self.platforms, key=lambda platform: platform.right_edge, reverse=True))[0]

    def reset_game(self):
        """Resets the game after the player's death"""

        for player in self.players:
            player.reset()

        self.setup_platforms()
        self.gravity_engine.reset()
        HistoryKeeper.last_objects = {}

        high_score_message = f"New High Score: {self.high_score}"
        non_high_score_message = f"Score: {self.player_score}"
        message = high_score_message if self.is_high_score else non_high_score_message

        self.intermediate_screen.set_texts([message])
        self.intermediate_screen.set_time_ranges([Range(0, self.death_message_time)])
        self.intermediate_screen.display()

        self.player_score = 0

    def run_all_collisions(self):
        """Runs all the collisions between the player, platforms, etc."""

        self.get_code_ready_for_collisions()

        for i in range(len(self.game_objects)):
            object1 = self.game_objects[i]

            for j in range(i, len(self.game_objects)):
                object2 = self.game_objects[j]

                collision_is_possible = len(object1.object_type) != len(object2.object_type)
                collision_has_happened = collision_is_possible and CollisionsEngine.is_collision(object1, object2)

                if collision_has_happened:
                    self.run_collision(object1, object2)

    def run_collision(self, main_object, other_object):
        """ Runs the collisions between the 'main_object' and the 'other_object;' the main_object acts upon the other_object.
            By act upon I mean damages the other_object, moves the other_object, etc."""

        if not self.is_platform(main_object):
            self.run_player_collisions(main_object, other_object)

        if not self.is_platform(other_object):
            self.run_player_collisions(other_object, main_object)

    def run_player_collisions(self, main_object, other_object):
        """Runs the collisions for when the player is the main object"""

        collision_function_parameters = [other_object, main_object.index]

        if self.is_player(main_object) and self.is_platform(other_object):
            main_object.run_inanimate_object_collision(*collision_function_parameters)

        elif self.is_player_weapon(main_object) and self.is_platform(other_object):
            main_object.user.run_inanimate_object_collision(*collision_function_parameters)

    def add_game_objects_to_history_keeper(self):
        """Adds all the game objects to the HistoryKeeper"""

        for game_object in self.game_objects:
            for component in game_object.get_collidable_components():
                if component.is_addable:
                    HistoryKeeper.add(component, component.name, needs_dimensions_only=True)

    def get_components(self):
        """
            Returns:
                list[Component]: all the components that should be rendered"""

        game_components = []

        for game_object in self.game_objects:
            game_components += game_object.get_components()

        game_components += self.player_health_bars + self.platforms + [self.hud]
        return game_components if self.intermediate_screen.has_finished() else self.intermediate_screen.get_components()

    def is_player(self, game_object):
        """
            Returns:
                boolean: if the game_object is the player --> object type would be 'Player'"""

        return len(game_object.object_type) == 6

    def is_player_weapon(self, game_object):
        """
            Returns:
                boolean: if the game_object is the player's weapon --> object type would be 'Player Weapon'"""

        return len(game_object.object_type) == 13

    def is_platform(self, game_object):
        """
            Returns:
                boolean: if the game_object is a platform --> object type would be 'Platform'"""

        return len(game_object.object_type) == 8

    def get_additional_generation_items(self, new_platform):
        """
            Returns:
                list[GameObject]: the additional game objects that should be added to the game once a new platform was generated
        """

        return []

    # Abstract Methods
    @abc.abstractmethod
    def get_enemy_types(self):
        """
            Returns:
                list[Enemy]: all the types of enemies that can be generated
        """

        pass

    @abc.abstractmethod
    def get_game_difficulty(self):
        """
            Returns:
                float: the difficulty of the game based on the score of the player (from 0 to 100 with 100 being the hardest)
        """

        pass

    @abc.abstractmethod
    def get_score_from_passing_platform(self):
        """
            Returns:
                int: the score from passing a platform
        """

        pass

    @abc.abstractmethod
    def get_start_platform_coordinates(self):
        """
            Returns:
                list[float]: {left_edge, top_edge, length, height} of the start platform
        """

        pass

    @abc.abstractmethod
    def get_players(self):
        """
            Returns:
                list[Player]: the players of the game
        """

        pass
