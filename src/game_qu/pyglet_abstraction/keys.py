"""Contains all the keys that the user can use. Feel free to add more by downloading the code off of GitHub and manually adding them"""

from pyglet.window import key


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


keyboard_keys_to_game_engine_keys = {
    KEY_A: key.A,
    KEY_B: key.B,
    KEY_C: key.C,
    KEY_D: key.D,
    KEY_E: key.E,
    KEY_F: key.F,
    KEY_G: key.G,
    KEY_H: key.H,
    KEY_I: key.I,
    KEY_J: key.J,
    KEY_K: key.K,
    KEY_L: key.L,
    KEY_M: key.M,
    KEY_N: key.N,
    KEY_O: key.O,
    KEY_P: key.P,
    KEY_Q: key.Q,
    KEY_R: key.R,
    KEY_S: key.S,
    KEY_T: key.T,
    KEY_U: key.U,
    KEY_V: key.V,
    KEY_W: key.W,
    KEY_X: key.X,
    KEY_Y: key.Y,
    KEY_Z: key.Z,
    KEY_LEFT: key.LEFT,
    KEY_RIGHT: key.RIGHT,
    KEY_UP: key.UP,
    KEY_DOWN: key.DOWN,
    KEY_QUESTION_MARK: key.QUESTION,
    KEY_PERIOD: key.PERIOD,
    KEY_COMMA: key.COMMA,
    KEY_COLON: key.COLON,
    KEY_QUOTATION_MARKS: key.DOUBLEQUOTE,
    KEY_LEFT_BRACKET: key.BRACKETLEFT,
    KEY_RIGHT_BRACKET: key.BRACKETRIGHT,
    KEY_ESCAPE: key.ESCAPE,
    KEY_SLASH: key.SLASH
}

keys = list(keyboard_keys_to_game_engine_keys.keys())
