"""Source-bound Shao contact outcomes under four physical-input distance policies.
Actual attack episodes and original owned damage, never universal hitbox/AI labels.
No guest state, health, difficulty, RNG, controller or captured record is modified.
"""
import argparse,json,struct,bisect
from pathlib import Path
from collections import defaultdict
import verify_current_shao_midrange_hp_boss_ledger_v2379 as ledger
import verify_current_shao_grounded_hp_boss_ledger_v2366 as prior
import diagnose_current_boss_damage_action_order_v2385 as ordered
ROOT=ledger.ROOT;launch=ledger.launch

def need(ok,message):
 if not ok:raise ValueError(message)

def source_check(guest,original):
 def data(raw,a,b):return raw[(a-0xff800000)//8:(b-0xff800000)//8]
 def u32(raw,a):return struct.unpack_from('<I',raw,(a-0xff800000)//8)[0]
 ranges=((0xff870dc0,0xff871080),(0xff8373f0,0xff837780),(0xff835410,0xff835dc0),(0xff83d910,0xff83dde0),(0xff8369f0,0xff836a40))
 for a,b in ranges:need(data(guest,a,b)==data(original,a,b),'Original uppercut startup, strike geometry/body helpers and Shao damage scaler unchanged '+hex(a))
 outer=u32(guest,0xff8eba30)
 need(data(guest,outer,outer+17*32)==data(original,0xff8eba90,0xff8eba90+17*32),'All original attack table rows preserved')
 donor=u32(original,u32(original,0xff8eba90+32)+8*32)
 descriptors=[]
 for identity in(17,18):
  row=u32(guest,outer+identity*32);descriptor=u32(guest,row+8*32)
  need(row!=u32(original,0xff8eba90+32)and descriptor!=donor,'True-ID dedicated row and relocated uppercut descriptor, not a character proxy')
  need(data(guest,descriptor,descriptor+144)==data(original,donor,donor+144),'Dedicated descriptor preserves complete original uppercut geometry/damage/reaction')
  descriptors.append(dict(identity=identity,row=row,descriptor=descriptor,words=struct.unpack('<9H',data(guest,descriptor,descriptor+144))))
 need(descriptors[0]['row']!=descriptors[1]['row']and descriptors[0]['descriptor']!=descriptors[1]['descriptor'],'Independent Kano and Sonya melee rows/descriptors')
 return dict(originalUnchangedRanges=[dict(first=a,lastExclusive=b)for a,b in ranges],trueIDUppercutDescriptors=descriptors)

def verify():
 pins={};cases={}
 def pin(path,wanted=None):
  path=str(Path(path).resolve())
  if path in pins:
   need(wanted is None or pins[path]==wanted,'Consistent accepted graph '+path);return
  actual=launch.sha(path);need(wanted is None or actual==wanted,'Unchanged actual graph '+path);pins[path]=actual
 guest=ledger.native.current_source.expected()[0];original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 source=source_check(guest,original);pin(ROOT/'mk2/mk2-maincpu.bin')
 for case,(fighter,side,capture,positive)in {**prior.CASES,**ledger.CASES}.items():
  folder=ROOT/capture;path=ROOT/positive/'report.json';proof=json.loads(path.read_text())
  need(proof['passed']and proof['bounded_campaign_evidence_proven']and not proof['fullPortAcceptance'],'Accepted complete bounded campaign control')
  for file,wanted in proof['inputHashes'].items():pin(file,wanted)
  pin(path);need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual initialized guest equals independent current source')
  rows=ledger.native.parse((folder/'run.log').read_text(encoding='utf-8-sig'),side,fighter);ledger.check(rows,17 if fighter=='kano'else 18,side)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16}
  actions=[r for r in rows if r['tag']=='BOSS_ACTION'and r['after']==0x107 and r['stage']==16]
  plans=[r for r in rows if r['tag']=='BOSS_PLAN'and r['stage']==16]
  damage=[r for r in ordered.classify(rows,side)if r['stage']==16 and r['actualDamageWriterAction']==0x107]
  episodes=[]
  for action in actions:
   f=fields[action['frame']]
   candidates=[r for r in plans if r['human_actor']==action['actor']and r['human_main']==action['main']and 0<=action['frame']-r['frame']<=15]
   need(len(candidates)==1,'One real physical plan owns this measured native107 start')
   plan=candidates[0]
   episodes.append(dict(event=action['event'],frame=action['frame'],actor=action['actor'],main=action['main'],actualPlanFrame=plan['frame'],planTo107Fields=action['frame']-plan['frame'],planGap=plan['gap'],planPreInputCPUPose=fields[plan['frame']]['cpu_pose'],planPreInputCPUBody=fields[plan['frame']]['cpu_body'],planPreInputCPUAction=fields[plan['frame']]['cpu_action'],gapAt107=f['gap'],preInputCPUAction=f['cpu_action'],preInputCPUBody=f['cpu_body'],preInputCPUPose=f['cpu_pose'],damageStores=[],exit=None))
  by_owner=defaultdict(list)
  for index,episode in enumerate(episodes):by_owner[episode['actor'],episode['main']].append((episode['event'],index))
  for hit in damage:
   entries=by_owner[hit['humanActor'],hit['humanMain']];at=bisect.bisect_right([r[0]for r in entries],hit['event'])-1
   need(at>=0,'Actual107 owned damage has a preceding own native107 assignment')
   episode=episodes[entries[at][1]]
   need(0<=hit['frame']-episode['frame']<60,'Damage belongs to a bounded original native107 episode')
   episode['damageStores'].append(hit)
  for episode in episodes:
   exits=[r for r in rows if r['tag']=='BOSS_ACTION'and r['event']>episode['event']and r['actor']==episode['actor']and r['main']==episode['main']and r['after']!=0x107]
   if exits:
    end=exits[0];episode['exit']=dict(frame=end['frame'],event=end['event'],action=end['after'],pc=end['pc'])
   need(not episode['damageStores']or not episode['exit']or max(r['event']for r in episode['damageStores'])<episode['exit']['event'],'Every actual107 hit precedes its true native exit')
   episode['ownedDamage']=sum(r['damage']for r in episode['damageStores'])
  groups=defaultdict(lambda:dict(actual107Starts=0,startsWithOwnedDamage=0,ownedDamage=0,actualGaps=[]))
  plan_groups=defaultdict(lambda:dict(actual107Starts=0,startsWithOwnedDamage=0,ownedDamage=0,actualGaps=[]))
  for e in episodes:
   group=groups[f"preInputCPU_{e['preInputCPUAction']:04X}_body_{e['preInputCPUBody']:04X}"]
   group['actual107Starts']+=1;group['startsWithOwnedDamage']+=bool(e['ownedDamage']);group['ownedDamage']+=e['ownedDamage'];group['actualGaps'].append(e['gapAt107'])
   plan_group=plan_groups[f"planCPU_{e['planPreInputCPUAction']:04X}_body_{e['planPreInputCPUBody']:04X}_pose_{e['planPreInputCPUPose']:08X}"]
   plan_group['actual107Starts']+=1;plan_group['startsWithOwnedDamage']+=bool(e['ownedDamage']);plan_group['ownedDamage']+=e['ownedDamage'];plan_group['actualGaps'].append(e['planGap'])
  for group in list(groups.values())+list(plan_groups.values()):
   group['actualGapRange']=[min(group['actualGaps']),max(group['actualGaps'])];del group['actualGaps']
  hit_gaps=sorted(set(e['gapAt107']for e in episodes if e['ownedDamage']))
  nohit_gaps=sorted(set(e['gapAt107']for e in episodes if not e['ownedDamage']and e['exit']))
  need(sum(e['ownedDamage']for e in episodes)==sum(r['damage']for r in damage),'Complete actual writer-action107 damage reconciliation')
  cases[case]=dict(actualPlans=len(plans),actual107Assignments=len(actions),assignmentsWithOwnedDamage=sum(bool(e['ownedDamage'])for e in episodes),actualOwnedDamageStores=len(damage),actualOwned107Damage=sum(r['damage']for r in damage),actualGapValuesWithHit=hit_gaps,actualGapValuesWithCompletedNoHit=nohit_gaps,sameActualGapCanHitOrNot=sorted(set(hit_gaps)&set(nohit_gaps)),preInputCPUStateGroups=dict(groups),planInputCPUStateGroups=dict(plan_groups),episodes=episodes,scope='Observed actual native107 episodes only; pre-input CPU states are not causal attack names. A completed zero-damage episode is not a character defect or universal geometry claim.')
 previous_path=ROOT/'audit_v2388_current_shao_contact_outcomes/report.json';previous=json.loads(previous_path.read_text())
 need(previous['passed']and not previous['gameOrCaptureModified'],'Accepted earlier complete contact episodes')
 for case,row in cases.items():
  restored={k:v for k,v in row.items()if k!='planInputCPUStateGroups'}
  restored['episodes']=[{k:v for k,v in e.items()if k not in('planPreInputCPUPose','planPreInputCPUBody','planPreInputCPUAction')}for e in row['episodes']]
  need(restored==previous['cases'][case],'All original source-bound contact episodes and counts preserved; only actual plan-time fields added')
 need(json.loads(json.dumps(source))==previous['source'],'Original source/descriptor facts preserved exactly under JSON tuple/list representation')
 for file,wanted in previous['inputHashes'].items():pin(file,wanted)
 pin(previous_path);pin(__file__);launch.module_pins(pins)
 return dict(passed=True,source=source,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable contact outcome proof')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({case:{k:v for k,v in row.items()if k not in('episodes','preInputCPUStateGroups','planInputCPUStateGroups')}for case,row in r['cases'].items()},indent=2),flush=True)
