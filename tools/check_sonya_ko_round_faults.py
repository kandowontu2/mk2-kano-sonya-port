"""Actual same-run Sonya KO/reset/body/input/source-state counterexamples."""
import json
from pathlib import Path
import check_launch_ko_round_faults as faults
import qualify_sonya_launch_ko_round as model
ROOT,need,sha=model.ROOT,model.need,model.sha

def check(c):
 side=c['side'];out=ROOT/f'audit_sonya_ko_round_faults_p{side}';need(not out.exists(),'Fresh actual Sonya counterexample receipt')
 path=ROOT/f'audit_sonya_launch_ko_round_checked_p{side}/report.json';proof=json.loads(path.read_text());need(proof['passed'],'Actual whole native KO/reset/source proof')
 pins=dict(proof['inputHashes']);pins[str(path)]=sha(path);pins[str(Path(__file__))]=sha(__file__)
 text=c['text'];positive,by=model.physical(text,c['guest']);reset=positive['fullHealthResetFrame'];ko=positive['koFrame'];rejected=[]
 def reject(label,fn):
  try:fn()
  except(ValueError,AssertionError,KeyError)as error:rejected.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actually changed Sonya evidence admitted: '+label)
 for key,value in(('roster','1'),('id','1'),('actor','01000000'),('main','01000000'),('owner','01000000'),('floor','80'),('hp','160'),('mode','7'),('vx','00010000'),('trail','01000000')):
  changed=faults.change(text,'MK2_KO_FIELD',lambda r:r['frame']==str(reset)and r['slot']==str(side),key,value)
  reject('actual reset '+key+' changed',lambda t=changed:model.physical(t,c['guest']))
 changed=faults.change(text,'MK2_KO_FIELD',lambda r:r['frame']==str(ko)and r['slot']==str(side),'hp','1');reject('actual KO health not zero',lambda:model.physical(changed,c['guest']))
 changed=faults.change(text,'MK2_KO_FIELD',lambda r:r['frame']==str(reset)and r['slot']==str(side),'hp',remove=True);reject('actual reset field omitted',lambda:model.physical(changed,c['guest']))
 changed=faults.change(text,'MK2_INTERRUPT_HEALTH',lambda r:r['after']=='0','pc',delta=16);reject('actual lethal native opcode site changed',lambda:model.physical(changed,c['guest']))
 changed=faults.change(text,'MK2_INTERRUPT_HEALTH',lambda r:r['pc']=='FF9DEF40','after','5');reject('actual original health-fill step changed',lambda:model.physical(changed,c['guest']))
 for tag in('MK2_INTERRUPT_IO','MK2_INTERRUPT_LOW_IO'):
  row=model.rows(text,tag)[0];changed=faults.change(text,tag,lambda r:r==row,'value',format(int(row['value'],16)^1,'04X'))
  reject('actual native input bit '+tag+' changed',lambda t=changed:model.prior.mirror.delivery.delivered(t))
 for tag,key in(('MK2_HPHASE_CANDIDATE','source'),('MK2_HPHASE_QUEUE','xy')):
  changed=faults.change(text,tag,lambda r:r['frame']==str(positive['rearmRecovered'])and r['slot']==str(side),key,delta=8 if key=='source'else 1)
  reject('actual post-reset body '+key+' changed',lambda t=changed:model.body_publication(t,c['guest'],by))
 events=model.source_events(c,pins);owned=model.owners(c,events)
 for key,value in(('actor','01000000'),('main','01000000'),('id','18'),('health','161')):
  changed=faults.change(text,'MK2_INTERRUPT_OWNER',lambda r:r['frame']==str(reset)and r['slot']==str(side),key,value)
  reject('actual stale post-reset source '+key,lambda t=changed:model.owners(dict(c,text=t),events))
 restored,restored_by=model.physical(text,c['guest']);need(restored==positive and restored_by==by and model.owners(c,events)==owned,'Entire same-run positive restored after every counterexample')
 for p in(Path(model.__file__),Path(faults.__file__)):pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Whole actual source/candidate/evidence stable')
 report=dict(passed=True,side=side,nativeTerminal=c['terminal'],actualFaultsRejected=rejected,completeIndependentOwnership=owned,inputHashes=pins,
             allKOResetMorphCoverageAccepted=False,fullPortAcceptance=False,goalStatus='active',newNativeBoots=0,newBuilds=0,newRawMedia=0)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(side=side,actualFaultsRejected=len(rejected))),flush=True);return report
