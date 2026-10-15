"""Actual native KO/reset/owner/body/input failures reject on same-run copies."""
import copy,json,re
from pathlib import Path
import qualify_launch_ko_round as base
import qualify_launch_ko_round_v2 as model
ROOT,need,sha=base.ROOT,base.need,base.sha

def change(text,tag,predicate,key,value=None,delta=None,remove=False):
 line=next(v for v in text.splitlines()if v.startswith(tag+' ')and predicate(dict(re.findall(r'(\w+)=([^\s]+)',v))))
 if remove:return text.replace(line+'\n','',1)
 old=re.search(r'\b'+key+r'=([^\s]+)',line)[1]
 if delta is not None:value=format(int(old,16)+delta,'08X')
 new=line.replace(key+'='+old,key+'='+str(value),1);need(new!=line,'Actually changed real evidence, no vacuous mutation');return text.replace(line,new,1)

def check(first,second):
 out=ROOT/'audit_launch_ko_round_faults';need(not out.exists(),'Fresh same-run fault receipt')
 proofs=[ROOT/'audit_launch_ko_round_checked_p1/report.json',ROOT/'audit_launch_ko_round_v2_checked_p2/report.json'];pins={str(Path(__file__)):sha(__file__)};cases=[]
 for c,p in zip((first,second),proofs,strict=True):
  proof=json.loads(p.read_text());need(proof['passed'],'Actual native semantic proof');pins[str(p)]=sha(p)
  for q,h in proof['inputHashes'].items():need(sha(q)==h,'All executed native source/evidence intact');pins[q]=h
  text=c['text'];positive,by=base.physical(text,c['guest']);faults=[];reset=positive['fullHealthResetFrame'];ko=positive['koFrame']
  def reject(label,fn):
   try:fn()
   except(ValueError,AssertionError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
   else:raise ValueError('Actual KO/reset/source fault admitted: '+label)
  for key,value in(('roster','1'),('id','1'),('actor','01000000'),('main','01000000'),('owner','01000000'),('floor','81'),('hp','160'),('mode','7'),('vx','00010000'),('trail','01000000')):
   bad=change(text,'MK2_KO_FIELD',lambda r:r['frame']==str(reset)and r['slot']=='1',key,value)
   reject('actual reset '+key+' changed',lambda t=bad:base.physical(t,c['guest']))
  bad=change(text,'MK2_KO_FIELD',lambda r:r['frame']==str(ko)and r['slot']=='1','hp','1');reject('actual KO health not zero',lambda:base.physical(bad,c['guest']))
  bad=change(text,'MK2_KO_FIELD',lambda r:r['frame']==str(reset)and r['slot']=='1','hp',remove=True);reject('actual reset field omitted',lambda:base.physical(bad,c['guest']))
  bad=change(text,'MK2_INTERRUPT_HEALTH',lambda r:r['after']=='0','pc',delta=16);reject('actual lethal native opcode site changed',lambda:base.physical(bad,c['guest']))
  bad=change(text,'MK2_INTERRUPT_HEALTH',lambda r:r['pc']=='FF9DEF40','after','5');reject('actual original health-fill step changed',lambda:base.physical(bad,c['guest']))
  for tag in('MK2_INTERRUPT_IO','MK2_INTERRUPT_LOW_IO'):
   row=base.rows(text,tag)[0];bad=change(text,tag,lambda r:r==row,'value',value=format(int(row['value'],16)^1,'04X'))
   reject('actual native input bit '+tag+' changed',lambda t=bad:base.mirror.delivery.delivered(t))
  for tag,key in(('MK2_HPHASE_CANDIDATE','source'),('MK2_HPHASE_QUEUE','xy')):
   bad=change(text,tag,lambda r:r['frame']==str(positive['rearmRecovered']),key,delta=8 if key=='source'else 1)
   reject('actual post-reset body '+key+' changed',lambda t=bad:base.body_publication(t,c['guest'],by))
  # Source-state clocks and actual channels survive in the first digest log.
  # That does not restore its lost PCM or upgrade its waveform acceptance.
  state=dict(c,pcmHeaders=base.rows(text,'MK2_BBAUDIO_PCM_DIGEST'))
  epins={};events=model.events(state,epins);owned=base.owners(state,events);pins.update(epins)
  for key,value in(('actor','01000000'),('main','01000000'),('id','17'),('health','161')):
   bad=change(text,'MK2_INTERRUPT_OWNER',lambda r:r['frame']==str(reset)and r['slot']=='2',key,value)
   reject('actual stale post-reset source '+key,lambda t=bad:base.owners(dict(state,text=t),events))
  restored,restored_by=base.physical(text,c['guest']);need(restored==positive and restored_by==by,'Complete native positive restored after every counterexample')
  cases.append(dict(side=c['side'],nativeTerminal=c['terminal'],actualFaultsRejected=faults,completeIndependentOwnership=owned,
                    sourceEvents=[{k:v for k,v in e.items()if k not in('sample','positions')}for e in events],
                    fullPCMComparisonAddedForFirstHost=False))
  print(json.dumps(dict(side=c['side'],actualFaultsRejected=len(faults),completeOwnerFields=owned['completeOwnerFields'])),flush=True)
 for path in(Path(base.__file__),Path(model.__file__)):pins[str(path)]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'Whole positive/evidence/source pins stable')
 report=dict(passed=True,cases=cases,actualFaultsRejected=sum(len(c['actualFaultsRejected'])for c in cases),inputHashes=pins,
             firstHostFullPCMComparisonAccepted=False,allKOResetMorphCoverageAccepted=False,fullPortAcceptance=False,goalStatus='active',newNativeBoots=0,newBuilds=0,newRawMedia=0)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
