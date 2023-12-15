from abc import ABC, abstractmethod


class SensorTargetBase(ABC):
    @abstractmethod
    def send(self, topic, payload):
        ...
