from abc import ABC, abstractmethod


class SensorFormatBase(ABC):
    @abstractmethod
    def transform(self, value):
        ...
