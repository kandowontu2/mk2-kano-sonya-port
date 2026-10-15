"""Current naturally chosen CPU cases and actual malformed-evidence rejection."""
import re
import unittest
from verify_natural_cpu_moves import ROOT, verify, verify_log, SPECS

CASES=('kano_boot605','kano_boot606','sonya_boot601','sonya_boot604')


class NaturalCPU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={name:(ROOT/f'audit_v317_natural_cpu_{name}/run.log').read_text(encoding='utf-8-sig') for name in CASES}

    def test_all_four_actual_natural_runs(self):
        union=set()
        for name in CASES:
            result=verify(ROOT/f'audit_v317_natural_cpu_{name}')
            self.assertTrue(result['passed'],(name,result['errors']))
            union.update(result['observed_moves'])
        self.assertEqual(union,set(SPECS))

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

    def test_no_summary_only_proof(self):
        log=re.sub(r'^MK2_NAT_CPU_(FIELD|ENTRY|GROUP|CHILD|EFFECT|EVENT|HEALTH)[^\r\n]*\r?\n','',self.logs['kano_boot605'],flags=re.M)
        self.assertFalse(verify_log(log,'sonya',17)['passed'])

    def test_wrong_natural_order(self): self.reject('FIELD','scheduled',18,predicate=lambda line:'slot=2 ' in line)
    def test_wrong_entry_cpu_role(self): self.reject('ENTRY','state',1)
    def test_wrong_entry_native_owner(self): self.reject('ENTRY','main','01034E90')
    def test_wrong_first_callback_identity(self): self.reject('FIELD','id',1,predicate=lambda line:'frame=6143 slot=2 ' in line)
    def test_missing_first_callback(self): self.reject('FIELD',predicate=lambda line:'frame=1643 slot=2 ' in line,name='sonya_boot601')
    def test_old_no_entry_role_schema_is_insufficient(self):
        log=(ROOT/'audit_v315_natural_cpu_kano_boot606/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify_log(log,'sonya',17)['passed'])
    def test_wrong_native_ready_pc(self): self.reject('EVENT','pc','FF861370',predicate=lambda line:'frame=6191 kind=ready ' in line)
    def test_missing_recovery_field(self): self.reject('FIELD',predicate=lambda line:'frame=6192 slot=2 ' in line)
    def test_persistent_owned_effect(self): self.reject('FIELD','trail','010316E0',predicate=lambda line:'frame=6192 slot=2 ' in line)
    def test_bad_floor_recovery(self): self.reject('FIELD','y',96,predicate=lambda line:'frame=6192 slot=2 ' in line)
    def test_wrong_child_owner(self): self.reject('EFFECT','owner','01030EA0')
    def test_wrong_projectile_speed(self): self.reject('GROUP','vx','00090000',predicate=lambda line:'body=0 group=FF614800 ' in line)
    def test_missing_original_intro_composite(self): self.reject('GROUP',predicate=lambda line:'body=0 group=FF614060 ' in line)
    def test_missing_child_retirement(self): self.reject('RETIRE')
    def test_guest_health_assistance(self): self.reject('HEALTH','pc','FF825930')
    def test_damage_ledger_tamper(self): self.reject('HEALTH','after',0,predicate=lambda line:'before=161 ' in line)
    def test_injected_roster_is_not_natural_evidence(self):
        self.assertFalse(verify_log(self.logs['kano_boot605']+'\nMK2KS_CPU_DIAGNOSTIC_WRITE frame=1001 native_choice=3 requested=17\n','sonya',17)['passed'])


if __name__=='__main__': unittest.main()
