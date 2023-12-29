import copy
import json

from jsonpath_ng import parse

from .base import SensorFormatBase


class JSONFormat(SensorFormatBase):
    """
    Formatter class that takes a templated JSON-compatible dict + a JSONPath
    selector spec for the value, and returns properly formatted JSON for any
    provided value.
    See also:
    - https://pypi.org/project/jsonpath-ng/
    """
    def __init__(self, tpl, value_path):
        """
        Constructor for class

        :param tpl: Template dict for JSON data
        :param value_path: JSONPath selector for value location
        """
        self.tpl = tpl
        self.value_selector = value_path
        self.jsonpath_expr = parse(value_path)

    def transform(self, value):
        """
        Apply formatter transform to value

        :param value: Value to inject into JSON template
        :return: JSON string
        """
        payload = copy.deepcopy(self.tpl)
        matches = self.jsonpath_expr.find(payload)
        matches[0].full_path.update(payload, value)
        return json.dumps(payload)
