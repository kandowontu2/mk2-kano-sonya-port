"""Independent per-field native boss action/health ledgers and specific corruptions.
Only immutable current-build real-input campaigns are accepted as controls.
An attack assignment cannot be counted without coherent native adjacent fields.
Full ladder/ending/art/audio acceptance remains outside this bounded extension.
"""
import argparse,copy,json
from collections import defaultdict
from pathlib import Path
import verify_current_boss_guard_edge_campaign_v2224 as native
import verify_current_interrupt_v1870 as launch
ROOT=native.ROOT
CASES={
 'kano_guard_edge12':('kano',1,'audit_v2225_current_kano_p1_guard_edge12_campaign','audit_v2226_current_kano_p1_guard_edge12_checked'),
 'sonya_guard_edge12':('sonya',1,'audit_v2225_current_sonya_p1_guard_edge12_campaign','audit_v2226_current_sonya_p1_guard_edge12_checked'),
 'kano_guard_edge16':('kano',1,'audit_v2233_current_kano_p1_guard_edge16_extended','audit_v2234_current_kano_p1_guard_edge16_extended_checked'),
 'sonya_guard_edge16':('sonya',1,'audit_v2225_current_sonya_p1_guard_edge16_campaign','audit_v2226_current_sonya_p1_guard_edge16_checked'),
}
def need(ok,message):
 if not ok:raise ValueError(message)
def check(rows,identity,side):
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
 need(fields and len(fields)==sum(r['tag']=='BOSS_FIELD'for r in rows),'Every real positive-health boss field uniquely inventoried')
 actions=defaultdict(list);health=defaultdict(list)
 for r in fields.values():
  need(r['human_id']==identity and r['cpu_id']==(12 if r['stage']==15 else 13),'True native human and boss IDs, never proxies')
 for r in rows:
  if r['tag']=='BOSS_ACTION':
   need(r['id']==r['roster']==identity and r['state']==1 and r['actor']==r['owner']and r['at']==r['main']+0x1f0 and r['mask']==0xffff,'Every actual action store has full native own character/Main provenance')
   if r['frame']in fields:
    f=fields[r['frame']]
    need(r['actor']==f['human_actor']and r['main']==f['human_main'],'Action store belongs to actual same-field physical human, not a swapped actor/process')
   if r['pc']==0xff83c340:
    need(r['after']==r['a1']&65535 and r['a8']==r['actor']and r['a13']==r['main'],'Common original action setter matches its actual incoming A1 and physical A8/A13')
   if r['after']==0x107:
    need(r['pc']==0xff83c340 and r['a1']&65535==0x107 and r['a8']==r['actor']and r['a13']==r['main'],'Human107 assignment uses original human action route, never CPU106 wrapper')
   actions[r['frame']].append(r)
  elif r['tag']=='HEALTH':health[r['frame'],r['slot']].append(r)
 pairs=action_changes=health_changes=0
 eligible=[]
 for frame,a in sorted(fields.items()):
  b=fields.get(frame+1)
  if not b or any(a[k]!=b[k]for k in ('human_actor','human_main','cpu_actor','cpu_main','stage')):continue
  pairs+=1;stores=actions[frame]
  coherent=(stores[0]['before']==a['human_action']and stores[-1]['after']==b['human_action']and all(x['after']==y['before']for x,y in zip(stores,stores[1:])))if stores else a['human_action']==b['human_action']
  need(coherent,'Action stores explain actual adjacent native fields and their ordered before/after ledger')
  action_changes+=a['human_action']!=b['human_action'];eligible.append(frame)
  ah,bh=[int(h)for h in a['health'].split(',')],[int(h)for h in b['health'].split(',')]
  for n,index in ((side,0),(3-side,1)):
   stores=health[frame,n]
   coherent=(stores[0]['before']==ah[index]and stores[-1]['after']==bh[index]and all(x['after']==y['before']for x,y in zip(stores,stores[1:])))if stores else ah[index]==bh[index]
   need(coherent,'Health stores explain actual adjacent native health and their ordered before/after ledger')
   health_changes+=ah[index]!=bh[index]
 return dict(positiveHealthAdjacentBossFieldPairs=pairs,nativeActionChanges=action_changes,
  nativeHealthChanges=health_changes,originalHuman107Assignments=sum(r['after']==0x107 for rs in actions.values()for r in rs),
  eligibleAdjacentFrames=eligible)
