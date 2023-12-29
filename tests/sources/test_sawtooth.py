import numpy as np
from _pytest.python_api import approx
from scipy import signal

from pashehnet.sensors.sources import SawtoothWaveSource


class TestSawtoothWaveSource:
    """
    Unit tests for SawtoothWaveSource class
    """

    def test_source(self):
        """
        Test that expected square wave values are returned in iterative
        requests
        """
        # Test parameters
        frequency, sample_rate, width = 5, 10, 0.5

        # Create SawtoothWaveSource object
        src = SawtoothWaveSource(frequency, sample_rate, width)

        # Generate values from the SquareWaveSource
        generated_values = [next(src) for i in range(sample_rate)]

        # Generate expected values
        t = np.linspace(0, 1, sample_rate, endpoint=False)
        expected_values = signal.sawtooth(
            2 * np.pi * frequency * t,
            width=width
        )

        # Compare generated values with expected values
        assert generated_values == approx(expected_values)
