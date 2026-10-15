"""Fail closed on missing, aliased, reordered or incomplete native recovery."""
import re
import unittest
import verify_cpu_action_recovery as pair
import verify_cpu_action_flow as flow
import verify_stock_cpu_uppercut as stock

SONYA = pair.ROOT / 'audit_v411_cpu_action_sonya_cage605'
KANO = pair.ROOT / 'audit_v412_cpu_action_kano_mirror604'
STOCK = pair.ROOT / 'audit_v412_cpu_action_stock_baraka_block601'


def change(log, tag, frame, key=None, value=None, *, contains=None, remove=False, all_matches=False):
    lines = log.splitlines(keepends=True)
    touched=0
    for i, line in enumerate(lines):
        if line.startswith('MK2_CPU_PAIR_' + tag + ' ') and f'frame={frame} ' in line and (
                contains is None or contains in line):
            if remove:
                lines[i]=''
            else:
                lines[i], count = re.subn(r'\b' + key + r'=[^\s]+', key + '=' + value, line)
                assert count == 1
            touched+=1
            if not all_matches:break
    assert touched, 'Mutation must touch actual declared evidence'
    return ''.join(lines)


MUTATIONS = [
    ('missing_attack', 'FLOW', 2588, None, None, 'entry=FF870880', True),
    ('old_action_dirty', 'FLOW', 2588, 'flags', '0010', 'entry=FF870880', False),
    ('setup_has_later_state', 'FLAG', 2588, 'action', '262', 'before=0012', False),
    ('wrong_body_target', 'FLAG', 2588, 'at', '01035000', 'before=0012', False),
    ('wrong_flag_owner', 'FLAG', 2588, 'a13', '0106C620', 'kind=flags', False),
    ('wrong_flag_writer', 'FLAG', 2588, 'pc', 'FF877D40', 'kind=flags', False),
    ('missing_native_assignment', 'ACTION', 2588, None, None, 'after=0106', True),
    ('wrong_native_assignment', 'ACTION', 2588, 'after', '0111', 'after=0106', False),
    ('assignment_prePC', 'ACTION', 2588, 'pc', 'FF83C320', 'after=0106', False),
    ('alias_assignment', 'ACTION', 2588, 'a8', '010350A0', 'after=0106', False),
    ('bad_action_address', 'ACTION', 2588, 'at', '0106C140', 'after=0106', False),
    ('assisted_assignment', 'ACTION', 2588, 'writes', '1', 'after=0106', False),
    ('wrong_role', 'ACTION', 2588, 'state', '1', 'after=0106', False),
    ('cycle_splice', 'ACTION', 2588, 'cycle', '1', 'after=0106', False),
    ('wrong_recovery_arg', 'FLOW', 2609, 'a1', '0000060C', 'entry=FF876350', False),
    ('wrong_recovery_timing', 'ACTION', 2609, 'frame', '2610', 'after=0600', False),
    ('missing_recovery_store', 'ACTION', 2609, None, None, 'after=0600', True),
    ('missing_original_cleanup', 'FLOW', 2621, None, None, 'entry=FF83ED80', True),
    ('missing_action_clear', 'ACTION', 2621, None, None, 'pc=FF83EDD0', True),
    ('body_not_cleared', 'FLAG', 2621, 'after', '0016', 'kind=body', False),
    ('flags_not_cleared', 'FLAG', 2621, 'after', '0010', 'kind=flags', False),
    ('wrong_cleanup_pc', 'FLAG', 2621, 'pc', 'FF83EFA0', 'kind=flags', False),
    ('wrong_clean_walk_state', 'ACTION', 2621, 'after', '0111', 'pc=FF9065D0', False),
    ('wrong_attack_pose', 'FIELD', 2594, 'pose', 'FF030580', None, False),
    ('wrong_recovery_pose', 'FIELD', 2618, 'pose', 'FF030540', None, False),
    ('recovery_cut_short', 'FIELD', 2621, None, None, None, True),
    ('ground_shift', 'FIELD', 2594, 'y', '82', None, False),
    ('own_health_mutation', 'FIELD', 2594, 'hp', '160', None, False),
    ('own_identity_alias', 'FIELD', 2594, 'id', '1', None, False),
    ('late_lock_residue', 'FIELD', 2625, 'flags', '00000010', None, False),
    ('late_throw_residue', 'FIELD', 2625, 'action', '272', None, False),
    ('walk_lock_before_attack', 'FIELD', 2570, 'body', '00000016', None, False),
    ('spoof_clean_completion', 'COMPLETE', 2602, 'flags', '00000000', None, False),
    ('false_complete_victim', 'COMPLETE', 2602, 'vaction', '272', None, False),
    ('missed_held_phase', 'EVENT', 2537, None, None, 'kind=step', True),
    ('pair_damage_missing', 'HEALTH', 2550, 'after', '119', 'slot=2', False),
    ('pair_cleanup_owner_alias', 'FLAG', 2559, 'a13', '0106C620', 'kind=body', False),
    ('victim_cleanup_missing', 'FLAG', 2601, None, None, 'kind=flags', True),
    ('duplicate_field', 'FIELD', 2594, 'id', '18 id=18', None, False),
    ('terminal_field_missing', 'FIELD', 2632, None, None, None, True),
]


class NativeActionRecovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = (SONYA / 'run.log').read_text(encoding='utf-8-sig')
        cls.stock_log = (STOCK / 'run.log').read_text(encoding='utf-8-sig')

    def test_current_sonya_full_followup(self):
        proof = pair.verify(SONYA, 'cage')
        self.assertTrue(proof['passed'], proof)
        self.assertEqual((proof['held_fields'], proof['damage']), (46, 35))
        self.assertEqual(proof['original_uppercut_followup']['clear'], 2621)

    def test_current_kano_pair_only(self):
        proof = pair.verify(KANO, 'kano')
        self.assertTrue(proof['passed'], proof)
        self.assertEqual((proof['held_fields'], proof['damage']), (70, 32))
        self.assertIsNone(proof['original_uppercut_followup'])

    def test_current_stock_full_uppercut(self):
        proof = stock.verify(STOCK)
        self.assertTrue(proof['passed'])
        self.assertEqual(proof['uppercut']['authored_fields'], 33)

    def test_frozen_old_verifier_still_rejects(self):
        import verify_cpu_recovery as old
        self.assertFalse(old.verify_log(self.log, 'cage')['passed'])
        rejected = (pair.ROOT / 'audit_v402_cpu_recovery_cage_boot605/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(pair.verify_log(rejected, 'cage')['passed'])

    def test_native_order_cannot_be_reversed(self):
        lines = self.log.splitlines(keepends=True)
        a = next(i for i, l in enumerate(lines) if l.startswith('MK2_CPU_PAIR_FLAG frame=2588') and 'before=0012' in l)
        b = next(i for i, l in enumerate(lines) if l.startswith('MK2_CPU_PAIR_ACTION frame=2588'))
        lines[a], lines[b] = lines[b], lines[a]
        self.assertFalse(pair.verify_log(''.join(lines), 'cage')['passed'])

    def test_hidden_action_store_rejected(self):
        line = next(l for l in self.log.splitlines(keepends=True) if l.startswith('MK2_CPU_PAIR_ACTION frame=2588'))
        self.assertFalse(pair.verify_log(self.log.replace(line, line + line), 'cage')['passed'])

    def test_stock_without_cleanup_is_not_full_control(self):
        earlier = (pair.ROOT / 'audit_v411_cpu_action_stock_baraka601/run.log').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):
            flow.verify_followup(earlier, 0x01034e90, 0x0106a370, 3, 1643, 2006, 'STOCK_FIELD')

    def test_stock_wrong_native_pose_rejected(self):
        bad = change(self.stock_log, 'STOCK_FIELD', 2069, 'pose', 'FF93F770')
        with self.assertRaises(ValueError):
            flow.verify_followup(bad, 0x01034e90, 0x0106a370, 3, 1643, 2041, 'STOCK_FIELD')

    def test_original_action_writer_operand_required(self):
        original = bytearray((pair.ROOT / 'mk2/mk2-maincpu.bin').read_bytes())
        original[(0xff83c330 - 0xff800000) // 8] ^= 1
        with self.assertRaises(ValueError):
            flow.original_instructions(original)


def mutation_test(case):
    def test(self):
        name, tag, frame, key, value, contains, remove = case
        bad = change(self.log, tag, frame, key, value, contains=contains, remove=remove,
                     all_matches=name=='pair_cleanup_owner_alias')
        self.assertFalse(pair.verify_log(bad, 'cage')['passed'], name)
    return test


for case in MUTATIONS:
    setattr(NativeActionRecovery, 'test_reject_' + case[0], mutation_test(case))


if __name__ == '__main__':
    unittest.main()
