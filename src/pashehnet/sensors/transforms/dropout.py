import numpy as np

from .base import SensorTransformBase


class DropoutTransform(SensorTransformBase):
    """
    Signal transform that provides the following features:

    - Probability of dropout starting (uniform distro)
    - Value to provide during dropout
    - Duration of dropout, one of
      - Time (constant or min/max variable from uniform distro)
      - Sequence count (constant or min/max variable from uniform distro)
    """
    def __init__(self, prob=0.01, value=0.0, duration=1, duration_range=None,
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
        self.value = value
        self.duration = duration
        self.duration_range = duration_range
        self.rng = rng or np.random.default_rng()
        self.rem_dropout = 0

    def transform(self, value):
        """
        Apply transform, calculating if a dropout is occurring and returning
        appropriate value

        :param value: Value to apply transform to
        :return: Transformed value
        """
        if self.rem_dropout <= 0:
            p = self.rng.random()
            if p <= self.prob:
                self.in_dropout = True
                self.start_count = 0
                self.rem_dropout = self.rng.integers(
                    self.duration_range[0], self.duration_range[1] + 1
                ) if self.duration_range else self.duration

        if self.rem_dropout > 0:
            self.rem_dropout -= 1
            return self.value
        return value
