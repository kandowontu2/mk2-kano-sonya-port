"""Actual damage/action chronology through native boss guard-release commands.
Read-only accepted real-input records. Damage provenance is the physical HP
slot/original collision writer, not an assumed CPU Main for child projectiles.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
import verify_current_boss_guard_edge_ledger_v2227 as ledger
ROOT=ledger.ROOT

def need(ok,message):
 if not ok:raise ValueError(message)

def verify():
 source=ROOT/'audit_v2245_current_boss_guard_phase/report.json';proof=json.loads(source.read_text());need(proof['passed'],'Accepted native phase context')
 pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():need(ledger.launch.sha(file)==wanted,'Unchanged accepted actual graph '+file)
 pins[str(source)]=ledger.launch.sha(source);cases={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  ledger.check(rows,17 if fighter=='kano'else 18,side)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
  actions=[r for r in rows if r['tag']=='BOSS_ACTION']
  incoming=[r for r in rows if r['tag']=='HEALTH'and r['slot']==side and r['pc']==0xff836700 and r['after']<r['before']]
  groups=defaultdict(lambda:dict(plans=0,activated=0,damagedBeforeRequestedHP=0,damagedDuringHP=0,nonstanceAtRequestedHP=0))
  windows=[];lead=16 if case.endswith('16')else 12
  for p in (r for r in rows if r['tag']=='BOSS_PLAN'):
   start=p['frame'];hp=start+lead;stop=start+36
   actual=[a for a in actions if start<=a['frame']<stop and a['after']==0x107 and a['actor']==p['human_actor']and a['main']==p['human_main']]
   damage=[r for r in incoming if start<=r['frame']<stop]
   before=[r for r in damage if r['frame']<hp];during=[r for r in damage if hp<=r['frame']<hp+8]
   f=fields.get(hp)
   free=bool(f and f['human_actor']==p['human_actor']and f['human_main']==p['human_main']and f['height']==0 and f['human_action']in(0x302,0x303,0x304)and not f['flags']&0x0c and not f['body']&0x0c)
   keys=[f"cpu_{p['cpu_action']:04X}",'activated'if actual else'missing107']
   for key in keys:
    g=groups[key];g['plans']+=1;g['activated']+=bool(actual);g['damagedBeforeRequestedHP']+=bool(before);g['damagedDuringHP']+=bool(during);g['nonstanceAtRequestedHP']+=not free
   windows.append(dict(frame=start,hpRequestFrame=hp,cpuAction=p['cpu_action'],cpuHeight=p['cpu_height'],gap=p['gap'],ownAction=p['human_action'],
    actual107Frames=[r['frame']for r in actual],firstHPAction=f['human_action']if f else None,firstHPHeight=f['height']if f else None,
    firstHPFlags=f['flags']if f else None,firstHPBody=f['body']if f else None,actualNativeStanceAtHP=free,
    incoming=[dict(frame=r['frame'],before=r['before'],after=r['after'],pc=r['pc'],a8=r['a8'],a13=r['a13'])for r in damage],
    damagedBeforeRequestedHP=bool(before),damagedDuringHP=bool(during)))
  need(sum(len(w['actual107Frames'])for w in windows)==proof['cases'][case]['actual107Assignments'],'All132real107assignments accounted for, never assumed from commands')
  cases[case]=dict(groups=dict(groups),windows=windows)
 pins[str(Path(__file__).resolve())]=ledger.launch.sha(__file__);ledger.launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 need(not args.output.exists(),'Immutable native release analysis')
 result=verify();args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v['groups']for k,v in result['cases'].items()},indent=2),flush=True)
