from queue import SimpleQueue

from .base import SensorSourceBase
from scipy.signal import sweep_poly


class SweepPolySource(SensorSourceBase):
    """
    Frequency-swept cosine generator, with a time-dependent frequency.
    See:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sweep_poly.html
    """
    def __init__(self, t, poly, phi=0):
        """
        Construct new object
        :param t: ndarray; times at which to evaluate the waveform
        :param poly: 1-D array_like or instance of numpy.poly1d
        :param phi: float, optional;  Phase offset, in degrees, Default: 0
        """
        self.t = t
        self.poly = poly
        self.phi = phi

        # Leverage Python core FIFO queue for infinite cycle sample
        self.sample = SimpleQueue()
        for x in sweep_poly(t, poly, phi):
            self.sample.put(x)

    def __iter__(self):
        """
        Implementation for iterator
        :return: Self
        """
        return self

    def __next__(self):
        """
        Implementation for iterator
        :return: Next value from source
        """
        val = self.sample.get()
        self.sample.put(val)
        return val
