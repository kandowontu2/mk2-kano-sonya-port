"""Bind bicycle feedback timing and shared MKII primitives to original ROM data."""
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parent.parent


class BicycleFeedbackReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mk2 = (ROOT / "mk2/mk2-maincpu.bin").read_bytes()
        cls.mk3 = (ROOT / "mk3/mk3-maincpu.bin").read_bytes()

    def words(self, data, address, count):
        return struct.unpack_from(f"<{count}H", data, (address - 0xFF800000) // 8)

    def test_original_paired_impact_countdown_and_seven_field_reset(self):
        self.assertEqual(self.words(self.mk3, 0xFF9E6080, 10),
                         (0xB5A0, 0x0250, 0x1420, 0xCB04, 0x0D5F, 0x6680, 0xFFAA, 0x18E0, 0xB00D, 0x0250))
        self.assertEqual(self.words(self.mk3, 0xFF9E5750, 3), (0x1820, 0xB00D, 0x0250))

    def test_original_camera_recipe_is_explicitly_cancelled_at_release(self):
        self.assertEqual(self.words(self.mk3, 0xFF9E54F0, 6), (0x09EB, 0x0030, 0x0003, 0x0D5F, 0x2A20, 0xFFAA))
        self.assertEqual(self.words(self.mk3, 0xFF9E5B40, 5), (0x09C0, 0x0103, 0x0D5F, 0xFE70, 0xFF95))
        self.assertEqual(self.words(self.mk3, 0xFFAA2BB0, 5), (0x0D5F, 0x6960, 0xFF92, 0x03AB, 0x3DCA))

    def test_native_mkii_primitive_uses_two_shared_impact_records(self):
        self.assertEqual(self.words(self.mk2, 0xFFA11EA0, 4), (0x09E0, 0x0014, 0x0002, 0xC02A))
        self.assertEqual(self.words(self.mk2, 0xFFA0EF20 + 0x14 * 32, 4), (0x4010, 0x0073, 0x4012, 0x0076))
        # Normal MKII hard-hit reactions invoke this same unvoiced primitive.
        self.assertEqual(self.words(self.mk2, 0xFF8E1AB0, 3), (0x0D5F, 0x1EA0, 0xFFA1))

    def test_native_mkii_camera_task_has_matching_id_and_cadence(self):
        self.assertEqual(self.words(self.mk2, 0xFF9E12E0, 8), (0x09C0, 0x0103, 0x09E7, 0x1390, 0xFF9E, 0x0D5F, 0x0070, 0xFF84))
        self.assertEqual(self.words(self.mk2, 0xFF9E1400, 7), (0x09C0, 0x0003, 0x0D5F, 0xDCC0, 0xFF80, 0x03AB, 0x3DCA))


if __name__ == "__main__":
    unittest.main()
