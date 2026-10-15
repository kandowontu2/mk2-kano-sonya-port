"""Retain full original port objective and exact both-slot native crouch/jump evidence."""
import json,re,copy
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_crouch_jump_comparison_v2452 as v
ROOT=v.ROOT
PREVIOUS=ROOT/'audit_v2438_current_shao_escape_cleanup_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2460_current_native_crouch_jump_checkpoint'
def need(ok,label):
 if not ok:raise ValueError(label)
def phase(text,side):
 terminal=v.check.rows(text,'RESULT')[0]
 return [(f['frame']-terminal['command']-120,f['action'],f['y']-f['floor'],f['vy'],f['gravity'],f['flags'],f['body'],f['trail'])
  for f in v.check.rows(text,'FIELD')if f['slot']==side and terminal['command']+120<=f['frame']<terminal['recovered']]
def prove_same(actual,reference):need(actual==reference,'Exact actual crouch-exit/jump/landing native phase differs from both-slot stock reference')
def save():
 prior=json.loads(PREVIOUS.read_text());need(prior['goalStatus']=='active'and not prior['fullPortAcceptance'],'Entire original objective active')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=v.launch.sha(PREVIOUS)
 for file in('audit_v2444_current_native_crouch_exit_diagnosis/report.json','audit_v2456_current_native_crouch_jump_matrix/report.json'):
  path=ROOT/file;report=json.loads(path.read_text());need(report['passed']and not report['fullPortAcceptance'],'Accepted bounded source/control report')
  for dependency,digest in report['inputHashes'].items():
   need(dependency not in pins or pins[dependency]==digest,'Consistent carried source dependency');pins[dependency]=digest
  pins[str(path)]=v.launch.sha(path)
  if 'cases'in report and isinstance(report['cases'],list):matrix=report
 need(len(matrix['cases'])==24 and matrix['negativeControls']==288,'Complete4characters2slots3profiles and specific invalid controls')
 need(not matrix['gameModified']and not matrix['oldFailedPilotDiscarded'],'No game modification or discarded original failure')
 compared=[];negatives=[]
 for side in(1,2):
  for lead,hold in((0,3),(0,16),(12,3)):
   reference_name=f'liu_p{side}_crouch_lead{lead}_hold{hold}_away'
   reference=phase((ROOT/f'audit_v2453_current_{reference_name}/run.log').read_text(encoding='utf-8-sig'),side)
   for character in('kano','sonya'):
    name=f'{character}_p{side}_crouch_lead{lead}_hold{hold}_away'
    actual=phase((ROOT/f'audit_v2453_current_{name}/run.log').read_text(encoding='utf-8-sig'),side);prove_same(actual,reference)
    compared.append(dict(case=name,stockReference=reference_name,exactNativePhaseFields=len(actual),
     comparedFields=['relativeReleaseFrame','action','YminusOwnFloor','VY','gravity','MainFlags','body','trail']))
    for label,column,value in(('wrong action',1,0x503),('raised foot contact',2,-1),('wrong vertical velocity',3,1)):
     altered=copy.deepcopy(actual);row=list(altered[2]);row[column]=value;altered[2]=tuple(row)
     try:prove_same(altered,reference)
     except ValueError as error:
      need(str(error)=='Exact actual crouch-exit/jump/landing native phase differs from both-slot stock reference','Specific native phase corruption rejection')
      negatives.append(dict(case=name,label=label,rejected=True))
     else:raise ValueError('Native phase corruption accepted')
    prove_same(actual,reference)
 need(len(compared)==12 and len(negatives)==36,'Both true additions exactly match complete measured Liu native phases in both slots')
 stock_differences=[]
 for side in(1,2):
  for lead,hold in((0,3),(0,16),(12,3)):
   stem=f'p{side}_crouch_lead{lead}_hold{hold}_away'
   reference=phase((ROOT/f'audit_v2453_current_liu_{stem}/run.log').read_text(encoding='utf-8-sig'),side)
   actual=phase((ROOT/f'audit_v2453_current_subzero_{stem}/run.log').read_text(encoding='utf-8-sig'),side)
   need(len(actual)==len(reference),'Whole stock comparison, no dropped native field')
   differences=[dict(relativeReleaseFrame=a[0],actual=list(a),reference=list(b))for a,b in zip(actual,reference)if a!=b]
   if side==1:need(not differences,'Stock P1 full native phases actually match')
   else:
    need(differences and all(a[:6]==b[:6]and a[7:]==b[7:]and a[6]==b[6]+0x40 for a,b in zip(actual,reference)),'Stock P2 sole raw difference is retained body bit40; no dropped action/grounding/movement field')
   stock_differences.append(dict(case='subzero_'+stem,reference='liu_'+stem,completeFields=len(actual),exactRawDifferences=differences,
    bit40SourceMeaningNotCertified=True,notClaimedAsExactFullStateEquivalence=bool(differences)))
 failure_path=ROOT/'audit_v2458_current_native_crouch_jump_checkpoint_failure/report.json'
 failure=json.loads(failure_path.read_text());need(not failure['passed'],'Original failed overbroad stock full-state assertion retained')
 pins[str(failure_path)]=v.launch.sha(failure_path)
 pins[str(ROOT/'tools/save_current_native_crouch_jump_checkpoint_v2457.py')]=v.launch.sha(ROOT/'tools/save_current_native_crouch_jump_checkpoint_v2457.py')
 for case in matrix['cases']:
  name=case['name'];delayed='lead12'in name;held='hold16'in name
  need(case['nativeCommandJumpObserved']==(delayed or held),'Observed native jump outcome for declared physical profile')
  need([f-case['command']-120 for f in case['actualCrouchExitFieldFrames']]==[2,3,4,5,6,7],'Original sixfield crouch exit')
  if delayed or held:
   need(case['actualNativeJumpEntry']-case['command']-120==(14 if delayed else 9),'Exact real native jump entry timing')
   need(case['actualAirborneCommandFields']==case['native308AirborneCommandFields']==37,'Native37field horizontal jump')
  else:need(case['actualNativeJumpEntry']==-1 and case['actualAirborneCommandFields']==0,'No activation is not fabricated')
 need(sum(case['nativeCommandJumpObserved']for case in matrix['cases'])==16,'Sixteen actual jumps and eight native short-input nonactivations')
 for file in('audit_v2449_current_kano_p1_crouch_lead0_hold3_checked/report.json','audit_v2449_current_kano_p1_crouch_lead0_hold16_checked/report.json'):
  path=ROOT/file;pins[str(path)]=v.launch.sha(path)
 failed=json.loads((ROOT/'audit_v2449_current_kano_p1_crouch_lead0_hold3_checked/report.json').read_text())
 need(not failed['passed']and 'Real native forward/back walking'in failed['error'],'Original collision-related full-check failure retained unchanged')
 pins[str(Path(__file__).resolve())]=v.launch.sha(__file__)
 print('Revalidating complete carried graph and new native evidence:',len(pins),'files',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(v.launch.sha,pins)),1):
   need(actual==wanted,'Changed actual pinned dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: status-only response; latest terminal authoritative checks re-read',
  thisGoalTurnClassification='progress: original native301crouch exit proved from unchanged source and real assignment events;24cold physical comparisons of Kano17,Sonya18,Liu1,Sub8 in both human slots. Sixteen actual jumps,eight ignored early short Up presses,all native recovery/free-backwalk/Up/HP follow-ups,288specific input/state negatives and36exact Kano/Sonya versus stock-Liu phase corruptions. Stock P2 Sub mirror extra body bit40 retained separately with source meaning uncertified. Original failed collision pilot retained. No ROM/source/AI/balance/health/stage/RNG changes.',
  currentNativeCrouchExitDiagnosis=str(ROOT/'audit_v2444_current_native_crouch_exit_diagnosis/report.json'),
  currentNativeCrouchJumpMatrix=str(ROOT/'audit_v2456_current_native_crouch_jump_matrix/report.json'),
  currentNativeCrouchJumpCases=matrix['cases'],currentNativeCrouchJumpSpecificCounterexamples=288,
  currentExactStockCrouchJumpPhaseComparisons=compared,currentSpecificStockPhaseCounterexamples=negatives,currentRawSubzeroStockPhaseDifferences=stock_differences,
  currentNativeCrouchJumpConclusions=dict(native301Means='original crouch-exit reverse animation',
   immediate3fieldUp='ignored for all4truecharacters in bothslots',immediate16fieldUp='actual native jump at release+9fields',
   delayed3fieldUp='actual native jump at release+14fields after12field neutral lead',
   actualJumpFlightFields=37,selectionIDsNeverChanged=True,completeNativeFollowupVerified=True,
   earlyIgnoredUpIsNotAddedCharacterDefectInTheseFixtures=True,stockSubzeroP2BodyBit40MeaningNotCertified=True,universalCPUOrGameplayAcceptance=False),
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],
  goalStatus='active',fullPortAcceptance=False,finishedRelease=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
  nextAction='Native crouch-exit/Up timing matches actual Liu/Sub in bothslots; entire measured Kano/Sonya native phases match Liu, while extra P2 Subzero mirror bodybit40 is recorded without asserting full-state equivalence; do not change game balance or patch native input merely to make an automated controller succeed. If continuing Shao controls, use measured native301recovery/heldUp semantics and actual owned attack episodes, leaving original AI/HP/RNG/stage untouched. Continue broader all-arena move-phase art/grounding/floor-shadow/cleanup/audio and CPU/repeat/KO/overlap checks, all finishers/victims/morphs/secrets/cinematics, actual earned fullKintaro/Shao clears and own ending/attract bothcharacters/bothslots, integratedUI regression, remaining dependency-aware old-build cleanup and finishedreleaseZIP. Entire original natural-in-all-aspects objective retained.',
  inputHashes=pins)
 need(len(prior['remaining'])>=5 and prior['currentRealShaoKahnMatchClears']==0,'All original unfinished gates preserved')
 return prior
if __name__=='__main__':
 need(not OUT.exists(),'Immutable complete-scope native crouch/jump checkpoint')
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',coldCases=24,actualNativeJumps=16,ignoredNativeEarlyUp=8,
  exactAddedCharacterStockPhaseComparisons=12,specificCounterexamples=324,stockP2BodyFlagMeaningUncertified=True,gameChanged=False,finishedRelease=False),indent=2),flush=True)
