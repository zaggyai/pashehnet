from abc import ABC, abstractmethod


class SensorTransformBase(ABC):
    """
    Abstract base class for all PashehNet transforms
    """
    @abstractmethod
    def transform(self, value):
        ...
