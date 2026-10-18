import unittest
from refresh_lethal_videos import plan

class LethalVideoPlanTests(unittest.TestCase):
    def test_four_unique_earned_audio_rejoin_profiles(self):
        fixtures=plan('current_lethal')
        self.assertEqual({kind for _,kind,_ in fixtures},{'extract','laser','kiss','bubble'})
        self.assertEqual(len({name for name,_,_ in fixtures}),4)
        for _,kind,args in fixtures:
            self.assertIn('--'+kind,args)
            self.assertTrue(all(flag in args for flag in ('--game','--audio','--sound-candidate','--capture-finish','--finisher-rejoin')))
            self.assertNotIn('--negative',args)
        with self.assertRaises(AssertionError):plan('../outside')
