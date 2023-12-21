import os

class FileReader:
    """ Reads the contents of a file. The contents of the file must follow this format in order to be read: name:value.
        For instance, 'high_score:219.0' The value types allowed are int, float, str, bool, float[], and str[]. Generally
        it would be recommended to use python's built-in json package, but this is also an option for simple file saving and retrieving

        int-format: name:int (high_score:219)
        float_format: name:float (high_score:219.0)
        str-format: name:str (name:a)
        bool_format: name:bool (has_won_game:True)
        float[]-format: name:[val1,val2,val3] (high_scores:[1.0,2.0,3.0])
        str[]-format: name:[val1,val2,val3] (names:[a,b,c,d])"""

    name_to_data = {}

    def __init__(self, file_path):
        """ Initialize the class by reading the file from the 'file_path' and storing the data in 'self.name_to_object'.

            :parameter file_path: str; the path to the file

            :returns: None
        """

        lines = self.get_lines(file_path)

        for line in lines:
            delimiter_start = line.index(":")

            name = line[:delimiter_start]

            data = line[delimiter_start + 1:]

            self.name_to_data[name] = data

    def get_lines(self, file_path, new_line_delimiter="\n"):
        """ Opens the file that was gotten from open(file_path) and uses 'new_line_delimeter' to determine what is a new line

            :parameter file_path: str; the path to the file
            :parameter new_line_delimiter: str; the delimiter that decides if a new entry in the return_value (lines) should be created

            :returns: str[]; all the lines of the file"""

        file = open(file_path, "r+")
        lines = file.read().split(new_line_delimiter)
        file.close()
        return lines

    def get_int(self, name):
        """ Retrieves the integer value from 'self.name_to_data' associated with the key 'name'

            :parameter name: str; the name of the key

            :returns: int; the int value associated with the key 'name'
        """

        return int(self.name_to_data[name])

    def get_float(self, name):
        """ Retrieves the float value from 'self.name_to_data' associated with the key 'name'

            :parameter name: str; the name of the key

            :returns: float; the float value associated with the key 'name'
        """

        return float(self.name_to_data[name])

    def get_bool(self, name):
        """ Retrieves the bool value from 'self.name_to_data' associated with the key 'name'

            :parameter name: str; the name of the key

            :returns: bool; the bool value associated with the key 'name'
        """

        return self.name_to_data[name] == "True"

    def get_string_list(self, name):
        """ Retrieves the string list from 'self.name_to_data' associated with the key 'name'

            :parameter name: str; the name of the key

            :returns: str[]; the str[] value associated with the key 'name'
        """

        return self.name_to_data[name][1:-1].split(",")

    def get_float_list(self, name):
        """ Retrieves the float list from 'self.name_to_data' associated with the key 'name' (calls get_string_list())

            :parameter name: str; the name of the key

            :returns: float[]; the float[] value associated with the key 'name'
        """

        string_list = self.get_string_list(name)
        float_list = []

        for item in string_list:
            float_list.append(float(item))

        return float_list

    def get_string(self, name):
        """ Retrieves the string from 'self.name_to_data' associated with the key 'name'

            :parameter name: str; the name of the key

            :returns: str; the str value associated with the key 'name'
        """

        return self.name_to_data[name]





