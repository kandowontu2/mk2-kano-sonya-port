"""Verify stock-referenced floor anchors without changing any sprite descriptor."""
from pathlib import Path
import re
import struct
import unittest

import build_mk2ks_mk3 as build
import upgrade_ksui_previews as ui

ROOT = Path(__file__).resolve().parent.parent


class NativeGroundAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mk2 = (ROOT / "mk2/mk2-maincpu.bin").read_bytes()
        cls.mk3 = (ROOT / "mk3/mk3-maincpu.bin").read_bytes()

    def test_stock_contact_line_is_below_logical_floor(self):
        root = build.u32(self.mk2, build.MK2_MAIN_TABLE + 4 * 4)
        first = build.u32(self.mk2, build.stock_file(root))
        groups = build.group_references(self.mk2, first, first + 0x1000, root, root + 0x10000)
        anchor = build.u16(self.mk2, build.stock_file(0xFF908010) + 4 * 2)
        self.assertEqual(anchor, 133)
        self.assertGreaterEqual(len(groups), 8)
        for _, _, frames in groups[:8]:
            bottom = max(ui.component_spec(self.mk2, address)[3] -
                         ui.component_spec(self.mk2, address)[5] for address in frames)
            self.assertEqual(bottom - anchor, 5)

    def test_all_imported_stance_frames_share_corrected_contact_line(self):
        for fighter, anchor in (("kano", 134), ("sonya", 135)):
            with self.subTest(fighter=fighter):
                for frames in ui.stance_groups(self.mk3, fighter):
                    bottom = max(ui.component_spec(self.mk3, address)[3] -
                                 ui.component_spec(self.mk3, address)[5] for address in frames)
                    self.assertEqual(bottom - anchor, 5)

    def test_native_constructor_and_landing_use_floor_state(self):
        at = build.stock_file(0xFF907FD0)
        self.assertEqual(struct.unpack_from("<4H", self.mk2, at), (0x4401, 0xB028, 0x00B0, 0x0960))
        at = build.stock_file(0xFF83D2F0)
        self.assertEqual(struct.unpack_from("<4H", self.mk2, at), (0xB9A8, 0x0200, 0x00B0, 0x0960))
        source = (ROOT / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        self.assertRegex(source, re.compile(
            r"extend_parameters\(0xff908010,\s*\{\s*0xff907f70\s*\},\s*134,\s*135\)"))


if __name__ == "__main__":
    unittest.main()
