import unittest
from refresh_morph_regression import plan


class MorphSpecialPlan(unittest.TestCase):
    def test_complete_special_profiles_both_sides(self):
        fixtures = plan('current', all_specials=True)
        self.assertEqual(len(fixtures), 10)
        self.assertEqual(len({name for name, _ in fixtures}), 10)
        for flag in ('specials', 'ball', 'square', 'melee', 'grapples'):
            cases = [args for _, args in fixtures if '--morph-' + flag in args]
            self.assertEqual(len(cases), 2)
            self.assertEqual(sum('--mirror' in args for args in cases), 1)
            for args in cases:
                self.assertIn('--game', args)
                self.assertIn('--morph', args)
                self.assertIn('--sound-candidate', args)

    def test_old_profiles_and_invalid_combinations(self):
        self.assertEqual(len(plan('current')), 4)
        self.assertEqual(len(plan('current', ball_only=True)), 2)
        with self.assertRaises(AssertionError):
            plan('current', ball_only=True, all_specials=True)
        with self.assertRaises(AssertionError):
            plan('../escape', all_specials=True)


if __name__ == '__main__':
    unittest.main()
