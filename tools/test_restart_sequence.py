"""Actual post-ending blade/bicycle fixtures and negative ownership/cleanup checks."""
import re
import unittest
from pathlib import Path

from verify_restart_sequence import verify
from verify_post_ending_restart import verify as verify_restart
from check_post_restart_assistance import verify as verify_assistance

ROOT = Path(__file__).resolve().parents[1]
CASES = {(1, 'kano'): 'audit_v284_sequence_p1_kano', (2, 'kano'): 'audit_v284_sequence_p2_kano',
         (1, 'sonya'): 'audit_v284_settled_sequence_p1_sonya', (2, 'sonya'): 'audit_v284_sequence_p2_sonya'}


class RestartSequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs = {key: (ROOT / folder / 'run.log').read_text(encoding='utf-8-sig') for key, folder in CASES.items()}
        cls.blade, cls.bike = cls.logs[1, 'kano'], cls.logs[2, 'sonya']

    def reject(self, log, target='kano', side=1):
        self.assertTrue(log != self.logs[side, target], 'Mutation did not change the fixture')
        self.assertFalse(verify(log, target, side)['passed'])

    def event(self, kind, field, value):
        return re.sub(r'^MK2_RESTART_SEQUENCE_EVENT[^\r\n]* kind=' + kind + r' [^\r\n]*',
                      lambda event: re.sub(r'(\b' + field + r'=)[^\s]+', lambda item: item[1] + value, event[0], count=1),
                      self.blade, count=1, flags=re.M)

    def test_all_four_owned_sequence_pipelines(self):
        for (side, target), log in self.logs.items():
            with self.subTest(side=side, target=target):
                result = verify(log, target, side)
                self.assertTrue(result['passed'], result['errors'])
                self.assertTrue(result['completed_owned_cycles'])
                self.assertEqual(result['memory_writes'], 0)
                self.assertIn('not_damage_parity_or_other_specials', result['scope'])

    def test_all_four_full_endings_restarts_and_health_assistance_stop(self):
        for (side, target), log in self.logs.items():
            source = 'sonya' if target == 'kano' else 'kano'
            with self.subTest(side=side, target=target):
                result = verify_restart(log, source, target, side, side, 'sequence')
                self.assertTrue(result['passed'], result['errors'])
                result = verify_assistance(log, source, side)
                self.assertTrue(result['passed'], result['errors'])

    def test_interrupted_original_p1_bicycle_remains_rejected(self):
        log = (ROOT / 'audit_v284_sequence_p1_sonya/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log, 'sonya', 1)['passed'])

    def test_idle_and_other_specials_do_not_prove_sequence(self):
        for folder in ('audit_v280_p2_to_p2_sonya_kano', 'audit_v282_start_p2_kano', 'audit_v283_mobility_p2_kano'):
            log = (ROOT / folder / 'run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log, 'kano', 2)['passed'])

    def test_wrong_native_guard(self):
        self.reject(self.blade.replace('intro=FFF8E800', 'intro=FF000000', 1))

    def test_missing_actual_command(self):
        self.reject(re.sub(r'^MK2_RESTART_SEQUENCE_COMMAND[^\r\n]*\r?\n', '', self.blade, count=1, flags=re.M))

    def test_timing_plan_cannot_replace_actual_events(self):
        self.reject(self.blade + '\nMK2_RESTART_SEQUENCE_PLAN first=60 interval=180 commands=3 writes=0\n')

    def test_wrong_input_button(self):
        self.reject(self.blade.replace('button=hp writes=0', 'button=lp writes=0', 1))

    def test_input_memory_mutation(self):
        self.reject(self.blade.replace('button=hp writes=0', 'button=hp writes=1', 1))

    def test_missing_each_native_stage(self):
        for kind in ('parser', 'action', 'intro', 'attack', 'effect', 'step', 'recovery'):
            with self.subTest(kind=kind):
                self.reject(re.sub(r'^MK2_RESTART_SEQUENCE_EVENT[^\r\n]* kind=' + kind + r' [^\r\n]*\r?\n', '', self.blade, flags=re.M))

    def test_wrong_main_process(self):
        self.reject(self.event('action', 'a13', '01000000'))

    def test_wrong_actor(self):
        self.reject(self.event('attack', 'actor', '01000000'))

    def test_wrong_identity(self):
        self.reject(self.event('action', 'id', '1'))

    def test_wrong_side(self):
        self.reject(self.event('intro', 'side', '2'))

    def test_wrong_epoch(self):
        self.reject(self.event('effect', 'age', '99999'))

    def test_wrong_cycle(self):
        self.reject(self.event('step', 'cycle', '99'))

    def test_wrong_code_entry(self):
        self.reject(self.event('attack', 'entry', 'FFFFEC00'))

    def test_event_count_cannot_be_fabricated(self):
        self.reject(self.event('effect', 'count', '99'))

    def test_missing_actual_live_attached_effect(self):
        self.reject(re.sub(r'(MK2_RESTART_SEQUENCE_STATE[^\r\n]* trail=)[0-9A-F]+', r'\g<1>00000000', self.blade))

    def test_missing_live_bicycle_motion(self):
        self.reject(re.sub(r'(MK2_RESTART_SEQUENCE_STATE[^\r\n]* vx=)[0-9A-F]+', r'\g<1>00000000', self.bike), 'sonya', 2)

    def test_hit_reaction_cannot_substitute_for_bicycle_flight(self):
        self.reject(re.sub(r'(MK2_RESTART_SEQUENCE_STATE[^\r\n]* action=)(0204|0214|0611)', r'\g<1>0503', self.bike), 'sonya', 2)

    def test_missing_ready_state(self):
        self.reject(re.sub(r'^MK2_RESTART_SEQUENCE_READY[^\r\n]*\r?\n', '', self.blade, flags=re.M))

    def test_incomplete_grounded_flag_effect_cleanup(self):
        for field, value in (('y', '1'), ('vx', '00010000'), ('vy', '00010000'), ('flags', '0005'),
                             ('body', '001A'), ('trail', '01000000'), ('process', '01000000'), ('writes', '1')):
            with self.subTest(field=field):
                changed = re.sub(r'(MK2_RESTART_SEQUENCE_READY[^\r\n]* ' + field + r'=)[^\s]+',
                                 lambda item: item[1] + value, self.blade, count=1)
                self.reject(changed)

    def test_result_counts_must_match_events(self):
        self.reject(self.blade.replace('move=blade commands=3 parsers=3', 'move=blade commands=9 parsers=3', 1))

    def test_runtime_error_cannot_be_hidden(self):
        self.reject(self.blade + '\nMK2_RESTART_SEQUENCE_ERROR wrong actual owned action\n')


if __name__ == '__main__':
    unittest.main()
