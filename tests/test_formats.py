from pashehnet.sensors.formats import (
    CSVFormat,
    JSONFormat,
    SimpleFormat,
    StringFormat,
)


class TestCSVFormat:
    """
    Unit tests for CSVFormat class
    """

    def test_headers_false(self):
        """
        Test case where CSV headers are disabled
        """
        fields = {
            'a': 1,
            'b': 2
        }
        fmt = CSVFormat(
            prefix_fields=fields,
            value_field='value',
            headers=False
        )
        assert '1,2,42' == fmt.transform(42)

    def test_headers_true(self):
        """
        Test case where CSV headers are enabled
        """
        fields = {
            'a': 1,
            'b': 2
        }
        fmt = CSVFormat(
            prefix_fields=fields,
            value_field='value',
            headers=True
        )
        assert 'a,b,value\n1,2,42' == fmt.transform(42)


class TestJSONFormat:
    """
    Unit tests for JSONFormat class
    """

    def test_format(self):
        tpl = {'sensor': 1, 'source': 'abc', 'data': {'value': None}}
        pathspec = 'data.value'
        fmt = JSONFormat(tpl, pathspec)

        payload = fmt.transform('a')
        expected = '{"sensor": 1, "source": "abc", "data": {"value": "a"}}'
        assert expected == payload


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
