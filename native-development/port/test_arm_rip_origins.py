import json
from pathlib import Path
import re
import unittest
from arm_rip_origins import REFERENCE,origin

PORT=Path(__file__).resolve().parent

class ArmOrigins(unittest.TestCase):
    def test_native_reference_rows(self):
        text=(PORT.parent/'baseline/mk2-rebuild-main/srcp/MKMK3.TBL').read_text()
        for actor,prefix in (('kano','LKRIPARM'),('sonya','NJGIRLARM')):
            for phase,expected in enumerate(REFERENCE[actor],1):
                with self.subTest(actor=actor,phase=phase):
                    match=re.search(rf'(?m)^{prefix}{phase}:\s*\n\s*\.word\s+([^\n]+)',text)
                    self.assertIsNotNone(match)
                    self.assertEqual(tuple(map(int,match[1].split(','))),expected)

    def test_dimension_adjusted_own_headers(self):
        metadata=json.loads((PORT/'generated_arm_rip/ARM_RIP_DATA.json').read_text())
        count=0
        for frame in metadata['frames']:
            if frame['role']!='arm':continue
            count+=1
            actor,phase=frame['actor'],frame['phase'];w,h=frame['width'],frame['height']
            oldw,oldh,oldx,oldy=REFERENCE[actor][phase]
            x,y=origin(actor,phase,w,h)
            with self.subTest(actor=actor,phase=phase):
                self.assertEqual((frame['xOffset'],frame['yOffset']),(x,y))
                self.assertLessEqual(abs((-x+w/2)-(-oldx+oldw/2)),0.5)
                self.assertEqual(-y+h,-oldy+oldh)
        self.assertEqual(count,10)

    def test_no_single_origin_for_all_phases(self):
        for actor in REFERENCE:
            self.assertEqual(len({origin(actor,phase,57,26) for phase in range(5)}),5)

if __name__=='__main__':unittest.main()
