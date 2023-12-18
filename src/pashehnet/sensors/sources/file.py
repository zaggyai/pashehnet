from queue import SimpleQueue

from .base import SensorSourceBase
from smart_open import open


class FileSource(SensorSourceBase):
    def __init__(self, uri, dtype=float):
        """
        Constructor for file source that can read file contents,
        one reading per line.
        :param uri: Local filesystem or URI to open file from
        :param dtype: Data type to cast read values from
        """
        self.sample = SimpleQueue()
        for line in open(uri):
            self.sample.put(dtype(line.strip()))

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
