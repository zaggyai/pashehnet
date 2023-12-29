from .base import SensorFormatBase


class SimpleFormat(SensorFormatBase):
    """
    Provides a plain, simple formatter that just returns the stringified value
    """
    def transform(self, value):
        """
        Format the value using ths builtin str()

        :param value: Value to format
        :return: Stringified value
        """
        return str(value)
