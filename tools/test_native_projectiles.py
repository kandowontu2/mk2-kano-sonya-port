"""Asset regression checks against the actual local ROM inputs."""
import struct
import unittest
from pathlib import Path

import build_mk2ks_mk3 as animation
import build_native_projectiles as native
import upgrade_ksui_previews as decoder


class NativeProjectileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = Path(__file__).resolve().parents[1]
        cls.program = (cls.workspace / "mk3/mk3-maincpu.bin").read_bytes()
        cls.payload = bytearray(b"\xff" * 0x200000)
        cls.report = native.build(cls.payload, cls.program, cls.workspace / "mk3")
        cls.gfx = decoder.load_gfx(cls.workspace / "mk3")

    def test_allocations_and_header(self):
        magic, source, size, destination = struct.unpack_from("<4sIII", self.payload, native.HEADER)
        self.assertEqual((magic, source, destination), (b"KFX1", native.PIXELS, native.GFX_DEST))
        self.assertLessEqual(source + size, len(self.payload))
        self.assertEqual(self.payload[:native.HEADER], b"\xff" * native.HEADER)

    def test_native_pixel_round_trip_and_palettes(self):
        for fighter in ("kano", "sonya"):
            self.assertLess(max(self.report[fighter]["used_indices"]), self.report[fighter]["palette_colors"])
            for record in self.report[fighter]["frames"]:
                with self.subTest(fighter=fighter, frame=record["source"]):
                    frame = int(record["native"], 16)
                    w, h, xo, yo, source, command, palette = struct.unpack_from(
                        "<4hIHI", self.payload, (frame - native.BASE) // 8)
                    self.assertEqual(command, 0x6000)
                    pal = (palette - native.BASE) // 8
                    self.assertEqual(struct.unpack_from("<HH", self.payload, pal), (64, 0))
                    # Decode donor pixels independently through the existing
                    # image decoder and compare every native pixel index.
                    spec = decoder.component_spec(self.program, int(record["source"], 16))
                    index_palette = [(index, 0, 0, 255) for index in range(256)]
                    original = decoder.decode_component(self.gfx, index_palette, *spec[:4])
                    for y in range(h):
                        for x in range(w):
                            actual = decoder.extract_bits(self.payload,
                                native.PIXELS * 8 + source - native.GFX_DEST * 8 + (y * w + x) * 6, 63)
                            self.assertEqual(actual, original.getpixel((x, y))[0])
                    if fighter == "kano":
                        self.assertEqual((xo, yo), (spec[4] - 100, spec[5] - 72))
                    else:
                        self.assertEqual((xo, yo), spec[4:])

    def test_occupied_storage_is_rejected(self):
        occupied = bytearray(b"\xff" * 0x200000)
        occupied[native.FRAMES] = 0
        with self.assertRaisesRegex(ValueError, "occupied"):
            native.build(occupied, self.program, self.workspace / "mk3")


if __name__ == "__main__":
    unittest.main()
