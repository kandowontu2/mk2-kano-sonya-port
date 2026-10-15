"""Native per-owner ready handoffs must prove full contact and new follow-up."""
import re
import unittest

import verify_cpu_recovery_v545_v2 as check

CASES=(('kano',604),('cage',605))


class NativeCpuRecovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={p:(check.ROOT/f'audit_v564_cpu_recovery_{p}_boot{b}/run.log').read_text(encoding='utf-8-sig')for p,b in CASES}
        for player,log in cls.logs.items():
            proof=check.verify_log(log,player)
            if not proof['passed']:raise AssertionError('Nonvacuous actual baseline required: '+str(proof))

    def reject(self,log,player='cage'):
        proof=check.verify_log(log,player)
        self.assertFalse(proof['passed'],proof)

    def change(self,tag,key,value,*,player='cage',contains=None,remove=False,all_matches=False):
        lines=self.logs[player].splitlines(keepends=True);count=0
        for i,line in enumerate(lines):
            if line.startswith('MK2_CPU_PAIR_'+tag+' ')and(contains is None or all(s in line for s in contains))and re.search(r'\b'+key+r'=',line):
                lines[i]=''if remove else re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
                count+=1
                if not all_matches:break
        self.assertGreater(count,0,'Mutation must affect actual source evidence')
        return ''.join(lines)

    def test_both_full_native_pairs_and_individual_handoffs(self):
        for player,boot in CASES:
            proof=check.verify(check.ROOT/f'audit_v564_cpu_recovery_{player}_boot{boot}',player)
            self.assertTrue(proof['passed'],proof)
            self.assertEqual(proof['held_fields'],70 if player=='kano'else 46)
            self.assertLess(proof['own_handoff'],proof['victim_handoff'])
            self.assertEqual(proof['complete'],proof['victim_handoff']+1)
            self.assertFalse(proof['whole_character_integration_complete'])

    def test_actual_CPU_role(self):self.reject(self.change('FIELD','state','1',contains=('cycle=2 ',)))
    def test_actual_human_role(self):self.reject(self.change('FIELD','vstate','0',contains=('cycle=2 ',)))
    def test_actual_roster(self):self.reject(self.change('FIELD','roster','1',contains=('cycle=2 ',)))
    def test_actual_owner_Main(self):self.reject(self.change('FIELD','owner','010350A0',contains=('cycle=2 ',)))
    def test_missing_held_callback(self):self.reject(self.change('FIELD','frame','',contains=('frame=2514 ',),remove=True))
    def test_leg_own_pose(self):self.reject(self.change('FIELD','pose','FE830600',contains=('frame=2514 ',)))
    def test_original_Cage_victim_pose(self):self.reject(self.change('FIELD','vpose','FE829500',contains=('frame=2514 ',)))
    def test_original_Cage_grip(self):self.reject(self.change('FIELD','vxpos','100',contains=('frame=2514 ',)))
    def test_leg_shake(self):self.reject(self.change('FIELD','vypos','100',contains=('frame=2514 ',)))
    def test_leg_push_lock(self):self.reject(self.change('FIELD','suppression','0',contains=('frame=2514 ',)))
    def test_leg_hold_health(self):self.reject(self.change('FIELD','vhp','161',contains=('frame=2514 ',)))
    def test_choke_own_pose(self):self.reject(self.change('FIELD','pose','FE830540',player='kano',contains=('frame=2030 ',)),'kano')
    def test_choke_grip(self):self.reject(self.change('FIELD','vxpos','100',player='kano',contains=('frame=2030 ',)),'kano')
    def test_choke_victim_pose(self):self.reject(self.change('FIELD','vpose','FF924DB0',player='kano',contains=('frame=2030 ',)),'kano')
    def test_choke_squeeze_cadence(self):self.reject(self.change('EVENT','frame','2050',player='kano',contains=('cycle=3 ','kind=pulse ')),'kano')
    def test_original_catch_descriptor(self):self.reject(self.change('EVENT','word','0065',contains=('cycle=2 ','kind=attack ')))
    def test_native_descriptor_consumer_PC(self):self.reject(self.change('EVENT','pc','FFF83010',contains=('cycle=2 ','kind=intro ')))
    def test_original_health_writer(self):self.reject(self.change('HEALTH','pc','00000000',contains=('cycle=2 ',)))
    def test_correct_actual_victim_health_slot(self):self.reject(self.change('HEALTH','slot','1',contains=('cycle=2 ','before=139 after=104 ')))
    def test_damage_call(self):self.reject(self.change('EVENT','a10','00000020',contains=('cycle=2 ','kind=damage ')))
    def test_fling_parameters(self):self.reject(self.change('EVENT','a2','00000000',contains=('cycle=2 ','kind=fling ')))
    def test_native_P2_velocity_slot(self):self.reject(self.change('EVENT','a1','010602D0',contains=('cycle=2 ','kind=velocity ')))
    def test_every_original_flight_step(self):self.reject(self.change('FIELD','vyraw','004B7000',contains=('frame=2552 ',)))
    def test_own_postcleanup_handoff_required(self):self.reject(self.change('OWN_REGAIN','frame','',contains=('cycle=2 ',),remove=True))
    def test_victim_postcleanup_handoff_required(self):self.reject(self.change('VICTIM_REGAIN','frame','',contains=('cycle=2 ',),remove=True))
    def test_handoff_entry_PC(self):self.reject(self.change('EVENT','pc','FF861360',contains=('cycle=2 ','kind=own_regain ')))
    def test_own_handoff_action_is_cleared(self):self.reject(self.change('OWN_REGAIN','action','771',contains=('cycle=2 ',)))
    def test_own_handoff_flags_are_cleared(self):self.reject(self.change('OWN_REGAIN','flags','00000010',contains=('cycle=2 ',)))
    def test_own_handoff_body_is_cleared(self):self.reject(self.change('OWN_REGAIN','body','00000016',contains=('cycle=2 ',)))
    def test_own_handoff_is_detached(self):self.reject(self.change('OWN_REGAIN','trail','01036540',contains=('cycle=2 ',)))
    def test_victim_handoff_action_is_cleared(self):self.reject(self.change('VICTIM_REGAIN','vaction','771',contains=('cycle=2 ',)))
    def test_victim_handoff_is_grounded(self):self.reject(self.change('VICTIM_REGAIN','vypos','40',contains=('cycle=2 ',)))
    def test_victim_handoff_is_stopped(self):self.reject(self.change('VICTIM_REGAIN','vvx','00030000',contains=('cycle=2 ',)))
    def test_original_own_body_clear_store_required(self):self.reject(self.change('FLAG','pc','',contains=('cycle=2 ','slot=1 ','frame=2559 ','kind=body '),remove=True,all_matches=True))
    def test_original_own_flag_clear_store_required(self):self.reject(self.change('FLAG','pc','',contains=('cycle=2 ','slot=1 ','frame=2559 ','kind=flags '),remove=True,all_matches=True))
    def test_original_victim_body_clear_store_required(self):self.reject(self.change('FLAG','pc','',contains=('cycle=2 ','slot=2 ','frame=2601 ','kind=body '),remove=True,all_matches=True))
    def test_original_victim_flag_clear_store_required(self):self.reject(self.change('FLAG','pc','',contains=('cycle=2 ','slot=2 ','frame=2601 ','kind=flags '),remove=True,all_matches=True))
    def test_cleanup_cannot_be_a_host_store(self):self.reject(self.change('FLAG','pc','00000000',contains=('cycle=2 ','slot=1 ','frame=2559 '),all_matches=True))
    def test_cleanup_bit_effect_not_just_PC(self):self.reject(self.change('FLAG','after','0016',contains=('cycle=2 ','slot=1 ','frame=2559 ','kind=body '),all_matches=True))
    def test_cleanup_store_actual_slot(self):self.reject(self.change('FLAG','slot','2',contains=('cycle=2 ','slot=1 ','frame=2559 '),all_matches=True))
    def test_new_CPU_action_setup_required_for_dirty_final_state(self):self.reject(self.change('FLAG','pc','',contains=('cycle=2 ','slot=1 ','frame=2588 ','kind=flags '),remove=True,all_matches=True))
    def test_new_CPU_action_setup_owning_Main(self):self.reject(self.change('FLAG','a13','0106C620',contains=('cycle=2 ','slot=1 ','frame=2588 '),all_matches=True))
    def test_new_CPU_action_setup_bit_effect(self):self.reject(self.change('FLAG','after','0000',contains=('cycle=2 ','slot=1 ','frame=2588 ','kind=flags '),all_matches=True))
    def test_no_unproved_residual_pair_body_bit(self):self.reject(self.change('COMPLETE','body','0000001E'))
    def test_final_not_still_the_paired_action(self):self.reject(self.change('COMPLETE','action','272'))
    def test_original_own_recovery_holds_not_shortened(self):self.reject(self.change('OWN_REGAIN','frame','2558',contains=('cycle=2 ',)))
    def test_coincidental_later_clean_callback_not_the_handoff(self):self.reject(self.change('COMPLETE','frame','3013'))
    def test_native_ready_entry_not_just_postcleanup_pose(self):self.reject(self.change('EVENT','pc','',contains=('cycle=2 ','kind=own_ready '),remove=True,all_matches=True))
    def test_readonly_native_flag_observation(self):self.reject(self.change('FLAG','writes','1',contains=('cycle=2 ',)))
    def test_duplicate_flag_labels_fail_closed(self):self.reject(self.change('FLAG','after','0012 after=0016',contains=('cycle=2 ',)))
    def test_hidden_Lua_error_is_not_exit_zero_success(self):self.reject(self.logs['cage']+'\n[LUA ERROR] failure\n')
    def test_final_victim_alive_health_unchanged(self):self.reject(self.change('COMPLETE','vhp','0'))
    def test_terminal_frame_matches_actual_followup_window(self):self.reject(self.change('RESULT','complete','3013'))


    def test_all_four_accepted_current_baselines(self):
        for player,boot in (('kano',604),('cage',605),('kano',605),('liu_kang',605)):
            proof=check.verify(check.ROOT/f'audit_v564_cpu_recovery_{player}_boot{boot}',player)
            self.assertTrue(proof['passed'],proof)
            self.assertFalse(proof['whole_character_integration_complete'])

    def test_other_natural_scouts_are_not_silently_accepted(self):
        for player,boot in (('sonya',602),('sub_zero',605),('liu_kang',604),('sonya',604)):
            proof=check.verify(check.ROOT/f'audit_v564_cpu_recovery_{player}_boot{boot}',player)
            self.assertFalse(proof['passed'],proof)

    def test_original_publication_instruction_register_address_and_ownership(self):
        for key,value in (('pc','00000000'),('a1','00000303'),('op0','B00D'),
                          ('op1','0210'),('at','0106C140'),('a13','0106C620'),
                          ('a8','010350A0'),('before','0000'),('after','0107'),
                          ('frame','2587'),('state','1'),('id','17')):
            with self.subTest(key=key):
                self.reject(self.change('FLAG',key,value,contains=('slot=1 ','kind=action ','frame=2588 ')))

    def test_missing_action_clear_walk_or_attack_store(self):
        for contains in (('frame=2559 ','after=0000 '),('frame=2566 ','after=0303 '),('frame=2588 ',)):
            with self.subTest(contains=contains):
                self.reject(self.change('FLAG','pc','',contains=('slot=1 ','kind=action ',*contains),remove=True,all_matches=True))

    def test_every_post_handoff_callback_action_is_crosschecked(self):
        self.reject(self.change('FIELD','action','771',contains=('frame=2590 ',)))
        self.reject(self.change('COMPLETE','action','263'))
        self.reject(self.change('COMPLETE','action','771'))

    def test_native_setup_must_precede_action_publication(self):
        lines=self.logs['cage'].splitlines(keepends=True)
        indices=[i for i,s in enumerate(lines) if s.startswith('MK2_CPU_PAIR_FLAG ') and 'slot=1 ' in s and 'frame=2588 ' in s]
        self.assertGreaterEqual(len(indices),3)
        publication=next(i for i in indices if 'kind=action ' in lines[i])
        setups=[i for i in indices if 'kind=body ' in lines[i] or 'kind=flags ' in lines[i]]
        text=lines[publication];lines[publication]='';lines.insert(min(setups),text)
        self.reject(''.join(lines))

    def test_followup_ordinary_attack_cleanup_is_required(self):
        for field in ('body','flags'):
            with self.subTest(field=field):
                self.reject(self.change('FLAG','pc','',contains=('slot=1 ','frame=2621 ','kind='+field+' '),remove=True,all_matches=True))
        self.reject(self.change('FLAG','a13','0106C620',contains=('slot=1 ','frame=2621 ',),all_matches=True))
        self.reject(self.change('FLAG','after','0010',contains=('slot=1 ','frame=2621 ','kind=flags '),all_matches=True))

    def test_wrong_schema_does_not_prove_action_provenance(self):
        self.reject(self.change('RESULT','schema','4'))

    def test_same_state_Kano_attack_still_requires_NEW_setup(self):
        self.reject(self.change('FLAG','pc','',player='kano',contains=('slot=1 ','frame=2128 ','kind=flags '),remove=True,all_matches=True),'kano')
        self.reject(self.change('FLAG','after','0012',player='kano',contains=('slot=1 ','frame=2128 ','kind=body '),all_matches=True),'kano')


if __name__=='__main__':unittest.main()
