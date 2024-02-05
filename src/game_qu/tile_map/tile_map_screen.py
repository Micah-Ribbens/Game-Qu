import math
import functools

from game_qu.base.library_changer import LibraryChanger
from game_qu.tile_map.tile import Tile

LibraryChanger.set_screen_dimensions(1000, 600)

from game_qu.base.game_runner_function import run_game
from game_qu.gui_components.button import Button
from game_qu.gui_components.component import Component
from game_qu.gui_components.dimensions import Dimensions
from game_qu.gui_components.grid import Grid
from game_qu.gui_components.screen import Screen
from game_qu.base.colors import *
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.base.important_variables import *
from game_qu.base.utility_functions import get_mouse_position, mouse_is_clicked


class TileMapScreen(Screen):
    save_button = Button("Save", 15, pleasing_green, white, True)
    load_button = Button("Load", 15, pleasing_green, white, True)
    play_button = Button("Play", 15, pleasing_green, white, True)
    show_grid_button = Button("Show Grid", 15, pleasing_green, white, True)

    paint_brush_button = Button("Paint Brush", 15, pleasing_green, white, True)
    eraser_button = Button("Eraser", 15, pleasing_green, white, True)

    top_tool_bar = []
    bottom_tool_bar = []
    grid_lines = []
    tiles = []

    # Modifiable variables
    top_tool_bar_height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 10)
    bottom_tool_bar_height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 10)
    rows = 8
    columns = 8
    line_width = VelocityCalculator.get_dimension(SCREEN_LENGTH, 0.5)

    is_painting = True
    last_tile_was_previously_visible = False
    temp_last_tile_was_previously_visible = False
    last_tile_was_clicked = False
    last_tile = None

    def __init__(self):
        """Initializes the object"""

        super().__init__("", light_gray)

        self.tiles = []

        self.top_tool_bar = [self.paint_brush_button, self.eraser_button]
        self.bottom_tool_bar = [self.save_button, self.load_button, self.play_button, self.show_grid_button]

        top_grid = Grid(Dimensions(0, 0, SCREEN_LENGTH, self.top_tool_bar_height), 1, None)
        bottom_grid = Grid(Dimensions(0, SCREEN_HEIGHT - self.bottom_tool_bar_height, SCREEN_LENGTH,
                            self.bottom_tool_bar_height), 1, None)

        top_grid.turn_into_grid(self.top_tool_bar)
        bottom_grid.turn_into_grid(self.bottom_tool_bar)
        self.update_grid_lines()

        self.buttons = [self.save_button, self.load_button, self.play_button, self.show_grid_button,
                            self.paint_brush_button, self.eraser_button]

        for button in self.buttons:
            button.set_colors(button.get_color(), dark_green, button.get_color())

        self.paint_brush_button.set_command(lambda: self.set_is_painting(True))
        self.eraser_button.set_command(lambda: self.set_is_painting(False))

    def run(self):
        for tile in self.tiles:
            tile.run()


    def update_grid_lines(self):
        for i in range(self.rows - 1):
            for j in range(self.columns - 1):
                left_edge = (i + 1) * self.box_length + self.start_left_edge
                top_edge = (j + 1) * self.box_height + self.start_top_edge

                line1 = Component("")
                line2 = Component("")

                line1.set_color(black)
                line2.set_color(black)

                line1.number_set_dimensions(left_edge, self.start_top_edge, self.line_width, self.grid_height)
                line2.number_set_dimensions(self.start_left_edge, top_edge, self.grid_length, self.line_width)

                self.grid_lines.extend([line1, line2])

        for i in range(self.rows):
            new_tiles = []

            for j in range(self.columns):
                tile = Tile("")
                tile.set_color(blue)
                tile.set_is_visible(False)
                tile.set_is_runnable(False)

                left_edge = j * self.box_length + self.start_left_edge + self.line_width
                top_edge = i * self.box_height + self.start_top_edge + self.line_width
                length = self.box_length - self.line_width + 1  # So the tile fills the entire box
                height = self.box_height - self.line_width + 1  # So the tile fills the entire box

                tile.number_set_dimensions(left_edge, top_edge, length, height)

                tile.set_mouse_enter_function(lambda x=tile: self.run_mouse_enter_tile(x))
                tile.set_mouse_exit_function(lambda x=tile: self.run_mouse_exit_tile(x))
                tile.set_command(lambda x=tile: self.run_tile_clicked(x))

                new_tiles.append(tile)

            self.tiles.extend(new_tiles)

    def get_grid_row_and_column(self, left_edge, top_edge):
        """Gets the row and column of the grid that the left edge and top edge are in"""

        column = math.floor((left_edge - self.start_left_edge) / self.box_length)
        row = math.floor((top_edge - self.start_top_edge) / self.box_height)

        return row, column

    def run_mouse_enter_tile(self, tile):
        """Runs what should happen when the mouse enters the tile"""

        if not self.is_painting:
            tile.set_is_temporarily_invisible(True)

        tile.set_is_visible(self.is_painting)

    def run_mouse_exit_tile(self, tile):
        """Runs what should happen when the mouse exits the tile"""

        tile.set_is_temporarily_invisible(False)
        tile.set_is_visible(tile.get_is_active())

    def run_tile_clicked(self, tile):
        """Runs what should happen when the tile is clicked"""

        tile.set_is_active(self.is_painting)

    def get_components(self):
        return self.bottom_tool_bar + self.grid_lines + self.top_tool_bar + self.tiles

    def set_is_painting(self, is_painting):
        self.is_painting = is_painting

    @property
    def start_top_edge(self):
        return self.top_tool_bar_height

    @property
    def start_left_edge(self):
        return 0

    @property
    def grid_length(self):
        return SCREEN_LENGTH

    @property
    def grid_height(self):
        return SCREEN_HEIGHT - self.top_tool_bar_height - self.bottom_tool_bar_height

    @property
    def box_length(self):
        return self.grid_length / self.columns

    @property
    def box_height(self):
        return self.grid_height / self.rows

    @property
    def tile(self):
        row, column = self.get_grid_row_and_column(*get_mouse_position())
        return self.tiles[row * self.columns + column]


run_game(TileMapScreen())
