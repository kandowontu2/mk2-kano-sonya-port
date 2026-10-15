"""Regression checks for original fatality art relocation, not activation."""
import unittest
import re
import struct
from pathlib import Path

import build_mk2ks_mk3 as animation
import build_native_fatality_art as fatality
from audit_stock_extraction_poses import NAMES as STOCK_NAMES


class FatalityArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.original = (root / "mk3/mk3-maincpu.bin").read_bytes()
        cls.base = (root / "diagnostic_v46_bicycle_assets/roms/mk2ks/mk2ks.mdata").read_bytes()

    def test_all_observed_groups_and_frames_are_relocated(self):
        payload = bytearray(self.base)
        report = fatality.build(payload, self.original)
        self.assertEqual((report["groups"], report["unique_frames"]), (73, 126))
        self.assertEqual((report["groups_changed"], report["frames_changed"]), (95, 83))
        self.assertEqual(report["palette_pointers_changed"], 4)
        for group in (*fatality.KANO_GROUPS, *fatality.KANO_SKELETON_GROUPS,
                      *fatality.KANO_SONYA_VICTIM_GROUPS,
                      *fatality.KANO_JAX_VICTIM_GROUPS,
                      *fatality.KANO_DIZZY_GROUPS, *fatality.SONYA_GROUPS,
                      *fatality.SONYA_DIZZY_GROUPS,
                      *fatality.SONYA_BURN_GROUPS):
            frames = animation.frame_group(self.original, group, group, group + 0x200)
            self.assertTrue(frames)
            offset = animation.stock_file(group)
            for index, frame in enumerate(frames):
                self.assertEqual(animation.u32(payload, offset + index * 4),
                                 animation.relocate_pointer(frame))
                frame_offset = animation.stock_file(frame)
                self.assertEqual(animation.u32(payload, frame_offset + 8),
                                 animation.u32(self.original, frame_offset + 8) +
                                 animation.GFX_REBASE)

    def test_change_scope_and_idempotence(self):
        payload = bytearray(self.base)
        allowed = set()
        frames = set()
        for group in (*fatality.KANO_GROUPS, *fatality.KANO_SKELETON_GROUPS,
                      *fatality.KANO_SONYA_VICTIM_GROUPS,
                      *fatality.KANO_JAX_VICTIM_GROUPS,
                      *fatality.KANO_DIZZY_GROUPS, *fatality.SONYA_DIZZY_GROUPS,
                      *fatality.SONYA_BURN_GROUPS):
            components = animation.frame_group(self.original, group, group, group + 0x200)
            frames.update(components)
            start = animation.stock_file(group)
            for index in range(len(components)):
                allowed.update(range(start + index * 4, start + index * 4 + 4))
        for frame in frames:
            start = animation.stock_file(frame) + 8
            allowed.update(range(start, start + 4))
            tail = animation.u32(self.original, animation.stock_file(frame) + 14)
            if animation.TMS_ROM_BASE <= tail <= 0xFFFFFFFF and not tail & 0x0F:
                start = animation.stock_file(frame) + 14
                allowed.update(range(start, start + 4))
        fatality.build(payload, self.original)
        changed = {index for index, (before, after) in
                   enumerate(zip(self.base, payload)) if before != after}
        self.assertTrue(changed)
        self.assertLessEqual(changed, allowed)
        snapshot = bytes(payload)
        second = fatality.build(payload, self.original)
        self.assertEqual(bytes(payload), snapshot)
        self.assertEqual((second["groups_changed"], second["frames_changed"],
                          second["palette_pointers_changed"]), (0, 0, 0))

    def test_character_owned_dizzy_rows_match_original_programs(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        body = source.split("constexpr uint32_t victim_dizzy_groups[19][7]={", 1)[1].split("};", 1)[0]
        actual = [[int(value, 16) for value in re.findall(r"0x[0-9a-f]+", row)]
                  for row in re.findall(r"\{([^{}]+)\}", body)]
        self.assertEqual((len(actual), {len(row) for row in actual}), (19, {7}))

        mk2 = (root / "mk2/mk2-maincpu.bin").read_bytes()
        stock_main = [animation.u32(mk2, animation.MK2_MAIN_TABLE + i * 4)
                      for i in range(17)]
        stock_special = [animation.u32(mk2, animation.MK2_SPECIAL_TABLE + i * 4)
                         for i in range(17)]
        for fighter, main in enumerate(stock_main):
            end = min((address for address in stock_main if address > main),
                      default=0xffe00000)
            spans = animation.sequence_spans(mk2, main, (main, end),
                                             (main, stock_special[fighter]))
            index = 40 if 40 in spans else 0
            groups = [address for _, address, _ in animation.group_references(
                mk2, *spans[index], main, end)][:7]
            self.assertEqual(actual[fighter], groups, f"MKII fighter {fighter}")

        for fighter, main, special, block in (
            (17, animation.KANO_MAIN, animation.KANO_SPECIAL, animation.KANO_BLOCK),
            (18, animation.SONYA_MAIN, animation.SONYA_SPECIAL, animation.SONYA_BLOCK),
        ):
            spans = animation.sequence_spans(self.original, main, block,
                                             (main, special))
            groups = [animation.relocate_pointer(address)
                      for _, address, _ in animation.group_references(
                          self.original, *spans[37], *block)][:7]
            self.assertEqual(actual[fighter], groups, f"MK3 fighter {fighter}")

    def test_sonya_extraction_sequence_matches_original_trace(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        body = source.split("constexpr uint32_t kano_sonya_victim_groups[]={", 1)[1].split("};", 1)[0]
        actual = [int(value, 16) for value in re.findall(r"0x[0-9a-f]+", body)]
        self.assertEqual(actual, [animation.relocate_pointer(group)
                                  for group in fatality.KANO_SONYA_VICTIM_GROUPS])
        trace = (root / "diagnostic_v116_mk3_kano_vs_sonya_fatality/run.log").read_text()
        observed = [int(value, 16) for value in re.findall(
            r"MK3_FATALITY_POSE fighter=kano[^\n]*side=2 id=1 pose=(FF9B[0-9A-F]{4})", trace)]
        self.assertEqual(observed, list(fatality.KANO_SONYA_VICTIM_GROUPS))

    def test_jax_extraction_sequence_matches_original_trace(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        body = source.split("constexpr uint32_t kano_jax_victim_groups[]={", 1)[1].split("};", 1)[0]
        actual = [int(value, 16) for value in re.findall(r"0x[0-9a-f]+", body)]
        self.assertEqual(actual, [animation.relocate_pointer(group)
                                  for group in fatality.KANO_JAX_VICTIM_GROUPS])
        trace = (root / "diagnostic_v137_mk3_kano_jax_zero_win_auto/run.log").read_text()
        observed = [int(value, 16) for value in re.findall(
            r"MK3_FATALITY_POSE fighter=kano[^\n]*side=2 id=2 pose=(FF9B[0-9A-F]{4})", trace)]
        self.assertEqual(observed, list(fatality.KANO_JAX_VICTIM_GROUPS))

    def test_jax_extraction_palette_matches_both_runtime_traces(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        self.assertIn("donor[0x92e9a+color*2]", source)
        self.assertEqual(struct.unpack_from("<H", self.original, 0x92e98)[0], 64)
        expected = list(struct.unpack_from("<64H", self.original, 0x92e9a))
        for path, marker in (
            ("diagnostic_v139_mk3_jax_victim_palette/run.log",
             "MK3_FATALITY_JAX_VICTIM_COLORS"),
            ("diagnostic_v140_kano_jax_finish/run.log",
             "MK2_FINISH_JAX_VICTIM_PALETTE"),
        ):
            trace = (root / path).read_text()
            match = re.search(marker + r"[^\n]*colors=([0-9A-F,]+)", trace)
            self.assertIsNotNone(match, path)
            actual = [int(value, 16) for value in match.group(1).split(",")]
            self.assertEqual(actual, expected, path)

    def test_masked_sub_zero_extraction_ends_in_stock_prone_pose(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        body = source.split("constexpr uint32_t kano_subzero_victim_groups[]={", 1)[1].split("};", 1)[0]
        actual = [int(value, 16) for value in re.findall(r"0x[0-9a-f]+", body)]
        self.assertEqual(actual, [0xff97bfd0, 0xff97c030, 0xff97c070,
                                  0xff97ba10, 0xff97ba70, 0xff97bad0])
        stock = (root / "diagnostic_v148_stock_subzero_prone/run.log").read_text()
        self.assertRegex(stock, r"MK2_STOCK_SUBZERO_PRONE[^\n]*health=0 pose=FF97BAD0")
        runtime = (root / "regression_v150_finish_victims_kano_vs_sub_zero/run.log").read_text()
        self.assertRegex(runtime, r"MK2_FINISH_ACTORS[^\n]*age=281[^\n]*:0008:FF97BAD0:")
        self.assertNotIn("MK2_FINISH_SUBZERO_VICTIM_PALETTE", runtime)
        p2_runtime = (root / "diagnostic_v150_p2_kano_vs_subzero_finish/run.log").read_text()
        self.assertRegex(p2_runtime, r"MK2_FINISH_ACTORS[^\n]*:0008:FF97BAD0:")
        self.assertIn("MK2KS_EXIT_RESULT pass=true", p2_runtime)

    def test_stock_victim_extraction_rows_match_mkii_and_held_prone_traces(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "mame-mkp/src/mame/midway/midtunit_m.cpp").read_text()
        body = source.split("constexpr uint32_t kano_stock_victim_groups[11][6]={", 1)[1].split("};", 1)[0]
        rows = [[int(value, 16) for value in re.findall(r"0x[0-9a-f]+", row)]
                for row in re.findall(r"\{([^{}]+)\}", body)]
        self.assertEqual((len(rows), {len(row) for row in rows}), (11, {6}))
        mk2 = (root / "mk2/mk2-maincpu.bin").read_bytes()
        main = [animation.u32(mk2, animation.MK2_MAIN_TABLE + i * 4)
                for i in range(17)]
        special = [animation.u32(mk2, animation.MK2_SPECIAL_TABLE + i * 4)
                   for i in range(17)]
        for fighter, name in enumerate(STOCK_NAMES[:11]):
            start = main[fighter]
            end = min((address for address in main if address > start),
                      default=0xffe00000)
            spans = animation.sequence_spans(mk2, start, (start, end),
                                             (start, special[fighter]))
            def groups(row):
                return [address for _, address, _ in animation.group_references(
                    mk2, *spans[row], start, end)]
            death, knockback = groups(15), groups(18)
            trace = (root / f"diagnostic_v151_stock_prone_{name}/run.log").read_text()
            held = re.search(r"MK2_STOCK_VICTIM_HELD[^\n]*health=0 pose=([0-9A-F]{8})", trace)
            self.assertIsNotNone(held, name)
            final = death.index(int(held.group(1), 16))
            expected = [*knockback[:3], *death[final-2:final+1]]
            self.assertEqual(rows[fighter], expected, name)


if __name__ == "__main__":
    unittest.main()
