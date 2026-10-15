"""Actual guard/stance at each physical plan and its native107 activation window.
Only immutable independently accepted native ledgers are controls. Unmapped
assignments remain explicit; plans are never promoted to successful attacks.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
import verify_current_boss_guard_edge_ledger_v2227 as ledger
ROOT=ledger.ROOT

def need(ok,message):
 if not ok:raise ValueError(message)

def verify():
 pins={};cases={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  path=ROOT/f'audit_v2235_current_{case}_boss_ledger_checked/report.json';accepted=json.loads(path.read_text())
  need(accepted['passed']and accepted['finalUnmodifiedControlPassed'],'Actual complete native ledger control')
  for file,wanted in accepted['inputHashes'].items():
   if file in pins:need(pins[file]==wanted,'Consistent native source graph')
   else:need(ledger.launch.sha(file)==wanted,'Changed actual accepted source/capture '+file)
   pins[file]=wanted
  pins[str(path)]=ledger.launch.sha(path)
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  ledger.check(rows,17 if fighter=='kano'else 18,side)
  plans=[r for r in rows if r['tag']=='BOSS_PLAN'];actions=[r for r in rows if r['tag']=='BOSS_ACTION'and r['after']==0x107]
  groups=defaultdict(lambda:dict(physicalPlans=0,plansWithActual107=0,actual107Assignments=0));bound=set();windows=[]
  for plan in plans:
   matches=[a for a in actions if plan['frame']<=a['frame']<plan['frame']+36 and a['actor']==plan['human_actor']and a['main']==plan['human_main']]
   g=groups[f"own_action_{plan['human_action']:04X}"];g['physicalPlans']+=1;g['plansWithActual107']+=bool(matches);g['actual107Assignments']+=len(matches)
   for a in matches:need(a['event']not in bound,'Native107belongs at most one actual physical command');bound.add(a['event'])
   windows.append(dict(frame=plan['frame'],ownAction=plan['human_action'],cpuAction=plan['cpu_action'],cpuHeight=plan['cpu_height'],native107Frames=[a['frame']for a in matches]))
  need(len(actions)==accepted['originalHuman107Assignments'],'Every real native107 assignment inventoried')
  cases[case]=dict(groups=dict(groups),actual107Assignments=len(actions),unmappedNative107Frames=[a['frame']for a in actions if a['event']not in bound],windows=windows)
 pins[str(Path(__file__).resolve())]=ledger.launch.sha(__file__);ledger.launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 need(not args.output.exists(),'Immutable native phase analysis')
 result=verify();args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({case:{k:v for k,v in r.items()if k!='windows'}for case,r in result['cases'].items()},indent=2),flush=True)
