"""Real capture unchanged; reject in-memory ordinal and fighter-state damage."""
import json,re
import verify_cpu_followup_v1423 as verifier
import verify_ring_native_lookup_v1342 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1425_cpu_cycle_counterexamples'

def changed(log,tag,frame,key,value):
 lines=log.splitlines();matches=[]
 for i,line in enumerate(lines):
  if line.startswith('MK2_CPU_PAIR_'+tag+' ') and re.search(r'\bframe='+str(frame)+r'\b',line):matches.append(i)
 assert len(matches)==1
 at=matches[0];need=len(re.findall(r'\b'+key+r'=\S+',lines[at]));assert need==1
 lines[at]=re.sub(r'\b'+key+r'=\S+',key+'='+str(value),lines[at]);return '\n'.join(lines)+'\n'

def verify():
 path=ROOT/'audit_v1419_cpu_queue_kano/run.log';log=path.read_text(encoding='utf-8-sig')
 pristine=verifier.verify_log(log,'kano','blade');assert pristine['passed'],pristine['errors']
 frame=2000
 mutations={
  'Wrong completed-follow ordinal':changed(log,'FOLLOW_FIELD',frame,'cycle',2),
  'Unexplained current-grab ordinal':changed(log,'FIELD',frame,'cycle',999),
  'Removed real second action entry':'\n'.join(line for line in log.splitlines()if not(line.startswith('MK2_CPU_PAIR_ENTRY ')and 'frame=1997 ' in line))+'\n',
  'Changed actual follow actor ID':changed(log,'FIELD',frame,'id',1),
  'Changed actual follow actor Main':changed(log,'FOLLOW_FIELD',frame,'main','01069D80'),
  'Changed actual follow HP':changed(log,'FOLLOW_FIELD',frame,'hp',100),
  'Changed actual follow coordinate':changed(log,'FOLLOW_FIELD',frame,'x',999),
  'Persistent flag at owning regain':changed(log,'FOLLOW_REGAIN',1989,'flags','00000010'),
  'Changed callback movement velocity':changed(log,'FOLLOW_FIELD',frame,'vx','00000000')}
 results=[]
 for label,mutant in mutations.items():
  proof=verifier.verify_log(mutant,'kano','blade');assert not proof['passed'],label
  results.append(dict(counterexample=label,rejected=True,errors=proof['errors']))
 assert source.digest(path)==source.digest(ROOT/'audit_v1419_cpu_queue_kano/run.log')
 pins={str(path):source.digest(path)}
 for name in ('tools/test_native_cpu_cycle_bookkeeping_v1425.py','tools/verify_cpu_followup_v1423.py','tools/cpu_followup_contract_v1423.py'):pins[str(ROOT/name)]=source.digest(ROOT/name)
 return dict(passed=True,pristineCurrentBladeFollowupAccepted=True,counterexamples=results,actualCaptureModified=False,inputHashes=pins,CPUAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 assert not OUT.exists()
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),actualCaptureModified=False,fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),rejected=len(report.get('counterexamples',[]))),indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
