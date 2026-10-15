import re
import unittest
from pathlib import Path
from verify_p2_campaign import verify

ROOT=Path(__file__).resolve().parents[1]


class NativeP2CampaignTests(unittest.TestCase):
    def setUp(self):
        self.sonya=(ROOT/'audit_v270_p2_campaign_loss_verified_sonya/run.log').read_text(encoding='utf-8-sig')
        self.kano=(ROOT/'audit_v270_p2_campaign_fight_kano/run.log').read_text(encoding='utf-8-sig')

    def test_actual_both_fighters_and_native_round_break(self):
        for name,log in (('sonya',self.sonya),('kano',self.kano)):
            result=verify(log,name)
            self.assertTrue(result['passed'],result['errors'])
        self.assertEqual(verify(self.kano,'kano')['verified_native_round_breaks'],1)

    def test_actual_uncorrected_transition_harness_is_rejected(self):
        for name in ('kano','sonya'):
            log=(ROOT/f'audit_v270_p2_campaign_zone_{name}/run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log,name,True)['passed'])

    def test_actual_both_native_ladder_advances(self):
        for name in ('kano','sonya'):
            log=(ROOT/f'audit_v270_p2_campaign_advance_{name}/run.log').read_text(encoding='utf-8-sig')
            result=verify(log,name,True)
            self.assertTrue(result['passed'],result['errors'])

    def test_wrong_cpu_live_actor_is_rejected(self):
        log=self.sonya.replace('cpu=18:18 human=18:18','cpu=18:17 human=18:18',1)
        self.assertFalse(verify(log,'sonya')['passed'])

    def test_wrong_human_live_actor_is_rejected(self):
        log=self.sonya.replace('human=18:18 flags=','human=18:17 flags=',1)
        self.assertFalse(verify(log,'sonya')['passed'])

    def test_reversed_human_participation_is_rejected(self):
        log=re.sub(r'(MK2_P2_CAMPAIGN_LIVE[^\r\n]*?)states=0,1',r'\1states=1,0',self.sonya,count=1)
        self.assertFalse(verify(log,'sonya')['passed'])

    def test_changed_native_schedule_is_rejected(self):
        log=self.sonya.replace('ids=18,7,4,0,11,1,3,8,17,5,9,2,10,14,6,12,13',
            'ids=17,7,4,0,11,1,3,8,18,5,9,2,10,14,6,12,13')
        self.assertFalse(verify(log,'sonya')['passed'])

    def test_missing_first_live_field_is_rejected(self):
        log=re.sub(r'^MK2_P2_CAMPAIGN_LIVE[^\r\n]*\r?\n','',self.sonya,count=1,flags=re.M)
        self.assertFalse(verify(log,'sonya')['passed'])

    def test_missing_internal_live_field_is_rejected(self):
        rows=re.findall(r'^MK2_P2_CAMPAIGN_LIVE[^\r\n]*',self.sonya,re.M)
        log=self.sonya.replace(rows[50],'',1)
        self.assertFalse(verify(log,'sonya')['passed'])

    def test_round_break_without_actual_constructor_is_rejected(self):
        log=re.sub(r'^MK2_P2_CAMPAIGN_STATE frame=5774[^\r\n]*','',self.kano,flags=re.M)
        self.assertFalse(verify(log,'kano')['passed'])

    def test_position_assistance_is_rejected(self):
        self.assertFalse(verify(self.sonya+'\nMK2_FINISH_POSITION_ASSIST applied','sonya')['passed'])

    def test_lost_campaign_does_not_prove_ladder_advance(self):
        self.assertFalse(verify(self.sonya,'sonya',True)['passed'])

    def test_actual_bounded_native_terminal_losses(self):
        for name in ('kano','sonya'):
            log=(ROOT/f'audit_v273_p2_loss_{name}/run.log').read_text(encoding='utf-8-sig')
            result=verify(log,name)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual(result['verified_native_terminal_losses'],1)

    def test_forged_terminal_ownership_rejected(self):
        log=(ROOT/'audit_v273_p2_loss_kano/run.log').read_text(encoding='utf-8-sig')
        log=re.sub(r'(MK2_P2_CAMPAIGN_TERMINAL[^\r\n]*?)actors=00000000,00000000',r'\1actors=01034E90,00000000',log)
        self.assertFalse(verify(log,'kano')['passed'])

    def test_duplicate_autoboot_campaign_is_rejected(self):
        log=(ROOT/'audit_v273_long_p2_kano/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log,'kano')['passed'])

    def test_actual_reboot_guard_preserves_one_campaign(self):
        log=(ROOT/'audit_v273_p2_reboot_guard_kano/run.log').read_text(encoding='utf-8-sig')
        result=verify(log,'kano')
        self.assertTrue(result['passed'],result['errors'])

    def test_terminal_without_owned_continue_is_rejected(self):
        log=(ROOT/'audit_v273_p2_loss_kano/run.log').read_text(encoding='utf-8-sig')
        log=re.sub(r'^MK2_P2_CAMPAIGN_STATE frame=7105[^\r\n]*\r?\n','',log,flags=re.M)
        self.assertFalse(verify(log,'kano')['passed'])

    def test_changed_native_continue_countdown_is_rejected(self):
        log=(ROOT/'audit_v273_p2_loss_kano/run.log').read_text(encoding='utf-8-sig')
        log=re.sub(r'(MK2_P2_CAMPAIGN_STATE frame=7440 mode=)3',r'\g<1>2',log)
        self.assertFalse(verify(log,'kano')['passed'])


if __name__=='__main__': unittest.main()
