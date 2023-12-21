"""Has all the variables that are important for the pyglet code to run"""

import pyglet

mouse_position = []
WINDOW = pyglet.window.Window(100, 100, "title")

BACKGROUND_COLOR = None
background_filler = None

keys = pyglet.window.key.KeyStateHandler()
mouse_buttons = pyglet.window.mouse.MouseStateHandler()
