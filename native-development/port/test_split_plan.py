import unittest
from refresh_split_regression import plan


class SplitPlan(unittest.TestCase):
    def test_roles_and_original_controls(self):
        fixtures = plan('current')
        self.assertEqual(len({name for name, _ in fixtures}), 6)
        roles, controls = set(), set()
        for _, args in fixtures:
            self.assertIn('--lao-split-victim', args)
            self.assertNotIn('--body-suck-victim', args)
            control = [a for a in args if a.startswith('--lao-split-control=')]
            if control:
                controls.add(int(control[0].split('=')[1]))
            else:
                roles.add((18 if '--sonya' in args else 17, 1 if '--mirror' in args else 2))
        self.assertEqual(roles, {(17, 1), (17, 2), (18, 1), (18, 2)})
        self.assertEqual(controls, {1, 4})

    def test_escape_rejected(self):
        with self.assertRaises(AssertionError):
            plan('../outside')


if __name__ == '__main__':
    unittest.main()