def verify(case):
 fighter,side,capture,positive=CASES[case];identity=17 if fighter=='kano'else 18
 folder=ROOT/capture;path=ROOT/positive/'report.json';proof=json.loads(path.read_text())
 need(proof['passed']and proof['bounded_campaign_evidence_proven']and not proof['fullPortAcceptance'],'Independent full current campaign context accepted')
 pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():need(launch.sha(file)==wanted,'Changed accepted trajectory '+file)
 pins[str(path)]=launch.sha(path);pins.update(launch.source_pins())
 need((folder/'guest_maincpu.bin').read_bytes()==native.current_source.expected()[0],'Every actual guest byte independently reconstructed for current build')
 rows=native.parse((folder/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
 control=check(rows,identity,side)
 need(control['originalHuman107Assignments']==proof['actualNativeUppercutAssignments'],'Native per-field ledger and accepted human107 classifier agree exactly')
 eligible=set(control['eligibleAdjacentFrames'])
 first_setter=next(i for i,r in enumerate(rows)if r['tag']=='BOSS_ACTION'and r['pc']==0xff83c340 and r['frame']in eligible)
 first_action=next(i for i,r in enumerate(rows)if r['tag']=='BOSS_ACTION'and r['frame']in eligible and r['before']!=r['after'])
 first_field=next(i for i,r in enumerate(rows)if r['tag']=='BOSS_FIELD')
 first_damage=next(i for i,r in enumerate(rows)if r['tag']=='HEALTH'and r['frame']in eligible and r['after']<r['before'])
 mutations=[
  ('wrong_incoming_setter',first_setter,'after',1,'Common original action setter'),
  ('wrong_action_before',first_action,'before',1,'Action stores explain'),
  ('proxy_human',first_field,'human_id',1,'True native human and boss IDs'),
  ('swapped_process',first_setter,'a13',16,'Common original action setter'),
  ('wrong_damage_after',first_damage,'after',-1,'Health stores explain'),
  ('missing_damage_store',first_damage,None,None,'Health stores explain'),
 ]
 upper=next((i for i,r in enumerate(rows)if r['tag']=='BOSS_ACTION'and r['after']==0x107),None)
 if upper is not None:mutations +=[
  ('cpu106_instead_of_human107',upper,'after',-1,'Common original action setter'),
  ('cpu_uppercut_wrapper_pc',upper,'pc',0xff870880-rows[upper]['pc'],'Human107 assignment'),
 ]
 outcomes=[]
 for name,index,key,delta,message in mutations:
  changed=copy.deepcopy(rows)
  if key is None:changed.pop(index)
  else:changed[index][key]+=delta
  try:check(changed,identity,side)
  except ValueError as error:
   need(message in str(error),'Intended native invariant, not incidental exception '+str(error));outcomes.append(dict(name=name,rejectedBy=str(error)))
  else:raise ValueError('Malformed native trajectory accepted '+name)
 need(check(rows,identity,side)==control,'Final untouched actual ledger control passes')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 control.pop('eligibleAdjacentFrames')
 return dict(passed=True,case=case,actualCampaignReport=str(path),**control,
  ownBossRoundWins=proof['actualBossRoundWins'],ownBossUppercutDamage=proof['actualBossUppercutDamage'],
  rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes,finalUnmodifiedControlPassed=True,
  fullLadderClearAccepted=proof['unassisted_clear_proven'],inputHashes=pins,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('case',choices=CASES);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 need(not args.output.exists(),'Immutable ledger proof')
 try:report=verify(args.case)
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','outcomes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
