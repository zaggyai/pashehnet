from abc import ABC, abstractmethod


class SensorTransformBase(ABC):
    """
    Abstract base class for all PashehNet transforms
    """
    @abstractmethod
    def transform(self, value):
        """
        Pue abstract method to apply transform to sensor datum

        :param value: Value to transform
        :return: Transformed value
        """
        ...
