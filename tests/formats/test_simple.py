from pashehnet.sensors.formats import SimpleFormat


class TestSimpleFormat:
    """
    Unit tests for SimpleFormat class
    """

    def test_format(self):
        fmt = SimpleFormat()
        values = [
            1,
            1.1,
            'a'
        ]
        for value in values:
            payload = fmt.transform(value)
            assert payload == str(value)
