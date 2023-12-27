from game_qu.base.count_event import CountEvent
from game_qu.library_abstraction import utility_functions


class Window:
    """Shows everything onto the users screen through adding components to it and displaying those added components"""

    screens = []
    is_rendering = True
    is_rendering_count_event = None

    def __init__(self, length, height, background_color, title):
        """ Creates a window with the length, height, and title of the values given

            Args:
                length (int): the length of the window
                height (int): the height of the window
                background_color (tuple): the (Red, Green, Blue) values of the window's background
                title (str): the title displayed of the window
     
            Returns:
                None
        """

        utility_functions.set_up_window(length, height, background_color, title)
        self.is_rendering_count_event = CountEvent(0)
        self.is_rendering_count_event.set_is_infinite(True)

    def add_screen(self, screen):
        """ Adds the screen to the Window if it is not already present, so the Window keeps track of it

            Returns:
                boolean: whether the screen was already present"""

        if not self.screens.__contains__(screen):
            self.screens.append(screen)

    def remove_screen(self, screen):
        """ Removes the screen from the Window if it is present, so the Window does not keep track of it

            Returns:
                boolean: whether the screen was present in the Window"""

        try:
            self.screens.remove(screen)
            return True
        except ValueError:
            return False

    def display_screen(self, screen):
        """ Makes all the other screen's invisible by setting their 'is_visible' attribute to False and makes the 'screen'
            visible by setting it's 'is_visible' attribute set to True"""

        for other_screen in self.screens:
            other_screen.hide()

        screen.show()

    def run(self, should_render):
        """ Calls the run() and render_background() method of all visible screens. It will also call the run() and render()
            methods for each of the Component(s) that the get_components() method returns for the visible screens"""

        # The window should be rendered if it was told to render or the rendering count event is done (the event is
        # modified by the user to define rendering behavior)
        user_says_to_render = self.is_rendering_count_event.current_count_is_positive()
        self.is_rendering_count_event.decrement()

        if user_says_to_render:
            should_render = True

        else:
            should_render &= self.is_rendering_count_event.get_is_infinite()

        for screen in self.screens:
            if not screen.is_visible:
                continue

            if screen.is_visible:
                screen.run()

            if screen.is_visible and should_render:
                screen.render_background()
                screen.render()

            for component in screen.get_components():
                if component.is_runnable:
                    component.run()

                if should_render:
                    component.render()

    def stop_rendering(self):
        """Stops the program from rendering"""

        self.is_rendering_count_event.set_is_infinite(False)
        self.is_rendering_count_event.disable()

    def render_for_one_frame(self):
        """Renders everything for exactly one frame"""

        self.render_for_x_frames(1)

    def render_for_x_frames(self, amount):
        """Renders the window for the specified number of frames"""

        self.is_rendering_count_event.set_times_needed_to_complete(amount)
        self.is_rendering_count_event.set_is_infinite(False)

    def continue_rendering(self):
        """Renders the window for all frames (runs as 'normal')"""

        self.is_rendering_count_event.set_is_infinite(True)
