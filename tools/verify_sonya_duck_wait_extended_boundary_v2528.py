"""Retain rejected timed-cutoff selection; prove longer unchanged input run completes it.
No capture, ID, health, game balance, CPU or guest state is modified.
"""
import json,re
from pathlib import Path
import verify_current_boss_shao_duck_wait_v2514 as native
ROOT=native.ROOT;launch=native.current_launch
OLD=ROOT/'audit_v2497_current_sonya_p1_shao_duck_wait_campaign'
NEW=ROOT/'audit_v2515_current_sonya_p1_shao_duck_wait_campaign'
OUT=ROOT/'audit_v2529_current_sonya_duck_wait_extended_boundary'
def need(ok,label):
 if not ok:raise ValueError(label)
def exact(a,b):need(a==b,'Complete rejected-capture chronology unchanged before original timed cutoff')
def verify():
 pins={}
 def graph(path,passed):
  report=json.loads(path.read_text());need(report['passed']==passed and not report['fullPortAcceptance'],'Exact retained full-verifier outcome')
  for file,digest in report['inputHashes'].items():
   if file in pins:need(pins[file]==digest,'Consistent graph')
   else:need(launch.sha(file)==digest,'Unchanged actual source/capture '+file);pins[file]=digest
  pins[str(path)]=launch.sha(path);return report
 failed=graph(ROOT/'audit_v2508_current_sonya_p1_shao_duck_wait_checked/report.json',False)
 accepted=graph(ROOT/'audit_v2516_current_sonya_p1_shao_duck_wait_checked/report.json',True)
 need(failed['errors']==['Own true ID before native confirm'],'Only original real incomplete selection failure, not discarded gameplay errors')
 before=json.loads((OLD/'result.json').read_text(encoding='utf-8-sig'));after=json.loads((NEW/'result.json').read_text(encoding='utf-8-sig'))
 need(before['seconds']==3600 and after['seconds']==3610,'Longer actual observation, never shorten to avoid failure')
 for key in('candidate','executable_sha256','payload_sha256','player','human_slot','cpu_slot','strategy','boot_frame','boss_policy','cheats_enabled','assistance'):
  need(before[key]==after[key],'Same real control/build '+key)
 old_text=(OLD/'run.log').read_text(encoding='utf-8-sig');new_text=(NEW/'run.log').read_text(encoding='utf-8-sig')
 old_rows=native.parse(old_text,1,'sonya');new_rows=native.parse(new_text,1,'sonya')
 terminal=next(r for r in old_rows if r['tag']=='RESULT');cutoff=terminal['frame']
 def prefix(text):return [line for line in text.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and (m:=re.search(r' frame=(\d+)',line))and int(m[1])<cutoff]
 old_prefix=prefix(old_text);new_prefix=prefix(new_text);exact(old_prefix,new_prefix)
 selection=next(r for r in old_rows if r['tag']=='SELECT'and r['number']==52)
 need(selection['initial']==1 and selection['target']==18 and selection['stage']==16 and selection['frame']==196845,'Actual original final paid-continue selection still in progress')
 need(not any(r['tag']=='SELECT_ID'and r['number']==52 for r in old_rows),'Rejected original capture has no fabricated confirm')
 for number in range(1,52):
  confirmations=[r for r in old_rows if r['tag']=='SELECT_ID'and r['number']==number]
  need(len(confirmations)==2 and all(r['roster']==18 and r['state']==3 for r in confirmations),'Every earlier original selection genuinely confirmed own Sonya')
 new_selection=next(r for r in new_rows if r['tag']=='SELECT'and r['number']==52)
 need({k:v for k,v in selection.items()if k!='event'}=={k:v for k,v in new_selection.items()if k!='event'},'Same final original native selection, not reseeded or substituted')
 confirmations=[r for r in new_rows if r['tag']=='SELECT_ID'and r['number']==52]
 need(len(confirmations)==2 and all(r['frame']>cutoff and r['roster']==18 and r['state']==3 for r in confirmations),'Longer real input route completes both actual Sonya18preconfirm observations')
 following=next(r for r in new_rows if r['tag']=='LIVE'and r['frame']>max(c['frame']for c in confirmations))
 need(following['stage']==16 and following['human']=='18:18'and following['cpu']=='13:13','Original confirmed Sonya proceeds into real Shao fight with both true IDs')
 index=next(i for i,line in enumerate(new_prefix)if line.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD '));negatives=[]
 for label in('missing field','changed real ID','changed real health'):
  altered=list(new_prefix)
  if label=='missing field':altered.pop(index)
  elif label=='changed real ID':altered[index]=altered[index].replace('human_id=18','human_id=1',1)
  else:altered[index]=re.sub(r' health=(\d+),',lambda m:' health='+str(int(m[1])-1)+',',altered[index],count=1)
  need(altered!=new_prefix,'Non-vacuous prefix counterexample')
  try:exact(old_prefix,altered)
  except ValueError as error:
   need(str(error)=='Complete rejected-capture chronology unchanged before original timed cutoff','Specific preserved chronology rejection');negatives.append(dict(label=label,rejected=True))
  else:raise ValueError('Modified original chronology accepted')
 exact(old_prefix,new_prefix);pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,originalFullCaptureRemainsRejected=True,originalError=failed['errors'],
  oldSeconds=3600,newSeconds=3610,originalCutoffFrame=cutoff,exactOriginalNativeRows=len(old_prefix),
  earlierActuallyConfirmedSonyaSelections=51,pendingSelectionNumber=52,
  genuineExtendedConfirmFrames=[c['frame']for c in confirmations],actualFollowingLiveFrame=following['frame'],
  actualHumanID=18,actualCPU_ID=13,rejectedSpecificPrefixCounterexamples=negatives,
  originalFailedCaptureNeverWaived=True,gameOrCaptureModified=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Immutable real longer-observation boundary proof')
 report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
