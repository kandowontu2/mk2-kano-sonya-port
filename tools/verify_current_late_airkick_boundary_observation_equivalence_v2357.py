"""Exact observer-only recapture: all native chronology unchanged, no ledger waiver."""
import argparse,copy,json,struct
from pathlib import Path
import verify_current_late_airkick_observed_boss_ledger_v2349 as ledger
ROOT=ledger.ROOT;launch=ledger.launch

def need(ok,message):
 if not ok:raise ValueError(message)

def chronology(text):
 return [line for line in text.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and not line.startswith('MK2_NAT_CAMPAIGN_BOSS_ACTION ')]

def action_equivalence(old,new,fields,states,identity):
 first={}
 for f in fields.values():first.setdefault(f['human_main'],f)
 extras=[];index=0
 for r in new:
  if index<len(old)and r==old[index]:index+=1;continue
  installed=first.get(r['main'])
  need(installed is not None and installed['human_actor']!=r['actor'],'Every added action was suppressed by the proven installation-actor filter')
  need(r['id']==r['roster']==identity and r['state']==1 and r['actor']==r['owner']and
   r['at']==r['main']+0x1f0 and r['mask']==65535 and
   all(0x01000000<=r[k]<0x01100000 for k in('actor','main'))and
   all(0<int(h)<=161 for h in r['health'].split(',')),'Every added native own action has complete actual actor/Main/ID/health provenance')
  f=fields.get(r['frame'])
  if f is not None:
   need(r['main']==f['human_main']and r['actor']==f['human_actor'],'Added action belongs to actual current physical actor/Main')
  else:
   # The real tap covers native Main construction and round refill too.
   # Do not drop those records or call them successful combat activations.
   context=max((s for s in states if s['frame']<=r['frame']),key=lambda s:s['frame'])
   clear=(context['mode']==6 and r['pc']==0xff83a100 and r['a1']==0 and
    r['after']in(r['before']&0xff00,r['before']&0x00ff))
   refill=(context['mode']==7 and r['pc']==0xff9065d0 and r['before']in(0,0x303)and r['after']==0x303 and
    r['a8']==r['actor']and r['a13']==r['main'])
   need(r['stage']==context['stage']==16 and context['states']=='1,0'and context['roster']==f'{identity},13'and
    (clear or refill),'Native between-round construction/refill action provenance')
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
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 guest=ledger.native.current_source.expected()[0]
 for at,words in((0xff83a0f0,(0x8c20,0x1100)),(0xff906590,(0x09c0,0x0303,0xb00d,0x01f0))):
  offset=(at-0xff800000)//8;expected=struct.pack('<'+'H'*len(words),*words)
  need(guest[offset:offset+len(expected)]==original[offset:offset+len(expected)]==expected,'Original unchanged native byte-clear/action303 instructions account for exact between-round stores')
 pins[str(ROOT/'mk2/mk2-maincpu.bin')]=launch.sha(ROOT/'mk2/mk2-maincpu.bin')
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
  states=[r for r in new_rows if r['tag']=='STATE'];identity=17 if fighter=='kano'else 18
  extras=action_equivalence(old_actions,new_actions,fields,states,identity)
  ledger.check(new_rows,17 if fighter=='kano'else 18,side)
  need(bool(extras)==bool(diagnostic['cases'][case]['missingAdjacentActionObservations']),'Exact preservation of passing control and completion of diagnosed suppressed-action cases')
  tests=[]
  altered=list(after);altered[0]+=' changed=1'
  try:need(before==altered,'Every native non-action chronology row byte-exact')
  except ValueError as error:need('non-action chronology'in str(error),'Specific full native chronology rejection');tests.append('changed_native_chronology')
  missing=list(new_actions)
  retained=next(i for i,r in enumerate(missing)if r==old_actions[0]);missing.pop(retained)
  try:action_equivalence(old_actions,missing,fields,states,identity)
  except ValueError as error:need('original native action observations'in str(error)or 'installation-actor filter'in str(error),'Specific dropped original action rejection');tests.append('dropped_original_action')
  else:raise ValueError('Dropped original action accepted')
  injected=copy.deepcopy(new_actions);fake=copy.deepcopy(old_actions[0]);fake['after']+=1;injected.insert(0,fake)
  try:action_equivalence(old_actions,injected,fields,states,identity)
  except ValueError as error:need('installation-actor filter'in str(error),'Specific irrelevant extra action rejection');tests.append('fabricated_unsuppressed_action')
  else:raise ValueError('Fabricated unsuppressed action accepted')
  outside=[r for r in extras if r['frame']not in fields]
  if outside:
   target=outside[0];target_index=next(i for i,r in enumerate(new_actions)if r==target)
   bad=copy.deepcopy(new_actions);bad[target_index]['pc']+=16
   try:action_equivalence(old_actions,bad,fields,states,identity)
   except ValueError as error:need('Native between-round construction/refill action provenance'in str(error),'Specific native boundary instruction rejection');tests.append('wrong_native_boundary_instruction')
   else:raise ValueError('Wrong native boundary instruction accepted')
   context=max((r for r in states if r['frame']<=target['frame']),key=lambda r:r['frame'])
   bad_states=copy.deepcopy(states);bad_states[states.index(context)]['mode']=2
   try:action_equivalence(old_actions,new_actions,fields,bad_states,identity)
   except ValueError as error:need('Native between-round construction/refill action provenance'in str(error),'Specific boundary mode rejection');tests.append('misclassified_boundary_as_combat')
   else:raise ValueError('Boundary action classified as combat accepted')
  need(before==after,'Final unmodified whole native chronology')
  action_equivalence(old_actions,new_actions,fields,states,identity)
  cases[case]=dict(nativeBetweenRoundAddedObservations=len(outside),boundaryRecordsNotCreditedAsCombatMoves=True,
   exactNativeNonActionRows=len(before),originalActionObservations=len(old_actions),
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
