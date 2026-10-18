import unittest
from refresh_clap_regression import plan

class ClapPlanTests(unittest.TestCase):
    def test_both_own_victims_and_player_sides_with_rejoin(self):
        cases=plan('current_clap')
        self.assertEqual(len({name for name,_ in cases}),4)
        self.assertEqual({(18 if '--sonya' in args else 17,1 if '--mirror' in args else 2) for _,args in cases},
                         {(actor,side) for actor in (17,18) for side in (1,2)})
        self.assertTrue(all('--clap-victim' in args and '--finisher-rejoin' in args and '--freeze-victim' not in args for _,args in cases))

    def test_path_prefix_rejected(self):
        with self.assertRaises(AssertionError):plan('../outside')
