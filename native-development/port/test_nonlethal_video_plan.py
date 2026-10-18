import unittest
from refresh_nonlethal_videos import plan
from nonlethal_profiles import profile

class NonlethalVideoPlanTests(unittest.TestCase):
    def test_four_eligible_own_profiles_with_recovery_and_audio(self):
        fixtures=plan('current_nonlethal')
        self.assertEqual({(kind,actor) for _,kind,actor,_ in fixtures},{(kind,actor) for kind in ('friend','baby') for actor in (17,18)})
        self.assertEqual(len({name for name,_,_,_ in fixtures}),4)
        for _,kind,actor,args in fixtures:
            self.assertEqual(profile(args)[:3],(kind,actor,1))
            self.assertTrue(all(flag in args for flag in ('--audio','--capture-finish','--finisher-rejoin')))
            self.assertNotIn('--punch-wins',args)
        with self.assertRaises(AssertionError):plan('../outside')
