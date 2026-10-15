"""Actual requested-HP height windows and native action/hit outcomes.
Every native107 mapped once to a physical plan; intentions never imply hits.
Full current guest, action and health ledgers accepted before analysis.
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
 pins={};cases={}
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Accepted actual context '+str(path))
  for file,wanted in r['inputHashes'].items():
   if file not in pins:need(prepared.launch.sha(file)==wanted,'Unchanged context '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent immutable graph '+file)
  pins[str(path)]=prepared.launch.sha(path);return r
 for module,version in ((prepared,2256),(ready,2276)):
  for case,(fighter,side,capture,positive)in module.CASES.items():
   proof=accept(ROOT/positive/'report.json');actual=accept(ROOT/f'audit_v{version}_current_{case}_boss_ledger_checked/report.json')
   rows=module.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
   module.check(rows,17 if fighter=='kano'else 18,side)
   fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
   plans=[r for r in rows if r['tag']=='BOSS_PLAN'];assignments=[r for r in rows if r['tag']=='BOSS_ACTION'and r['after']==0x107]
   combat=[r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before']]
   groups=defaultdict(lambda:dict(plans=0,native107=0,ownedHitPlans=0,ownedDamage=0,interruptedHPPlans=0))
   windows=[];mapped=set();lead=6 if module is prepared else 0
   for i,p in enumerate(plans):
    start=p['frame'];hp=start+lead;stop=min(start+36,plans[i+1]['frame']if i+1<len(plans)else start+36)
    native=[r for r in assignments if start<=r['frame']<stop and r['actor']==p['human_actor']and r['main']==p['human_main']]
    for r in native:need(r['event']not in mapped,'Actual107uniquely mapped');mapped.add(r['event'])
    f=fields.get(hp)
    damage=[r for r in combat if r['slot']==3-side and start<=r['frame']<stop and r['a8']==p['human_actor']and r['a13']==p['human_main']and r['frame']in fields and fields[r['frame']]['human_action']==0x107]
    incoming=[r for r in combat if r['slot']==side and hp<=r['frame']<hp+3]
    height=f['cpu_height']if f else None
    bucket='missing'if height is None else'ground'if height<=0 else'1_80'if height<=80 else'81_160'if height<=160 else'161_240'if height<=240 else'241_plus'
    key=f"cpu_{f['cpu_action']:04X}_{bucket}"if f else'missing_HP_field'
    g=groups[key];g['plans']+=1;g['native107']+=len(native);g['ownedHitPlans']+=bool(damage)
    g['ownedDamage']+=sum(r['before']-r['after']for r in damage);g['interruptedHPPlans']+=bool(incoming)
    windows.append(dict(start=start,requestedHPFrame=hp,firstHPCPUHeight=height,firstHPCPUAction=f['cpu_action']if f else None,
     actual107Frames=[r['frame']for r in native],ownedDamage=sum(r['before']-r['after']for r in damage),incomingHPWindowDamage=sum(r['before']-r['after']for r in incoming)))
   need(len(mapped)==len(assignments)==proof['actualNativeUppercutAssignments']==actual['originalHuman107Assignments'],'Every actual human107mapped, never an input intention')
   cases[case]=dict(groups=dict(groups),windows=windows,actualHuman107Assignments=len(assignments),unmappedNative107Frames=[])
 pins[str(Path(__file__).resolve())]=prepared.launch.sha(__file__);prepared.launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable height-window evidence')
 result=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v['groups']for k,v in result['cases'].items()},indent=2),flush=True)
