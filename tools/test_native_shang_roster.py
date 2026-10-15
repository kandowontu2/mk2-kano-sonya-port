"""Actual observed CPU morph chains and fail-closed mutation regressions."""
import re
import struct
import unittest
from pathlib import Path

import verify_native_shang_roster as check

ROOT=Path(__file__).resolve().parents[1]


class NativeRoster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        cls.rates=[f'{v:08X}' for v in struct.unpack_from('<17I',original,(0xff8702c0-0xff800000)//8)]
        cls.logs={name:(ROOT/f'audit_v338_shang_{name}_full_roster_table/run.log').read_text(encoding='utf-8-sig')
                  for name in ('kano','sonya')}

    def rejects(self,log,fighter='sonya'):
        proof=check.verify_log(log,fighter,self.rates)
        self.assertFalse(proof['passed'],proof)

    def test_actual_kano_forward_reverse_and_later_stock_morph(self):
        self.assertTrue(check.verify_log(self.logs['kano'],'kano',self.rates)['passed'])

    def test_actual_sonya_leg_turn_reverse_and_later_stock_morph(self):
        self.assertTrue(check.verify_log(self.logs['sonya'],'sonya',self.rates)['passed'])

    def test_scope_does_not_claim_unassisted_tower_pixels_commands_or_goal(self):
        proof=check.verify_log(self.logs['sonya'],'sonya',self.rates)
        self.assertFalse(proof['whole_character_integration_complete'])
        self.assertEqual(proof['scope'],check.SCOPE)

    def test_original_cpu_rate_table_overrun_is_rejected(self):
        self.rejects(self.logs['sonya'].replace('cpu=FFFFBF80','cpu=FF8702C0'))

    def test_new_rate_cannot_use_following_machine_code(self):
        self.rejects(self.logs['sonya'].replace('sonya=00000002','sonya=000D09C9'))

    def test_stock_rate_rows_are_not_overwritten(self):
        self.rejects(self.logs['sonya'].replace('stock=00000004','stock=00000002'))

    def test_random_selection_must_include_both_new_ids(self):
        self.rejects(self.logs['sonya'].replace('random=19C0','random=1980'))

    def test_native_random_call_must_have_correct_bound(self):
        self.rejects(self.logs['sonya'].replace('bound=14','bound=12'))

    def test_choice_not_proved_by_written_display_name(self):
        self.rejects(re.sub(r'^MK2_SHANG_ROSTER_CHOICE[^\n]*id=18[^\n]*\n','',self.logs['sonya'],flags=re.M))

    def test_actual_actor_id_store_required(self):
        self.rejects(re.sub(r'^MK2_SHANG_ROSTER_STORE[^\n]*old=6 id=18[^\n]*\n','',self.logs['sonya'],flags=re.M))

    def test_native_id_store_cannot_be_a_lua_or_other_writer(self):
        self.rejects(self.logs['sonya'].replace('pc=FF86E670','pc=00000000'))

    def test_wrong_transition_sequence_is_rejected(self):
        self.rejects(self.logs['sonya'].replace('root=FF0C1A00','root=FF0C1800'))

    def test_missing_original_transition_component_group(self):
        self.rejects(self.logs['sonya'].replace('group=FF0C4180','group=FF0C4120',1))

    def test_wrong_original_transition_palette(self):
        self.rejects(self.logs['sonya'].replace('palette=FF0C1000','palette=FF0C0800'))

    def test_native_restore_lookup_required(self):
        self.rejects(re.sub(r'^MK2_SHANG_ROSTER_RESTORE_LOOKUP[^\n]*id=18[^\n]*\n','',self.logs['sonya'],flags=re.M))

    def test_sonya_stalled_until_timeout_is_not_restoration(self):
        self.rejects(re.sub(r'^MK2_SHANG_ROSTER_STORE[^\n]*old=18 id=6[^\n]*\n','',self.logs['sonya'],flags=re.M))

    def test_forced_restore_store_cannot_pass(self):
        self.rejects(self.logs['sonya'].replace('pc=FFA16700','pc=00000000'))

    def test_every_form_field_required(self):
        self.rejects(re.sub(r'^MK2_SHANG_ROSTER_FIELD frame=1600[^\n]*\n','',self.logs['sonya'],flags=re.M))

    def test_actor_cpu_roster_must_remain_shang_not_pinned_sonya(self):
        self.rejects(self.logs['sonya'].replace('id=18 roster=6','id=18 roster=18',1))

    def test_owned_actor_task_cannot_silently_change(self):
        self.rejects(self.logs['sonya'].replace('FIELD frame=1600 actor=010350A0','FIELD frame=1600 actor=01034E90'))

    def test_no_silent_observer_identity_writes(self):
        self.rejects(self.logs['sonya'].replace('writes=0','writes=1',1))

    def test_restored_cpu_needs_consecutive_control_fields(self):
        self.rejects(re.sub(r'^MK2_SHANG_ROSTER_RESTORED_FIELD[^\n]*age=60 [^\n]*\n','',self.logs['sonya'],flags=re.M))

    def test_wrong_restored_floor_is_not_natural(self):
        self.rejects(self.logs['sonya'].replace('floor=87','floor=81'))

    def test_later_stock_morph_not_broken_by_new_slots(self):
        self.rejects(re.sub(r'^MK2_SHANG_ROSTER_STORE[^\n]*old=6 id=(4|10) [^\n]*\n','',self.logs['sonya'],flags=re.M))

    def test_sonya_leg_cannot_be_disabled_to_hide_turn_failure(self):
        self.rejects(self.logs['sonya'].replace('action=0110','action=0000'))

    def test_sonya_actual_turn_timing_cannot_remain_thousands_of_fields(self):
        self.rejects(self.logs['sonya'].replace('rate=00000002 list=FF020DC0','rate=000D09C9 list=FF020DC0'))

    def test_stage_fixture_assistance_must_be_declared(self):
        self.rejects(self.logs['sonya'].replace('requested=14 injected=true','requested=14 injected=false'))


if __name__=='__main__':unittest.main()
