from game_qu.gui_components.text_box import TextBox
from game_qu.base.timed_event import TimedEvent


class Button(TextBox):
    """ Essentially a 'TextBox,' but with other useful features: mainly it can change color when the user hovers their
        mouse over it and/or clicks it"""

    default_color = None
    hover_color = None
    clicked_color = None
    switch_back_to_default_color_timed_event = None

    def __init__(self, text, font_size, background_color, text_color, is_centered):
        """ Initializes the object

            Args:
                text (str): the text that is displayed
                font_size (int): the size of the font
                background_color (tuple): the (Red, Green, Blue) values of the text box's background
                text_color (tuple): the (Red, Green, Blue) values of the text's color
                is_centered (bool): whether the text inside the text box is centered
     
            Returns:
                None
        """

        super().__init__(text, font_size, background_color, text_color, is_centered)
        self.set_colors(background_color, background_color, background_color)  # So the button doesn't change color
        self.switch_back_to_default_color_timed_event = TimedEvent(float("inf"), False)

        self.set_mouse_functions(self.mouse_enter, self.mouse_exit)

    def set_colors(self, default_color, hover_color, clicked_color):
        """Sets the colors of the Button
        
            Args:
                default_color: (list[int]): {red, green, blue}; The color of the button when the button isn't clicked or hovered over
                hover_color: (list[int]): {red, green, blue}; The color of the button when it is hovered over
                clicked_color: (list[int]): {red, green, blue}; The color of the button after it is clicked"""

        self.default_color = default_color
        self.hover_color = hover_color
        self.clicked_color = clicked_color

    def set_click_color_change_duration(self, duration):
        """Sets the duration that the button changes color to 'clicked_color' after it is clicked"""

        self.switch_back_to_default_color_timed_event.set_time_needed(duration)

    def run(self):
        """Runs everything necessary for the Button to function properly"""

        super().run()
        self.switch_back_to_default_color_timed_event.run()

        if self.got_clicked():
            self.set_background_color(self.clicked_color)
            self.switch_back_to_default_color_timed_event.start()

        if self.switch_back_to_default_color_timed_event.is_done():
            self.set_background_color(self.default_color)
            self.switch_back_to_default_color_timed_event.reset()

    def mouse_enter(self):
        """Runs what happens when the mouse enters the button: the button changing color to the 'hover_color'"""

        self.set_background_color(self.hover_color)

    def mouse_exit(self):
        """Runs what happens when the mouse exits the button: the button changing color to the 'default_color'"""

        self.set_background_color(self.default_color)
