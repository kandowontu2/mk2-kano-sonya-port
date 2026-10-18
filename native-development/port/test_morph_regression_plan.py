from pathlib import Path
import unittest
from refresh_morph_regression import plan

class MorphPlan(unittest.TestCase):
    def test_ball_mode_is_explicit_both_sides_without_other_commands(self):
        fixtures=plan('ball_current',True)
        self.assertEqual(len(fixtures),2)
        self.assertEqual(sum('--mirror' in args for _,args in fixtures),1)
        for _,args in fixtures:
            self.assertIn('--morph-ball',args)
            self.assertNotIn('--morph-specials',args)
            self.assertNotIn('--morph-throws',args)

    def test_both_sides_and_late_throw_modes(self):
        fixtures=plan('test_current')
        self.assertEqual(len({name for name,_ in fixtures}),4)
        self.assertEqual(sum('--morph-specials' in args for _,args in fixtures),2)
        self.assertEqual(sum('--morph-late-throw' in args and '--morph-throws' in args for _,args in fixtures),2)
        self.assertEqual(sum('--mirror' in args for _,args in fixtures),2)

    def test_escape_and_silent_historical_art_default_rejected(self):
        with self.assertRaises(AssertionError):plan('../outside')
        source=(Path(__file__).parent/'qualify_morph_art_trace.py').read_text()
        self.assertNotIn('or [323,324]',source)
        self.assertIn('Supply two explicit completed current morph runs',source)

if __name__=='__main__':unittest.main()
