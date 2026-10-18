import json
from pathlib import Path
import unittest
from build_arm_rip_assets import read_pgm
from build_inflation_assets import unpack6, sha
from kiss_inflate_source import DIE, DEATH, WAIT_OLD, WAIT_NEW

PORT = Path(__file__).resolve().parent
SRC = PORT.parent/'baseline/mk2-rebuild-main/srcp'


class InflationSourceTests(unittest.TestCase):
    def test_linked_dispatches(self):
        for filename, replacements in (('MKDIE.ASM', DIE), ('MKDEATH.ASM', DEATH)):
            text = (SRC/filename).read_text()
            for old, new in replacements:
                self.assertEqual(text.count(new), 1)
                self.assertEqual(new.count(old), 1)  # original helper path retained
        self.assertIn(WAIT_OLD, (SRC/'MKDEATH.ASM').read_text())
        self.assertNotIn(WAIT_NEW, (SRC/'MKDEATH.ASM').read_text())
        self.assertTrue(WAIT_NEW.startswith(WAIT_OLD))
        self.assertIn('cmpi 17,a0', WAIT_NEW)
        self.assertIn('cmpi 18,a0', WAIT_NEW)
        self.assertIn('movi 0100H,a10', WAIT_NEW)
        self.assertIn('andi m_inviso,a0', WAIT_NEW)

    def test_all_native_pixels_and_origins_reflected(self):
        folder = PORT/'generated_inflation_v3'
        data = json.loads((folder/'INFLATION_DATA.json').read_text())
        packed = (folder/'fighter_ui_finish_inflate_graphics.bin').read_bytes()
        self.assertEqual(sha(packed), data['packedSHA256'])
        self.assertTrue(data['nativeFacingNormalized'])
        for frame in data['frames']:
            w, h, source = read_pgm(PORT/'assets/inflation_v3'/frame['file'])
            start = frame['packedByteOffset']
            decoded = unpack6(packed[start:start+frame['packedBytes']], w*h)
            for y in range(h):
                self.assertEqual(decoded[y*w:(y+1)*w], source[y*w:(y+1)*w][::-1])
            self.assertEqual(frame['xOffset'], w-1-frame['sourceXOffset'])


if __name__ == '__main__':
    unittest.main()
