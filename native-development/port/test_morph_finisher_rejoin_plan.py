import unittest
from refresh_morph_finisher_rejoin import plan

class MorphRejoinPlan(unittest.TestCase):
    def test_exact_supported_kinds_and_both_sides(self):
        fixtures=plan('current')
        self.assertEqual(len({n for n,_,_,_ in fixtures}),8)
        self.assertEqual({(k,s) for _,k,s,_ in fixtures},{(k,s) for k in ('extract','kiss','laser','bubble') for s in (1,2)})
        for _,_,side,args in fixtures:
            self.assertIn('--finisher-morph',args)
            self.assertIn('--finisher-rejoin',args)
            self.assertEqual('--mirror' in args,side==2)

    def test_path_escape_rejected(self):
        with self.assertRaises(AssertionError):plan('../outside')

if __name__=='__main__':unittest.main()
