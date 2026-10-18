import unittest
from refresh_normal_videos import plan
from qualify_captured_normal import verify_interval

class NormalVideoTests(unittest.TestCase):
    def test_thirty_four_distinct_native_action_demonstrations(self):
        fixtures=plan('normal_video_test')
        self.assertEqual(len(fixtures),34)
        self.assertEqual(len({name for name,_,_,_ in fixtures}),34)
        for actor in (17,18):
            self.assertEqual(len({label for _,a,label,_ in fixtures if a==actor}),17)
        for _,actor,_,args in fixtures:
            for flag in ('--audio','--capture-move','--capture-min-fields=150','--capture-side=1'):
                self.assertIn(flag,args)
            self.assertEqual('--mirror' in args,actor==18)
        with self.assertRaises(AssertionError):plan('../outside')

    def test_other_run_hit_or_no_recovery_cannot_pass_clip_interval(self):
        def row(action,hp,hitby):return dict(mode='2',p1action=str(action),p2action='771',p2hp=str(hp),p2hitby=str(hitby))
        rows=[row(0x101,161,0),row(0x303,150,0x101)]
        verify_interval(rows,1,0x101,11)
        rows[-1]['p2hp']='161'
        with self.assertRaises(AssertionError):verify_interval(rows,1,0x101,11)
