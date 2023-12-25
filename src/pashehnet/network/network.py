import logging
import os
import signal
import sys
from collections import namedtuple
from multiprocessing import Process

from pashehnet import Sensor
from pashehnet.targets import SensorTargetBase

########################################
# Set up logging
########################################
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logging.getLogger().setLevel(
    logging.getLevelName(
        os.getenv('LOG_LEVEL', 'WARN').upper()
    )
)

TopicSensor = namedtuple('TopicSensor', ['topic', 'sensor'])


class SensorProcess(Process):
    def __init__(self, target: SensorTargetBase, topic, sensor: Sensor):
        super(SensorProcess, self).__init__()
        self.target = target
        self.topic = topic
        self.sensor = sensor
        self.kill_now = False

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

    def run(self):
        while not self.kill_now:
            payload = next(self.sensor)
            self.target.send(self.topic, payload)


class SensorNetwork(object):
    def __init__(self, target):
        self.sensors = []
        self.sensor_procs = []
        self.target = target
        self.running = False

    def add_sensor(self, topic, sensor):
        if not self.running:
            self.sensors.append(TopicSensor(topic, sensor))

    def add_sensors(self, topic, sensors):
        for sensor in sensors:
            self.add_sensor(topic, sensor)

    def start(self):
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
        except Exception as e:
            logging.error(str(e))

    def stop(self):
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
