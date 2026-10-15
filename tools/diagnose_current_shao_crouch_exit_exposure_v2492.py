"""Ordered incoming301damage and preceding physical inputs; no causal attack claim."""
import json,argparse,bisect
from pathlib import Path
from collections import defaultdict
import verify_current_shao_crouch_exit_boss_ledger_v2466 as ledger
from analyze_current_shao_opening_damage_states_v2408 import own_damage
ROOT=ledger.ROOT;launch=ledger.launch
def need(ok,label):
 if not ok:raise ValueError(label)
def diagnose():
 progress_path=ROOT/'audit_v2472_current_shao_crouch_exit_progress/report.json'
 progress=json.loads(progress_path.read_text());need(progress['passed'],'Accepted actual native progress')
 pins=dict(progress['inputHashes']);pins[str(progress_path)]=launch.sha(progress_path);cases={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  path=ROOT/capture/'run.log';need(launch.sha(path)==pins[str(path)],'Unchanged actual capture')
  rows=ledger.native.parse(path.read_text(encoding='utf-8-sig'),side,fighter);ledger.check(rows,17 if fighter=='kano'else 18,side)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16}
  inputs=defaultdict(set)
  for row in rows:
   if row['tag']=='INPUT'and row['frame']in fields:inputs[row['frame']].add(row['button'])
  plans=[r for r in rows if r['tag']=='BOSS_PLAN'and r['stage']==16]
  plan_frames=[r['frame']for r in plans]
  episodes=[];groups=defaultdict(lambda:dict(stores=0,damage=0))
  for hit in own_damage(rows,side):
   if hit['actionAtOwnDamage']!=0x301:continue
   frame=hit['frame'];field=fields[frame]
   at=bisect.bisect_right(plan_frames,frame)-1;plan=plans[at]if at>=0 else None
   near=plan if plan and frame-plan['frame']<=16 and plan['human_actor']==field['human_actor']and plan['human_main']==field['human_main']else None
   key=('within16fields_of_'+near['move'])if near else 'no_recent_same_actor_plan'
   groups[key]['stores']+=1;groups[key]['damage']+=hit['damage']
   window=[]
   for t in range(frame-16,frame+1):
    f=fields.get(t)
    if not f or (f['human_actor'],f['human_main'])!=(field['human_actor'],field['human_main']):continue
    window.append(dict(frame=t,action=f['human_action'],gap=f['gap'],cpuPose=f['cpu_pose'],cpuAction=f['cpu_action'],buttons=sorted(inputs[t])))
   episodes.append(dict(frame=frame,actualDamage=hit['damage'],actualActionAtDamage=0x301,
    sameActorRecentPlan=near,precedingPhysicalWindow=window,classification=key))
  need(sum(e['actualDamage']for e in episodes)==progress['cases'][case]['actualShaoIncomingDamageByActualAction']['nativeAction_0301']['damage'],'Every actual301incoming store accounted')
  cases[case]=dict(actual301DamageStores=len(episodes),actual301Damage=sum(e['actualDamage']for e in episodes),
   measuredPlanProximityGroups=dict(groups),episodes=episodes,
   scope='Actual preceding physical commands and native action at damage; proximity does not establish causal CPU attack or character defect')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable native exposure diagnostic')
 r=diagnose();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({case:{k:v for k,v in row.items()if k!='episodes'}for case,row in r['cases'].items()},indent=2),flush=True)
