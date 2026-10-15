"""Current naturally chosen CPU cases and actual malformed-evidence rejection."""
import re
import unittest
from verify_natural_cpu_moves_v545 import ROOT, verify, verify_log, SPECS, rows

CASES=('kano_boot605','kano_boot606','sonya_boot601','sonya_boot604')
FOLDERS={name:ROOT/f'audit_v554_cpu_{name}' for name in CASES}


class NaturalCPU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={name:(FOLDERS[name]/'run.log').read_text(encoding='utf-8-sig') for name in CASES}
        for name in CASES:
            baseline=verify(FOLDERS[name])
            assert baseline['passed'], (name, baseline['errors'])

    def test_all_four_actual_natural_runs(self):
        union=set()
        for name in CASES:
            result=verify(FOLDERS[name])
            self.assertTrue(result['passed'],(name,result['errors']))
            union.update(result['observed_moves'])
        self.assertEqual(union,set(SPECS)-{'ring'})

    def reject(self,tag,key=None,value=None,name='kano_boot605',predicate=lambda line:True):
        changed=False
        def replace(m):
            nonlocal changed
            if changed or not predicate(m[0]): return m[0]
            changed=True
            return '' if key is None else re.sub(r'(\b'+key+r'=)[^\s]+',lambda n:n[1]+str(value),m[0],count=1)
        log=re.sub(r'^MK2_NAT_CPU_'+tag+r' [^\r\n]*',replace,self.logs[name],flags=re.M)
        self.assertTrue(changed and log!=self.logs[name])
        self.assertFalse(verify_log(log,'sonya',17 if name.startswith('kano') else 18)['passed'])

    def first_entry(self):
        return rows(self.logs['kano_boot605'], 'ENTRY')[0]

    def first_ready(self):
        entry = self.first_entry()
        return next(r for r in rows(self.logs['kano_boot605'], 'EVENT')
                    if r['kind']=='ready' and r['frame']>entry['frame'] and
                    (r['actor'],r['main'])==(entry['actor'],entry['main']))['frame']

    def test_no_summary_only_proof(self):
        log=re.sub(r'^MK2_NAT_CPU_(FIELD|ENTRY|GROUP|CHILD|EFFECT|EVENT|HEALTH)[^\r\n]*\r?\n','',self.logs['kano_boot605'],flags=re.M)
        self.assertFalse(verify_log(log,'sonya',17)['passed'])

    def test_wrong_natural_order(self): self.reject('FIELD','scheduled',18,predicate=lambda line:'slot=2 ' in line)
    def test_wrong_entry_cpu_role(self): self.reject('ENTRY','state',1)
    def test_wrong_entry_native_owner(self): self.reject('ENTRY','main','01034E90')
    def test_wrong_first_callback_identity(self): self.reject('FIELD','id',1,predicate=lambda line:f"frame={self.first_entry()['frame']+1} slot=2 " in line)
    def test_missing_first_callback(self): self.reject('FIELD',predicate=lambda line:'frame=1643 slot=2 ' in line,name='sonya_boot601')
    def test_old_no_entry_role_schema_is_insufficient(self):
        log=(ROOT/'audit_v315_natural_cpu_kano_boot606/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify_log(log,'sonya',17)['passed'])
    def test_wrong_native_ready_pc(self): self.reject('EVENT','pc','FF861370',predicate=lambda line:f'frame={self.first_ready()} kind=ready ' in line)
    def test_missing_recovery_field(self): self.reject('FIELD',predicate=lambda line:f'frame={self.first_ready()+1} slot=2 ' in line)
    def test_persistent_owned_effect(self): self.reject('FIELD','trail','010316E0',predicate=lambda line:f'frame={self.first_ready()+1} slot=2 ' in line)
    def test_bad_floor_recovery(self): self.reject('FIELD','y',96,predicate=lambda line:f'frame={self.first_ready()+1} slot=2 ' in line)
    def test_wrong_child_owner(self): self.reject('EFFECT','owner','01030EA0')
    def test_wrong_projectile_speed(self): self.reject('GROUP','vx','00090000',predicate=lambda line:'body=0 group=FF614800 ' in line)
    def test_missing_original_intro_composite(self): self.reject('GROUP',predicate=lambda line:'body=0 group=FF614060 ' in line)
    def test_missing_child_retirement(self): self.reject('RETIRE')
    def test_guest_health_assistance(self): self.reject('HEALTH','pc','FF825930')
    def test_damage_ledger_tamper(self): self.reject('HEALTH','after',0,predicate=lambda line:'before=161 ' in line)
    def test_injected_roster_is_not_natural_evidence(self):
        self.assertFalse(verify_log(self.logs['kano_boot605']+'\nMK2KS_CPU_DIAGNOSTIC_WRITE frame=1001 native_choice=3 requested=17\n','sonya',17)['passed'])


    def test_missing_native_hurt_draw(self):self.reject('CANCEL_DRAW',predicate=lambda l:'frame=9011 ' in l)
    def test_wrong_native_hurt_caller(self):self.reject('CANCEL_DRAW','callers','FFFC1370,FFFC3B00,FF811740,00000000',predicate=lambda l:'frame=9011 ' in l)
    def test_wrong_native_hurt_pose(self):self.reject('CANCEL_DRAW','group','FE82F580',predicate=lambda l:'frame=9011 ' in l)
    def test_wrong_native_hurt_owner(self):self.reject('CANCEL_DRAW','main','01034E90',predicate=lambda l:'frame=9011 ' in l)
    def test_non_native_hurt_draw_pc(self):self.reject('CANCEL_DRAW','pc','FF8387B0',predicate=lambda l:'frame=9011 ' in l)
    def test_cancellation_without_hurt_flag(self):self.reject('FIELD','flags','0010',predicate=lambda l:'frame=9012 slot=2 ' in l)
    def test_cancellation_pose_hold_tamper(self):self.reject('FIELD','pose','FE82F580',predicate=lambda l:'frame=9012 slot=2 ' in l)
    def test_wrong_cancellation_damage(self):self.reject('HEALTH','after','94',predicate=lambda l:'frame=9010 slot=2 ' in l)
    def test_cancelled_child_still_requires_full_intro(self):self.reject('GROUP',predicate=lambda l:'frame=9014 ' in l and 'body=0 group=FF6141E0 ' in l)
    def test_missing_cancellation_ready(self):self.reject('EVENT',predicate=lambda l:'frame=9031 kind=ready ' in l)
    def test_own_release_draw_during_hurt(self):
        log=self.logs['kano_boot605']+'\nMK2_NAT_CPU_GROUP frame=9012 actor=010310B0 main=0106BF30 body=1 group=FE82F580\n'
        self.assertFalse(verify_log(log,'sonya',17)['passed'])


if __name__=='__main__': unittest.main()
