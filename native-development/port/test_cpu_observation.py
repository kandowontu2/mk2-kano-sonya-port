import unittest
from cpu_observation import post_health_fill_observations

def sample(frame,hp,**changes):
    row=dict(frame=str(frame),p1char='0',p2char='17',p1selected='0',p2selected='17',p1hp=str(hp),p2hp=str(hp))
    row.update(changes)
    return row,2

class CPUObservation(unittest.TestCase):
    def test_fill_is_excluded_before_full_health(self):
        accepted,full=post_health_fill_observations([sample(4000,6),sample(4002,161),sample(4004,140)],17)
        self.assertEqual([r['frame'] for r,_ in accepted],['4002','4004'])
        self.assertEqual(full,[4002])

    def test_gap_requires_new_full_health(self):
        accepted,full=post_health_fill_observations([sample(4000,161),sample(4010,140),sample(4012,161)],17)
        self.assertEqual([r['frame'] for r,_ in accepted],['4000','4012'])
        self.assertEqual(full,[4000,4012])

    def test_new_identity_context_requires_full_health(self):
        accepted,_=post_health_fill_observations([sample(4000,161),sample(4002,100,p1char='2'),
                                                sample(4004,161,p1char='2')],17)
        self.assertEqual([r['frame'] for r,_ in accepted],['4000','4004'])

if __name__=='__main__': unittest.main()
