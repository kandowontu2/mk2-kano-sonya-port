import unittest
from inspect_knife_clearance import windows


def sample(frame,gap=200,hp=161,action=0,mode=2):
    return {k:str(v) for k,v in dict(frame=frame,p1x=0,p2x=gap,p1hp=hp,
        p1action=action,mode=mode,p1char=17,p2char=12).items()}


class KnifeClearanceTests(unittest.TestCase):
    def test_observed_action_gap_is_not_request_gap(self):
        result=windows([dict(frame='10',distance='260')],iter([
            sample(10),sample(26,119,121,529),sample(76,1,0,529)]))[0]
        self.assertEqual(result['requestGap'],260)
        self.assertEqual(result['minimumKnifeGap'],119)
        self.assertEqual(result['minimumPlayerHP'],121)
        self.assertEqual(result['samples'],2)

    def test_noncombat_transition_ends_window(self):
        result=windows([dict(frame='10',distance='260')],iter([
            sample(10),sample(12,mode=5),sample(14,1,0,529)]))[0]
        self.assertEqual(result['samples'],1)
        self.assertIsNone(result['minimumKnifeGap'])


if __name__=='__main__':unittest.main()
