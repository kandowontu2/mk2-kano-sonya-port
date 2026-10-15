"""Fail closed on altered ownership, missing fields, stores, physics and inputs."""
import re
import unittest
import verify_cpu_projectile_followup as v
from verify_cpu_air_runtime import matched_launch

CASES = (
    ('audit_v421_cpu_projectile_kano604', 17, 'block', 'v3'),
    ('audit_v420_cpu_projectile_sonya_cage605', 18, 'block', 'v2'),
    ('audit_v421_cpu_projectile_sonya_duck605', 18, 'duck_miss', 'v3'),
)


def change(log, tag, frame, key=None, value=None, contains=None, remove=False):
    lines = log.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith('MK2_CPU_SHOT_'+tag+' ') and f'frame={frame} ' in line and (
                contains is None or contains in line):
            if remove:
                lines[i] = ''
            else:
                lines[i], count = re.subn(r'\b'+key+r'=[^\s]+', key+'='+value, line)
                assert count == 1, 'Mutation must alter exactly one real field'
            return ''.join(lines)
    raise AssertionError('Mutation target must exist')


# case, label, tag, frame, key, value, optional discriminator, remove
MUTATIONS = [
    (0, 'canonical_entry_missing', 'ENTRY', 2795, None, None, None, True),
    (0, 'fake_actual_entry', 'ENTRY', 2795, 'entry', 'FF9B9470', None, False),
    (0, 'CPU_ID_proxy', 'FIELD', 2810, 'id', '1', None, False),
    (0, 'roster_proxy', 'FIELD', 2810, 'roster', '1', None, False),
    (0, 'wrong_cpu_controller', 'FIELD', 2810, 'state', '1', None, False),
    (0, 'wrong_human_identity', 'FIELD', 2810, 'vid', '18', None, False),
    (0, 'wrong_Main_owner', 'FIELD', 2810, 'owner', '010350A0', None, False),
    (0, 'draw_list_changed', 'FIELD', 2810, 'list', '0105F230', None, False),
    (0, 'paired_field_missing', 'FIELD', 2810, None, None, None, True),
    (0, 'body_pose_wrong', 'FIELD', 2810, 'pose', 'FE82F400', None, False),
    (0, 'body_busy_state_missing', 'FIELD', 2810, 'action', '771', None, False),
    (0, 'recovery_state_wrong', 'FIELD', 2830, 'action', '117', None, False),
    (0, 'body_position_shifted', 'FIELD', 2810, 'xraw', '01D60000', None, False),
    (0, 'body_floor_hover', 'FIELD', 2810, 'y', '81', None, False),
    (0, 'body_moves_while_locked', 'FIELD', 2810, 'vx', '00028000', None, False),
    (0, 'actual_renderer_missing', 'GROUP', 2804, None, None, 'child=0', True),
    (0, 'renderer_wrong_CPU_Main', 'GROUP', 2804, 'main', '0106BF30', 'child=0', False),
    (0, 'setup_store_missing', 'STORE', 2795, None, None, 'after=0016', True),
    (0, 'setup_flags_wrong_writer', 'STORE', 2795, 'pc', 'FF83C340', 'after=0010', False),
    (0, 'action_store_wrong_target', 'STORE', 2795, 'at', '0106C120', 'after=0004', False),
    (0, 'recovery_store_missing', 'STORE', 2820, None, None, 'after=0604', True),
    (0, 'cleanup_action_missing', 'STORE', 2844, None, None, 'before=0604', True),
    (0, 'cleanup_body_missing', 'STORE', 2844, None, None, 'before=0016', True),
    (0, 'cleanup_flags_missing', 'STORE', 2844, None, None, 'before=0010', True),
    (0, 'cleanup_store_wrong_owner', 'STORE', 2844, 'a13', '0106BF30', 'before=0604', False),
    (0, 'ready_still_busy', 'HANDOFF', 2844, 'flags', '00000010', None, False),
    (0, 'native_walk_store_missing', 'STORE', 2844, None, None, 'after=0303', True),
    (0, 'native_walk_wrong_speed', 'FIELD', 2847, 'vx', '00030000', None, False),
    (0, 'native_walk_wrong_raw_physics', 'FIELD', 2847, 'xraw', '01D50000', None, False),
    (0, 'AI_request_proxy_index', 'FLOW', 2795, 'a0', '00000001', 'entry=FF8A5900', False),
    (0, 'AI_route_missing', 'FLOW', 2795, None, None, 'entry=FFFBC000', True),
    (0, 'CPU_flow_wrong_owner', 'FLOW', 2795, 'a8', '010350A0', 'entry=FFFC3800', False),
    (0, 'child_birth_wrong', 'CHILD', 2798, 'frame', '2799', None, False),
    (0, 'child_owner_wrong', 'CHILD', 2798, 'owner', '010350A0', None, False),
    (0, 'child_missing_lifetime_field', 'EFFECT', 2810, None, None, None, True),
    (0, 'child_type_wrong', 'EFFECT', 2810, 'type', '80', None, False),
    (0, 'child_native_velocity_param_wrong', 'EFFECT', 2810, 'velocity_parameter', '00020000', None, False),
    (0, 'knife_intro_wrong_hold', 'EFFECT', 2807, 'pose', 'FF614000', None, False),
    (0, 'knife_intro_moves_early', 'EFFECT', 2810, 'vx', '00080000', None, False),
    (0, 'knife_handoff_wrong', 'EFFECT', 2817, 'xraw', '01C90000', None, False),
    (0, 'knife_flight_wrong_pose', 'EFFECT', 2820, 'pose', 'FF614800', None, False),
    (0, 'knife_flight_wrong_speed', 'EFFECT', 2820, 'vx', '00060000', None, False),
    (0, 'knife_impact_wrong_pose', 'EFFECT', 2833, 'pose', 'FF60C000', None, False),
    (0, 'knife_impact_wrong_state', 'EFFECT', 2833, 'action', '1792', None, False),
    (0, 'knife_impact_should_stop', 'EFFECT', 2833, 'vx', '00020000', None, False),
    (0, 'health_wrong_writer', 'HEALTH', 2828, 'pc', 'FF8366F0', None, False),
    (0, 'health_wrong_child', 'HEALTH', 2828, 'a8', '01034E90', None, False),
    (0, 'chip_wrong_amount', 'HEALTH', 2828, 'after', '145', None, False),
    (0, 'ledger_disagrees', 'FIELD', 2830, 'vhp', '161', None, False),
    (0, 'actual_guard_flag_missing', 'FIELD', 2828, 'vflags', '00000000', None, False),
    (0, 'actual_Block_input_missing', 'INPUT', 2827, 'buttons', 'Neutral', None, False),
    (0, 'child_retirement_missing', 'RETIRE', 2852, None, None, None, True),
    (0, 'child_retirement_wrong_Main', 'RETIRE', 2852, 'main', '0106A370', None, False),
    (0, 'completion_before_retirement', 'COMPLETE', 2853, 'frame', '2845', None, False),
    (0, 'result_stale_child', 'RESULT', 2883, 'live_children', '1', None, False),
    (0, 'terminal_field_missing', 'FIELD', 2883, None, None, None, True),
    (0, 'duplicate_ambiguous_key', 'FIELD', 2810, 'id', '17 id=17', None, False),
    (0, 'assisted_record', 'EFFECT', 2810, 'writes', '1', None, False),
    (0, 'spliced_cycle', 'EFFECT', 2810, 'child_serial', '2', None, False),
    (1, 'ring_release_wrong_hold', 'FIELD', 1861, 'pose', 'FE83DBE0', None, False),
    (1, 'ring_first_handoff_wrong', 'EFFECT', 1871, 'xraw', '02918000', None, False),
    (1, 'ring_flight_wrong_cadence', 'EFFECT', 1874, 'pose', 'FF614AC0', None, False),
    (1, 'ring_burst_should_move', 'EFFECT', 1884, 'vx', '00000000', None, False),
    (1, 'ring_last_burst_missing', 'GROUP', 1900, None, None, 'child=1', True),
    (2, 'miss_duck_input_missing', 'INPUT', 1875, 'buttons', 'Block', None, False),
    (2, 'miss_full_cycle_missing', 'GROUP', 1880, None, None, 'child=1', True),
    (2, 'miss_becomes_impact', 'EFFECT', 1880, 'action', '1280', None, False),
    (2, 'miss_last_lifetime_field_missing', 'EFFECT', 1887, None, None, None, True),
]


class NativeCPUProjectiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs = []
        for name, identity, scenario, version in CASES:
            _, log, original = matched_launch(v.ROOT/name,
                f'mk2ks_cpu_projectile_followup_{version}_probe.lua',
                f'run_cpu_projectile_followup_{version}_probe.ps1')
            cls.logs.append(log)
            cls.original = original

    def test_actual_knife(self):
        proof = v.verify(v.ROOT/CASES[0][0], *CASES[0][1:])
        self.assertEqual((proof['child_fields'], proof['impact_groups'], proof['chip_damage']), (54, 6, 6))
        self.assertTrue(proof['full_flight_cycle'])

    def test_actual_ring_block(self):
        proof = v.verify(v.ROOT/CASES[1][0], *CASES[1][1:])
        self.assertEqual((proof['child_fields'], proof['impact_groups'], proof['chip_damage']), (34, 7, 6))
        self.assertFalse(proof['full_flight_cycle'])  # Contact precedes the other two flight poses.

    def test_actual_ring_duck_miss(self):
        proof = v.verify(v.ROOT/CASES[2][0], *CASES[2][1:])
        self.assertEqual((proof['child_fields'], proof['impact_groups'], proof['chip_damage']), (17, 0, 0))
        self.assertTrue(proof['full_flight_cycle'])
        self.assertFalse(proof['whole_character_integration_complete'])

    def test_rejected_duplicate_field_observers(self):
        for name, identity in [('audit_v419_cpu_projectile_kano604', 17),
                               ('audit_v419_cpu_projectile_sonya_cage605', 18)]:
            log = (v.ROOT/name/'run.log').read_text(encoding='utf-8-sig')
            with self.assertRaises(ValueError):v.verify_log(log, identity, 'block', self.original)

    def test_no_actual_knife_is_not_completion(self):
        log = (v.ROOT/'audit_v420_cpu_projectile_kano604/run.log').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):v.verify_log(log, 17, 'block', self.original)

    def test_compiled_program_mutations(self):
        for start in ('FFFFB000', 'FFFC3800', 'FFFBC000'):
            r = next(r for r in v.records(self.logs[0], 'CODE') if r['start'] == start)
            words = r['words'].split(',');words[0] = '0300'
            altered = change(self.logs[0], 'CODE', 1, 'words', ','.join(words), 'start='+start)
            with self.assertRaises(ValueError):v.verify_log(altered, 17, 'block', self.original)

    def test_original_guard_instruction_mutation(self):
        original = bytearray(self.original)
        original[(0xff837d80-0xff800000)//8] ^= 0x20
        with self.assertRaises(ValueError):v.verify_log(self.logs[0], 17, 'block', original)

    def test_cleanup_order_cannot_be_reversed(self):
        lines = self.logs[0].splitlines(keepends=True)
        a = next(i for i, line in enumerate(lines) if line.startswith('MK2_CPU_SHOT_STORE frame=2844 ') and 'before=0604' in line)
        b = next(i for i, line in enumerate(lines) if line.startswith('MK2_CPU_SHOT_STORE frame=2844 ') and 'before=0016' in line)
        lines[a], lines[b] = lines[b], lines[a]
        with self.assertRaises(ValueError):v.verify_log(''.join(lines), 17, 'block', self.original)

    def test_unobserved_Kano_miss_not_claimed(self):
        with self.assertRaises(ValueError):v.verify_log(self.logs[0], 17, 'duck_miss', self.original)


def mutation_test(case, tag, frame, key, value, contains, remove):
    def test(self):
        altered = change(self.logs[case], tag, frame, key, value, contains, remove)
        with self.assertRaises(ValueError):v.verify_log(altered, CASES[case][1], CASES[case][2], self.original)
    return test


for case, label, tag, frame, key, value, contains, remove in MUTATIONS:
    setattr(NativeCPUProjectiles, 'test_reject_'+label, mutation_test(case, tag, frame, key, value, contains, remove))


if __name__ == '__main__':unittest.main()
