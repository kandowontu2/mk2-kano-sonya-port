import unittest
from refresh_ground_contact import plan

class GroundContactPlanTests(unittest.TestCase):
    def test_crouch_retry_does_not_repeat_qualified_back_attacks(self):
        fixtures=plan('crouch_retry',True)
        self.assertEqual(len(fixtures),8)
        self.assertTrue(all('--normal-case=roundhouse' not in args and '--normal-case=sweep' not in args for _,args in fixtures))
    def test_twelve_distinct_ground_cases_with_low_guard_for_low_attacks(self):
        fixtures=plan('ground_contact_test')
        self.assertEqual(len(fixtures),12)
        self.assertEqual(len({name for name,_ in fixtures}),12)
        for _,args in fixtures:
            low=any(f'--normal-case={move}' in args for move in ('sweep','duckpunch','duckhighkick','ducklowkick'))
            self.assertEqual('--normal-low-block' in args,low and '--normal-block' in args)
        with self.assertRaises(AssertionError):plan('../outside')
