import unittest
from pathlib import Path
from inspect_sub_ball import release_case,charge_observations,counter_case,counter_phase,verify_approach,verify_post_guard

def sample():
    rows={i:dict(frame=str(i),age=str(i),phase='prepare' if i>=86 else 'charge',
                 eligible='1',lk='1',block='0' if i>=86 else '1',down='1',
                 ownHeight='0',ownFlags='1',enemyFlags='1',projectile='0',
                 distance='120',ownAction='771') for i in range(99)}
    for i in range(90,99):rows[i].update(phase='released',lk='0',block='0',down='0')
    rows[92]['ownAction']=str(0x20b)
    return rows

class SubBallRelease(unittest.TestCase):
    def test_post_guard_preserves_release_window_and_resets_each_episode(self):
        rows=[dict(frame=str(i),phase='released',block=str(int(i>=8)),away=str(int(i>=8)),down='0') for i in range(12)]
        self.assertEqual(verify_post_guard(rows),4)
        self.assertEqual(verify_post_guard(rows+[dict(frame='12',phase='charge'),dict(frame='13',phase='released',block='0',away='0',down='0')]),4)
        with self.assertRaises(AssertionError):verify_post_guard([dict(rows[0],block='1')])
        with self.assertRaises(AssertionError):verify_post_guard(rows[:8]+[dict(rows[8],block='0')])

    def test_approach_rejects_projectile_busy_airborne_and_near_opponent(self):
        row=dict(toward='1',lk='1',away='0',block='0',down='0',phase='charge',age='10',
                 ownHeight='0',ownFlags='1',enemyFlags='0',enemyAction='771',projectile='0',distance='180')
        verify_approach(row)
        for change in ({'projectile':'1'},{'ownFlags':'5'},{'enemyFlags':'16'},{'enemyAction':'16'},
                       {'ownHeight':'1'},{'distance':'140'},{'phase':'released'},{'lk':'0'}):
            with self.assertRaises(AssertionError):verify_approach(dict(row,**change))

    def test_recharge_preserves_release_gap_and_real_charge_start(self):
        port=Path(__file__).resolve().parent
        wrapper=(port.parent/'baseline/test_wolf_baseline.py').read_text()
        source=(port/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("if '--campaign-kano-sub-recharge' in sys.argv:\n        assert '--campaign-kano-sub-recovery-ball' in sys.argv",wrapper)
        self.assertIn('subBallRecovery.recharge and subBallReleased and n-subBallReleaseAt>=4',source)
        self.assertIn('if not subBallRecovery.start then subBallRecovery.start=n end',source)
        self.assertIn('subBallStart=subBallRecovery.start;',source)
        self.assertIn('local recoveryBallReady=subBallRecovery.ball and (not subBallRecovery.recharge or age>85)',source)

    def test_busy_enemy_release_requires_explicit_native_recovery(self):
        rows=sample();rows[90]['enemyFlags']='16'
        context=dict(rapidPunch='1',enemyFlags='16',recovering='1',punchesLeft='7',punchAnimation='19')
        self.assertTrue(release_case(rows,90,context)['ballStateObservedWithin8'])
        with self.assertRaises(AssertionError):release_case(rows,90)
        with self.assertRaises(AssertionError):release_case(rows,90,dict(context,recovering='0'))
        rows[90]['enemyFlags']='20'
        with self.assertRaises(AssertionError):release_case(rows,90,context)

    def test_counter_phase_rejects_active_low_final_and_unclassified_states(self):
        context=dict(rapidPunch='1',enemyFlags='16',recovering='0',punchesLeft='3',punchAnimation='19')
        self.assertEqual(counter_phase(context),'early-high-punch')
        for change in ({'rapidPunch':'0'},{'enemyFlags':'0'},{'punchesLeft':'1'},{'punchAnimation':'20'}):
            with self.assertRaises(AssertionError):counter_phase(dict(context,**change))
        self.assertEqual(counter_phase(dict(context,recovering='1',punchAnimation='20')),'native-recovery')

    def test_recovery_counter_requires_explicit_native_recovery(self):
        port=Path(__file__).resolve().parent
        wrapper=(port.parent/'baseline/test_wolf_baseline.py').read_text()
        source=(port/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("if '--campaign-kano-sub-recovery-counter' in sys.argv:\n        assert '--campaign-kano-sub-ball-counter' in sys.argv",wrapper)
        self.assertIn('if highRfp or (subBallRecovery.counter and rapid and recovering) then',source)
        self.assertIn('local highRfp=rapid and not recovering and left>1 and root==0x13',source)

    def test_counter_request_requires_safe_inputs_and_actual_uppercut(self):
        rows=sample()
        rows[85].update(hp='1',block='0',distance='100')
        rows[88]['ownAction']=str(0x107)
        self.assertTrue(counter_case(rows,85)['uppercutStateObservedWithin8'])
        rows[88]['ownAction']='771'
        self.assertFalse(counter_case(rows,85)['uppercutStateObservedWithin8'])
        rows[85]['block']='1'
        with self.assertRaises(AssertionError):counter_case(rows,85)

    def test_ball_counter_requires_native_duck_dispatch_and_no_busy_flags(self):
        port=Path(__file__).resolve().parent
        wrapper=(port.parent/'baseline/test_wolf_baseline.py').read_text()
        source=(port/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("assert '--campaign-kano-sub-adaptive-charge' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv",wrapper)
        branch=source.split('if kanoSubBallCounter and not (recoveryBallReady and recovering) then',1)[1].split('elseif projectile',1)[0]
        self.assertIn('height==0 and (ownFlags&0x1c)==0 and distance<105',branch)
        self.assertIn('bodyHeight<=96 and buttons==duckButtons',branch)
        self.assertIn("set('P1 High Punch',1)",branch)

    def test_adaptive_charge_requires_standing_profile_and_high_rfp_gate(self):
        port=Path(__file__).resolve().parent
        wrapper=(port.parent/'baseline/test_wolf_baseline.py').read_text()
        source=(port/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("if '--campaign-kano-sub-adaptive-charge' in sys.argv:\n        assert '--campaign-kano-sub-standing-charge' in sys.argv",wrapper)
        branch=source.split('if kanoSubAdaptiveCharge then',1)[1].split('local phase=',1)[0]
        self.assertIn('rapid and not recovering and left>1 and root==0x13',branch)
        self.assertIn("set('P1 Down',1);set('P1 Block',0)",branch)
        self.assertIn('enemyAction==0x20c',branch)

    def test_charge_pressure_counts_fields_not_hits(self):
        rows=[dict(phase='charge',down='0',block='1',enemyAction=str(0x507),ownFlags='4'),
              dict(phase='prepare',down='0',block='0',enemyAction='771',ownFlags='1'),
              dict(phase='released',down='1',block='1',enemyAction=str(0x507),ownFlags='4')]
        self.assertEqual(charge_observations(rows),dict(chargingFields=2,chargingDownFields=0,
                         chargingBlockFields=1,chargingEnemyBodySlamFields=1,chargingOwnReactionFields=1))

    def test_standing_charge_is_opt_in_and_ball_scoped(self):
        port=Path(__file__).resolve().parent
        wrapper=(port.parent/'baseline/test_wolf_baseline.py').read_text()
        source=(port/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("if '--campaign-kano-sub-standing-charge' in sys.argv:\n        assert '--campaign-kano-sub-ball' in sys.argv",wrapper)
        self.assertIn("local kanoSubStandingCharge=os.getenv('KS_CAMPAIGN_KANO_SUB_STANDING_CHARGE')=='1'",source)
        branch=source.split('elseif kanoSubBall and target==17 and c2==8 then',1)[1].split('elseif kanoSubJump',1)[0]
        self.assertIn("if not kanoSubStandingCharge then set('P1 Down',1) end",branch)
        self.assertIn("set('P1 Low Kick',1);set(away,1)",branch)
        self.assertIn("if not subBallReleaseAt then set('P1 Block',1) end",branch)

    def test_valid_charge_release_and_actual_state(self):
        self.assertTrue(release_case(sample(),90)['ballStateObservedWithin8'])

    def test_busy_airborne_projectile_and_bad_range_rejected(self):
        for change in ({'ownFlags':'5'},{'ownHeight':'1'},{'enemyFlags':'16'},
                       {'projectile':'1'},{'distance':'79'},{'distance':'261'},{'lk':'1'}):
            rows=sample();rows[90].update(change)
            with self.assertRaises(AssertionError):release_case(rows,90)

    def test_hold_gap_and_short_guard_release_rejected(self):
        rows=sample();rows.pop(30)
        with self.assertRaises(AssertionError):release_case(rows,90)
        rows=sample();rows[87]['phase']='charge'
        with self.assertRaises(AssertionError):release_case(rows,90)

    def test_truncated_window_does_not_prove_rejection(self):
        rows={i:r for i,r in sample().items() if i<=91}
        self.assertIsNone(release_case(rows,90)['ballStateObservedWithin8'])

if __name__=='__main__':unittest.main()
