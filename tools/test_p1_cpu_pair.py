"""Natural CPU paired-contact fixtures; fail closed on false/incomplete proofs."""
import re
import unittest

import verify_p1_cpu_pair as check

CASES=((373,'sonya',602),(373,'sonya',604),(373,'sonya',605),(374,'kano',605),(374,'liu_kang',604),(374,'liu_kang',605),(374,'sub_zero',605))


class P1CpuPair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(name,boot):(check.ROOT/f'audit_v{version}_p1_cpu_pair_{name}_boot{boot}/run.log').read_text(encoding='utf-8-sig')for version,name,boot in CASES}
        leg_events=check.rows(cls.logs[('sonya',605)],'EVENT')
        choke_events=check.rows(cls.logs[('sonya',604)],'EVENT')
        cls.leg_hold='frame='+str(next(r['frame']for r in leg_events if r['kind']=='step')+10)+' '
        cls.choke_hold='frame='+str([r['frame']for r in choke_events if r['kind']=='step'][3]+1)+' '
        cls.leg_flight='frame='+str(next(r['frame']for r in leg_events if r['kind']=='release')+2)+' '

    def rejects(self,log,player='sonya'):
        proof=check.verify_log(log,player)
        self.assertFalse(proof['passed'],proof)

    def change(self,tag,key,value,*,kano=False,contains=None,remove=False):
        log=self.logs[('sonya',604 if kano else 605)];lines=log.splitlines(keepends=True)
        for i,line in enumerate(lines):
            if line.startswith('MK2_CPU_PAIR_'+tag+' ')and(contains is None or contains in line)and re.search(r'\b'+key+r'=',line):
                lines[i]=''if remove else re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
                return ''.join(lines)
        self.fail('Mutation must affect actual evidence')

    def test_seven_actual_cold_P1_CPU_full_pairs(self):
        for version,name,boot in CASES:
            with self.subTest(name=name,boot=boot):
                proof=check.verify_log(self.logs[(name,boot)],name)
                self.assertTrue(proof['passed'],proof)
                self.assertIn(proof['damage'],(32,35))
                self.assertGreater(proof['victim_flight_fields'],8)

    def test_ambiguous_early_schema_is_rejected(self):
        for case in ('audit_v367_cpu_pair_sonya_boot601','audit_v368_cpu_pair_sonya_boot602','audit_v369_cpu_pair_kano_boot601'):
            self.rejects((check.ROOT/case/'run.log').read_text(encoding='utf-8-sig'))

    def test_logging_error_cannot_pass_exit_zero(self):
        self.rejects((check.ROOT/'audit_v366_cpu_pair_sonya_boot601/run.log').read_text(encoding='utf-8-sig'))

    def test_missing_native_descriptor_reads_is_not_complete(self):
        self.rejects((check.ROOT/'audit_v370_cpu_pair_sonya_boot601/run.log').read_text(encoding='utf-8-sig'))

    def test_scope_does_not_claim_every_observed_cycle_all_slots_or_goal(self):
        proof=check.verify_log(self.logs[('liu_kang',605)],'liu_kang')
        self.assertTrue(proof['passed'],proof)
        self.assertEqual(proof['cycle'],1)
        self.assertGreater(proof['observed_cycles'],1)
        self.assertEqual((proof['CPU_slot'],proof['human_slot']),(1,2))
        self.assertFalse(proof['whole_character_integration_complete'])
        self.assertIn('other_misses_interruptions',proof['completed_cycle_scope'])

    def test_actual_native_CPU_role(self):self.rejects(self.change('FIELD','state','1',contains='cycle=1 '))
    def test_actual_human_victim_role(self):self.rejects(self.change('FIELD','vstate','0',contains='cycle=1 '))
    def test_actual_roster_not_proxy(self):self.rejects(self.change('FIELD','roster','1',contains='cycle=1 '))
    def test_actual_own_Main(self):self.rejects(self.change('FIELD','main','0106BF30',contains='cycle=1 '))
    def test_native_original_ladder_order(self):self.rejects(self.logs[('sonya',605)].replace('ids=18,8,2,0,1,9,3,17','ids=1,8,2,0,18,9,3,17'))
    def test_no_health_assistance(self):self.rejects(self.change('FIELD','writes','1',contains=self.leg_hold))
    def test_missing_held_field(self):self.rejects(self.change('FIELD','frame','',contains=self.leg_hold,remove=True))
    def test_leg_own_pose(self):self.rejects(self.change('FIELD','pose','FE830600',contains=self.leg_hold))
    def test_leg_victim_pose(self):self.rejects(self.change('FIELD','vpose','FE829500',contains=self.leg_hold))
    def test_leg_grip(self):self.rejects(self.change('FIELD','vxpos','100',contains=self.leg_hold))
    def test_leg_shake(self):self.rejects(self.change('FIELD','vypos','100',contains=self.leg_hold))
    def test_leg_lock(self):self.rejects(self.change('FIELD','suppression','0',contains=self.leg_hold))
    def test_leg_hold_health(self):self.rejects(self.change('FIELD','vhp','161',contains=self.leg_hold))
    def test_choke_every_held_pose(self):self.rejects(self.change('FIELD','pose','FE830540',kano=True,contains=self.choke_hold))
    def test_choke_grip(self):self.rejects(self.change('FIELD','vxpos','100',kano=True,contains=self.choke_hold))
    def test_choke_squeeze_cadence(self):self.rejects(self.change('EVENT','frame','2299',kano=True,contains='kind=pulse '))
    def test_missing_native_release(self):self.rejects(self.change('EVENT','entry','',contains='kind=release ',remove=True))
    def test_data_read_PC_is_not_code_entry_PC(self):self.rejects(self.change('EVENT','pc','FFF83010',contains='kind=intro '))
    def test_real_catch_descriptor(self):self.rejects(self.change('EVENT','word','0065',contains='kind=attack '))
    def test_forced_health_store(self):self.rejects(self.change('HEALTH','pc','00000000',contains='cycle=1 '))
    def test_wrong_damage_argument(self):self.rejects(self.change('EVENT','a10','00000020',contains='kind=damage '))
    def test_wrong_fling_gravity(self):self.rejects(self.change('EVENT','a2','00000000',contains='kind=fling '))
    def test_wrong_victim_velocity_request(self):self.rejects(self.change('EVENT','a1','010602D0',contains='kind=velocity '))
    def test_every_native_flight_step(self):self.rejects(self.change('FIELD','vyraw','004B7000',contains=self.leg_flight))
    def test_both_recoveries_required(self):self.rejects(re.sub(r'^MK2_CPU_PAIR_EVENT[^\n]*kind=victim_ready[^\n]*\n','',self.logs[('sonya',605)],flags=re.M))
    def test_final_grounded_recovery(self):self.rejects(self.change('COMPLETE','vypos','40'))
    def test_final_detached_child(self):self.rejects(self.change('COMPLETE','vtrail','010352B0'))
    def test_terminal_complete_frame(self):self.rejects(self.change('RESULT','complete','2000'))
    def test_duplicate_fields_cannot_silently_overwrite(self):self.rejects(self.change('FIELD','vx','00000000 vx=100',contains=self.leg_hold))
    def test_an_entry_and_ready_without_full_contact_is_rejected(self):
        self.rejects(re.sub(r'^MK2_CPU_PAIR_EVENT[^\n]*kind=step[^\n]*\n','',self.logs[('sonya',605)],flags=re.M))


    def test_no_CPU_P2_case_may_be_relabelled_P1(self):
        self.rejects((check.ROOT/'audit_v371_cpu_pair_sonya_boot601/run.log').read_text(encoding='utf-8-sig'))

    def test_no_incomplete_or_KO_scout_is_a_completed_pair(self):
        for case,player in (('audit_v373_p1_cpu_pair_sonya_boot601','sonya'),
                            ('audit_v373_p1_cpu_pair_sonya_boot603','sonya'),
                            ('audit_v374_p1_cpu_pair_kano_boot604','kano'),
                            ('audit_v375_p1_cpu_pair_cage_boot605','cage')):
            self.rejects((check.ROOT/case/'run.log').read_text(encoding='utf-8-sig'),player)

    def test_actual_logged_CPU_slot(self):self.rejects(self.change('FIELD','cpu_slot','2',contains=self.leg_hold))
    def test_actual_logged_human_slot(self):self.rejects(self.change('FIELD','human_slot','1',contains=self.leg_hold))
    def test_actual_health_slot_not_P1(self):self.rejects(self.change('HEALTH','slot','1',contains='before=95 after=60 '))

    def cold_change(self,tag,key,value):
        log=self.logs[('sonya',605)]
        lines=log.splitlines(keepends=True)
        for i,line in enumerate(lines):
            if line.startswith('MK2_P1CPU_'+tag+' ')and re.search(r'\b'+key+r'=',line):
                lines[i]=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
                return ''.join(lines)
        self.fail('Cold-selection mutation must affect actual evidence')

    def test_cold_P2_selection_identity(self):self.rejects(self.cold_change('SELECT_RESULT','human_id','1'))
    def test_cold_P2_selection_had_no_errors(self):self.rejects(self.cold_change('SELECT_RESULT','errors','1'))
    def test_cold_P2_selection_observed_checks(self):self.rejects(self.cold_change('SELECT_RESULT','checks','0'))
    def test_cold_selection_order(self):self.rejects(self.cold_change('SELECT_RESULT','exit','1800'))
    def test_cold_native_stage_zero(self):self.rejects(self.cold_change('COLD_LIVE','stage','5'))
    def test_cold_actual_original_order(self):self.rejects(self.cold_change('COLD_LIVE','schedule','FFFA3000'))
    def test_no_host_assistance_on_cold_selection(self):self.rejects(self.cold_change('SELECT_RESULT','assistance','health_only'))
    def test_cold_actual_CPU_id(self):self.rejects(self.cold_change('COLD_LIVE','cpu_id','17'))
    def test_cold_summary_cannot_have_duplicate_keys(self):self.rejects(self.cold_change('SELECT_RESULT','errors','0 errors=1'))
    def test_no_zero_exit_hidden_Lua_failure(self):self.rejects(self.logs[('sonya',605)]+'\n[LUA ERROR] probe failure\n')
    def test_stock_victim_is_original_actual_body(self):self.rejects(self.logs[('sub_zero',605)],'reptile')

    def test_exact_current_build_and_frozen_launch_inputs(self):
        for version,player,boot in CASES:
            proof=check.verify(check.ROOT/f'audit_v{version}_p1_cpu_pair_{player}_boot{boot}',player)
            self.assertTrue(proof['passed'],proof)
            self.assertEqual(proof['checked_inputs'],22)


if __name__=='__main__':unittest.main()
