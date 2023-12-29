from _pytest.python_api import approx

from pashehnet.sensors.sources import FileSource


class TestFileSource:
    """
    Unit tests for FileSource class
    """
    def test_local(self):
        uri = 'tests/sources/file_source.txt'
        src = FileSource(uri)
        expected = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 0.0]
        sample = [next(src) for _ in range(len(expected))]
        assert expected == approx(sample)

    def test_remote(self):
        uri = 'https://gist.githubusercontent.com/arpieb/2e0d262e4099f3c28f4befdfe0958a15/raw/e35f12955d1328998a226c550cf9a51867ce5197/gistfile1.txt'  # noqa E501
        src = FileSource(uri)
        expected = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 0.0]
        sample = [next(src) for _ in range(len(expected))]
        assert expected == approx(sample)
