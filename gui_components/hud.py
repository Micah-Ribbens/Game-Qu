from game_qu.gui_components.grid import Grid
from game_qu.base.colors import *
from game_qu.gui_components.component import Component
from game_qu.base.important_variables import *
from game_qu.gui_components.text_box import TextBox
from game_qu.gui_components.dimensions import Dimensions

class HUD(Component):
    """HUD stands for Heads Up Display. This class provides an easy way to show all the information that the player needs"""

    player_points_fields = []
    other_fields = []
    high_score_field = None
    components = []
    high_score_is_needed = False
    rows = 1
    columns = None

    def __init__(self, number_of_points_fields, other_fields, length, height, rows=1, columns=None, high_score_is_needed=False):
        """ Initializes the object with the values provided by initializing the TextBox(s) needed.
            Also fields is just another way of saying TextBox. The HUD uses the Grid class from game_qu.gui_components/grid.py to make the grid pattern

            :parameter number_of_points_fields: int; the number of fields that contain points for players (generally equal to the number of players)
            :parameter other_fields: Component[]; the other fields that should be displayed
            :parameter length: float; the length of the HUD (in pixels)
            :parameter height: float; the height of the HUD (in pixels)
            :parameter rows: int; the number of rows for the grid of the HUD (see gui_components/grid.py for more information)
            :parameter columns: int; the number of columns for the grid of the HUD (see gui_components/grid.py for more information)
            :parameter high_score_is_needed: bool; whether a high score is wanted for the HUD

            :returns: None
        """

        self.player_points_fields = []
        self.rows = rows
        self.columns = columns
        self.high_score_is_needed = high_score_is_needed

        if high_score_is_needed:
            self.high_score_field = TextBox("", 28, pleasing_green, white, True)
            other_fields += [self.high_score_field]

        colors = [blue, red, black, orange, purple, yellow]

        for x in range(number_of_points_fields):
            self.player_points_fields.append(TextBox("", 28, white, colors[x], True))

        self.components = self.player_points_fields + other_fields

        grid = Grid(Dimensions(0, 0, length, height), rows, columns)
        grid.turn_into_grid(self.components, None, None)

    def update(self, player_points, high_score=0):
        """Updates the points in the 'player_points_fields' and if the 'high_score_is_needed' it updates the high score in the 'high_score_field'"""

        for x in range(len(player_points)):
            self.player_points_fields[x].text = f"Player #{x + 1}: {player_points[x]}"

        if self.high_score_is_needed:
            self.high_score_field.text = f"High Score: {high_score}"

    def render(self):
        """Renders the HUD onto the screen"""

        for component in self.components:
            component.render()

    def set_dimensions(self, left_edge, top_edge, length, height):
        """Changes the dimensions of the Grid that defines the components layouts"""

        grid = Grid(Dimensions(left_edge, top_edge, length, height), self.rows, self.columns)
        grid.turn_into_grid(self.components, None, None)

    def set_rows_and_columns(self, rows, columns):
        """Sets the 'self.rows' and 'self.columns' to the values provided: 'rows' and 'columns'"""

        self.rows = rows
        self.columns = columns
