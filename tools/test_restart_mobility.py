"""Actual post-ending mobility fixtures and rejection of misleading evidence."""
import re
import unittest
from pathlib import Path

from verify_restart_mobility import verify
from verify_post_ending_restart import verify as verify_restart
from check_post_restart_assistance import verify as verify_assistance

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    (1, 'kano'): 'audit_v283_retreat_p1_kano_retry',
    (2, 'kano'): 'audit_v283_mobility_p2_kano',
    (1, 'sonya'): 'audit_v283_mobility_p1_sonya',
    (2, 'sonya'): 'audit_v283_extended_p2_sonya_retry',
}


class RestartMobilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs = {key: (ROOT / folder / 'run.log').read_text(encoding='utf-8-sig')
                    for key, folder in CASES.items()}
        cls.ball = cls.logs[2, 'kano']
        cls.square = cls.logs[1, 'sonya']

    def reject(self, changed, target='kano', side=2):
        self.assertTrue(changed != self.logs[side, target], 'Mutation did not change the fixture')
        result = verify(changed, target, side)
        self.assertFalse(result['passed'], result)

    def mutate_event(self, kind, key, value):
        return re.sub(r'^MK2_RESTART_MOBILITY_EVENT[^\r\n]* kind=' + kind + r' [^\r\n]*',
                      lambda event: re.sub(r'(\b' + key + r'=)[^\s]+',
                                           lambda field: field[1] + value, event[0], count=1),
                      self.ball, count=1, flags=re.M)

    def mutate_ready(self, key, value):
        return re.sub(r'(MK2_RESTART_MOBILITY_READY[^\r\n]* ' + key + r'=)[^\s]+',
                      lambda m: m[1] + value, self.ball, count=1)

    def test_all_four_actual_owned_mobility_cycles(self):
        for (side, target), log in self.logs.items():
            with self.subTest(side=side, target=target):
                result = verify(log, target, side)
                self.assertTrue(result['passed'], result['errors'])
                self.assertTrue(result['completed_owned_cycles'])
                self.assertEqual(result['memory_writes'], 0)
                self.assertIn('not_damage_parity_or_other_specials', result['scope'])

    def test_all_four_full_source_towers_restarts_and_assistance_stop(self):
        for (side, target), log in self.logs.items():
            source = 'sonya' if target == 'kano' else 'kano'
            with self.subTest(side=side, target=target):
                result = verify_restart(log, source, target, side, side, 'mobility')
                self.assertTrue(result['passed'], result['errors'])
                result = verify_assistance(log, source, side)
                self.assertTrue(result['passed'], result['errors'])

    def test_idle_or_projectile_match_is_not_mobility_proof(self):
        for folder in ('audit_v280_p2_to_p2_sonya_kano', 'audit_v282_start_p2_kano'):
            log = (ROOT / folder / 'run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log, 'kano', 2)['passed'])

    def test_original_failed_mobility_cases_remain_rejected(self):
        for side, target in ((1, 'kano'), (2, 'sonya')):
            log = (ROOT / f'audit_v283_mobility_p{side}_{target}/run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log, target, side)['passed'])

    def test_disk_full_partial_runs_cannot_pass(self):
        for side, target, folder in (
            (1, 'kano', 'audit_v283_retreat_p1_kano'),
            (2, 'sonya', 'audit_v283_extended_p2_sonya'),
        ):
            log = (ROOT / folder / 'run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log, target, side)['passed'])

    def test_wrong_code_guard(self):
        self.reject(self.ball.replace('parser=FFFFDB00', 'parser=FFFFAC00', 1))

    def test_missing_actual_lk_press(self):
        self.reject(re.sub(r'^MK2_RESTART_MOBILITY_PRESS[^\r\n]*\r?\n', '', self.ball, flags=re.M))

    def test_missing_actual_lk_release(self):
        self.reject(re.sub(r'^MK2_RESTART_MOBILITY_RELEASE[^\r\n]*\r?\n', '', self.ball, flags=re.M))

    def test_false_charge_duration(self):
        self.reject(re.sub(r'(MK2_RESTART_MOBILITY_RELEASE[^\r\n]* hold=)\d+', r'\g<1>80', self.ball, count=1))

    def test_wrong_native_elapsed_instruction(self):
        self.reject(self.ball.replace('pc=FFFFDB70', 'pc=FFFFDB80', 1))

    def test_native_elapsed_threshold_not_met(self):
        self.reject(re.sub(r'(MK2_RESTART_MOBILITY_ELAPSED[^\r\n]* ticks=)\d+', r'\g<1>80', self.ball, count=1))

    def test_missing_native_elapsed_observation(self):
        self.reject(re.sub(r'^MK2_RESTART_MOBILITY_ELAPSED[^\r\n]*\r?\n', '', self.ball, flags=re.M))

    def test_input_memory_mutation_declared(self):
        self.reject(re.sub(r'(MK2_RESTART_MOBILITY_RELEASE[^\r\n]* writes=)0', r'\g<1>1', self.ball, count=1))

    def test_missing_square_command(self):
        self.reject(re.sub(r'^MK2_RESTART_MOBILITY_COMMAND[^\r\n]*\r?\n', '', self.square, count=1, flags=re.M), 'sonya', 1)

    def test_wrong_square_button(self):
        self.reject(self.square.replace('button=hp writes=0', 'button=lp writes=0', 1), 'sonya', 1)

    def test_missing_pipeline_stages(self):
        for kind in ('parser', 'action', 'animation', 'attack', 'recovery'):
            with self.subTest(kind=kind):
                self.reject(re.sub(r'^MK2_RESTART_MOBILITY_EVENT[^\r\n]* kind=' + kind + r' [^\r\n]*\r?\n', '', self.ball, flags=re.M))

    def test_wrong_main_process(self):
        self.reject(self.mutate_event('action', 'a13', '01000000'))

    def test_wrong_actor(self):
        self.reject(self.mutate_event('action', 'actor', '01000000'))

    def test_wrong_character_identity(self):
        self.reject(self.mutate_event('action', 'id', '1'))

    def test_wrong_player_slot(self):
        self.reject(self.mutate_event('action', 'side', '1'))

    def test_wrong_cycle(self):
        self.reject(self.mutate_event('attack', 'cycle', '99'))

    def test_wrong_epoch(self):
        self.reject(self.mutate_event('action', 'age', '99999'))

    def test_wrong_code_entry(self):
        self.reject(self.mutate_event('attack', 'entry', 'FF800000'))

    def test_counter_cannot_replace_event(self):
        self.reject(self.mutate_event('attack', 'count', '99'))

    def test_no_rolling_flight(self):
        self.reject(re.sub(r'(MK2_RESTART_MOBILITY_PHYSICS[^\r\n]* vx=)[0-9A-F]+', r'\g<1>00000000', self.ball))

    def test_missing_physics(self):
        self.reject(re.sub(r'^MK2_RESTART_MOBILITY_PHYSICS[^\r\n]*\r?\n', '', self.ball, flags=re.M))

    def test_missing_grounded_recovery(self):
        self.reject(re.sub(r'^MK2_RESTART_MOBILITY_READY[^\r\n]*\r?\n', '', self.ball, flags=re.M))

    def test_incomplete_recovery_rejected(self):
        for key, value in (('y', '1'), ('vx', '00010000'), ('vy', '00010000'),
                           ('flags', '0005'), ('body', '001A'), ('trail', '01000000'),
                           ('process', '01000000'), ('writes', '1')):
            with self.subTest(key=key):
                self.reject(self.mutate_ready(key, value))

    def test_false_result(self):
        self.reject(self.ball.replace('move=ball commands=1 parsers=1', 'move=ball commands=9 parsers=1', 1))

    def test_observer_error_cannot_be_hidden(self):
        self.reject(self.ball + '\nMK2_RESTART_MOBILITY_ERROR wrong ownership\n')


if __name__ == '__main__':
    unittest.main()
