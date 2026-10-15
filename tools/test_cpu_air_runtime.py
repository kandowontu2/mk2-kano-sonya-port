import re
import unittest
from verify_cpu_air_runtime import ROOT, verify, verify_log, verify_y_provenance
from verify_cpu_air_counter import verify_compiled


class AirRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = (ROOT / 'audit_v401_cpu_air_kano_jump604/run.log').read_text(encoding='utf-8-sig')
        cls.original = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()

    def reject(self, tag, field, value, condition=lambda line: True):
        lines = self.log.splitlines()
        for index, line in enumerate(lines):
            if line.startswith('MK2_CPU_AIR_' + tag + ' ') and condition(line):
                changed = re.sub(r'\b' + field + r'=\S+', field + '=' + str(value), line)
                self.assertNotEqual(changed, line)
                lines[index] = changed
                break
        else:
            self.fail('Mutation target missing')
        with self.assertRaises((ValueError, KeyError, IndexError)):
            verify_log('\n'.join(lines), 'kano', self.original)

    def test_current_mirror_catch(self):
        proof = verify(ROOT / 'audit_v401_cpu_air_kano_jump604')
        self.assertEqual((proof['paired_fields'], proof['held_fields'], proof['native_callback_fields']), (65, 26, 31))
        self.assertFalse(proof['whole_character_integration_complete'])

    def test_current_sonya_victim(self):
        proof = verify(ROOT / 'audit_v401_cpu_air_sonya_jump604')
        self.assertEqual(proof['damage'], 16)
        self.assertFalse(proof['cleanup_store_provenance'])

    def test_actual_sonya_native_floor_store(self):
        self.assertTrue(verify_y_provenance(ROOT / 'audit_v403_cpu_air_sonya_y604')['original_impact_floor_word_store'])

    def test_old_guard_padding_fails(self):
        log = (ROOT / 'audit_v397_cpu_air_liu_jump604/run.log').read_text(encoding='utf-8-sig')
        # Preserve only the first observer segment to test the compiled bug,
        # separate from this file's later duplicate observer-ROM rejection.
        start = log.find('MK2_CPU_AIR_ROM start=FF9BEEF0', 1)
        with self.assertRaises(ValueError):
            verify_compiled(log[:start] if start > 0 else log)

    def test_old_rehit_and_height_candidate_not_current(self):
        with self.assertRaises(ValueError):
            verify(ROOT / 'audit_v399_cpu_air_sonya_jump604')

    def test_duplicate_observer_segment(self):
        with self.assertRaises(ValueError):
            verify_log(self.log + self.log, 'kano', self.original)

    def test_missing_owned_field(self):
        log = '\n'.join(line for line in self.log.splitlines() if not line.startswith('MK2_CPU_AIR_FIELD frame=1672 '))
        with self.assertRaises(ValueError):
            verify_log(log, 'kano', self.original)

    def test_missing_height_entry(self):
        log = '\n'.join(line for line in self.log.splitlines() if not ('MK2_CPU_AIR_EVENT' in line and 'entry=FFFCAC00 ' in line))
        with self.assertRaises(ValueError):
            verify_log(log, 'kano', self.original)

    def test_duplicate_fields(self):
        self.reject('CAUGHT', 'cid', '17 cid=17')

    def test_assisted_trace(self):
        self.reject('FIELD', 'writes', 1, lambda l: 'frame=1672 ' in l)

    def test_proxy_identity(self):
        self.reject('FIELD', 'cid', 11, lambda l: 'frame=1672 ' in l)

    def test_wrong_victim_roster(self):
        self.reject('FIELD', 'hroster', 1, lambda l: 'frame=1672 ' in l)

    def test_human_cpu_controller_swap(self):
        self.reject('CAUGHT', 'cstate', 1)

    def test_changed_main(self):
        self.reject('FIELD', 'cmain', '0106A380', lambda l: 'frame=1672 ' in l)

    def test_event_operand_not_instruction(self):
        self.reject('EVENT', 'pc', 'FF8B7010', lambda l: 'entry=FF8B6FF0 ' in l)

    def test_wrong_damage_process(self):
        self.reject('HEALTH', 'a13', '0106BF30', lambda l: 'frame=1695 ' in l)

    def test_wrong_damage_writer(self):
        self.reject('HEALTH', 'pc', 'FFFFF000', lambda l: 'frame=1695 ' in l)

    def test_jax_damage(self):
        self.reject('HEALTH', 'after', 129, lambda l: 'frame=1695 ' in l)

    def test_extra_hit_not_air_damage(self):
        line = next(l for l in self.log.splitlines() if l.startswith('MK2_CPU_AIR_HEALTH frame=1695 '))
        with self.assertRaises(ValueError):
            verify_log(self.log + '\n' + line.replace('frame=1695', 'frame=1700'), 'kano', self.original)

    def test_jax_height_shift(self):
        self.reject('FIELD', 'cyraw', '00688000', lambda l: 'frame=1672 ' in l)

    def test_missing_owned_pose(self):
        self.reject('FIELD', 'cpose', 'FF0102C0', lambda l: 'frame=1685 ' in l)

    def test_wrong_full_fraction_grip(self):
        self.reject('FIELD', 'hyraw', '00450000', lambda l: 'frame=1672 ' in l)

    def test_native_chance_threshold(self):
        self.reject('EVENT', 'a0', '000003E8', lambda l: 'entry=FF80EC20 ' in l and 'frame=1669 ' in l)

    def test_wrong_jump_callback(self):
        self.reject('EVENT', 'a6', 'FF9BEC00', lambda l: 'entry=FF9C8180 ' in l)

    def test_wrong_flight_velocity(self):
        self.reject('FIELD', 'hvx', '00040000', lambda l: 'frame=1680 ' in l)

    def test_wrong_bounce_fraction(self):
        self.reject('FIELD', 'hyraw', '00520000', lambda l: 'frame=1686 ' in l)

    def test_missing_flight_callback(self):
        log = '\n'.join(l for l in self.log.splitlines() if not ('MK2_CPU_AIR_EVENT frame=1690 ' in l and 'entry=FFFFF800 ' in l))
        with self.assertRaises(ValueError):
            verify_log(log, 'kano', self.original)

    def test_remaining_own_lock(self):
        self.reject('OWN_READY', 'cflags', '00000010')

    def test_detachment_not_proven(self):
        self.reject('VICTIM_READY', 'htrail', '01060000')

    def test_delayed_completion(self):
        self.reject('COMPLETE', 'frame', 1740)

    def test_counter_save_mask(self):
        with self.assertRaises(ValueError):
            verify_log(self.log.replace('098F,FE00', '098F,F000', 1), 'kano', self.original)

    def test_guard_missing_nop(self):
        with self.assertRaises(ValueError):
            verify_log(self.log.replace('F050,FF9B,0300,C080,EF40', 'F050,FF9B,FFFF,C080,EF40', 1), 'kano', self.original)

    def test_height_wrong_register_clear(self):
        with self.assertRaises(ValueError):
            verify_log(self.log.replace('CB01,5621', 'CB01,5601', 1), 'kano', self.original)

    def test_native_eligibility_changed(self):
        with self.assertRaises(ValueError):
            verify_log(self.log.replace('0B43,FF9F', '0B43,FF8F', 1), 'kano', self.original)


if __name__ == '__main__':
    unittest.main()
