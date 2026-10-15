"""Read-only actual incoming collision timing in the accepted held-crouch runs."""
import argparse,json
from collections import Counter
from pathlib import Path
import analyze_current_boss_uppercut_windows_v2186 as previous
ROOT=previous.ROOT

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 previous.need(not args.output.exists(),'Immutable incoming analysis')
 source=ROOT/'audit_v2187_current_boss_uppercut_windows/report.json';proof=json.loads(source.read_text())
 previous.need(proof['passed'],'Accepted window context');pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():previous.need(previous.launch.sha(file)==wanted,'Unchanged window source graph '+file)
 pins[str(source)]=previous.launch.sha(source);cases={}
 for name in ('kano','sonya'):
  rows=previous.ledger.native.parse((ROOT/f'audit_v2177_current_{name}_p1_held_boss_uppercut_campaign/run.log').read_text(encoding='utf-8-sig'),1,name)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
  plans=[r['frame']for r in rows if r['tag']=='BOSS_PLAN'];starts=[f for f in fields if f-1 not in fields]
  groups=Counter();details=[]
  for r in rows:
   if r['tag']!='HEALTH'or r['pc']!=0xff836700 or r['slot']!=1 or r['after']>=r['before']or r['frame']not in fields:continue
   f=fields[r['frame']]
   previous.need(r['a8']==f['cpu_actor']and r['a13']==f['cpu_main'],'Incoming damage uses the actual native CPU actor/Main')
   amount=r['before']-r['after'];start=max(s for s in starts if s<=r['frame'])
   prior=max((s for s in plans if start<=s<=r['frame']),default=-1)
   age=r['frame']-prior if prior>=0 else None
   groups[f"own{f['human_action']:04X}_cpu{f['cpu_action']:04X}"]+=amount
   groups['warm120'if r['frame']-start<120 else 'after_warm']+=amount
   groups['cooldown_under90'if age is not None and age<90 else 'no_recent_attempt']+=amount
   details.append(dict(frame=r['frame'],damage=amount,ownAction=f['human_action'],cpuAction=f['cpu_action'],
    cpuHeight=f['cpu_height'],gap=f['gap'],ownHeight=f['height'],flags=f['flags'],body=f['body'],
    fieldsSinceRound=start and r['frame']-start,fieldsSinceAttempt=age))
  cases[name]=dict(incomingEvents=len(details),totalIncomingDamage=sum(r['damage']for r in details),groups=dict(groups),events=details)
 pins[str(Path(__file__).resolve())]=previous.launch.sha(__file__);previous.launch.module_pins(pins)
 report=dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)
 args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:{a:b for a,b in v.items()if a!='events'}for k,v in cases.items()},indent=2),flush=True)

if __name__=='__main__':main()
