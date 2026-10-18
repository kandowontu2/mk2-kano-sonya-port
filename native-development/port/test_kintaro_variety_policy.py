from pathlib import Path
import unittest
from kintaro_variety_policy import next_move, air_attack_age


class VarietyPolicyTests(unittest.TestCase):
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
        branch=source.split('elseif (distance<175 or (subBallRecovery.variedRetreating and distance<220)) and',1)[1].split('elseif',1)[0]
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


if __name__=='__main__':unittest.main()
