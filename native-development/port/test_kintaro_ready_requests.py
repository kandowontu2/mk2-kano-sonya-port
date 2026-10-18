import unittest
from inspect_kintaro_ready_counter import ready_request

class KintaroReadyRequestTests(unittest.TestCase):
    def test_early_counter_removes_only_the_kano_kintaro_opening_delay(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('(combat>60 or ((subBallRecovery.kintaroEarlyCounter or subBallRecovery.kintaroVaried) and target==17 and c2==12))',source)
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
