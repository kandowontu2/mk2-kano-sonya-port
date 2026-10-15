"""Real repeated CPU morph fixtures; mutations must not hide second-cycle failures."""
import re
import struct
import unittest
from pathlib import Path

import verify_native_shang_roster as check

ROOT=Path(__file__).resolve().parents[1]


class RepeatedRoster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        cls.rates=[f'{v:08X}' for v in struct.unpack_from('<17I',original,(0xff8702c0-0xff800000)//8)]
        cls.logs={name:(ROOT/f'audit_v359_palette_fix_cpu_{name}/run.log').read_text(encoding='utf-8-sig')
                  for name in ('kano','sonya')}

    def rejects(self,log,fighter='sonya'):
        proof=check.verify_log(log,fighter,self.rates)
        self.assertFalse(proof['passed'],proof)

    def second(self,tag,old,new,*,remove=False):
        lines=self.logs['sonya'].splitlines(keepends=True)
        for index,line in enumerate(lines):
            match=re.search(r'frame=(\d+)',line)
            if line.startswith(check.PREFIX+tag+' ') and match and int(match[1])>=3394 and old in line:
                lines[index]='' if remove else line.replace(old,new)
                return ''.join(lines)
        self.fail('Mutation must affect actual second-cycle evidence')

    def test_actual_two_kano_cycles(self):
        proof=check.verify_log(self.logs['kano'],'kano',self.rates)
        self.assertTrue(proof['passed'],proof)
        self.assertEqual(proof['form_fields'],1190)
        self.assertEqual(len(proof['morph_cycles']),2)
        self.assertEqual(proof['post_restore_fields'],240)

    def test_actual_two_sonya_cycles_without_forcing_random_leg_every_cycle(self):
        proof=check.verify_log(self.logs['sonya'],'sonya',self.rates)
        self.assertTrue(proof['passed'],proof)
        self.assertEqual(proof['form_fields'],1156)
        self.assertEqual([c['signature_leg_observed'] for c in proof['morph_cycles']],[True,False])
        self.assertIn('not_required_after_every_random_repeat',proof['later_stock_morph_scope'])
        self.assertFalse(proof['whole_character_integration_complete'])

    def test_second_choice_required(self):
        self.rejects(self.second('CHOICE','id=18','',remove=True))

    def test_second_forward_store_required(self):
        self.rejects(self.second('STORE','old=6 id=18','',remove=True))

    def test_second_reverse_store_required(self):
        self.rejects(self.second('STORE','old=18 id=6','',remove=True))

    def test_second_reverse_store_must_be_native(self):
        self.rejects(self.second('STORE','pc=FFA16700','pc=00000000'))

    def test_second_lookup_required(self):
        self.rejects(self.second('RESTORE_LOOKUP','id=18','',remove=True))

    def test_second_transition_hold_required(self):
        self.rejects(self.second('GROUP','group=FF0C4120','',remove=True))

    def test_second_palette_required(self):
        self.rejects(self.second('PALETTE','palette=FF0C1000','palette=FF0C0800'))

    def test_second_field_required(self):
        self.rejects(self.second('FIELD','id=18','',remove=True))

    def test_second_ownership_required(self):
        self.rejects(self.second('FIELD','main=0106C620','main=0106CCF0'))

    def test_second_restored_field_required(self):
        self.rejects(self.second('RESTORED_FIELD','from=18','',remove=True))

    def test_second_restored_floor_required(self):
        self.rejects(self.second('RESTORED_FIELD','floor=87','floor=81'))

    def test_no_leg_in_any_cycle_is_rejected(self):
        self.rejects(self.logs['sonya'].replace('action=0110','action=0000'))

    def test_observed_leg_turn_stall_is_rejected(self):
        self.rejects(self.logs['sonya'].replace('rate=00000002 list=FF020DC0','rate=000D09C9 list=FF020DC0'))

    def test_result_counts_cannot_hide_second_cycle(self):
        self.rejects(self.logs['sonya'].replace('restore_sonya=2','restore_sonya=1'))

    def test_stock_fallback_still_required_in_repeat_fixture(self):
        self.rejects(re.sub(r'^MK2_SHANG_ROSTER_STORE[^\n]*old=6 id=7 [^\n]*\n','',self.logs['sonya'],flags=re.M))


if __name__=='__main__':unittest.main()
