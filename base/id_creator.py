import random

from game_qu.base.unique_ids_list import unique_ids
from game_qu.base.library_independant_utility_functions import get_string


class IDCreator:
    """A class that creates simple unique identifiers"""

    all_chs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'z', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?']

    current_unique_id_index = -1  # So when one is added it goes to index 0

    def get_unique_id_of_length(self, length):
        """ :returns: str; a unique id with the length 'length.' IMPORTANT: it is recommended to call
            'self.get_unique_id' because that method will be quicker."""

        random.shuffle(self.all_chs)
        return get_string(self.all_chs[:length])

    def get_unique_id(self):
        """:returns: str; a unique identifier"""

        self.current_unique_id_index += 1
        return_value = None

        if self.current_unique_id_index < len(unique_ids):
            return_value = unique_ids[self.current_unique_id_index]

        else:
            return_value = self.get_unique_id_of_length(5)

        return return_value


id_creator = IDCreator()
