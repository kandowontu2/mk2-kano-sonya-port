"""Independent small codec regression checks; not gameplay qualification."""
import unittest
from build_inflation_assets import pack6, unpack6


class InflationCodecTests(unittest.TestCase):
    def test_known_bit_order(self):
        self.assertEqual(pack6([1, 2, 3, 4]), bytes.fromhex('813010'))

    def test_all_indices_and_tail_lengths(self):
        for count in range(1, 260):
            values = [i % 64 for i in range(count)]
            self.assertEqual(unpack6(pack6(values), count), values)
            self.assertEqual(len(pack6(values)), (count*6+7)//8)

    def test_invalid_index_rejected(self):
        for value in (-1, 64):
            with self.assertRaises(AssertionError):
                pack6([value])


if __name__ == '__main__':
    unittest.main()
