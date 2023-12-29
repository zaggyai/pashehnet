from pashehnet.sensors.formats import StringFormat


class TestStringFormat:
    """
    Unit tests for StringFormat
    """

    def test_format(self):
        tpl = 'value: {x}'
        fmt = StringFormat(tpl, value_field='x')
        values = [
            1,
            1.1,
            'a'
        ]
        for value in values:
            payload = fmt.transform(value)
            assert payload == tpl.format(x=value)
