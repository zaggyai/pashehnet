from abc import ABC, abstractmethod


class SensorTransformBase(ABC):
    @abstractmethod
    def transform(self, value):
        ...
