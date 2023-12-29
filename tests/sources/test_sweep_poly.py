import numpy as np
from _pytest.python_api import approx

from pashehnet.sensors.sources import SweepPolySource


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
