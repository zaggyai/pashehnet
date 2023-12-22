import uuid

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

    def __init__(self,
                 hostname="localhost",
                 port=1883,
                 username=None,
                 password=None,
                 client_id=None,
                 client_id_prefix=None,
                 protocol=MQTTv311):
        """
        CTOR for MQTT publishing target

        :param hostname:
        :param port:
        :param username:
        :param password:
        :param client_id:
        :param client_id_prefix:
        :param protocol:
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_id_prefix = client_id_prefix
        self.protocol = protocol if (
                protocol in [self.MQTTv311, self.MQTTv31, self.MQTTv5]) else (
            self.__getattribute__(protocol))

        self.auth = {'username': self.username, 'password': self.password} if (
            self.username) else None

        if not self.client_id:
            if not self.client_id_prefix:
                self.client_id_prefix = 'pashehnet'
            self.client_id = f'{self.client_id_prefix}--{str(uuid.uuid4())}'

    def send(self, topic, payload):
        publish.single(
            topic=topic,
            payload=payload,
            hostname=self.hostname,
            port=self.port,
            auth=self.auth,
            client_id=self.client_id,
            protocol=self.protocol,
            retain=False
        )
