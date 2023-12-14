import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from .base import SensorTargetBase


class MQTTTarget(SensorTargetBase):
    """
    Class implementing MQTT target for PashehNet
    """
    MQTTv31 = mqtt.MQTTv31
    MQTTv311 = mqtt.MQTTv311
    MQTTv5 = mqtt.MQTTv5

    def __init__(self, hostname="localhost", port=1883, client_id="",
                 protocol=MQTTv311, retain=False):
        self.hostname = hostname
        self.port = port
        self.client_id = client_id
        self.protocol = protocol
        self.retain = retain

    def send(self, topic, payload):
        publish.single(
            topic=topic,
            payload=payload,
            retain=self.retain,
            hostname=self.hostname,
            port=self.port,
            client_id=self.client_id,
            protocol=self.protocol
        )