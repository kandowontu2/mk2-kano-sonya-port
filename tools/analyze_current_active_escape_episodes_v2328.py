"""Native jump/air-kick dispatch and actual HP chronology in real boss inputs.
Planned Up or observed airborne hurt states do not prove an executed jump.
Opening120field incoming damage is measured; no guard-only delay is applied.
Paired old/new pre-boss traces must match exactly; later damage rates are descriptive.
"""
import argparse,json,copy
from collections import defaultdict
from pathlib import Path
import verify_current_stomp_window_boss_ledger_v2288 as old
import verify_current_active_escape_boss_ledger_v2318 as held
ROOT=old.ROOT

def need(ok,message):
 if not ok:raise ValueError(message)

def actual_exit(kick,candidate,fields,actions):
 next_action=next((r for r in actions if r['event']>kick['event']and r['actor']==kick['actor']and r['main']==kick['main']and r['after']!=0x200),None)
 need(candidate is not None and next_action is not None and candidate==next_action,'Actual original next owned action transition, not a later recycled Main')
 need(candidate['before']==0x200,'Observed end begins from the same native200action')
 for at in range(kick['frame'],candidate['frame']+1):
  field=fields.get(at)
  need(field is not None,'Continuous positive-health boss episode, no missing frame or later round')
  need(field['human_actor']==kick['actor']and field['human_main']==kick['main'],'Continuous actual own actor/Main episode, no task recycling')
 return candidate

