import os

import pytest


@pytest.fixture()
def mqtt_host():
    return os.getenv('MQTT_HOST', 'localhost').strip()


@pytest.fixture()
def mqtt_port():
    return int(os.getenv('MQTT_PORT', '1883').strip())


@pytest.fixture()
def mqtt_user():
    return os.getenv('MQTT_USER').strip()


@pytest.fixture()
def mqtt_pwd():
    return os.getenv('MQTT_PWD').strip()


@pytest.fixture()
def mqtt_use_ssl():
    val = os.getenv('MQTT_USE_SSL', 'false').strip().lower()
    return val == 'true' or val == '1'


class TestMQTT:
    def test_noop(self):
        assert 42 == 42
