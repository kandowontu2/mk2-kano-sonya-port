import json
from pathlib import Path
import re
import unittest
from extend_dcs_kano_ball import encode,ROOT,DEST,OUT,sha
from current_sound import verify_latest_playlist

PORT=Path(__file__).resolve().parent

class Ball(unittest.TestCase):
    def test_original_asset_reproduces_pcm(self):
        report=json.loads((OUT/'DCS_KANO_BALL_INPUTS.json').read_text())
        pcm,metadata=encode(ROOT/'samples/mk2ks/kano_ball_launch.wav')
        self.assertEqual(pcm.tobytes(),(DEST/'SNDS/KSKB.SND').read_bytes())
        self.assertEqual(sha(pcm.tobytes()),report['pcmSHA256'])
        self.assertEqual(metadata['samples'],36111)
        self.assertEqual(report['duration'],72)
        verify_latest_playlist()
        text=(DEST/'MK2.PLS').read_text()
        for event in range(2000,2036):
            self.assertEqual(len(re.findall(rf'^\s*{event}\s+immed\s+{event}\s*$',text,re.M)),1)
            self.assertEqual(len(re.findall(rf'^\s*playlist\s+{event},',text,re.M)),1)

    def test_native_caller(self):
        source=(PORT/'asm/KANOMOV.ASM').read_text()
        live=PORT.parent/'baseline/mk2-rebuild-main/srcp'
        self.assertEqual(source,(live/'KANOMOV.ASM').read_text())
        self.assertEqual(source.count('tsound 0105h'),1)
        self.assertIn('calla init_special_act\n        tsound 0105h',source)
        self.assertIn('sp_attkv1|72,07f1H',(live/'MKSOUND.ASM').read_text())

if __name__=='__main__':unittest.main()
