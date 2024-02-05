from queue import SimpleQueue

import numpy as np
from scipy import signal
from .base import SensorSourceBase


class GaussianPulseSource(SensorSourceBase):
    """
    Provides a Gaussian pulse wave source using scipy.signal.gausspulse
    """
    def __init__(self, center_frequency=1000, fractional_bandwidth=0.5,
                 reference_level=-6, cutoff_time=-60, sample_rate=1000):
        """
        Construct a new GaussianPulseSource object

        :param center_frequency: Center frequency of the Gaussian pulse in Hz \
        (default is 1000)
        :param fractional_bandwidth: Fractional bandwidth in frequency domain \
        of pulse (default is 0.5)
        :param reference_level: Reference level at which fractional bandwidth \
        is calculated (dB) (default is -6)
        :param cutoff_time: Cutoff time for when the pulse amplitude falls \
        below the specified level (in dB) (default is -60)
        :param sample_rate: Sampling rate in Hz (default is 1000)
        """
        self.center_frequency = center_frequency
        self.fractional_bandwidth = fractional_bandwidth
        self.reference_level = reference_level
        self.cutoff_time = cutoff_time
        self.sample_rate = sample_rate
        self.sample = None

    def __next__(self):
        """
        Implementation for iterator

        :return: Next value from the Gaussian pulse source
        """
        if not self.sample:
            self._init_sample()
        val = self.sample.get()
        self.sample.put(val)
        return val

    def _init_sample(self):
        # Leverage Python core FIFO queue for infinite cycle sample
        self.sample = SimpleQueue()
        t = np.linspace(0, 1, self.sample_rate, endpoint=False)
        for x in signal.gausspulse(
                t, fc=self.center_frequency, bw=self.fractional_bandwidth,
                bwr=self.reference_level, tpr=self.cutoff_time,
                retenv=False, retquad=False):
            self.sample.put(x)
