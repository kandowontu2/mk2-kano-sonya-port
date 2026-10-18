import unittest
from refresh_special_videos import plan

class SpecialVideoPlanTests(unittest.TestCase):
    def test_eight_unique_bounded_audio_profiles(self):
        fixtures=plan('current_video')
        self.assertEqual({kind for _,kind,_ in fixtures},{'ball','blade','choke','leg','bike','square','knife','ring'})
        self.assertEqual(len({name for name,_,_ in fixtures}),8)
        for _,_,args in fixtures:
            self.assertTrue(all(flag in args for flag in ('--game','--audio','--capture-move','--sound-candidate','--capture-min-fields=150')))
        with self.assertRaises(AssertionError):plan('../outside')
