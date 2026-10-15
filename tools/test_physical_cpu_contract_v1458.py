"""Counterexamples on real Sonya CPU captures; never alter actual evidence."""
import json,re
from pathlib import Path
import verify_physical_p2_cpu_pair_v1456 as p2
import verify_physical_p1_cpu_pair_v1457 as p1
import verify_native_grab_audio_v1415 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1458_physical_cpu_counterexamples'

def change(log,tag,frame,key,value,predicate=lambda line:True,all_matches=False):
 lines=log.splitlines();found=[i for i,line in enumerate(lines)if line.startswith('MK2_CPU_PAIR_'+tag+' ')and re.search(r'\bframe='+str(frame)+r'\b',line)and predicate(line)]
 assert len(found)>=1 if all_matches else len(found)==1,(tag,frame,key,len(found))
 for at in found:
  old=lines[at]
  assert len(re.findall(r'\b'+key+r'=\S+',old))==1
  lines[at]=re.sub(r'\b'+key+r'=\S+',key+'='+str(value),old)
  assert lines[at]!=old,'No-op counterexample'
 return '\n'.join(lines)+'\n'

def run():
 pins={};results=[];baselines=[]
 cases=[('audit_v1439_cpu_sonya_p2_human_kano','kano',p2),('audit_v1439_cpu_sonya_p2_human_sonya','sonya',p2),('audit_v1446_cpu_p1_boot605_human_sonya','sonya',p1)]
 for case,player,model in cases:
  path=ROOT/case/'run.log';before=source.prior.digest(path);raw=path.read_text(encoding='utf-8-sig')
  proof=model.verify_log(raw,player);assert proof['passed'],proof['errors']
  # The state model ignores rendering lines. Retain EVERY actual state,
  # native instruction/store, input, ROM and cold-selection line unchanged.
  log='\n'.join(line for line in raw.splitlines()if line.startswith(('MK2_CPU_PAIR_','MK2_P1CPU_','MK2_P2CPU_')))+'\n'
  assert model.verify_log(log,player)==proof
  baselines.append(dict(case=case,CPU_slot=model.CPU_SLOT,human_slot=model.HUMAN_SLOT,passed=True))
  start=proof['start'];release=proof['release'];ready=proof['native_followup']['first_ready'];field=ready+3
  row=next(r for r in model.rows(log,'FIELD')if r['frame']==field)
  body=f"{row['body']^4:08X}"
  paired=model.rows(log,'EVENT');first=next(r['frame']for r in paired if r['kind']=='step')+1
  both_body=change(change(log,'FIELD',field,'body',body),'FOLLOW_FIELD',field,'body',body)
  mutants={
   'CPU metadata relabelled as other physical slot':change(log,'FIELD',first,'cpu_slot',model.HUMAN_SLOT),
   'Human metadata relabelled as CPU physical slot':change(log,'FIELD',first,'human_slot',model.CPU_SLOT),
   'Victim velocity request targets CPU slot':change(log,'EVENT',release,'a1','010602D0'if model.CPU_SLOT==1 else'01060EA0',lambda l:'kind=velocity 'in l),
   'Held own actor ID replaced by Liu Kang':change(log,'FIELD',first,'id',1),
   'Held body group is not actual leg phase':change(log,'FIELD',first,'pose','FE83BBE0'),
   'Victim damage detached from native ledger':change(log,'FIELD',release+2,'vhp',1),
   'Completed-follow ordinal altered':change(log,'FOLLOW_FIELD',field,'cycle',999),
   'Current-grab ordinal has no real entry':change(log,'FIELD',field,'cycle',999),
   'Recovered follow-up keeps persistent body lock':change(log,'FOLLOW_REGAIN',ready,'body',f"{next(r for r in model.rows(log,'FOLLOW_REGAIN')if r['frame']==ready)['body']|4:08X}"),
   'Recovered follow-up keeps Main busy flag':change(log,'FOLLOW_REGAIN',ready,'flags','00000010'),
   'Both callback streams share unlogged body change':both_body,
   'Follow-up Main is another native actor':change(log,'FOLLOW_FIELD',field,'main','01000000'),
   'Native cleanup rows come from wrong executing PC':change(log,'FLAG',ready,'pc','FF83EFA0',lambda l:'kind=flags 'in l and f'slot={model.CPU_SLOT} 'in l and'pc=FF83EFC0 'in l,all_matches=True),
  }
  if player=='kano':
   mutants['Removed real second grab entry']='\n'.join(l for l in log.splitlines()if not(l.startswith('MK2_CPU_PAIR_ENTRY ')and'cycle=2 'in l))+'\n'
   mutants['Native ordinary recovery state has wrong operand']=change(log,'FLAG',2160,'a0','00000005',lambda l:'kind=action 'in l and'slot=2 'in l)
   mutants['Earlier attack cleanup assigned to human slot']=change(log,'FLAG',2172,'slot',1,lambda l:'kind=body 'in l and'slot=2 'in l)
   mutants['Earlier attack cleanup omitted']='\n'.join(l for l in log.splitlines()if not(l.startswith('MK2_CPU_PAIR_FLAG ')and'frame=2172 'in l and'kind=body 'in l and'slot=2 'in l))+'\n'
  for label,mutant in mutants.items():
   assert mutant!=log
   checked=model.verify_log(mutant,player);assert not checked['passed'],(case,label)
   results.append(dict(case=case,counterexample=label,rejected=True,errors=checked['errors']))
  assert source.prior.digest(path)==before; pins[str(path)]=before
  print(case+' pristine accepted; '+str(len(mutants))+' corruptions rejected',flush=True)
 for path in (Path(__file__),Path(p1.__file__),Path(p2.__file__)):
  pins[str(path.resolve())]=source.prior.digest(path)
 return dict(passed=True,candidate=source.NAME,baselines=baselines,counterexamples=results,inputHashes=pins,actualCapturesModified=False,CPUAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 assert not OUT.exists()
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),rejected=len(report.get('counterexamples',[]))),indent=2))
 raise SystemExit(0 if report['passed']else 1)
