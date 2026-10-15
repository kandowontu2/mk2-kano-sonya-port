"""Actual current paired moves/air throws and rejection of incomplete proof."""
import re
import unittest
from pathlib import Path
from unittest.mock import patch

import verify_current_post_ending_specials as current
from verify_restart_airthrow import verify as air

ROOT=Path(__file__).resolve().parents[1]
CASES=(
    ('audit_v319_current_pair_p1_kano','sonya','kano',1,1,'pair','sonya',False),
    ('audit_v319_current_pair_p1_sonya','kano','sonya',1,1,'pair','sonya',False),
    ('audit_v319_current_pair_p2_kano','sonya','kano',2,2,'pair','sonya',False),
    ('audit_v319_current_pair_p2_sonya','kano','sonya',2,2,'pair','sonya',False),
    ('audit_v319_current_air_p1_sonya_followup','kano','kano',1,1,'airthrow','sonya',True),
    ('audit_v321_current_air_p2_subzero_followup','sonya','kano',2,2,'airthrow','sub_zero',True),
)


class CurrentPostEndingSpecials(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs=[(ROOT/spec[0]/'run.log').read_text(encoding='utf-8-sig') for spec in CASES]
        cls.cold=(ROOT/'audit_v321_subzero_follow_walk_pilot/run.log').read_text(encoding='utf-8-sig')

    def reject(self,tag,key=None,value=None,index=0,predicate=lambda s:True):
        lines=self.logs[index].splitlines()
        row=next(i for i,line in enumerate(lines) if line.startswith(tag+' ') and predicate(line))
        if key is None:del lines[row]
        else:lines[row],count=re.subn(r'\b'+key+r'=\S+',key+'='+str(value),lines[row]);self.assertEqual(count,1)
        result=current.verify_log('\n'.join(lines),*CASES[index][1:])
        self.assertFalse(result['passed'],result)

    def test_all_six_current_paths_exact_build_and_frozen_inputs(self):
        for spec in CASES:
            with self.subTest(case=spec[0]):
                result=current.verify(ROOT/spec[0],*spec[1:])
                self.assertTrue(result['passed'],result['errors'])
                self.assertFalse(result['whole_character_integration_complete'])

    def test_current_identity_not_previous_launcher(self):
        with patch.object(current,'EXE_SHA','0'*64):
            self.assertFalse(current.verify(ROOT/CASES[0][0],*CASES[0][1:])['passed'])

    def test_wrong_case_parameters_not_accepted(self):
        self.assertFalse(current.verify(ROOT/CASES[0][0],'kano','sonya',1,1,'pair')['passed'])

    def test_all_native_ending_fetches_required(self):self.reject('MK2_RESTART_PICTURE',predicate=lambda s:'page=2' in s)
    def test_native_attract_required(self):self.reject('MK2_RESTART_ATTRACT')
    def test_true_character_identity_required(self):self.reject('MK2_RESTART_MATCH','id',1)
    def test_fresh_full_game_fields_required(self):self.reject('MK2_RESTART_COMPLETE','live',120)
    def test_fresh_cpu_p1_scope_also_checked(self):self.reject('MK2_RESTART_CPU','cpu_side',1)
    def test_fresh_cpu_native_order_required(self):self.reject('MK2_RESTART_CPU','schedule','FF8A1320')
    def test_fresh_cpu_identity_not_alias(self):self.reject('MK2_RESTART_CPU','id',1)
    def test_actual_p1_regeneration_inventory(self):self.reject('MK2KS_DIAGNOSTIC_P1_REGEN')
    def test_actual_p2_assistance_inventory(self):self.reject('MK2_P2_TOWER_HEALTH',index=2)

    def test_no_assistance_after_attract(self):
        end=int(re.search(r'MK2_RESTART_ATTRACT frame=(\d+)',self.logs[0])[1])
        self.reject('MK2KS_DIAGNOSTIC_P1_REGEN','frame',end+1)

    def test_paired_per_field_pose_required(self):
        self.reject('MK2_RESTART_PAIR_STATE','pose','FF977350',predicate=lambda s:'pose=FE8304E0' in s and 'vaction=0112' in s)

    def test_choke_mid_hold_not_only_first_phase_field(self):
        self.reject('MK2_RESTART_PAIR_STATE','pose','FF977350',predicate=lambda s:'age=35 ' in s)

    def test_choke_mid_hold_grip_coordinates(self):
        self.reject('MK2_RESTART_PAIR_STATE','vxpos',1,predicate=lambda s:'age=35 ' in s)

    def test_paired_native_release_required(self):self.reject('MK2_RESTART_PAIR_EVENT',predicate=lambda s:'kind=release' in s)
    def test_air_actual_victim_required(self):self.reject('MK2_AIR_JOIN_BEGIN','victim','sonya',index=5)
    def test_air_actual_native_damage_required(self):self.reject('MK2_AIR_JOIN_HEALTH','delta',1,index=5)
    def test_subzero_complete_24_walk_fields_required(self):self.reject('MK2_AIR_JOIN_FOLLOW_CONTROL',index=5,predicate=lambda s:'button=left' in s or 'button=right' in s)
    def test_subzero_plan_cannot_shorten_actual_walk(self):self.reject('MK2_AIR_JOIN_FOLLOW_PLAN','walk','0,8',index=5)
    def test_followup_punch_contact_cannot_be_waived(self):self.reject('MK2_AIR_JOIN_FOLLOW_HEALTH',index=5)
    def test_followup_native_trajectory_required(self):self.reject('MK2_AIR_JOIN_FOLLOW_EVENT','a1','00000000',index=5)
    def test_followup_final_clean_state_required(self):self.reject('MK2_AIR_JOIN_FOLLOW_SAMPLE','vflags','0005',index=5,predicate=lambda s:'action=0303' in s)

    def test_retained_old_short_walk_subzero_miss_still_rejected(self):
        log=(ROOT/'audit_v319_current_air_p2_subzero_followup/run.log').read_text(encoding='utf-8-sig')
        result=air(log,side=2,require_followup=True)
        self.assertFalse(result['passed'])
        self.assertIn('Actual unassisted follow-up punch contact required',result['errors'])

    def test_cold_can_prove_controls_but_never_an_ending(self):
        self.assertTrue(air(self.cold,require_followup=True,require_restart=False)['passed'])
        self.assertFalse(air(self.cold,require_followup=True)['passed'])
        self.assertFalse(current.verify_log(self.cold,*CASES[4][1:])['passed'])


if __name__=='__main__':unittest.main()
