"""Actual ready-gate and hit/recovery observations, plus tampering negatives."""
import re
import unittest
from pathlib import Path

from verify_projectile_flag_lifecycle import verify

ROOT=Path(__file__).resolve().parents[1]


class ProjectileFlagLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(side,target):(ROOT/('audit_v282_settled_p1_sonya' if (side,target)==(1,'sonya') else f'audit_v282_start_p{side}_{target}')/'run.log').read_text(encoding='utf-8-sig')
                  for side in (1,2) for target in ('kano','sonya')}

    def reject(self,changed):
        self.assertNotEqual(changed,self.logs[1,'kano'])
        self.assertFalse(verify(changed,'kano',1)['passed'])

    def test_all_four_actual_native_lifecycles(self):
        for (side,target),log in self.logs.items():
            result=verify(log,target,side)
            self.assertTrue(result['passed'],result['errors'])
            self.assertGreater(result['native_flag_sets'],0)
            self.assertGreater(result['native_recovery_clears'],0)
            self.assertGreater(result['owned_actions'],0)

    def test_missing_initial_state(self):
        self.reject(re.sub(r'^MK2_PROJECTILE_INITIAL_STATE[^\r\n]*\r?\n','',self.logs[1,'kano'],flags=re.M))

    def test_stale_initial_flag(self):
        self.reject(re.sub(r'(MK2_PROJECTILE_INITIAL_STATE[^\r\n]* flags=)[0-9A-F]+',r'\g<1>0005',self.logs[1,'kano'],count=1))

    def test_wrong_native_writer(self):
        self.reject(self.logs[1,'kano'].replace('writer=native_game','writer=test_assistance',1))

    def test_other_actor_write(self):
        self.reject(re.sub(r'(MK2_PROJECTILE_NATIVE_FLAGS[^\r\n]* actor=)[0-9A-F]+',r'\g<1>01000000',self.logs[1,'kano'],count=1))

    def test_broken_flag_accounting(self):
        self.reject(re.sub(r'(MK2_PROJECTILE_NATIVE_FLAGS[^\r\n]* before=)[0-9A-F]+',r'\g<1>FFFF',self.logs[1,'kano'],count=1))

    def test_missing_real_recovery(self):
        self.reject(re.sub(r'^MK2_PROJECTILE_NATIVE_FLAGS[^\r\n]* pc=FF83EFC0[^\r\n]*\r?\n','',self.logs[1,'kano'],flags=re.M))

    def test_fake_recovery_store(self):
        self.reject(self.logs[1,'kano'].replace('pc=FF83EFC0','pc=FF800000'))

    def test_missing_ready_gate(self):
        self.reject(re.sub(r'^MK2_PROJECTILE_GATE[^\r\n]* at=FF8772F0[^\r\n]*\r?\n','',self.logs[1,'kano'],flags=re.M))

    def test_wrong_action_process(self):
        self.reject(re.sub(r'(MK2_RESTART_PROJECTILE_EVENT[^\r\n]* kind=action[^\r\n]* a13=)[0-9A-F]+',r'\g<1>01000000',self.logs[1,'kano'],count=1))

    def test_zero_write_mask(self):
        self.reject(re.sub(r'(MK2_PROJECTILE_NATIVE_FLAGS[^\r\n]* mask=)[0-9A-F]+',r'\g<1>0000',self.logs[1,'kano'],count=1))


if __name__=='__main__':unittest.main()
