from .base import SensorFormatBase


class CSVFormat(SensorFormatBase):
    """
    CSV formatter class for sensor data.  Given a value, format into CSV based
    on the provided template specs.
    """
    def __init__(self, prefix_fields=None, value_field='value', headers=True):
        """
        CTOR for class

        :param prefix_fields: Dict of prefix fields+values to include \
        in CSV output
        :param value_field: Name of field where the value will be emitted
        :param headers: Toggle whether headers are generated during formatting
        """
        self.prefix_fields = prefix_fields or {}
        self.value_field = value_field
        self.headers = headers

    def transform(self, value):
        """
        Apply the CSV formatting to the given value

        :param value: Value to transform.
        :return: CSV formatted string
        """
        lines = []
        keys = self.prefix_fields.keys()
        values = self.prefix_fields.values()
        if self.headers:
            lines.append(','.join(keys) + ',' + self.value_field)
        lines.append(','.join([str(x) for x in values]) + ',' + str(value))
        return "\n".join(lines)
