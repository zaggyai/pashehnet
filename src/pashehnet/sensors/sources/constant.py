from .base import SensorSourceBase


class ConstantValueSource(SensorSourceBase):
    """
    Provides a constant value source
    """
    def __init__(self, value):
        """
        Construct new object

        :param value: Constant value to emit
        """
        self.value = value

    def __next__(self):
        """
        Implementation for iterator

        :return: Next value from source
        """
        return self.value
