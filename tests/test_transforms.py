import itertools

import numpy as np

from pashehnet.sensors.transforms import (
    DropoutTransform,
    StuckTransform
)


class TestDropoutTransform:
    def test_prob(self):
        """
        VERY hard to test a probability, but we can test to see if it falls
        within a reasonable statistical range
        """
        xform = DropoutTransform(prob=0.5, value=1)
        dropped_pct = np.mean([xform.transform(x) for x in [0] * 1000])
        assert dropped_pct < 0.6 and dropped_pct > 0.4

    def test_duration(self):
        d = 3
        xform = DropoutTransform(prob=0.1, value=1, duration=d)
        sample = [xform.transform(x) for x in [0] * 100]
        runs = self._runs_of_ones_list(sample)
        assert max(runs) >= d

    def test_duration_range(self):
        """
        VERY hard to test a probabilistic config, but we can test to see if
        it falls within a reasonable range
        """
        d_min = 1
        d_max = 5
        xform = DropoutTransform(
            prob=0.05,
            value=1,
            duration_range=(d_min, d_max)
        )
        sample = [xform.transform(x) for x in [0] * 100]
        runs = self._runs_of_ones_list(sample)
        assert min(runs) >= d_min and max(runs) <= d_max

    @staticmethod
    def _runs_of_ones_list(bits):
        """
        Util method to count up runs of ones in a sample, shamelessly
        borrowed from
        https://stackoverflow.com/a/1066838/773376
        :param bits List of 0/1 values to count run groups of 1s
        :return: List of counts for 1 value run groups in bits
        """
        return [sum(g) for b, g in itertools.groupby(bits) if b]


class TestStuckTransform:
    def test_prob(self):
        """
        VERY hard to test a probability, but we can test to see if it falls
        within a reasonable statistical range
        """
        xform = StuckTransform(prob=0.5, value=1)
        dropped_pct = np.mean([xform.transform(x) for x in [0] * 1000])
        assert dropped_pct < 0.6 and dropped_pct > 0.4

    def test_duration(self):
        d = 3
        xform = StuckTransform(prob=0.1, value=1, duration=d)
        sample = [xform.transform(x) for x in [0] * 100]
        runs = self._runs_of_ones_list(sample)
        assert max(runs) >= d

    def test_duration_range(self):
        """
        VERY hard to test a probabilistic config, but we can test to see if
        it falls within a reasonable range
        """
        d_min = 1
        d_max = 5
        xform = StuckTransform(
            prob=0.05,
            value=1,
            duration_range=(d_min, d_max)
        )
        sample = [xform.transform(x) for x in [0] * 100]
        runs = self._runs_of_ones_list(sample)
        # Check if there are any runs before applying the min and max checks
        assert runs, "No runs of ones found in the sample"

        # Check if the maximum run length is within the expected range
        assert max(runs) <= d_max, f"Max run length {max(runs)} exceeds {d_max}"

        # Check if the minimum run length is within the expected range
        assert min(runs) >= d_min, f"Min run length {min(runs)} is less than {d_min}"

    @staticmethod
    def _runs_of_ones_list(bits):
        """
        Util method to count up runs of ones in a sample, shamelessly
        borrowed from
        https://stackoverflow.com/a/1066838/773376
        :param bits List of 0/1 values to count run groups of 1s
        :return: List of counts for 1 value run groups in bits
        """
        run_lengths = [sum(g) for b, g in itertools.groupby(bits) if b]
        # Ensure the first run starts from the beginning
        if bits[0] == 1:
            run_lengths = [0] + run_lengths
        return run_lengths