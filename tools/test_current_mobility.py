"""Actual current contact cases, including reverse slots and malformed proof."""
import re
import unittest
from pathlib import Path

from verify_current_mobility import verify, ROOT
from verify_restart_lifecycle import verify_mobility_join
from verify_mobility_contact import verify as contact


def folder(target, side, scenario):
    return ROOT/f'audit_v312_current_{"ball" if target=="kano" else "square"}_{scenario}_p{side}'


class CurrentMobility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs = {(t, s, c):(folder(t, s, c)/'run.log').read_text(encoding='utf-8-sig')
                    for t in ('kano', 'sonya') for s in (1, 2) for c in ('hit', 'block', 'miss')}

    def test_all_twelve_actual_current_paths(self):
        for spec in self.logs:
            result = verify(folder(*spec), *spec)
            self.assertTrue(result['passed'], (spec, result['errors']))

    def test_cold_contacts_do_not_prove_endings(self):
        for (target, side, _), log in self.logs.items():
            self.assertFalse(verify_mobility_join(log, target, side)['passed'])

    def test_wrong_case_identity(self):
        self.assertFalse(verify(folder('kano', 1, 'hit'), 'sonya', 1, 'hit')['passed'])

    def test_wrong_case_scenario(self):
        self.assertFalse(verify(folder('kano', 1, 'hit'), 'kano', 1, 'block')['passed'])

    def test_wrong_case_slot(self):
        self.assertFalse(verify(folder('sonya', 2, 'hit'), 'sonya', 1, 'hit')['passed'])

    def change(self, tag, key, value, target='kano', side=2, scenario='hit', predicate=lambda line:True):
        log = self.logs[target, side, scenario]
        changed = False
        def replace(m):
            nonlocal changed
            if changed or not predicate(m[0]):
                return m[0]
            result = re.sub(r'(\b'+key+r'=)[^\s]+', lambda n:n[1]+str(value), m[0], count=1)
            changed = result != m[0]
            return result
        result = re.sub(r'^MK2_MOB_CONTACT_'+tag+r' [^\r\n]*', replace, log, flags=re.M)
        self.assertTrue(changed, 'Mutation must change the actual trace')
        self.assertFalse(verify_mobility_join(result, target, side, False)['passed'])

    def test_reverse_slot_actor_identity(self):
        self.change('FIELD', 'id', 1, predicate=lambda line:'slot=2 ' in line)

    def test_reverse_slot_cpu_proxy(self):
        self.change('FIELD', 'state', 0, target='sonya', predicate=lambda line:'slot=2 ' in line)

    def test_reverse_slot_wrong_native_damage(self):
        self.change('HEALTH', 'pc', 'FF825930')

    def test_reverse_slot_wrong_flight_pose(self):
        self.change('FIELD', 'pose', 'FF00EB80', predicate=lambda line:'slot=2 ' in line and 'pose=FF00EB40 ' in line)

    def test_reverse_slot_missing_field(self):
        log = re.sub(r'^MK2_MOB_CONTACT_FIELD[^\r\n]*\r?\n', '', self.logs['sonya', 2, 'block'], count=1, flags=re.M)
        self.assertFalse(verify_mobility_join(log, 'sonya', 2, False)['passed'])

    def test_reverse_slot_missing_cleanup(self):
        log = re.sub(r'^MK2_MOB_CONTACT_FIELD[^\r\n]*age=600 [^\r\n]*\r?\n', '', self.logs['kano', 2, 'miss'], flags=re.M)
        self.assertFalse(contact(log, 'kano', 2)['passed'])

    def test_misses_cannot_hide_damage(self):
        self.change('FIELD', 'hp', 160, scenario='miss', predicate=lambda line:'age=600 slot=1 ' in line)


if __name__ == '__main__':
    unittest.main()
