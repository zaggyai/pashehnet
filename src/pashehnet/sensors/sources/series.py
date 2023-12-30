from queue import SimpleQueue

from .base import SensorSourceBase


class SeriesSource(SensorSourceBase):
    """
    Class to provide a sensor data source from a list
    """
    def __init__(self, series):
        """
        Constructor for series source

        :param series: List of values to loop over
        """
        self.sample = None
        self.series = series

    def __next__(self):
        """
        Implementation for iterator

        :return: Next value from source
        """
        if not self.sample:
            self._init_sample()
        val = self.sample.get()
        self.sample.put(val)
        return val

    def _init_sample(self):
        self.sample = SimpleQueue()
        for x in self.series:
            self.sample.put(x)
