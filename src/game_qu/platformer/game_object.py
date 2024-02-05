from game_qu.base.id_creator import id_creator
from game_qu.gui_components.component import Component


class GameObject(Component):
    """A class that use is for providing functions and attributes that must be in common for all game objects (or at least almost all)"""

    object_type = ""
    name = None

    def __init__(self, path_to_image=""):
        """Initializes the object"""

        super().__init__(path_to_image)
        self.name = id_creator.get_unique_id()

    def update_for_side_scrolling(self, amount):
        """Updates the inanimate object, so it side scrolls"""

        self.left_edge -= amount

    def get_collidable_components(self):
        """
            Returns:
                list[Component]: the components of this object that are collidable"""

        return [self]

    def run_collisions(self):
        """Runs all the collision logic for a game object"""

        pass

    def get_all_components(self):
        """
            Returns:
                list[Component]: all the components of this game_object
        """

        return [self]