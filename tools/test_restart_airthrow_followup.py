"""Both own controllers really work after a full restarted/joined air throw."""
import re
import unittest
from pathlib import Path
from verify_restart_airthrow import verify
from verify_post_ending_restart import verify as verify_restart
from check_post_restart_assistance import verify as verify_assistance

ROOT=Path(__file__).resolve().parents[1]


class AirThrowFollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={side:(ROOT/f'audit_v287_fractional_followup_p{side}_kano_sonya/run.log').read_text(encoding='utf-8-sig') for side in (1,2)}

    def reject(self,log,side=1):
        self.assertNotEqual(log,self.logs[side], 'Mutation did not change the actual fixture')
        self.assertFalse(verify(log,side=side,require_followup=True)['passed'])

    def change(self,tag,key,value,side=1):
        return re.sub(r'^MK2_AIR_JOIN_'+tag+r' [^\r\n]*',
            lambda m:re.sub(r'(\b'+key+r'=)[^\s]+',lambda a:a[1]+str(value),m[0],count=1),self.logs[side],flags=re.M)

    def epoch(self,side=1):
        return int(re.search(r'^MK2_AIR_JOIN_FOLLOW_PLAN[^\r\n]* begin=(\d+)',self.logs[side],re.M)[1])

    def field_change(self,elapsed,key,value,side=1):
        frame=self.epoch(side)+elapsed
        return re.sub(r'^MK2_AIR_JOIN_FIELD frame='+str(frame)+r' [^\r\n]*',
            lambda m:re.sub(r'(\b'+key+r'=)[^\s]+',lambda a:a[1]+str(value),m[0],count=1),self.logs[side],flags=re.M)

    def test_full_both_slots_endings_join_moves_and_normal_followups(self):
        for side,log in self.logs.items():
            result=verify(log,side=side,require_followup=True)
            self.assertTrue(result['passed'],result['errors'])
            self.assertTrue(result['followup_verified'])
            self.assertEqual(result['victim'],'sonya')
            self.assertFalse(result['full_goal_complete'])
            source='sonya' if side==1 else 'kano'
            result=verify_restart(log,source,'kano',1,side,'airthrow',True)
            self.assertTrue(result['passed'],result['errors'])
            result=verify_assistance(log,source,1)
            self.assertTrue(result['passed'],result['errors'])

    def test_previous_idle_only_cases_cannot_prove_normal_followup(self):
        for side,folder in ((1,'audit_v286_after_ending_join_p1_kano'),(2,'audit_v286_ordered_join_p2_kano')):
            log=(ROOT/folder/'run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log,side=side,require_followup=True)['passed'])

    def test_cold_diagnostics_never_substitute_after_ending_proof(self):
        log=(ROOT/'audit_v287_cold_fractional_followup_kano_sonya/run.log').read_text(encoding='utf-8-sig')
        result=verify(log,require_followup=True)
        self.assertFalse(result['passed'])
        self.assertEqual(result['errors'],['Fresh target epoch missing (cold probes are not acceptance)',
                                         'Join must follow exact actual 601-field post-ending completion'])

    def test_missing_plan_or_real_controls(self):
        for tag in ('FOLLOW_PLAN','FOLLOW_CONTROL','FOLLOW_EVENT','FOLLOW_RESULT'):
            self.reject(re.sub(r'^MK2_AIR_JOIN_'+tag+r' [^\r\n]*\r?\n','',self.logs[1],flags=re.M))

    def test_plan_timing_and_buttons_exact(self):
        for key,value in (('begin',0),('walk','0,1'),('jump','40,1'),('hp','112,1'),('block','136,1'),('settle',140)):
            self.reject(self.change('FOLLOW_PLAN',key,value))
        self.reject(self.change('FOLLOW_CONTROL','value',0))
        self.reject(self.change('FOLLOW_CONTROL','slot',3))

    def test_original_jump_entry_and_native_ownership(self):
        for key,value in (('entry','FF876650'),('pc','FF876660'),('a8','01000000'),('a13','01000000'),('actor','01000000'),('main','01000000')):
            self.reject(self.change('FOLLOW_EVENT',key,value))

    def test_real_jump_parameters_and_cleared_callback(self):
        for key,value in (('a0','00030000'),('a1','FFF80000'),('a2','00007000'),('a6','FFFFF800')):
            self.reject(self.change('FOLLOW_EVENT',key,value))
        for side in (1,2):
            self.reject(self.field_change(64,'callback','FFFFF800',side),side)
            self.reject(self.field_change(64,'vcallback','FFFFF800',side),side)

    def test_exact_followup_trajectory_including_fractional_start(self):
        for side in (1,2):
            for key,value in (('y',0),('vy','00000000'),('yraw','00000000'),('vyraw','00000000')):
                self.reject(self.field_change(64,key,value,side),side)

    def test_own_imported_jump_poses_not_proxy(self):
        for key in ('pose','vpose'):
            self.reject(self.field_change(64,key,'FF977350'))

    def test_actual_walking_velocity_and_displacement(self):
        self.reject(self.field_change(8,'vx','00030000'))
        self.reject(self.field_change(8,'vvx','00030000'))
        self.reject(self.field_change(8,'action','0109'))

    def test_native_punch_and_block_not_idle(self):
        for tag,key in (('action','0101'),('vaction','0101')):
            log=re.sub(r'^MK2_AIR_JOIN_FIELD [^\r\n]*',lambda m:m[0].replace(tag+'='+key,tag+'=0303'),self.logs[1],flags=re.M)
            self.reject(log)
        for key in ('action','vaction'):
            log=re.sub(r'^MK2_AIR_JOIN_FIELD [^\r\n]*',lambda m:m[0].replace(key+'=0700',key+'=0303'),self.logs[1],flags=re.M)
            self.reject(log)

    def test_native_normal_punch_health_writer_and_context(self):
        for key,value in (('pc','FFFFF100'),('a8','01000000'),('a13','01000000'),('delta',16),('before',99),('after',99),('slot',3)):
            self.reject(self.change('FOLLOW_HEALTH',key,value))
        self.reject(re.sub(r'^MK2_AIR_JOIN_FOLLOW_HEALTH [^\r\n]*\r?\n','',self.logs[1],flags=re.M))

    def test_health_never_changes_without_actual_original_store(self):
        self.reject(self.field_change(124,'hp',1))
        self.reject(self.field_change(124,'vhp',1))

    def test_native_hit_flags_and_body_clear_after_followup(self):
        for key,value in (('flags','0005'),('vflags','0005'),('body','001A'),('vbody','0016'),('trail','01000000'),('vtrail','01000000')):
            self.reject(self.field_change(160,key,value))

    def test_followup_snapshots_match_actual_field_observations(self):
        self.reject(self.change('FOLLOW_SAMPLE','pose','FF977350'))
        self.reject(self.change('FOLLOW_SAMPLE','frame',0))

    def test_summary_must_follow_real_complete_controls(self):
        self.reject(self.change('FOLLOW_RESULT','pass','false'))
        self.reject(self.change('FOLLOW_RESULT','fields',160))
        self.reject(self.change('FOLLOW_RESULT','begin',0))
        self.reject(self.change('FOLLOW_RESULT','writes',1))

    def test_post_followup_idle_and_ground_stay_clean(self):
        for key,value in (('action','0109'),('vaction','0000'),('y',0),('vy','00008000'),('vx','00028000')):
            if key=='vaction':value='0506'
            self.reject(self.field_change(190,key,value))

    def test_original_throw_evidence_still_required(self):
        self.reject(re.sub(r'^MK2_AIR_JOIN_HEALTH [^\r\n]*\r?\n','',self.logs[1],flags=re.M))
        self.reject(self.change('RESULT','damage',32))


if __name__=='__main__':
    unittest.main()
