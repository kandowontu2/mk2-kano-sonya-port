from pathlib import Path
import unittest
from kintaro_variety_policy import next_move


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
        self.assertIn('planAge>=28 and planAge<=31',source)
        self.assertNotIn(':write_u',source)

    def test_spacing_uses_retreat_hysteresis_without_block(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif distance<175 or (subBallRecovery.variedRetreating and distance<220) then',1)[1].split('elseif',1)[0]
        self.assertIn('variedRetreating=true',branch)
        self.assertIn('set(away,1)',branch)
        self.assertNotIn("set('P1 Block'",branch)


if __name__=='__main__':unittest.main()
