import logging
import time
from collections import namedtuple

import pytest

from pashehnet import Sensor
from pashehnet.network import SensorNetwork
from pashehnet.sensors.formats import CSVFormat
from pashehnet.sensors.sources import ConstantValueSource
from pashehnet.targets import SensorTargetBase


@pytest.fixture()


q = multiprocessing.Queue()

@pytest.fixture()
def target():
    return MockSensorTarget()


TopicPayload = namedtuple('TopicPayload', ['topic', 'payload'])


class MockSensorTarget(SensorTargetBase):
    def __init__(self):
        super().__init__()
        self.log = []

    def send(self, topic, payload):
        print('sending')
        self.log.append(TopicPayload(topic, payload))


class TestNetwork:
    def test_network(self, target, caplog):
        topic = 'foo'
        id = 'bar'
        source = ConstantValueSource(42)
        format = CSVFormat(headers=False)
        sensor = Sensor(id, source=source, format=format)

        network = SensorNetwork(target)
        network.add_sensor(topic, sensor)

        network.start()
        time.sleep(5)
        network.stop()

        print(f'target log: {target.log}')
        assert 0 < len(target.log)
