import unittest
from refresh_morph_videos import plan

class MorphVideoPlanTests(unittest.TestCase):
    def test_both_targets_with_bounded_morph_capture(self):
        fixtures=plan('morph_video_test')
        self.assertEqual([actor for _,actor,_ in fixtures],[17,18])
        self.assertEqual(len({name for name,_,_ in fixtures}),2)
        for _,actor,args in fixtures:
            for flag in ('--game','--morph','--morph-specials','--capture-move',
                         '--capture-action=0x404','--audio','--sound-candidate'):
                self.assertIn(flag,args)
            self.assertEqual('--mirror' in args,actor==18)
            self.assertIn(f'--capture-side={2 if actor==18 else 1}',args)
        self.assertIn('--capture-not-before=4500',fixtures[1][2])
        with self.assertRaises(AssertionError):plan('../outside')
