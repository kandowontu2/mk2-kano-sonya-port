import unittest
from inspect_kintaro_variety import validate_decision, retreat_summary, reactive_attack_ages, compare_prefix


class VarietyAuditTests(unittest.TestCase):
    def test_prefix_comparison_detects_pre_override_drift(self):
        rows=[dict(frame=str(f),value='same') for f in (1,2,3)]
        self.assertTrue(compare_prefix(iter(rows),iter(rows),3)['matches'])
        changed=[rows[0],dict(rows[1],value='different'),rows[2]]
        self.assertFalse(compare_prefix(iter(rows),iter(changed),3)['matches'])
        with self.assertRaises(AssertionError):compare_prefix(iter(rows),iter(rows),4)
    def test_reactive_fire_waits_for_eligible_windup_then_pulses_once(self):
        rows=[dict(frame=str(100+age),requestFrame='100',plan='mixkick',age=str(age),
                   windup='1' if age==8 else '0',attackAt=str(8 if age>=8 else -1),
                   hp='0',hk='1' if 8<=age<=11 else '0') for age in range(1,15)]
        self.assertEqual(reactive_attack_ages(rows),{100:8})
        bad=[dict(r) for r in rows];bad[5]['attackAt']='6';bad[5]['hk']='1'
        with self.assertRaises(AssertionError):reactive_attack_ages(bad)
        shifted=[dict(r,frame=str(int(r['frame'])-1)) for r in rows]
        with self.assertRaises(AssertionError):reactive_attack_ages(shifted)
    def row(self):
        return dict(history='0200:0200:0000:0000:0000:0000',kicks='2',punches='0',
                    decision='mixpunch',ownAction='771',ownFlags='1',ownHeight='0',ownHP='161')

    def test_request_must_match_native_queue_not_preferred_attack(self):
        self.assertTrue(validate_decision(self.row()))
        with self.assertRaises(AssertionError):validate_decision(dict(self.row(),decision='mixkick'))
        with self.assertRaises(AssertionError):validate_decision(dict(self.row(),kicks='1'))

    def test_unready_request_cannot_pass(self):
        with self.assertRaises(AssertionError):validate_decision(dict(self.row(),ownFlags='4'))
        self.assertFalse(validate_decision(dict(self.row(),decision='wait')))

    def test_retreat_count_does_not_bridge_unobserved_fields(self):
        rows=[dict(frame=str(f),decision=d) for f,d in
              ((1,'retreat'),(2,'retreat'),(4,'retreat'),(5,'wait'),(6,'retreat'))]
        self.assertEqual(retreat_summary(rows),dict(observedRetreatFields=4,longestContiguousRetreatFields=2))
        with self.assertRaises(AssertionError): retreat_summary(rows+rows)


if __name__=='__main__':unittest.main()
