import numpy as np
from scipy import signal
from .base import SensorSourceBase


class SawtoothWaveSource(SensorSourceBase):
    """
    Provides a sawtooth wave source using scipy.signal.sawtooth
    """
    def __init__(self, frequency, sample_rate, width=1.0):
        """
        Construct a new SawtoothWaveSource object

        :param frequency: Frequency of the sawtooth wave in Hz
        :param sample_rate: Sampling rate in Hz
        :param width: Width of the rising ramp as a proportion of the total \
        cycle (default is 1.0)
        """
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.width = width
        self.time = 0

    def __next__(self):
        """
        Implementation for iterator

        :return: Next value from the sawtooth wave source
        """
        t = np.linspace(
            self.time,
            self.time + 1/self.sample_rate,
            2,
            endpoint=False
        )
        sawtooth_wave = signal.sawtooth(
            2 * np.pi * self.frequency * t,
            width=self.width
        )[0]
        self.time += 1/self.sample_rate
        return sawtooth_wave
