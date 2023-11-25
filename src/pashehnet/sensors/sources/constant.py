from .base import SensorSourceBase


class ConstantValueSource(SensorSourceBase):
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return self

    def __next__(self):
        return self.value
