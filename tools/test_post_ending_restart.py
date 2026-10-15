import re
import unittest
from pathlib import Path
from verify_post_ending_restart import verify
from check_post_restart_assistance import verify as verify_assistance

ROOT=Path(__file__).resolve().parents[1]

class PostEndingRestartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={fighter:(ROOT/f'audit_v278_settled_p1_restart_{fighter}_{target}/run.log').read_text(encoding='utf-8-sig')
                  for fighter,target in (('kano','sonya'),('sonya','kano'))}
    def reject(self,changed):
        self.assertNotEqual(changed,self.logs['kano'])
        self.assertFalse(verify(changed,'kano','sonya')['passed'])
    def test_both_actual_complete_towers_and_cross_restarts(self):
        for fighter,target in (('kano','sonya'),('sonya','kano')):
            result=verify(self.logs[fighter],fighter,target)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual(result['restart_assistance'],'none')
            self.assertFalse(result['unassisted_tower_clear_proven'])
    def test_actual_wrong_route_pilot_rejected(self):
        log=(ROOT/'audit_v278_p1_restart_kano_sonya/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log,'kano','sonya')['passed'])
    def test_both_actual_same_character_restarts(self):
        for fighter in ('kano','sonya'):
            log=(ROOT/f'audit_v278_settled_p1_restart_{fighter}_{fighter}/run.log').read_text(encoding='utf-8-sig')
            result=verify(log,fighter,fighter)
            self.assertTrue(result['passed'],result['errors'])
    def test_missing_second_picture(self):
        self.reject(re.sub(r'^MK2_RESTART_PICTURE[^\r\n]* page=2 [^\r\n]*\r?\n','',self.logs['kano'],flags=re.M))
    def test_wrong_owned_ending_identity(self):
        self.reject(self.logs['kano'].replace('page=1 id=17 pc=','page=1 id=1 pc=',1))
    def test_missing_text_page(self):
        self.reject(re.sub(r'^MK2_RESTART_TEXT[^\r\n]* page=2 [^\r\n]*\r?\n','',self.logs['kano'],flags=re.M))
    def test_missing_stage_wins(self):
        self.reject(self.logs['kano'].replace('wins=0:2,1:2,','wins=0:2,1:1,',1))
    def test_diagnostic_stage_jump(self):
        self.reject(self.logs['kano'].replace('diagnostic=false,false','diagnostic=true,false',1))
    def test_wrong_live_new_character(self):
        self.reject(re.sub(r'(MK2_RESTART_MATCH[^\r\n]* id=)18',r'\g<1>1',self.logs['kano'],count=1))
    def test_non_ram_new_actor(self):
        self.reject(re.sub(r'(MK2_RESTART_MATCH[^\r\n]* actor=)[0-9A-F]+',r'\g<1>FF800000',self.logs['kano'],count=1))
    def test_retained_ladder_index(self):
        self.reject(re.sub(r'(MK2_RESTART_MATCH[^\r\n]* stage=)0',r'\g<1>16',self.logs['kano'],count=1))
    def test_wrong_highlight_roster(self):
        self.reject(re.sub(r'(MK2_RESTART_HIGHLIGHT[^\r\n]* roster=)18',r'\g<1>9',self.logs['kano'],count=1))
    def test_new_name_shadow_missing(self):
        self.reject(re.sub(r'^MK2_RESTART_SHADOW[^\r\n]*\r?\n','',self.logs['kano'],flags=re.M))
    def test_wrong_name_shadow_pixels(self):
        self.reject(re.sub(r'(MK2_RESTART_SHADOW[^\r\n]* matched=)\d+',r'\g<1>0',self.logs['kano'],count=1))
    def test_short_new_combat(self):
        self.reject(self.logs['kano'].replace('live=601','live=120'))
    def test_restart_assistance_not_allowed(self):
        self.reject(re.sub(r'(MK2_RESTART_COMPLETE[^\r\n]* restart_writes=)0',r'\g<1>1',self.logs['kano'],count=1))
    def test_actual_error_not_hidden_by_pass(self):
        self.reject(self.logs['kano']+'\nMK2_RESTART_ERROR wrong live actor\n')
    def test_health_assistance_counters_stop_at_completed_tower(self):
        for fighter in ('kano','sonya'):
            for target in ('kano','sonya'):
                log=(ROOT/f'audit_v278_settled_p1_restart_{fighter}_{target}/run.log').read_text(encoding='utf-8-sig')
                result=verify_assistance(log,fighter)
                self.assertTrue(result['passed'],result['errors'])
    def test_post_restart_health_assistance_rejected(self):
        changed=self.logs['kano'].replace('enabled=true writes=3772','enabled=true writes=3773')
        self.assertNotEqual(changed,self.logs['kano'])
        self.assertFalse(verify_assistance(changed,'kano')['passed'])
        changed=self.logs['kano']+'\nMK2KS_DIAGNOSTIC_HEALTH_WRITE frame=999999 stage=0 cpu=3 old=161 new=1\n'
        self.assertFalse(verify_assistance(changed,'kano')['passed'])

if __name__=='__main__':unittest.main()
