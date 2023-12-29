import logging
import os
import signal
from collections import namedtuple
from multiprocessing import Process

from pashehnet.targets import SensorTargetBase

########################################
# Set up logging
########################################
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
logging.getLogger().setLevel(
    logging.getLevelName(
        os.getenv('LOG_LEVEL', 'WARN').upper()
    )
)


# Define namedtuples
TopicSensor = namedtuple('TopicSensor', ['topic', 'sensor'])


class SensorProcess(Process):
    """
    Class that wraps a SensorNetwork sensor child process
    """
    def __init__(self, target: SensorTargetBase, topic, sensor):
        super(SensorProcess, self).__init__()
        self.target = target
        self.topic = topic
        self.sensor = sensor

    def run(self):
        while True:
            try:
                payload = next(self.sensor)
                logging.debug(
                    f'Sensor {self.sensor.id} '
                    f'sending payload {payload} '
                    f'to {self.topic}')
                self.target.send(self.topic, payload)
            except Exception as e:
                logging.error(f'Sensor {self.sensor.id}, exception: {str(e)}')
                continue


class SensorNetwork(object):
    """
    Class that provides a network of simulated sensors, publishing to a single
    target.
    """
    def __init__(self, target):
        self.sensors = []
        self.sensor_procs = []
        self.target = target
        self.running = False

    def add_sensor(self, topic, sensor):
        """
        Add a sensor publishing to a given topic

        :param topic: Topic/channel to publish to
        :param sensor: Sensor to read from and publish to topic
        """
        if not self.running:
            self.sensors.append(TopicSensor(topic, sensor))

    def add_sensors(self, topic, sensors):
        """
        Add a collection of sensors publishing to the same topic

        :param topic: Topic/channel to publish to
        :param sensor: Sensors to read from and publish to topic
        """
        for sensor in sensors:
            self.add_sensor(topic, sensor)

    def start(self):
        """
        Start the simulated sensor network
        """
        try:
            for (topic, sensor) in self.sensors:
                self.sensor_procs.append(SensorProcess(
                    target=self.target,
                    topic=topic,
                    sensor=sensor
                ))
            for p in self.sensor_procs:
                logging.debug(
                    f'SensorProcess starting: {p.topic} // {p.sensor}'
                )
                p.start()

            logging.debug(
                f'Started {len(self.sensor_procs)} sensor processes.'
            )
            self.running = True

            signal.signal(signal.SIGINT, self.stop)
            signal.signal(signal.SIGTERM, self.stop)
        except Exception as e:
            logging.error(str(e))

    def stop(self, signum=None, frame=None):
        """
        Stop the simulated sensor network; doubles as a signal handler for
        SIGINT and SIGTERM
        """
        try:
            for p in self.sensor_procs:
                logging.debug(
                    f'SensorProcess terminating: {p.topic} // {p.sensor}'
                )
                p.terminate()

            for p in self.sensor_procs:
                logging.debug(
                    f'SensorProcess joining: {p.topic} // {p.sensor}'
                )
                p.join()

            logging.debug(
                f'Terminated {len(self.sensor_procs)} sensor processes.'
            )
            self.running = False
        except Exception as e:
            logging.error(str(e))
