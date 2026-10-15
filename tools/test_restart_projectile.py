"""Owned native projectile command pipelines after actual own endings."""
import re
import unittest
from pathlib import Path

from verify_restart_projectile import verify
from verify_post_ending_restart import verify as verify_restart
from check_post_restart_assistance import verify as verify_assistance

ROOT=Path(__file__).resolve().parents[1]


class RestartProjectileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(side,target):(ROOT/('audit_v282_settled_p1_sonya' if (side,target)==(1,'sonya') else f'audit_v282_start_p{side}_{target}')/'run.log').read_text(encoding='utf-8-sig')
                  for side in (1,2) for target in ('kano','sonya')}

    def reject(self,changed):
        self.assertNotEqual(changed,self.logs[1,'kano'])
        self.assertFalse(verify(changed,'kano',1)['passed'])

    def test_all_four_actual_owned_projectile_pipelines(self):
        for (side,target),log in self.logs.items():
            result=verify(log,target,side)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual(result['memory_writes'],0)
            self.assertTrue(all(count>0 for count in result['native_pipeline_counts'].values()))

    def test_all_four_complete_source_towers_and_restarts(self):
        for (side,target),log in self.logs.items():
            source='sonya' if target=='kano' else 'kano'
            result=verify_restart(log,source,target,side,side,'projectile')
            self.assertTrue(result['passed'],result['errors'])
            result=verify_assistance(log,source,side)
            self.assertTrue(result['passed'],result['errors'])

    def test_idle_restart_does_not_prove_projectile_activation(self):
        log=(ROOT/'audit_v280_p2_to_p2_sonya_kano/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log,'kano',2)['passed'])

    def test_failed_late_and_neutral_attempts_remain_rejected(self):
        for prefix in ('audit_v281_restart_projectile','audit_v282_native_gates','audit_v282_neutral'):
            for side in (1,2):
                log=(ROOT/f'{prefix}_p{side}_kano/run.log').read_text(encoding='utf-8-sig')
                self.assertFalse(verify(log,'kano',side)['passed'])

    def test_wrong_actual_code_guard(self):
        self.reject(self.logs[1,'kano'].replace('opcode=574A','opcode=0000',1))

    def test_missing_actual_command(self):
        self.reject(re.sub(r'^MK2_RESTART_PROJECTILE_COMMAND[^\r\n]*\r?\n','',self.logs[1,'kano'],count=1,flags=re.M))

    def test_wrong_command_button(self):
        self.reject(self.logs[1,'kano'].replace('button=hp writes=0','button=lp writes=0',1))

    def test_command_memory_mutation_declared(self):
        self.reject(self.logs[1,'kano'].replace('button=hp writes=0','button=hp writes=1',1))

    def test_declared_plan_does_not_replace_actual_input_events(self):
        self.reject(self.logs[1,'kano']+'\nMK2_RESTART_PROJECTILE_PLAN first=60 interval=160 commands=3 writes=0\n')

    def test_missing_parser_event(self):
        self.reject(re.sub(r'^MK2_RESTART_PROJECTILE_EVENT[^\r\n]* kind=parser [^\r\n]*\r?\n','',self.logs[1,'kano'],flags=re.M))

    def test_missing_action_event(self):
        self.reject(re.sub(r'^MK2_RESTART_PROJECTILE_EVENT[^\r\n]* kind=action [^\r\n]*\r?\n','',self.logs[1,'kano'],flags=re.M))

    def test_missing_animation_event(self):
        self.reject(re.sub(r'^MK2_RESTART_PROJECTILE_EVENT[^\r\n]* kind=animation [^\r\n]*\r?\n','',self.logs[1,'kano'],flags=re.M))

    def test_another_slot_cannot_claim_owned_action(self):
        self.reject(re.sub(r'(MK2_RESTART_PROJECTILE_EVENT[^\r\n]* kind=action side=)1',r'\g<1>2',self.logs[1,'kano'],count=1))

    def test_another_character_cannot_claim_owned_action(self):
        self.reject(re.sub(r'(MK2_RESTART_PROJECTILE_EVENT[^\r\n]* kind=action side=1 id=)17',r'\g<1>1',self.logs[1,'kano'],count=1))

    def test_another_actor_cannot_claim_owned_action(self):
        self.reject(re.sub(r'(MK2_RESTART_PROJECTILE_EVENT[^\r\n]* kind=action[^\r\n]* actor=)[0-9A-F]+',r'\g<1>01000000',self.logs[1,'kano'],count=1))

    def test_wrong_action_entry(self):
        self.reject(re.sub(r'(MK2_RESTART_PROJECTILE_EVENT[^\r\n]* kind=action[^\r\n]* entry=)[0-9A-F]+',r'\g<1>FF800000',self.logs[1,'kano'],count=1))

    def test_wrong_process_address(self):
        self.reject(re.sub(r'(MK2_RESTART_PROJECTILE_EVENT[^\r\n]* process=)[0-9A-F]+',r'\g<1>FF800000',self.logs[1,'kano'],count=1))

    def test_wrong_epoch(self):
        self.reject(re.sub(r'(MK2_RESTART_PROJECTILE_EVENT[^\r\n]* age=)\d+',r'\g<1>99999',self.logs[1,'kano'],count=1))

    def test_declared_success_does_not_hide_runtime_error(self):
        self.reject(self.logs[1,'kano']+'\nMK2_RESTART_PROJECTILE_ERROR wrong actual ownership\n')


if __name__=='__main__':unittest.main()
