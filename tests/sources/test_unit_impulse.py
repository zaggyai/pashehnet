from _pytest.python_api import approx

from pashehnet.sensors.sources import UnitImpulseSource


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
