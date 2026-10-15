"""Native jump/air-kick dispatch and actual HP chronology in real boss inputs.
Planned Up or observed airborne hurt states do not prove an executed jump.
Quiet-window incoming damage is measured, not called inherently avoidable.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
import verify_current_stomp_window_boss_ledger_v2288 as old
import verify_current_escape_hold_boss_ledger_v2298 as held
ROOT=old.ROOT

def need(ok,message):
 if not ok:raise ValueError(message)

def verify():
 pins={};cases={}
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Accepted actual source/trajectory '+str(path))
  for file,wanted in r['inputHashes'].items():
   if file not in pins:need(old.launch.sha(file)==wanted,'Unchanged actual graph '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent actual graph '+file)
  pins[str(path)]=old.launch.sha(path);return r
 for module,ledger_version in((old,2299),(held,2300)):
  for case,(fighter,side,capture,positive)in module.CASES.items():
   proof=accept(ROOT/positive/'report.json');book=accept(ROOT/f'audit_v{ledger_version}_current_{case}_boss_ledger_checked/report.json')
   accept(ROOT/f'audit_v2301_current_{case}_input_counterexamples/report.json')
   rows=module.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
   module.check(rows,17 if fighter=='kano'else 18,side)
   fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
   actions=[r for r in rows if r['tag']=='BOSS_ACTION']
   jumps=[r for r in actions if r['after']==0x308 and r['pc']==0xff831360]
   kicks=[r for r in actions if r['after']==0x200 and r['pc']==0xff871f50]
   for r in jumps+kicks:
    need(r['a8']==r['actor']==r['owner']and r['a13']==r['main']and r['mask']==65535 and r['id']==r['roster']==(17 if fighter=='kano'else 18),'Original native human jump/airkick dispatch owner and actual registers')
   combat=[r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before']]
   incoming=[r for r in combat if r['slot']==side and r['frame']in fields]
   owned=[r for r in combat if r['slot']==3-side and r['frame']in fields and r['a8']==fields[r['frame']]['human_actor']and r['a13']==fields[r['frame']]['human_main']]
   damage_groups=defaultdict(lambda:dict(stores=0,damage=0,cpuGuardStores=0))
   for r in owned:
    f=fields[r['frame']];g=damage_groups[f"own_{f['human_action']:04X}"]
    g['stores']+=1;g['damage']+=r['before']-r['after'];g['cpuGuardStores']+=f['cpu_action']in(0x700,0x701)
   plans=[r for r in rows if r['tag']=='BOSS_PLAN'and r['move']=='close_pressure_jumpkick_attempt']
   windows=[];mapped=set()
   for i,p in enumerate(plans):
    start=p['frame'];stop=min(start+60,plans[i+1]['frame']if i+1<len(plans)else start+60)
    actual=[r for r in jumps if start<=r['frame']<stop and r['actor']==p['human_actor']and r['main']==p['human_main']]
    attacks=[r for r in kicks if start<=r['frame']<stop and r['actor']==p['human_actor']and r['main']==p['human_main']]
    for r in actual:need(r['event']not in mapped,'Native jump uniquely assigned to actual physical plan');mapped.add(r['event'])
    flight_damage=[r for r in owned if start<=r['frame']<stop and fields[r['frame']]['human_action']==0x200]
    windows.append(dict(start=start,gap=p['gap'],ownStartAction=p['human_action'],actualJumpFrames=[r['frame']for r in actual],
     actualAirKickFrames=[r['frame']for r in attacks],airKickDamage=sum(r['before']-r['after']for r in flight_damage),
     guardedAirKickDamage=sum(r['before']-r['after']for r in flight_damage if fields[r['frame']]['cpu_action']in(0x700,0x701))))
   need(len(mapped)==len(jumps),'Every actual308jump mapped once, no hurt-flight promoted to a jump')
   rounds=[];current=None
   for frame,f in sorted(fields.items()):
    if current is None or frame!=current['lastFrame']+1:
     current=dict(firstFrame=frame,lastFrame=frame,initialHealth=f['health'],healthAfterQuiet=None);rounds.append(current)
    current['lastFrame']=frame
    if frame-current['firstFrame']==119:current['healthAfterQuiet']=f['health']
   for r in rounds:
    quiet=[d for d in incoming if r['firstFrame']<=d['frame']<r['firstFrame']+120]
    r['actualQuietDamage']=sum(d['before']-d['after']for d in quiet)
   need(len(owned)==proof['actualBossOwnedDamageStores'],'All own original-writer boss damage inventoried')
   need(sum(g['damage']for k,g in damage_groups.items()if k=='own_0107')==proof['actualBossUppercutDamage']==book['ownBossUppercutDamage'],'Native107damage accounting exactly retained')
   cases[case]=dict(actualHuman308Jumps=len(jumps),actualHuman200AirKicks=len(kicks),physicalJumpkickPlans=len(plans),
    actualOwnedBossDamage=sum(r['before']-r['after']for r in owned),ownedDamageGroups=dict(damage_groups),jumpWindows=windows,
    actualQuietWindowIncomingDamage=sum(r['actualQuietDamage']for r in rounds),actualPositiveHealthBossSegments=len(rounds),rounds=rounds)
 pins[str(Path(__file__).resolve())]=old.launch.sha(__file__);old.launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable native jump/quiet chronology')
 result=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:{q:v[q]for q in('actualHuman308Jumps','actualHuman200AirKicks','physicalJumpkickPlans','ownedDamageGroups','actualQuietWindowIncomingDamage','actualPositiveHealthBossSegments')}for k,v in result['cases'].items()},indent=2),flush=True)
