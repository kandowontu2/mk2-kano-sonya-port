"""Actual challenger/full move evidence, with ending anchors kept mandatory."""
import re
import unittest
from pathlib import Path
from verify_restart_lifecycle import verify
from verify_post_ending_restart import verify as verify_restart
from check_post_restart_assistance import verify as verify_assistance

ROOT=Path(__file__).resolve().parents[1]


class ColdJoinedLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={target:(ROOT/f'audit_v289_native_join_{"blade" if target=="kano" else "bicycle"}/run.log').read_text(encoding='utf-8-sig') for target in ('kano','sonya')}

    def mutate(self,tag,key,value,target='kano',where=''):
        changed=False
        def replace(m):
            nonlocal changed
            if changed or where not in m[0]:return m[0]
            result=re.sub(r'(\b'+key+r'=)[^\s]+',lambda n:n[1]+str(value),m[0],count=1)
            changed=result!=m[0];return result
        return re.sub(r'^MK2_JOIN_LIFE_'+tag+r' [^\r\n]*',replace,self.logs[target],flags=re.M)

    def reject(self,log,target='kano'):
        self.assertNotEqual(log,self.logs[target]);self.assertFalse(verify(log,target,1,False)['passed'])

    def test_actual_cold_diagnoses_only(self):
        for target,log in self.logs.items():self.assertTrue(verify(log,target,1,False)['passed'])
    def test_cold_cannot_prove_post_ending(self):
        for target,log in self.logs.items():self.assertFalse(verify(log,target,1)['passed'])
    def test_original_null_actor_assumption_remains_failed(self):
        for target in self.logs:
            move='blade' if target=='kano' else 'bicycle'
            log=(ROOT/f'audit_v289_cold_join_{move}/run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log,target,1,False)['passed'])
    def test_wrong_joining_player_rejected(self):self.reject(self.mutate('BEGIN','joining',1))
    def test_wrong_native_css_initial_route_rejected(self):self.reject(self.mutate('CSS','initial',9))
    def test_wrong_actual_highlight_rejected(self):self.reject(self.mutate('HIGHLIGHT','roster',1))
    def test_wrong_human_state_rejected(self):self.reject(self.mutate('HIGHLIGHT','state',0))
    def test_missing_coin_or_start_pulse_rejected(self):
        self.reject(re.sub(r'^MK2_JOIN_LIFE_CONTROL [^\r\n]*\r?\n','',self.logs['kano'],count=1,flags=re.M))
    def test_attach_after_match_rejected(self):self.reject(self.mutate('ATTACH','frame',99999))
    def test_match_full_health_rejected(self):self.reject(self.mutate('MATCH','hp',160))
    def test_wrong_proxy_actor_identity_rejected(self):self.reject(self.mutate('FIELD','id',1))
    def test_missing_whole_joined_field_rejected(self):
        self.reject(re.sub(r'^MK2_JOIN_LIFE_FIELD [^\r\n]*\r?\n','',self.logs['kano'],count=1,flags=re.M))
    def test_rogue_health_writer_rejected(self):self.reject(self.mutate('HEALTH','pc','FF9DECE0',where='before=161 after=135 '))
    def test_wrong_native_hud_refill_pc_rejected(self):self.reject(self.mutate('HEALTH','pc','FF9DEF70',where='slot=1 before=65535 '))
    def test_wrong_native_hud_sentinel_rejected(self):self.reject(self.mutate('HEALTH','after',4,where='slot=1 before=161 after=65535 '))
    def test_fake_health_refill_chain_rejected(self):self.reject(self.mutate('HEALTH','before',3,where='slot=1 before=4 after=6 '))
    def test_native_round_construction_mode_rejected(self):self.reject(self.mutate('FIELD','mode',2,where='actor=00000000 '))
    def test_native_round_construction_slot_retirement_rejected(self):self.reject(self.mutate('FIELD','actor','01000000',where='actor=00000000 '))
    def test_native_match_controller_rejected(self):self.reject(self.mutate('FIELD','state',0))
    def test_result_only_cannot_prove_moves(self):
        self.reject(re.sub(r'^MK2_LIFE_TRACE_[^\r\n]*\r?\n','',self.logs['kano'],flags=re.M))
    def test_wrong_result_field_count_rejected(self):self.reject(self.mutate('RESULT','fields',601))
    def test_observer_write_rejected(self):self.reject(self.mutate('FIELD','writes',1))


class FullEndingJoinedLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(target,side):(ROOT/f'audit_v289_{"ending" if side==1 else "slot_reset"}_join_{"blade" if target=="kano" else "bicycle"}_p{side}/run.log').read_text(encoding='utf-8-sig') for target in ('kano','sonya') for side in (1,2)}

    def grade(self,log,target='kano',side=1):
        return verify_restart(log,'sonya' if target=='kano' else 'kano',target,1,side,'lifecycle')

    def reject(self,log,target='kano',side=1):
        self.assertNotEqual(log,self.logs[target,side]);self.assertFalse(self.grade(log,target,side)['passed'])

    def test_actual_all_four_full_source_endings_restarts_joins(self):
        for (target,side),log in self.logs.items():
            self.assertTrue(self.grade(log,target,side)['passed'],self.grade(log,target,side))
            self.assertTrue(verify_assistance(log,'sonya' if target=='kano' else 'kano',1)['passed'])
    def test_cold_diag_not_full_source_proof(self):
        for target in ('kano','sonya'):
            move='blade' if target=='kano' else 'bicycle'
            s=(ROOT/f'audit_v289_native_join_{move}/run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(self.grade(s,target)['passed'])
    def test_missing_own_ending_picture_rejected(self):
        self.reject(re.sub(r'^MK2_RESTART_PICTURE [^\r\n]*page=2[^\r\n]*\r?\n','',self.logs['kano',1],flags=re.M))
    def test_missing_own_ending_text_rejected(self):
        self.reject(re.sub(r'^MK2_RESTART_TEXT [^\r\n]*page=2[^\r\n]*\r?\n','',self.logs['kano',1],flags=re.M))
    def test_missing_full_tower_summary_rejected(self):
        self.reject(re.sub(r'^MK2KS_MULTI_FINAL[^\r\n]*\r?\n','',self.logs['kano',1],flags=re.M))
    def test_wrong_fresh_match_epoch_rejected(self):
        self.reject(re.sub(r'(MK2_RESTART_COMPLETE frame=)\d+',r'\g<1>1',self.logs['kano',1]))
    def test_wrong_fresh_slot_scope_rejected(self):
        self.assertFalse(self.grade(self.logs['kano',2],'kano',1)['passed'])
    def test_wrong_special_character_rejected(self):
        self.assertFalse(self.grade(self.logs['sonya',1],'kano',1)['passed'])
    def test_parent_cannot_ignore_missing_native_lifecycle(self):
        self.reject(re.sub(r'^MK2_LIFE_TRACE_[^\r\n]*\r?\n','',self.logs['kano',1],flags=re.M))
    def test_native_post_restart_health_assistance_excluded(self):
        log=self.logs['kano',1]
        attract=re.search(r'MK2_RESTART_ATTRACT frame=(\d+)',log)[1]
        self.assertFalse(verify_assistance(log+'\nMK2KS_DIAGNOSTIC_HEALTH_WRITE frame='+attract+'\n','sonya',1)['passed'])
    def test_wrong_original_slot_reset_pc_rejected(self):
        log=self.logs['kano',2]
        changed=re.sub(r'(MK2_JOIN_LIFE_HEALTH[^\r\n]*slot=1 before=0 after=161 pc=)FF825930',r'\g<1>FF825960',log)
        self.reject(changed,'kano',2)


if __name__=='__main__':unittest.main()
