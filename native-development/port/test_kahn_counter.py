import unittest
from qualify_kahn_counter import request_window,verify_request,profile

def row(action='770',hp='161',cpu='161',attempt='1',round_number='1'):
    return dict(p1action=action,p1hp=hp,p2hp=cpu,attempt=attempt,round=round_number)

class CounterWindows(unittest.TestCase):
    def test_explicit_kano_and_sonya_profiles(self):
        kano=['--campaign-kano-boss-guard','--campaign-kano-human-prepare','--campaign-subzero-rfp-duck']
        self.assertEqual(profile(kano),(17,True))
        self.assertEqual(profile(['--sonya','--campaign-sonya-kahn-guard']),(18,False))
        with self.assertRaises(AssertionError):profile(kano+['--sonya'])
        with self.assertRaises(AssertionError):profile(['--campaign-kano-boss-guard'])
        with self.assertRaises(AssertionError):profile([])

    def test_contact_mode_requires_exact_wake_and_normal_readiness(self):
        candidate=dict(chargeRoutine='1',contactRecovery='1',velocity='196608',distance='62',
                       ownHeight='0',ownFlags='1',bodyHeight='64',buttonTable='a',duckTable='a',
                       down='1',block='0',enemyWake='ff921fa0')
        verify_request(candidate,True,0xff921fa0)
        for changed in (dict(candidate,enemyWake='ff921fa8'),dict(candidate,ownFlags='5'),
                        dict(candidate,distance='106'),dict(candidate,buttonTable='b')):
            with self.assertRaises(AssertionError):verify_request(changed,True,0xff921fa0)
        with self.assertRaises(AssertionError):verify_request(candidate)

    def test_actual_entry_and_later_health_drop(self):
        result=request_window({100:row(),102:row('263'),106:row('263',cpu='131')},100)
        self.assertTrue(result['uppercutStateEntryWithin8'])
        self.assertEqual(result['opponentHealthDropWithin24'],30)

    def test_existing_tag_is_not_a_new_entry(self):
        self.assertFalse(request_window({100:row('263'),102:row('263')},100)['uppercutStateEntryWithin8'])

    def test_different_attempt_or_round_cannot_supply_a_hit(self):
        for changed in (row('263',cpu='0',attempt='2'),row('263',cpu='0',round_number='2')):
            result=request_window({100:row(),102:changed},100)
            self.assertFalse(result['uppercutStateEntryWithin8'])
            self.assertEqual(result['opponentHealthDropWithin24'],0)

    def test_late_tag_and_health_drop_are_out_of_scope(self):
        result=request_window({100:row(),110:row('263'),126:row('263',cpu='0')},100)
        self.assertFalse(result['uppercutStateEntryWithin8'])
        self.assertEqual(result['opponentHealthDropWithin24'],0)

if __name__=='__main__':unittest.main()
