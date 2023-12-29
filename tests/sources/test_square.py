import numpy as np
from _pytest.python_api import approx
from scipy import signal

from pashehnet.sensors.sources import SquareWaveSource


class TestSquareWaveSource:
    """
    Unit tests for SquareWaveSource class
    """

    def test_source(self):
        """
        Test that expected square wave values are returned in iterative
        requests
        """
        # Test parameters
        frequency, sample_rate, duty_cycle = 5, 500, 0.5

        # Create SquareWaveSource object
        src = SquareWaveSource(frequency, sample_rate, duty_cycle)

        # Generate values from the SquareWaveSource
        generated_values = [next(src) for i in range(sample_rate)]

        # Generate expected values
        t = np.linspace(0, 1, sample_rate, endpoint=False)
        expected_values = signal.square(
            2 * np.pi * frequency * t,
            duty=duty_cycle
        )

        # Compare generated values with expected values
        assert generated_values == approx(expected_values)
