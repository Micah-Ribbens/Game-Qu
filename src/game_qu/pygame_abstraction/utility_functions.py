from game_qu.pygame_abstraction import variables
from game_qu.pygame_abstraction.keys import *
import pygame
import time

fonts = {}
images = {}

def convert_to_int(*args):
    """
             Returns:
            list[int]: each arg as an int"""

    return_value = []

    for arg in args:
        return_value.append(int(arg))

    return return_value

def load_image(path_to_image):
    """ Loads the image from that path_to_image for quick rendering (should be called before the game starts running)

         Returns:
            list[int]: {image_length, image_height}; the length and height of the image"""

    if images.get(path_to_image) is None:
        images[path_to_image] = pygame.image.load(path_to_image).convert_alpha()

    return images[path_to_image].get_size()

def load_text(name, font_size, background_color, text_color):
    """Loads the text for quick rendering (should be called before the game starts running)"""

    if fonts.get(font_size) is None:
        fonts[font_size] = pygame.font.Font("freesansbold.ttf", font_size)

def render_text(left_edge, top_edge, text_color, background_color, text, font_size, is_centered, name, is_rendering_background=True):
    """Renders the text onto the screen"""

    left_edge, top_edge = convert_to_int(left_edge, top_edge)

    font = fonts.get(font_size)
    if not is_rendering_background:
        background_color = None

    rendered_text = font.render(text, True, text_color, background_color)
    text_rectangle = rendered_text.get_rect()

    if is_centered:
        text_rectangle.center = [left_edge, top_edge]

    else:
        text_rectangle.left = left_edge
        text_rectangle.top = top_edge

    variables.window.blit(rendered_text, text_rectangle)

def render_image(path_to_image, left_edge, top_edge, length, height):
    """Renders the image onto the screen"""

    left_edge, top_edge, length, height = convert_to_int(left_edge, top_edge, length, height)
    image = images.get(path_to_image)
    image = pygame.transform.scale(image, (length, height))
    variables.window.blit(image, (left_edge, top_edge))


def render_rectangle(left_edge, top_edge, length, height, color):
    """Renders the rectangle onto the screen"""

    left_edge, top_edge, length, height = convert_to_int(left_edge, top_edge, length, height)
    pygame.draw.rect(variables.window, color, [left_edge, top_edge, length, height])


def render_ellipse(left_edge, top_edge, length, height, color):
    """Renders the elipse onto the screen"""

    left_edge, top_edge, length, height = convert_to_int(left_edge, top_edge, length, height)
    pygame.draw.ellipse(variables.window, color, [left_edge, top_edge, length, height])

def set_up_window(length, height, background_color, title):
    """Initializes all the pygame code, so the game be run and rendered"""

    length, height = convert_to_int(length, height)
    variables.window = pygame.display.set_mode((length, height))
    pygame.display.set_caption(title)
    variables.background_color = background_color


def key_is_pressed(keyboard_key):
    """
             Returns:
            bool: if the 'keyboard_key' is currently pressed this game cycle"""

    game_engine_key = keyboard_keys_to_game_engine_keys.get(keyboard_key)

    controls = pygame.key.get_pressed()
    return controls[game_engine_key]

def button_is_pressed(button):
    """
             Returns:
            bool: if the 'button' is currently pressed this game cycle"""

    game_engine_button = keyboard_keys_to_game_engine_keys.get(button)

    dpad_buttons = {DPAD_UP: 0, DPAD_DOWN: 0, DPAD_LEFT: 0, DPAD_RIGHT: 0}
    return_value = None

    if dpad_buttons.get(button) is not None:
        return_value = dpad_is_pressed(button)

    else:
        return_value = variables.joystick.get_button(game_engine_button)

    return return_value

def dpad_is_pressed(dpad_button):
    """
             Returns:
            bool: if the 'dpad_button' is currently pressed this game cycle"""

    joystick_axis = 0
    value_wanted = .8

    if dpad_button == DPAD_UP or dpad_button == DPAD_DOWN:
        joystick_axis = 1

    if dpad_button == DPAD_LEFT or dpad_button == DPAD_UP:
        value_wanted = -value_wanted

    return_value = None

    if value_wanted < 0:
        return_value = variables.joystick.get_axis(joystick_axis) <= value_wanted

    else:
        return_value = variables.joystick.get_axis(joystick_axis) >= value_wanted

    return return_value


def mouse_was_pressed():
    """
             Returns:
            bool: whether the mouse is currently held down this game cycle"""

    return pygame.mouse.get_pressed()[0]


def call_every_cycle(function):
    """Makes pygame call the 'function' given every game cycle (60fps)"""

    while True:
        start_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        variables.window.fill(variables.background_color)

        function(start_time, True, True)
        pygame.display.update()

def run_checking_closing():
    """Runs all the pygame code that checks to make sure the game should be closed"""

    pass


def is_mouse_collision(dimensions):
    """
             Returns:
            bool: whether the mouse has collided with that rectangle - dimensions (left_edge, top_edge, length, height)"""

    area = pygame.Rect(dimensions.left_edge, dimensions.top_edge, dimensions.length, dimensions.height)
    mouse_left_edge, mouse_top_edge = pygame.mouse.get_pos()
    return area.collidepoint(mouse_left_edge, mouse_top_edge)


def get_mouse_position():
    """
        Returns:
            tuple[int]: {left_edge, top_edge}; the position of the mouse"""

    return pygame.mouse.get_pos()


def get_time_passed(start_time):
    """
             Returns:
            bool: the amount of time that has passed between the current time and start time"""

    return time.time() - start_time


def load_and_transform_image(image_path):
    """Loads the image at the 'image_path' then it also loads an image that is the horizontal mirror of the original image"""

    base_image = pygame.image.load(f"{image_path}_right.png").convert_alpha()
    transformed_image = pygame.transform.flip(base_image, True, False)

    images[f"{image_path}_right.png"] = base_image
    images[f"{image_path}_left.png"] = transformed_image


def get_directional_path_to_image(base_image_path, direction_is_right, additional_path_after_direction):
    """
             Returns:
            str: the path to the image that includes direction"""

    direction_image_path = "right" if direction_is_right else "left"

    return f"{base_image_path}_{direction_image_path}{additional_path_after_direction}.png"
