"""Actual current-build full move traces must survive independent tampering QA."""
import re
import unittest
from pathlib import Path
from verify_current_lifecycle import verify

ROOT=Path(__file__).resolve().parents[1]


class CurrentLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(move,side):(ROOT/f'audit_v288_{"boundary_" if move=="bicycle" else ""}{move}_p{side}_{"sonya" if move=="blade" else "kano"}/run.log').read_text(encoding='utf-8-sig') for move in ('blade','bicycle') for side in (1,2)}

    def grade(self,log,move='blade',side=1):
        return verify(log,move,side,'sonya' if move=='blade' else 'kano')

    def reject(self,log,move='blade',side=1):
        self.assertNotEqual(log,self.logs[move,side],'Mutation must affect actual fixture')
        self.assertFalse(self.grade(log,move,side)['passed'])

    def mutate(self,tag,key,value,move='blade',where='cycle=1 ',side=1):
        done=False
        def replace(match):
            nonlocal done
            if done or where not in match[0]:return match[0]
            changed=re.sub(r'(\b'+key+r'=)[^\s]+',lambda m:m[1]+str(value),match[0],count=1)
            done=changed!=match[0];return changed
        return re.sub(r'^MK2_LIFE_TRACE_'+tag+r' [^\r\n]*',replace,self.logs[move,side],flags=re.M)

    def test_actual_both_moves_both_slots(self):
        for (move,side),log in self.logs.items():self.assertTrue(self.grade(log,move,side)['passed'],self.grade(log,move,side))

    def test_old_untraced_weak_summary_rejected(self):
        self.reject(re.sub(r'^MK2_LIFE_TRACE_[^\r\n]*\r?\n','',self.logs['blade',1],flags=re.M))

    def test_original_bicycle_trace_without_boundary_evidence_rejected(self):
        log=(ROOT/'audit_v288_bicycle_p1_kano/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(self.grade(log,'bicycle')['passed'])

    def test_missing_actual_field_rejected(self):
        self.reject(re.sub(r'^MK2_LIFE_TRACE_FIELD [^\r\n]*\r?\n','',self.logs['blade',1],count=1,flags=re.M))

    def test_duplicate_and_wrong_epoch_rejected(self):self.reject(self.mutate('FIELD','frame',0))
    def test_proxy_actor_id_rejected(self):self.reject(self.mutate('FIELD','id',1))
    def test_cpu_participation_in_human_trace_rejected(self):self.reject(self.mutate('FIELD','state',0))
    def test_wrong_main_owner_rejected(self):self.reject(self.mutate('EVENT','a13','01000000',where='kind=action '))
    def test_wrong_action_entry_rejected(self):self.reject(self.mutate('EVENT','entry','FFF91400',where='kind=action '))
    def test_wrong_native_damage_writer_rejected(self):self.reject(self.mutate('HEALTH','pc','FF836710'))
    def test_damage_health_ledger_rejected(self):self.reject(self.mutate('FIELD','hp',160))
    def test_wrong_damage_victim_slot_rejected(self):self.reject(self.mutate('HEALTH','slot',1))
    def test_wrong_damage_amount_rejected(self):self.reject(self.mutate('HEALTH','after',134))
    def test_missing_damage_event_rejected(self):self.reject(re.sub(r'^MK2_LIFE_TRACE_HEALTH [^\r\n]*\r?\n','',self.logs['blade',1],count=1,flags=re.M))
    def test_blade_pose_hold_rejected(self):self.reject(self.mutate('FIELD','pose','FE82FFA0',where='cycle=1 age=9 slot=1 '))
    def test_blade_trail_descriptor_rejected(self):self.reject(self.mutate('FIELD','descriptor','FFF8F900',where='cycle=1 age=9 slot=1 '))
    def test_missing_blood_cleanup_rejected(self):self.reject(re.sub(r'^MK2_LIFE_TRACE_EVENT [^\r\n]*kind=blood_cleanup [^\r\n]*\r?\n','',self.logs['blade',1],count=1,flags=re.M))
    def test_wrong_blood_victim_rejected(self):self.reject(self.mutate('EVENT','a11','01034E90',where='kind=blood_allocate '))
    def test_bicycle_paired_pose_rejected(self):self.reject(self.mutate('FIELD','pose','FE83EB40','bicycle',where='cycle=1 age=25 slot=1 '),'bicycle')
    def test_bicycle_victim_pose_rejected(self):self.reject(self.mutate('FIELD','pose','FE829680','bicycle',where='cycle=1 age=25 slot=2 '),'bicycle')
    def test_bicycle_paired_offset_rejected(self):self.reject(self.mutate('FIELD','x',0,'bicycle',where='cycle=1 age=25 slot=2 '),'bicycle')
    def test_bicycle_fixed_point_trajectory_rejected(self):self.reject(self.mutate('FIELD','yraw','00000000','bicycle',where='cycle=1 age=25 slot=1 '),'bicycle')
    def test_wrong_native_boundary_pc_rejected(self):
        log=re.sub(r'(MK2_LIFE_TRACE_VELOCITY [^\r\n]*pc=)FF805610',r'\g<1>FF805600',self.logs['bicycle',1])
        self.reject(log,'bicycle')
    def test_wrong_native_boundary_actor_rejected(self):
        log=re.sub(r'^MK2_LIFE_TRACE_VELOCITY [^\r\n]*',lambda m:re.sub(r'a2=[^\s]+','a2=01000000',m[0]),self.logs['bicycle',1],flags=re.M)
        self.reject(log,'bicycle')
    def test_stale_surviving_hit_flag_rejected(self):self.reject(self.mutate('FIELD','flags','0005','bicycle',where='cycle=1 age=200 slot=2 '),'bicycle')
    def test_native_victim_fling_rejected(self):self.reject(self.mutate('EVENT','a2','00008000','bicycle',where='kind=fling '),'bicycle')
    def test_missing_next_round_rejected(self):self.reject(re.sub(r'^MK2KS_BLADE_LIFECYCLE_NEXT_ROUND[^\r\n]*','',self.logs['blade',1],flags=re.M))
    def test_changed_next_round_health_rejected(self):self.reject(self.mutate('FIELD','hp',5,where='cycle=8 age=0 slot=2 '))
    def test_missing_actual_recovery_rejected(self):self.reject(re.sub(r'^MK2_LIFE_TRACE_EVENT [^\r\n]*kind=recovery [^\r\n]*\r?\n','',self.logs['blade',1],flags=re.M))
    def test_observer_write_rejected(self):self.reject(self.mutate('FIELD','writes',1))


if __name__=='__main__':unittest.main()
