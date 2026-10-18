import re
import unittest
from pathlib import Path

class NormalProbeTests(unittest.TestCase):
    def test_contact_crouch_preparation_does_not_change_baseline_schedule(self):
        source=(Path(__file__).parent/'diagnostics/normal_probe.lua').read_text()
        self.assertIn("((requested~='' and case[3]=='Down') and 24 or 12)",source)
        self.assertIn("case[3]=='Down' and age<attackAge+4",source)
    def test_contact_controls_are_explicit_and_never_position_writes(self):
        port=Path(__file__).parent
        source=(port/'diagnostics/normal_probe.lua').read_text()
        self.assertIn("requested=='' or side==attacker",source)
        self.assertIn("if requested~='' and blocking then set('P'..(3-attacker)..' Block',1) end",source)
        self.assertIn("set('P'..attacker..' '..direction,1)",source)
        self.assertIn("gap==70 or gap==90 or gap==100",source)
        self.assertNotIn(':write_u',source)
    def test_fourteen_explicit_physical_profiles_and_read_only_observation(self):
        port=Path(__file__).parent
        source=(port/'diagnostics/normal_probe.lua').read_text()
        names=re.findall(r"\{'([a-z]+)','",source)
        self.assertEqual(len(names),14)
        self.assertEqual(len(set(names)),14)
        self.assertNotIn(':write_u',source)
        self.assertNotRegex(source,r'\.value\s*=(?!=)')
        self.assertIn('combat>=#cases*120+120',source)
        self.assertIn("word(a+0x1f0),word(b+0x1f0)",source)
        wrapper=(port.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--normal-moves' in sys.argv:",wrapper)
        self.assertIn("probe=HERE.parent/'port/diagnostics/normal_probe.lua'",wrapper)
