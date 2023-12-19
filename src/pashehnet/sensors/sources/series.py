from queue import SimpleQueue

from .base import SensorSourceBase


class SeriesSource(SensorSourceBase):
    """
    Class to provide a sensor source data from a list
    """

    def __init__(self, series):
        """
        Constructor for series source
        :param series: List of values to loop over
        """
        self.sample = SimpleQueue()
        for val in series:
            self.sample.put(val)

    def __iter__(self):
        """
        Implementation for iterator
        :return: Self
        """
        return self

    def __next__(self):
        """
        Implementation for iterator
        :return: Next value from source
        """
        val = self.sample.get()
        self.sample.put(val)
        return val
