import numpy as np
from _pytest.python_api import approx
from scipy import signal

from pashehnet.sensors.sources import GaussianPulseSource


class TestGaussianPulseSource:
    """
    Unit tests for GaussianPulseSource class
    """

    def test_source(self):
        """
        Test that expected Gaussian pulse values are returned in iterative
        requests
        """
        # Test parameters
        center_frequency, fractional_bandwidth, reference_level = 1000, 0.5, -6
        cutoff_time, sample_rate = -60, 1000

        # Create GaussianPulseSource object
        src = GaussianPulseSource(
            center_frequency, fractional_bandwidth, reference_level,
            cutoff_time, sample_rate)

        # Generate values from the GaussianPulseSource
        generated_values = [next(src) for _ in range(sample_rate)]

        # Generate expected values
        t = np.linspace(0, 1, sample_rate, endpoint=False)
        expected_values = signal.gausspulse(
            t, fc=center_frequency, bw=fractional_bandwidth,
            bwr=reference_level, tpr=cutoff_time,
            retenv=False, retquad=False)

        # Compare generated values with expected values
        assert generated_values == approx(expected_values)
