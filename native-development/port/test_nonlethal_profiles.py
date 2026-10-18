import unittest
from nonlethal_profiles import profile
from refresh_nonlethal_regression import plan

class NonlethalProfiles(unittest.TestCase):
    def test_complete_distinct_positive_and_negative_roles(self):
        fixtures=plan('test_current')
        self.assertEqual(len({name for name,_,_ in fixtures}),16)
        for mode in (False,True):
            roles={profile(args,negative) for _,args,negative in fixtures if negative==mode}
            self.assertEqual(len(roles),8)
            self.assertIn(('baby',18,2,17),roles)
            self.assertIn(('friend',17,1,18),roles)

    def test_rejoin_and_eligibility_modes_cannot_be_mixed(self):
        for args,negative in ((['--friend','--kano'],False),
                              (['--friend','--kano','--punch-wins','--finisher-rejoin'],True),
                              (['--baby','--finisher-rejoin'],False),
                              (['--friend','--finisher-rejoin'],False)):
            with self.assertRaises(AssertionError):profile(args,negative)

    def test_ambiguous_families_and_output_escape_rejected(self):
        with self.assertRaises(AssertionError):profile(['--friend','--baby','--finisher-rejoin'])
        with self.assertRaises(AssertionError):plan('../outside')

if __name__=='__main__':unittest.main()
