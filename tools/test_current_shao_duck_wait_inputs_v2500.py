"""Complete independent campaign checks under specific input/plan corruptions.
Legacy simultaneous Down/Up is verified as sent, not accepted as a jump.
New holds must omit conflicting Down and retain every required Up field.
No captured record, source, health, AI or guest state is modified.
"""
import argparse,json,re
from pathlib import Path
import verify_current_stomp_window_boss_ledger_v2288 as old
import verify_current_shao_duck_wait_boss_ledger_v2499 as held
CASES={k:(held,v)for k,v in held.CASES.items()}

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
 input_error='Every actual boss-only crouch-wait/opening/descending-stomp/guard input'
 plan_error='Only actual measured stomp/Shao crouching counter or declared physical forward jumpkick plan'
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
 # Require actual flight-phase fixtures, not merely an Up plan or airborne hurt.
 input_at={}
 for row in rows:
  if row['tag']=='INPUT'and row['frame']in fields:input_at.setdefault(row['frame'],set()).add(row['button'])
 rising=next(at for at,f in fields.items()if f['height']>8 and f['human_action']==0x308 and f['human_vy']>=0x80000000 and at%6<3 and input_at.get(at,set())<=set(('Left','Right')))
 rising_line=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD ')and frame(l)==rising)
 mutations += [('premature_rising_air_kick',rising_line,'inject_hk',input_error),
  ('missing_due_late_air_kick',input_line('High_Kick'),'delete',input_error)]
 if proof['bossPolicy']=='late_descend':
  apex=next(at for at,f in fields.items()if f['height']>8 and f['human_action']==0x308 and 0<=f['human_vy']<0x20000 and at%6<3 and input_at.get(at,set())<=set(('Left','Right')))
  apex_line=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD ')and frame(l)==apex)
  mutations += [('apex_kick_before_descend_threshold',apex_line,'inject_hk',input_error)]
 # Seven non-vacuous Shao-only policy counterexamples, not Kintaro substitutes.
 shao_plan=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_PLAN ')and 'move=shao_opening_uppercut_attempt'in l)
 shao_frame=frame(lines[shao_plan]);shao_hp=input_line('High_Punch',shao_frame)
 shao_down=input_line('Down',shao_frame);shao_previous=input_line('Down',shao_frame-1)
 shao_hold=input_line('Down',shao_frame+5)
 shao_guard=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_INPUT ')and ' button=Block 'in l and frame(l)in fields and fields[frame(l)]['stage']==16)
 shao_field=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD ')and frame(l)==shao_frame)
 mutations += [('missing_actual_Shao_HP',shao_hp,'delete',input_error),
  ('undeclared_Shao_jump',shao_down,'replace_up',input_error),
  ('premature_Shao_HP',shao_previous,'inject_hp',input_error),
  ('late_held_Shao_HP',shao_hold,'inject_hp',input_error),
  ('wrong_Shao_plan',shao_plan,'plan',plan_error),
  ('HP_during_Shao_guard',shao_guard,'extra_hp',input_error),
  ('wrong_Shao_native_ID',shao_field,'shao_id','Actual native boss/human field IDs'),
  ('Shao_HP_without_visible_opening',shao_field,'shao_pose',input_error),
  ('Shao_HP_with_actual_busy_body',shao_field,'shao_body',input_error)]
 # Non-vacuous current Shao crouch-wait fixtures, not absent escape plans.
 wait_frame=next(at for at,f in fields.items()if f['stage']==16 and f['height']==0 and f['human_action']==0x302 and input_at.get(at)=={'Down'}and
  not(not f['cpu_body']&0x0c and f['cpu_height']<20 and ((f['cpu_pose']in(0xff9a37e0,0xff9a3880,0xff9a3920)and f['gap']<125)or(f['cpu_pose']==0xff99f600 and f['gap']<95))))
 wait_down=input_line('Down',wait_frame)
 mutations += [('missing_actual_Shao_wait_Down',wait_down,'delete',input_error),
  ('undeclared_Shao_wait_Up',wait_down,'replace_up',input_error),
  ('undeclared_Shao_wait_forward',wait_down,'extra_forward',input_error),
  ('HP_without_actual_Shao_wait_opening',wait_down,'inject_hp',input_error)]
 outcomes=[]
 for name,index,kind,message in mutations:
  changed=list(lines)
  if kind=='inject_hk':
   at=frame(changed[index]);template=lines[hp]
   injected=re.sub(r' frame=\d+',lambda m:' frame='+str(at),template,count=1).replace('button=High_Punch','button=High_Kick')
   actual_selection=max(r['number']for r in rows if r['tag']=='SELECT'and r['frame']<=at)
   injected=re.sub(r' selection=\d+',lambda m:' selection='+str(actual_selection),injected,count=1)
   changed.insert(index,injected)
  elif kind=='reverse_direction_button':changed[index]=re.sub(r' button=(Left|Right)',lambda m:' button='+('Left'if m[1]=='Right'else'Right'),changed[index],count=1)
  elif kind=='extra_forward':
   at=frame(changed[index]);f=fields[at];key='Right'if f['h_x']<f['c_x']else'Left';changed.insert(index,changed[index].replace('button=Down','button='+key))
  elif kind=='replace_up':changed[index]=changed[index].replace('button=Down','button=Up')
  elif kind=='inject_hp':changed.insert(index,changed[index].replace('button=Down','button=High_Punch'))
  elif kind=='shao_id':changed[index]=changed[index].replace('cpu_id=13','cpu_id=12')
  elif kind=='shao_pose':changed[index]=re.sub(r' cpu_pose=[0-9A-F]+',' cpu_pose=FF99F020',changed[index],count=1)
  elif kind=='shao_body':changed[index]=re.sub(r' cpu_body=([0-9A-F]+)',lambda m:' cpu_body='+f'{int(m[1],16)|4:04X}',changed[index],count=1)
  elif kind=='delete':changed.pop(index)
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
