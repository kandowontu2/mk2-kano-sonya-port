import re
import unittest
from verify_human_air_height import ROOT, verify, verify_log


CASES = ('audit_v405_human_air_kano_sonya_p2_d20', 'audit_v406_human_air_kano_sonya_p1_d8',
         'audit_v406_human_air_kano_sonya_p1_d20', 'audit_v406_human_air_kano_sonya_p2_d8',
         'audit_v408_stock_jax_air_control_p1', 'audit_v408_stock_jax_air_control_p2')


class HumanAirTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
        cls.log = (ROOT / CASES[2] / 'run.log').read_text(encoding='utf-8-sig')
        cls.jax = (ROOT / CASES[4] / 'run.log').read_text(encoding='utf-8-sig')

    def reject(self, tag, field, value, condition=lambda line: True, stock=False):
        log = self.jax if stock else self.log
        lines = log.splitlines()
        for index, line in enumerate(lines):
            if line.startswith('MK2_HUMAN_AIR_' + tag + ' ') and condition(line):
                replacement = re.sub(r'\b' + field + r'=\S+', field + '=' + str(value), line)
                self.assertNotEqual(replacement, line)
                lines[index] = replacement
                break
        else:
            self.fail('Mutation target absent')
        with self.assertRaises((ValueError, KeyError, IndexError)):
            verify_log('\n'.join(lines), 'jax' if stock else 'kano', 'sub_zero' if stock else 'sonya', 1, 20, self.original)

    def test_four_current_kano_catches(self):
        proofs = [verify(ROOT / name) for name in CASES[:4]]
        self.assertEqual(sum(p['held_fields'] for p in proofs), 104)
        self.assertEqual({(p['side'], p['delay']) for p in proofs}, {(1, 8), (1, 20), (2, 8), (2, 20)})
        self.assertEqual({p['catch_y'] for p in proofs}, {-13, 32})
        self.assertTrue(all(p['original_cleanup_stores'] and not p['whole_character_integration_complete'] for p in proofs))

    def test_two_stock_controls(self):
        for name in CASES[4:]:
            p = verify(ROOT / name)
            self.assertEqual(p['damage'], 32)
            self.assertTrue(p['Jax_original_shift_preserved'])

    def test_old_early_overlap_is_not_air_catch(self):
        with self.assertRaises(ValueError):
            verify(ROOT / 'audit_v405_human_air_kano_sonya_p1_d2')

    def test_inapplicable_stock_custom_hud_fixture_rejected(self):
        with self.assertRaises(ValueError):
            verify(ROOT / 'audit_v405_human_air_jax_sub_zero_p1_d20')

    def test_stock_clinch_not_normal_punch_block_proof(self):
        with self.assertRaises(ValueError):
            verify(ROOT / 'audit_v407_stock_jax_air_p1')

    def test_duplicate_segments(self):
        with self.assertRaises(ValueError):
            verify_log(self.log + self.log, 'kano', 'sonya', 1, 20, self.original)

    def test_duplicate_field_key(self):
        self.reject('CAUGHT', 'aid', '17 aid=17')

    def test_assistance(self):
        self.reject('FIELD', 'writes', 1)

    def test_proxy(self):
        self.reject('CAUGHT', 'aid', 11)

    def test_controller_not_human(self):
        self.reject('FIELD', 'vstate', 0)

    def test_owner(self):
        self.reject('FIELD', 'aowner', '010350A0')

    def test_operand_not_instruction(self):
        self.reject('EVENT', 'pc', 'FF8B7010', lambda l: 'entry=FF8B6FF0 ' in l)

    def test_kano_height_shift(self):
        self.reject('FIELD', 'ayraw', '00138000', lambda l: 'frame=1582 ' in l)

    def test_jax_height_erased(self):
        self.reject('FIELD', 'ayraw', 'FFEE8000', lambda l: 'frame=1608 ' in l, stock=True)

    def test_original_position_argument(self):
        self.reject('EVENT', 'a1', '00000020', lambda l: 'frame=1580 ' in l and 'entry=FF83CC20 ' in l and 'a8=01034E90 ' in l)

    def test_missing_native_pose(self):
        self.reject('FIELD', 'apose', 'FF0102C0', lambda l: 'frame=1595 ' in l)

    def test_grip_fraction(self):
        self.reject('FIELD', 'vyraw', 'FFF00000', lambda l: 'frame=1582 ' in l)

    def test_flight_y(self):
        self.reject('FIELD', 'vyraw', 'FFF00000', lambda l: 'frame=1600 ' in l)

    def test_rebound_velocity(self):
        self.reject('FIELD', 'vvx', '00030000', lambda l: 'frame=1608 ' in l)

    def test_damage_writer(self):
        self.reject('HEALTH', 'pc', 'FFFFF000', lambda l: 'frame=1605 ' in l)

    def test_damage_amount(self):
        self.reject('HEALTH', 'after', 129, lambda l: 'frame=1605 ' in l)

    def test_ready_body_lock(self):
        self.reject('OWN_READY', 'abody', '00000016')

    def test_cleanup_writer(self):
        self.reject('LOCK', 'pc', 'FFFFF000', lambda l: 'frame=1632 ' in l and 'role=1 ' in l and 'kind=body ' in l and 'pc=FF83EEB0 ' in l)

    def test_follow_jump_callback(self):
        self.reject('EVENT', 'a6', 'FFFFF800', lambda l: 'entry=FF876660 ' in l and 'frame=1717 ' in l)

    def test_persistent_callback_during_new_jump(self):
        self.reject('FIELD', 'acallback', 'FFFFF800', lambda l: 'frame=1720 ' in l)

    def test_unexpected_after_catch_control(self):
        self.reject('INPUT', 'button', 'High_Punch', lambda l: 'frame=1581 ' in l)

    def test_missing_continuous_field(self):
        changed = '\n'.join(l for l in self.log.splitlines() if not l.startswith('MK2_HUMAN_AIR_FIELD frame=1582 '))
        with self.assertRaises(ValueError):
            verify_log(changed, 'kano', 'sonya', 1, 20, self.original)

    def test_wrong_stock_walk_plan(self):
        self.reject('INPUT', 'button', 'Right', lambda l: 'frame=1713 ' in l and 'slot=1 ' in l, stock=True)


if __name__ == '__main__':
    unittest.main()
