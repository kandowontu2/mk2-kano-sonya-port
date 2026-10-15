"""Specific real physical guard/attack input corruptions; full unmodified control.
Every counterexample reruns the complete independent campaign verifier in
memory, including true selection, native progress, source and health/win gates.
No on-disk capture or frozen input is changed. Full-port acceptance stays false.
"""
import argparse,json,re
from pathlib import Path
import verify_current_boss_guard_edge_ledger_v2227 as guarded
import verify_current_interrupt_v1870 as launch
import verify_current_boss_guard_edge_extended_v2232 as extended
CASES={k:(guarded,v)for k,v in guarded.CASES.items()}

def need(ok,message):
 if not ok:raise ValueError(message)

def verify(case):
 module,(fighter,side,capture,positive)=CASES[case];verifier=extended if case=='kano_guard_edge16'else module.native
 folder=module.ROOT/capture;path=module.ROOT/positive/'report.json';proof=json.loads(path.read_text())
 need(proof['passed']and proof['bounded_campaign_evidence_proven'],'Full actual current campaign accepted first')
 pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():need(launch.sha(file)==wanted,'Changed accepted actual source graph '+file)
 pins[str(path)]=launch.sha(path)
 text=(folder/'run.log').read_text(encoding='utf-8-sig');rows=verifier.parse(text,side,fighter)
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
 lines=text.splitlines(keepends=True)
 warm_end=min(fields)+120
 guard=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_INPUT ')and' button=Block 'in line and(int(re.search(r' frame=(\d+)',line)[1])in fields)and int(re.search(r' frame=(\d+)',line)[1])>=warm_end)
 hp=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_INPUT ')and' button=High_Punch 'in line and int(re.search(r' frame=(\d+)',line)[1])in fields)
 plan=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_BOSS_PLAN '))
 mutations=[('missing_actual_guard',guard,'delete'),('attack_during_guard',guard,'extra_hp'),('early_physical_hp',hp,'early'),('wrong_physical_plan',plan,'plan')]
 outcomes=[]
 for name,index,kind in mutations:
  changed=list(lines)
  if kind=='delete':changed.pop(index)
  elif kind=='extra_hp':changed.insert(index,changed[index].replace('button=Block','button=High_Punch'))
  elif kind=='early':changed[index]=re.sub(r' frame=(\d+)',lambda m:' frame='+str(int(m[1])-1),changed[index],count=1)
  else:changed[index]=changed[index].replace('move=guard_release_edge_uppercut_attempt','move=unproven_attack')
  result=verifier.verify(folder,text_override=''.join(changed))
  message='Only fresh HP-edge guarded uppercut plan'if kind=='plan'else 'Every actual physical guard/release/'
  need(not result['passed']and any(message in e for e in result['errors']),'Intended physical-input invariant rejects '+name)
  outcomes.append(dict(name=name,errors=result['errors']))
 control=verifier.verify(folder)
 need(control['passed']and control['actualNativeUppercutAssignments']==proof['actualNativeUppercutAssignments']and control['actualBossRoundWins']==proof['actualBossRoundWins'],'Final unmodified full actual campaign control passes')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,case=case,rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes,
  finalUnmodifiedFullCampaignControlPassed=True,inputHashes=pins,captureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',choices=CASES);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 need(not args.output.exists(),'Immutable counterexample report')
 result=verify(args.case);args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in('inputHashes','outcomes')},indent=2),flush=True)
