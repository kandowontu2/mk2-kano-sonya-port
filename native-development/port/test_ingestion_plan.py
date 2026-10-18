import unittest
from refresh_ingestion_regression import plan


class IngestionPlan(unittest.TestCase):
    def test_both_actual_victims_and_physical_sides(self):
        fixtures = plan('current')
        self.assertEqual(len({name for name, _ in fixtures}), 4)
        roles = set()
        for _, args in fixtures:
            self.assertIn('--game', args)
            self.assertIn('--body-suck-victim', args)
            self.assertIn('--sound-candidate', args)
            self.assertFalse(any(a.startswith('--ingestion-control=') for a in args))
            roles.add((18 if '--sonya' in args else 17, 1 if '--mirror' in args else 2))
        self.assertEqual(roles, {(17, 1), (17, 2), (18, 1), (18, 2)})

    def test_path_escape_rejected(self):
        for prefix in ('', '../outside', 'a/b', 'a\\b'):
            with self.assertRaises(AssertionError):
                plan(prefix)


if __name__ == '__main__':
    unittest.main()
