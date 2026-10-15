"""Locate actual incoming boss damage in unchanged physical-input campaigns.
Native HP writer and actor/action chronology, not assumptions about animation.
No game writes and no full campaign/port acceptance implied.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
import verify_current_prepared_boss_ledger_v2255 as ledger
ROOT=ledger.ROOT

def need(ok,message):
 if not ok:raise ValueError(message)

def verify():
 pins={};cases={}
 def accept(path):
  report=json.loads(path.read_text());need(report['passed'],'Accepted full campaign/ledger '+str(path))
  for file,wanted in report['inputHashes'].items():
   if file not in pins:need(ledger.launch.sha(file)==wanted,'Unchanged actual source/capture '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent actual graph '+file)
  pins[str(path)]=ledger.launch.sha(path)
  return report
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof=accept(ROOT/positive/'report.json')
  accepted=accept(ROOT/f'audit_v2256_current_{case}_boss_ledger_checked/report.json')
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  control=ledger.check(rows,17 if fighter=='kano'else 18,side)
  need(control['originalHuman107Assignments']==accepted['originalHuman107Assignments'],'Full native ledger control')
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
  groups=defaultdict(lambda:dict(stores=0,damage=0))
  incoming=[]
  for r in rows:
   if r['tag']!='HEALTH'or r['slot']!=side or r['pc']!=0xff836700 or r['after']>=r['before']or r['frame']not in fields:continue
   f=fields[r['frame']];amount=r['before']-r['after']
   for key in (f"own_{f['human_action']:04X}",f"cpu_{f['cpu_action']:04X}"):
    groups[key]['stores']+=1;groups[key]['damage']+=amount
   incoming.append(dict(frame=r['frame'],before=r['before'],after=r['after'],nativeWriter=f"{r['pc']:08X}",
    ownAction=f['human_action'],cpuAction=f['cpu_action'],gap=f['gap'],height=f['height'],cpuHeight=f['cpu_height']))
  rounds=[];current=None
  for frame,f in sorted(fields.items()):
   if current is None or frame!=current['lastFrame']+1:
    current=dict(firstFrame=frame,lastFrame=frame,initialHealth=f['health'],lastPositiveHealth=f['health'],stage=f['stage']);rounds.append(current)
   current['lastFrame']=frame;current['lastPositiveHealth']=f['health']
  for r in rounds:
   damage=[d for d in incoming if r['firstFrame']<=d['frame']<=r['lastFrame']]
   r['incomingDamage']=sum(d['before']-d['after']for d in damage)
   r['actualHuman107Assignments']=sum(a['tag']=='BOSS_ACTION'and a['after']==0x107 and r['firstFrame']<=a['frame']<=r['lastFrame']for a in rows)
   r['ownNativeRoundWinFrames']=[a['frame']for a in rows if a['tag']=='WIN'and a['slot']==side and a['stage']==r['stage']and r['firstFrame']<=a['frame']<=r['lastFrame']+8]
  cases[case]=dict(actualHuman107Assignments=proof['actualNativeUppercutAssignments'],ownBossRoundWins=proof['actualBossRoundWins'],
   actualIncomingNativeDamageStores=len(incoming),actualIncomingNativeDamage=sum(d['before']-d['after']for d in incoming),groups=dict(groups),rounds=rounds,incoming=incoming)
 pins[str(Path(__file__).resolve())]=ledger.launch.sha(__file__);ledger.launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable incoming-damage proof')
 result=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:{'nativeIncomingDamage':v['actualIncomingNativeDamage'],'groups':v['groups']}for k,v in result['cases'].items()},indent=2),flush=True)
