"""Leg-grab conversion tests against typed original ROM animation records."""
from pathlib import Path
import struct
import unittest

import build_mk2ks_mk3 as build


class LegGrabConversionTests(unittest.TestCase):
    def test_negative_x_is_not_an_overlapping_pointer(self):
        source = bytearray(struct.pack("<III", 10, 0x0000FFAB, 0xFF829800))
        count = build.relocate_pointer_words(source, 0, len(source), ((4, 8),))
        self.assertEqual(count, 1)
        self.assertEqual(struct.unpack("<III", source), (10, 0x0000FFAB, 0xFE829800))

    def test_both_signed_coordinates_survive(self):
        source = bytearray(struct.pack("<III", 10, 0xFFD7FFBC, 0xFF82AA60))
        build.relocate_pointer_words(source, 0, len(source), ((4, 8),))
        self.assertEqual(struct.unpack("<III", source), (10, 0xFFD7FFBC, 0xFE82AA60))

    def test_original_kano_and_sonya_pose_records(self):
        original = (Path(__file__).resolve().parent.parent / "mk3/mk3-maincpu.bin").read_bytes()
        for fighter, block in (("kano", build.KANO_BLOCK), ("sonya", build.SONYA_BLOCK)):
            with self.subTest(fighter=fighter):
                protected = build.leg_victim_operands(original, fighter)
                converted = bytearray(original)
                build.relocate_pointer_words(converted, build.stock_file(block[0]),
                    build.stock_file(block[1]), protected)
                for first, last in protected:
                    self.assertEqual(converted[first:last], original[first:last])
                    self.assertEqual(build.u32(converted, first - 4), 10)
                    self.assertEqual(build.u32(converted, last), build.u32(original, last) - 0x01000000)


if __name__ == "__main__":
    unittest.main()
