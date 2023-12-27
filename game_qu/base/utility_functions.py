import math

from math import sqrt
from game_qu.base.library_changer import LibraryChanger

if not LibraryChanger.get_library_has_been_set():
    LibraryChanger.set_game_library("pygame")

from game_qu.base.fraction import Fraction
from game_qu.base.important_variables import keyboard, SCREEN_LENGTH, SCREEN_HEIGHT, IS_USING_CONTROLLER
import random

from game_qu.library_abstraction import utility_functions
from game_qu.base.range import Range

# Retrieving the functions from the game library code
load_image = getattr(utility_functions, "load_image")
load_text = getattr(utility_functions, "load_text")
render_text = getattr(utility_functions, "render_text")
render_image = getattr(utility_functions, "render_image")
render_ellipse = getattr(utility_functions, "render_ellipse")
render_rectangle = getattr(utility_functions, "render_rectangle")
set_up_window = getattr(utility_functions, "set_up_window")
key_is_pressed = getattr(utility_functions, "key_is_pressed")
mouse_was_pressed = getattr(utility_functions, "mouse_was_pressed")
call_every_cycle = getattr(utility_functions, "call_every_cycle")
is_mouse_collision = getattr(utility_functions, "is_mouse_collision")
get_time_passed = getattr(utility_functions, "get_time_passed")
load_and_transform_image = getattr(utility_functions, "load_and_transform_image")
get_directional_path_to_image = getattr(utility_functions, "get_directional_path_to_image")

def key_is_pressed(key):
    """ Returns:
            bool: whether that key is currently held down (pressed)"""

    return keyboard.get_key_event(key).happened_this_cycle


def key_is_clicked(key):
    """ Returns:
            bool: whether the key was not held down last cycle and is this cycle (clicked)"""

    return keyboard.get_key_event(key).is_click()


def key_has_been_released(key):
    """ Returns:
            bool: whether the key was held down last cycle and is not this cycle (released)"""
    return keyboard.get_key_event(key).has_stopped()


def get_time_of_key_being_held_in(key):
    """ Returns:
            float: the amount of time that the key has been held down"""

    return keyboard.get_key_timed_event(key).current_time

def button_is_pressed(button):
    """ Returns:
            bool: whether that button is currently held down (pressed)"""

    return keyboard.get_button_event(button).happened_this_cycle


def button_is_clicked(button):
    """ Returns:
            bool: whether the button was not held down last cycle and is this cycle (clicked)"""

    return keyboard.get_button_event(button).is_click()


def button_has_been_released(button):
    """ Returns:
            bool: whether the button was held down last cycle and is not this cycle (released)"""

    return keyboard.get_button_event(button).has_stopped()

def get_time_of_button_being_held_in(button):
    """ Returns:
            float: the amount of time that the button has been held down"""

    return keyboard.get_button_timed_event(button).current_time

def button_is_pressed(button):
    """ Returns:
            bool: whether that button is currently held down (pressed)"""

    return keyboard.get_button_event(button).happened_this_cycle

def get_game_button_timed_event(game_button):
    """ Returns:
            TimedEvent: the TimedEvent that is associated with the current state (using the keyboard or controller)"""

    return keyboard.get_button_timed_event(game_button) if IS_USING_CONTROLLER else keyboard.get_key_timed_event(game_button)
def get_game_button_event(game_button):
    """ Returns:
            Event: the Event that is associated with the current state (using the keyboard or controller)"""

    return keyboard.get_button_event(game_button) if IS_USING_CONTROLLER else keyboard.get_key_event(game_button)

def game_button_is_pressed(game_button):
    """ Returns:
            bool: whether that game_button is currently held down (pressed)"""

    return get_game_button_event(game_button).happened_this_cycle

def game_button_is_clicked(game_button):
    """ Returns:
            bool: whether the game_button was not held down last cycle and is this cycle (clicked)"""

    return get_game_button_event(game_button).is_click()

def game_button_has_been_released(game_button):
    """ Returns:
            bool: whether the game_button was held down last cycle and is not this cycle (released)"""

    return get_game_button_event(game_button).has_stopped()

def get_time_of_game_button_being_held_in(game_button):
    """ Returns:
            float: the amount of time that the game_button has been held down"""

    return get_game_button_timed_event(game_button).current_time


def mouse_is_clicked():
    """ Returns:
            bool: whether the mouse was not pressed last cycle and is this cycle (clicked)"""

    return keyboard.mouse_clicked_event.is_click()


def get_index_of_range(number, range_lengths=[], ranges=None):
    """ Finds the index of the range that contains the current number. A range is defined by the numbers between
        two adjacent indexes (range_lengths[0] -> range_lengths[1])

        Args:
            range_lengths (list[float]): the lengths of the ranges. For instance, if the range_lengths is [1, 1, 1] then the ranges would be [0 -> 1, 1 -> 2, 2 -> 3]
            number (float): the number that is wanted to be within a range

         Returns:
            int: The index of the range that contains the number and -1 no range contains it"""

    index = -1

    if ranges is None:
        ranges = get_ranges(range_lengths)

    for x in range(len(ranges)):
        if ranges[x].__contains__(number):
            index = x
            break

    return index


def get_ranges(range_lengths) -> list[Range]:
    """ Returns:
            list[Range]: the ranges gotten from the range_lengths. A range is defined by two adjacent indexes (range_lengths[0] -> range_lengths[1])"""

    return_value = []
    current_value = 0

    for range_length in range_lengths:
        return_value.append(Range(current_value, current_value + range_length))
        current_value += range_length

    return return_value

