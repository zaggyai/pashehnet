from pashehnet.sensors.formats import JSONFormat


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
