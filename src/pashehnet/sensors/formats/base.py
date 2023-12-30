from abc import ABC, abstractmethod


class SensorFormatBase(ABC):
    """
    Abstract base class for all PashehNet formatters
    """
    @abstractmethod
    def transform(self, value):
        """
        Abstract method to apply formatter to given value

        :param value: Value to format
        :return: Formatted value
        """
        ...
