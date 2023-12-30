from queue import SimpleQueue

from scipy.signal import sweep_poly

from .base import SensorSourceBase


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
        for x in sweep_poly(
                self.t,
                self.poly,
                self.phi
        ):
            self.sample.put(x)
