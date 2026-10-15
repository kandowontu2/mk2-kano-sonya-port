"""Reject corruption of either real repeated CPU grab and native continuation."""
import json
from pathlib import Path
from test_physical_cpu_contract_v1458 import change
import verify_repeated_sonya_cpu_v1463 as model
import verify_native_grab_audio_v1415 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1465_repeated_cpu_counterexamples'

def run():
 path=ROOT/'audit_v1460_sonya_cpu_repeated_kano_p1/run.log';before=source.prior.digest(path)
 raw=path.read_text(encoding='utf-8-sig');pristine=model.verify_log(raw,'kano');assert pristine['passed'],pristine['errors']
 log='\n'.join(l for l in raw.splitlines()if l.startswith(('MK2_CPU_PAIR_','MK2_P1CPU_')))+'\n'
 assert model.verify_log(log,'kano')==pristine
 second=pristine['pairs'][1];step=next(r['frame']for r in model.rows(log,'EVENT')if r['cycle']==2 and r['kind']=='step')+1
 remove=lambda tag,condition:'\n'.join(l for l in log.splitlines()if not(l.startswith('MK2_CPU_PAIR_'+tag+' ')and condition(l)))+'\n'
 mutants={
  'Second completed contact omitted':remove('COMPLETE',lambda l:'cycle=2 'in l),
  'Second real action entry omitted':remove('ENTRY',lambda l:'cycle=2 'in l),
  'Second actual victim regain omitted':remove('VICTIM_REGAIN',lambda l:'cycle=2 'in l),
  'Second victim held pose changed':change(log,'FIELD',step,'vpose','FF000000'),
  'Second victim grip offset changed':change(log,'FIELD',step,'vxpos',999),
  'Second paired damage ledger changed':change(log,'FIELD',second['release']+2,'vhp',1),
  'Second CPU handoff remains busy':change(log,'OWN_REGAIN',second['own_handoff'],'flags','00000010'),
  'Second victim handoff has wrong physical role':change(log,'VICTIM_REGAIN',second['victim_handoff'],'human_slot',1),
  'Initial pre-entry callback ordinal fabricated':change(log,'FIELD',pristine['start'],'cycle',1),
  'Completed/current ordinal distinction erased':change(log,'FOLLOW_FIELD',second['start']+1,'cycle',2),
 }
 results=[]
 for label,mutant in mutants.items():
  assert mutant!=log
  checked=model.verify_log(mutant,'kano');assert not checked['passed'],label
  results.append(dict(counterexample=label,rejected=True,errors=checked['errors']))
 assert source.prior.digest(path)==before
 paths=(path,Path(__file__),Path(model.__file__),ROOT/'tools/test_physical_cpu_contract_v1458.py')
 return dict(passed=True,candidate=source.NAME,actualPairs=2,actualCapturesModified=False,counterexamples=results,
  inputHashes={str(p.resolve()):source.prior.digest(p)for p in paths},CPUAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 assert not OUT.exists()
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),rejected=len(report.get('counterexamples',[]))),indent=2))
 raise SystemExit(0 if report['passed']else 1)
