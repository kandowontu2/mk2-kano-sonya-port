"""Actual physical/input/identity/source counterexamples in the same runs."""
import json
from pathlib import Path
import check_launch_ko_round_faults as mutate
import qualify_morph_startup_return_v3 as model
ROOT,need,sha=model.ROOT,model.need,model.sha

def input_provenance(c,by):
 rows=model.previous.rows(c['text'],'MK2_HUMAN_SHANG_INPUT')
 first=int(model.previous.original.prior.one(c['text'],'MK2_MAUDIO_BEGIN')['frame'])
 target='kano'if c['move']=='ball'else'sonya';side=c['side']
 for r in rows:
  at=int(r['frame']);state=by[at,side]
  need(at==first+int(r['age'])and r['side']==str(side)and r['target']==target and r['profile']=='adversity_formed'and r['form']=='added'and r['writes']=='0'and r['actor']==state['actor']and r['id']==state['id'],'Every actual controller operation binds exact current actor/live form/native roster')
 return dict(passed=True,actualPhysicalControllerRows=len(rows))

def check(c):
 side=c['side'];out=ROOT/f"audit_morph_startup_return_faults_{c['move']}_p{side}";need(not out.exists(),'Fresh same-terminal faults')
 path=ROOT/f"audit_morph_startup_return_checked_{c['move']}_p{side}/report.json";proof=json.loads(path.read_text());need(proof['passed'],'Whole actual morph/return/source proof')
 pins=dict(proof['inputHashes']);pins[str(path)]=sha(path)
 state,by=model.physical(c);inputs=input_provenance(c,by);events=model.previous.events(c,pins,by);owned=model.previous.owners(c,events)
 restored=state['originalReturnStoreFrame']+1;formed=state['originalForwardStoreFrame']+1;first=int(model.previous.original.prior.one(c['text'],'MK2_MAUDIO_BEGIN')['frame']);text=c['text'];faults=[]
 def reject(label,tag,predicate,key,value,fn,remove=False):
  changed=mutate.change(text,tag,predicate,key,value,remove=remove)
  try:fn(dict(c,text=changed))
  except(ValueError,KeyError,AssertionError,StopIteration)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Changed actual morph evidence admitted: '+label)
 for key,value in(('id','17'),('roster','17'),('actor','01000000'),('main','01000000'),('floor','82'),('hp','160')):
  reject('restored actual '+key,'MK2_KO_FIELD',lambda r:r['frame']==str(restored)and r['slot']==str(side),key,value,model.physical)
 reject('true form replaced by proxy','MK2_KO_FIELD',lambda r:r['frame']==str(formed)and r['slot']==str(side),'id','0',model.physical)
 reject('actual native return opcode site changed','MK2_HUMAN_SHANG_STORE',lambda r:r['id']=='6','pc','FFA16710',model.physical)
 reject('actual return store missing','MK2_HUMAN_SHANG_STORE',lambda r:r['id']=='6','pc',None,model.physical,True)
 reject('post-return walk input reversed','MK2_HUMAN_SHANG_INPUT',lambda r:r['age']=='1100','buttons','Down',model.physical)
 reject('input attached to another actor','MK2_HUMAN_SHANG_INPUT',lambda r:r['age']=='1100','actor','01000000',lambda bad:input_provenance(bad,by))
 reject('input disguised as proxy','MK2_HUMAN_SHANG_INPUT',lambda r:r['age']=='1100','id','0',lambda bad:input_provenance(bad,by))
 for key,value in(('actor','01000000'),('main','01000000'),('id','17'),('health','161')):
  reject('retired source '+key,'MK2_INTERRUPT_OWNER',lambda r:r['frame']==str(restored)and r['slot']==str(side),key,value,lambda bad:model.previous.owners(bad,events))
 for key,value in(('loop','1'),('paused','1')):
  reject('battle channel '+key,'MK2_INTERRUPT_CHANNEL',lambda r:r['frame']==str(restored)and r['channel']==str(events[0]['channel']),key,value,lambda bad:model.previous.owners(bad,events))
 need(model.physical(c)[0]==state and input_provenance(c,by)==inputs and model.previous.owners(c,events)==owned,'Full same-run positives restored')
 for p in(Path(__file__),Path(mutate.__file__),Path(model.__file__),Path(model.previous.__file__)):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual executed sources and artifacts stable')
 report=dict(passed=True,nativeTerminal=c['terminal'],actualFaultsRejected=faults,wholeNativeInputProvenance=inputs,inputHashes=pins,allMorphContextsAccepted=False,fullRasterAcceptance=False,fullPortAcceptance=False,newNativeBoots=0,newBuilds=0,newRawMedia=0)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(move=c['move'],side=side,faults=len(faults))),flush=True);return report
