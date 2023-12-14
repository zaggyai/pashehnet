import pytest

from pashehnet.sensors import Sensor
from pashehnet.sensors.formats import CSVFormat
from pashehnet.sensors.sources import ConstantValueSource


@pytest.fixture()
def cv_source():
    return ConstantValueSource(42)


@pytest.fixture()
def csv_format():
    fields = {
        'a': 1,
        'b': 2
    }
    return CSVFormat(prefix_fields=fields, value_field='value')


class TestSensor:
    """
    Unit tests for Sensor class
    """

    def test(self, cv_source, csv_format):
        """
        Test sensor returns expected value from iterator
        :param cv_source: ConstantValueSource fixture
        :param csv_format: CSVFormat fixture
        """
        sensor = Sensor(0, source=cv_source, format=csv_format)
        assert 'a,b,value\n1,2,42' == next(sensor)
