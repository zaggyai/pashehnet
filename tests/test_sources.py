from pashehnet.sensors.sources import ConstantValueSource
from pashehnet.sensors.sources import SquareWaveSource
from pashehnet.sensors.sources import SawtoothWaveSource
import numpy as np
from scipy import signal
from pytest import approx

class TestConstantValueSource:
    """
    Unit tests for ConstantValueSource class
    """

    def test_source(self):
        """
        Test that expected value is returned in iterative requests
        :return:
        """
        val = 42
        src = ConstantValueSource(val)
        values = [next(src) for i in range(10)]
        assert all(v == val for v in values)


class TestSquareWaveSource:
    """
    Unit tests for SquareWaveSource class
    """

    def test_source(self):
        """
        Test that expected square wave values are returned in iterative requests
        """
        # Test parameters
        frequency, sample_rate, duty_cycle = 5, 500, 0.5

        # Create SquareWaveSource object
        src = SquareWaveSource(frequency, sample_rate, duty_cycle)

        # Generate values from the SquareWaveSource
        generated_values = [next(src) for i in range(sample_rate)]

        # Generate expected values
        t = np.linspace(0, 1, sample_rate, endpoint=False)
        expected_values = signal.square(2 * np.pi * frequency * t, duty=duty_cycle)

        # Compare generated values with expected values
        assert generated_values == approx(expected_values)


class TestSawtoothWaveSource:
    """
    Unit tests for SawtoothWaveSource class
    """

    def test_source(self):
        """
        Test that expected square wave values are returned in iterative requests
        """
        # Test parameters
        frequency, sample_rate, width = 5, 10, 0.5

        # Create SawtoothWaveSource object
        src = SawtoothWaveSource(frequency, sample_rate, width)

        # Generate values from the SquareWaveSource
        generated_values = [next(src) for i in range(sample_rate)]

        # Generate expected values
        t = np.linspace(0, 1, sample_rate, endpoint=False)
        expected_values = signal.sawtooth(2 * np.pi * frequency * t, width=width)
        

        # Compare generated values with expected values
        assert generated_values == approx(expected_values)

        





