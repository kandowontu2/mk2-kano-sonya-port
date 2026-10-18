import unittest
from inspect_kintaro_ready_counter import ready_request, ready_recovery_request, valid_recovery_approach, ready_finishing_request

class KintaroReadyRequestTests(unittest.TestCase):
    def test_finishing_uppercut_requires_low_boss_hp_and_native_readiness(self):
        row=dict(phase='fire',hp='1',ownHP='1',enemyHP='8',ownHeight='0',enemyHeight='0',ownFlags='1',
                 bodyHeight='90',distance='100',buttonTable='123',duckTable='123')
        self.assertTrue(ready_finishing_request(row))
        self.assertFalse(ready_finishing_request(dict(row,enemyHP='21')))
        self.assertFalse(ready_finishing_request(dict(row,buttonTable='124')))
        self.assertTrue(ready_finishing_request(dict(row,enemyHP='13'),13))
        self.assertFalse(ready_finishing_request(dict(row,enemyHP='14'),13))
    def test_recovery_approach_is_gated_and_never_walks_with_block_or_down(self):
        row=dict(phase='approach',enemyRecovery='1',distance='140',ownHeight='0',enemyHeight='0',
                 ownFlags='1',ownHP='161',toward='1',down='0',block='0')
        self.assertTrue(valid_recovery_approach(row))
        for key,value in (('enemyRecovery','0'),('distance','181'),('distance','104'),('ownHeight','1'),
                          ('ownFlags','4'),('toward','0'),('down','1'),('block','1')):
            self.assertFalse(valid_recovery_approach(dict(row,**{key:value})),key)
    def test_recovery_counter_rejects_ordinary_boss_readiness(self):
        row=dict(phase='fire',hp='1',ownHP='161',ownHeight='0',enemyHeight='0',ownFlags='0',
                 bodyHeight='90',distance='100',buttonTable='123',duckTable='123',enemyRecovery='1')
        self.assertTrue(ready_recovery_request(row))
        self.assertFalse(ready_recovery_request(dict(row,enemyRecovery='0')))
        self.assertFalse(ready_recovery_request(dict(row,distance='105')))
    def test_recovery_gate_uses_linked_native_code_without_guest_writes(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif subBallRecovery.kintaroRecovery and target==17 and c2==12 then',1)[1].split('elseif subBallRecovery.kintaroVertical',1)[0]
        self.assertIn('nativeRoutineActive(proc2',branch)
        self.assertIn('subBallRecovery.bossRecovering and distance<=104',branch)
        self.assertIn("set('P1 Block',0)",branch)
        self.assertNotIn(':write_u',branch)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("boss_origin+boss_local('goro_strike_missed')",wrapper)
        self.assertIn("boss_origin+boss_local('goro_block')",wrapper)
    def test_early_counter_removes_only_the_kano_kintaro_opening_delay(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('(combat>60 or ((subBallRecovery.kintaroEarlyCounter or subBallRecovery.kintaroVaried or subBallRecovery.kintaroVertical or subBallRecovery.kintaroRecovery) and target==17 and c2==12))',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-early-counter' in sys.argv:",1)[1].split('\n    assert ',1)[0]
        self.assertIn("assert '--campaign-kano-kintaro-ready-counter' in sys.argv",setup)
        self.assertNotIn(':write_u',source)
    def test_explicit_tighter_range_cannot_accept_a_far_request(self):
        row=dict(phase='fire',hp='1',ownHP='161',ownHeight='0',enemyHeight='0',ownFlags='0',
                 bodyHeight='90',distance='105',buttonTable='123',duckTable='123')
        self.assertTrue(ready_request(row,115))
        self.assertFalse(ready_request(row,104))
        self.assertTrue(ready_request(dict(row,distance='104'),104))
        self.assertFalse(ready_request(dict(row,distance='85'),84))
        self.assertTrue(ready_request(dict(row,distance='84'),84))
        with self.assertRaises(AssertionError):ready_request(row,200)
    def test_only_real_native_duck_readiness_is_accepted(self):
        row=dict(phase='fire',hp='1',ownHP='161',ownHeight='0',enemyHeight='0',ownFlags='0',
                 bodyHeight='90',distance='100',buttonTable='123',duckTable='123')
        self.assertTrue(ready_request(row))
        for key,value in (('phase','duck'),('hp','0'),('ownHeight','1'),('enemyHeight','1'),
                          ('ownFlags','4'),('bodyHeight','97'),('distance','116'),('buttonTable','124'),('ownHP','0')):
            with self.subTest(key=key):self.assertFalse(ready_request(dict(row,**{key:value})))
