"""Actual Shao attack outcomes, own damage states and exact longer Sonya recapture.
Recorded native action states and physical Block inputs are not causal attack names.
No guest, health, AI, difficulty, RNG, controller or recorded byte is modified.
"""
import argparse,json,re,bisect
from pathlib import Path
from collections import defaultdict
import verify_current_shao_opening_guard_boss_ledger_v2400 as ledger
import diagnose_current_boss_damage_action_order_v2385 as ordered
ROOT=ledger.ROOT;launch=ledger.launch
def need(ok,message):
 if not ok:raise ValueError(message)

def own_damage(rows,side):
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
 inputs=defaultdict(set)
 for r in rows:
  if r['tag']=='INPUT':inputs[r['frame']].add(r['button'])
 current=None;items=[]
 for r in rows:
  f=fields.get(r['frame'])
  if r['tag']=='BOSS_FIELD':current=dict(frame=r['frame'],actor=r['human_actor'],main=r['human_main'],action=r['human_action'])
  elif r['tag']=='BOSS_ACTION'and f:
   need(current and current['frame']==r['frame']and current['actor']==r['actor']and current['main']==r['main'],'Actual ordered own action context')
   need(current['action']==r['before'],'Actual action before/after chain');current['action']=r['after']
  elif r['tag']=='HEALTH'and f and f['stage']==16 and r['slot']==side and r['pc']==0xff836700 and r['after']<r['before']:
   need(current and current['frame']==r['frame'],'Actual native own damage in this field')
   items.append(dict(frame=r['frame'],event=r['event'],damage=r['before']-r['after'],actionAtOwnDamage=current['action'],preInputCPUPose=f['cpu_pose'],preInputCPUBody=f['cpu_body'],physicalBlockHeld='Block'in inputs[r['frame']],attackerActor=r['a8'],attackerMain=r['a13'],registersMatchScheduledBoss=r['a8']==f['cpu_actor']and r['a13']==f['cpu_main']))
 return items

def native_prefix(text,until):
 return [line for line in text.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and int(re.search(r' frame=(\d+)',line)[1])<until]
def exact(a,b):need(a==b,'Every nonterminal native row from original incomplete capture matches longer actual recapture')

