from collections import Counter

import numpy as np

from pashehnet.sensors.transforms import StuckTransform


class TestStuckTransform:
    def test_prob(self):
        """
        VERY hard to test a probability, but we can test to see if it falls
        within a reasonable statistical range
        """
        xform = StuckTransform(prob=0.25)
        sample = [xform.transform(v) for v in np.linspace(0, 100, 101)]
        c = Counter()
        for x in sample:
            c[x] += 1
        assert max(c.values()) > 1

    def test_duration(self):
        d = 3
        xform = StuckTransform(prob=0.25, duration=d)
        sample = [xform.transform(v) for v in np.linspace(0, 100, 101)]
        c = Counter()
        for x in sample:
            c[x] += 1
        assert max(c.values()) >= 3

    def test_duration_range(self):
        """
        VERY hard to test a probabilistic config, but we can test to see if
        it falls within a reasonable range
        """
        d_min = 3
        d_max = 5
        xform = StuckTransform(
            prob=0.25,
            duration_range=(d_min, d_max)
        )
        sample = [xform.transform(v) for v in np.linspace(0, 100, 101)]
        c = Counter()
        for x in sample:
            c[x] += 1
        assert max(c.values()) >= d_min
