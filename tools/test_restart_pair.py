"""Real restart evidence must prove the entire native close pair, not a summary."""
import re
import unittest
from pathlib import Path

from verify_restart_pair import verify
from verify_post_ending_restart import verify as verify_restart
from check_post_restart_assistance import verify as verify_assistance

ROOT = Path(__file__).resolve().parents[1]


class RestartPairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs = {target: (ROOT / f'audit_v285_native_pair_p2_{target}/run.log').read_text(encoding='utf-8-sig')
                    for target in ('kano', 'sonya')}
        cls.p1logs = {target: (ROOT / folder / 'run.log').read_text(encoding='utf-8-sig') for target, folder in (
            ('kano', 'audit_v285_cross_slot_pair_p1_kano'), ('sonya', 'audit_v285_walking_recovery_p1_sonya'))}

    def reject(self, changed, target='kano'):
        self.assertNotEqual(changed, self.logs[target], 'Mutation did not change the actual fixture')
        self.assertFalse(verify(changed, target, 2)['passed'])

    def change(self, tag, field, value, target='kano', kind=None):
        pattern = r'^MK2_RESTART_PAIR_' + tag + r'[^\r\n]*'
        if kind:
            pattern += r' kind=' + kind + r' [^\r\n]*'
        return re.sub(pattern, lambda line: re.sub(r'(\b' + field + r'=)[^\s]+',
                      lambda item: item[1] + value, line[0], count=1), self.logs[target], count=1, flags=re.M)

    def pose_change(self, field, value, target='kano', elapsed=0):
        log = self.logs[target]
        step = int(re.search(r'^MK2_RESTART_PAIR_EVENT frame=(\d+)[^\r\n]* kind=step ', log, re.M)[1])
        return re.sub(r'^MK2_RESTART_PAIR_STATE frame=' + str(step+1+elapsed) + r' [^\r\n]*',
                      lambda line: re.sub(r'(\b' + field + r'=)[^\s]+', lambda item: item[1] + value,
                                          line[0], count=1), log, count=1, flags=re.M)

    def test_all_four_actual_full_native_pairs(self):
        for side, logs in ((1, self.p1logs), (2, self.logs)):
            for target, log in logs.items():
                result = verify(log, target, side)
                self.assertTrue(result['passed'], result['errors'])
                self.assertTrue(result['completed_owned_cycles'])
                self.assertEqual(result['damage_per_cycle'], 32 if target == 'kano' else 35)
                self.assertEqual(result['memory_writes'], 0)

    def test_all_four_complete_endings_restarts_and_assistance_stop(self):
        for side, logs in ((1, self.p1logs), (2, self.logs)):
            for target, log in logs.items():
                source = 'sonya' if target == 'kano' else 'kano'
                source_side = 2 if side == 2 or target == 'kano' else 1
                result = verify_restart(log, source, target, source_side, side, 'pair')
                self.assertTrue(result['passed'], result['errors'])
                result = verify_assistance(log, source, source_side)
                self.assertTrue(result['passed'], result['errors'])

    def test_original_cpu_walking_after_recovery_is_not_stale_fling(self):
        log = self.p1logs['sonya']
        ready = re.search(r'^MK2_RESTART_PAIR_READY[^\r\n]*', log, re.M)[0]
        self.assertIn('vaction=0303', ready)
        self.assertIn('vvx=00030000', ready)
        self.assertIn('vflags=0000', ready)
        self.assertTrue(verify(log, 'sonya', 1)['passed'])

    def test_walking_exception_still_requires_complete_native_cleanup(self):
        log = self.p1logs['sonya']
        for field, value in (('vaction', '0506'), ('vflags', '0014'), ('vbody', '001A'),
                             ('vvy', 'FFFA0000'), ('vtrail', '01000000'), ('vypos', '1')):
            changed = re.sub(r'(MK2_RESTART_PAIR_READY[^\r\n]* ' + field + r'=)[^\s]+',
                             lambda item: item[1]+value, log, count=1)
            self.assertNotEqual(log, changed)
            self.assertFalse(verify(changed, 'sonya', 1)['passed'])

    def test_cold_probes_cannot_replace_post_ending_proof(self):
        for target in ('kano', 'sonya'):
            log = (ROOT / f'audit_v285_anticipatory_{target}/run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log, target, 1)['passed'])

    def test_original_full_p1_failures_remain_rejected(self):
        for target in ('kano', 'sonya'):
            log = (ROOT / f'audit_v285_native_pair_p1_{target}/run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log, target, 1)['passed'])

    def test_wrong_actual_side_and_target(self):
        self.assertFalse(verify(self.logs['kano'], 'kano', 1)['passed'])
        self.assertFalse(verify(self.logs['kano'], 'sonya', 2)['passed'])

    def test_native_descriptor_cannot_be_substituted(self):
        self.reject(self.change('ROM', 'descriptor', '101,32,63,17,6656,8,0,0,1'))

    def test_missing_real_command(self):
        self.reject(re.sub(r'^MK2_RESTART_PAIR_COMMAND[^\r\n]*\r?\n', '', self.logs['kano'], flags=re.M))

    def test_wrong_command_direction_and_button(self):
        self.reject(self.change('COMMAND', 'forward', 'right'))
        self.reject(self.change('COMMAND', 'button', 'hp'))

    def test_missing_each_actual_native_stage(self):
        for kind in ('parser', 'action', 'intro', 'attack', 'step', 'pulse', 'damage', 'release',
                     'fling', 'velocity', 'own_recovery', 'victim_recovery'):
            with self.subTest(kind=kind):
                self.reject(re.sub(r'^MK2_RESTART_PAIR_EVENT[^\r\n]* kind=' + kind + r' [^\r\n]*\r?\n',
                                   '', self.logs['kano'], flags=re.M))

    def test_wrong_actor_process_identity_and_code(self):
        for field, value in (('actor', '01000000'), ('id', '1'), ('process', '01000000'),
                             ('a13', '01000000'), ('entry', 'FFFFB000'), ('cycle', '99'), ('age', '0')):
            with self.subTest(field=field):
                self.reject(self.change('EVENT', field, value, kind='action'))

    def test_recovery_must_execute_in_actual_victim_process(self):
        self.reject(self.change('EVENT', 'a8', '01000000', kind='victim_recovery'))
        self.reject(self.change('EVENT', 'a13', '01000000', kind='victim_recovery'))

    def test_native_health_writer_must_be_original_store(self):
        self.reject(self.change('HEALTH', 'pc', 'FF807F80'))

    def test_wrong_native_damage_argument(self):
        self.reject(self.change('EVENT', 'value', '00000007', kind='damage'))
        self.reject(self.change('EVENT', 'value', '00000020', target='sonya', kind='damage'), 'sonya')

    def test_missing_native_health_store(self):
        self.reject(re.sub(r'^MK2_RESTART_PAIR_HEALTH[^\r\n]*\r?\n', '', self.logs['kano'], count=1, flags=re.M))

    def test_health_chain_cannot_jump_even_with_each_correct_dose(self):
        count = 0
        def corrupt(line):
            nonlocal count
            count += 1
            if count != 2:
                return line[0]
            return re.sub(r'\b(before|after)=(\d+)', lambda item: item[1]+'='+str(int(item[2])-1), line[0])
        self.reject(re.sub(r'^MK2_RESTART_PAIR_HEALTH[^\r\n]*', corrupt, self.logs['kano'], flags=re.M))

    def test_recovered_health_must_match_actual_native_stores(self):
        self.reject(self.change('READY', 'vhealth', '161'))

    def test_actual_paired_art_and_contacts_are_required(self):
        for field, value in (('pose', 'FF0004E0'), ('vpose', 'FF917430'), ('vxpos', '0'),
                             ('vypos', '0'), ('vaction', '0506'), ('vx', '00010000')):
            with self.subTest(field=field):
                self.reject(self.pose_change(field, value))

    def test_every_original_leg_shake_field_is_checked(self):
        self.reject(self.pose_change('vypos', '0', target='sonya', elapsed=3), 'sonya')

    def test_paired_leg_health_and_push_suppression_are_required(self):
        self.reject(self.pose_change('suppression', '0', target='sonya'), 'sonya')
        self.reject(self.pose_change('vhealth', '160', target='sonya'), 'sonya')

    def test_native_fling_and_signed_velocity_are_required(self):
        for kind, field, value in (('fling', 'a1', 'FFFA0000'), ('fling', 'a3', '00000004'),
                                   ('velocity', 'a0', '00040000'), ('velocity', 'a1', '01060EA0')):
            self.reject(self.change('EVENT', field, value, kind=kind))

    def test_missing_per_field_choreography_or_recovery(self):
        # Remove an intervening field of the actually completed pair, rather
        # than the earlier CPU-interrupted attempt which has no paired poses.
        step = int(re.search(r'^MK2_RESTART_PAIR_EVENT frame=(\d+)[^\r\n]* kind=step ', self.logs['kano'], re.M)[1])
        self.reject(re.sub(r'^MK2_RESTART_PAIR_STATE frame=' + str(step+2) + r' [^\r\n]*\r?\n',
                           '', self.logs['kano'], count=1, flags=re.M))

    def test_missing_ready_state(self):
        self.reject(re.sub(r'^MK2_RESTART_PAIR_READY[^\r\n]*\r?\n', '', self.logs['kano'], flags=re.M))

    def test_unclean_ready_cannot_be_hidden_as_walking(self):
        for field, value in (('y', '1'), ('vx', '00010000'), ('vy', '00010000'), ('flags', '0005'),
                             ('body', '001A'), ('trail', '01000000'), ('vypos', '0'), ('vvy', '00010000'),
                             ('vflags', '0010'), ('vbody', '001A'), ('vtrail', '01000000'),
                             ('vvx', '00040000'), ('writes', '1')):
            self.reject(self.change('READY', field, value))

    def test_slow_fling_cannot_be_called_native_walking(self):
        changed = self.change('READY', 'vvx', '00030000')
        changed = re.sub(r'(MK2_RESTART_PAIR_READY[^\r\n]* vaction=)[^\s]+', r'\g<1>0506', changed)
        self.reject(changed)

    def test_event_and_summary_counts_cannot_be_forged(self):
        self.reject(self.change('EVENT', 'count', '99', kind='step'))
        self.reject(self.change('RESULT', 'steps', '21'))

    def test_observer_error_or_memory_write_cannot_be_hidden(self):
        self.reject(self.logs['kano']+'\nMK2_RESTART_PAIR_ERROR unexpected native state\n')
        self.reject(self.change('HEALTH', 'observer_writes', '1'))

    def test_original_failed_approaches_remain_rejected(self):
        for side in (1, 2):
            for target in ('kano', 'sonya'):
                with self.subTest(side=side, target=target):
                    log = (ROOT / f'audit_v285_pair_p{side}_{target}/run.log').read_text(encoding='utf-8-sig')
                    result = verify(log, target, side)
                    self.assertFalse(result['passed'])
                    self.assertFalse(result['completed_owned_cycles'])

    def test_idle_match_cannot_prove_close_pair(self):
        log = (ROOT / 'audit_v280_p2_to_p2_sonya_kano/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log, 'kano', 2)['passed'])

    def test_projectile_cannot_prove_close_pair(self):
        log = (ROOT / 'audit_v282_start_p2_kano/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log, 'kano', 2)['passed'])

    def test_ball_cannot_prove_close_pair(self):
        log = (ROOT / 'audit_v283_mobility_p2_kano/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log, 'kano', 2)['passed'])

    def test_blade_and_bicycle_cannot_prove_close_pair(self):
        for target, folder in (('kano', 'audit_v284_sequence_p1_kano'),
                               ('sonya', 'audit_v284_settled_sequence_p1_sonya')):
            log = (ROOT / folder / 'run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log, target, 1)['passed'])

    def test_forged_success_summary_does_not_supply_missing_actual_pair(self):
        log = (ROOT / 'audit_v285_pair_p1_kano/run.log').read_text(encoding='utf-8-sig')
        log = re.sub(r'^MK2_RESTART_PAIR_RESULT[^\r\n]*',
                     'MK2_RESTART_PAIR_RESULT pass=true target=kano side=1 move=choke commands=1 '
                     'parsers=1 actions=1 intros=1 attacks=1 steps=22 pulses=4 damage_calls=4 '
                     'releases=1 flings=1 velocities=1 own_recoveries=1 victim_recoveries=1 '
                     'health_stores=4 ready=1 misses=0 errors=0 writes=0', log, flags=re.M)
        self.assertFalse(verify(log, 'kano', 1)['passed'])

    def test_empty_or_truncated_evidence_is_not_completion(self):
        for log in ('', 'MK2_RESTART_PAIR_RESULT pass=true target=kano side=1 move=choke errors=0 writes=0\n'):
            self.assertFalse(verify(log, 'kano', 1)['passed'])


if __name__ == '__main__':
    unittest.main()
