"""Holds all the important variables for the game like screen_dimensions, BACKGROUND_COLOR, etc"""

from game_qu.base.library_changer import LibraryChanger
from game_qu.base.important_constants import *

if not LibraryChanger.get_library_has_been_set():
    LibraryChanger.set_game_library(DEFAULT_RENDERING_ENGINE)

from game_qu.base.keyboard import Keyboard
from game_qu.gui_components.window import Window
from game_qu.library_abstraction import keys

keyboard = Keyboard()
game_window = Window(SCREEN_LENGTH, SCREEN_HEIGHT, BACKGROUND_COLOR, "Game Basics")

KEY_A = keys.KEY_A
KEY_B = keys.KEY_B
KEY_C = keys.KEY_C
KEY_D = keys.KEY_D
KEY_E = keys.KEY_E
KEY_F = keys.KEY_F
KEY_G = keys.KEY_G
KEY_H = keys.KEY_H
KEY_I = keys.KEY_I
KEY_J = keys.KEY_J
KEY_K = keys.KEY_K
KEY_L = keys.KEY_L
KEY_M = keys.KEY_M
KEY_N = keys.KEY_N
KEY_O = keys.KEY_O
KEY_P = keys.KEY_P
KEY_Q = keys.KEY_Q
KEY_R = keys.KEY_R
KEY_S = keys.KEY_S
KEY_T = keys.KEY_T
KEY_U = keys.KEY_U
KEY_V = keys.KEY_V
KEY_W = keys.KEY_W
KEY_X = keys.KEY_X
KEY_Y = keys.KEY_Y
KEY_Z = keys.KEY_Z
KEY_LEFT = keys.KEY_LEFT
KEY_RIGHT = keys.KEY_RIGHT
KEY_UP = keys.KEY_UP
KEY_DOWN = keys.KEY_DOWN
KEY_QUESTION_MARK = keys.KEY_QUESTION_MARK
KEY_PERIOD = keys.KEY_PERIOD
KEY_COMMA = keys.KEY_COMMA
KEY_COLON = keys.KEY_COLON
KEY_QUOTATION_MARKS = keys.KEY_QUOTATION_MARKS
KEY_LEFT_BRACKET = keys.KEY_LEFT_BRACKET
KEY_RIGHT_BRACKET = keys.KEY_RIGHT_BRACKET
KEY_ESCAPE = keys.KEY_ESCAPE
KEY_SLASH = keys.KEY_SLASH

BUTTON_X = 0
BUTTON_A = 0
BUTTON_B = 0
BUTTON_Y = 0
BUTTON_L = 0
BUTTON_R = 0
BUTTON_SELECT = 0
BUTTON_START = 0
DPAD_UP = 0
DPAD_DOWN = 0
DPAD_LEFT = 0
DPAD_RIGHT = 0

if LibraryChanger.current_library_name == "pygame":
    BUTTON_X = keys.BUTTON_X
    BUTTON_A = keys.BUTTON_A
    BUTTON_B = keys.BUTTON_B
    BUTTON_Y = keys.BUTTON_Y
    BUTTON_L = keys.BUTTON_L
    BUTTON_R = keys.BUTTON_R
    BUTTON_SELECT = keys.BUTTON_SELECT
    BUTTON_START = keys.BUTTON_START
    DPAD_UP = keys.DPAD_UP
    DPAD_DOWN = keys.DPAD_DOWN
    DPAD_LEFT = keys.DPAD_LEFT
    DPAD_RIGHT = keys.DPAD_RIGHT