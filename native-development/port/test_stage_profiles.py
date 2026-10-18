import collections
import unittest
from stage_profiles import profile
from refresh_stage_regression import plan

class StageProfiles(unittest.TestCase):
    def test_all_sixteen_distinct_roles(self):
        fixtures=plan('test_current')
        self.assertEqual(len({name for name,_ in fixtures}),16)
        roles=[profile(args) for _,args in fixtures]
        self.assertEqual(len(set(roles)),16)
        self.assertEqual(collections.Counter(k for k,_,_ in roles),dict(deadpool=4,tomb=4,negative=4,pit=4))

    def test_ambiguous_or_incomplete_stage_modes_rejected(self):
        base=['--stage','--own-victim']
        for extra in ([],['--deadpool','--pit-progress','--pit-rejoin'],
                      ['--deadpool-no-chord','--stage-rematch'],
                      ['--stage-rematch','--pit-progress'],['--stage-rematch','--pit-rejoin']):
            with self.assertRaises(AssertionError):profile(base+extra)

    def test_output_escape_rejected(self):
        with self.assertRaises(AssertionError):plan('../outside')

if __name__=='__main__':unittest.main()
