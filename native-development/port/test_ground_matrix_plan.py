import unittest
from refresh_ground_matrix import plan

class GroundMatrixPlanTests(unittest.TestCase):
    def test_sonya_diagonal_punch_uses_separate_spaced_evidence(self):
        fixtures=plan('spaced_jump',True)
        changed=[]
        for name,args,reuse in fixtures:
            if '--normal-gap=220' in args:
                self.assertIn('--normal-case=flyingpunch',args)
                self.assertIn('_220_',name)
                self.assertFalse(reuse)
                side=int(next(a.split('=')[1] for a in args if a.startswith('--normal-attacker=')))
                actor=((18,17) if '--mirror' in args else (17,18))[side-1]
                self.assertEqual(actor,18)
                changed.append(name)
        self.assertEqual(len(changed),4)
    def test_jump_matrix_covers_all_roles_with_eight_reuses(self):
        fixtures=plan('jump_matrix_test',True)
        self.assertEqual(len(fixtures),32)
        self.assertEqual(len({name for name,_,_ in fixtures}),32)
        self.assertEqual(sum(reuse for _,_,reuse in fixtures),8)
        cells=set()
        for name,args,reuse in fixtures:
            side=int(next(a.split('=')[1] for a in args if a.startswith('--normal-attacker=')))
            actor=((18,17) if '--mirror' in args else (17,18))[side-1]
            move=next(a.split('=')[1] for a in args if a.startswith('--normal-case='))
            cells.add((actor,side,move,'--normal-block' in args))
            if reuse:self.assertTrue(name.startswith('stock_wolf_2219_jump_contact_'))
        self.assertEqual(len(cells),32)
    def test_all_roles_and_six_ground_families_with_twelve_reuses(self):
        fixtures=plan('ground_matrix_test')
        self.assertEqual(len(fixtures),48)
        self.assertEqual(len({name for name,_,_ in fixtures}),48)
        self.assertEqual(sum(reuse for _,_,reuse in fixtures),12)
        cells=set()
        for _,args,_ in fixtures:
            side=int(next(a.split('=')[1] for a in args if a.startswith('--normal-attacker=')))
            actor=((18,17) if '--mirror' in args else (17,18))[side-1]
            move=next(a.split('=')[1] for a in args if a.startswith('--normal-case='))
            cells.add((actor,side,move,'--normal-block' in args))
        self.assertEqual(len(cells),48)
        with self.assertRaises(AssertionError):plan('../outside')
