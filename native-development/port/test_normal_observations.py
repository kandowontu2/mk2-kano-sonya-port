import unittest
from inspect_normal_runtime import cells

class NormalObservationTests(unittest.TestCase):
    def test_mirror_roles_are_not_relabelled_as_original_sides(self):
        result=cells([],actors=(18,17))
        self.assertEqual([(r['side'],r['actor']) for r in result[:2]],[(1,18),(2,17)])
        self.assertTrue(all(not r['actionAndLateRecoveryObserved'] for r in result))
    def test_request_without_expected_action_cannot_pass(self):
        rows=[dict(case='hp',age='12',p1action='771',p2action='771',p1shape='1',p2shape='2'),
              dict(case='hp',age='95',p1action='771',p2action='771',p1shape='1',p2shape='2')]
        self.assertFalse(cells(rows)[0]['actionAndLateRecoveryObserved'])
        rows[0]['p1action']='257'
        results=cells(rows)
        self.assertTrue(results[0]['actionAndLateRecoveryObserved'])
        self.assertFalse(results[1]['actionAndLateRecoveryObserved'])
