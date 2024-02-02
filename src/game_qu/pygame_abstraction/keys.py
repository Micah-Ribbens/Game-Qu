"""Contains all the keys that the user can use. Feel free to add more by downloading the code off of GitHub and manually adding them"""

import pygame

KEY_A = 0
KEY_B = 1
KEY_C = 2
KEY_D = 3
KEY_E = 4
KEY_F = 5
KEY_G = 6
KEY_H = 7
KEY_I = 8
KEY_J = 9
KEY_K = 10
KEY_L = 11
KEY_M = 12
KEY_N = 13
KEY_O = 14
KEY_P = 15
KEY_Q = 16
KEY_R = 17
KEY_S = 18
KEY_T = 19
KEY_U = 20
KEY_V = 21
KEY_W = 22
KEY_X = 23
KEY_Y = 24
KEY_Z = 25
KEY_LEFT = 26
KEY_RIGHT = 27
KEY_UP = 28
KEY_DOWN = 29
KEY_QUESTION_MARK = 30
KEY_PERIOD = 31
KEY_COMMA = 32
KEY_COLON = 33
KEY_QUOTATION_MARKS = 34
KEY_LEFT_BRACKET = 35
KEY_RIGHT_BRACKET = 36
KEY_ESCAPE = 37
KEY_SLASH = 38
BUTTON_X = 39
BUTTON_A = 40
BUTTON_B = 41
BUTTON_Y = 42
BUTTON_L = 43
BUTTON_R = 44
BUTTON_SELECT = 45
BUTTON_START = 46
DPAD_UP = 47
DPAD_DOWN = 48
DPAD_LEFT = 49
DPAD_RIGHT = 50

keyboard_keys_to_game_engine_keys = {
    KEY_A: pygame.K_a,
    KEY_B: pygame.K_b,
    KEY_C: pygame.K_c,
    KEY_D: pygame.K_d,
    KEY_E: pygame.K_e,
    KEY_F: pygame.K_f,
    KEY_G: pygame.K_g,
    KEY_H: pygame.K_h,
    KEY_I: pygame.K_i,
    KEY_J: pygame.K_j,
    KEY_K: pygame.K_k,
    KEY_L: pygame.K_l,
    KEY_M: pygame.K_m,
    KEY_N: pygame.K_n,
    KEY_O: pygame.K_o,
    KEY_P: pygame.K_p,
    KEY_Q: pygame.K_q,
    KEY_R: pygame.K_r,
    KEY_S: pygame.K_s,
    KEY_T: pygame.K_t,
    KEY_U: pygame.K_u,
    KEY_V: pygame.K_v,
    KEY_W: pygame.K_w,
    KEY_X: pygame.K_x,
    KEY_Y: pygame.K_y,
    KEY_Z: pygame.K_z,
    KEY_LEFT: pygame.K_LEFT,
    KEY_RIGHT: pygame.K_RIGHT,
    KEY_UP: pygame.K_UP,
    KEY_DOWN: pygame.K_DOWN,
    KEY_LEFT: pygame.K_LEFT,
    KEY_RIGHT: pygame.K_RIGHT,
    KEY_UP: pygame.K_UP,
    KEY_DOWN: pygame.K_DOWN,
    KEY_QUESTION_MARK: pygame.K_QUESTION,
    KEY_PERIOD: pygame.K_PERIOD,
    KEY_COMMA: pygame.K_COMMA,
    KEY_COLON: pygame.K_COLON,
    KEY_QUOTATION_MARKS: pygame.K_QUOTE,
    KEY_LEFT_BRACKET: pygame.K_LEFTBRACKET,
    KEY_RIGHT_BRACKET: pygame.K_RIGHTBRACKET,
    KEY_ESCAPE: pygame.K_ESCAPE,
    KEY_SLASH: pygame.K_SLASH,
    BUTTON_X: 0,
    BUTTON_A: 1,
    BUTTON_B: 2,
    BUTTON_Y: 3,
    BUTTON_L: 4,
    BUTTON_R: 5,
    BUTTON_SELECT: 8,
    BUTTON_START: 9,
    DPAD_UP: 0,
    DPAD_DOWN: 1,
    DPAD_LEFT: 2,
    DPAD_RIGHT: 3
}

# keys = list(keyboard_keys_to_game_engine_keys.keys())
keys = [x for x in range(39)]
buttons = [BUTTON_A, BUTTON_X, BUTTON_Y, BUTTON_B, BUTTON_START, BUTTON_SELECT, BUTTON_L, BUTTON_R, DPAD_UP, DPAD_DOWN, DPAD_RIGHT, DPAD_LEFT]