import unittest
from refresh_lightning_regression import plan

class LightningPlanTests(unittest.TestCase):
    def test_complete_actor_side_coverage_and_exact_family(self):
        cases=plan('current_lightning')
        self.assertEqual(len({name for name,_ in cases}),4)
        self.assertEqual({(18 if '--sonya' in args else 17,1 if '--mirror' in args else 2) for _,args in cases},
                         {(actor,side) for actor in (17,18) for side in (1,2)})
        self.assertTrue(all('--lightning-victim' in args and '--freeze-victim' not in args for _,args in cases))

    def test_path_prefix_rejected(self):
        with self.assertRaises(AssertionError):plan('../outside')
