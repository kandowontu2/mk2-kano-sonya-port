"""Exact pre-Shao native chronology and earned boss matches under physical inputs.
Native combat/ending transitions are not universal ending art/audio certification.
No guest, health, AI, stage, difficulty, RNG or captured record is modified.
"""
import argparse,json,re,copy,struct
from pathlib import Path
from collections import defaultdict
import verify_current_shao_crouch_exit_boss_ledger_v2466 as ledger
import diagnose_current_boss_damage_action_order_v2385 as ordered
from analyze_current_shao_opening_damage_states_v2408 import own_damage
ROOT=ledger.ROOT;launch=ledger.launch

def need(ok,message):
 if not ok:raise ValueError(message)

def prefix(text,until,policy):
 return [line.replace('policy='+policy,'policy=late_apex') for line in text.splitlines()
  if line.startswith('MK2_NAT_CAMPAIGN_')and int(re.search(r' frame=(\d+)',line)[1])<until]

def exact(a,b):
 need(a==b,'Entire pre-Shao native trajectory equals accepted baseline; only explicit policy labels normalized')

def earned(rows,stage,side,identity,boundary):
 losses=[r['event']for r in rows if r['tag']=='LOSS'and r['stage']==stage and r['event']<boundary['event']]
 beginnings=[r['event']for r in rows if r['tag']=='STAGE'and r['stage']==stage and r['event']<boundary['event']]
 need(beginnings,'Actual owned live native stage before match retirement')
 start=max(losses+beginnings)
 wins=[r for r in rows if r['tag']=='WIN'and r['stage']==stage and r['slot']==side and start<r['event']<boundary['event']]
 need(len(wins)==2 and all(r['id']==identity for r in wins),'Two actual owned native round wins in the same successful attempt, never accumulated lost attempts')
 return dict(stage=stage,actualOwnedWinFrames=[r['frame']for r in wins],nativeRetirementFrame=boundary['frame'])

