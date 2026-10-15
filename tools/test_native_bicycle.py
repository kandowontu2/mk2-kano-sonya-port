"""Original Sonya bicycle phases and the selected donor body/victim records."""
import os
from pathlib import Path
import struct
import unittest

import build_mk2ks_mk3 as build

ROOT = Path(__file__).resolve().parent.parent
INTRO = (0xFF83EA40, 0xFF83EA80, 0xFF83EAE0)
CYCLE = (0xFF83EB40, 0xFF83EB80, 0xFF83EBC0, 0xFF83EC00, 0xFF83EC40,
         0xFF83EC80, 0xFF83EC40, 0xFF83EC00, 0xFF83EBC0, 0xFF83EB80)
VICTIMS = {
    "kano": (0xFF8292C0, (0xFF8294A0, 0xFF829500, 0xFF829560, 0xFF8295A0, 0xFF829620, 0xFF829680)),
    "sonya": (0xFF836680, (0xFF836860, 0xFF8368C0, 0xFF836920, 0xFF836960, 0xFF8369C0, 0xFF836A00)),
}


class BicycleAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = (ROOT / "mk3/mk3-maincpu.bin").read_bytes()

    def test_original_displaced_two_field_startup_records(self):
        self.assertEqual(build.u32(self.original, build.stock_file(build.SONYA_SPECIAL) + 4), 0xFF83E620)
        for index, group in enumerate(INTRO):
            self.assertEqual(struct.unpack_from("<5I", self.original, build.stock_file(0xFF83E620) + index * 20),
                             (6, 0xFF95E870, 4, 0x000A0005, group))
        self.assertEqual(build.u32(self.original, build.stock_file(0xFF83E800)), 0)

    def test_original_cycle_is_ten_poses_with_a_real_loop(self):
        expected = CYCLE + (1, 0xFF83E820, 0) + tuple(reversed(INTRO)) + (0,)
        self.assertEqual(struct.unpack_from("<17I", self.original, build.stock_file(0xFF83E820)), expected)

    def test_original_victim_stumbles_are_independent_six_pose_loops(self):
        for address, groups in VICTIMS.values():
            expected = groups + (0,) + groups + (1, address + 7 * 32)
            self.assertEqual(struct.unpack_from("<15I", self.original, build.stock_file(address)), expected)

    def test_relocation_prioritizes_verified_frame_over_overlapping_null(self):
        converted = bytearray(self.original)
        for fighter, block in (("kano", build.KANO_BLOCK), ("sonya", build.SONYA_BLOCK)):
            build.relocate_pointer_words(converted, *map(build.stock_file, block),
                build.paired_victim_operands(self.original, fighter))
        self.assertEqual(build.u32(converted, build.stock_file(0xFF825EC0)), 0xFEB0FFE0)
        self.assertEqual(build.u32(converted, build.stock_file(0xFF8369A0)), 0)
        self.assertEqual(build.u32(converted, build.stock_file(0xFF8369C0)), 0xFEB1FF90)

    @unittest.skipUnless(os.environ.get("MK2KS_TEST_BICYCLE_PAYLOAD"), "no candidate payload selected")
    def test_all_verified_fighter_frame_fields_relocate_intact(self):
        payload = Path(os.environ["MK2KS_TEST_BICYCLE_PAYLOAD"]).read_bytes()
        count = 0
        for block in (build.KANO_BLOCK, build.SONYA_BLOCK):
            for offset, pointer in build.frame_references(self.original, *block):
                with self.subTest(offset=f"{offset:X}"):
                    self.assertEqual(build.u32(payload, offset), pointer - 0x01000000)
                count += 1
        self.assertGreater(count, 500)

    @unittest.skipUnless(os.environ.get("MK2KS_TEST_BICYCLE_PAYLOAD"), "no candidate payload selected")
    def test_selected_payload_preserves_body_composite_members(self):
        payload = Path(os.environ["MK2KS_TEST_BICYCLE_PAYLOAD"]).read_bytes()
        groups = set(INTRO + CYCLE)
        for _, victim_groups in VICTIMS.values():
            groups.update(victim_groups)
        for group in groups:
            base = build.stock_file(group)
            for part in range(8):
                original = build.u32(self.original, base + part * 4)
                with self.subTest(group=f"{group:08X}", part=part):
                    self.assertEqual(build.u32(payload, base + part * 4), original - 0x01000000 if original else 0)
                if not original:
                    break
            else:
                self.fail(f"Unterminated original composite {group:08X}")

    @unittest.skipUnless(os.environ.get("MK2KS_TEST_BICYCLE_PAYLOAD"), "no candidate payload selected")
    def test_selected_payload_preserves_actual_victim_loops(self):
        payload = Path(os.environ["MK2KS_TEST_BICYCLE_PAYLOAD"]).read_bytes()
        for address, groups in VICTIMS.values():
            expected = tuple(value - 0x01000000 for value in groups)
            expected = expected + (0,) + expected + (1, address + 7 * 32 - 0x01000000)
            self.assertEqual(struct.unpack_from("<15I", payload, build.stock_file(address)), expected)


if __name__ == "__main__":
    unittest.main()
