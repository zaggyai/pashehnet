import numpy as np
from pytest import approx
from scipy import signal

from pashehnet.sensors.sources import (
    ConstantValueSource,
    SweepPolySource,
    UnitImpulseSource, 
    ChirpSource,
    SquareWaveSource,
    SawtoothWaveSource,
    GaussianPulseSource
)


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
        

class TestSweepPolySource:
    """
    Unit tests for SweepPolySource
    """

    def test_source(self):
        """
        Test that expected values are returned AND they are repeating cycles
        :return:
        """
        expected = [
            1.0,
            -0.9975027964162702,
            -0.6374239897486864,
            0.7754957431722314,
            0.8763066800438636
        ]
        p = np.poly1d([0.025, -0.36, 1.25, 2.0])
        t = np.linspace(0, 4, 5)
        src = SweepPolySource(t, p)
        cycle1 = [next(src) for _ in range(5)]
        assert cycle1 == approx(expected)

        cycle2 = [next(src) for _ in range(5)]
        assert cycle1 == cycle2


class TestUnitImpulseSource:
    """
    Unit tests for UnitImpulseSource class
    """

    def test_defaults(self):
        expected = [
            1.0, 0.0, 0.0,
        ]
        shape = len(expected)
        src = UnitImpulseSource(shape)
        cycle1 = [next(src) for _ in range(shape)]
        assert cycle1 == approx(expected)

        cycle2 = [next(src) for _ in range(shape)]
        assert cycle1 == cycle2

    def test_idx(self):
        expected = [
            0.0, 1.0, 0.0,
        ]
        idx = 1
        shape = len(expected)
        src = UnitImpulseSource(shape, idx)
        cycle1 = [next(src) for _ in range(shape)]
        assert cycle1 == approx(expected)

        cycle2 = [next(src) for _ in range(shape)]
        assert cycle1 == cycle2

    def test_mid(self):
        expected = [
            0.0, 0.0, 1.0, 0.0, 0.0,
        ]
        idx = 'mid'
        shape = len(expected)
        src = UnitImpulseSource(shape, idx)
        cycle1 = [next(src) for _ in range(shape)]
        assert cycle1 == approx(expected)

        cycle2 = [next(src) for _ in range(shape)]
        assert cycle1 == cycle2


class TestChirpSource:
    """
    Unit tests for ConstantValueSource class
    """

    def test_linear(self):
        self._test_method('linear')

    def test_quadratic(self):
        self._test_method('quadratic')

    def test_logarithmic(self):
        self._test_method('logarithmic')

    def test_hyperbolic(self):
        self._test_method('hyperbolic')

    def _test_method(self, method):
        """
        Util method to wrap common test harness for different methods
        """
        t = np.linspace(0, 10, 1500)
        w = signal.chirp(t, f0=6, f1=1, t1=5, method=method)

        src = ChirpSource(t, f0=6, f1=1, t1=5, method=method)
        sample = [next(src) for _ in range(len(t))]

        assert all(sample == w), f'{method} did not match with scipy'

    def test_phi(self):
        phi = 90
        t = np.linspace(0, 10, 1500)
        w = signal.chirp(t, f0=6, f1=1, t1=5, method='linear', phi=phi)

        src = ChirpSource(t, f0=6, f1=1, t1=5, method='linear', phi=phi)
        sample = [next(src) for _ in range(len(t))]

        assert all(sample == w)

    def test_vertex_zero(self):
        t = np.linspace(0, 10, 1500)
        w = signal.chirp(t, f0=6, f1=1, t1=5, method='quadratic', vertex_zero=False)

        src = ChirpSource(t, f0=6, f1=1, t1=5, method='quadratic', vertex_zero=False)
        sample = [next(src) for _ in range(len(t))]

        assert all(sample == w)


class TestGaussianPulseSource:
    """
    Unit tests for GaussianPulseSource class
    """

    def test_source(self):
        """
        Test that expected Gaussian pulse values are returned in iterative requests
        """
        # Test parameters
        center_frequency, fractional_bandwidth, reference_level = 1000, 0.5, -6
        cutoff_time, sample_rate, ret_quad, ret_env = -60, 1000, False, False

        # Create GaussianPulseSource object
        src = GaussianPulseSource(center_frequency, fractional_bandwidth, reference_level,
                                  cutoff_time, sample_rate, ret_quad, ret_env)

        # Generate values from the GaussianPulseSource
        generated_values = [next(src) for _ in range(sample_rate)]

        # Generate expected values
        t = np.linspace(0, 1, sample_rate, endpoint=False)
        expected_values = signal.gausspulse(t, fc=center_frequency, bw=fractional_bandwidth,
                                            bwr=reference_level, tpr=cutoff_time,
                                            retquad=ret_quad, retenv=ret_env)[0]

        # Compare generated values with expected values
        assert generated_values == approx(expected_values)
