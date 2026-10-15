"""Exact pre-Shao chronology and actual ordered outcomes under physical crouch-wait.
No plan is an activation, no partial tower is a clear, and no game state is changed.
"""
import argparse,json,re,struct
from pathlib import Path
from collections import defaultdict
import verify_current_shao_duck_wait_boss_ledger_v2526 as ledger
import diagnose_current_boss_damage_action_order_v2385 as ordered
from analyze_current_shao_opening_damage_states_v2408 import own_damage
from analyze_current_shao_crouch_exit_progress_v2471 import earned
ROOT=ledger.ROOT;launch=ledger.launch
CHECKS={'kano_shao_duck_wait':('audit_v2510_current_kano_shao_duck_wait_boss_ledger_checked','audit_v2511_current_kano_shao_duck_wait_input_counterexamples'),
 'sonya_shao_duck_wait':('audit_v2530_current_sonya_shao_duck_wait_boss_ledger_checked','audit_v2531_current_sonya_shao_duck_wait_input_counterexamples')}
def need(ok,label):
 if not ok:raise ValueError(label)
def exact(a,b):need(a==b,'Entire pre-Shao native chronology exactly preserved; only policy labels normalized')
def verify():
 pins={};cases={}
 def accept(path):
  report=json.loads(path.read_text());need(report['passed']and not report['fullPortAcceptance'],'Actual accepted bounded proof '+str(path))
  for file,wanted in report['inputHashes'].items():
   if file in pins:need(pins[file]==wanted,'Consistent old/new graph')
   else:need(launch.sha(file)==wanted,'Unchanged actual source/capture '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);return report
 boundary=accept(ROOT/'audit_v2529_current_sonya_duck_wait_extended_boundary/report.json')
 need(boundary['originalFullCaptureRemainsRejected']and boundary['originalFailedCaptureNeverWaived']and boundary['exactOriginalNativeRows']==312603,'Original failed3600capture retained; entire genuine extended chronology proven')
 current=ledger.native.current_source.expected()[0];original_path=ROOT/'mk2/mk2-maincpu.bin';original=original_path.read_bytes();pins[str(original_path)]=launch.sha(original_path)
 for at,words in((0xff870e70,(0x09c0,1)),(0xff870e90,(0x0d5f,0xdcc0,0xff80)),(0xff870ef0,(0x09c0,1)),(0xff870f10,(0x0d5f,0xdcc0,0xff80)),(0xff870f50,(0x09c1,0x0107))):
  offset=(at-0xff800000)//8;expected=struct.pack('<'+'H'*len(words),*words)
  need(current[offset:offset+len(expected)]==original[offset:offset+len(expected)]==expected,'Original two one-tick human uppercut startup sleeps and native107 dispatch unchanged')
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof=accept(ROOT/positive/'report.json');book_name,negative_name=CHECKS[case]
  book=accept(ROOT/book_name/'report.json');negative=accept(ROOT/negative_name/'report.json')
  need(book['rejectedSpecificCounterexamples']==8 and book['finalUnmodifiedControlPassed'],'Complete ordered native ledger and8specific negatives')
  need(negative['rejectedSpecificCounterexamples']==27 and negative['finalUnmodifiedFullCampaignControlPassed'],'All14original boss physical controls,9Shao openings and4non-vacuous crouch-wait controls; no absent escape fixture substituted')
  accept(ROOT/f'audit_v2348_current_{fighter}_p1_late_apex_checked/report.json')
  text=(ROOT/capture/'run.log').read_text(encoding='utf-8-sig');old=(ROOT/f'audit_v2347_current_{fighter}_p1_late_apex_campaign/run.log').read_text(encoding='utf-8-sig')
  rows=ledger.native.parse(text,side,fighter);identity=17 if fighter=='kano'else 18
  ledger.check(rows,identity,side)
  first=next(r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16)
  def prefix(raw,policy):return [line.replace('policy='+policy,'policy=late_apex')for line in raw.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and int(re.search(r' frame=(\d+)',line)[1])<first['frame']]
  before=prefix(old,'late_apex');after=prefix(text,proof['bossPolicy']);exact(before,after)
  index=next(i for i,line in enumerate(after)if line.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD '));negatives=[]
  for kind in('missing_native_field','changed_own_ID','changed_actual_health'):
   changed=list(after)
   if kind=='missing_native_field':changed.pop(index)
   elif kind=='changed_own_ID':changed[index]=changed[index].replace('human_id='+str(identity),'human_id=1',1)
   else:changed[index]=re.sub(r' health=(\d+),',lambda m:' health='+str(int(m[1])-1)+',',changed[index],count=1)
   need(changed!=after,'Non-vacuous exact prefix control')
   try:exact(before,changed)
   except ValueError as error:need('Entire pre-Shao native chronology'in str(error),'Specific prefix rejection');negatives.append(kind)
   else:raise ValueError('Changed true native chronology accepted')
  exact(before,after)
  transition=next(r for r in rows if r['tag']=='STAGE'and r['stage']==16);kintaro=earned(rows,15,side,identity,transition)
  fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16}
  actions=[r for r in rows if r['tag']=='BOSS_ACTION'and r['stage']==16]
  inputs=defaultdict(set)
  for r in rows:
   if r['tag']=='INPUT'and r['frame']in fields:inputs[r['frame']].add(r['button'])
  need(all('Down'in inputs[frame]and inputs[frame]<=set(('Down','Block','High_Punch'))for frame in fields),'Every real stage16field uses only declared physical crouch/guard/freshHP; no hidden Up/walk command')
  plans=[r for r in rows if r['tag']=='BOSS_PLAN'and r['stage']==16]
  need(plans and all(r['move']=='shao_opening_uppercut_attempt'for r in plans),'Only actual visible-opening HP plans at Shao, no plan-only jump credited')
  owned=[r for r in ordered.classify(rows,side)if r['stage']==16];incoming=own_damage(rows,side)
  damage=defaultdict(lambda:dict(stores=0,damage=0));hurt=defaultdict(lambda:dict(stores=0,damage=0,physicalBlockHeldDamage=0))
  for r in owned:group=damage[f"nativeAction_{r['actualDamageWriterAction']:04X}"];group['stores']+=1;group['damage']+=r['damage']
  for r in incoming:group=hurt[f"nativeAction_{r['actionAtOwnDamage']:04X}"];group['stores']+=1;group['damage']+=r['damage'];group['physicalBlockHeldDamage']+=r['damage']if r['physicalBlockHeld']else 0
  starts=[r for r in rows if r['tag']=='ENDING_START'];completed=[r for r in rows if r['tag']=='ENDING_COMPLETED']
  shao_match=earned(rows,16,side,identity,starts[0])if starts else None
  need(proof['unassisted_clear_proven']==bool(shao_match and completed),'Only actual earned boss match plus own ending/return is a campaign clear')
  cases[case]=dict(exactPreShaoNativeRecords=len(before),onlyPolicyLabelsNormalized=True,rejectedSpecificPrefixCounterexamples=negatives,
   actualKintaroMatchClear=kintaro,actualKintaroRoundWins=sum(r['tag']=='WIN'and r['slot']==side and r['stage']==15 for r in rows),
   actualShaoRoundWins=sum(r['tag']=='WIN'and r['slot']==side and r['stage']==16 for r in rows),actualShaoMatchClear=shao_match,
   actualEndingStarts=len(starts),actualEndingCompletions=len(completed),actualFullNativeCampaignAndReturnPath=proof['unassisted_clear_proven'],
   actualStage16PhysicalFields=len(fields),actualShaoUppercutPlans=len(plans),actualShaoHuman107Assignments=sum(r['after']==0x107 for r in actions),
   actualShaoHorizontalJumpAssignments=sum(r['after']==0x308 for r in actions),actualShaoCrouchExit301Assignments=sum(r['after']==0x301 for r in actions),
   actualShaoOwnedDamage=sum(r['damage']for r in owned),actualShaoIncomingDamage=sum(r['damage']for r in incoming),
   actualShaoOwnedDamageByActualAction=dict(damage),actualShaoIncomingDamageByActualAction=dict(hurt),
   originalHuman107Assignments=book['originalHuman107Assignments'],ownBossUppercutDamage=book['ownBossUppercutDamage'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=27,fullEndingArtAudioAcceptance=False)
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullEndingArtAudioAcceptance=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable exact crouch-wait progress proof')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
