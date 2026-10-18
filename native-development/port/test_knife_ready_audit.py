import unittest
from inspect_kintaro_knife_ready import ready_request
from prepare_normal_video_review import sample_frame


class KnifeReadyAuditTests(unittest.TestCase):
    def test_retreat_ball_waits_for_charge_and_actual_stance(self):
        from pathlib import Path
        source = (Path(__file__).parent / 'diagnostics/campaign_probe.lua').read_text()
        branch = source.split('elseif subBallRecovery.kintaroRetreatBall and target==17 and c2==12 and not plan and', 1)[1].split('elseif subBallRecovery.kintaroShortKick', 1)[0]
        for expected in ('bossBallAge<88', '==0x303', 'KS_CAMPAIGN_STANCE_BUTTONS', "set('P1 Low Kick',0)", "set(away,1)"):
            self.assertIn(expected, branch)
        self.assertNotIn(':write_u', source)

    def test_ball_finish_knife_is_low_hp_only_and_does_not_cancel_active_plan(self):
        from pathlib import Path
        here = Path(__file__).parent
        source = (here / 'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('not (subBallRecovery.kintaroBallFinishKnife and u16(0x01060ec0)<=50)', source)
        self.assertIn('(subBallRecovery.kintaroBallFinishKnife and u16(0x01060ec0)<=50)) and target==17 and c2==12 and not plan then', source)
        wrapper = (here.parent / 'baseline/test_wolf_baseline.py').read_text()
        setup = wrapper.split("if '--campaign-kano-kintaro-retreat-ball-finish-knife' in sys.argv:", 1)[1].split('\n    if ', 1)[0]
        self.assertIn("assert '--campaign-kano-kintaro-retreat-ball' in sys.argv", setup)

    def test_short_kick_preserves_native_recovery_and_uses_stance_dispatch(self):
        from pathlib import Path
        source = (Path(__file__).parent / 'diagnostics/campaign_probe.lua').read_text()
        branch = source.split('elseif subBallRecovery.kintaroShortKick and target==17 and c2==12 then', 1)[1].split('elseif subBallRecovery.kintaroReady', 1)[0]
        for expected in ('distance<85', 'distance<=120', 'shortKickAt>=12', '==0x303', 'KS_CAMPAIGN_STANCE_BUTTONS', "set('P1 High Kick',1)"):
            self.assertIn(expected, branch)
        self.assertNotIn("set('P1 Down'", branch)
        self.assertNotIn(':write_u', branch)

    def test_evade_counter_is_opt_in_and_reuses_existing_guard_policy(self):
        from pathlib import Path
        here = Path(__file__).parent
        source = (here / 'diagnostics/campaign_probe.lua').read_text()
        branch = source.split('or (subBallRecovery.kintaroEvadeCounter and target==17)) and c2==12 then', 1)[1].split('elseif subBallRecovery.normalThrow', 1)[0]
        for expected in ('distance<=100', 'n-bossCounterRetry>=36', 'bodyHeight<=96', 'duckButtons', "set(away,1)"):
            self.assertIn(expected, branch)
        self.assertNotIn(':write_u', source)
        wrapper = (here.parent / 'baseline/test_wolf_baseline.py').read_text()
        setup = wrapper.split("if '--campaign-kano-kintaro-evade-counter' in sys.argv:", 1)[1].split('\n    if ', 1)[0]
        self.assertIn("'--campaign-subzero-rfp-duck' in sys.argv", setup)
        self.assertIn('assert not any', setup)

    def test_readiness_requires_actual_stance(self):
        row = dict(phase='fire', ownHP='161', ownAction='771', ownHeight='0',
                   ownFlags='1', bodyHeight='122', distance='175',
                   buttonTable='100', stanceTable='100')
        self.assertTrue(ready_request(row))
        for key, value in [('phase', 'retreat'), ('ownHP', '0'), ('ownAction', '0'),
                           ('ownHeight', '1'), ('ownFlags', '4'), ('bodyHeight', '119'),
                           ('distance', '174'), ('buttonTable', '101')]:
            with self.subTest(key=key):
                self.assertFalse(ready_request(dict(row, **{key: value})))

    def test_contact_frame_is_bounded(self):
        rows = [dict(frame='100', p2hp='161'), dict(frame='101', p2hp='150')]
        self.assertEqual(sample_frame('hp', rows, 90, 150), 11)
        self.assertEqual(sample_frame('throw', rows, 90, 150), 12)
        with self.assertRaises(AssertionError):
            sample_frame('hp', rows, 110, 150)


if __name__ == '__main__':
    unittest.main()
