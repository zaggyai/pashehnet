from queue import SimpleQueue

from scipy.signal import chirp

from .base import SensorSourceBase


class ChirpSource(SensorSourceBase):
    """
    Frequency-swept cosine generator.
    See:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.chirp.html
    """
    def __init__(self, t, f0, t1, f1, method='linear', phi=0,
                 vertex_zero=True):
        """
        CTOR

        :param t: array_like; Times at which to evaluate the waveform
        :param f0: float; Frequency (e.g. Hz) at time t=0
        :param t1: float; Time at which f1 is specified
        :param f1: float; Frequency (e.g. Hz) of the waveform at time t1
        :param method: {‘linear’, ‘quadratic’, ‘logarithmic’, ‘hyperbolic’}, \
        optional.  Kind of frequency sweep. If not given, linear is \
        assumed. See scipy.signal.chirp notes for more details.
        :param phi: float, optional; Phase offset, in degrees. Default is 0
        :param vertex_zero: bool, optional; This parameter is only used when \
        method is ‘quadratic’. It determines whether the vertex of the \
        parabola that is the graph of the frequency is at t=0 or t=t1
        """
        self.t = t
        self.f0 = f0
        self.t1 = t1
        self.f1 = f1
        self.method = method
        self.phi = phi
        self.vertex_zero = vertex_zero
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
        for x in chirp(
                self.t,
                self.f0,
                self.t1,
                self.f1,
                self.method,
                self.phi,
                self.vertex_zero
        ):
            self.sample.put(x)
