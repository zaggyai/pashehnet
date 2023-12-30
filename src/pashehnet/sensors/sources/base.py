from abc import ABC, abstractmethod


class SensorSourceBase(ABC):
    """
    Abstract base class for all sensor sources;
    atm a thin wrapper for an iterator.
    """
    def __iter__(self):
        """
        Implementation for iterator

        :return: Self
        """
        return self

    @abstractmethod
    def __next__(self):
        """
        Implementation for iterator

        :return: Next value from sensor source
        """
        ...
