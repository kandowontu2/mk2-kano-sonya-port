"""Actual P2 endings -> fresh P1 games, and rejection of incomplete evidence."""
import re
import unittest
from pathlib import Path

from verify_post_ending_restart import verify
from check_post_restart_assistance import verify as verify_assistance

ROOT=Path(__file__).resolve().parents[1]


class P2PostEndingRestartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(fighter,target):(ROOT/f'audit_v279_settled_p2_restart_{fighter}_{target}/run.log').read_text(encoding='utf-8-sig')
                  for fighter in ('kano','sonya') for target in ('kano','sonya')}

    def reject(self,changed):
        original=self.logs['kano','sonya']
        self.assertNotEqual(changed,original)
        self.assertFalse(verify(changed,'kano','sonya',2)['passed'])

    def test_all_four_actual_p2_endings_to_new_p1_games(self):
        for (fighter,target),log in self.logs.items():
            result=verify(log,fighter,target,2)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual((result['source_side'],result['new_game_side']),(2,1))
            self.assertFalse(result['unassisted_tower_clear_proven'])

    def test_p1_tower_is_not_p2_completion(self):
        log=(ROOT/'audit_v278_settled_p1_restart_kano_sonya/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log,'kano','sonya',2)['passed'])

    def test_p2_tower_is_not_p1_completion(self):
        self.assertFalse(verify(self.logs['kano','sonya'],'kano','sonya',1)['passed'])

    def test_initial_narrower_pilots_do_not_prove_fresh_cpu_acceptance(self):
        for fighter,target in (('kano','sonya'),('sonya','kano')):
            log=(ROOT/f'audit_v279_p2_restart_{fighter}_{target}/run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log,fighter,target,2)['passed'])

    def test_wrong_source_side(self):
        self.reject(self.logs['kano','sonya'].replace('source_side=2 new_side=1','source_side=1 new_side=1'))

    def test_missing_native_p2_win(self):
        self.reject(re.sub(r'^MK2_P2_TOWER_WIN[^\r\n]*\r?\n','',self.logs['kano','sonya'],count=1,flags=re.M))

    def test_wrong_p2_human_identity(self):
        self.reject(re.sub(r'(MK2_P2_TOWER_LIVE[^\r\n]* human=17:)17',r'\g<1>1',self.logs['kano','sonya'],count=1))

    def test_missing_p2_completed_ending(self):
        self.reject(re.sub(r'^MK2_P2_TOWER_COMPLETED[^\r\n]*\r?\n','',self.logs['kano','sonya'],flags=re.M))

    def test_wrong_completion_field(self):
        self.reject(re.sub(r'(MK2_P2_TOWER_COMPLETED frame=)\d+',r'\g<1>99999',self.logs['kano','sonya'],count=1))

    def test_missing_own_second_picture(self):
        self.reject(re.sub(r'^MK2_RESTART_PICTURE[^\r\n]* page=2 [^\r\n]*\r?\n','',self.logs['kano','sonya'],flags=re.M))

    def test_wrong_ending_owner(self):
        self.reject(self.logs['kano','sonya'].replace('page=1 id=17 pc=','page=1 id=1 pc=',1))

    def test_wrong_new_game_actor(self):
        self.reject(re.sub(r'(MK2_RESTART_MATCH[^\r\n]* id=)18',r'\g<1>1',self.logs['kano','sonya'],count=1))

    def test_wrong_new_game_stage(self):
        self.reject(re.sub(r'(MK2_RESTART_MATCH[^\r\n]* stage=)0',r'\g<1>16',self.logs['kano','sonya'],count=1))

    def test_retained_p2_human_participation(self):
        self.reject(re.sub(r'(MK2_RESTART_CPU[^\r\n]* state=)0',r'\g<1>1',self.logs['kano','sonya'],count=1))

    def test_wrong_fresh_cpu_identity(self):
        self.reject(re.sub(r'(MK2_RESTART_CPU[^\r\n]* id=)\d+',r'\g<1>65535',self.logs['kano','sonya'],count=1))
        self.reject(re.sub(r'(MK2_RESTART_CPU[^\r\n]* schedule=)[0-9A-F]+',r'\g<1>FF800000',self.logs['kano','sonya'],count=1))

    def test_missing_fresh_cpu_coverage(self):
        self.reject(re.sub(r'^MK2_RESTART_CPU[^\r\n]*\r?\n','',self.logs['kano','sonya'],flags=re.M))

    def test_wrong_highlight(self):
        self.reject(re.sub(r'(MK2_RESTART_HIGHLIGHT[^\r\n]* roster=)18',r'\g<1>9',self.logs['kano','sonya'],count=1))

    def test_missing_name_shadow(self):
        self.reject(re.sub(r'^MK2_RESTART_SHADOW[^\r\n]*\r?\n','',self.logs['kano','sonya'],flags=re.M))

    def test_insufficient_live_fields(self):
        self.reject(self.logs['kano','sonya'].replace('live=601','live=120'))

    def test_no_health_assistance_after_each_actual_attract(self):
        for (fighter,target),log in self.logs.items():
            result=verify_assistance(log,fighter,2)
            self.assertTrue(result['passed'],result['errors'])

    def test_late_health_assistance_rejected(self):
        # Keep all declared/event counters EXACTLY correct; only move a real
        # write beyond attract. This must fail chronology, not just accounting.
        changed=re.sub(r'(MK2_P2_TOWER_HEALTH frame=)\d+',r'\g<1>999999',self.logs['kano','sonya'],count=1)
        self.assertNotEqual(changed,self.logs['kano','sonya'])
        self.assertFalse(verify_assistance(changed,'kano',2)['passed'])

    def test_health_event_omission_rejected(self):
        changed=re.sub(r'^MK2_P2_TOWER_HEALTH[^\r\n]*\r?\n','',self.logs['kano','sonya'],count=1,flags=re.M)
        self.assertNotEqual(changed,self.logs['kano','sonya'])
        self.assertFalse(verify_assistance(changed,'kano',2)['passed'])

    def test_invalid_health_write_rejected_with_correct_counts(self):
        changed=re.sub(r'(MK2_P2_TOWER_HEALTH[^\r\n]* new=)\d+',r'\g<1>0',self.logs['kano','sonya'],count=1)
        self.assertNotEqual(changed,self.logs['kano','sonya'])
        self.assertFalse(verify_assistance(changed,'kano',2)['passed'])


if __name__=='__main__':unittest.main()
