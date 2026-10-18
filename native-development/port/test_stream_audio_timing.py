import unittest
from mux_stream_native_audio import timing


class StreamAudioTimingTests(unittest.TestCase):
    def rows(self):
        return [dict(frame=str(n), seconds=str(n / 55), width='400', height='254', bytes='406400') for n in range(1, 9)]

    def test_clock_uses_actual_guest_seconds(self):
        result = timing(iter(self.rows()))
        self.assertEqual(result['frames'], 8)
        self.assertAlmostEqual(result['rate'], 55)
        self.assertAlmostEqual(result['duration'], 8/55)

    def test_frame_gap_rejected(self):
        rows = self.rows(); del rows[3]
        with self.assertRaises(AssertionError):
            timing(rows)

    def test_wrong_geometry_or_insufficient_observations_rejected(self):
        rows = self.rows(); rows[3]['bytes'] = '4'
        with self.assertRaises(AssertionError):
            timing(rows)
        with self.assertRaises(AssertionError):
            timing(self.rows()[:1])


if __name__ == '__main__':
    unittest.main()
