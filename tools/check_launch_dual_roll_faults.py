"""Actual changed-record counterexamples to the complete mirror qualification."""
import json,re,subprocess
from pathlib import Path
import qualify_launch_dual_roll as model
ROOT,need,sha=model.ROOT,model.need,model.sha

def check(carrier):
 out=ROOT/f"audit_launch_dual_roll_faults_p{carrier['side']}";need(not out.exists(),'Fresh same-run negative controls')
 positive=ROOT/f"audit_launch_dual_roll_checked_p{carrier['side']}/report.json";proof=json.loads(positive.read_text())
 need(proof['passed']and carrier['terminal']==proof['nativeTerminal'],'Exact accepted native terminal, not a replay')
 pins=dict(proof['inputHashes']);pins[str(positive)]=sha(positive)
 need(all(sha(p)==h for p,h in pins.items()),'Accepted entire source/evidence intact')
 events=model.sources(carrier,pins);ownership=model.owners(carrier,events);physical=model.whole_physical(carrier);faults=[]
 def reject(label,tag,key,value,where,fn):
  line=next(s for s in carrier['text'].splitlines()if s.startswith(tag+' ')and all(f'{k}={v} 'in s+' 'for k,v in where.items()))
  changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and line!=changed,'Nonvacuous actual native fault '+label)
  bad=dict(carrier,text=carrier['text'].replace(line,changed,1))
  try:fn(bad)
  except(ValueError,KeyError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual mirror counterexample admitted '+label)
 for event in events:
  frame=int(event['marker']['frame'])+1;slot=event['slot']
  for key,value in [('actor','01000000'),('main','01000000'),('id','1'),('health','1')]:
   reject(f'{frame} slot{slot} wrong owned {key}','MK2_INTERRUPT_OWNER',key,value,dict(frame=frame,slot=slot),lambda c:model.owners(c,events))
  if event['incoming']:
   hit=int(event['incoming']['frame'])+1
   reject(f'{hit} stale hit owner','MK2_INTERRUPT_OWNER','actor',event['marker']['a8'],dict(frame=hit,slot=slot),lambda c:model.owners(c,events))
   reject(f'{hit} interrupted source resumes','MK2_INTERRUPT_CHANNEL','position','1',dict(frame=hit,channel=event['channel']),lambda c:model.owners(c,events))
   reject(f'{hit} opponent cancelled by own hit','MK2_INTERRUPT_OWNER','actor','00000000',dict(frame=hit,slot=3-slot),lambda c:model.owners(c,events))
 for tag,key,value in [('MK2_HPHASE_POST_FIELD','id','1'),('MK2_HPHASE_POST_FIELD','floor','99'),
                       ('MK2_HPHASE_CANDIDATE','source','00000000'),('MK2_HPHASE_QUEUE','xy','00000000')]:
  r=model.rows(carrier['text'],tag)[0]
  reject(tag+' wrong '+key,tag,key,value,dict(frame=r['frame'],slot=r['slot']),model.whole_physical)
 for tag in('MK2_INTERRUPT_IO','MK2_INTERRUPT_LOW_IO'):
  r=model.rows(carrier['text'],tag)[0]
  reject(tag+' actual input bit',tag,'value',format(int(r['value'],16)^1,'04X'),dict(frame=r['frame'],pc=r['pc']),lambda c:model.delivery.delivered(c['text']))
 need(model.owners(carrier,events)==ownership and model.whole_physical(carrier)==physical,'Entire positive restored after actual faults')
 for path in(Path(__file__),Path(model.__file__)):pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'No accepted source/evidence mutated')
 report=dict(passed=True,nativeTerminal=carrier['terminal'],actualSemanticFaultsRejected=faults,inputHashes=pins,
             originalPositiveRestored=True,newNativeBoots=0,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,fullPortAcceptance=False,goalStatus='active')
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(report,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Lossless actual fault receipt')
 print(json.dumps(dict(passed=True,side=carrier['side'],actualFaultsRejected=len(faults))),flush=True)
 return report
