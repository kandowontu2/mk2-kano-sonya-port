"""Actual physically pressed HP edges, native boss height and motion direction.
Distinguishes a cancelled/planned HP window from a button really requested.
No source/capture writes, no all-boss/ending or whole-port acceptance.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
import verify_current_prepared_boss_ledger_v2255 as prepared
import verify_current_ready_crouch_boss_ledger_v2274 as ready
ROOT=prepared.ROOT

def need(ok,message):
 if not ok:raise ValueError(message)

def verify():
 source=ROOT/'audit_v2277_current_boss_height_windows/report.json';proof=json.loads(source.read_text())
 need(proof['passed']and not proof['gameOrCaptureModified'],'Accepted native107/hit chronology')
 pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():need(prepared.launch.sha(file)==wanted,'Unchanged current actual graph '+file)
 pins[str(source)]=prepared.launch.sha(source);cases={}
 for module in (prepared,ready):
  for case,(fighter,side,capture,positive)in module.CASES.items():
   rows=module.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
   module.check(rows,17 if fighter=='kano'else 18,side)
   fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
   plans=[r for r in rows if r['tag']=='BOSS_PLAN']
   hp=[r for r in rows if r['tag']=='INPUT'and r['button']=='High_Punch'and r['frame']in fields]
   groups=defaultdict(lambda:dict(plans=0,native107=0,ownedHitPlans=0,ownedDamage=0))
   windows=[]
   for i,p in enumerate(plans):
    known=proof['cases'][case]['windows'][i];start=p['frame']
    need(known['start']==start,'Same actual physical plan chronology')
    stop=min(start+36,plans[i+1]['frame']if i+1<len(plans)else start+36)
    pressed=[r['frame']for r in hp if start<=r['frame']<stop]
    first=pressed[0]if pressed else None;f=fields.get(first);previous=fields.get(first-1)if first is not None else None
    direction='no_actual_HP';velocity=None;delta=None;height=None
    if f:
     velocity=f['cpu_vy'];velocity=velocity-0x100000000 if velocity&0x80000000 else velocity
     height=f['cpu_height']
     if previous and all(previous[k]==f[k]for k in('stage','cpu_actor','cpu_main')):
      delta=f['cpu_height']-previous['cpu_height'];direction='rising'if delta>0 else'descending'if delta<0 else'held'
     else:direction='missing_adjacent_field'
    bucket='missing'if height is None else'ground'if height<=0 else'1_80'if height<=80 else'81_160'if height<=160 else'161_240'if height<=240 else'241_plus'
    key=f"cpu_{f['cpu_action']:04X}_{bucket}_{direction}"if f else'cancelled_before_actual_HP'
    g=groups[key];g['plans']+=1;g['native107']+=len(known['actual107Frames']);g['ownedHitPlans']+=known['ownedDamage']>0;g['ownedDamage']+=known['ownedDamage']
    need(not known['actual107Frames']or pressed,'No human107credited to an unpressed physical HP command')
    windows.append(dict(start=start,actualHPFields=pressed,firstActualHPFrame=first,cpuHeight=height,
     cpuHeightDelta=delta,cpuSignedVelocity=velocity,direction=direction,
     actual107Frames=known['actual107Frames'],ownedDamage=known['ownedDamage']))
   need(sum(g['native107']for g in groups.values())==proof['cases'][case]['actualHuman107Assignments'],'All actual107preserved')
   cases[case]=dict(groups=dict(groups),windows=windows)
 pins[str(Path(__file__).resolve())]=prepared.launch.sha(__file__);prepared.launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable physical HP geometry evidence')
 result=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v['groups']for k,v in result['cases'].items()},indent=2),flush=True)
