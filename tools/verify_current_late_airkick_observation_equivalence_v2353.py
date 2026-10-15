"""Exact observer-only recapture: all native chronology unchanged, no ledger waiver."""
import argparse,copy,json
from pathlib import Path
import verify_current_late_airkick_observed_boss_ledger_v2349 as ledger
ROOT=ledger.ROOT;launch=ledger.launch

def need(ok,message):
 if not ok:raise ValueError(message)

def chronology(text):
 return [line for line in text.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and not line.startswith('MK2_NAT_CAMPAIGN_BOSS_ACTION ')]

def action_equivalence(old,new,fields):
 first={}
 for f in fields.values():first.setdefault(f['human_main'],f)
 extras=[];index=0
 for r in new:
  if index<len(old)and r==old[index]:index+=1;continue
  f=fields.get(r['frame'])
  need(f is not None,'Every added observation belongs to an actual recorded native boss field')
  installed=first.get(r['main'])
  need(installed is not None and installed['human_actor']!=r['actor'],'Every added action was suppressed by the proven installation-actor filter')
  need(r['main']==f['human_main']and r['actor']==r['owner']==f['human_actor'],'Added action belongs to actual current physical actor/Main')
  extras.append(r)
 need(index==len(old),'All original native action observations retained exactly in order')
 return extras

def verify():
 pins={};cases={}
 def accept(path):
  result=json.loads(path.read_text());need(result['passed']and not result['fullPortAcceptance'],'Accepted exact current proof '+str(path))
  for file,wanted in result['inputHashes'].items():
   if file not in pins:need(launch.sha(file)==wanted,'Unchanged graph '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent dependency '+file)
  pins[str(path)]=launch.sha(path);return result
 diagnostic=accept(ROOT/'audit_v2343_current_late_airkick_action_tap_diagnostic/report.json')
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof=accept(ROOT/positive/'report.json')
  book=accept(ROOT/f'audit_v2350_current_{case}_boss_ledger_checked/report.json')
  accept(ROOT/f"audit_v2336_current_{fighter}_p1_{case.split('_',1)[1]}_checked/report.json")
  old_folder=ROOT/f"audit_v2335_current_{fighter}_p1_{case.split('_',1)[1]}_campaign"
  old_text=(old_folder/'run.log').read_text(encoding='utf-8-sig')
  new_text=(ROOT/capture/'run.log').read_text(encoding='utf-8-sig')
  before=chronology(old_text);after=chronology(new_text)
  need(before==after,'Every native non-action chronology row byte-exact, without normalization or exclusions beyond repaired action observations')
  old_rows=ledger.native.parse(old_text,side,fighter);new_rows=ledger.native.parse(new_text,side,fighter)
  old_actions=[{k:v for k,v in r.items()if k!='event'}for r in old_rows if r['tag']=='BOSS_ACTION']
  new_actions=[{k:v for k,v in r.items()if k!='event'}for r in new_rows if r['tag']=='BOSS_ACTION']
  fields={r['frame']:r for r in new_rows if r['tag']=='BOSS_FIELD'}
  extras=action_equivalence(old_actions,new_actions,fields)
  ledger.check(new_rows,17 if fighter=='kano'else 18,side)
  need(bool(extras)==bool(diagnostic['cases'][case]['missingAdjacentActionObservations']),'Exact preservation of passing control and completion of diagnosed suppressed-action cases')
  tests=[]
  altered=list(after);altered[0]+=' changed=1'
  try:need(before==altered,'Every native non-action chronology row byte-exact')
  except ValueError as error:need('non-action chronology'in str(error),'Specific full native chronology rejection');tests.append('changed_native_chronology')
  missing=list(new_actions)
  retained=next(i for i,r in enumerate(missing)if r==old_actions[0]);missing.pop(retained)
  try:action_equivalence(old_actions,missing,fields)
  except ValueError as error:need('original native action observations'in str(error)or 'installation-actor filter'in str(error),'Specific dropped original action rejection');tests.append('dropped_original_action')
  else:raise ValueError('Dropped original action accepted')
  injected=copy.deepcopy(new_actions);fake=copy.deepcopy(old_actions[0]);fake['after']+=1;injected.insert(0,fake)
  try:action_equivalence(old_actions,injected,fields)
  except ValueError as error:need('installation-actor filter'in str(error),'Specific irrelevant extra action rejection');tests.append('fabricated_unsuppressed_action')
  else:raise ValueError('Fabricated unsuppressed action accepted')
  need(before==after,'Final unmodified whole native chronology')
  action_equivalence(old_actions,new_actions,fields)
  cases[case]=dict(exactNativeNonActionRows=len(before),originalActionObservations=len(old_actions),
   completeCurrentActionObservations=len(new_actions),addedPreviouslySuppressedActions=len(extras),
   diagnosedMissingAdjacentPairs=diagnostic['cases'][case]['missingAdjacentActionObservations'],
   everyOriginalActionRetainedInOrder=True,allAddedActionsHaveProvenStaleBinding=True,
   strictOrderedActionHealthLedgerPassed=book['passed'],specificCounterexamples=tests)
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,
  nativeRowsNormalized=False,originalLedgerGateWaived=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 need(not args.output.exists(),'Immutable full native chronology equivalence proof')
 result=verify();args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result['cases'],indent=2),flush=True)
