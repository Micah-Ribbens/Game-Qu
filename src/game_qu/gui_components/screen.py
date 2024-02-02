from game_qu.base.colors import light_gray
from game_qu.base.utility_functions import render_image
from game_qu.gui_components.component import Component
from game_qu.base.important_variables import *
from game_qu.base.utility_functions import *

screen_sized_component = Component()
screen_sized_component.number_set_dimensions(0, 0, SCREEN_LENGTH, SCREEN_HEIGHT)


class Screen(Component):
    """ Is the only thing that shows on the window at a time. The Window class (gui_components/window.py) will call the Screen's
        run() and render_background() method will be called every game frame. It will also the run() and render() method for
        all the Component(s) that the Screen's get_components() method returns"""

    components = []
    path_to_background_image = ""
    is_visible = True
    background_color = light_gray

    def __init__(self, path_to_background_image="", background_color=light_gray):
        """ Initializes the object and also loads the image which is at the path 'path_to_background_image.' No image will
            be loaded if path_to_background_image is ''"""

        super().__init__("")

        self.path_to_background_image = path_to_background_image
        self.background_color = background_color

        if self.path_to_background_image != "":
            load_image(path_to_background_image)

    def get_components(self):
        """
             Returns:
                list[Component]: the components of the screen"""

        return self.components

    def render_background(self):
        """Renders the background image that is at the path 'path_to_background_image'"""

        if self.path_to_background_image != "":
            render_image(self.path_to_background_image, 0, 0, SCREEN_LENGTH, SCREEN_HEIGHT)

        else:
            screen_sized_component.color = self.background_color
            screen_sized_component.render()

    def set_is_visible(self, is_visible):
        """Sets whether this screen is visible"""

        self.is_visible = is_visible

    def show(self):
        """Makes the screen visible"""

        self.set_is_visible(True)

    def hide(self):
        """Makes the screen not visible"""

        self.set_is_visible(False)

    def set_background_color(self, background_color):
        """Sets the background color"""

        self.background_color = background_color

    def set_path_to_background_image(self, path_to_background_image):
        """Sets the path to the background image (if it is '' then the screen is filled with the 'background_color'"""

        self.path_to_background_image = path_to_background_image

    def render(self):
        pass
