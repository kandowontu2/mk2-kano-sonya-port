import hashlib
import json
from pathlib import Path
import re
import unittest
import wave
from current_sound import verify_latest_playlist

PORT=Path(__file__).resolve().parent
BUILD=PORT.parent/'baseline/mk2-rebuild-main'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()

class KanoPopStaging(unittest.TestCase):
    def test_native_call_at_pop_pose(self):
        text=(PORT/'asm/KSFRIEND.ASM').read_text()
        self.assertEqual((BUILD/'srcp/KSFRIEND.ASM').read_text(),text)
        self.assertIn('cmpi ks_friend_pose_ff9d2750,a0\n        jrne ks_gum_no_pop\n        tsound 0104h',text)
        self.assertEqual(text.count('tsound 0104h'),1)
        self.assertEqual(text.count('.long ks_friend_pose_ff9d2710,ks_friend_pose_ff9d2750'),1)
        source=(BUILD/'srcp/MKSOUND.ASM').read_text()
        self.assertEqual(source.count('sp_effect|40,07eeH'),1)

    def test_bounded_staged_clip_and_calls(self):
        report=json.loads((PORT/'generated_dcs/DCS_KANO_POP_INPUTS.json').read_text())
        source=Path(report['source'])
        self.assertEqual(sha(source.read_bytes()),report['sourceSHA256'])
        with wave.open(str(source),'rb') as wav:
            self.assertLessEqual(wav.getnframes(),wav.getframerate()*2)
        pcm=(BUILD/'soundp/SNDS/KSKP.SND').read_bytes()
        self.assertEqual(len(pcm),report['samples']*2)
        self.assertEqual(sha(pcm),report['pcmSHA256'])
        playlist=(BUILD/'soundp/MK2.PLS').read_bytes()
        ball=json.loads((PORT/'generated_dcs/DCS_KANO_BALL_INPUTS.json').read_text())
        self.assertEqual(ball['previousPlaylistSHA256'],report['stagedPlaylistSHA256'])
        verify_latest_playlist()
        text=playlist.decode('latin-1')
        for event in range(2000,2033):
            self.assertEqual(len(re.findall(rf'^\s*{event}\s+immed\s+{event}\s*$',text,re.M)),1)
            self.assertEqual(len(re.findall(rf'^\s*playlist\s+{event},',text,re.M)),1)
        self.assertEqual(report['tableIndex'],260)
        self.assertEqual(report['duration'],40)

if __name__=='__main__':unittest.main()
