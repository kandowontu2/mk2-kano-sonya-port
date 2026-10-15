"""Checks for the original Sonya fatality fire-orb asset conversion."""
import re
import struct
import unittest
from pathlib import Path

import build_native_kiss as kiss


class NativeKissTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.original = (cls.root / "mk3/mk3-maincpu.bin").read_bytes()
        cls.base = (cls.root / "diagnostic_v118_full_payload_rebuild/mk2ks.mdata").read_bytes()
        cls.full = (cls.root / "diagnostic_v128_kiss_aligned_full_build/mk2ks.mdata").read_bytes()

    def test_frames_are_the_observed_original_projectile(self):
        trace = (self.root / "diagnostic_v122_mk3_sonya_orb_frames/run.log").read_text()
        observed = [int(value, 16) for value in re.findall(
            r"MK3_FATALITY_ORB_FRAME age=\d+[^\n]*graphic=(FFB[0-9A-F]{5}) pose=00000000",
            trace)]
        self.assertEqual(observed, list(kiss.SOURCE_FRAMES))
        payload = bytearray(self.base)
        report = kiss.build(payload, self.original, self.root / "mk3")
        self.assertEqual(bytes(payload), self.full)
        self.assertEqual((len(report["frames"]), report["pixel_bytes"]), (7, 3804))
        self.assertEqual(report["used_indices"], list(range(31)))

    def test_native_palette_descriptors_and_scope(self):
        payload = self.full
        self.assertEqual(payload[kiss.HEADER:kiss.HEADER + 4], b"KKS2")
        self.assertEqual(struct.unpack_from("<I", payload, kiss.HEADER + 16)[0], 7)
        self.assertEqual(struct.unpack_from("<H", payload, kiss.PALETTE)[0], 64)
        colors = struct.unpack_from("<32H", payload, kiss.PALETTE + 2)
        self.assertEqual(colors[:4], (0, 0x7FFF, 0x7FFB, 0x7FF8))
        for index in range(7):
            self.assertEqual((kiss.FRAMES + index * kiss.FRAME_STRIDE) & 0xF, 0)
            width, height, xo, yo, source, command, palette = struct.unpack_from(
                "<4hIHI", payload, kiss.FRAMES + index * kiss.FRAME_STRIDE)
            self.assertIn(width, (29, 30))
            self.assertIn(height, (24, 25, 26))
            self.assertIn(xo, (-36, -35))
            self.assertEqual(yo, -24)
            self.assertEqual(command, 0x6000)
            self.assertEqual(palette, kiss.BASE + kiss.PALETTE * 8)
            self.assertGreaterEqual(source, kiss.GFX_DEST * 8)
        self.assertEqual(payload[:kiss.HEADER], self.base[:kiss.HEADER])


if __name__ == "__main__":
    unittest.main()
