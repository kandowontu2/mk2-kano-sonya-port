import unittest
from refresh_original_torso_controls import plan

class OriginalTorsoPlanTests(unittest.TestCase):
    def test_exact_original_families_and_sides(self):
        cases=plan('original_controls')
        self.assertEqual(len({name for name,_ in cases}),4)
        self.assertEqual({('swipe' if '--swipe-victim' in args else 'torso',2 if '--mirror' in args else 1) for _,args in cases},
                         {(family,side) for family in ('torso','swipe') for side in (1,2)})
        self.assertTrue(all('--stock-victim' in args and '--finisher-rejoin' in args and '--sonya' not in args for _,args in cases))

    def test_path_prefix_rejected(self):
        with self.assertRaises(AssertionError):plan('../outside')
