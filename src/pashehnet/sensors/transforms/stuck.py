import numpy as np

from .base import SensorTransformBase


class StuckTransform(SensorTransformBase):
    """
    Signal transform that simulates a sensor getting "stuck" on a reading
    (e.g. mechanical sensor jamming), providing the following features:

    - Probability of "stuck" sensor starting (uniform distro)
    - Duration of sensor being "stuck", count (constant or min/max variable
      from uniform distro)
    """
    def __init__(self, prob=0.01, duration=1, duration_range=None,
                 rng=None):
        """
        CTOR for class

        :param prob: Probability of dropout [0.0, 1.0]
        :param value: Value to use when dropout of signal occurs
        :param duration: Sample count in dropout
        :param duration_range: Tuple of min/max dropout counts
        :param rng: NumPy random number generator to use; defaults to \
        numpy.random.default_rng
        """
        self.prob = prob
        self.last_value = None
        self.duration = duration
        self.duration_range = duration_range
        self.rng = rng or np.random.default_rng()
        self.rem_stuck = 0

    def transform(self, value):
        """
        Apply transform, calculating if a stuck sensor is occurring and
        returning appropriate value

        :param value:
        :return:
        """
        if self.rem_stuck <= 0:
            p = self.rng.random()
            if p <= self.prob:
                self.in_dropout = True
                self.start_count = 0
                self.rem_stuck = self.rng.integers(
                    self.duration_range[0], self.duration_range[1] + 1
                ) if self.duration_range else self.duration

        if self.rem_stuck > 0:
            self.rem_stuck -= 1
            return self.last_value
        self.last_value = value
        return value
