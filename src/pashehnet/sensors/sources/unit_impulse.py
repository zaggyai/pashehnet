from queue import SimpleQueue

import numpy as np
from scipy.signal import unit_impulse

from .base import SensorSourceBase


class UnitImpulseSource(SensorSourceBase):
    """
    Unit impulse signal (discrete delta function) or unit basis vector.
    See:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.unit_impulse.html
    """

    def __init__(self, shape, idx=None, dtype=np.float64):
        self.shape = shape
        self.idx = idx
        self.dtype = dtype

        # Leverage Python core FIFO queue for infinite cycle sample
        self.sample = SimpleQueue()
        for x in unit_impulse(self.shape, self.idx, self.dtype):
            self.sample.put(x)

    def __next__(self):
        """
        Implementation for iterator
        :return: Next value from source
        """
        val = self.sample.get()
        self.sample.put(val)
        return val
