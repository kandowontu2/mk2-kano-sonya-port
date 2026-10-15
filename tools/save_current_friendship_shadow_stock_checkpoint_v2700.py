"""Preserve the entire unfinished port scope and current stock shadow evidence."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2686_current_friendship_audio_art_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2701_current_friendship_shadow_stock_full_scope_checkpoint'
def need(ok,label):
 if not ok:raise ValueError(label)
def save():
 prior=json.loads(PREVIOUS.read_text())
 need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and len(prior['remaining'])>=5 and len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],'Original full scope and unfinished natural campaign/endings retained')
 path=ROOT/'audit_v2699_current_friendship_shadow_stock_comparison_checked/report.json'
 r=json.loads(path.read_text())
 need(r['passed'] and r['currentStockAndNewCharacterShadowSchedulingMatches'] and len(r['cases'])==8 and r['actualContinuousFields']==32867 and r['actualNativeShadowCopies']==1970757 and r['actualNativeShadowComponents']==91147 and r['actualInventoryCounterexamples']==56 and r['stockComparisonCounterexamples']==25 and r['finalUnmodifiedControlPassed'],'Actual eight stock/new continuous native shadow controls')
 need(len(r['failedOriginalVerifiers'])==3 and all(not x['accepted'] for x in r['failedOriginalVerifiers']) and r['onlyOriginalScannerSemanticsAndSourceAddressingCorrected'] and r['everyFinalInventoryControlFullyRepeated'] and r['executedSourcesAndCapturedGameplayNeverEdited'],'Original failed harnesses retained and exact independently sourced correction repeated')
 need(not any(r[k] for k in ('gameChanged','fullShadowRowsOrPixelsAccepted','childObjectCleanupAccepted','completeSceneRasterShadowAudioAccepted','fullFinisherAcceptance','fullPortAcceptance')),'No rendered-row/pixel/child/full-scene or full-port acceptance inferred')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 for file,wanted in r['inputHashes'].items():
  need(file not in pins or pins[file]==wanted,'Consistent authoritative dependency '+file);pins[file]=wanted
 pins[str(path)]=launch.sha(path)
 disassembly=path.parent/'native_shadow_scanner_disassembly.txt'
 need(disassembly.read_text()==r['originalScannerDisassembly'],'Actual original scanner disassembly retained')
 pins[str(disassembly)]=launch.sha(disassembly);pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 print('Revalidating full original-scope graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4) as pool:
  for index,((file,wanted),actual) in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed actual goal dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: user-requested status reply only, current authoritative checkpoints inspected; next safe rendering verification resumed',
  thisGoalTurnClassification='progress: all eight current stock/new native shadow controls and original scanner correction evidence incorporated and entire preserved proof graph revalidated',
  currentFriendshipShadowStockComparisonReport=str(path),currentFriendshipShadowCases=r['cases'],currentFriendshipShadowScheduleAndPhysicalActorRetirementAccepted=True,
  currentFriendshipShadowContinuousFields=r['actualContinuousFields'],currentFriendshipShadowNativeCopies=r['actualNativeShadowCopies'],currentFriendshipShadowNativeComponents=r['actualNativeShadowComponents'],
  currentFriendshipShadowInventoryCounterexamples=56,currentFriendshipShadowStockComparisonCounterexamples=25,
  currentFriendshipIntermediateShadowRowsAccepted=False,currentFriendshipRenderedShadowPixelsAccepted=False,currentFriendshipChildObjectCleanupAccepted=False,
  currentFriendshipCompleteSceneRasterShadowAudioAccepted=False,
  currentFriendshipShadowAcceptanceScope='One native arena, cross-character victims, Cage/Liu/Kano/Sonya both slots. Original source-bound first/last shadow rows, copy counts and geometry; startup ages 0..9, no later native shadow commands, physical actor retirement 441 fields after common handoff. Not intermediate row sequence, rendered pixels, child-object cleanup or complete scene.',
  nextAction='Capture and independently replay full Friendship FIFO/CPU/DMA/continuous erasure and scanouts including actual native transition, rendered shadows and child retirement. Broader victims/mirrors/arenas still required. Full natural Shao match clears and own ending art/audio/return remain both fighters/both slots. All original move-phase/arena/CPU/repeated/KO/overlap/other-finisher/victim/morph/secret/cinematic/final integrated UI/ladder/names/audio/finished release gates remain intact. Protect historical native dependencies.',
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',inputHashes=pins)
 return prior
if __name__=='__main__':
 need(not OUT.exists(),'Immutable full-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=r['goalStatus'],actualFilePins=len(r['inputHashes']),stockAndNewContexts=8,continuousFields=32867,gameChanged=False,fullPortAcceptance=False,finishedRelease=False),indent=2),flush=True)