def is_within_screen(game_object):
    """ Returns:
            bool: if the game_object is within the screen (can be seen on the screen)"""

    return (game_object.right_edge > 0 and game_object.left_edge < SCREEN_LENGTH and
            game_object.bottom_edge > 0 and game_object.top_edge < SCREEN_HEIGHT)


def is_random_chance(probability: Fraction):
    """ Uses the probability for the random chance (for instance if the probability is 7/10 then 7 out of 10
        times it will return True and the other 3 times it will return False)

        Args:
            probability (Fraction): the probability this function will return True

         Returns:
            bool: if the random number between 1-probability.denominator is >= probability.numerator
    """

    return random.randint(1, probability.denominator) <= probability.numerator


def is_beyond_screen_left(left_edge):
    """ Returns:
            bool: if the left_edge is beyond the left side of the screen"""

    return left_edge <= 0


def is_beyond_screen_right(right_edge):
    """ Returns:
            bool: if the right_edge is beyond the right side of the screen"""

    return right_edge >= SCREEN_LENGTH


def min_value(item1, item2):
    """ Returns:
            float: the smallest item"""

    if item1 is None:
        return item2

    if item2 is None:
        return item1

    return item1 if item1 < item2 else item2


def max_value(item1, item2):
    """Returns:
        float: the biggest item"""

    return item1 if item1 > item2 else item2


def get_combined_number_values(numbers):
    """ Returns:
            float or int: all the numbers in 'numbers' added up together in one number"""

    return_value = 0

    for number in numbers:
        return_value += number

    return return_value

def get_next_index(current_index, max_index):
    """ Returns:
            int: the index after current_index (it cycles, so once it gets beyond the max_index it goes back to 0)"""

    next_index = current_index + 1
    return next_index if next_index <= max_index else 0


def get_previous_index(current_index, max_index):
    """ Returns:
            int: the index before current_index (it cycles, so once it gets below 0 it goes to the max_index"""

    prev_index = current_index - 1
    return prev_index if prev_index >= 0 else max_index

def rounded(number, places):
    """ Returns:
            float: the number rounded to that many decimal places"""

    rounded_number = int(number * pow(10, places))

    # Converting it back to the proper decimals once it gets rounded from above
    return rounded_number / pow(10, places)

def get_kwarg_item(kwargs, key, default_value):
    """ Returns the value associated with the key in kwargs and the default value if the key is not in kwargs
    
        Args:
            kwargs (dict): the **kwargs
            key (object): the key for the item
            default_value (object): the value that will be obtained if the kwargs doesn't contain the key

         Returns:
            object: kwargs.get(key) if kwargs contains the key otherwise it will return the default_value
    """

    return kwargs.get(key) if kwargs.__contains__(key) else default_value

def solve_quadratic(a, b, c):
    """ Returns:
            list[float]: [answer1, answer2] the answers to the quadratic
            and if the answer is an imaginary number it returns float('nan')"""

    number_under_square_root = pow(b, 2) - 4 * a * c
    number_under_square_root = rounded(number_under_square_root, 4)

    if number_under_square_root < 0:
        return None

    square_root = sqrt(number_under_square_root)

    answer1 = (-b + square_root) / (2 * a)
    answer2 = (-b - square_root) / (2 * a)

    answers = [answer2, answer1]

    # If the answers are the same I should only return one of them
    return answers if answers[0] != answers[1] else [answers[0]]


def modified_mod(number, modulus):
    """ This is a modified version of the modulus operator. This performs the same way for negative numbers and positive
        numbers. This means that 50 % 9 = 5 and -50 % 9 = -5.

         Returns:
            float: the number % modulus that conforms to the rules specified above"""

    number_is_negative = number < 0
    value = math.fabs(number) % modulus
    constant_factor = -1 if number_is_negative else 1  # So the number can be converted back to a negative number

    # If the decimal is chopped off by converting it into an int and it is still the same value, it must be equal
    modulus_is_whole_number = modulus == int(modulus)

    if modulus_is_whole_number:
        number_decimal = get_decimal_with_full_accuracy(number)
        int_number = int(number)
        value = int(math.fabs(int_number)) % modulus
        value += number_decimal

    return value * constant_factor  # An int should be gotten back


def get_decimal_with_full_accuracy(number):
    """ Returns:
            float: the decimal part of the number i.e. 1.2345 -> 0.2345 (maintains full decimal accuracy)"""

    string_number = str(number)
    float_string = ""
    for x in range(len(string_number)):
        if string_number[x] == ".":
            float_string = f"0{string_number[x:]}"  # [x:] gives the entire decimal ('.' onwards)

    return float(float_string) if len(float_string) != 0 else 0


def do_nothing(*args):
    """This function does absolutely nothing (useful if you want to have a command and have it by default do nothing)"""

    pass


def is_within_bounds(value, min_value, max_value):
    """ Checks if the 'value' is within the specified bounds
    
        Args:
            value (float): value to be checked
            min_value (float): minimum bound
            max_value (float): maximum bound

        Returns:
            bool: whether the value is within the specified bounds"""

    return min_value <= value <= max_value

def get_sign(number):
    """ Returns:
            int: -1 if the number is negative and 1 if the number is positive"""

    return -1 if number < 0 else 1


def get_inverse_sign(number):
    """ Returns:
            int: 1 if the number is negative and -1 if the number is positive"""

    return -get_sign(number)

