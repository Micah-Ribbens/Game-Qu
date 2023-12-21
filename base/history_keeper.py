from copy import deepcopy

from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.important_constants import *


class HistoryKeeper:
    last_objects = {}
    last_frame_id = 0

    @staticmethod
    def add(history_keeper_object, name, needs_dimensions_only=False, needs_deepcopy=False):
        """ Adds the object to the HistoryKeeper; IMPORTANT: make sure to provide a unique name for each unique object!

            :parameter history_keeper_object: Object; the object that is going to be added to the HistoryKeeper
            :parameter name: String; the unique name (identifier) for the object
            :parameter needs_deepcopy: bool; the object provided is an instance of GameObject
            :parameter needs_dimensions_only: bool; whether the object stored only needs the dimensions stored for it

            :returns: None
        """

        if needs_deepcopy:
            history_keeper_object = deepcopy(history_keeper_object)
            history_keeper_object.name = name

        if needs_dimensions_only:
            history_keeper_object = Dimensions(history_keeper_object.left_edge, history_keeper_object.top_edge,
                                               history_keeper_object.length, history_keeper_object.height)
            history_keeper_object.name = name

        frame_id = HistoryKeeper.get_frame_id(VelocityCalculator.current_cycle_number)
        HistoryKeeper.last_objects[f"{name}_{frame_id}"] = history_keeper_object

    @staticmethod
    def get_last(name):
        """ Gets the version of that object from the last cycle

            :parameter name: str; the unique name (identifier) given for the object in HistoryKeeper.add() that is used to retrieve the previous version of the object

            :returns: the version of the object from the last cycle
        """

        return HistoryKeeper.get_last_using_frame_id(name, HistoryKeeper.last_frame_id)

    @staticmethod
    def get_last_using_frame_id(name, frame_id):
        """ Gets the version of that object from at that cycle (decided by 'frame_id')

            :parameter name: str; the unique name (identifier) given for the object in HistoryKeeper.add() that is used to get the object at the specific cycle
            :parameter frame_id: int; the frame_id of the cycle

            :returns: the version of the object from the last cycle
        """
        return HistoryKeeper.last_objects.get(f"{name}_{frame_id}")

    @staticmethod
    def reset():
        """Resets the HistoryKeeper, so it has no more values of past objects"""

        HistoryKeeper.last_objects = {}
        HistoryKeeper.times = []

    @staticmethod
    def set_last_frame_id(cycle_number):
        """Sets the last time of the HistoryKeeper"""

        HistoryKeeper.last_frame_id = HistoryKeeper.get_frame_id(cycle_number)

    @staticmethod
    def get_frame_id(cycle_number):
        """ :returns: int; the identifier for that frame (the number of frames that the HistoryKeeper stores is equal to
            'FRAMES_HISTORY_KEEPER_STORES' in base/important_variables"""
        
        return cycle_number % NUMBER_OF_FRAMES_HISTORY_KEEPER_STORES

    @staticmethod
    def get_all_of_name(name):
        """:returns: all the objects in the HistoryKeeper that have the name 'name'"""

        return_value = {}

        for x in range(NUMBER_OF_FRAMES_HISTORY_KEEPER_STORES):
            key = f"{name}_{x}"
            value = HistoryKeeper.last_objects.get(key)

            if value is not None:
                return_value[key] = value

        return return_value








