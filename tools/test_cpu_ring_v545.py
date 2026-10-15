"""Fresh native CPU ring block/duck lifetimes and non-vacuous corruptions."""
import re
import unittest
import verify_cpu_projectile_followup_v545 as v

CASES = [('audit_v555_cpu_ring_block', 'block', 'v2'),
         ('audit_v555_cpu_ring_duck', 'duck_miss', 'v3')]

class Ring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs=[]
        cls.original=(v.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        for name,scenario,version in CASES:
            proof=v.verify(v.ROOT/name,18,scenario,version)
            assert proof['passed'], 'Mutations require an actually passing baseline'
            cls.logs.append((v.ROOT/name/'run.log').read_text(encoding='utf-8-sig'))

    def reject(self,tag,key=None,value=None,case=0,predicate=lambda row:True):
        lines=self.logs[case].splitlines(keepends=True)
        start=int(v.records(self.logs[case],'ENTRY')[0]['frame'])
        for index,line in enumerate(lines):
            if not line.startswith('MK2_CPU_SHOT_'+tag+' '):continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if int(row['frame'])<start or (tag in ('FIELD','INPUT') and int(row['frame'])==start) or not predicate(row):continue
            if key is None:lines[index]=''
            else:
                lines[index],count=re.subn(r'\b'+key+r'=[^\s]+',key+'='+value,line)
                self.assertEqual(count,1)
            self.assertNotEqual(lines[index],line,'Mutation must change actual evidence')
            break
        else:self.fail('Actual mutation target absent')
        with self.assertRaises(ValueError):v.verify_log(''.join(lines),18,CASES[case][1],self.original)

    def test_actual_block_and_duck(self):
        for name,scenario,version in CASES:
            self.assertTrue(v.verify(v.ROOT/name,18,scenario,version)['passed'])
    def test_missing_field(self):self.reject('FIELD')
    def test_proxy_identity(self):self.reject('FIELD','id','1')
    def test_human_CPU(self):self.reject('FIELD','state','1')
    def test_wrong_owner(self):self.reject('FIELD','owner','00000000')
    def test_wrong_native_entry(self):self.reject('ENTRY','pc','FFFFB420')
    def test_native_health_writer(self):self.reject('HEALTH','pc','00000000')
    def test_wrong_damage(self):self.reject('HEALTH','after','0')
    def test_missing_damage(self):self.reject('HEALTH')
    def test_missing_handoff(self):self.reject('HANDOFF')
    def test_wrong_child_owner(self):self.reject('CHILD','owner','00000000')
    def test_missing_child_field(self):self.reject('EFFECT')
    def test_wrong_flight_speed(self):self.reject('EFFECT','vx','00090000',case=1,predicate=lambda r:r['vx']=='00080000')
    def test_missing_native_retirement(self):self.reject('RETIRE')
    def test_persistent_child(self):self.reject('RESULT','live_children','1')
    def test_missing_duck_input(self):self.reject('INPUT',case=1)
    def test_wrong_duck_input(self):self.reject('INPUT','buttons','Block',case=1)

if __name__=='__main__':unittest.main()
