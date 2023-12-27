class VelocityCalculator:
    """A utility class that has methods for figuring out the velocity, distance, and sizes of components"""

    time = 0
    delta_time = 0
    current_cycle_number = 1

    @staticmethod
    def get_velocity(unit_of_measurement, amount):
        """ Returns:
                float: (unit_of_measurement / 1000) * amount- This method breaks the unit_of_measurement into easier units to work with"""

        return (unit_of_measurement / 1000) * amount

    @staticmethod
    def get_dimension(unit_of_measurement, amount):
        """ Returns:
                float: (unit_of_measurement / 100) * amount- This method breaks the unit_of_measurement into easier units to work with"""
        return (unit_of_measurement / 100) * amount

    @staticmethod
    def get_distance(velocity):
        """ Returns:
                float: the amount of distance that has been traveled from that velocity since the last cycle (delta time * velocity)"""

        return velocity * VelocityCalculator.delta_time

    @staticmethod
    def set_delta_time(time):
        """Sets the delta time of the VelocityCalculator (the time between cycles)"""

        VelocityCalculator.time = time
        VelocityCalculator.delta_time = time

