from queue import SimpleQueue

import numpy as np
from scipy.signal import unit_impulse

from .base import SensorSourceBase


class UnitImpulseSource(SensorSourceBase):
    """
    Unit impulse signal (discrete delta function) or unit basis vector.
    See:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.unit_impulse.html

    :param shape: int or tuple of int. Number of samples in the output (1-D), \
    or a tuple that represents the shape of the output (N-D).
    :param idx: None or int or tuple of int or ‘mid’, optional. Index at \
    which the value is 1. If None, defaults to the 0th element. If idx='mid', \
    the impulse will be centered at shape // 2 in all dimensions. If an int, \
    the impulse will be at idx in all dimensions.
    :param dtype: data-type, optional. The desired data-type for the array, \
    e.g., numpy.int8. Default is numpy.float64.
    """
    def __init__(self, shape, idx=None, dtype=np.float64):
        self.shape = shape
        self.idx = idx
        self.dtype = dtype
        self.sample = None

    def __next__(self):
        """
        Implementation for iterator

        :return: Next value from source
        """
        if not self.sample:
            self._init_sample()
        val = self.sample.get()
        self.sample.put(val)
        return val

    def _init_sample(self):
        # Leverage Python core FIFO queue for infinite cycle sample
        self.sample = SimpleQueue()
        for x in unit_impulse(self.shape, self.idx, self.dtype):
            self.sample.put(x)
