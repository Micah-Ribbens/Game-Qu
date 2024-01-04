from game_qu.base.colors import light_gray
from game_qu.base.history_keeper import HistoryKeeper
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.utility_functions import load_image, render_image, render_rectangle, mouse_is_clicked, \
    is_mouse_collision, do_nothing
from game_qu.base.id_creator import id_creator
from game_qu.base.events import Event


class Component(Dimensions):
    """ The components that are added to the game's window. If a screen's get_components() method returns a component,
        that components run and render methods will be called"""

    color = light_gray
    path_to_image = None
    name = ""
    is_addable = True
    is_runnable = True  # Sometimes the screen has to run the player, so some components shouldn't be run
    last_frame_id_when_visible = 0
    image_length = 1
    image_height = 1

    # So these functions by default do nothing when called
    mouse_enter_function = do_nothing
    mouse_exit_function = do_nothing
    mouse_enter_event = None
    mouse_exit_event = None

    def __init__(self, path_to_image=""):
        """Initializes the object and loads an image if the path_to_image is not empty"""

        super().__init__(self.left_edge, self.top_edge, self.length, self.height)

        self.path_to_image = path_to_image

        if path_to_image != "":
            self.image_length, self.image_height = load_image(path_to_image)

        self.name = id_creator.get_unique_id()
        self.mouse_enter_event = Event()
        self.mouse_exit_event = Event()

    def run(self):
        """Runs everything the component needs every game cycle"""

        self.mouse_enter_event.run(is_mouse_collision(self))
        self.mouse_exit_event.run(not is_mouse_collision(self))

        # 'is_click()' in this circumstance means whether the mouse has either first exited this component or first
        # entered this component
        if self.mouse_enter_event.is_click():
            self.mouse_enter_function()

        if self.mouse_exit_event.is_click():
            self.mouse_exit_function()

    def render(self):
        """ Renders the component onto the screen- it will either render the image if 'self.path_to_image' is not empty
            otherwise it will render a rectangle with the color from 'self.color'"""

        if self.path_to_image != "":
            render_image(self.path_to_image, self.left_edge, self.top_edge, self.length, self.height)

        else:
            render_rectangle(self.left_edge, self.top_edge, self.length, self.height, self.color)

        self.last_frame_id_when_visible = HistoryKeeper.get_frame_id(VelocityCalculator.current_cycle_number)

    def got_clicked(self):
        """
             Returns:
                bool: the mouse is over the component and the mouse was clicked"""

        was_visible_last_cycle = self.last_frame_id_when_visible == HistoryKeeper.last_frame_id
        return mouse_is_clicked() and is_mouse_collision(self) and was_visible_last_cycle

    def get_scaled_dimensions(self, unscaled_length, unscaled_height):
        """
             Returns:
                list[float]: [scaled_length, scaled_height]; the length and height of the image that is scaled by the
                smallest of the two, so there is no stretching"""

        horizontal_scale_factor = unscaled_length / self.image_length
        vertical_scale_factor = unscaled_height / self.image_height

        smaller_scale_factor = horizontal_scale_factor if horizontal_scale_factor < vertical_scale_factor else vertical_scale_factor

        return [self.image_length * smaller_scale_factor, self.image_height * smaller_scale_factor]

    def set_mouse_functions(self, mouse_enter_function, mouse_exit_function):
        """Sets the functions that are called when the mouse enters and exits the component"""

        self.set_mouse_enter_function(mouse_enter_function)
        self.set_mouse_exit_function(mouse_exit_function)

    def set_mouse_enter_function(self, mouse_enter_function):
        """Sets the action that happens when a mouse enters this object"""

        self.mouse_enter_function = mouse_enter_function

    def set_mouse_exit_function(self, mouse_exit_function):
        """Sets the function that is called when the mouse exits this object"""

        self.mouse_exit_function = mouse_exit_function

    def set_color(self, color):
        """ Sets the color of the component. Only matters if 'path_to_image' is not set. If 'path_to_image' is set,
            then the image will be rendered instead of the default rectangle with a color of 'color'"""

        self.color = color

    def get_color(self):
        return self.color
