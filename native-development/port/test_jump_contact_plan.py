import unittest
from pathlib import Path
from refresh_jump_contact import plan

class JumpContactPlanTests(unittest.TestCase):
    def test_eight_cases_preserve_native_physics_and_baseline_timing(self):
        fixtures=plan('jump_contact_test')
        self.assertEqual(len(fixtures),8)
        self.assertEqual(len({name for name,_ in fixtures}),8)
        for _,args in fixtures:
            diagonal=any(a in args for a in ('--normal-case=flyingkick','--normal-case=flyingpunch'))
            self.assertIn('--normal-gap=180' if diagonal else '--normal-gap=70',args)
        source=(Path(__file__).parent/'diagnostics/normal_probe.lua').read_text()
        self.assertIn("local jumpAge=requested~='' and 20 or 0",source)
        self.assertIn("then attackAge=48 end",source)
        self.assertNotIn(':write_u',source)
        with self.assertRaises(AssertionError):plan('../outside')
