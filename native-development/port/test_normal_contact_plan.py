import unittest
from refresh_normal_contact import plan

class NormalContactPlanTests(unittest.TestCase):
    def test_basic_forty_cells_reuse_six_correct_pilot_paths(self):
        fixtures=plan('basic_contact_test',True)
        self.assertEqual(len(fixtures),40)
        self.assertEqual(len({name for name,_,_ in fixtures}),40)
        self.assertEqual(sum(reuse for _,_,reuse in fixtures),6)
        self.assertTrue(any(name=='stock_wolf_2219_normal_basic_lk_hit_pilot' and reuse for name,_,reuse in fixtures))
        self.assertTrue(any('--normal-case=hp' in args and '--normal-gap=90' in args and not reuse for _,args,reuse in fixtures))
        cells=set()
        for _,args,_ in fixtures:
            side=int(next(a.split('=')[1] for a in args if a.startswith('--normal-attacker=')))
            actor=((18,17) if '--mirror' in args else (17,18))[side-1]
            move=next(a.split('=')[1] for a in args if a.startswith('--normal-case='))
            gap=int(next((a.split('=')[1] for a in args if a.startswith('--normal-gap=')),'70'))
            cells.add((actor,side,move,gap,'--normal-block' in args))
        self.assertEqual(len(cells),40)
    def test_sixteen_cells_four_immutable_reuses(self):
        fixtures=plan('contact_test')
        self.assertEqual(len(fixtures),16)
        self.assertEqual(len({name for name,_,_ in fixtures}),16)
        self.assertEqual(sum(reuse for _,_,reuse in fixtures),4)
        for _,args,_ in fixtures:
            self.assertIn('--normal-case=hk',args)
            self.assertIn('--sound-candidate',args)
        with self.assertRaises(AssertionError):plan('../outside')
