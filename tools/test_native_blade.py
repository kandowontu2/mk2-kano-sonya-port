"""Exact donor-art regression checks for the separately owned blade trail."""
import struct
import unittest
from pathlib import Path

import build_mk2ks_mk3 as animation
import build_native_blade as native
import build_native_projectiles as projectiles
import upgrade_ksui_previews as decoder


class NativeBladeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.program = (cls.root / "mk3/mk3-maincpu.bin").read_bytes()
        cls.gfx = decoder.load_gfx(cls.root / "mk3")
        cls.payload = bytearray(b"\xff" * 0x200000)
        projectiles.build(cls.payload, cls.program, cls.root / "mk3")
        cls.before = bytes(cls.payload)
        cls.report = native.build(cls.payload, cls.program, cls.root / "mk3")

    def test_separate_allocation_preserves_all_existing_assets(self):
        self.assertEqual(self.payload[:native.HEADER], self.before[:native.HEADER])
        self.assertEqual(self.payload[native.END:], self.before[native.END:])
        header = struct.unpack_from("<4sIIII", self.payload, native.HEADER)
        self.assertEqual(header, (b"KBL1", native.PIXELS,
                                 self.report["pixel_bytes"], native.GFX_DEST, 10))
        self.assertLessEqual(native.PIXELS + header[2], native.END)
        projectile_size = struct.unpack_from("<I", self.payload, projectiles.HEADER + 8)[0]
        self.assertLessEqual(projectiles.GFX_DEST + projectile_size, native.GFX_DEST)

    def test_original_palette_not_body_palette(self):
        palette = struct.unpack_from("<H64H", self.payload, native.PALETTE)
        original_offset = animation.stock_file(native.SOURCE_PALETTE)
        original = struct.unpack_from("<H24H", self.program, original_offset)
        self.assertEqual(palette[:2], (64, 0))
        self.assertEqual(palette[2:25], original[2:])
        self.assertEqual(palette[25:], (0,) * 40)
        self.assertTrue(any(index >= 13 for frame in self.report["frames"]
                            for index in frame["used_indices"]))

    def test_all_ten_frames_match_original_pixels_and_offsets(self):
        self.assertEqual(len(self.report["frames"]), 10)
        for index, record in enumerate(self.report["frames"]):
            with self.subTest(frame=record["source"]):
                spec = decoder.component_spec(self.program, native.SOURCE_FRAMES[index])
                # The preview decoder supports compressed rows only. Frame
                # zero is full-copy; decode its continuous source bits directly
                # instead of incorrectly treating pixel zero as a skip byte.
                original = (decoder.decode_component(self.gfx,
                    [(value, 0, 0, 255) for value in range(256)], *spec[:4])
                    if spec[1] & 0x80 else None)
                w, h, xo, yo, gfx, command, palette = struct.unpack_from(
                    "<4hIHI", self.payload, record["descriptor_offset"])
                self.assertEqual((w, h, xo, yo), spec[2:])
                self.assertEqual((command, palette), (0x6000, native.BASE + native.PALETTE * 8))
                source = native.PIXELS * 8 + gfx - native.GFX_DEST * 8
                for y in range(h):
                    for x in range(w):
                        if original is not None:
                            expected = original.getpixel((x, y))[0]
                        else:
                            bits = (spec[1] >> 12) & 7
                            bit = spec[0] + (y * w + x) * bits
                            word = int.from_bytes(self.gfx[bit // 8:bit // 8 + 2], "little")
                            expected = (word >> (bit & 7)) & ((1 << bits) - 1)
                        self.assertEqual(decoder.extract_bits(self.payload,
                            source + (y * w + x) * 6, 63), expected)

    def test_original_phase_timing_and_displacement(self):
        self.assertEqual(sum(native.POSE_FIELDS), 38)
        self.assertEqual(sum(native.X_ADVANCES), 57)
        self.assertEqual(sum(native.POSE_FIELDS[:5]), 10)
        self.assertEqual(native.POSE_FIELDS[7], 4 + 8)
        self.assertEqual(native.BODY_GROUPS[0], 0xFE82FC40)
        self.assertEqual(native.BODY_GROUPS[-1], 0xFE82FFA0)

    def test_occupied_allocation_rejected_without_mutation(self):
        payload = bytearray(self.before)
        payload[native.FRAMES] = 0
        before = bytes(payload)
        with self.assertRaisesRegex(ValueError, "occupied"):
            native.build(payload, self.program, self.root / "mk3")
        self.assertEqual(payload, before)

    def test_wrong_source_group_rejected_without_mutation(self):
        program = bytearray(self.program)
        struct.pack_into("<I", program, animation.stock_file(native.GROUPS[4]), 0)
        payload = bytearray(self.before)
        with self.assertRaisesRegex(ValueError, "component group"):
            native.build(payload, program, self.root / "mk3")
        self.assertEqual(payload, self.before)


if __name__ == "__main__":
    unittest.main()
