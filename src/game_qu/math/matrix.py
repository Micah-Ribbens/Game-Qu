from copy import deepcopy


class Matrix:
    """Represents an n x m matrix. This supports many common matrix operations"""

    backing_list = []

    def __init__(self, backing_list):
        """Initializes the object with the backing_list; the list must be a n x m matrix"""

        self.set_backing_list(backing_list)

    def set_backing_list(self, backing_list):
        """ Sets the backing_list; the list must be a n x m matrix

            Returns:
                Matrix: 'self'"""

        self.backing_list = backing_list
        return self

    def get_vector_with_backing_list(self, backing_list):
        """
             Returns:
                Matrix: a matrix with the provided backing list"""

        return self.get_copy().set_backing_list(backing_list)

    def get_backing_list(self):
        """
             Returns:
                list[object]: the n x m backing list"""

        return self.backing_list

    def validate_matrices_are_same_size(self, other_matrix):
        """Raises a ValueError if the other matrix does not have the same n and m values for the n x m matrix"""

        other_backing_list = other_matrix.get_backing_list()

        if len(other_backing_list) != len(self.backing_list):
            raise ValueError("The matrices must have the same n and m values for the n x m matrix")

        if len(self.backing_list) != 0 and len(other_backing_list[0]) == len(self.backing_list[0]):
            raise ValueError("The matrices must have teh same n and m values for the n x m matrix")

    def add(self, other_matrix):
        """ Adds the other matrix to the current matrix; note they must both have same n and m values for the n x m matrix

            Returns:
                Matrix: 'self'"""

        other_backing_list = other_matrix.get_backing_list()
        self.validate_matrices_are_same_size(other_matrix)

        for i in range(len(self.backing_list)):
            for j in range(len(self.backing_list[0])):
                self.backing_list[i][j] += other_backing_list[i][j]

        return self

    def get_added_matrix(self, other_matrix):
        """
             Returns:
                Matrix: the matrix that results from adding the other matrix to this matrix (does not modify this matrix)"""

        return self.get_copy().add(other_matrix)

    def subtract(self, other_matrix):
        """ Subtracts the other matrix from the current matrix; note they must both have same n and m values for the n x m matrix

            Returns:
                Matrix: 'self'"""

        other_backing_list = other_matrix.get_backing_list()
        self.validate_matrices_are_same_size(other_matrix)

        for i in range(len(self.backing_list)):
            for j in range(len(self.backing_list[0])):
                self.backing_list[i][j] -= other_backing_list[i][j]

        return self

    def get_subtracted_matrix(self, other_matrix):
        """
             Returns:
                Matrix: the matrix that results from subtracting the other matrix from this matrix (does not modify this matrix)"""

        return self.get_copy().subtract(other_matrix)

    def subtract_constant(self, constant):
        """ Subtract a constant from all values in the matrix

            Returns:
                Matrix: 'self'"""

        for i in range(len(self.backing_list)):
            for j in range(len(self.backing_list[0])):
                self.backing_list[i][j] -= constant

        return self

    def get_constant_subtracted_matrix(self, constant):
        """
             Returns:
                Matrix: the matrix that results from subtracting a constant from all values in this matrix (does not modify this matrix)"""

        return self.get_copy().subtract_constant(constant)

    def add_constant(self, constant):
        """ Adds a constant to all values in the matrix

            Returns:
                Matrix: 'self'"""

        for i in range(len(self.backing_list)):
            for j in range(len(self.backing_list[0])):
                self.backing_list[i][j] += constant

        return self

    def get_constant_added_matrix(self, constant):
        """
             Returns:
                Matrix: the matrix that results from adding a constant to all values in this matrix (does not modify this matrix)"""

        return self.get_copy().add_constant(constant)

    def multiply_by_scalar(self, scalar):
        """ Multiplies all values in the matrix by the scalar

            Returns:
                Matrix: 'self'"""

        for i in range(len(self.backing_list)):
            for j in range(len(self.backing_list[0])):
                self.backing_list[i][j] *= scalar

        return self

    def get_scalar_multiplied_matrix(self, scalar):
        """
             Returns:
                Matrix: the matrix that results from multiplying all values in this matrix by a scalar (does not modify this matrix)"""

        return self.get_copy().multiply_by_scalar(scalar)

    def hadamard_product(self, other_matrix):
        """ Multiplies all values each matrix and adds the result to this matrix. Both matrices must have the same n and m values for the n x m matrix

            Returns:
                Matrix: 'self'"""

        other_backing_list = other_matrix.get_backing_list()
        self.validate_matrices_are_same_size(other_matrix)

        for i in range(len(self.backing_list)):
            for j in range(len(self.backing_list[0])):
                self.backing_list[i][j] *= other_backing_list[i][j]

        return self

    def get_hadamard_product_matrix(self, other_matrix):
        """
             Returns:
                Matrix: the matrix that results from the Hadamard product of this matrix with another matrix (does not modify this matrix)"""

        return self.get_copy().hadamard_product(other_matrix)


    def __add__(self, other_matrix):
        """ Adds the other matrix to the current matrix; note they must both have same n and m values for the n x m matrix

            Returns:
                Matrix: 'self'"""

        return self.add(other_matrix)

    def __sub__(self, other_matrix):
        """ Subtracts the other matrix from the current matrix; note they must both have same n and m values for the n x m matrix

            Returns:
                Matrix: 'self'"""

        return self.subtract(other_matrix)

    def __mul__(self, other_matrix):
        """ Multiplies all values each matrix and adds the result to this matrix. Both matrices must have the same n and m values for the n x m matrix

            Returns:
                Matrix: 'self'"""

        return self.hadamard_product(other_matrix)

    def get_copy(self):
        """
             Returns:
                Matrix: the copy of the current matrix"""

        list_copy = deepcopy(self.backing_list)
        return Matrix(list_copy)
