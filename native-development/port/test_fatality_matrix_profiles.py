import unittest
from qualify_own_fatality_matrix import profile,qualify

class FatalityProfiles(unittest.TestCase):
    def test_refresh_plan_is_complete_and_distinct(self):
        from refresh_fatality_regression import plan
        fixtures=plan('test_current')
        self.assertEqual(len({name for name,_ in fixtures}),8)
        self.assertEqual(len({profile(args) for _,args in fixtures}),8)
        with self.assertRaises(AssertionError):plan('../outside')

    def test_all_own_finishers_both_sides(self):
        cases=[profile(['--'+kind,'--finisher-rejoin',*mirror])
               for kind in ('extract','laser','kiss','bubble') for mirror in ([],['--mirror'])]
        self.assertEqual(len(set(cases)),8)
        self.assertIn(('kiss',2,17),cases)
        self.assertIn(('laser',1,18),cases)

    def test_missing_rejoin_negative_or_ambiguous_is_rejected(self):
        for args in ([],['--extract'],['--extract','--laser','--finisher-rejoin'],
                     ['--kiss','--finisher-rejoin','--negative']):
            with self.assertRaises(AssertionError):profile(args)

    def test_no_historical_defaults_or_duplicate_cases(self):
        with self.assertRaises(AssertionError):qualify([])
        with self.assertRaises(AssertionError):qualify(['same']*8)

if __name__=='__main__':unittest.main()
