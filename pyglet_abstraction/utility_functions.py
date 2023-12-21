from pyglet.window import mouse

from game_qu.pyglet_abstraction.keys import *
from game_qu.pyglet_abstraction import variables
import pyglet
from pyglet import window, clock

images = {}
drawable_images = {}
text_boxes = {}
rectangles = {}

def load_image(path_to_image):
    """ Loads the image from that path_to_image for quick rendering (should be called before the game starts running)
        :returns: int[2] {image_length, image_height}; the length and height of the image"""

    if images.get(path_to_image) is None:
        images[path_to_image] = [pyglet.image.load(path_to_image), False]

    image = images[path_to_image][0]

    return image.width, image.height

def load_text(name, font_size, background_color, text_color):
    """Loads the text for quick rendering (should be called before the game starts running)"""

    text_boxes[name] = pyglet.text.Label("", font_name="Freesansbold", font_size=font_size, color=list(text_color)+[255])

def get_dimensions_conversion(top_edge, height):
    """Converts from 0, 0 being the top left side of the screen to 0, 0 being the bottom left side of the screen"""

    top_edge = variables.WINDOW.height - top_edge - height
    bottom_edge = top_edge + height
    return [top_edge, bottom_edge]

def render_text(left_edge, top_edge, text_color, background_color, text, font_size, is_centered, name):
    """Renders the text onto the screen"""

    top_edge, unused = get_dimensions_conversion(top_edge, 0)
    text_box: pyglet.text.Label = text_boxes.get(name)

    if text_box.x != left_edge or text_box.y != top_edge:
        text_box.x, text_box.y = left_edge, top_edge

    if text_box.text != text:
        text_box.text = text

    anchor_type = "center" if is_centered else ""
    if text_box.anchor_x != anchor_type:
        text_box.anchor_x, text_box.anchor_y = anchor_type, anchor_type

    text_box.draw()

def render_image(path_to_image, left_edge, top_edge, length, height):
    """Renders the image onto the screen"""

    top_edge, unused = get_dimensions_conversion(top_edge, height)
    image = images.get(path_to_image)[0]

    name = f"{path_to_image}{length}{height}"

    if drawable_images.get(name) is None:
        drawable_image = pyglet.sprite.Sprite(image, left_edge, top_edge)
        drawable_image.scale_x = length / drawable_image.width
        drawable_image.scale_y = height / drawable_image.height
        drawable_images[name] = drawable_image

    drawable_image = drawable_images.get(name)

    was_transformed = images.get(path_to_image)[1]

    if was_transformed:
        left_edge += length

    if drawable_image.x != left_edge or drawable_image.y != top_edge:

        drawable_image.x, drawable_image.y = left_edge, top_edge

    drawable_image.draw()


def render_rectangle(left_edge, top_edge, length, height, color):
    """Renders the rectangle onto the screen"""

    top_edge, unused = get_dimensions_conversion(top_edge, height)
    name = f"{left_edge}{top_edge}{length}{height}{color}"

    if rectangles.get(name) is None:
        rectangles[name] = pyglet.shapes.Rectangle(left_edge, top_edge, length, height, color=color)

    rectangles.get(name).draw()

def set_up_window(length, height, background_color, title):
    """Initializes all the pyglet code, so the game be run and rendered"""

    variables.WINDOW.set_size(length, height)
    variables.WINDOW.set_caption(title)

    variables.background_color = background_color
    variables.background_filler = pyglet.shapes.Rectangle(0, 0, length, height, color=background_color)

    variables.WINDOW.push_handlers(variables.keys)
    variables.WINDOW.push_handlers(variables.mouse_buttons)

def key_is_pressed(keyboard_key):
    """:returns: bool; if the keyboard key is currently pressed this game cycle"""

    game_engine_key = keyboard_keys_to_game_engine_keys.get(keyboard_key)
    return variables.keys[game_engine_key]

def call_every_cycle(function):
    """Makes pyglet call the 'function' given every game cycle (60fps); makes pyglet call the function _call_every_cycle every game cycle"""

    clock.schedule_interval(lambda time: _call_every_cycle(time, function), 1 / 60)
    pyglet.app.run()

def _call_every_cycle(time, function):
    """This is the function that pyglet actually calls every cycle (calls the 'function' passed into call_every_cyle()"""

    variables.background_filler.draw()
    function(time, False, True)

def is_mouse_collision(dimensions):
    """:returns: bool; whether the mouse has collided with that rectangle - dimensions (left_edge, top_edge, length, height)"""

    mouse_left_edge, mouse_top_edge = variables.mouse_position

    dimensions_top_edge, dimensions_bottom_edge = get_dimensions_conversion(dimensions.top_edge, dimensions.height)

    is_horizontal_collision = mouse_left_edge >= dimensions.left_edge and mouse_left_edge <= dimensions.right_edge
    is_vertical_collision = mouse_top_edge >= dimensions_top_edge and mouse_top_edge <= dimensions_bottom_edge

    return is_horizontal_collision and is_vertical_collision

def get_time_passed(unused):
    """This function is never used, but other game engines like pygame need this function, so it must exist"""

    return -1

def get_mouse_position():
    """:returns: int[]; the left_edge, top_edge of the mouse"""

    return variables.mouse_position

@variables.WINDOW.event
def on_mouse_motion(x, y, dx, dy):
    """Updates the position of the mouse"""

    variables.mouse_position = [x, y]

@variables.WINDOW.event
def on_key_press(symbol, modifiers):
    """When the Escape key is pressed it makes sure not to close the window"""

    if symbol == key.ESCAPE:
        return pyglet.event.EVENT_HANDLED

def mouse_was_pressed():
    """:returns: bool; whether the mouse is currently held down this game cycle"""

    return variables.mouse_buttons[pyglet.window.mouse.LEFT]


def load_and_transform_image(image_path):
    """Loads the image at the 'image_path' then it also loads an image that is the horizontal mirror of the original image"""

    original_image = pyglet.image.load(f"{image_path}_right.png")
    transformed_image = original_image.get_texture().get_transform(flip_x=True)

    images[f"{image_path}_right.png"] = [original_image, False]
    images[f"{image_path}_left.png"] = [transformed_image, True]


def get_directional_path_to_image(base_image_path, direction_is_right, additional_path_after_direction):
    """:returns: str; the path to the image that includes direction"""

    direction_image_path = "right" if direction_is_right else "left"

    return f"{base_image_path}_{direction_image_path}{additional_path_after_direction}.png"
