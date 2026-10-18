"""Source eligibility of all fourteen demo choices; not CPU runtime coverage."""
from pathlib import Path
import re
import unittest
import zipfile

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'

class DemoRoster(unittest.TestCase):
    def test_three_native_random_choice_paths(self):
        pattern=(r'movk\s+14,a0\s+calla\s+randu\s+dec\s+a0\s+'
            r'cmpi 12,a0\s+jrlo (ks_demo_\w+_ready)\s+addk 5,a0\s+\1\s+'
            r'move\s+a0,@(p[12]_char),w')
        amode=re.findall(pattern,(SRC/'MKAMODE.ASM').read_text())
        main=re.findall(pattern,(SRC/'MAIN.ASM').read_text())
        self.assertEqual(amode,[('ks_demo_p1_ready','p1_char'),('ks_demo_p2_ready','p2_char')])
        self.assertEqual(main,[('ks_demo_cpu_ready','p2_char')])
        outcomes=[i if i<12 else i+5 for i in range(14)]
        self.assertEqual(outcomes,list(range(12))+[17,18])
        self.assertEqual(len(set(outcomes)),14)

    def test_original_random_helper_preserved(self):
        with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as archive:
            original=archive.read('mk2-rebuild-main/src/UTIL.ASM').decode('cp437').replace('\r\n','\n')
        def body(text):return text.split('randu:',1)[1].split('srand:',1)[0]
        self.assertEqual(body(original),body((SRC/'UTIL.ASM').read_text()))

    def test_cpu_observer_has_no_guest_writes_or_gameplay_inputs(self):
        source=(PORT/'diagnostics/cpu_attract_probe.lua').read_text()
        self.assertNotIn('write_u',source)
        self.assertNotIn("'Coin 1'",source)
        self.assertNotIn("'1 Player Start'",source)
        self.assertIn('n>=ackStart and n<3000 and n%40<4 and 1 or 0',source)
        self.assertIn('n-seen[c]>=60',source)
        self.assertIn('u16(0x010602f0)<161 or u16(0x01060ec0)<161',source)

    def test_long_cpu_run_gets_long_wall_bound(self):
        source=PORT.parent/'baseline/test_wolf_baseline.py'
        text=source.read_text()
        self.assertIn("wall_limit=90 if any(flag in sys.argv for flag in ('--campaign-long','--cpu-long')) else 60",text)
        self.assertIn('timeout=wall_limit',text)
        self.assertIn('wallTimeoutSeconds=wall_limit',text)

if __name__=='__main__':unittest.main()
