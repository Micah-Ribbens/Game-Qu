from game_qu.math.linear_interpolation import LinearInterpolation
from game_qu.paths.action_followable_path import ActionFollowablePath
from game_qu.paths.velocity_followable_path import VelocityFollowablePath


class Path(LinearInterpolation):
    """ Made up of multiple lines that are all connected. The previous point and the next point are connected by a line.
        For instance, a line looks like: LineSegment(points[0], points[1]). IMPORTANT: no LineSegments can share the same
        x_coordinate (besides the first x_coordinate between adjacent lines) otherwise the code won't work. Also understand
        that this the same as LinearInterpolation. I kept this class to have the API of the library stay the same across
        versions. It is not c"""

    pass


class VelocityPath(VelocityFollowablePath):
    """A path that takes into account velocity. This is the same as VelocityFollowablePath. I kept this class here to have
        the programming API across versions (it is recommended to use the other 'VelocityFollowablePath' because it is
        technically more correct)."""

    pass


class ActionPath(ActionFollowablePath):
    """ A path that performs an action at each of the points. This does not work the FollowablePath methods. This will have
        to change in the future. This is the same as ActionFollowablePath. I kept this class here to have
        the programming API across versions (it is recommended to use the other 'ActionFollowablePath' because it is
        technically more correct)."""

    pass


