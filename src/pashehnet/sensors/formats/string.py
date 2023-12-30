from .base import SensorFormatBase


class StringFormat(SensorFormatBase):
    """
    Class providing string formatter based on Python core str.format()
    """
    def __init__(self, tpl, value_field):
        """
        CTOR

        :param tpl: Template string to format
        :param value_field: Field in template to place value
        """
        self.tpl = tpl
        self.value_field = value_field

    def transform(self, value):
        """
        Transform the value into formatted payload

        :param value: Value to transform
        :return: Formatted string payload
        """
        kwargs = {
            self.value_field: value
        }
        return self.tpl.format(**kwargs)
