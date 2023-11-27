class Sensor(object):
    """
    Generic wrapper class for source, transform(s) and formatting of sensor
    data
    """

    def __init__(self, source, format, transforms=[]):
        """
        Construct new object
        :param source: Source object, subclass of SensorSourceBase
        :param format: Format object, subclass of SensorFormatBase
        :param transforms: One or more transforms in order to be called,
            subclasses of SensorTransformBase
        """
        self.source = source
        self.format = format
        self.transforms = transforms

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
        # Get next value from source iterator
        value = next(self.source)

        # Apply all transforms in order provided, if given
        for xform in self.transforms:
            value = xform.transform(value)

        # Format final output
        return self.format.transform(value)
