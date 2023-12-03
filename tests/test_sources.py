import numpy as np
from pytest import approx

from pashehnet.sensors.sources import ConstantValueSource, SweepPolySource


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
