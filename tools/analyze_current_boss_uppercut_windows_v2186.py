"""Source-bound actual human107 windows, not controller intents or assumed hits.
Read-only analysis of six immutable native campaigns. Does not establish a full
boss match, ending, universal gameplay, artistic or audio acceptance.
"""
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path
import verify_current_boss_action_health_ledger_v2184 as ledger
import verify_current_interrupt_v1870 as launch
ROOT=ledger.ROOT

def need(ok,message):
 if not ok:raise ValueError(message)

def analyze(case,pins):
 fighter,side,capture,positive=ledger.CASES[case]
 path=ROOT/f'audit_v2185_current_{case}_boss_ledger_checked/report.json'
 accepted=json.loads(path.read_text());need(accepted['passed']and accepted['finalUnmodifiedControlPassed'],'Accepted complete native action/health ledger')
 for file,wanted in accepted['inputHashes'].items():
  need(file not in pins or pins[file]==wanted,'Consistent dependency graph')
  if file not in pins:need(launch.sha(file)==wanted,'Unchanged accepted source/capture dependency '+file)
  pins[file]=wanted
 pins[str(path)]=launch.sha(path)
 rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
 control=ledger.check(rows,17 if fighter=='kano'else 18,side)
 need(control['originalHuman107Assignments']==accepted['originalHuman107Assignments'],'Replayed actual native action/health ledger')
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
 actions=defaultdict(list);damage=defaultdict(list)
 for r in rows:
  if r['tag']=='BOSS_ACTION':actions[r['frame']].append(r)
  if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before']:damage[r['frame']].append(r)
 windows=[]
 for r in rows:
  if r['tag']!='BOSS_ACTION'or r['after']!=0x107:continue
  start=r['frame'];f=fields.get(start)
  need(f is not None,'Actual assignment has same-field physical geometry')
  outgoing=incoming=0;hit_frames=[];incoming_frames=[];end=start
  # Include the assignment field and each consecutive actual pre-input107
  # field, stopping at its original next-action assignment or a native gap.
  for frame in range(start,start+512):
   actual=fields.get(frame)
   if not actual or any(actual[k]!=f[k]for k in('human_actor','human_main','cpu_actor','cpu_main','stage')):break
   if frame>start and actual['human_action']!=0x107:break
   end=frame
   for hp in damage[frame]:
    amount=hp['before']-hp['after']
    if hp['slot']==3-side and hp['a8']==f['human_actor']and hp['a13']==f['human_main']:
     outgoing+=amount;hit_frames.append(frame)
    elif hp['slot']==side and hp['a8']==f['cpu_actor']and hp['a13']==f['cpu_main']:
     incoming+=amount;incoming_frames.append(frame)
   if any(a['event']>r['event']and a['after']!=0x107 for a in actions[frame]):break
  windows.append(dict(frame=start,last107Field=end,fields=end-start+1,
   cpuHeight=f['cpu_height'],cpuAction=f['cpu_action'],gap=f['gap'],
   ownActionBefore=r['before'],outgoingDamage=outgoing,incomingDamage=incoming,
   hitFrames=hit_frames,incomingFrames=incoming_frames))
 need(len(windows)==accepted['originalHuman107Assignments'],'Every actual human107 assignment inventoried')
 groups=defaultdict(lambda:dict(assignments=0,hits=0,outgoingDamage=0,incomingDamage=0))
 for w in windows:
  height='ground_0'if w['cpuHeight']==0 else 'low_1_12'if 0<w['cpuHeight']<=12 else 'air_above12'if w['cpuHeight']>12 else 'below_floor'
  for key in(height,f"cpu_action_{w['cpuAction']:04X}",f"gap_{(w['gap']//20)*20}_{(w['gap']//20)*20+19}"):
   g=groups[key];g['assignments']+=1;g['hits']+=bool(w['outgoingDamage']);g['outgoingDamage']+=w['outgoingDamage'];g['incomingDamage']+=w['incomingDamage']
 return dict(acceptedLedger=str(path),native107Assignments=len(windows),
  hitWindows=sum(bool(w['outgoingDamage'])for w in windows),
  ownedOutgoingDamage=sum(w['outgoingDamage']for w in windows),
  ownedIncomingDamage=sum(w['incomingDamage']for w in windows),
  groupedActualAssignmentGeometry=dict(groups),windows=windows,
  nativeBossRoundWins=accepted['ownBossRoundWins'])

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 need(not args.output.exists(),'Immutable analysis successor')
 pins={};cases={case:analyze(case,pins)for case in ledger.CASES}
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 report=dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,fullPortAcceptance=False,scope=__doc__)
 args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({case:{k:v for k,v in data.items()if k not in('windows','acceptedLedger')}for case,data in cases.items()},indent=2),flush=True)

if __name__=='__main__':main()
