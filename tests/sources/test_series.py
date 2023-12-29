from _pytest.python_api import approx

from pashehnet.sensors.sources import SeriesSource


class TestSeriesSource:
    """
    Unit tests for FileSource class
    """
    def test_source(self):
        series = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        src = SeriesSource(series)
        expected = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 0.0]
        sample = [next(src) for _ in range(len(expected))]
        assert expected == approx(sample)
