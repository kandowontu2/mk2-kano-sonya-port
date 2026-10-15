"""Read-only diagnosis of missing action observations; never waive a ledger gate."""
import argparse,json
from collections import defaultdict
from pathlib import Path
import verify_current_late_airkick_boss_ledger_v2337 as ledger
ROOT=ledger.ROOT;launch=ledger.launch

def need(ok,message):
 if not ok:raise ValueError(message)

def verify():
 pins={};cases={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  path=ROOT/positive/'report.json';proof=json.loads(path.read_text())
  need(proof['passed']and proof['bounded_campaign_evidence_proven'],'Accepted entire current true-ID/progression control')
  for file,wanted in proof['inputHashes'].items():
   if file not in pins:need(launch.sha(file)==wanted,'Unchanged actual input/capture '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent actual input graph')
  pins[str(path)]=launch.sha(path)
  path=ROOT/f'audit_v2338_current_{case}_boss_ledger_checked/report.json';book=json.loads(path.read_text());pins[str(path)]=launch.sha(path)
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'};actions=defaultdict(list);first={}
  for f in fields.values():first.setdefault(f['human_main'],f)
  for r in rows:
   if r['tag']=='BOSS_ACTION':actions[r['frame']].append(r)
  missing=[]
  for frame,a in fields.items():
   b=fields.get(frame+1)
   if not b or any(a[k]!=b[k]for k in('human_actor','human_main','cpu_actor','cpu_main','stage')):continue
   stores=actions[frame]
   coherent=(stores[0]['before']==a['human_action']and stores[-1]['after']==b['human_action']and all(x['after']==y['before']for x,y in zip(stores,stores[1:])))if stores else a['human_action']==b['human_action']
   if coherent:continue
   original=first[a['human_main']]
   need(not stores and original['human_actor']!=a['human_actor'],'Every missing adjacent action observation is explained by the exact stale captured actor filter, not an unknown game change')
   missing.append(dict(frame=frame,stage=a['stage'],main=a['human_main'],actualActor=a['human_actor'],installedActor=original['human_actor'],
    firstInstallationField=original['frame'],before=a['human_action'],after=b['human_action']))
  if missing:need(not book['passed']and 'Action stores explain actual adjacent native fields'in book['error'],'Preserve original strict ledger failure')
  else:need(book['passed'],'Untouched complete passing observer control remains passing')
  cases[case]=dict(missingAdjacentActionObservations=len(missing),missingObservations=missing,
   recycledMainAddresses=sorted({r['main']for r in missing}),originalLedgerPassed=book['passed'])
 source=ROOT/'mk2ks_natural_campaign_boss_late_airkick_v2332.lua';text=source.read_text()
 need('local observed_main,observed_actor=human.main,human.actor'in text and
  'p:read_u32(slots[side].actor)~=observed_actor'in text and
  'if not boss_action_taps[human.main] then'in text,'Actual observer caches only Main address and filters against installation-time actor')
 pins[str(source)]=launch.sha(source);pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,readOnlyObserverDiagnosis=True,
  gameOrCaptureModified=False,originalLedgerGateWaived=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 need(not args.output.exists(),'Immutable missing-observation diagnostic')
 result=verify();args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({case:{key:r[key]for key in('missingAdjacentActionObservations','recycledMainAddresses','originalLedgerPassed')}for case,r in result['cases'].items()},indent=2),flush=True)
