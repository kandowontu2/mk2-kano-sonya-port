"""Actual current CPU grab chronology and cleanup corruption regressions.

Only in-memory log mutations; no game-state or retained-capture changes.
"""
import hashlib
import io
import json
import re
import sys
import unittest
from pathlib import Path
import verify_current_cpu_pair_display_v835 as v


class PairState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={name:(v.ROOT/name/'run.log').read_text(encoding='utf-8-sig')for name in v.CASES}
        cls.proofs={name:cls.verify(name,log)for name,log in cls.logs.items()}
        assert all(p['passed']for p in cls.proofs.values()),cls.proofs

    @staticmethod
    def verify(name,log):
        player,profile=v.CASES[name]
        return v.ordinary.verify_log(log,player)if profile=='ordinary'else v.special.verify_log(log,player,profile)

    def mutate(self,name,tag,field,value,predicate,remove=False):
        lines=self.logs[name].splitlines(keepends=True)
        for i,line in enumerate(lines):
            if not line.startswith('MK2_CPU_PAIR_'+tag+' '):continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if field not in row or not predicate(row):continue
            altered=''if remove else re.sub(r'\b'+field+r'=\S+',field+'='+str(value),line,count=1)
            self.assertNotEqual(altered,line,'Mutation must change actual evidence')
            lines[i]=altered
            return ''.join(lines)
        self.fail('Missing actual mutation target: '+name+' '+tag+' '+field)

    def test_five_current_native_baselines(self):
        self.assertEqual(len(self.proofs),5)
        for name,proof in self.proofs.items():
            with self.subTest(capture=name):
                v.matched(v.ROOT/name,{})
                self.assertEqual(proof['held_fields'],70 if proof['target']=='kano'else 46)
                self.assertEqual(proof['damage'],32 if proof['target']=='kano'else 35)
                self.assertFalse(proof['whole_character_integration_complete'])

    def test_summaries_cannot_replace_chronology(self):
        for name,log in self.logs.items():
            altered=re.sub(r'^MK2_CPU_PAIR_(FIELD|FOLLOW_FIELD|EVENT|HEALTH|FLAG) [^\r\n]*\r?\n','',log,flags=re.M)
            self.assertFalse(self.verify(name,altered)['passed'])

    def test_ordinary_followup_cannot_replace_signature(self):
        for name,(player,profile)in v.CASES.items():
            if profile!='ordinary':self.assertFalse(v.ordinary.verify_log(self.logs[name],player)['passed'])


def held_test(field,value,remove=False):
    def test(self):
        for name,proof in self.proofs.items():
            step=next(r for r in v.ordinary.rows(self.logs[name],'EVENT')if r['kind']=='step'and r['cycle']==proof['cycle'])
            at=step['frame']+1
            with self.subTest(capture=name):
                altered=self.mutate(name,'FIELD',field,value,lambda r:int(r['frame'])==at,remove)
                self.assertFalse(self.verify(name,altered)['passed'])
    return test


for field,value in (('state','1'),('vstate','0'),('roster','1'),('owner','00000000'),
                    ('pose','00000000'),('vpose','00000000'),('vxpos','-999'),
                    ('vypos','-999'),('vx','00010000'),('vaction','0'),('vhp','1')):
    setattr(PairState,'test_held_'+field,held_test(field,value))
setattr(PairState,'test_missing_held_callback',held_test('frame',0,True))


def native_test(tag,field,value,predicate):
    def test(self):
        for name,proof in self.proofs.items():
            def actual_pair(row):
                return (tag=='RESULT'or proof['start']<=int(row['frame'])<=proof['complete'])and predicate(row)
            with self.subTest(capture=name):
                altered=self.mutate(name,tag,field,value,actual_pair)
                self.assertFalse(self.verify(name,altered)['passed'])
    return test


for label,tag,field,value,predicate in (
    ('health_writer','HEALTH','pc','00000000',lambda r:r['before']!=r['after']),
    ('damage_register','EVENT','a10','00000001',lambda r:r['kind']=='damage'),
    ('fling_gravity','EVENT','a2','00000000',lambda r:r['kind']=='fling'),
    ('native_catch_descriptor','EVENT','word','0000',lambda r:r['kind']=='attack'),
    ('own_dirty_ready','OWN_REGAIN','flags','00000010',lambda r:True),
    ('victim_dirty_ready','VICTIM_REGAIN','vbody','0000001E',lambda r:True),
    ('terminal_schema','RESULT','schema','6',lambda r:True),
):setattr(PairState,'test_'+label,native_test(tag,field,value,predicate))


if __name__=='__main__':
    out=v.ROOT/'audit_v836_current_cpu_pair_state_units'
    if out.exists():raise ValueError('Refusing to overwrite evidence')
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PairState))
    paths=[v.ROOT/name/'run.log'for name in v.CASES]
    paths+=[v.ROOT/name/'result.json'for name in v.CASES]
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(v.ROOT/'tools')and path.suffix=='.py':paths.append(path)
    hashes={str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest().upper()for p in paths}
    out.mkdir();(out/'unit-tests.log').write_text(stream.getvalue())
    (out/'verification.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
        'baseline_cases':5,'inputHashes':hashes,'fullPortAcceptance':False},indent=2)+'\n')
    print(stream.getvalue());sys.exit(0 if result.wasSuccessful()else 1)
