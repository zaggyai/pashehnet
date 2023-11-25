from .base import SensorTypeBase


class CSVType(SensorTypeBase):
    def __init__(self, prefix_fields, value_field, headers=True):
        self.prefix_fields = prefix_fields
        self.value_field = value_field
        self.headers = headers

    def format_value(self, value):
        lines = []
        keys = self.prefix_fields.keys()
        values = self.prefix_fields.values()
        if self.headers:
            lines.append(','.join(keys) + ',' + self.value_field)
        lines.append(','.join([str(x) for x in values]) + ',' + str(value))
        return "\n".join(lines)