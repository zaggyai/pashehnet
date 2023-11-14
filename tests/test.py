import os
import pytest


@pytest.fixture()
def mqtt_host():
    return os.getenv('MQTT_HOST')


@pytest.fixture()
def mqtt_port():
    return os.getenv('MQTT_PORT')


@pytest.fixture()
def mqtt_user():
    return os.getenv('MQTT_USER')


@pytest.fixture()
def mqtt_pwd():
    return os.getenv('MQTT_PWD')


@pytest.fixture()
def mqtt_use_ssl():
    return os.getenv('MQTT_USE_SSL', False)


class TestSensors:
    pass


class TestAPI:
    pass


class TestClient:
    pass
