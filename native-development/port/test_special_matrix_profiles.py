import unittest
from qualify_special_matrix import profile,qualify

class SpecialProfiles(unittest.TestCase):
    def test_refresh_plan_covers_sixteen_unique_cases_without_overwrites(self):
        from refresh_special_regression import plan
        fixtures=plan('test_current')
        self.assertEqual(len(fixtures),14)
        self.assertEqual(len({name for name,_ in fixtures}),14)
        self.assertEqual(len({entry for _,args in fixtures for entry in profile(args)[1]}),16)
        with self.assertRaises(AssertionError):plan('../outside')

    def test_full_both_side_mapping(self):
        cases=[]
        for args in (['--projectiles'],['--special'],['--special','--square'],
                     ['--blade'],['--choke'],['--bike'],['--leg']):
            for mirror in ([],['--mirror']):cases.extend(profile(args+mirror)[1])
        self.assertEqual(len(cases),16)
        self.assertEqual(len(set(cases)),16)
        self.assertIn((17,'knife',2),cases)
        self.assertIn((18,'square',1),cases)

    def test_ambiguous_or_missing_family_rejected(self):
        for args in ([],['--blade','--choke'],['--projectiles','--square'],['--square']):
            with self.assertRaises(AssertionError):profile(args)

    def test_no_silent_historical_defaults(self):
        with self.assertRaises(AssertionError):qualify([])
        with self.assertRaises(AssertionError):qualify(['same']*14)

if __name__=='__main__':unittest.main()
