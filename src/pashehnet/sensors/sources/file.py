from queue import SimpleQueue

from .base import SensorSourceBase
from smart_open import open


class FileSource(SensorSourceBase):
    """
    Provides a file-based source, one value per line, from a local file or URI
    """
    def __init__(self, uri, dtype=float):
        """
        Constructor for file source that can read file contents,
        one reading per line.

        :param uri: Local filesystem or URI to open file from
        :param dtype: Data type to cast read values from
        """
        self.uri = uri
        self.dtype = dtype
        self.sample = None

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
        for line in open(self.uri):
            self.sample.put(self.dtype(line.strip()))
