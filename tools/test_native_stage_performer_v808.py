"""Baseline and adversarial log tests for current native stage-performer proof."""
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import unittest
import verify_native_stage_performer_v807 as proof

ROOT = Path(__file__).resolve().parents[1]
CASES = []
for fighter in ('kano','sonya'):
    for side in (1,2):
        CASES += [(f'audit_v805_{fighter}_stage_p{side}',fighter,side,1,'positive'),
                  (f'audit_v806_{fighter}_tomb_p{side}',fighter,side,6,'positive')]
        CASES += [(f'audit_v806_{fighter}_{suffix}_p{side}',fighter,side,arena,case)
                  for suffix,arena,case in [('wrong',1,'wrong_command'),('far',1,'far'),('arena0',0,'positive')]]
LOGS = {name:(ROOT/name/'run.log').read_text(encoding='utf-8-sig') for name,*_ in CASES}

def mutate(log, tag, key, value, predicate=lambda r: True):
    lines = log.splitlines(); changed = False
    for index,line in enumerate(lines):
        if not line.startswith('MK2_STAGE_'+tag+' '):continue
        row = dict(re.findall(r'(\w+)=([^\s]+)',line))
        if predicate(row):
            lines[index], count = re.subn(r'\b'+key+r'=\S+',key+'='+str(value),line)
            assert count == 1
            changed = True;break
    assert changed, 'Mutation target missing'
    return '\n'.join(lines)+'\n'

class StageProof(unittest.TestCase):
    def check(self, spec, log):
        _,fighter,side,arena,case=spec
        return proof.check_log(log,fighter,side,arena,case)
    def positives(self):
        return [s for s in CASES if s[3] in (1,6) and s[4]=='positive']
    def reject_mutation(self, tag, key, value, predicate=lambda r: True, specs=None):
        for spec in specs or self.positives():
            with self.subTest(case=spec[0]):
                with self.assertRaises(ValueError):self.check(spec,mutate(LOGS[spec[0]],tag,key,value,predicate))
    def test_twenty_actual_baselines(self):
        for spec in CASES:
            with self.subTest(case=spec[0]):self.assertTrue(self.check(spec,LOGS[spec[0]])['passed'])
    def test_wrong_boot_identity(self):self.reject_mutation('BOOT','own_id',1)
    def test_wrong_selected_identity(self):self.reject_mutation('SELECT_ID','actual',1)
    def test_skipped_native_arena(self):self.reject_mutation('MATCH','arena',9)
    def test_proxy_rematch_identity(self):self.reject_mutation('MATCH','ids','1,18')
    def test_assisted_damage_store(self):self.reject_mutation('DAMAGE','pc','FF800000')
    def test_partial_health_round(self):self.reject_mutation('DAMAGE','before',160)
    def test_unearned_finish_window(self):self.reject_mutation('WINDOW','kos',1)
    def test_wrong_command_button(self):
        for spec in self.positives():
            begin=int(proof.rows(LOGS[spec[0]],'COMMAND')[0]['frame'])
            with self.subTest(case=spec[0]):
                log=mutate(LOGS[spec[0]],'INPUT','button','Low_Punch',lambda r:int(r['frame'])==begin+40)
                with self.assertRaises(ValueError):self.check(spec,log)
    def test_wrong_action_owner(self):
        self.reject_mutation('ENTRY','a8','01000000',lambda r:r['entry'] in ('FF8BDDE0','FF8BDFE0'))
    def test_wrong_native_arena_action(self):
        for spec in self.positives():
            with self.subTest(case=spec[0]):
                pc='FF8BDDE0' if spec[3]==1 else 'FF8BDFE0'
                log=mutate(LOGS[spec[0]],'ENTRY','entry',pc,lambda r:r['entry'] in ('FF8BDDE0','FF8BDFE0'))
                with self.assertRaises(ValueError):self.check(spec,log)
    def test_removed_native_gate(self):
        for spec in self.positives():
            with self.subTest(case=spec[0]):
                log='\n'.join(line for line in LOGS[spec[0]].splitlines() if 'entry=FF8773A0 ' not in line)+'\n'
                with self.assertRaises(ValueError):self.check(spec,log)
    def test_proxy_live_body(self):self.reject_mutation('FIELD','id',1,lambda r:r['age']=='40')
    def test_proxy_victim_body(self):self.reject_mutation('FIELD','victim_id',1,lambda r:r['age']=='40')
    def test_missing_consecutive_field(self):
        for spec in self.positives():
            with self.subTest(case=spec[0]):
                log='\n'.join(line for line in LOGS[spec[0]].splitlines() if not(line.startswith('MK2_STAGE_FIELD ')and' age=40 ' in line))+'\n'
                with self.assertRaises(ValueError):self.check(spec,log)
    def test_no_retirement_softlock(self):self.reject_mutation('FIELD','mode',5,lambda r:r['age']=='800')
    def test_missing_paid_rematch(self):
        for spec in self.positives():
            with self.subTest(case=spec[0]):
                log='\n'.join(line for line in LOGS[spec[0]].splitlines() if not(line.startswith('MK2_STAGE_INPUT ')and'button=Coin' in line and int(re.search(r'frame=(\d+)',line)[1])>700))+'\n'
                with self.assertRaises(ValueError):self.check(spec,log)
    def test_rejection_changed_to_accepted(self):
        specs=[s for s in CASES if s[3]==0 or s[4]!='positive']
        self.reject_mutation('RESULT','action',1234,specs=specs)
    def test_wrong_far_range_boundary(self):
        for spec in [s for s in CASES if s[4]=='far']:
            log=LOGS[spec[0]];begin=int(proof.rows(log,'COMMAND')[0]['frame'])
            event=next(r for r in proof.rows(log,'ENTRY')if r['entry'] in ('FFFAA200','FFFAA400') and int(r['frame'])>=begin+40)
            with self.subTest(case=spec[0]):
                bad=mutate(log,'ENTRY','a3','00000048',lambda r:r['entry']=='FF877420' and r['frame']==event['frame'])
                with self.assertRaises(ValueError):self.check(spec,bad)
    def test_rejection_cleanup_softlock(self):
        self.reject_mutation('REJECT_END','mode',5,specs=[s for s in CASES if s[3]==0 or s[4]!='positive'])

if __name__=='__main__':
    out=ROOT/'audit_v808_native_stage_performer_units'
    if out.exists():raise ValueError('Do not overwrite evidence')
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(StageProof))
    out.mkdir();(out/'unit-tests.log').write_text(stream.getvalue())
    paths=[Path(__file__),Path(proof.__file__),Path(proof.candidate.__file__)]+[ROOT/name/'run.log' for name,*_ in CASES]
    (out/'verification.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,'baseline_cases':20,
        'scope':__doc__,'fullPortAcceptance':False,'checked_inputs':{str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in paths}},indent=2)+'\n')
    print(stream.getvalue());sys.exit(0 if result.wasSuccessful()else 1)
