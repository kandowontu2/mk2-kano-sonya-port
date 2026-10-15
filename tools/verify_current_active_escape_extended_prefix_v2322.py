"""Preserve a timer-truncated selection diagnostic; require a complete real replay.
Every original native record, including drawing rows, must be an exact prefix.
No ID/confirmation gate is waived and no captured record is edited.
"""
import argparse,json,re
from pathlib import Path
import verify_current_boss_active_escape_campaign_v2308 as native
ROOT=native.ROOT;launch=native.current_launch
OLD=ROOT/'audit_v2309_current_kano_p1_escape_active_early_campaign'
NEW=ROOT/'audit_v2315_current_kano_p1_escape_active_early_extended_campaign'
FAILED=ROOT/'audit_v2310_current_kano_p1_escape_active_early_checked/report.json'
ACCEPTED=ROOT/'audit_v2316_current_kano_p1_escape_active_early_extended_checked/report.json'

def need(ok,message):
 if not ok:raise ValueError(message)

def lines(path,limit=None):
 result=[]
 with path.open(encoding='utf-8-sig') as stream:
  for line in stream:
   if not line.startswith('MK2_NAT_CAMPAIGN_') or line.startswith('MK2_NAT_CAMPAIGN_RESULT '):continue
   frame=int(re.search(r' frame=(\d+)',line)[1])
   if limit is None or frame<=limit:result.append(line.rstrip('\r\n'))
 return result

def exact(a,b):
 need(a==b,'Entire actual native prefix, with all fields and drawing records retained')

def verify():
 failed=json.loads(FAILED.read_text());proof=json.loads(ACCEPTED.read_text())
 need(not failed['passed'] and failed['errors']==['Own true ID before native confirm'],'Preserved original failure has only missing pre-confirmation evidence')
 need(proof['passed'] and proof['bounded_campaign_evidence_proven'] and not proof['fullPortAcceptance'],'Entire extended replay passes unchanged native ID/confirmation/progression gates')
 pins={}
 for result in (failed,proof):
  for file,wanted in result['inputHashes'].items():
   if file not in pins:need(launch.sha(file)==wanted,'Unchanged actual input/capture '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent actual input graph '+file)
 for path in (FAILED,ACCEPTED,Path(__file__).resolve()):pins[str(path)]=launch.sha(path)
 old_rows=native.parse((OLD/'run.log').read_text(encoding='utf-8-sig'),1,'kano')
 new_rows=native.parse((NEW/'run.log').read_text(encoding='utf-8-sig'),1,'kano')
 final=next(r for r in old_rows if r['tag']=='RESULT')
 last=max((r for r in old_rows if r['tag']=='SELECT'),key=lambda r:r['number'])
 missing=[r for r in old_rows if r['tag']=='SELECT_ID' and r['number']==last['number']]
 need(last['number']==17 and not missing and final['frame']-last['frame']==79,'Fixed recording limit ended at selection age79, before actual130/146samples')
 need(all(len([r for r in old_rows if r['tag']=='SELECT_ID' and r['number']==n and r['roster']==17 and r['state']==3])==2 for n in range(1,17)),'All sixteen prior actual selections have both true-ID confirmations')
 extension=[r for r in new_rows if r['tag']=='SELECT_ID' and r['number']==17]
 need([(r['frame']-last['frame'],r['roster'],r['state']) for r in extension]==[(130,17,3),(146,17,3)],'Actual later true Kano IDs in both original pre-confirmation fields')
 a=lines(OLD/'run.log');b=lines(NEW/'run.log',final['frame']);exact(a,b)
 need(len(a)>100000,'Non-vacuous complete native prefix')
 index=next(i for i,line in enumerate(b) if line.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD '))
 corruptions=[]
 for name in ('missing_native_field','changed_native_identity','changed_native_health'):
  changed=list(b)
  if name=='missing_native_field':changed.pop(index)
  elif name=='changed_native_identity':changed[index]=changed[index].replace('human_id=17','human_id=1',1)
  else:changed[index]=re.sub(r' health=(\d+),',lambda m:' health='+str(int(m[1])-1)+',',changed[index],count=1)
  need(changed!=b,'Specific prefix corruption is non-vacuous')
  try:exact(a,changed)
  except ValueError as error:need('Entire actual native prefix' in str(error),'Specific prefix invariant');corruptions.append(name)
  else:raise ValueError('Malformed full native prefix accepted')
 exact(a,b);launch.module_pins(pins)
 return dict(passed=True,preservedFailure=str(FAILED),acceptedCompleteReplay=str(ACCEPTED),
  originalTerminalFrame=final['frame'],originalTerminalSelection=17,originalTerminalSelectionAge=79,
  exactOriginalNativeRecords=len(a),completeNativePrefixWithoutNormalization=True,
  actualExtendedConfirmationFrames=[r['frame'] for r in extension],
  rejectedSpecificCounterexamples=len(corruptions),inputHashes=pins,gameOrCaptureModified=False,
  identityGateWaived=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 need(not args.output.exists(),'Immutable complete native prefix proof')
 result=verify();args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({key:value for key,value in result.items() if key!='inputHashes'},indent=2),flush=True)
