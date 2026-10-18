import unittest
import numpy as np
from inspect_showcase_audio_alignment import alignment, RATE


class ShowcaseAlignmentTests(unittest.TestCase):
    def test_finds_known_delay_and_ignores_gain_and_dc(self):
        signal = np.random.default_rng(7).normal(size=8000)
        observed = np.r_[np.zeros(1700), signal * .7 + .1, np.zeros(1500)]
        result = alignment(signal, observed, .2)
        self.assertAlmostEqual(result['offsetSeconds'], 100 / RATE)
        self.assertAlmostEqual(result['correlation'], 1)

    def test_silence_cannot_pass(self):
        with self.assertRaises(AssertionError):
            alignment(np.zeros(8000), np.zeros(11200), .2)


if __name__ == '__main__':
    unittest.main()
