import math

from game_qu.base.important_variables import SCREEN_HEIGHT
from game_qu.base.utility_functions import get_kwarg_item, solve_quadratic
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.math.function import Function
from game_qu.math.physics_function import PhysicsFunction
from game_qu.math.quadratic_function import QuadraticFunction
from game_qu.paths.physics_followable_path import PhysicsFollowablePath


class QuadraticEquation(QuadraticFunction):
    """The same class as QuadraticFunction, but this is kept to keep the API the same between library versions"""

    pass


class PhysicsEquation(PhysicsFunction):
    """The same class as PhysicsFunction, but this is kept to keep the API the same between library versions"""

    pass


class PhysicsPath(PhysicsFollowablePath):
    """The same class as PhysicsFollowablePath, but this is kept to keep the API the same between library versions"""

    pass
