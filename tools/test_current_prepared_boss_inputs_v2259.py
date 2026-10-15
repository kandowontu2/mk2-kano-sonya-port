"""Targeted physical preparation/cancellation/handler corruptions.
Entire current campaign verification rerun in memory; no actual capture edits.
All native selection/guest/health/win/ending gates kept, including final control.
"""
import argparse,json,re
from pathlib import Path
import verify_current_prepared_boss_ledger_v2255 as ledger
native=ledger.native

def need(ok,message):
 if not ok:raise ValueError(message)

def verify(case):
 fighter,side,capture,positive=ledger.CASES[case];folder=ledger.ROOT/capture
 path=ledger.ROOT/positive/'report.json';proof=json.loads(path.read_text())
 need(proof['passed']and proof['bounded_campaign_evidence_proven'],'Full actual current campaign accepted first')
 pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():need(ledger.launch.sha(file)==wanted,'Unchanged accepted graph '+file)
 pins[str(path)]=ledger.launch.sha(path)
 text=(folder/'run.log').read_text(encoding='utf-8-sig');rows=native.parse(text,side,fighter)
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'};lines=text.splitlines(keepends=True)
 def frame(line):return int(re.search(r' frame=(\d+)',line)[1])
 guard=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_INPUT ')and' button=Block 'in l and frame(l)in fields)
 hp=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_INPUT ')and' button=High_Punch 'in l and frame(l)in fields)
 plan=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_PLAN '))
 cancel=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_CANCEL '))
 handler=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_HANDLER '))
 input_error='Every actual prepared Down/HP/guard input'
 handler_error='Actual native boss handler instruction/true own actor/Main/register provenance'
 mutations=[('missing_guard',guard,'delete',input_error),('hp_during_guard',guard,'extra_hp',input_error),
  ('early_hp_edge',hp,'early',input_error),('false_plan_label',plan,'plan','Only prepared native crouch uppercut plan'),
  ('missing_cancel',cancel,'delete','Every physical cancellation follows actual nonstance'),
  ('wrong_cancel_start',cancel,'cancel_start','Actual physical cancellation provenance'),
  ('wrong_handler_pc',handler,'handler_pc',handler_error),('wrong_handler_owner',handler,'handler_owner',handler_error)]
 outcomes=[]
 for name,index,kind,message in mutations:
  changed=list(lines)
  if kind=='delete':changed.pop(index)
  elif kind=='extra_hp':changed.insert(index,changed[index].replace('button=Block','button=High_Punch'))
  elif kind=='early':changed[index]=re.sub(r' frame=(\d+)',lambda m:' frame='+str(int(m[1])-1),changed[index],count=1)
  elif kind=='plan':changed[index]=changed[index].replace('move=prepared_crouch_uppercut_attempt','move=unproven_attack')
  elif kind=='cancel_start':changed[index]=re.sub(r' start=(\d+)',lambda m:' start='+str(int(m[1])+1),changed[index],count=1)
  elif kind=='handler_pc':changed[index]=re.sub(r' pc=([0-9A-F]+)',lambda m:' pc='+f'{int(m[1],16)+16:08X}',changed[index],count=1)
  elif kind=='handler_owner':changed[index]=re.sub(r' owner=([0-9A-F]+)',lambda m:' owner='+f'{int(m[1],16)+16:08X}',changed[index],count=1)
  result=native.verify(folder,text_override=''.join(changed))
  need(not result['passed']and any(message in e for e in result['errors']),'Intended specific invariant rejects '+name+' '+str(result['errors']))
  outcomes.append(dict(name=name,errors=result['errors']))
 control=native.verify(folder)
 need(control['passed']and control['actualNativeUppercutAssignments']==proof['actualNativeUppercutAssignments']and control['actualBossRoundWins']==proof['actualBossRoundWins'],'Final unmodified whole campaign control passes')
 pins[str(Path(__file__).resolve())]=ledger.launch.sha(__file__);ledger.launch.module_pins(pins)
 return dict(passed=True,case=case,rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes,
  finalUnmodifiedFullCampaignControlPassed=True,inputHashes=pins,captureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',choices=ledger.CASES);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable counterexample proof')
 result=verify(a.case);a.output.mkdir();(a.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in('inputHashes','outcomes')},indent=2),flush=True)
