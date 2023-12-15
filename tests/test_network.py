import multiprocessing
import time
from collections import namedtuple

import pytest

from pashehnet import Sensor
from pashehnet.network import SensorNetwork
from pashehnet.sensors.formats import CSVFormat
from pashehnet.sensors.sources import ConstantValueSource
from pashehnet.targets import SensorTargetBase


@pytest.fixture()
def mp_queue():
    return multiprocessing.Queue()


@pytest.fixture()
def target(mp_queue):
    return MockSensorTarget(mp_queue)


TopicPayload = namedtuple('TopicPayload', ['topic', 'payload'])


class MockSensorTarget(SensorTargetBase):
    def __init__(self, mp_queue):
        super().__init__()
        self.log = mp_queue

    def send(self, topic, payload):
        self.log.put(TopicPayload(topic, payload))


class TestNetwork:
    def test_network(self, target, mp_queue):
        topic = 'foo'
        id = 'bar'
        source = ConstantValueSource(42)
        format = CSVFormat(headers=False)
        sensor = Sensor(id, source=source, format=format, frequency=10)

        network = SensorNetwork(target)
        network.add_sensor(topic, sensor)

        network.start()
        time.sleep(3)
        network.stop()

        print(f'target log: {target.log}')
        assert not target.log.empty()
