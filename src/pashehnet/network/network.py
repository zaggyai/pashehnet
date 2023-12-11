import logging
import multiprocessing
import os
import signal
import sys
from multiprocessing import Process
from time import sleep

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


class SensorProcess(Process):
    def signal_handler(self, sig, frame):
        logging.debug('SensorProcess closing')
        sys.exit(1)

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        super.run()


class SensorNetwork(object):
    def __init__(self, target, sensors=[]):
        self.sensors = []
        self.sensor_procs = []
        self.target = target
        self.running = False
        self.add_sensors(sensors)

    def add_sensor(self, sensor):
        if not self.running:
            self.sensors.append(sensor)

    def add_sensors(self, sensors):
        for sensor in sensors:
            self.add_sensor(sensor)

    def start(self):
        try:
            self.sensor_procs = [
                multiprocessing.Process(target=self._proc_fn, args=(sensor))
                for
                sensor in self.sensors
            ]

            for p in self.sensor_procs:
                p.start()

            self.running = True
        except Exception as e:
            logging.error(str(e))

    @staticmethod
    def _proc_fn(sensor):
        while True:
            sleep(1)

    def stop(self):
        try:
            for p in self.sensor_procs:
                p.terminate()

            for p in self.sensor_procs:
                p.join()

            self.running = False
        except Exception as e:
            logging.error(str(e))
