"""Check the original jump phase semantics, not just the presence of own art."""
from pathlib import Path
import struct
import unittest

import build_mk2ks_mk3 as build


class NativeJumpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = Path(__file__).resolve().parent.parent
        cls.original = (cls.workspace / "mk3/mk3-maincpu.bin").read_bytes()
        cls.mk2 = (cls.workspace / "mk2/mk2-maincpu.bin").read_bytes()

    def test_exact_air_and_landing_order(self):
        for fighter, poses in {
            "kano": (0xFE8282C0, 0xFE828320, 0xFE828380),
            "sonya": (0xFE835BC0, 0xFE835C20, 0xFE835C80),
        }.items():
            first, middle, tucked = poses
            with self.subTest(fighter=fighter):
                self.assertEqual(build.native_vertical_jump(self.original, fighter),
                    (middle, tucked, 0, middle, first, 0))

    def test_reject_changed_phase_layout(self):
        source = bytearray(self.original)
        at = build.stock_file(build.u32(source, build.stock_file(build.KANO_MAIN) + 22 * 4))
        build.put_u32(source, at + 12, 0xFF8282C0)
        with self.assertRaisesRegex(ValueError, "vertical-jump layout"):
            build.native_vertical_jump(source, "kano")

    def test_exported_roots_use_own_script(self):
        output = bytearray(b"\xff" * 0x200000)
        for fighter, block, main, special in (
            ("kano", build.KANO_BLOCK, build.KANO_MAIN, build.KANO_SPECIAL),
            ("sonya", build.SONYA_BLOCK, build.SONYA_MAIN, build.SONYA_SPECIAL),
        ):
            with self.subTest(fighter=fighter):
                report = build.build_hybrid_block(output, self.mk2, self.original, fighter, block, main, special)
                base = build.HYBRID_FILE_BASES[fighter]
                at = (build.u32(output, base + 6 * 4) - build.DONOR_TMS_BASE) // 8
                self.assertGreaterEqual(at, base + report["script_bytes"])
                self.assertLessEqual(at + 24, base + 0x4000)
                self.assertEqual(struct.unpack_from("<6I", output, at), build.native_vertical_jump(self.original, fighter))


if __name__ == "__main__":
    unittest.main()
