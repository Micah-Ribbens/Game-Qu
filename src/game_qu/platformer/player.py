from math import sqrt
from game_qu.base.lines import LineSegment
from game_qu.base.events import TimedEvent
from game_qu.base.game_movement import GameMovement

from game_qu.base.quadratic_equations import PhysicsPath
from game_qu.base.history_keeper import HistoryKeeper
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.math.bounded_function import BoundedFunction
from game_qu.math.function import Function
from game_qu.math.linear_interpolation import LinearInterpolation
from game_qu.math.matrix import Matrix
from game_qu.math.physics_function import PhysicsFunction
from game_qu.math.piecewise_function import PiecewiseFunction
from game_qu.math.point import Point
from game_qu.math.polynomial import Polynomial, PolynomialTerm
from game_qu.paths.piecewise_followable_path import PiecewiseFollowablePath
from game_qu.platformer.weapon_user import WeaponUser
from game_qu.base.utility_functions import *
from game_qu.platformer.constants import *


class Player(WeaponUser):
    """The way that people can play the game (accepts user input to move)"""

    all_paths_and_events = []

    # Modifiable Variables
    length = VelocityCalculator.get_dimension(SCREEN_LENGTH, 5)
    height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 15)

    total_hit_points = 50
    object_type = "Player"

    # So you can control all the jump movements (it feels better if there is different jump arcs for up and down)
    apex_jump_time = 0.1
    apex_horizontal_velocity_multiplier = 1.25
    coyote_time = 0.2
    terminal_velocity = VelocityCalculator.get_velocity(SCREEN_LENGTH, 1500)
    jump_buffer_time = 0.5

    # Variable Jump Heights
    time_to_high_jump_vertex = 0.55
    time_from_high_jump_vertex_to_ground = 0.35
    high_jump_height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 30)
    high_jump_time_held_in = 0.35

    time_to_medium_jump_vertex = 0.4
    time_from_medium_jump_vertex_to_ground = 0.2
    medium_jump_height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 20)
    medium_jump_time_held_in = 0.2

    time_to_small_jump_vertex = 0.3
    time_from_small_jump_vertex_to_ground = 0.2
    small_jump_height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 10)
    small_jump_time_held_in = 0.1

    running_deceleration_time = 0.3
    invincibility_total_time = 1
    max_horizontal_velocity = VelocityCalculator.get_velocity(SCREEN_LENGTH, 500)
    running_acceleration_time = 0.2

    minimum_jump_deceleration_time = 0.1

    # Miscellaneous
    hit_points_left = total_hit_points
    jumping_path = None
    deceleration_path = None
    acceleration_path = None
    current_velocity = 0
    initial_upwards_velocity = 0
    invincibility_event = None
    platform_is_on = None
    last_platform_was_on = None
    # So the player can be run and side scrolling can be done before the rendering (otherwise it doesn't look smooth)
    is_runnable = False
    has_jumped = False
    jumping_piecewise_function = None
    falling_piecewise_function = None
    time_to_jump_type_index = None
    coyote_timed_event = None
    jump_buffer_timed_event = None
    base_left_edge = -1
    base_top_edge = -1
    jump_key_held_in_time = -1
    jump_types = None

    # Booleans
    can_move_down = False
    can_move_left = False
    can_move_right = False
    is_on_platform = True
    is_facing_right = True

    # Keys
    left_key = None
    right_key = None
    jump_key = None
    down_key = None
    attack_key = None

    def __init__(self, left_key, right_key, jump_key, down_key, attack_key):
        """Initializes the object"""

        super().__init__("")

        self.left_key, self.right_key, self.jump_key = left_key, right_key, jump_key
        self.down_key, self.attack_key = down_key, attack_key
        self.invincibility_event = TimedEvent(self.invincibility_total_time, False)
        self.coyote_timed_event = TimedEvent(self.coyote_time, False)
        self.jump_buffer_timed_event = TimedEvent(self.jump_buffer_time, False)

        self.create_paths()
        self.all_paths_and_events = [self.jumping_path, self.deceleration_path, self.acceleration_path]
        self.jumping_functions = [self._set_jumping_path_to_small_jump, self._set_jumping_path_to_medium_jump,
                                  self._set_jumping_path_to_high_jump]
        self.update_jump_types()

    def create_paths(self):
        """Creates all the paths for the player: jumping_path, decelerating_path, etc."""

        self.jumping_piecewise_function = PiecewiseFunction([])
        self.falling_piecewise_function = PiecewiseFunction([])

        self.jumping_path = PiecewiseFollowablePath(self.jumping_piecewise_function, game_object=self, attribute_modifying="top_edge")

        self.set_running_acceleration_time(self.running_acceleration_time)
        self.set_running_deceleration_time(self.running_deceleration_time)

    def run(self):
        """Runs all the code that is necessary for the player to work properly"""

        self.invincibility_event.run(self.invincibility_event.current_time > self.invincibility_event.time_needed, False)
        self.run_horizontal_movement()
        self.run_vertical_movement()

    def run_vertical_movement(self):
        """Runs all the vertical movement (mostly jumping)"""

        if game_button_is_clicked(self.jump_key):
            if self.is_on_platform:
                self.jump()

            if self.coyote_timed_event.is_running():
                self.jump()
                self.coyote_timed_event.reset()

        if game_button_has_been_released(self.jump_key):
            self.jump_key_held_in_time = get_time_of_game_button_being_held_in(self.jump_key)

            if self.has_jumped:
                self.run_jump_type()

        if self.top_edge <= 0:
            self.run_bottom_edge_collision(0)

        self.jumping_path.run(is_changing_attribute=True)

    def run_horizontal_movement(self):
        """Runs all the code for horizontal movement: acceleration, deceleration, etc."""

        self.is_facing_right = True if game_button_is_pressed(self.right_key) else self.is_facing_right
        self.is_facing_right = False if game_button_is_pressed(self.left_key) else self.is_facing_right

        self.run_deceleration()
        self.run_acceleration()

        GameMovement.player_horizontal_movement(self, self.current_velocity, self.left_key, self.right_key)

    def run_acceleration(self):
        """Runs all the code for acceleration (so the player comes to the max velocity)"""

        if self.player_movement_direction_is_same_as_deceleration():
            self.continue_acceleration_after_partial_deceleration()

        if self.deceleration_path.has_finished():
            GameMovement.run_acceleration(self, game_button_is_pressed(self.left_key) or game_button_is_pressed(self.right_key), self.acceleration_path, self.max_horizontal_velocity)

        if not self.acceleration_direction_is_possible(self.acceleration_path.acceleration > 0):
            self.acceleration_path.reset()

    def run_deceleration(self):
        """Runs all the code for decelerating (so the player comes to a stop slowly)"""

        deceleration_direction_is_possible = self.acceleration_direction_is_possible(self.get_deceleration_is_rightwards())

        # Meaning no outside force has stopped the deceleration like platforms or screen limits
        deceleration_has_manually_stopped = self.deceleration_path.has_finished() or self.player_movement_direction_is_same_as_deceleration()
        can_decelerate = deceleration_direction_is_possible and not deceleration_has_manually_stopped

        if can_decelerate:
            self.deceleration_path.run(False, False, is_changing_coordinates=False)
            self.left_edge += self.deceleration_path.get_total_displacement()

        else:
            self.deceleration_path.reset()

        if self.horizontal_movement_has_stopped():
            self.decelerate_player(game_button_has_been_released(self.right_key))

    def horizontal_movement_has_stopped(self):
        """
            Returns:
                boolean: if horizontal movement has stopped (player has released a movement key)"""

        return game_button_has_been_released(self.right_key) or game_button_has_been_released(self.left_key)

    def acceleration_direction_is_possible(self, movement_is_rightwards):
        """
            Returns:
                boolean: whether the path acceleration's movement is not possible because of either the screen or a platform
                | This is used for both the acceleration_path and deceleration_path. Figures out if the direction of acceleration
                is possible (if it can't move right it can't accelerate right"""

        return self.can_move_right if movement_is_rightwards else self.can_move_left

    def set_is_on_platform(self, is_on_platform, platform_is_on):
        """Sets the player's 'is_on_platform' attribute"""

        if not self.is_on_platform and is_on_platform:
            self.jumping_path.reset()

        if self.is_on_platform and not is_on_platform and not self.has_jumped:
            self.set_jumping_path_to_falling_path()

        if self.jump_buffer_timed_event.is_running():
            self.jump()
            self.jump_buffer_timed_event.reset()

        self.last_platform_was_on = platform_is_on if is_on_platform else self.last_platform_was_on
        self.platform_is_on = platform_is_on if is_on_platform else None
        self.is_on_platform = is_on_platform

    def reset(self):
        """Resets the player back to the start of the game"""

        self.left_edge = self.base_left_edge
        self.top_edge = self.base_top_edge

        self.run_respawning()  # Resetting from the game ending and respawning has a lot in similarity

    def run_respawning(self):
        """Makes the player respawn (resets most things)"""

        self.is_on_platform = True
        self.hit_points_left = self.total_hit_points
        self.invincibility_event.reset()

        # Resetting the direction the player can move
        self.can_move_left, self.can_move_right, self.can_move_down = False, False, False

        for path_or_event in self.all_paths_and_events:
            path_or_event.reset()

    def jump(self):
        """Makes the player jump"""

        self.jumping_path.start()
        self.set_jumping_path_to_default_jump()
        self.has_jumped = True

        if self.jump_key_held_in_time != -1:
            self.run_jump_type()

    def decelerate_player(self, is_moving_right):
        """Makes the player decelerate by calling deceleration_path.start()"""

        self.deceleration_path.initial_distance = self.left_edge
        self.deceleration_path.initial_velocity = self.current_velocity if is_moving_right else -self.current_velocity

        # If the player is not at maximum velocity it shouldn't take as long to decelerate
        fraction_of_max_velocity = self.current_velocity / self.max_horizontal_velocity
        time_needed = self.running_deceleration_time * fraction_of_max_velocity

        # Gotten using math; Makes the player stop in the amount of time 'self.running_deceleration_time'
        self.deceleration_path.acceleration = -self.deceleration_path.initial_velocity / time_needed

        self.deceleration_path.start()
        self.deceleration_path.max_time = time_needed

    def player_movement_direction_is_same_as_deceleration(self):
        """
            Returns:
                boolean: if the direction the player is moving is equal to the deceleration"""

        deceleration_direction_is_rightwards = self.deceleration_path.acceleration < 0

        # Looking at both the leftwards and rightwards movement: movement and deceleration have both to be leftwards or rightwards
        rightwards_movement_is_same_as_deceleration = deceleration_direction_is_rightwards and game_button_is_pressed(self.right_key)
        leftwards_movement_is_same_as_deceleration = not deceleration_direction_is_rightwards and game_button_is_pressed(self.left_key)

        return leftwards_movement_is_same_as_deceleration or rightwards_movement_is_same_as_deceleration

    def continue_acceleration_after_partial_deceleration(self):
        """Updates the time of the acceleration_path, so that it will pick up at the velocity where the deceleration ended at"""

        current_velocity = self.deceleration_path.get_velocity_using_time(self.deceleration_path.current_time)
        self.acceleration_path.start()

        # Figuring out the time to get to that velocity, so the player can continue to accelerate to the max velocity
        self.acceleration_path.current_time = sqrt(abs(current_velocity) / self.acceleration_path.acceleration)

    def run_bottom_edge_collision(self, top_edge):
        """Runs what should happen after a bottom collision (the player should rebound off of it)"""

        velocity = self.get_vertical_velocity()
        falling_function = PhysicsFunction(self.high_jump_height, self.time_to_high_jump_vertex, self.top_edge)
        falling_function.set_initial_velocity(velocity)
        functions = self.get_jumping_path_bounded_functions([falling_function],
                                                            [self.time_from_high_jump_vertex_to_ground])

        self.falling_piecewise_function.set_functions(functions)
        self.set_jumping_path_to_falling_path()

        self.jumping_path.reset()
        self.top_edge = top_edge

    def get_horizontal_velocity(self):
        """
            Returns:
                double: the current velocity of the player"""

        # The velocity of the player is two-fold: either it has its usual velocity when it is not decelerating, or it has
        # The velocity from the deceleration. The deceleration_path does not affect the current_velocity because it was
        # Easier not to do that, so it does not do it that way
        deceleration_velocity = self.deceleration_path.get_velocity_using_time(self.deceleration_path.current_time)
        normal_velocity = self.current_velocity

        return normal_velocity if self.deceleration_path.has_finished() else deceleration_velocity

    # Collision Stuff
    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen when the player collides with an inanimate object"""

        if index_of_sub_component == self.index_of_user:
            self.update_platform_collision_data(inanimate_object)

        if index_of_sub_component != self.index_of_user:
            self.weapon.run_inanimate_object_collision(inanimate_object, index_of_sub_component - self.weapon_index_offset)

    def run_collisions(self):
        """Runs what should happen based on what got stored in the collision data"""

        # The player should only act upon the collision data if there was stuff in the History Keeper because if there wasn't
        # Then the game is automatically going to say it was not a collision (top, left, right, bottom)
        if HistoryKeeper.get_last(self.name) is not None:
            self.alter_player_horizontal_movement()
            self.alter_player_vertical_movement()

    def alter_player_horizontal_movement(self):
        """Alters the player's horizontal movement so it stays within the screen and is not touching the platforms"""

        player_is_beyond_screen_left = is_beyond_screen_left(self.left_edge)
        player_is_beyond_screen_right = is_beyond_screen_right(self.right_edge)

        self.alter_player_horizontal_movement_booleans(player_is_beyond_screen_left, player_is_beyond_screen_right)
        self.alter_player_left_edge_if_necessary(player_is_beyond_screen_left, player_is_beyond_screen_right)

    def alter_player_horizontal_movement_booleans(self, player_is_beyond_screen_left, player_is_beyond_screen_right):
        """Alters the player's horizontal movement direction boolean attributes: 'can_move_left' and 'can_move_right'"""

        is_decelerating_rightwards = not self.deceleration_path.has_finished() and self.get_deceleration_is_rightwards()
        is_decelerating_leftwards = not self.deceleration_path.has_finished() and not self.get_deceleration_is_rightwards()

        # Possible relating to everything but the deceleration
        leftwards_movement_is_possible = not self.right_collision_data[0] and not player_is_beyond_screen_left
        rightwards_movement_is_possible = not self.left_collision_data[0] and not player_is_beyond_screen_right

        self.can_move_left = leftwards_movement_is_possible and not is_decelerating_rightwards
        self.can_move_right = rightwards_movement_is_possible and not is_decelerating_leftwards

    def alter_player_left_edge_if_necessary(self, player_is_beyond_screen_left, player_is_beyond_screen_right):
        """Alters the player's left edge if it is needed: the player has collided with the platform, or has gone beyond the screen"""

        # Setting the player's x coordinate if the any of the above conditions were met (collided with platform or beyond screen)
        self.change_attribute_if(player_is_beyond_screen_left, self.set_left_edge, 0)
        self.change_attribute_if(player_is_beyond_screen_right, self.set_left_edge, SCREEN_LENGTH - self.length)

        if self.right_collision_data[0]:
            self.set_left_edge(self.right_collision_data[1].right_edge)

        if self.left_collision_data[0]:
            self.set_left_edge(self.left_collision_data[1].left_edge - self.length)

    def get_deceleration_is_rightwards(self):
        """
            Returns:
                boolean: if the deceleration direction is rightwards"""

        # The deceleration must be going left to stop the player from moving right and vice versa
        return self.deceleration_path.acceleration < 0

    def alter_player_vertical_movement(self):
        """Alters the player's vertical movement so it can't go through platforms"""

        player_is_on_platform = self.top_collision_data[0]

        if player_is_on_platform:
            self.set_top_edge(self.top_collision_data[1].top_edge - self.height)

        self.set_is_on_platform(player_is_on_platform, self.top_collision_data[1])

        if self.bottom_collision_data[0]:
            self.run_bottom_edge_collision(self.bottom_collision_data[1].bottom_edge)

    def set_left_edge(self, left_edge):
        """Sets the left edge of the player equal to the value provided"""

        self.left_edge = left_edge

    def change_attribute_if(self, condition, function, value):
        """Changes the attribute to the value if 'condition()' is True"""

        if condition:
            function(value)

    def cause_damage(self, amount):
        """Damages the player by that amount and also starts the player's invincibility"""

        if self.invincibility_event.has_finished():
            self.hit_points_left -= amount
            self.invincibility_event.start()

    def get_topmost_top_edge(self, last_platform, accuracy, min_accuracy):
        """Figures out the minimum top edge of the next platform (remember the closer to the top of the screen the lower the top edge)

            Args:
                last_platform (Platform): the platform the player would be jumping from
                accuracy (double): how accurate the player has to be to clear this jump
                min_accuracy (double): the minimum accuracy possible

            Returns:
                double: the max top edge that the next platform could be at that leaves the player 'margin_of_error'
        """

        topmost_top_edge = last_platform.top_edge - (self.high_jump_height * accuracy) + self.height

        # The absolute max of a platform is the player's height because the player has to get its bottom_edge on the platform
        # Which would mean the player's top edge would be 0 also

        if topmost_top_edge <= self.height:
            topmost_top_edge = self.height

        return topmost_top_edge

    def get_distance_to_reach_max_velocity(self):
        """
            Returns:
                double: the distance needed for the player to reach max velocity"""

        time_needed = self.max_horizontal_velocity / self.acceleration_path.acceleration
        return self.acceleration_path.get_distance(time_needed)

    def get_vertical_velocity(self):
        """
            Returns:
                float: the velocity of the player at this moment in time
        """

        return self.get_vertical_velocity_at_time(self.jumping_path.get_current_time())

    def get_vertical_velocity_at_time(self, time):
        """
            Returns:
                float: the velocity of the player at that moment in time
        """

        derivative = self.jumping_path.get_piecewise_function().get_derivative()
        return derivative.get_y_coordinate(time)

    def get_vertical_acceleration(self):
        """
            Returns:
                float: the acceleration in the vertical direction of the player (falling acceleration)
        """

        return PhysicsFunction(self.high_jump_height, self.time_to_high_jump_vertex, 0).get_acceleration()

    # Setters
    def set_total_hit_points(self, total_hit_points):
        self.total_hit_points = total_hit_points

    def set_object_type(self, object_type):
        self.object_type = object_type

    def set_base_left_edge(self, base_left_edge):
        self.base_left_edge = base_left_edge

    def set_base_top_edge(self, base_top_edge):
        self.base_top_edge = base_top_edge

    def set_running_deceleration_time(self, running_deceleration_time):
        self.running_deceleration_time = running_deceleration_time

        self.deceleration_path = PhysicsPath(game_object=self, attribute_modifying="left_edge", max_time=self.running_deceleration_time)

    def set_invincibility_total_time(self, invincibility_total_time):
        self.invincibility_total_time = invincibility_total_time

    def set_max_horizontal_velocity(self, max_horizontal_velocity):
        self.max_horizontal_velocity = max_horizontal_velocity

    def set_running_acceleration_time(self, running_acceleration_time):
        self.running_acceleration_time = running_acceleration_time
        self.acceleration_path = PhysicsPath()
        self.acceleration_path.set_acceleration_with_velocity(self.running_acceleration_time, self.max_horizontal_velocity)

    # Jumping
    def update_jumping_path(self):
        """Updates the path of the player, so they jump"""

        initial_velocity = PhysicsFunction(self.top_edge - self.high_jump_height, self.time_to_high_jump_vertex, self.top_edge).get_initial_velocity()
        self.set_jumping_path_with_kinematics(self.top_edge - self.high_jump_height, self.time_to_high_jump_vertex,
                                              initial_velocity, self.time_from_high_jump_vertex_to_ground)

    def update_falling_path(self):
        """Updates the path of the player, so they fall"""

        # Finding the normal falling path as defined by its 2 functions (falling, terminal velocity)
        falling_function = PhysicsFunction(self.top_edge + self.high_jump_height, self.time_to_high_jump_vertex, self.top_edge)
        bounded_functions = self.get_jumping_path_bounded_functions([falling_function], [self.time_to_high_jump_vertex])
        self.falling_piecewise_function.set_functions(bounded_functions)

    def update_jump_types(self):
        """Updates the variables of the player, so the jump heights work"""

        # The x coordinate is the time the jump key is held in and the y coordinate is the index of the function
        self.time_to_jump_type_index = LinearInterpolation(Point(0, 0),
                                                           [Point(self.small_jump_time_held_in, 0),
                                                      Point(self.medium_jump_time_held_in, 1),
                                                      Point(self.high_jump_time_held_in, 2),
                                                      Point(float("inf"), 2)])

        self.jump_types = [self._set_jumping_path_to_small_jump, self._set_jumping_path_to_medium_jump,
                           self._set_jumping_path_to_high_jump]

    def set_jumping_path_with_apex(self, time_to_jump_vertex, jump_height, time_from_vertex_to_ground):
        """Sets the jumping path of the player, so it has the jump height and time to vertex"""

        # Finding the jumping path as defined by its 4 functions (upwards, apex, downwards, terminal velocity)
        # Finding the initial variables we need for the calculations below
        jumping_function: PhysicsFunction = self.jumping_piecewise_function.get_functions()[0].get_function()
        time_spent_in_air = self.jumping_path.get_current_time()
        height_jumped = jumping_function.get_displacement(0, time_spent_in_air)
        jump_height_left = jump_height - height_jumped
        time_left = time_to_jump_vertex - time_spent_in_air

        # Calculating the apex variables
        apex_time_left = max_value(self.minimum_jump_deceleration_time, time_left)
        vertex = self.top_edge - jump_height_left
        initial_velocity = self.get_vertical_velocity()

        self.set_jumping_path_with_kinematics(vertex, apex_time_left, initial_velocity, time_from_vertex_to_ground)

    def set_jumping_path_with_kinematics(self, vertex, time_to_vertex, initial_velocity, time_from_vertex_to_ground):
        """Sets the jumping path based on the passed in variables"""

        # Using variables found above to get the functions
        upwards_function = PhysicsFunction()
        upwards_function.set_variables(initial_velocity=initial_velocity, initial_distance=self.top_edge)
        upwards_function.set_acceleration_with_velocity(time_to_vertex, -initial_velocity)

        apex_function = Polynomial(Matrix([])).set_terms([PolynomialTerm(vertex, 0)])  # So the player stays at the vertex
        downwards_function = PhysicsFunction(self.top_edge, time_from_vertex_to_ground, vertex)

        functions = [upwards_function, apex_function, downwards_function]
        delta_times = [time_to_vertex, self.apex_jump_time, time_from_vertex_to_ground]

        bounded_functions = self.get_jumping_path_bounded_functions(functions, delta_times)
        self.jumping_piecewise_function.set_functions(bounded_functions)

    def _set_jumping_path_to_small_jump(self):
        """Sets the jumping path to a small jump"""

        self.set_jumping_path_with_apex(self.time_to_small_jump_vertex, self.small_jump_height, self.time_from_small_jump_vertex_to_ground)

    def _set_jumping_path_to_medium_jump(self):
        """Sets the jumping path to a medium jump"""

        self.set_jumping_path_with_apex(self.time_to_medium_jump_vertex, self.medium_jump_height, self.time_from_medium_jump_vertex_to_ground)

    def _set_jumping_path_to_high_jump(self):
        """Sets the jumping path to a high jump"""

        self.set_jumping_path_with_apex(self.time_to_high_jump_vertex, self.high_jump_height, self.time_from_high_jump_vertex_to_ground)

    def get_jumping_path_bounded_functions(self, functions, delta_times):
        """
            Returns:
                list[BoundedFunction]: the piecewise function with the specified functions and delta times (adds a terminal
                velocity function if the terminal velocity is reached). Assumes the last function is the one which should
                have the velocity clamped at terminal velocity.
        """

        # So the player's velocity is clamped at terminal velocity
        terminal_velocity_function = Polynomial(Matrix([])).set_terms([PolynomialTerm(self.terminal_velocity, 1)])
        last_function = functions[len(functions) - 1]
        terminal_velocity_delta_time = self.get_terminal_velocity_delta_time(last_function.get_polynomial(),
                                                                             self.terminal_velocity)
        if terminal_velocity_delta_time is not None:
            functions.append(terminal_velocity_function)
            delta_times[len(delta_times) - 1] = terminal_velocity_delta_time
            delta_times.append(float("inf"))

        return PiecewiseFunction.get_bounded_functions_with_delta_times(functions, delta_times, 0)

    def get_max_time_to_top_edge(self, start_top_edge, new_top_edge):
        """
            Returns:
                 double: the max amount of time for the player's bottom_edge to reach the new y coordinate"""

        # TODO actually solve this
        return 1.2


    def get_terminal_velocity_delta_time(self, function: Polynomial, terminal_velocity):
        """
            Returns:
                float: how long it takes for the player to go from falling to reaching terminal velocity (None if the terminal velocity is never reached)
        """

        times_when_terminal_velocity_is_reached = function.get_derivative().get_x_coordinates(terminal_velocity)

        # Only the positive time is wanted (don't care about other side of polynomial)
        for time in times_when_terminal_velocity_is_reached:
            if time > 0:
                return time

        raise None

    def set_jumping_path_to_default_jump(self):
        """ Sets the variable 'jumping_path' to a path that defines the player's jump (falling and jumping have different
            gravities to make the game feel better)"""

        self.update_jumping_path()
        self.jumping_path.set_piecewise_function(self.jumping_piecewise_function)
        self.jumping_path.restart()

    def set_jumping_path_to_falling_path(self):
        """ Sets the variable 'jumping_path' to a path that defines the player's fall (falling and jumping have different
            gravities to make the game feel better)"""

        self.update_falling_path()
        self.jumping_path.set_piecewise_function(self.falling_piecewise_function)
        self.jumping_path.restart()

    def run_jump_type(self):
        """Runs a different jump type (small, medium, or large) depending on how long the key was held in"""

        index = self.time_to_jump_type_index.get_y_coordinate(self.jump_key_held_in_time)
        self.jump_types[int(index)]()

        self.jump_key_held_in_time = -1

    def set_coyote_time(self, coyote_time):
        self.coyote_time = coyote_time

    def set_terminal_velocity(self, terminal_velocity):
        self.terminal_velocity = terminal_velocity

    def set_jump_buffer_time(self, jump_buffer_time):
        self.jump_buffer_time = jump_buffer_time

    def set_apex_jump_time(self, apex_jump_time):
        self.apex_jump_time = apex_jump_time

    def set_apex_horizontal_velocity_multiplier(self, apex_horizontal_velocity_multiplier):
        self.apex_horizontal_velocity_multiplier = apex_horizontal_velocity_multiplier

    def set_time_to_high_jump_vertex(self, variable):
        self.time_to_high_jump_vertex = variable
        self.update_jump_types()

    def set_time_from_high_jump_vertex_to_ground(self, variable):
        self.time_from_high_jump_vertex_to_ground = variable
        self.update_jump_types()

    def set_high_jump_height(self, variable):
        self.high_jump_height = variable
        self.update_jump_types()

    def set_high_jump_time_held_in(self, variable):
        self.high_jump_time_held_in = variable
        self.update_jump_types()

    def set_time_to_medium_jump_vertex(self, variable):
        self.time_to_medium_jump_vertex = variable
        self.update_jump_types()

    def set_time_from_medium_jump_vertex_to_ground(self, variable):
        self.time_from_medium_jump_vertex_to_ground = variable
        self.update_jump_types()

    def set_medium_jump_height(self, variable):
        self.medium_jump_height = variable
        self.update_jump_types()

    def set_medium_jump_time_held_in(self, variable):
        self.medium_jump_time_held_in = variable
        self.update_jump_types()

    def set_time_to_small_jump_vertex(self, variable):
        self.time_to_small_jump_vertex = variable
        self.update_jump_types()

    def set_time_from_small_jump_vertex_to_ground(self, variable):
        self.time_from_small_jump_vertex_to_ground = variable
        self.update_jump_types()

    def set_small_jump_height(self, variable):
        self.small_jump_height = variable
        self.update_jump_types()

    def set_small_jump_time_held_in(self, variable):
        self.small_jump_time_held_in = variable
        self.update_jump_types()

    def set_base_coordinates(self, base_left_edge, base_top_edge):
        """Sets the base coordinates of the player"""

        self.base_left_edge = base_left_edge
        self.base_top_edge = base_top_edge
