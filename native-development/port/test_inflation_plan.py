import unittest
from refresh_inflation_regression import plan


class InflationPlan(unittest.TestCase):
    def test_four_actual_roles(self):
        fixtures = plan('current')
        self.assertEqual(len({name for name, _ in fixtures}), 4)
        roles = set()
        for _, args in fixtures:
            self.assertIn('--kitana-kiss-victim', args)
            self.assertNotIn('--body-suck-victim', args)
            self.assertFalse(any(a.startswith('--kitkiss-control=') for a in args))
            roles.add((18 if '--sonya' in args else 17, 1 if '--mirror' in args else 2))
        self.assertEqual(roles, {(17, 1), (17, 2), (18, 1), (18, 2)})

    def test_escape_rejected(self):
        with self.assertRaises(AssertionError):
            plan('../outside')


if __name__ == '__main__':
    unittest.main()