def verify():
 pins={};cases={}
 def accept(path):
  report=json.loads(path.read_text());need(report['passed']and not report['fullPortAcceptance'],'Accepted current bounded proof '+str(path))
  for file,wanted in report['inputHashes'].items():
   if file not in pins:need(launch.sha(file)==wanted,'Unchanged actual graph '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent actual graph '+file)
  pins[str(path)]=launch.sha(path);return report
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();guest=ledger.native.current_source.expected()[0]
 for at,words in((0xff870e70,(0x09c0,1)),(0xff870e90,(0x0d5f,0xdcc0,0xff80)),(0xff870ef0,(0x09c0,1)),(0xff870f10,(0x0d5f,0xdcc0,0xff80)),(0xff870f50,(0x09c1,0x0107))):
  offset=(at-0xff800000)//8;expected=struct.pack('<'+'H'*len(words),*words)
  need(guest[offset:offset+len(expected)]==original[offset:offset+len(expected)]==expected,'Unchanged original human uppercut two one-tick startup sleeps and native107 dispatch')
 pins[str(ROOT/'mk2/mk2-maincpu.bin')]=launch.sha(ROOT/'mk2/mk2-maincpu.bin')
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  identity=17 if fighter=='kano'else 18
  proof=accept(ROOT/positive/'report.json')
  book=accept(ROOT/f'audit_v2467_current_{case}_boss_ledger_checked/report.json')
  negative=accept(ROOT/f'audit_v2469_current_{case}_input_counterexamples/report.json')
  need(negative['rejectedSpecificCounterexamples']==34,'All29complete prior physical controls plus5actual301/native-entry-specific corruptions')
  baseline_path=ROOT/f'audit_v2348_current_{fighter}_p1_late_apex_checked/report.json';accept(baseline_path)
  old_text=(ROOT/f'audit_v2347_current_{fighter}_p1_late_apex_campaign/run.log').read_text(encoding='utf-8-sig')
  text=(ROOT/capture/'run.log').read_text(encoding='utf-8-sig')
  rows=ledger.native.parse(text,side,fighter);ledger.check(rows,identity,side)
  first_shao=next(r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16)
  before=prefix(old_text,first_shao['frame'],'late_apex');after=prefix(text,first_shao['frame'],proof['bossPolicy']);exact(before,after)
  index=next(i for i,line in enumerate(after)if line.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD '))
  counterexamples=[]
  for kind in ('missing_native_field','changed_identity','changed_health'):
   changed=list(after)
   if kind=='missing_native_field':changed.pop(index)
   elif kind=='changed_identity':changed[index]=changed[index].replace('human_id='+str(identity),'human_id=1',1)
   else:changed[index]=re.sub(r' health=(\d+),',lambda m:' health='+str(int(m[1])-1)+',',changed[index],count=1)
   need(changed!=after,'Non-vacuous specific actual prefix mutation')
   try:exact(before,changed)
   except ValueError as error:need('Entire pre-Shao native trajectory'in str(error),'Specific prefix invariant');counterexamples.append(kind)
   else:raise ValueError('Changed actual pre-Shao control accepted')
  exact(before,after)
  transition=next(r for r in rows if r['tag']=='STAGE'and r['stage']==16)
  kintaro=earned(rows,15,side,identity,transition)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
  actions=[r for r in rows if r['tag']=='BOSS_ACTION']
  stage16_upper=[r for r in actions if r['stage']==16 and r['after']==0x107]
  plans=[r for r in rows if r['tag']=='BOSS_PLAN'and r['stage']==16]
  need(plans and all(r['move']in('shao_opening_uppercut_attempt','shao_pressure_escape_jumpkick_attempt')for r in plans),'Only independently replayed current visible opening and physical pressure-escape plans')
  upper_plans=[r for r in plans if r['move']=='shao_opening_uppercut_attempt']
  escape_plans=[r for r in plans if r['move']=='shao_pressure_escape_jumpkick_attempt']
  exit_assignments=[r for r in actions if r['stage']==16 and r['after']==0x301]
  exit_handlers=[r for r in rows if r['tag']=='BOSS_HANDLER'and r['stage']==16 and r['entry']==0xff82fd70]
  jump_handlers=[r for r in rows if r['tag']=='BOSS_HANDLER'and r['stage']==16 and r['entry']==0xff831360]
  native_jump_assignments=[r for r in actions if r['stage']==16 and r['after']==0x308]
  for event in exit_assignments:
   need(event['before']==0x302 and event['pc']==0xff82fdb0 and event['a1']&65535==0x301 and event['a8']==event['actor']and event['a13']==event['main'],'Actual original302to301writer/ownMain/register provenance')
   paired=[h for h in exit_handlers if h['frame']==event['frame']and h['actor']==event['actor']and h['main']==event['main']]
   need(len(paired)==1 and paired[0]['action']==0x302,'Actual originalFD70entry immediately precedes original301assignment')
  for event in jump_handlers:
   paired=[a for a in native_jump_assignments if a['actor']==event['actor']and a['main']==event['main']and 0<=a['frame']-event['frame']<=2]
   need(len(paired)==1,'Actual original831360jump entry belongs to one own native308assignment, not airborne hurt')
  exit_plans=[r for r in escape_plans if r['human_action']==0x301]
  need(exit_plans,'New physical native301escape gate is non-vacuous')
  episodes=[]
  for plan in exit_plans:
   entries=[h for h in jump_handlers if h['actor']==plan['human_actor']and h['main']==plan['human_main']and 0<=h['frame']-plan['frame']<=16]
   need(len(entries)<=1,'One actual301escape plan cannot fabricate repeated independent jumps')
   sequence=[fields.get(plan['frame']+offset)for offset in range(17)]
   complete=all(f and f['stage']==16 and f['human_actor']==plan['human_actor']and f['human_main']==plan['human_main']for f in sequence)
   episodes.append(dict(planFrame=plan['frame'],actualPlanAction=0x301,actualPlanGap=plan['gap'],direction=plan['direction'],
    actualNativeJumpEntryFrame=entries[0]['frame']if entries else None,
    planToNativeJumpFields=entries[0]['frame']-plan['frame']if entries else None,
    completePositiveHealthSameActorObservation=complete,
    actualObservedNativeActions=[f['human_action']for f in sequence if f],
    scope='Measured actual physical301escape and original jump entry; no credit for plan-only or hurt'))
  for a,b in((0xff82f9f0,0xff82fe00),(0xff831360,0xff831510),(0xff83c430,0xff83c5b0)):
   need(guest[(a-0xff800000)//8:(b-0xff800000)//8]==original[(a-0xff800000)//8:(b-0xff800000)//8],'Original native crouch-exit/horizontal-jump/reverse-animation code unchanged')
  combat=[r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before']and r['frame']in fields]
  owned=[r for r in combat if r['slot']==3-side and r['a8']==fields[r['frame']]['human_actor']and r['a13']==fields[r['frame']]['human_main']]
  need(len(owned)==proof['actualBossOwnedDamageStores'],'Complete actual own damage inventory')
  need(sum(r['before']-r['after']for r in owned if fields[r['frame']]['human_action']==0x107)==book['ownBossUppercutDamage']==proof['actualBossUppercutDamage'],'Actual native107 original damage reconciliation')
  shao_owned=[r for r in owned if fields[r['frame']]['stage']==16]
  incoming=[r for r in combat if r['slot']==side and fields[r['frame']]['stage']==16]
  starts=[r for r in rows if r['tag']=='ENDING_START'];completed=[r for r in rows if r['tag']=='ENDING_COMPLETED']
  shao_match=earned(rows,16,side,identity,starts[0])if starts else None
  if starts:
   need(len(starts)==1 and starts[0]['winner']==side and starts[0]['roster']==identity,'Actual owned native ending retirement')
  if completed:
   need(starts and len(completed)==1 and completed[0]['frame']>starts[0]['frame'],'Actual own ending follows naturally earned Shao match')
  need(proof['unassisted_clear_proven']==bool(shao_match and completed),'Do not promote partial rounds or ending starts to a complete owned campaign/return path')
  groups=defaultdict(lambda:dict(stores=0,damage=0))
  for r in incoming:
   f=fields[r['frame']];group=groups[f"preInputHuman_{f['human_action']:04X}_CPU_{f['cpu_action']:04X}"]
   group['stores']+=1;group['damage']+=r['before']-r['after']
  spacing=[]
  for attack in stage16_upper:
   possible=[r for r in upper_plans if r['human_actor']==attack['actor']and r['human_main']==attack['main']and 0<=attack['frame']-r['frame']<=15]
   need(len(possible)<=1,'Measured30field attempt cooldown prevents ambiguous15field activation window')
   planned=possible[0]if possible else None;f=fields.get(attack['frame'])
   observed=[];complete=True
   for at in range(attack['frame']+1,attack['frame']+9):
    next_field=fields.get(at)
    if not f or not next_field or any(next_field[k]!=f[k]for k in ('human_actor','human_main','cpu_actor','cpu_main','stage')):complete=False;break
    observed.append(next_field['gap'])
   damage=[r for r in shao_owned if attack['frame']<=r['frame']<=attack['frame']+8 and fields[r['frame']]['human_actor']==attack['actor']and fields[r['frame']]['human_main']==attack['main']]
   spacing.append(dict(actual107Frame=attack['frame'],actualPlanFrame=planned['frame']if planned else None,
    actualPlanGap=planned['gap']if planned else None,planTo107Fields=attack['frame']-planned['frame']if planned else None,
    preInput107FieldGap=f['gap']if f else None,postEightFieldGaps=observed,completeSameNativeEpisodeWindow=complete,
    ownedDamageInWindow=sum(r['before']-r['after']for r in damage),
    scope='Measured short native field window; no assumption that every plan activates, or that an incomplete/zero-damage window proves a character defect'))
  actual_owned=[r for r in ordered.classify(rows,side)if r['stage']==16]
  actual_incoming=own_damage(rows,side)
  need(sum(r['damage']for r in actual_owned if r['actualDamageWriterAction']==0x107)==sum(r['before']-r['after']for r in shao_owned if fields[r['frame']]['human_action']==0x107),'Actual ordered native107 writer and legacy field inventory reconcile')
  need(sum(r['damage']for r in actual_owned)==sum(r['before']-r['after']for r in shao_owned),'Complete actual ordered owned damage')
  need(sum(r['damage']for r in actual_incoming)==sum(r['before']-r['after']for r in incoming),'Complete actual ordered incoming damage')
  actual_damage_groups=defaultdict(lambda:dict(stores=0,damage=0))
  for hit in actual_owned:
   g=actual_damage_groups[f"nativeAction_{hit['actualDamageWriterAction']:04X}"];g['stores']+=1;g['damage']+=hit['damage']
  actual_incoming_groups=defaultdict(lambda:dict(stores=0,damage=0,blockHeldDamage=0))
  for hit in actual_incoming:
   g=actual_incoming_groups[f"nativeAction_{hit['actionAtOwnDamage']:04X}"];g['stores']+=1;g['damage']+=hit['damage']
   g['blockHeldDamage']+=hit['damage']if hit['physicalBlockHeld']else 0
  cases[case]=dict(actualShao301EscapePlans=len(exit_plans),actualShao301EscapePlansWithNativeJump=sum(e['actualNativeJumpEntryFrame']is not None for e in episodes),actualShao301EscapeEpisodes=episodes,actualOriginal301Assignments=len(exit_assignments),actualOriginalHorizontalJumpEntries=len(jump_handlers),actualShaoOwnedDamageByActualAction=dict(actual_damage_groups),
   actualShaoIncomingDamageByActualAction=dict(actual_incoming_groups),
   actualShaoIncomingDamageWhileNativeGuard=sum(r['damage']for r in actual_incoming if r['actionAtOwnDamage']in(0x700,0x701)),
   actualShaoIncomingDamageWithPhysicalBlockHeld=sum(r['damage']for r in actual_incoming if r['physicalBlockHeld']),
   actualPositiveHealthShaoFields=sum(r['stage']==16 for r in fields.values()),
exactPreShaoNativeRecords=len(before),onlyExplicitPolicyLabelsNormalized=True,
   rejectedSpecificPrefixCounterexamples=counterexamples,actualKintaroMatchClear=kintaro,
   actualShaoUppercutPlans=len(upper_plans),actualShaoEscapeJumpkickPlans=len(escape_plans),
   actualShaoHorizontalJumpAssignments=sum(r['stage']==16 and r['after']==0x308 for r in actions),actualShaoHuman107Assignments=len(stage16_upper),
   actualShaoOwnedDamageStores=len(shao_owned),actualShaoOwnedDamage=sum(r['before']-r['after']for r in shao_owned),
   actualShaoUppercutDamage=sum(r['before']-r['after']for r in shao_owned if fields[r['frame']]['human_action']==0x107),
   actualShaoIncomingDamage=sum(r['before']-r['after']for r in incoming),actualShaoIncomingGroups=dict(groups),
   actualKintaroRoundWins=sum(r['tag']=='WIN'and r['slot']==side and r['stage']==15 for r in rows),
   actualShaoRoundWins=sum(r['tag']=='WIN'and r['slot']==side and r['stage']==16 for r in rows),
   actualShaoMatchClear=shao_match,actualEndingStarts=len(starts),actualEndingCompletions=len(completed),
   actualFullNativeCampaignAndReturnPath=proof['unassisted_clear_proven'],fullEndingArtAudioAcceptance=False,
   nativeStartupSleepCalls=2,measuredShaoUppercutSpacing=spacing,
   groupScope='Recorded pre-input native states, not causal CPU attack names or draw-time poses')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,
  fullEndingArtAudioAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 need(not args.output.exists(),'Immutable exact native boss-progress proof')
 result=verify();args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({case:{k:v for k,v in r.items()if k not in('measuredShaoUppercutSpacing','actualShaoIncomingGroups','actualShao301EscapeEpisodes')}for case,r in result['cases'].items()},indent=2),flush=True)
