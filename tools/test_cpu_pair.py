"""Natural CPU paired-contact fixtures; fail closed on false/incomplete proofs."""
import re
import unittest

import verify_cpu_pair as check

CASES=(('sonya',601),('sonya',602),('kano',601),('liu',601),('liu',602))


class CpuPair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(name,boot):(check.ROOT/f'audit_v371_cpu_pair_{name}_boot{boot}/run.log').read_text(encoding='utf-8-sig')for name,boot in CASES}

    def rejects(self,log,player='sonya'):
        proof=check.verify_log(log,player)
        self.assertFalse(proof['passed'],proof)

    def change(self,tag,key,value,*,kano=False,contains=None,remove=False):
        log=self.logs[('sonya',602 if kano else 601)];lines=log.splitlines(keepends=True)
        for i,line in enumerate(lines):
            if line.startswith('MK2_CPU_PAIR_'+tag+' ')and(contains is None or contains in line)and re.search(r'\b'+key+r'=',line):
                lines[i]=''if remove else re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
                return ''.join(lines)
        self.fail('Mutation must affect actual evidence')

    def test_five_actual_natural_CPU_full_pairs(self):
        for name,boot in CASES:
            with self.subTest(name=name,boot=boot):
                proof=check.verify_log(self.logs[(name,boot)],'liu_kang'if name=='liu'else name)
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
        proof=check.verify_log(self.logs[('liu',602)],'liu_kang')
        self.assertTrue(proof['passed'],proof)
        self.assertEqual(proof['cycle'],2)
        self.assertFalse(proof['whole_character_integration_complete'])
        self.assertIn('other_misses_interruptions',proof['completed_cycle_scope'])

    def test_actual_native_CPU_role(self):self.rejects(self.change('FIELD','state','1',contains='cycle=1 '))
    def test_actual_human_victim_role(self):self.rejects(self.change('FIELD','vstate','0',contains='cycle=1 '))
    def test_actual_roster_not_proxy(self):self.rejects(self.change('FIELD','roster','1',contains='cycle=1 '))
    def test_actual_own_Main(self):self.rejects(self.change('FIELD','main','0106A370',contains='cycle=1 '))
    def test_native_original_ladder_order(self):self.rejects(self.logs[('sonya',601)].replace('ids=18,8,2,0,1,9,3,17','ids=1,8,2,0,18,9,3,17'))
    def test_no_health_assistance(self):self.rejects(self.logs[('sonya',601)].replace('enabled=false writes=0','enabled=true writes=1'))
    def test_missing_held_field(self):self.rejects(self.change('FIELD','frame','',contains='frame=1920 ',remove=True))
    def test_leg_own_pose(self):self.rejects(self.change('FIELD','pose','FE830600',contains='frame=1920 '))
    def test_leg_victim_pose(self):self.rejects(self.change('FIELD','vpose','FE829500',contains='frame=1920 '))
    def test_leg_grip(self):self.rejects(self.change('FIELD','vxpos','100',contains='frame=1920 '))
    def test_leg_shake(self):self.rejects(self.change('FIELD','vypos','100',contains='frame=1920 '))
    def test_leg_lock(self):self.rejects(self.change('FIELD','suppression','0',contains='frame=1920 '))
    def test_leg_hold_health(self):self.rejects(self.change('FIELD','vhp','161',contains='frame=1920 '))
    def test_choke_every_held_pose(self):self.rejects(self.change('FIELD','pose','FE830540',kano=True,contains='frame=2290 '))
    def test_choke_grip(self):self.rejects(self.change('FIELD','vxpos','100',kano=True,contains='frame=2290 '))
    def test_choke_squeeze_cadence(self):self.rejects(self.change('EVENT','frame','2299',kano=True,contains='kind=pulse '))
    def test_missing_native_release(self):self.rejects(self.change('EVENT','entry','',contains='kind=release ',remove=True))
    def test_data_read_PC_is_not_code_entry_PC(self):self.rejects(self.change('EVENT','pc','FFF83010',contains='kind=intro '))
    def test_real_catch_descriptor(self):self.rejects(self.change('EVENT','word','0065',contains='kind=attack '))
    def test_forced_health_store(self):self.rejects(self.change('HEALTH','pc','00000000',contains='cycle=1 '))
    def test_wrong_damage_argument(self):self.rejects(self.change('EVENT','a10','00000020',contains='kind=damage '))
    def test_wrong_fling_gravity(self):self.rejects(self.change('EVENT','a2','00000000',contains='kind=fling '))
    def test_wrong_victim_velocity_request(self):self.rejects(self.logs[('sonya',601)].replace('a0=FFFD0000 a1=010602D0','a0=00030000 a1=010602D0'))
    def test_every_native_flight_step(self):self.rejects(self.change('FIELD','vyraw','004B7000',contains='frame=1952 '))
    def test_both_recoveries_required(self):self.rejects(re.sub(r'^MK2_CPU_PAIR_EVENT[^\n]*kind=victim_ready[^\n]*\n','',self.logs[('sonya',601)],flags=re.M))
    def test_final_grounded_recovery(self):self.rejects(self.change('COMPLETE','vypos','40'))
    def test_final_detached_child(self):self.rejects(self.change('COMPLETE','vtrail','010352B0'))
    def test_terminal_complete_frame(self):self.rejects(self.change('RESULT','complete','2000'))
    def test_duplicate_fields_cannot_silently_overwrite(self):self.rejects(self.change('FIELD','vx','00000000 vx=100',contains='frame=1920 '))
    def test_an_entry_and_ready_without_full_contact_is_rejected(self):
        self.rejects(re.sub(r'^MK2_CPU_PAIR_EVENT[^\n]*kind=step[^\n]*\n','',self.logs[('sonya',601)],flags=re.M))


if __name__=='__main__':unittest.main()
