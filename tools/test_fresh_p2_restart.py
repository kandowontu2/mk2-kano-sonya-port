"""Fresh P2 START/selection after either player's complete own ending."""
import re
import unittest
from pathlib import Path

from verify_post_ending_restart import verify
from check_post_restart_assistance import verify as assistance

ROOT=Path(__file__).resolve().parents[1]


class FreshP2RestartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(side,fighter,target):
                  (ROOT/f'audit_v280_p{side}_to_p2_{fighter}_{target}/run.log').read_text(encoding='utf-8-sig')
                  for side in (1,2) for fighter in ('kano','sonya') for target in ('kano','sonya')}

    def reject(self,changed):
        self.assertNotEqual(changed,self.logs[2,'kano','sonya'])
        self.assertFalse(verify(changed,'kano','sonya',2,2)['passed'])

    def test_all_eight_actual_fresh_p2_games(self):
        for (side,fighter,target),log in self.logs.items():
            result=verify(log,fighter,target,side,2)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual((result['source_side'],result['new_game_side']),(side,2))
            self.assertFalse(result['unassisted_tower_clear_proven'])

    def test_all_eight_assistance_stops_before_attract(self):
        for (side,fighter,target),log in self.logs.items():
            result=assistance(log,fighter,side)
            self.assertTrue(result['passed'],result['errors'])

    def test_new_p1_evidence_is_not_new_p2(self):
        log=(ROOT/'audit_v279_settled_p2_restart_kano_sonya/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log,'kano','sonya',2,2)['passed'])

    def test_new_p2_evidence_is_not_new_p1(self):
        self.assertFalse(verify(self.logs[2,'kano','sonya'],'kano','sonya',2,1)['passed'])

    def test_wrong_boot_slot(self):
        self.reject(self.logs[2,'kano','sonya'].replace('source_side=2 new_side=2','source_side=2 new_side=1'))

    def test_cpu_on_wrong_slot(self):
        self.reject(self.logs[2,'kano','sonya'].replace('cpu_side=1','cpu_side=2'))

    def test_missing_cpu_side(self):
        self.reject(self.logs[2,'kano','sonya'].replace(' cpu_side=1',''))

    def test_opposite_human_participation_retained(self):
        self.reject(re.sub(r'(MK2_RESTART_CPU[^\r\n]* state=)0',r'\g<1>1',self.logs[2,'kano','sonya'],count=1))

    def test_wrong_new_human_identity(self):
        self.reject(re.sub(r'(MK2_RESTART_MATCH[^\r\n]* id=)18',r'\g<1>1',self.logs[2,'kano','sonya'],count=1))

    def test_wrong_new_cpu_identity(self):
        self.reject(re.sub(r'(MK2_RESTART_CPU[^\r\n]* id=)\d+',r'\g<1>65535',self.logs[2,'kano','sonya'],count=1))

    def test_wrong_new_cpu_schedule(self):
        self.reject(re.sub(r'(MK2_RESTART_CPU[^\r\n]* schedule=)[0-9A-F]+',r'\g<1>FF800000',self.logs[2,'kano','sonya'],count=1))

    def test_wrong_highlight(self):
        self.reject(re.sub(r'(MK2_RESTART_HIGHLIGHT[^\r\n]* roster=)18',r'\g<1>9',self.logs[2,'kano','sonya'],count=1))

    def test_missing_right_lifebar_shadow(self):
        self.reject(re.sub(r'^MK2_RESTART_SHADOW[^\r\n]*\r?\n','',self.logs[2,'kano','sonya'],flags=re.M))

    def test_incorrect_right_lifebar_shadow(self):
        self.reject(re.sub(r'(MK2_RESTART_SHADOW[^\r\n]* matched=)\d+',r'\g<1>0',self.logs[2,'kano','sonya'],count=1))

    def test_short_coverage(self):
        self.reject(self.logs[2,'kano','sonya'].replace('live=601','live=120'))

    def test_memory_assistance_declaration_rejected(self):
        self.reject(re.sub(r'(MK2_RESTART_COMPLETE[^\r\n]* restart_writes=)0',r'\g<1>1',self.logs[2,'kano','sonya'],count=1))


if __name__=='__main__':unittest.main()
