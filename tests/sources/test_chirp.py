import numpy as np
from scipy import signal

from pashehnet.sensors.sources import ChirpSource


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
        w = signal.chirp(
            t,
            f0=6,
            f1=1,
            t1=5,
            method='quadratic',
            vertex_zero=False
        )

        src = ChirpSource(
            t,
            f0=6,
            f1=1,
            t1=5,
            method='quadratic',
            vertex_zero=False
        )
        sample = [next(src) for _ in range(len(t))]

        assert all(sample == w)
