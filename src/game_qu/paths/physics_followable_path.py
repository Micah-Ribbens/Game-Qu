from game_qu.base.utility_functions import get_kwarg_item
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.math.physics_function import PhysicsFunction
from game_qu.paths.followable_path import FollowablePath


class PhysicsFollowablePath(FollowablePath, PhysicsFunction):
    """ An extension of physics function that allows for automatically changing the player's coordinates; implements
        the FollowablePath 'interface'"""

    game_object = None
    current_time = 0
    is_started = False
    attribute_modifying = None
    height_of_path = 0
    time_to_vertex = 0
    max_time = 0
    last_time = 0
    has_max_time = False
    all_distance = 0
    last_delta_time = 0
    is_using_everything_this_cycle = False

    def __init__(self, **kwargs):
        """ Initializes the object

            Args:
                game_object (GameObject): the game object that is following this path
                attribute_modifying (str): the name of the attribute this path is modifying
                time (float): the time to the vertex of the path
                height_of_path (float): the difference between the initial distance and the vertex of the path
                max_time (float): the max time of the path - the time the path should end (None if the path should not end)
     
            Returns:
                None
        """

        FollowablePath.__init__(self, **kwargs)
        self.time_to_vertex, self.height_of_path = get_kwarg_item(kwargs, "time", .5), get_kwarg_item(kwargs, "height_of_path", 0)
        self.initial_distance = get_kwarg_item(kwargs, "initial_distance", 0)

        # Adding the initial_distance, so it that is the height of the parabola
        self.set_all_variables(self.height_of_path + self.initial_distance, self.time_to_vertex, self.initial_distance)

    def run(self, is_reset_event, is_start_event, is_using_everything=False, is_changing_coordinates=True):
        """ Runs the code for the game_object following the physics path

            Args:
                is_reset_event (bool): if True it will call reset()
                is_start_event (bool): if True it will call start()
                is_using_everything (bool): if True it will use both velocity and acceleration and if False will just use velocity
     
            Returns:
                None
        """

        self.is_using_everything_this_cycle = is_using_everything

        # Calling the super method, but being explicit about which one I am looking for
        FollowablePath.run(self, is_reset_event, is_start_event, is_changing_coordinates)

        can_change_attribute = self.is_started and self.game_object is not None
        should_change_attribute = can_change_attribute and is_changing_coordinates

        if is_using_everything and should_change_attribute:
            self.game_object.__dict__[self.attribute_modifying] = self.get_distance(self.current_time)

    def set_initial_distance(self, initial_distance):
        """Sets the initial distance, so the height of the parabola is equal to the vertex"""

        self.initial_distance = initial_distance
        self.set_all_variables(self.initial_distance + self.height_of_path, self.time_to_vertex, self.initial_distance)

    def get_velocity_displacement(self):
        """
             Returns:
                float: the displacement from velocity (the last_time - start_time)"""

        return self.get_displacement_due_to_velocity(self.last_time, self.current_time)

    def get_acceleration_displacement(self):
        """
             Returns:
                float: the distance from acceleration with gravity"""

        return self.get_displacement_due_to_acceleration(self.last_time, self.current_time)

    def get_total_displacement(self):
        """
             Returns:
                float: the displacement from both velocity and acceleration"""

        return self.get_velocity_displacement() + self.get_acceleration_displacement()

    def get_acceleration_displacement_from_time(self, time):
        """
             Returns:
                float: the displacement from acceleration at that time"""

        return self.get_displacement_due_to_acceleration(0, time)

    def get_final_velocity(self):
        """
             Returns:
                float: the velocity from acceleration (assumes initial_velocity is 0)"""

        return self.acceleration * self.current_time

    def get_value_at_time(self, time):
        """
             Returns:
                object: the value of the attribute this path is modifying at 'time'"""

        if self.is_using_everything_this_cycle:
            return self.get_distance(time)

        else:
            return self.get_displacement_due_to_velocity(0, time)

    def get_delta_value(self, start_time, end_time):
        """
             Returns:
                object: the delta value of the attribute within the domain [start_time, end_time]"""

        if self.is_using_everything_this_cycle:
            return 0

        else:
            return self.get_displacement_due_to_velocity(start_time, end_time)
