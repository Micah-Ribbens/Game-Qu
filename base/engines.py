from game_qu.base.history_keeper import HistoryKeeper


class CollisionsEngine:
    """Provides methods for figuring out if objects have collided"""

    @staticmethod
    def is_horizontal_collision(object1, object2):
        """:returns: bool; whether object1 and object2 have collided horizontally (ignores vertical direction- 1D)"""

        return object1.left_edge <= object2.right_edge and object1.right_edge >= object2.left_edge

    @staticmethod
    def is_vertical_collision(object1, object2):
        """:returns: bool; whether object1 and object2 have collided vertically (ignores horizontal direction- 1D)"""

        return object1.top_edge <= object2.bottom_edge and object1.bottom_edge >= object2.top_edge

    @staticmethod
    def is_collision(object1, object2):
        """:returns: bool; whether object1 and object2 have collided vertically and horizontally"""

        return CollisionsEngine.is_horizontal_collision(object1, object2) and CollisionsEngine.is_vertical_collision(object1, object2)

    @staticmethod
    def is_left_collision(object1, object2, is_collision=None, last_time=None):
        """ :returns: bool; if object1 has collided with object2's left edge"""

        objects_are_touching = object1.right_edge == object2.left_edge and CollisionsEngine.is_vertical_collision(
            object1, object2)
        is_moving_left_collision = CollisionsEngine.is_moving_left_collision(object1, object2, is_collision, last_time)

        return is_moving_left_collision or objects_are_touching

    @staticmethod
    def is_right_collision(object1, object2, is_collision=None, last_time=None):
        """:returns: bool; if object1 has collided with object2's right_edge"""

        is_moving_right_collision = CollisionsEngine.is_moving_right_collision(object1, object2, is_collision,
                                                                               last_time)

        objects_are_touching = object1.left_edge == object2.right_edge and CollisionsEngine.is_vertical_collision(
            object1, object2)

        return is_moving_right_collision or objects_are_touching

    @staticmethod
    def is_moving_right_collision(object1, object2, is_collision=None, last_time=None):
        """ :returns: bool; if object1 has collided with object2's right_edge because one of the objects has moved
            (the object1 did not collide with object2 horizontally last cycle)"""

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        is_collision = is_collision if is_collision is not None else CollisionsEngine.is_collision(object1, object2)
        object1_has_moved_into_object2 = (
                prev_object1.left_edge > prev_object2.right_edge and object1.left_edge < object2.right_edge)

        return is_collision and object1_has_moved_into_object2

    @staticmethod
    def is_moving_left_collision(object1, object2, is_collision=None, last_time=None):
        """ :returns: bool; if object1 has hit object2's left_edge because one of the objects has moved
            (the object1 did not collide with object2 horizontally last cycle)"""

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        is_collision = is_collision if is_collision is not None else CollisionsEngine.is_collision(object1, object2)

        object1_has_moved_into_object2 = prev_object1.right_edge < prev_object2.left_edge and object1.right_edge > object2.left_edge
        return is_collision and object1_has_moved_into_object2

    @staticmethod
    def is_bottom_collision(object1, object2, is_collision=None, time=None):
        """ :returns: bool; whether object1 has collided with object2's bottom_edge
        """

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        objects_are_touching = object1.top_edge == object2.bottom_edge and CollisionsEngine.is_horizontal_collision(
            object1,
            object2)
        is_collision = is_collision if is_collision is not None else CollisionsEngine.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.top_edge > prev_object2.bottom_edge and
                object1.top_edge < object2.bottom_edge) or objects_are_touching

    @staticmethod
    def is_top_collision(object1, object2, is_collision=None, time=None):
        """:returns: bool; whether object1 has collided with object2's top_edge"""

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        # So rounding doesn't cause any issues
        objects_are_touching = int(object1.bottom_edge) == int(object2.top_edge) and CollisionsEngine.is_horizontal_collision(object1, object2)
        is_collision = is_collision if is_collision is not None else CollisionsEngine.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.bottom_edge < prev_object2.top_edge
                and object1.bottom_edge > object2.top_edge) or objects_are_touching


