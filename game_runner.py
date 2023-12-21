from game_qu.base.library_changer import LibraryChanger

LibraryChanger.set_game_library("pygame")
LibraryChanger.set_screen_dimensions(2200, 1300)
LibraryChanger.set_is_using_controller(False)

from game_qu.base.game_runner_function import run_game
from game_qu.gui_components.screen import Screen

run_game(Screen())