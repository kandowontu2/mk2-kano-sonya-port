"""Validate runtime-test pose constants against the independently decoded ROM art."""
from pathlib import Path
import re
import unittest

import build_mk2ks_mk3 as b
from audit_leg_victims import stock_phases, stock_gfx, stock_palette, NAMES
from audit_animation_poses import render_group
import upgrade_ksui_previews as ui
from leg_contact_points import adapted_offsets, contact_points, flip_indices, ORIGINAL_KANO_OFFSETS


class LegVictimExpectationTests(unittest.TestCase):
    def test_reference_offsets_match_unmodified_original_records(self):
        workspace = Path(__file__).resolve().parent.parent
        donor = (workspace / "mk3/mk3-maincpu.bin").read_bytes()
        at = b.stock_file(b.u32(donor, b.stock_file(b.KANO_MAIN) + 54 * 4))
        actual = [(-b.signed(b.u16(donor, at+i*12+4)), b.signed(b.u16(donor, at+i*12+6)))
                  for i in range(5)]
        self.assertEqual(actual, ORIGINAL_KANO_OFFSETS)
        self.assertEqual(adapted_offsets("kano"), actual)

    def test_authored_pivots_are_on_actual_stock_body_pixels(self):
        workspace = Path(__file__).resolve().parent.parent
        stock = (workspace / "mk2/mk2-maincpu.bin").read_bytes()
        gfx = stock_gfx(workspace)
        for fighter_id, name in enumerate(NAMES[:12]):
            root = b.u32(stock, b.MK2_MAIN_TABLE + fighter_id*4)
            flip = stock_phases(stock, root, 43, 2)
            groups = [stock_phases(stock, root, 15, 1)[0]] + [flip[i] for i in flip_indices(fighter_id)]
            for pose, (group, point) in enumerate(zip(groups, contact_points(name), strict=True)):
                with self.subTest(fighter=name, pose=pose):
                    frames = b.frame_group(stock, group, b.TMS_ROM_BASE, 0xFFFFFFFF)
                    specs = [ui.component_spec(stock, address) for address in frames]
                    left, top = min(-s[4] for s in specs), min(-s[5] for s in specs)
                    image = render_group(stock, gfx, stock_palette(stock, fighter_id), frames)
                    self.assertGreater(image.getpixel((point[0]-left, point[1]-top))[3], 0)

    def test_stock_offsets_preserve_original_waist_path_on_both_sides(self):
        for name in NAMES[:12]:
            for facing in (1, -1):
                with self.subTest(fighter=name, facing=facing):
                    for (dx, dy), (x, y), (rdx, rdy), (rx, ry) in zip(
                            adapted_offsets(name), contact_points(name), ORIGINAL_KANO_OFFSETS,
                            contact_points("kano"), strict=True):
                        self.assertEqual((facing*(dx-x), dy+y), (facing*(rdx-rx), rdy+ry))
                        self.assertTrue(-128 <= dx <= 128 and -128 <= dy <= 128)

    def test_cpp_and_runtime_expectations_match_authored_contact_data(self):
        workspace = Path(__file__).resolve().parent.parent
        cpp = (workspace / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        lua = (workspace / "mk2ks_selector_exit_test.lua").read_text()
        cpp_block = cpp.split("constexpr int16_t leg_stock_xy[12][5][2] = {", 1)[1].split("\n\t};", 1)[0]
        lua_block = lua.split("local leg_stock_offsets = {", 1)[1].split("\n}\n", 1)[0]
        for label, block in (("C++", cpp_block), ("runtime", lua_block)):
            pairs = [tuple(map(int, values)) for values in re.findall(r"\{(-?\d+),(-?\d+)\}", block)]
            self.assertEqual(len(pairs), 60, label)
            self.assertEqual(pairs, [xy for name in NAMES[:12] for xy in adapted_offsets(name)], label)

    def test_all_runtime_expectations_name_original_composites(self):
        workspace = Path(__file__).resolve().parent.parent
        stock = (workspace / "mk2/mk2-maincpu.bin").read_bytes()
        donor = (workspace / "mk3/mk3-maincpu.bin").read_bytes()
        script = (workspace / "mk2ks_selector_exit_test.lua").read_text()
        block = script.split("local leg_victim_poses = {", 1)[1].split("\n}\n", 1)[0]
        rows = {int(key): [int(value.strip(), 16) for value in values.split(',')]
                for key, values in re.findall(r"\[(\d+)\]=\{([^}]+)\}", block)}
        self.assertEqual(set(rows), {0, 1, 2, 3, 4, 6, 7, 8, 11, 17, 18})
        for fighter_id, actual in rows.items():
            with self.subTest(fighter_id=fighter_id):
                if fighter_id >= 17:
                    root = b.KANO_MAIN if fighter_id == 17 else b.SONYA_MAIN
                    at = b.stock_file(b.u32(donor, b.stock_file(root) + 54 * 4))
                    expected = [b.u32(donor, at + index * 12 + 8) - 0x1000000 for index in range(5)]
                else:
                    root = b.u32(stock, b.MK2_MAIN_TABLE + fighter_id * 4)
                    flip = stock_phases(stock, root, 43, 2)
                    expected = [stock_phases(stock, root, 15, 1)[0]] + [flip[i] for i in flip_indices(fighter_id)]
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
