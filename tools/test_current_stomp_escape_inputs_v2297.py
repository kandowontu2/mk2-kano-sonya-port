"""Complete independent campaign checks under specific input/plan corruptions.
Legacy simultaneous Down/Up is verified as sent, not accepted as a jump.
New holds must omit conflicting Down and retain every required Up field.
No captured record, source, health, AI or guest state is modified.
"""
import argparse,json,re
from pathlib import Path
import verify_current_stomp_window_boss_ledger_v2288 as old
import verify_current_escape_hold_boss_ledger_v2298 as held
CASES={**{k:(old,v)for k,v in old.CASES.items()},**{k:(held,v)for k,v in held.CASES.items()}}

def need(ok,message):
 if not ok:raise ValueError(message)

def verify(case):
 module,(fighter,side,capture,positive)=CASES[case];native=module.native
 folder=module.ROOT/capture;path=module.ROOT/positive/'report.json';proof=json.loads(path.read_text())
 need(proof['passed']and proof['bounded_campaign_evidence_proven'],'Independent actual full campaign accepted')
 pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():need(module.launch.sha(file)==wanted,'Unchanged accepted source/capture '+file)
 pins[str(path)]=module.launch.sha(path)
 text=(folder/'run.log').read_text(encoding='utf-8-sig');rows=native.parse(text,side,fighter)
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'};lines=text.splitlines(keepends=True)
 def frame(line):return int(re.search(r' frame=(\d+)',line)[1])
 def input_line(button,at=None):
  return next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_INPUT ')and(' button='+button+' ')in l and frame(l)in fields and(at is None or frame(l)==at))
 guard=input_line('Block');hp=input_line('High_Punch')
 plan=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_PLAN '))
 cancel=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_CANCEL '))
 handler=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_HANDLER '))
 input_error='Every actual stomp-window crouch/HP/jumpkick/guard input'
 plan_error='Only actual measured stomp counter or declared physical forward jumpkick plan'
 handler_error='Actual native boss handler instruction/true own actor/Main/register provenance'
 mutations=[('missing_actual_guard',guard,'delete',input_error),('hp_during_guard',guard,'extra_hp',input_error),
  ('early_hp_edge',hp,'early',input_error),('wrong_plan_label',plan,'plan',plan_error),
  ('missing_native_cancel',cancel,'delete','Every physical cancellation follows actual nonstance'),
  ('wrong_cancel_start',cancel,'cancel_start','Actual physical cancellation provenance'),
  ('wrong_handler_pc',handler,'handler_pc',handler_error),('wrong_handler_owner',handler,'handler_owner',handler_error)]
 jumps=[i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_PLAN ')and'move=close_pressure_jumpkick_attempt'in l]
 if jumps:
  jump=jumps[0];at=frame(lines[jump]);up=input_line('Up',at)
  mutations += [('wrong_jump_direction',jump,'direction',plan_error),('missing_jump_up',up,'delete',input_error)]
  if module is old:mutations +=[('missing_legacy_simultaneous_down',input_line('Down',at),'delete',input_error)]
  else:
   mutations +=[('conflicting_down_on_new_jump',up,'extra_down',input_error)]
   long=next(j for j in jumps if frame(lines[j])+10 in fields)
   mutations +=[('truncated_native_stand_jump_hold',input_line('Up',frame(lines[long])+10),'delete',input_error)]
 outcomes=[]
 for name,index,kind,message in mutations:
  changed=list(lines)
  if kind=='delete':changed.pop(index)
  elif kind=='extra_hp':changed.insert(index,changed[index].replace('button=Block','button=High_Punch'))
  elif kind=='extra_down':changed.insert(index,changed[index].replace('button=Up','button=Down'))
  elif kind=='early':changed[index]=re.sub(r' frame=(\d+)',lambda m:' frame='+str(int(m[1])-1),changed[index],count=1)
  elif kind=='plan':changed[index]=re.sub(r' move=\S+',' move=unproven_attack',changed[index],count=1)
  elif kind=='direction':changed[index]=re.sub(r' direction=(Right|Left)',lambda m:' direction='+('Left'if m[1]=='Right'else'Right'),changed[index],count=1)
  elif kind=='cancel_start':changed[index]=re.sub(r' start=(\d+)',lambda m:' start='+str(int(m[1])+1),changed[index],count=1)
  elif kind=='handler_pc':changed[index]=re.sub(r' pc=([0-9A-F]+)',lambda m:' pc='+f'{int(m[1],16)+16:08X}',changed[index],count=1)
  elif kind=='handler_owner':changed[index]=re.sub(r' owner=([0-9A-F]+)',lambda m:' owner='+f'{int(m[1],16)+16:08X}',changed[index],count=1)
  result=native.verify(folder,text_override=''.join(changed))
  need(not result['passed']and any(message in e for e in result['errors']),'Intended invariant rejects '+name+' '+str(result['errors']))
  outcomes.append(dict(name=name,errors=result['errors']))
 control=native.verify(folder)
 need(control['passed']and control['actualNativeUppercutAssignments']==proof['actualNativeUppercutAssignments']and control['actualBossRoundWins']==proof['actualBossRoundWins'],'Final untouched entire campaign control')
 pins[str(Path(__file__).resolve())]=module.launch.sha(__file__);module.launch.module_pins(pins)
 return dict(passed=True,case=case,rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes,
  finalUnmodifiedFullCampaignControlPassed=True,inputHashes=pins,captureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',choices=CASES);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable input/plan counterexample proof')
 result=verify(a.case);a.output.mkdir();(a.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in('inputHashes','outcomes')},indent=2),flush=True)
