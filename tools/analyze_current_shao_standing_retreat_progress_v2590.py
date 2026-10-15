"""Exact pre-Shao trajectory and actual ordered guarded-walk outcomes.
Only earned native boss matches and own ending/return count as a full campaign.
"""
import argparse,json,re
from pathlib import Path
from collections import defaultdict
import verify_current_shao_standing_retreat_boss_ledger_v2586 as ledger
import diagnose_current_boss_damage_action_order_v2385 as ordered
from analyze_current_shao_opening_damage_states_v2408 import own_damage
from analyze_current_shao_crouch_exit_progress_v2471 import earned
ROOT=ledger.ROOT;launch=ledger.launch

def need(ok,label):
 if not ok:raise ValueError(label)

def exact(a,b):need(a==b,'Entire pre-Shao native chronology exactly preserved; only policy labels normalized')

def verify(case):
 fighter,side,capture,positive=ledger.CASES[case];pins={}
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual accepted bounded proof '+str(path))
  for file,wanted in r['inputHashes'].items():
   if file in pins:need(pins[file]==wanted,'Consistent actual dependency')
   else:need(launch.sha(file)==wanted,'Unchanged actual dependency '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);return r
 proof=accept(ROOT/positive/'report.json')
 book=accept(ROOT/f'audit_v2588_current_{fighter}_shao_standing_retreat_boss_ledger_checked/report.json')
 negative=accept(ROOT/f'audit_v2589_current_{fighter}_shao_standing_retreat_input_counterexamples/report.json')
 source=accept(ROOT/'audit_v2584_standing_retreat_source_boundary_checked/report.json')
 recovery=accept(ROOT/'audit_v2548_dynamic_native_source_dependencies_recovered/report.json')
 compression=accept(ROOT/'audit_v2554_restored_native_dependencies_compressed/report.json')
 need(book['rejectedSpecificCounterexamples']==8 and book['finalUnmodifiedControlPassed'],'Complete ordered native ledger with eight specific negatives')
 need(negative['rejectedSpecificCounterexamples']>=20 and negative['finalUnmodifiedFullCampaignControlPassed'],'Complete independent boss input replay with specific actual input negatives')
 need(source['fullSourceInverse']and source['wholeLauncherInverse']and recovery['wholeCurrentGuestAndPayloadReconstructed'],'Exact original ordinary controls and actual native reconstruction retained')
 accept(ROOT/f'audit_v2348_current_{fighter}_p1_late_apex_checked/report.json')
 text=(ROOT/capture/'run.log').read_text(encoding='utf-8-sig')
 old=(ROOT/f'audit_v2347_current_{fighter}_p1_late_apex_campaign/run.log').read_text(encoding='utf-8-sig')
 rows=ledger.native.parse(text,side,fighter);identity=17 if fighter=='kano'else 18;ledger.check(rows,identity,side)
 first=next(r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16)
 def prefix(raw,policy):return[line.replace('policy='+policy,'policy=late_apex')for line in raw.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and int(re.search(r' frame=(\d+)',line)[1])<first['frame']]
 before=prefix(old,'late_apex');after=prefix(text,proof['bossPolicy']);exact(before,after)
 index=next(i for i,line in enumerate(after)if line.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD '));counterexamples=[]
 for kind in('missing_native_field','changed_own_ID','changed_actual_health'):
  changed=list(after)
  if kind=='missing_native_field':changed.pop(index)
  elif kind=='changed_own_ID':changed[index]=changed[index].replace('human_id='+str(identity),'human_id=1',1)
  else:changed[index]=re.sub(r' health=(\d+),',lambda m:' health='+str(int(m[1])-1)+',',changed[index],count=1)
  need(changed!=after,'Non-vacuous chronological counterexample')
  try:exact(before,changed)
  except ValueError as error:need('Entire pre-Shao native chronology'in str(error),'Specific chronological rejection');counterexamples.append(kind)
  else:raise ValueError('Changed native chronology accepted')
 exact(before,after)
 transition=next(r for r in rows if r['tag']=='STAGE'and r['stage']==16);kintaro=earned(rows,15,side,identity,transition)
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16}
 actions=[r for r in rows if r['tag']=='BOSS_ACTION'and r['stage']==16];inputs=defaultdict(set)
 for r in rows:
  if r['tag']=='INPUT'and r['frame']in fields:inputs[r['frame']].add(r['button'])
 need(all(inputs[f]<=set(('Up','Left','Right','High_Kick'))for f in fields),'Only declared stage16 physical standing movement/jump/kick inputs; no crouch or guard')
 plans=[r for r in rows if r['tag']=='BOSS_PLAN'and r['stage']==16]
 need(plans and all(r['move']=='shao_standing_retreat_jumpkick_attempt'for r in plans),'Actual Shao-only standing jump plans; none assumed to activate')
 owned=[r for r in ordered.classify(rows,side)if r['stage']==16];incoming=own_damage(rows,side)
 damage=defaultdict(lambda:dict(stores=0,damage=0));hurt=defaultdict(lambda:dict(stores=0,damage=0,physicalBlockHeldDamage=0))
 for r in owned:g=damage[f"nativeAction_{r['actualDamageWriterAction']:04X}"];g['stores']+=1;g['damage']+=r['damage']
 for r in incoming:g=hurt[f"nativeAction_{r['actionAtOwnDamage']:04X}"];g['stores']+=1;g['damage']+=r['damage'];g['physicalBlockHeldDamage']+=r['damage']if r['physicalBlockHeld']else 0
 starts=[r for r in rows if r['tag']=='ENDING_START'];completed=[r for r in rows if r['tag']=='ENDING_COMPLETED']
 shao=earned(rows,16,side,identity,starts[0])if starts else None
 need(proof['unassisted_clear_proven']==bool(shao and completed),'Only actual earned Shao match plus own ending/return counts as full campaign')
 launch.module_pins(pins);pins[str(Path(__file__).resolve())]=launch.sha(__file__)
 return dict(passed=True,case=case,campaignReport=str(ROOT/positive/'report.json'),exactPreShaoNativeRecords=len(before),onlyPolicyLabelsNormalized=True,
  rejectedSpecificPrefixCounterexamples=counterexamples,actualKintaroMatchClear=kintaro,repeatedKintaroControlNotIndependentStrategyCoverage=True,
  actualKintaroRoundWins=sum(r['tag']=='WIN'and r['slot']==side and r['stage']==15 for r in rows),
  actualShaoRoundWins=sum(r['tag']=='WIN'and r['slot']==side and r['stage']==16 for r in rows),actualShaoMatchClear=shao,
  actualEndingStarts=len(starts),actualEndingCompletions=len(completed),actualFullNativeCampaignAndReturnPath=proof['unassisted_clear_proven'],
  actualStage16PhysicalFields=len(fields),actualShaoStandingJumpPlans=len(plans),actualShaoNative308Assignments=sum(r['after']==0x308 for r in actions),actualShaoAirborneTransitions=sum(r['tag']=='BOSS_RESPONSE'and r['stage']==16 for r in rows),actualShaoHuman107Assignments=sum(r['after']==0x107 for r in actions),
  actualShaoBlockHeldFields=sum('Block'in inputs[f]for f in fields),actualShaoOwnedDamage=sum(r['damage']for r in owned),actualShaoIncomingDamage=sum(r['damage']for r in incoming),
  actualShaoOwnedDamageByActualAction=dict(damage),actualShaoIncomingDamageByActualAction=dict(hurt),
  originalHuman107Assignments=book['originalHuman107Assignments'],ownBossUppercutDamage=book['ownBossUppercutDamage'],ownBossRoundWins=book['ownBossRoundWins'],
  rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=negative['rejectedSpecificCounterexamples'],inputHashes=pins,gameChanged=False,
  fullEndingArtAudioAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',choices=ledger.CASES);p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable actual progress evidence')
 r=verify(a.case);a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
