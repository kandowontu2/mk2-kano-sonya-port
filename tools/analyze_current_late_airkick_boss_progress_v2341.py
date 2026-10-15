"""Actual late air-kicks, earned Kintaro matches and remaining native Shao combat.
Physical intent, pre-input action groups and hurt flights are not move activations.
No captured file, guest state, difficulty, health, position or AI is modified.
"""
import argparse,json,copy
from collections import defaultdict
from pathlib import Path
import verify_current_late_airkick_observed_boss_ledger_v2349 as ledger
import analyze_current_active_escape_episodes_v2328 as episode
ROOT=ledger.ROOT;launch=ledger.launch

def need(ok,message):
 if not ok:raise ValueError(message)

def verify():
 pins={};cases={}
 def accept(path):
  result=json.loads(path.read_text());need(result['passed']and not result['fullPortAcceptance'],'Actual accepted current campaign '+str(path))
  for file,wanted in result['inputHashes'].items():
   if file not in pins:need(launch.sha(file)==wanted,'Unchanged actual graph '+file);pins[file]=wanted
   else:need(pins[file]==wanted,'Consistent actual input graph '+file)
  pins[str(path)]=launch.sha(path);return result
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof=accept(ROOT/positive/'report.json')
  book=accept(ROOT/f'audit_v2350_current_{case}_boss_ledger_checked/report.json')
  negative=accept(ROOT/f'audit_v2352_current_{case}_input_counterexamples/report.json')
  need(negative['rejectedSpecificCounterexamples']==(15 if case.endswith('descend')else 14),'Actual non-vacuous rising/late/apex phase fixtures plus full input controls')
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  ledger.check(rows,17 if fighter=='kano'else 18,side)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
  actions=[r for r in rows if r['tag']=='BOSS_ACTION']
  jumps=[r for r in actions if r['after']==0x308 and r['pc']==0xff831360]
  kicks=[r for r in actions if r['after']==0x200 and r['pc']==0xff871f50]
  for r in jumps+kicks:
   need(r['a8']==r['actor']==r['owner']and r['a13']==r['main']and r['mask']==65535 and r['id']==r['roster']==(17 if fighter=='kano'else 18),'Original actual own jump/air-kick instruction dispatch and native registers')
  exits=[];closed=[]
  for kick in kicks:
   candidate=next((r for r in actions if r['event']>kick['event']and r['actor']==kick['actor']and r['main']==kick['main']and r['after']!=0x200),None)
   try:end=episode.actual_exit(kick,candidate,fields,actions)
   except ValueError:end=None
   if end:closed.append((kick,end))
   field=fields.get(kick['frame'])
   exits.append(dict(entryFrame=kick['frame'],entryHeight=field['height']if field else None,entryVY=field['human_vy']if field else None,
    exitFrame=end['frame']if end else None,exitAction=end['after']if end else None,durationFields=end['frame']-kick['frame']if end else None))
  need(closed,'Non-vacuous observed continuous own kick episodes')
  kick,end=next((a,b)for a,b in closed if b['frame']-a['frame']>4)
  changes=[];altered=copy.deepcopy(fields);altered.pop(kick['frame']+1)
  changes.append(('missing_episode_field',end,altered,'Continuous positive-health boss episode'))
  altered=copy.deepcopy(fields);altered[kick['frame']+1]['human_main']+=16
  changes.append(('recycled_main',end,altered,'Continuous actual own actor/Main episode'))
  altered_end=dict(end);altered_end['event']+=1
  changes.append(('unproven_exit',altered_end,fields,'Actual original next owned action transition'))
  for name,candidate,altered,message in changes:
   try:episode.actual_exit(kick,candidate,altered,actions)
   except ValueError as error:need(message in str(error),'Specific episode invariant '+name)
   else:raise ValueError('Malformed actual kick episode accepted '+name)
  episode.actual_exit(kick,end,fields,actions)
  earned=[]
  for transition in (r for r in rows if r['tag']=='STAGE'and r['stage']==16):
   start=max([r['event']for r in rows if r['tag']=='LOSS'and r['stage']==15 and r['event']<transition['event']]+[r['event']for r in rows if r['tag']=='STAGE'and r['stage']==15])
   wins=[r for r in rows if r['tag']=='WIN'and r['slot']==side and r['stage']==15 and start<r['event']<transition['event']]
   need(len(wins)==2 and all(r['id']==(17 if fighter=='kano'else 18)for r in wins),'Exactly two actual owned Kintaro round wins in one successful attempt, not accumulated losses')
   following=[r for r in rows if r['tag']=='LIVE'and r['stage']==16 and r['event']>transition['event']]
   need(following and following[0]['human']==f'{17 if fighter=="kano"else 18}:{17 if fighter=="kano"else 18}'and following[0]['cpu']=='13:13','Actual own true-ID live fight against native Shao Kahn after earned Kintaro match')
   earned.append(dict(actualStage16Frame=transition['frame'],actualOwnedKintaroWinFrames=[r['frame']for r in wins],firstActualShaoLiveFrame=following[0]['frame']))
  need(len(earned)==1,'One actual naturally earned Kintaro match per current control')
  combat=[r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before']and r['frame']in fields]
  owned=[r for r in combat if r['slot']==3-side and r['a8']==fields[r['frame']]['human_actor']and r['a13']==fields[r['frame']]['human_main']]
  need(len(owned)==proof['actualBossOwnedDamageStores'],'Complete actual owned boss damage inventory')
  need(sum(r['before']-r['after']for r in owned if fields[r['frame']]['human_action']==0x107)==proof['actualBossUppercutDamage']==book['ownBossUppercutDamage'],'Exact preserved original human107 damage accounting')
  per_stage={}
  for stage in (15,16):
   owned_groups=defaultdict(lambda:dict(stores=0,damage=0,preInputCPUGuardStores=0))
   incoming_groups=defaultdict(lambda:dict(stores=0,damage=0))
   for r in combat:
    f=fields[r['frame']]
    if f['stage']!=stage:continue
    if r['slot']==side:
     group=incoming_groups[f"preInputCPU_{f['cpu_action']:04X}"];group['stores']+=1;group['damage']+=r['before']-r['after']
    elif r in owned:
     group=owned_groups[f"preInputHuman_{f['human_action']:04X}"];group['stores']+=1;group['damage']+=r['before']-r['after'];group['preInputCPUGuardStores']+=f['cpu_action']in(0x700,0x701)
   per_stage[str(stage)]=dict(actualFields=sum(f['stage']==stage for f in fields.values()),ownedDamageGroups=dict(owned_groups),
    incomingDamageGroups=dict(incoming_groups),actualOwnRoundWins=sum(r['tag']=='WIN'and r['slot']==side and r['stage']==stage for r in rows),
    actionGroupScope='Recorded pre-input state groups only; not an inferred causal CPU attack name or draw-time pose')
  cases[case]=dict(actualHuman308Jumps=len(jumps),actualHuman200AirKicks=len(kicks),nativeKickEpisodes=exits,
   rejectedSpecificEpisodeCounterexamples=3,actualKintaroMatchClears=earned,actualKintaroRoundWins=per_stage['15']['actualOwnRoundWins'],
   actualShaoRoundWins=per_stage['16']['actualOwnRoundWins'],stages=per_stage,actualEndingStarts=proof['ending_starts'],actualEndingCompletions=proof['ending_completions'],
   fullLadderClear=proof['unassisted_clear_proven'],rejectedSpecificInputCounterexamples=negative['rejectedSpecificCounterexamples'])
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 need(not args.output.exists(),'Immutable natural boss-progress proof')
 result=verify();args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({case:{key:r[key]for key in('actualHuman308Jumps','actualHuman200AirKicks','actualKintaroMatchClears','actualKintaroRoundWins','actualShaoRoundWins','actualEndingStarts','stages')}for case,r in result['cases'].items()},indent=2),flush=True)
