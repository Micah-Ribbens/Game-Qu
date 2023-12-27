from math import sqrt


def get_string(string_list):
    """ Returns:
            str: all the items of 'string_list' combined into one string value"""

    return_value = ""

    for item in string_list:
        return_value += item

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
    """ Finds the kwarg item (return 'get_kwarg_item_or_default.' This function is kept to have the library API stay the same across versions)

        Args:
            kwargs (dict): the **kwargs
            key (object): the key for the item
            default_value (object): the value that will be obtained if the kwargs doesn't contain the key

         Returns:
            Object; kwargs.get(key) if kwargs contains the key otherwise it will return the default_value
    """

    return get_kwarg_item_or_default(kwargs, key, default_value)


def get_kwarg_item_or_default(kwargs, key, default_value):
    """ Finds the kwarg item

        Args:
            kwargs (dict): the **kwargs
            key (object): the key for the item
            default_value (object): the value that will be obtained if the kwargs doesn't contain the key

         Returns:
            object: kwargs.get(key) if kwargs contains the key otherwise it will return the default_value
    """

    return kwargs.get(key) if kwargs.__contains__(key) else default_value


def solve_quadratic(a, b, c):
    """  Returns:
            list[float]: [answer1, answer2] the answers to the quadratic
            and if the answer is an imaginary number it  Returns:
            float('nan')"""

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


def min_value(item1, item2):
    """ Returns:
            float: the smallest item"""

    if item1 is None:
        return item2

    if item2 is None:
        return item1

    return item1 if item1 < item2 else item2


def max_value(item1, item2):
    """ Returns:
            float: the biggest item"""

    if item1 is None:
        return item2

    if item2 is None:
        return item1

    return item1 if item1 > item2 else item2
