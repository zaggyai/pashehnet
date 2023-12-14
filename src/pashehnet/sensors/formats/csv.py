from .base import SensorFormatBase


class CSVFormat(SensorFormatBase):
    def __init__(self, prefix_fields=None, value_field='value', headers=True):
        self.prefix_fields = prefix_fields or {}
        self.value_field = value_field
        self.headers = headers

    def transform(self, value):
        lines = []
        keys = self.prefix_fields.keys()
        values = self.prefix_fields.values()
        if self.headers:
            lines.append(','.join(keys) + ',' + self.value_field)
        lines.append(','.join([str(x) for x in values]) + ',' + str(value))
        return "\n".join(lines)
