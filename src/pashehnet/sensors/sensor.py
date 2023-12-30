import time


class Sensor(object):
    """
    Wrapper class for source, transform(s) and formatting of sensor
    data, implemented as an iterator. Applies transforms and
    formatter to values provided by source.
    """
    def __init__(self, id, source, format, transforms=[], frequency=1):
        """
        Construct new object

        :param id: the unique ID of this sensor
        :param source: Source object, subclass of SensorSourceBase
        :param format: Format object, subclass of SensorFormatBase
        :param transforms: One or more transforms in order to be called, \
        subclasses of SensorTransformBase
        :param freq: Frequency of signal in Hz
        """
        self.id = id
        self.source = source
        self.format = format
        self.transforms = transforms
        self.frequency = frequency
        self.delay = 1.0 / frequency if \
            (frequency and frequency > 0.0) else \
            None

    def __iter__(self):
        """
        Implementation for iterator

        :return: Self
        """
        return self

    def __next__(self):
        """
        Implementation for iterator

        :return: Next value from sensor stream
        """
        if self.delay:
            time.sleep(self.delay)

        # Get next value from source iterator
        value = next(self.source)

        # Apply all transforms in order provided, if given
        for xform in self.transforms:
            value = xform.transform(value)

        # Format final output
        return self.format.transform(value)
