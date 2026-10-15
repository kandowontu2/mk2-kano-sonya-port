"""Audit authored grip pivots against original pixels and native pose tables."""
from pathlib import Path
import re
import unittest

import build_mk2ks_mk3 as b
from audit_animation_poses import render_group
from audit_leg_victims import stock_gfx, stock_palette, stock_phases, NAMES
import upgrade_ksui_previews as ui


ROOT = Path(__file__).resolve().parent.parent


class ChokeContactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stock = (ROOT / "mk2/mk2-maincpu.bin").read_bytes()
        cls.donor = (ROOT / "mk3/mk3-maincpu.bin").read_bytes()
        cls.cpp = (ROOT / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        cls.lua = (ROOT / "mk2ks_choke_test.lua").read_text()
        block = cls.cpp.split("constexpr int16_t choke_stock_grip[12][2]={", 1)[1].split("};", 1)[0]
        cls.points = [tuple(map(int, xy)) for xy in re.findall(r"\{(-?\d+),(-?\d+)\}", block)]

    def test_actual_stock_pose_tables_match_runtime_expectations(self):
        block = self.lua.split("local stock_groups={", 1)[1].split("}", 1)[0]
        expected = [int(value.strip(), 16) for value in block.split(",")]
        self.assertEqual(len(expected), 12)
        for fighter in range(12):
            root = b.u32(self.stock, b.MK2_MAIN_TABLE + fighter * 4)
            self.assertEqual(stock_phases(self.stock, root, 16, 1)[1], expected[fighter])

    def test_pivots_are_on_original_body_pixels(self):
        gfx = stock_gfx(ROOT)
        self.assertEqual(len(self.points), 12)
        for fighter, point in enumerate(self.points):
            with self.subTest(fighter=NAMES[fighter]):
                root = b.u32(self.stock, b.MK2_MAIN_TABLE + fighter * 4)
                group = stock_phases(self.stock, root, 16, 1)[1]
                frames = b.frame_group(self.stock, group, b.TMS_ROM_BASE, 0xFFFFFFFF)
                specs = [ui.component_spec(self.stock, address) for address in frames]
                left, top = min(-s[4] for s in specs), min(-s[5] for s in specs)
                picture = render_group(self.stock, gfx, stock_palette(self.stock, fighter), frames)
                self.assertGreater(picture.getpixel((point[0]-left, point[1]-top))[3], 0)

    def test_authored_translation_preserves_original_grip_path_both_sides(self):
        operands = b.choke_victim_operands(self.donor, "sonya")
        for point in self.points:
            for first, _ in operands:
                dx, dy = -b.signed(b.u16(self.donor, first)), b.signed(b.u16(self.donor, first + 2))
                adapted = (dx + 8 + point[0], dy + 54 - point[1])
                for facing in (1, -1):
                    self.assertEqual((facing * (adapted[0] - point[0]), adapted[1] + point[1]),
                        (facing * (dx + 8), dy + 54))

    def test_runtime_uses_same_authored_pivots(self):
        block = self.lua.split("local stock_grip={", 1)[1].split("\nlocal function", 1)[0]
        expected = [tuple(map(int, xy)) for xy in re.findall(r"\{(-?\d+),(-?\d+)\}", block)]
        self.assertEqual(self.points, expected)


if __name__ == "__main__":
    unittest.main()
