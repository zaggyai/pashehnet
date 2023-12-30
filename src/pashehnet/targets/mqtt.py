import uuid

import paho.mqtt.client as mqtt

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

        :param hostname: MQTT broker hostname
        :param port: MQTT broker port
        :param username: MQTT broker username
        :param password: MQTT broker password
        :param client_id: MQTT client ID
        :param client_id_prefix: MQTT client prefix
        :param protocol: MQTT protocol version (MQTTv31 | MQTTv311 | MQTTv5)
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

        if not self.client_id:
            if not self.client_id_prefix:
                self.client_id_prefix = 'pashehnet'
            self.client_id = f'{self.client_id_prefix}--{str(uuid.uuid4())}'

        # Client object; needs to be instantiated on worker proc/thread
        self.client = None

    def send(self, topic, payload):
        """
        Publish the payload to the topic

        :param topic: Topic (channel) to publish to
        :param payload: Payload (data) to publish
        :return: None
        """
        if not self.client:
            self._init_client()
        self.client.publish(topic, payload)

    def _init_client(self):
        """
        Internal method to initialize the MQTT client on the local
        thread/process to get around MP issues with calling
        paho.mqtt.publish.single()
        :return: None
        """
        client = mqtt.Client(
            client_id=self.client_id,
            clean_session=True,
            userdata=None,
            protocol=self.protocol,
            transport="tcp"
        )
        client.username_pw_set(
            self.username,
            self.password
        )
        client.connect(
            self.hostname,
            self.port
        )
        client.loop_start()
        self.client = client
