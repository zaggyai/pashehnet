from abc import ABC, abstractmethod


class SensorTargetBase(ABC):
    """
    Abstract base class for all PashehNet targets
    """
    @abstractmethod
    def send(self, topic, payload):
        """
        Pure abstract method for sending a payload to a topic/channel

        :param topic: Topic/channel to publish to
        :param payload: Payload to publish
        :return: None
        """
        ...
