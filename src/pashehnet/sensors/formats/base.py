from abc import ABC, abstractmethod


class SensorFormatBase(ABC):
    """
    Abstract base class for all PashehNet formatters
    """
    @abstractmethod
    def transform(self, value):
        ...
