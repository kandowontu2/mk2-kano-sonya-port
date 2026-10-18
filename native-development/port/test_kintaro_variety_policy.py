from pathlib import Path
import unittest
from kintaro_variety_policy import next_move, air_attack_age


class VarietyPolicyTests(unittest.TestCase):
    def test_finishing_override_requires_explicit_mode_and_low_health(self):
        history=[0x200,0x200,0x201,0x201,0,0]
        self.assertEqual(next_move(history,13,True),'mixkick')
        self.assertEqual(next_move(history,14,True),'readyknife')
        self.assertEqual(next_move(history,13,False),'readyknife')
        with self.assertRaises(AssertionError):next_move(history,None,True)
    def test_switches_before_three_native_queue_repeats(self):
        self.assertEqual(next_move([0]*6),'mixkick')
        self.assertEqual(next_move([0x200,0x200,0,0,0,0]),'mixpunch')
        self.assertEqual(next_move([0x200,0x200,0x201,0x201,0,0]),'readyknife')

    def test_actual_history_not_request_count_selects_move(self):
        self.assertEqual(next_move([0x211,0x211,0x201,0x201,0x200,0x200]),'readyknife')
        self.assertEqual(next_move([0x211,0x211,0x211,0x201,0x201,0x200]),'mixkick')
        with self.assertRaises(AssertionError):next_move([0]*7)

    def test_lua_reads_six_words_and_uses_late_physical_air_attacks(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif subBallRecovery.kintaroVaried and target==17 and c2==12 and not plan then',1)[1].split('elseif subBallRecovery.kintaroRetreatBall',1)[0]
        self.assertIn('for index=0,5 do',branch)
        self.assertIn('variedKicks<2',branch)
        self.assertIn('variedPunches<2',branch)
        self.assertIn('KS_CAMPAIGN_BOSS_HITQ',branch)
        self.assertIn('planAge>=(subBallRecovery.variedAirAttackAge or 28)',source)
        self.assertNotIn(':write_u',source)

    def test_spacing_uses_retreat_hysteresis_without_block(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif not subBallRecovery.kintaroVariedFinish and (distance<175 or (subBallRecovery.variedRetreating and distance<220)) and',1)[1].split('elseif',1)[0]
        self.assertIn('n-subBallRecovery.variedRetreatSince<48',branch)
        self.assertIn('variedRetreating=true',branch)
        self.assertIn('set(away,1)',branch)
        self.assertNotIn("set('P1 Block'",branch)

    def test_close_counter_requires_physical_duck_readiness(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif subBallRecovery.kintaroVariedCounter and (distance<=104',1)[1].split('elseif (distance<175',1)[0]
        for check in ('readyBody<=96','readyButton==subBallRecovery.readyDuck',
                      'n-subBallRecovery.uppercutAt>=6',"set('P1 Down',1)",
                      "set('P1 High Punch',1)","readyPhase='fire'"):
            self.assertIn(check,branch)
        self.assertNotIn(':write_u',branch)

    def test_distance_timing_is_bounded(self):
        self.assertEqual([air_attack_age(d) for d in (0,116,160,192,260)],[10,10,20,28,28])
        with self.assertRaises(AssertionError):air_attack_age(-1)

    def test_stomp_refresh_does_not_count_an_older_airborne_attack(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('if subBallRecovery.kintaroStompRefresh and target==17 then',1)[1].split('else',1)[0]
        self.assertIn('ownHeight>0 and subBallRecovery.stompJumpRequested',branch)
        self.assertIn('ownHeight==0 and not stompJumped',branch)
        self.assertIn("set('P1 Up',1);subBallRecovery.stompJumpRequested=true",branch)
        self.assertIn('stompEscapeLast=-1000;subBallRecovery.stompJumpRequested=false',source)

    def test_stomp_momentum_is_opt_in_and_edge_limited(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('if subBallRecovery.kintaroStompMomentum and target==17 then',1)[1].split('stompEscapeLast=n',1)[0]
        self.assertIn('u32(a+0x40)',branch)
        self.assertIn('stompVelocity>0 and rightDistance>=128',branch)
        self.assertIn('stompVelocity<0 and leftDistance>=128',branch)
        self.assertNotIn(':write_u',branch)

    def test_vertical_kick_is_neutral_jump_not_flip_attack(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split("elseif plan=='upkick' then",1)[1].split("elseif plan=='mixkick'",1)[0]
        self.assertIn("set('P1 Up',1)",branch)
        self.assertIn('planAge>=subBallRecovery.verticalAttackAge',branch)
        self.assertIn('planAge<=subBallRecovery.verticalAttackAge+3',branch)
        self.assertNotIn('planToward',branch)
        self.assertNotIn('set(toward',branch)

    def test_vertical_timing_accounts_for_normal_fixture_pre_jump_delay(self):
        source=(Path(__file__).parent/'diagnostics/normal_probe.lua').read_text()
        self.assertIn("local jumpAge=requested~='' and 20 or 0",source)
        self.assertIn("then attackAge=48 end",source)
        self.assertEqual(48-20,28)

    def test_reactive_air_attack_has_one_windup_trigger_and_bounded_fallback(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('not subBallRecovery.reactiveAirAt and ((planAge>=6 and subBallRecovery.reactiveWindup) or planAge>=28)',source)
        self.assertIn('subBallRecovery.reactiveAirAt=planAge',source)
        self.assertIn('planAge<=subBallRecovery.reactiveAirAt+3',source)
        self.assertIn('KS_KINTARO_UPPERCUT_BEGIN',source)
        self.assertNotIn(':write_u',source)


if __name__=='__main__':unittest.main()