def verify():
 pins={};cases={};episode_counterexamples={};rejected_recycled_exits={}
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Accepted actual source/trajectory '+str(path))
  for file,wanted in r['inputHashes'].items():
   if file not in pins:need(old.launch.sha(file)==wanted,'Unchanged actual graph '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent actual graph '+file)
  pins[str(path)]=old.launch.sha(path);return r
 prefix=accept(ROOT/'audit_v2323_current_active_escape_extended_prefix/report.json')
 need(not prefix['identityGateWaived']and prefix['completeNativePrefixWithoutNormalization'],'Actual extended recording completes original selection without any gate waiver')
 for module,ledger_version in((held,2320),):
  for case,(fighter,side,capture,positive)in module.CASES.items():
   proof=accept(ROOT/positive/'report.json');book=accept(ROOT/f'audit_v{ledger_version}_current_{case}_boss_ledger_checked/report.json')
   accept(ROOT/f'audit_v2321_current_{case}_input_counterexamples/report.json')
   rows=module.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
   module.check(rows,17 if fighter=='kano'else 18,side)
   fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
   actions=[r for r in rows if r['tag']=='BOSS_ACTION']
   jumps=[r for r in actions if r['after']==0x308 and r['pc']==0xff831360]
   kicks=[r for r in actions if r['after']==0x200 and r['pc']==0xff871f50]
   kick_exits=[];closed=[]
   for kick in kicks:
    candidate=next((r for r in actions if r['event']>kick['event']and r['actor']==kick['actor']and r['main']==kick['main']and r['after']!=0x200),None)
    try:following=actual_exit(kick,candidate,fields,actions)
    except ValueError:following=None
    if following:closed.append((kick,following))
    entry_field=fields.get(kick['frame']);exit_field=fields.get(following['frame'])if following else None
    kick_exits.append(dict(entryFrame=kick['frame'],entryGap=entry_field['gap']if entry_field else None,
     entryHeight=entry_field['height']if entry_field else None,entryVY=entry_field['human_vy']if entry_field else None,
     exitFrame=following['frame']if following else None,exitAction=following['after']if following else None,
     exitPC=following['pc']if following else None,durationFields=following['frame']-kick['frame']if following else None,
     exitGap=exit_field['gap']if exit_field else None,exitHeight=exit_field['height']if exit_field else None,
     scope='First observed non200transition in the same continuous positive-health own actor/Main episode. Unknown exits are not inferred failures; field geometry is pre-input, not a draw-time pose'))
   need(closed,'Non-vacuous actual within-episode air-kick recovery '+case)
   kick,end=next((kick,end)for kick,end in closed if end['frame']-kick['frame']>4)
   middle=kick['frame']+1;checks=[]
   changed=copy.deepcopy(fields);changed.pop(middle)
   changes=[('missing_native_episode_frame',end,changed,'Continuous positive-health boss episode')]
   changed=copy.deepcopy(fields);changed[middle]['human_main']+=16
   changes.append(('recycled_owned_main',end,changed,'Continuous actual own actor/Main episode'))
   changed_end=dict(end);changed_end['event']+=1
   changes.append(('later_unproven_action_end',changed_end,fields,'Actual original next owned action transition'))
   for name,candidate,changed_fields,message in changes:
    try:actual_exit(kick,candidate,changed_fields,actions)
    except ValueError as error:need(message in str(error),'Specific episode invariant '+name);checks.append(name)
    else:raise ValueError('Malformed native episode accepted '+name)
   actual_exit(kick,end,fields,actions);episode_counterexamples[case]=checks
   superseded=json.loads((ROOT/'audit_v2325_current_active_escape_windows/report.json').read_text())
   alias_failures=[]
   for previous in superseded['cases'][case]['nativeAirKickExits']:
    if previous['exitFrame']is None:continue
    start=next(r for r in kicks if r['frame']==previous['entryFrame'])
    old_end=next(r for r in actions if r['frame']==previous['exitFrame']and r['actor']==start['actor']and r['main']==start['main']and r['before']==0x200 and r['after']==previous['exitAction'])
    try:actual_exit(start,old_end,fields,actions)
    except ValueError as error:alias_failures.append(dict(entryFrame=start['frame'],incorrectExitFrame=old_end['frame'],rejectedBy=str(error)))
   rejected_recycled_exits[case]=alias_failures
   for r in jumps+kicks:
    need(r['a8']==r['actor']==r['owner']and r['a13']==r['main']and r['mask']==65535 and r['id']==r['roster']==(17 if fighter=='kano'else 18),'Original native human jump/airkick dispatch owner and actual registers')
   combat=[r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before']]
   incoming=[r for r in combat if r['slot']==side and r['frame']in fields]
   owned=[r for r in combat if r['slot']==3-side and r['frame']in fields and r['a8']==fields[r['frame']]['human_actor']and r['a13']==fields[r['frame']]['human_main']]
   damage_groups=defaultdict(lambda:dict(stores=0,damage=0,cpuGuardStores=0))
   for r in owned:
    f=fields[r['frame']];g=damage_groups[f"own_{f['human_action']:04X}"]
    g['stores']+=1;g['damage']+=r['before']-r['after'];g['cpuGuardStores']+=f['cpu_action']in(0x700,0x701)
   plans=[r for r in rows if r['tag']=='BOSS_PLAN'and r['move']=='close_pressure_jumpkick_attempt']
   windows=[];mapped=set()
   for i,p in enumerate(plans):
    start=p['frame'];stop=min(start+60,plans[i+1]['frame']if i+1<len(plans)else start+60)
    actual=[r for r in jumps if start<=r['frame']<stop and r['actor']==p['human_actor']and r['main']==p['human_main']]
    attacks=[r for r in kicks if start<=r['frame']<stop and r['actor']==p['human_actor']and r['main']==p['human_main']]
    for r in actual:need(r['event']not in mapped,'Native jump uniquely assigned to actual physical plan');mapped.add(r['event'])
    flight_damage=[r for r in owned if start<=r['frame']<stop and fields[r['frame']]['human_action']==0x200]
    windows.append(dict(start=start,gap=p['gap'],ownStartAction=p['human_action'],actualJumpFrames=[r['frame']for r in actual],
     actualAirKickFrames=[r['frame']for r in attacks],airKickDamage=sum(r['before']-r['after']for r in flight_damage),
     guardedAirKickDamage=sum(r['before']-r['after']for r in flight_damage if fields[r['frame']]['cpu_action']in(0x700,0x701))))
   need(len(mapped)==len(jumps),'Every actual308jump mapped once, no hurt-flight promoted to a jump')
   rounds=[];current=None
   for frame,f in sorted(fields.items()):
    if current is None or frame!=current['lastFrame']+1:
     current=dict(firstFrame=frame,lastFrame=frame,initialHealth=f['health'],healthAfterFirst120=None);rounds.append(current)
    current['lastFrame']=frame
    if frame-current['firstFrame']==119:current['healthAfterFirst120']=f['health']
   for r in rounds:
    quiet=[d for d in incoming if r['firstFrame']<=d['frame']<r['firstFrame']+120]
    r['actualFirst120Damage']=sum(d['before']-d['after']for d in quiet)
   need(len(owned)==proof['actualBossOwnedDamageStores'],'All own original-writer boss damage inventoried')
   need(sum(g['damage']for k,g in damage_groups.items()if k=='own_0107')==proof['actualBossUppercutDamage']==book['ownBossUppercutDamage'],'Native107damage accounting exactly retained')
   cases[case]=dict(actualHuman308Jumps=len(jumps),actualHuman200AirKicks=len(kicks),physicalJumpkickPlans=len(plans),
    actualOwnedBossDamage=sum(r['before']-r['after']for r in owned),ownedDamageGroups=dict(damage_groups),jumpWindows=windows,nativeAirKickExits=kick_exits,
    actualFirst120IncomingDamage=sum(r['actualFirst120Damage']for r in rounds),actualPositiveHealthBossSegments=len(rounds),rounds=rounds)
 comparisons={}
 for case,(fighter,side,capture,positive)in held.CASES.items():
  previous_case=case.replace('escape_active_','escape_hold_')
  # Accepted unchanged-delay baselines remain actual full campaigns, not edited logs.
  previous_capture=f'audit_v2292_current_{fighter}_p1_'+previous_case.split(fighter+'_',1)[1]+'_campaign'
  previous_report=f'audit_v2293_current_{fighter}_p1_'+previous_case.split(fighter+'_',1)[1]+'_checked/report.json'
  accept(ROOT/previous_report)
  previous_rows=old.native.parse((ROOT/previous_capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  current_rows=held.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  before_frame=min(r['frame']for r in current_rows if r['tag']=='BOSS_FIELD')
  old_frame=min(r['frame']for r in previous_rows if r['tag']=='BOSS_FIELD')
  need(before_frame==old_frame,'Same actual first-boss frame, no changed ordinary progression '+case)
  def before(path,policy):
   result=[]
   with path.open(encoding='utf-8-sig')as stream:
    for line in stream:
     if not line.startswith('MK2_NAT_CAMPAIGN_'):continue
     frame=int(__import__('re').search(r' frame=(\d+)',line)[1])
     if frame>=before_frame:break
     result.append(line.replace('policy='+policy,'policy=paired_escape').rstrip('\r\n'))
   return result
  left=before(ROOT/previous_capture/'run.log',previous_case.split(fighter+'_',1)[1])
  right=before(ROOT/capture/'run.log',case.split(fighter+'_',1)[1])
  need(left==right and len(left)>10000,'Every actual pre-boss native record matches; only declared policy labels normalized '+case)
  limit=prefix['originalTerminalFrame']
  def measured(rows):
   fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'and r['frame']<=limit}
   damage=[r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before']and r['frame']in fields]
   incoming=sum(r['before']-r['after']for r in damage if r['slot']==side)
   owned=sum(r['before']-r['after']for r in damage if r['slot']==3-side and r['a8']==fields[r['frame']]['human_actor']and r['a13']==fields[r['frame']]['human_main'])
   wins=sum(r['tag']=='WIN'and r['slot']==side and r['stage']in(15,16)and r['frame']<=limit for r in rows)
   return dict(actualBossFields=len(fields),actualIncomingHP=incoming,actualOwnedBossDamage=owned,actualOwnBossRoundWins=wins,
    incomingHPPer1000BossFields=incoming*1000/len(fields),ownedDamagePer1000BossFields=owned*1000/len(fields))
  comparisons[case]=dict(exactPreBossNativeRecords=len(left),sameChronologicalFrameLimit=limit,
   openingDelay120=measured(previous_rows),openingDelay0=measured(current_rows),
   scope='Same cold native pre-boss chronology. Subsequent rounds and RNG diverge with different real inputs; rates are descriptive, not per-round causal claims.')
 for diagnostic in (ROOT/'tools/analyze_current_active_escape_windows_v2324.py',ROOT/'audit_v2325_current_active_escape_windows/report.json'):
  pins[str(diagnostic)]=old.launch.sha(diagnostic)
 pins[str(Path(__file__).resolve())]=old.launch.sha(__file__);old.launch.module_pins(pins)
 return dict(passed=True,cases=cases,pairedDelayComparisons=comparisons,rejectedSpecificEpisodeCounterexamples=sum(map(len,episode_counterexamples.values())),episodeCounterexamples=episode_counterexamples,rejectedSupersededRecycledExits=rejected_recycled_exits,supersededResidencyReport=str(ROOT/'audit_v2325_current_active_escape_windows/report.json'),inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable native active-escape chronology')
 result=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(cases={k:{q:v[q]for q in('actualHuman308Jumps','actualHuman200AirKicks','physicalJumpkickPlans','ownedDamageGroups','actualFirst120IncomingDamage','actualPositiveHealthBossSegments')}for k,v in result['cases'].items()},pairedDelayComparisons=result['pairedDelayComparisons'],rejectedSpecificEpisodeCounterexamples=result['rejectedSpecificEpisodeCounterexamples'],rejectedSupersededRecycledExits=result['rejectedSupersededRecycledExits']),indent=2),flush=True)
