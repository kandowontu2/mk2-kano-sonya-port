"""Actual native107 assignment-to-collision timing, not an inferred hit from an input."""
import argparse,bisect,json
from pathlib import Path
from collections import Counter,defaultdict
import verify_current_shao_duck_wait_boss_ledger_v2526 as ledger
import diagnose_current_boss_damage_action_order_v2385 as ordered
ROOT=ledger.ROOT;launch=ledger.launch
def need(ok,label):
 if not ok:raise ValueError(label)
def verify():
 pins={};cases={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof_path=ROOT/positive/'report.json';proof=json.loads(proof_path.read_text());need(proof['passed'],'Whole actual campaign accepted')
  for file,wanted in proof['inputHashes'].items():
   if file in pins:need(pins[file]==wanted,'Consistent actual graph')
   else:need(launch.sha(file)==wanted,'Unchanged actual input/capture '+file);pins[file]=wanted
  pins[str(proof_path)]=launch.sha(proof_path)
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter);ledger.check(rows,17 if fighter=='kano'else 18,side)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16}
  attacks=[r for r in rows if r['tag']=='BOSS_ACTION'and r['stage']==16 and r['after']==0x107]
  groups=defaultdict(list)
  for index,attack in enumerate(attacks):groups[attack['actor'],attack['main']].append((attack['event'],index))
  episodes=[dict(assignmentFrame=r['frame'],assignmentEvent=r['event'],humanActor=r['actor'],humanMain=r['main'],
   preInputAssignmentGap=fields[r['frame']]['gap'],preInputCPUPose=fields[r['frame']]['cpu_pose'],damageStores=[])for r in attacks]
  damage=[r for r in ordered.classify(rows,side)if r['stage']==16 and r['actualDamageWriterAction']==0x107]
  for hit in damage:
   candidates=groups[hit['humanActor'],hit['humanMain']];at=bisect.bisect_right([r[0]for r in candidates],hit['event'])-1
   need(at>=0,'Actual damage has preceding same-owner107assignment');episode=episodes[candidates[at][1]]
   need(0<=hit['frame']-episode['assignmentFrame']<=15,'Same real original attack episode')
   episode['damageStores'].append(dict(frame=hit['frame'],deltaFrom107=hit['frame']-episode['assignmentFrame'],damage=hit['damage'],
    preInputDamageGap=fields[hit['frame']]['gap'],preInputDamageCPUPose=fields[hit['frame']]['cpu_pose']))
  histogram=Counter(hit['deltaFrom107']for e in episodes for hit in e['damageStores'])
  cases[case]=dict(actual107Assignments=len(attacks),episodesWithActualOwnedDamage=sum(bool(e['damageStores'])for e in episodes),
   actualOwned107Damage=sum(r['damage']for r in damage),actualDamageTimingHistogram=dict(histogram),episodes=episodes,
   noInputPlanAssumedToHit=True,scope='Read-only native event ordering and pre-input geometry; geometry samples are not exact collision-time coordinates')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable collision timing diagnosis')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:{key:value for key,value in row.items()if key!='episodes'}for k,row in r['cases'].items()},indent=2),flush=True)
