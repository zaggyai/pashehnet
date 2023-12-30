import numpy as np
from scipy import signal
from .base import SensorSourceBase


class SquareWaveSource(SensorSourceBase):
    """
    Provides a square wave source using scipy.signal.square
    """
    def __init__(self, frequency, sample_rate, duty_cycle=0.5):
        """
        Construct a new SquareWaveSource object

        :param frequency: Frequency of the square wave in Hz
        :param sample_rate: Sampling rate in Hz
        :param duty_cycle: Duty cycle of the square wave (default is 0.5)
        """
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.duty_cycle = duty_cycle
        self.time = 0

    def __next__(self):
        """
        Implementation for iterator

        :return: Next value from the square wave source
        """
        t = np.linspace(
            self.time,
            self.time + 1/self.sample_rate,
            2,
            endpoint=False
        )
        square_wave = signal.square(
            2 * np.pi * self.frequency * t,
            duty=self.duty_cycle
        )[0]
        self.time += 1/self.sample_rate
        return square_wave
