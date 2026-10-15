import struct
import unittest
from pathlib import Path

import build_native_kiss as kiss
from prepare_sonya_arc_payload import upgrade

ROOT=Path(__file__).resolve().parents[1]


class SonyaArcAssetsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current=(ROOT/'diagnostic_v265_skeleton_facing_trial/roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        cls.output,cls.report=upgrade(cls.current,cls.program,ROOT/'mk3')

    def test_missing_frame_comes_from_actual_original_trace(self):
        log=(ROOT/'audit_v266_original_sonya_native_contact/run.log').read_text(encoding='utf-8-sig')
        self.assertIn('launch_age=41',log)
        self.assertIn('graphic=FFB26700',log)
        self.assertEqual(self.report['frames'][-1]['source'],'ffb26700')
        self.assertEqual(len(self.report['frames']),8)

    def test_preserves_all_other_character_data_and_legacy_pixels(self):
        self.assertEqual(self.current[:kiss.HEADER],self.output[:kiss.HEADER])
        old_bytes=struct.unpack_from('<I',self.current,kiss.HEADER+8)[0]
        self.assertEqual(self.current[kiss.PIXELS:kiss.PIXELS+old_bytes],
                         self.output[kiss.PIXELS:kiss.PIXELS+old_bytes])

    def test_eighth_descriptor_is_real_native_six_bit_art(self):
        record=struct.unpack_from('<4hIHI',self.output,kiss.FRAMES+7*kiss.FRAME_STRIDE)
        self.assertEqual(record[:4],(29,25,-36,-24))
        self.assertEqual(record[5],0x6000)
        self.assertEqual(record[6],kiss.BASE+kiss.PALETTE*8)
        self.assertEqual(struct.unpack_from('<I',self.output,kiss.HEADER+16)[0],8)

    def test_rejects_unrelated_or_changed_current_payload(self):
        changed=bytearray(self.current)
        changed[kiss.PALETTE+4]^=1
        with self.assertRaises(ValueError):
            upgrade(bytes(changed),self.program,ROOT/'mk3')


if __name__=='__main__':
    unittest.main()
