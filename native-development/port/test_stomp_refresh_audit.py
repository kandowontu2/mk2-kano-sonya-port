import unittest
from inspect_stomp_refresh import escape_intervals


class StompRefreshAuditTests(unittest.TestCase):
    def rows(self,values):
        return [dict(frame=str(f),ownHeight=str(h),up=str(u)) for f,h,u in values]

    def test_older_jump_must_land_before_new_request(self):
        cases=escape_intervals(self.rows([(1,40,0),(2,0,1),(3,10,0)]))
        self.assertTrue(cases[0]['oldAirThenGroundedUp'])
        self.assertTrue(cases[0]['observedAirAfterUp'])

    def test_gaps_do_not_prove_one_phase_or_airborne_completion(self):
        cases=escape_intervals(self.rows([(1,40,0),(3,0,1),(5,10,0)]))
        self.assertEqual(len(cases),3)
        self.assertFalse(any(c['oldAirThenGroundedUp'] or c['observedAirAfterUp'] for c in cases))

    def test_up_request_is_not_airborne_completion(self):
        case=escape_intervals(self.rows([(1,40,0),(2,0,1)]))[0]
        self.assertTrue(case['oldAirThenGroundedUp'])
        self.assertFalse(case['observedAirAfterUp'])


if __name__=='__main__':unittest.main()
