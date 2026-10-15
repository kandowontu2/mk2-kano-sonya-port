"""Retain full original scope with actual current Friendship audio/body evidence.
Original uncompleted gates remain intact. All dependencies are revalidated.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2666_current_friendship_restrictions_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2686_current_friendship_audio_art_full_scope_checkpoint'

def need(ok,label):
 if not ok:raise ValueError(label)

def save():
 prior=json.loads(PREVIOUS.read_text())
 need(prior['goalStatus']=='active'and not prior['fullPortAcceptance']and not prior['finishedRelease']and len(prior['currentSourceBoundBossCampaigns'])==70 and len(prior['remaining'])>=5 and prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],'Complete original unfinished goal and actual boss/ending boundaries retained')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 def include(relative):
  path=ROOT/relative;report=json.loads(path.read_text())
  need(report['passed']and not report['fullPortAcceptance'],'Actual scoped accepted new evidence '+relative)
  for file,wanted in report['inputHashes'].items():
   need(file not in pins or pins[file]==wanted,'Consistent actual old/current dependency '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path)
  return report,str(path)
 baseline,baseline_path=include('audit_v2669_current_friendship_audio_baselines_checked/report.json')
 need(baseline['samplesSettingNeverChangedGameplay']and baseline['wholeActualGuestAndPayloadReconstructed']and len(baseline['cases'])==4 and not baseline['originalPCMAndAudibleOverlapAccepted'],'Exact current native samples-on/off chronology remains separately scoped')
 audio,audio_path=include('audit_v2673_current_friendship_audio_checked/report.json')
 need(audio['originalPCMAndAudibleOverlapAccepted']and audio['currentWholeGuestAndPayloadReconstructed']and audio['all20OriginalCluckChannelsReconstructed']and audio['audibleCues']==80 and audio['audibleGroups']==28 and audio['rejectedSpecificAudioCounterexamples']==36 and len(audio['physicalRestrictions'])==8 and not audio['gameChanged']and not audio['completeSceneRasterShadowAudioAccepted'],'Exact actual original-PCM audio and independent overlap, not whole-scene acceptance')
 corrections,correction_path=include('audit_v2677_friendship_audio_verifier_correction_checked/report.json')
 need(not corrections['failedOriginalAccepted']and corrections['onlyMissingVoiceExpectedRejectionAndOutputLeafChanged']and corrections['PCMThresholdsUnchanged']and corrections['executedSourcesCapturesAndReferencesNeverEdited'],'Failed original verifier retained with exact repeated correction boundary')
 diagnostic,diagnostic_path=include('audit_v2675_current_friendship_body_pixels_diagnostic/report.json')
 need(diagnostic['diagnosticCompleted']and not diagnostic['currentAllOriginalBodyGroupsBothSlotsPixelMatched']and diagnostic['cases']['sonya_p2']['exactMatchedBodyGroups']==9,'Original actual gap-160 occluded groups remain unaccepted')
 body,body_path=include('audit_v2684_current_friendship_body_supplement_checked/report.json')
 need(body['originalBodyGroupsBothSlotsPixelAccepted']and body['bodyGroupsByCharacterSlot']==dict(kano_p1=18,kano_p2=18,sonya_p1=11,sonya_p2=11)and body['actualCommandGap']==145 and body['wholeActualGuestAndPayloadReconstructed']and body['solePhysicalRetreatDistanceChange']and body['completePreDistanceNativeChronologyExact']and body['rejectedSpecificCounterexamples']==17 and body['finalUnmodifiedControlPassed']and not body['gameChanged']and not body['completeSceneRasterShadowAudioAccepted']and not body['supplementAudiblePCMAccepted'],'Current body pixels independently covered in actual two-distance scenes; shadow/full-raster/supplement PCM gates not silently promoted')
 audio_summary={key:dict(cues=case['cues'],audibleGroups=len(case['audibleGroups']),minimumCorrelation=min(group['correlation']for group in case['audibleGroups']),
  maximumResidualPCM=max(group['residual_rms_pcm']for group in case['audibleGroups']),
  rejectedSpecificCounterexamples=len(case['PCMCorruptions'])+len(case['cueCorruptions']),finalUnmodifiedControlPassed=case['finalUnmodifiedControlPassed'])for key,case in audio['cases'].items()}
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 print('Revalidating full preserved/current proof graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed authoritative full-goal dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: user-requested status response only; actual existing evidence revalidated and next safe audio/art work resumed without restarting captures',
  thisGoalTurnClassification='progress: original hardware/reference graphs reconstructed, four unchanged-build physical Friendship mixes match all complete original variants/tails and independent overlap:80 actual cues/28groups/36 specific audio negatives. Failed original harness retained with exact expected-zero-energy rejection correction, all four controls fully repeated. Current body pixels matched Kano18/Sonya11 original groups in both slots across actual gap-160/140 scenes; original gap-160 Sonya P2 missing groups preserved. Physical supplement uses only closer retreat, earned KOs, true ID18 and native handoff.17 specific control/pixel corruptions rejected. Every original uncompleted floor-shadow/scene-raster/arena/finisher/victim/morph/secret/cinematic/ending/integrated-regression/release gate retained. Game unchanged.',
  currentFriendshipAudioBaselineReport=baseline_path,currentFriendshipOriginalAudioReport=audio_path,
  currentFriendshipAudioVerifierCorrectionReport=correction_path,currentFriendshipAudioCases=audio_summary,
  currentFriendshipOriginalPCMAudibleOverlapAccepted=True,currentFriendshipAudibleCues=80,currentFriendshipAudibleGroups=28,currentFriendshipAudioCounterexamples=36,
  currentFriendshipBodyPixelDiagnosticReport=diagnostic_path,currentFriendshipBodyPixelSupplementReport=body_path,
  currentFriendshipOriginalBodyGroupsBothSlotsPixelAccepted=True,currentFriendshipOriginalBodyGroupsBySlot=body['bodyGroupsByCharacterSlot'],
  currentFriendshipBodyPixelAcceptanceScope='One native arena, cross-character victims, actual physical gap-160 cases plus Sonya P2 gap-140 supplement. Every opaque original body pixel matches; not whole-scene raster, floor shadows, other victims/mirrors, all arenas or all finishers.',
  currentFriendshipBodySupplementCounterexamples=17,currentFriendshipCompleteSceneRasterShadowAudioAccepted=False,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='Current Friendship native cue/voice allocation and original full PCM/overlap are accepted in four samples-on/off contexts; original body groups now match both slots across the physical gap-160/140 scenes. Next verify full Friendship scene floor-shadow behavior, raster and cleanup against current native stock controls, plus broader victims/mirrors/arenas. Full natural Shao matches and own ending art/audio/return remain required for both fighters/both slots; individual Shao rounds are not full clears. Continue every original move-phase/arena/CPU/repeated/KO/overlap, other finisher/victim/morph/secret/cinematic, final integrated UI/ladder/names/audio and finished release gate. Protect required historical native dependencies.',
  inputHashes=pins)
 return prior

if __name__=='__main__':
 need(not OUT.exists(),'Immutable complete original-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=r['goalStatus'],actualFilePins=len(r['inputHashes']),acceptedBossContexts=len(r['currentSourceBoundBossCampaigns']),
  currentFriendshipOriginalBodyGroupsBySlot=r['currentFriendshipOriginalBodyGroupsBySlot'],currentFriendshipAudibleCues=80,currentFriendshipAudibleGroups=28,
  audioAndBodySpecificCounterexamples=53,actualShaoMatchClears=r['currentRealShaoKahnMatchClears'],actualEndingsAccepted=False,
  fullPortAcceptance=False,finishedRelease=False,gameChanged=False),indent=2),flush=True)
