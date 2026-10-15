"""Typed choke data: original MK3 2.1 operands, not inferred pointer patterns."""
import os
from pathlib import Path
import struct
import unittest

import build_mk2ks_mk3 as build


ROOT = Path(__file__).resolve().parent.parent
# Independently read from original main 56 (three lift + four squeeze poses).
ORIGINAL = {
    "kano": (0xFF82DF60, (
        0xFFF8FFB1, 0xFFE1FFC8, 0xFFE4FFE5,
        0xFFE6FFE3, 0xFFD5FFCD, 0xFFD3FFBC, 0xFFD5FFCD,
    ), (0xFF829500,) * 6 + (0xFF8294A0,)),
    "sonya": (0xFF83AAE0, (
        0xFFEDFFB3, 0xFFD5FFCC, 0xFFDCFFE6,
        0xFFDCFFE3, 0xFFCEFFCA, 0xFFCEFFC0, 0xFFCEFFCA,
    ), (0xFF836860,) * 7),
}
OFFSETS = (0, 12, 24, 40, 52, 64, 76)


class ChokeConversionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = (ROOT / "mk3/mk3-maincpu.bin").read_bytes()

    def test_original_two_phase_layout(self):
        for fighter, (address, coordinates, groups) in ORIGINAL.items():
            with self.subTest(fighter=fighter):
                base = build.stock_file(address)
                self.assertEqual(build.choke_victim_operands(self.original, fighter),
                    tuple((base + at + 4, base + at + 8) for at in OFFSETS))
                self.assertEqual(build.u32(self.original, base + 36), 0)
                self.assertEqual(build.u32(self.original, base + 88), 0)
                for at, xy, group in zip(OFFSETS, coordinates, groups):
                    self.assertEqual(struct.unpack_from("<III", self.original, base + at),
                        (10, xy, group))

    def test_full_fighter_relocation_preserves_all_paired_operands(self):
        for fighter, block in (("kano", build.KANO_BLOCK), ("sonya", build.SONYA_BLOCK)):
            converted = bytearray(self.original)
            protected = build.paired_victim_operands(self.original, fighter)
            self.assertEqual(len(protected), 12)
            build.relocate_pointer_words(converted, *map(build.stock_file, block), protected)
            for first, last in protected:
                with self.subTest(fighter=fighter, offset=first):
                    self.assertEqual(converted[first:last], self.original[first:last])
                    self.assertEqual(build.u32(converted, first - 4), 10)
                    self.assertEqual(build.u32(converted, last),
                        build.u32(self.original, last) - 0x01000000)

    def test_both_phase_terminators_are_required(self):
        for at in (36, 88):
            with self.subTest(terminator=at):
                invalid = bytearray(self.original)
                build.put_u32(invalid, build.stock_file(ORIGINAL["kano"][0]) + at, 10)
                with self.assertRaisesRegex(ValueError, "terminator"):
                    build.choke_victim_operands(invalid, "kano")

    def test_every_record_is_typed(self):
        for at in OFFSETS:
            with self.subTest(record=at):
                invalid = bytearray(self.original)
                build.put_u32(invalid, build.stock_file(ORIGINAL["sonya"][0]) + at, 6)
                with self.assertRaisesRegex(ValueError, "record"):
                    build.choke_victim_operands(invalid, "sonya")

    def test_unknown_fighter_is_not_silently_sonya(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            build.paired_victim_operands(self.original, "reptile")

    @unittest.skipUnless(os.environ.get("MK2KS_TEST_CHOKE_PAYLOAD"), "no candidate payload selected")
    def test_selected_built_payload_preserves_original_records(self):
        payload = Path(os.environ["MK2KS_TEST_CHOKE_PAYLOAD"]).read_bytes()
        for fighter, (address, coordinates, groups) in ORIGINAL.items():
            base = build.stock_file(address)
            for at, xy, group in zip(OFFSETS, coordinates, groups):
                with self.subTest(fighter=fighter, pose=at):
                    self.assertEqual(struct.unpack_from("<III", payload, base + at),
                        (10, xy, group - 0x01000000))
            self.assertEqual(build.u32(payload, base + 36), 0)
            self.assertEqual(build.u32(payload, base + 88), 0)


if __name__ == "__main__":
    unittest.main()
