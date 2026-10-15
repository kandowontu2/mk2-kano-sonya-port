"""Actual full ending/restart/native-join air throws and evidence mutations."""
import re
import unittest
from pathlib import Path

from verify_restart_airthrow import verify, ENTRIES
from verify_post_ending_restart import verify as verify_restart
from check_post_restart_assistance import verify as verify_assistance

ROOT=Path(__file__).resolve().parents[1]


class RestartAirThrowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={1:(ROOT/'audit_v286_after_ending_join_p1_kano/run.log').read_text(encoding='utf-8-sig'),
                  2:(ROOT/'audit_v286_ordered_join_p2_kano/run.log').read_text(encoding='utf-8-sig')}

    def change(self,tag,key,value,side=1,kind=None):
        pattern=r'^MK2_AIR_JOIN_'+tag+r' [^\r\n]*'
        def mutate(item):
            line=item[0]
            if kind and ' kind='+kind+' ' not in line:
                return line
            return re.sub(r'(\b'+key+r'=)[^\s]+',lambda m:m[1]+str(value),line,count=1)
        return re.sub(pattern,mutate,self.logs[side],flags=re.M)

    def reject(self,changed,side=1):
        self.assertNotEqual(changed,self.logs[side], 'Mutation did not affect actual fixture')
        self.assertFalse(verify(changed,side=side)['passed'])

    def test_actual_both_slots_native_join_throw_and_cleanup(self):
        for side,log in self.logs.items():
            result=verify(log,side=side)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual(result['joined_fields'],601)
            self.assertGreaterEqual(result['native_events']['callback'],20)
            self.assertFalse(result['full_goal_complete'])

    def test_full_source_endings_restart_and_assistance_stop(self):
        for side,log in self.logs.items():
            source='sonya' if side==1 else 'kano'
            result=verify_restart(log,source,'kano',1,side,'airthrow')
            self.assertTrue(result['passed'],result['errors'])
            result=verify_assistance(log,source,1)
            self.assertTrue(result['passed'],result['errors'])

    def test_cold_diagnostics_not_after_ending_acceptance(self):
        for folder in ('audit_v286_cold_join_kano_sonya','audit_v286_cold_join_idle_kano_sonya','audit_v286_cold_guarded_join_kano_sonya'):
            log=(ROOT/folder/'run.log').read_text(encoding='utf-8-sig')
            self.assertFalse(verify(log)['passed'])

    def test_missing_actual_each_native_phase(self):
        for kind in ENTRIES:
            with self.subTest(kind=kind):
                self.reject(re.sub(r'^MK2_AIR_JOIN_EVENT[^\r\n]* kind='+kind+r' [^\r\n]*\r?\n','',self.logs[1],flags=re.M))

    def test_wrong_side_or_character(self):
        self.assertFalse(verify(self.logs[1],side=2)['passed'])
        self.assertFalse(verify(self.logs[2],target='sonya',side=2)['passed'])

    def test_canonical_live_identity_alias_rejected(self):
        for key in ('id','roster','vid','vroster'):
            self.reject(self.change('FIELD',key,1))

    def test_joined_two_human_roles_required(self):
        for key in ('state','vstate'):
            self.reject(self.change('FIELD',key,0))
        self.reject(self.change('BEGIN','p2','1,18'))

    def test_actual_select_identity_and_topology(self):
        self.reject(self.change('CSS','route','right,right'))
        self.reject(self.change('HIGHLIGHT','roster',1))
        self.reject(self.change('HIGHLIGHT','state',0))

    def test_missing_real_coin_start_join(self):
        self.reject(re.sub(r'^MK2_AIR_JOIN_INPUT[^\r\n]* button=start [^\r\n]*\r?\n','',self.logs[1],flags=re.M))

    def test_actual_jump_and_block_controls(self):
        self.reject(re.sub(r'^MK2_AIR_JOIN_CONTROL[^\r\n]* button=up [^\r\n]*\r?\n','',self.logs[1],flags=re.M))
        self.reject(self.change('CONTROL','value',0))
        self.reject(self.change('COMMAND','button','hp'))
        self.reject(self.change('COMMAND','hold',5))

    def test_complete_field_coverage(self):
        self.reject(re.sub(r'^MK2_AIR_JOIN_FIELD[^\r\n]*\r?\n','',self.logs[1],count=1,flags=re.M))

    def test_native_code_pose_roots_and_descriptors(self):
        for key,value in (('block_gate','FF877420'),('root','FF980000'),('poses','FE828E80'),('alignment','FFB5000A'),('flight_pose','FF02DD00')):
            self.reject(self.change('ROM',key,value))

    def test_actual_action_not_jax_or_knife(self):
        self.reject(self.change('EVENT','entry','FFFFB000',kind='action'))
        self.reject(self.change('EVENT','pc','FF8B7020',kind='action'))

    def test_executing_actor_and_process_bound(self):
        for side in (1,2):
            for kind in ('gate','action','flight','callback','bounce','own_recovery','victim_recovery'):
                self.reject(self.change('EVENT','a8','01000000',side,kind),side)
                self.reject(self.change('EVENT','a13','00000000',side,kind),side)

    def test_actual_damage_amount_and_native_health_store(self):
        self.reject(self.change('EVENT','a0','00000020',kind='damage'))
        for key,value in (('pc','FFFFF100'),('delta',32),('after',129),('before',160),('a8','01000000'),('a13','01000000')):
            self.reject(self.change('HEALTH',key,value))

    def test_missing_actual_health_write(self):
        self.reject(re.sub(r'^MK2_AIR_JOIN_HEALTH[^\r\n]*\r?\n','',self.logs[1],flags=re.M))

    def test_health_continuity(self):
        self.reject(self.change('FIELD','vhp',129))

    def test_catch_pose_and_alignment(self):
        log=self.logs[1]
        af=int(re.search(r'^MK2_AIR_JOIN_EVENT frame=(\d+)[^\r\n]* kind=action ',log,re.M)[1])
        for key,value in (('pose','FF00DC40'),('vxpos',0),('vypos',0),('action','0303')):
            changed=re.sub(r'^MK2_AIR_JOIN_FIELD frame='+str(af+1)+r' [^\r\n]*',
                lambda m:re.sub(r'(\b'+key+r'=)[^\s]+',lambda x:x[1]+str(value),m[0],count=1),log,flags=re.M)
            self.reject(changed)

    def test_actual_native_flight_callback(self):
        self.reject(self.change('EVENT','a6','00000000',kind='callback'))
        for side,log in self.logs.items():
            flight=int(re.search(r'^MK2_AIR_JOIN_EVENT frame=(\d+)[^\r\n]* kind=flight ',log,re.M)[1])
            bounce=int(re.search(r'^MK2_AIR_JOIN_EVENT frame=(\d+)[^\r\n]* kind=bounce ',log,re.M)[1])
            for field,key,value in ((flight+2,'vvx','00000000'),(flight+3,'vvy','00000000'),
                                    (flight+3,'vpose','FF02DD00'),(bounce+1,'vvy','00000000'),
                                    (bounce+2,'vvx','00030000')):
                changed=re.sub(r'^MK2_AIR_JOIN_FIELD frame='+str(field)+r' [^\r\n]*',
                    lambda m:re.sub(r'(\b'+key+r'=)[^\s]+',lambda x:x[1]+value,m[0],count=1),log,flags=re.M)
                self.reject(changed,side)

    def test_native_event_timing(self):
        self.reject(self.change('EVENT','frame',1,kind='release'))
        self.reject(self.change('EVENT','count',2,kind='action'))

    def test_missing_sustained_recovered_fields(self):
        self.reject(self.change('FINAL','frame',9))

    def test_clean_grounded_control_state(self):
        for key,value in (('action','0109'),('y',0),('vy','00008000'),('vx','00030000'),('flags','0011'),('body','001A'),('body','0016'),('vbody','0016'),('trail','01000000'),('vaction','0506'),('vflags','0005'),('vtrail','01000000')):
            self.reject(self.change('READY',key,value))

    def test_summary_cannot_replace_events(self):
        changed=re.sub(r'^MK2_AIR_JOIN_(EVENT|HEALTH|FIELD)[^\r\n]*\r?\n','',self.logs[1],flags=re.M)
        self.reject(changed)

    def test_claimed_summary_must_match_actual_native_evidence(self):
        for key,value in (('damage',32),('stores',0),('caught',0),('own_recovery',0),('victim_recovery',0),('writes',1)):
            self.reject(self.change('RESULT',key,value))

    def test_runtime_errors_not_ignored(self):
        self.reject(self.logs[1]+'\nMK2_AIR_JOIN_ERROR genuine failure\n')

    def test_previous_close_pair_cannot_prove_airthrow(self):
        log=(ROOT/'audit_v285_cross_slot_pair_p1_kano/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log)['passed'])


if __name__=='__main__':
    unittest.main()
