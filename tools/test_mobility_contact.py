"""Current native-contact fixtures plus deliberate missing/tampered evidence."""
import re
import unittest
from pathlib import Path
from verify_mobility_contact import verify
from verify_restart_lifecycle import verify_mobility_join
from verify_post_ending_restart import verify as verify_restart
from check_post_restart_assistance import verify as verify_assistance

ROOT=Path(__file__).resolve().parents[1]


class ColdContactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={name:(ROOT/f'audit_v290_{name}/run.log').read_text(encoding='utf-8-sig') for name in
                  ('separation_ball_hit','root_square_hit','ball_block','ball_duck_miss','square_ground_block','square_far_miss')}

    def mutate(self,tag,key,value,name='separation_ball_hit',where=''):
        changed=False
        def replace(m):
            nonlocal changed
            if changed or where not in m[0]:return m[0]
            result=re.sub(r'(\b'+key+r'=)[^\s]+',lambda n:n[1]+str(value),m[0],count=1)
            changed=result!=m[0];return result
        return re.sub(r'^MK2_MOB_CONTACT_'+tag+r' [^\r\n]*',replace,self.logs[name],flags=re.M)

    def reject(self,log,target='kano'):
        self.assertFalse(verify_mobility_join(log,target,1,False)['passed'])

    def test_six_actual_cold_contact_paths(self):
        for name,log in self.logs.items():
            self.assertTrue(verify_mobility_join(log,'kano' if 'ball' in name else 'sonya',1,False)['passed'],name)
    def test_cold_runs_cannot_prove_ending(self):
        for name,log in self.logs.items():
            self.assertFalse(verify_mobility_join(log,'kano' if 'ball' in name else 'sonya',1)['passed'])
    def test_original_missing_separation_observation_stays_insufficient(self):
        log=(ROOT/'audit_v290_root_ball_hit/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify_mobility_join(log,'kano',1,False)['passed'])
    def test_result_only_is_not_contact_proof(self):
        self.reject(re.sub(r'^MK2_MOB_CONTACT_(FIELD|EVENT|HEALTH|CONTROL)[^\r\n]*\r?\n','',self.logs['separation_ball_hit'],flags=re.M))
    def test_wrong_live_fighter_rejected(self):self.reject(self.mutate('FIELD','id',1))
    def test_wrong_human_controller_rejected(self):self.reject(self.mutate('FIELD','state',0))
    def test_missing_actual_field_rejected(self):
        self.reject(re.sub(r'^MK2_MOB_CONTACT_FIELD[^\r\n]*\r?\n','',self.logs['separation_ball_hit'],count=1,flags=re.M))
    def test_wrong_native_charge_threshold_rejected(self):self.reject(self.mutate('EVENT','a1','00000050',where='kind=elapsed '))
    def test_missing_charge_field_rejected(self):
        self.reject(re.sub(r'^MK2_MOB_CONTACT_CONTROL[^\r\n]*button=lk[^\r\n]*\r?\n','',self.logs['separation_ball_hit'],count=1,flags=re.M))
    def test_wrong_damage_rejected(self):self.reject(self.mutate('HEALTH','after',138,where='before=161 after=137 '))
    def test_wrong_native_damage_owner_rejected(self):self.reject(self.mutate('HEALTH','a8','010350A0',where='before=161 after=137 '))
    def test_wrong_native_damage_writer_rejected(self):self.reject(self.mutate('HEALTH','pc','FF825960'))
    def test_wrong_descriptor_rejected(self):self.reject(self.mutate('DESCRIPTOR','values','57,14,72,31,1417,1804,0,0,1'))
    def test_wrong_own_roll_pose_rejected(self):self.reject(self.mutate('FIELD','pose','FF00EB80',where='pose=FF00EB40 '))
    def test_wrong_horizontal_flight_step_rejected(self):self.reject(self.mutate('FIELD','xraw','01EA0001',where='age=265 slot=1 '))
    def test_wrong_own_square_flight_pose_rejected(self):self.reject(self.mutate('FIELD','pose','FF031380','root_square_hit','pose=FF031340 '),'sonya')
    def test_wrong_square_pause_pose_rejected(self):self.reject(self.mutate('FIELD','pose','FF031340','root_square_hit','pose=FF031480 '),'sonya')
    def test_wrong_rebound_gravity_rejected(self):self.reject(self.mutate('FIELD','gravity','00005000',where='gravity=00006000 '))
    def test_wrong_full_fractional_trajectory_rejected(self):self.reject(self.mutate('FIELD','yraw','004A6001',where='yraw=004A6000 '))
    def test_wrong_separation_limit_writer_rejected(self):self.reject(self.mutate('VELOCITY','pc','FF805580',where='age=297 slot=1 '))
    def test_wrong_separation_limit_request_rejected(self):self.reject(self.mutate('VELOCITY','request','FFFF0000',where='age=297 slot=1 '))
    def test_wrong_separation_correction_rejected(self):self.reject(self.mutate('VELOCITY','a5','00000001',where='age=297 slot=1 '))
    def test_missing_subsequent_native_control_rejected(self):
        self.reject(re.sub(r'^MK2_MOB_CONTACT_EVENT[^\r\n]*kind=projectile[^\r\n]*\r?\n','',self.logs['separation_ball_hit'],flags=re.M))
    def test_unclean_recovery_rejected(self):self.reject(self.mutate('FIELD','trail','01000000',where='age=440 slot=1 '))
    def test_observer_write_rejected(self):self.reject(self.mutate('FIELD','writes',1))


class P2EndingContactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(target,side):(ROOT/(f'audit_v290_observer_guard_join_square_p1' if target=='sonya' and side==1 else
                                     f'audit_v290_p2_ending_join_{"ball" if target=="kano" else "square"}_p{side}')/'run.log').read_text(encoding='utf-8-sig')
                  for target in ('kano','sonya') for side in (1,2)}
    def check_rejected(self,change):
        for (target,side),log in self.logs.items():
            source='sonya' if target=='kano' else 'kano'
            altered=change(log);self.assertNotEqual(altered,log)
            self.assertFalse(verify_restart(altered,source,target,2,side,'mobility_contact')['passed'])
    def test_four_actual_full_p2_ending_cases(self):
        for (target,side),log in self.logs.items():
            source='sonya' if target=='kano' else 'kano'
            self.assertTrue(verify_restart(log,source,target,2,side,'mobility_contact')['passed'])
            self.assertTrue(verify_assistance(log,source,2)['passed'])
    def test_original_observer_self_reads_are_not_gameplay_proof(self):
        log=(ROOT/'audit_v290_p2_ending_join_square_p1/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify_restart(log,'kano','sonya',2,1,'mobility_contact')['passed'])
    def test_missing_source_ending_page_rejected(self):
        self.check_rejected(lambda s:re.sub(r'^MK2_RESTART_PICTURE[^\r\n]*\r?\n','',s,count=1,flags=re.M))
    def test_missing_p2_tower_completion_rejected(self):
        self.check_rejected(lambda s:re.sub(r'^MK2_P2_TOWER_COMPLETED[^\r\n]*\r?\n','',s,flags=re.M))
    def test_missing_fresh_cpu_match_rejected(self):
        self.check_rejected(lambda s:re.sub(r'^MK2_RESTART_MATCH[^\r\n]*\r?\n','',s,flags=re.M))
    def test_missing_fresh_601_completion_rejected(self):
        self.check_rejected(lambda s:re.sub(r'^MK2_RESTART_COMPLETE[^\r\n]*\r?\n','',s,flags=re.M))
    def test_missing_actual_join_selection_rejected(self):
        self.check_rejected(lambda s:re.sub(r'^MK2_JOIN_LIFE_HIGHLIGHT[^\r\n]*\r?\n','',s,count=1,flags=re.M))
    def test_missing_full_contact_trace_rejected(self):
        self.check_rejected(lambda s:re.sub(r'^MK2_MOB_CONTACT_FIELD[^\r\n]*\r?\n','',s,flags=re.M))
    def test_wrong_source_slot_rejected(self):
        for (target,side),log in self.logs.items():
            self.assertFalse(verify_restart(log,'sonya' if target=='kano' else 'kano',target,1,side,'mobility_contact')['passed'])
    def test_post_ending_health_assistance_rejected(self):
        for (target,side),log in self.logs.items():
            at=re.search(r'MK2_RESTART_ATTRACT frame=(\d+)',log)[1]
            self.assertFalse(verify_assistance(log+'\nMK2_P2_TOWER_HEALTH frame='+at+' side=2 stage=0 old=1 new=161\n','sonya' if target=='kano' else 'kano',2)['passed'])