def verify():
 pins={};cases={}
 def pin(path,wanted=None):
  path=str(Path(path).resolve())
  if path in pins:need(wanted is None or pins[path]==wanted,'Consistent actual graph '+path);return
  actual=launch.sha(path);need(wanted is None or actual==wanted,'Unchanged actual graph '+path);pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Accepted actual bounded report '+str(path))
  for file,wanted in r['inputHashes'].items():pin(file,wanted)
  pin(path);return r
 progress=accept(ROOT/'audit_v2405_current_shao_opening_guard_progress/report.json')
 boundary=accept(ROOT/'audit_v2413_current_sonya_opening_boundary/report.json');need(boundary['originalFullCampaignStillRejected'],'Incomplete recording never accepted')
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof=accept(ROOT/positive/'report.json');accept(ROOT/f'audit_v2402_current_{case}_boss_ledger_checked/report.json');negative=accept(ROOT/f'audit_v2403_current_{case}_input_counterexamples/report.json')
  need(negative['rejectedSpecificCounterexamples']==23,'Nine specific current Shao physical/visible-pose/body negatives plus fourteen original boss negatives')
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter);ledger.check(rows,17 if fighter=='kano'else 18,side)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16}
  attacks=[r for r in rows if r['tag']=='BOSS_ACTION'and r['stage']==16 and r['after']==0x107]
  owned=[r for r in ordered.classify(rows,side)if r['stage']==16 and r['actualDamageWriterAction']==0x107]
  episodes=[]
  by_owner=defaultdict(list)
  for index,r in enumerate(attacks):
   by_owner[r['actor'],r['main']].append((r['event'],index))
   episodes.append(dict(frame=r['frame'],event=r['event'],actor=r['actor'],main=r['main'],damageStores=[],preInputCPUPose=fields[r['frame']]['cpu_pose']))
  for hit in owned:
   entries=by_owner[hit['humanActor'],hit['humanMain']];at=bisect.bisect_right([r[0]for r in entries],hit['event'])-1
   need(at>=0,'Owned107 damage has a preceding native107 assignment');episode=episodes[entries[at][1]]
   need(0<=hit['frame']-episode['frame']<=15,'Same measured original uppercut episode');episode['damageStores'].append(hit)
  incoming=own_damage(rows,side)
  need(sum(r['damage']for r in owned)==progress['cases'][case]['actualShaoUppercutDamage'],'Original owned damage and independent progress inventory reconcile')
  need(sum(r['damage']for r in incoming)==progress['cases'][case]['actualShaoIncomingDamage'],'Complete original incoming damage inventory reconciles')
  groups=defaultdict(lambda:dict(stores=0,damage=0,physicalBlockHeldStores=0,physicalBlockHeldDamage=0,scheduledBossRegisterMatches=0))
  for r in incoming:
   group=groups[f"actualOwnAction_{r['actionAtOwnDamage']:04X}_preInputCPU_{r['preInputCPUPose']:08X}_body_{r['preInputCPUBody']:04X}"]
   group['stores']+=1;group['damage']+=r['damage'];group['physicalBlockHeldStores']+=r['physicalBlockHeld'];group['physicalBlockHeldDamage']+=r['damage']if r['physicalBlockHeld']else 0;group['scheduledBossRegisterMatches']+=r['registersMatchScheduledBoss']
  cases[case]=dict(actual107Assignments=len(attacks),actual107EpisodesWithOwnedDamage=sum(bool(e['damageStores'])for e in episodes),actualOwned107Damage=sum(r['damage']for r in owned),allActual107EpisodesHaveExactlyOneOwned30HPStore=bool(episodes)and all(len(e['damageStores'])==1 and e['damageStores'][0]['damage']==30 for e in episodes),actualOwnCombatDamage=sum(r['damage']for r in incoming),actualOwnCombatDamageWhileNativeGuard=sum(r['damage']for r in incoming if r['actionAtOwnDamage']in(0x700,0x701)),actualOwnCombatDamageWithPhysicalBlockHeld=sum(r['damage']for r in incoming if r['physicalBlockHeld']),incomingGroups=dict(groups),episodes=episodes,incoming=incoming)
 old_text=(ROOT/'audit_v2398_current_sonya_p1_shao_taunt_guard_campaign/run.log').read_text(encoding='utf-8-sig')
 new_text=(ROOT/'audit_v2410_current_sonya_p1_shao_taunt_guard_campaign/run.log').read_text(encoding='utf-8-sig')
 before=native_prefix(old_text,boundary['terminalFrame']);after=native_prefix(new_text,boundary['terminalFrame']);exact(before,after)
 index=next(i for i,l in enumerate(after)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD '))
 negatives=[]
 for kind in('missing_actual_field','changed_true_ID','changed_actual_health'):
  changed=list(after)
  if kind=='missing_actual_field':changed.pop(index)
  elif kind=='changed_true_ID':changed[index]=changed[index].replace('human_id=18','human_id=1',1)
  else:changed[index]=re.sub(r' health=(\d+),',lambda m:' health='+str(int(m[1])-1)+',',changed[index],count=1)
  need(changed!=after,'Nonvacuous native prefix mutation')
  try:exact(before,changed)
  except ValueError as error:need('Every nonterminal native row'in str(error),'Specific exact replay invariant');negatives.append(kind)
  else:raise ValueError('Changed actual incomplete prefix accepted')
 exact(before,after)
 rows=ledger.native.parse(new_text,1,'sonya')
 selected=[r for r in rows if r['tag']=='SELECT_ID'and r['number']==22]
 need(len(selected)==2 and [r['frame']for r in selected]==[boundary['firstMissingObservationDue'],boundary['secondMissingObservationDue']]and all(r['roster']==18 and r['state']==3 for r in selected),'Previously clipped22nd selection completes at original due fields with true Sonya18')
 next_fight=next(r for r in rows if r['tag']=='FIGHT'and r['selection']==22)
 need(next_fight['stage']==16 and next_fight['human']=='18:18'and next_fight['cpu']=='13:13','Same completed selection actually enters native Sonya versus Shao')
 pin(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,exactRecapturedNonterminalNativeRecords=len(before),recapturedSelection22Confirmed=selected,recapturedSelection22Fight=next_fight,rejectedSpecificRecapturePrefixCounterexamples=negatives,shortRunStillRejected=True,recaptureNotAnotherIndependentStrategy=True,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable actual opening damage-state proof')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({case:{k:v for k,v in row.items()if k not in('incomingGroups','episodes','incoming')}for case,row in r['cases'].items()},indent=2),flush=True)
