from abc import ABC, abstractmethod


class SensorTypeBase(ABC):
    @abstractmethod
    def format_value(self, value):
        ...
