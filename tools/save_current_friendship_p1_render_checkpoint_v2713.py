"""Full original port scope with bounded current P1 Friendship rendering proof.
No player-two, child freelist, other arenas/victims/finishers, boss matches,
endings, final integration or finished-release gate is silently accepted.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2701_current_friendship_shadow_stock_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2714_current_friendship_p1_render_full_scope_checkpoint'
def need(ok,label):
 if not ok:raise ValueError(label)
def save():
 prior=json.loads(PREVIOUS.read_text())
 need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and len(prior['remaining'])>=5 and len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],'Entire original unfinished goal remains intact')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 def include(relative):
  path=ROOT/relative;report=json.loads(path.read_text());need(report['passed'] and not report['fullPortAcceptance'],'Actual scoped positive evidence '+relative)
  for file,wanted in report['inputHashes'].items():
   need(file not in pins or pins[file]==wanted,'Consistent actual full-goal dependency '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);return report,str(path)
 boundary,boundary_path=include('audit_v2712_friendship_render_scaling_boundary_checked/report.json')
 need(boundary['onlyExistingSourceVerifiedScalingAndSourceBindingAdded'] and boundary['allOriginalChecksRetained'] and boundary['independentScaleModeFlipCasesRepeated']==108 and boundary['exactCompressedUnitScaleRegressionsRepeated']==16 and boundary['entirePriorScreenshotsByteIdentical']>600 and boundary['executedSourcesAndCapturesNeverEdited'] and not boundary['gameChanged'],'Exact preserved original model limitation, 124 repeated source controls and every original screenshot unchanged')
 cases={}
 for fighter in ('kano','sonya'):
  render,path=include(f'audit_v2710_current_{fighter}_friendship_scaled_render_p1_diagnostic/report.json')
  need(render['fighter']==fighter and render['side']==1 and render['physicalInputAndNativeChronologyUnchanged'] and render['wholeActualGuestAndPayloadReconstructed'] and render['allActualGraphicsBuffersROMBound'] and render['actualConsecutiveScanouts']==1600 and render['actualBoundPixels']==162560000 and render['fullDrawingAndContinuousErasureAccepted'] and render['heldOriginalScanouts']==63 and len(render['actualRenderedPixelCounterexamples'])==1 and not render['gameChanged'] and not render['childObjectCleanupAccepted'] and not render['completeSceneRasterShadowAudioAccepted'],'Actual P1 full source-bound drawing/erasure and unaccepted broad scene/child boundaries')
  drawing=render['diagnostics']['drawing'];erase=render['diagnostics']['continuousErasure']
  need(drawing['passed'] and drawing['frames']==1537 and all(row['vram_mismatches']==row['displayed_mismatches']==row['shadow_mismatches']==0 for row in drawing['records']) and erase['passed'] and erase['continuousExactFlips']==1537 and erase['oneInitialBaseOnly'] and not erase['laterBuffersUsedAsAnchors'],'Every actual native drawing/erase pass exact without per-frame anchor substitution')
  rows,rows_path=include(f'audit_v2708_current_{fighter}_friendship_shadow_rows_p1_checked/report.json')
  need(rows['fighter']==fighter and rows['side']==1 and rows['originalSourcePoseCacheAndAllIntermediateRowsAccepted'] and rows['rejectedSpecificCounterexamples']==6 and rows['finalUnmodifiedControlPassed'] and not rows['renderedSceneAccepted'] and not rows['absoluteShadowGeometryAccepted'] and not rows['childObjectCleanupAccepted'],'Complete signed source-scanner row sequence separately accepted; absolute geometry and child lifecycle remain open')
  old,old_path=include(f'audit_v2706_current_{fighter}_friendship_full_render_p1_diagnostic/report.json')
  need(not old['fullDrawingAndContinuousErasureAccepted'] and all(not value['passed'] for value in old['diagnostics'].values()),'Original unit-only renderer remains incomplete, not promoted or edited')
  observed=boundary['cases'][fighter]
  need(observed['fullDrawingAndContinuousErasureAccepted'] and observed['sourceExactBlackShadowFrames']>=10 and observed['noBubblePublicationAfterPhysicalRetirement'] and not observed['completeChildFreelistAndProcessTeardownAccepted'],'Actual rendered black shadows and whole-list publication cleanup, not complete child memory/process teardown')
  cases[fighter]=dict(renderReport=path,intermediateRowsReport=rows_path,originalIncompleteDiagnostic=old_path,
   consecutiveScanouts=1600,sourceExactPixels=162560000,sourceExactDrawingPasses=1537,heldScanouts=63,
   continuousNativeShiftTransfers=erase['nativeShiftTransfers'],intermediateShadowCopies=rows['checkedCopies'],intermediateShadowComponents=rows['components'],
   sourceExactBlackShadowFrames=observed['sourceExactBlackShadowFrames'],actualBubblePublications=observed['actualBubblePublications'],lastActualBubblePublication=observed['lastActualBubblePublication'],
   rejectedSpecificRowCounterexamples=6,rejectedSpecificRenderedPixelCounterexamples=1,fullChildFreelistAndProcessTeardownAccepted=False)
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 print('Revalidating entire preserved/current full-goal graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4) as pool:
  for index,((file,wanted),actual) in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed actual full-goal dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: user-requested status response only; existing current results inspected before next rendering work',
  thisGoalTurnClassification='progress: actual unchanged-build physical Kano/Sonya P1 Friendships reconstructed through 3200 consecutive scanouts/325120000 pixels, 3074 complete native drawing/erase passes and 126 original held frames. Complete intermediate shadow sources/pose caches and black rendered pens checked; 12 actual row and two actual pixel corruptions rejected. Original unit-only zoom limitation retained, exact original scaling extension and 124 unit controls repeated, every old screenshot unchanged. No gameplay/build/public setting changes; all original unfinished gates intact.',
  currentFriendshipP1RenderCases=cases,currentFriendshipP1ScalingBoundaryReport=boundary_path,
  currentFriendshipP1SourceExactConsecutiveRasterAndContinuousErasureAccepted=True,currentFriendshipP1SourceExactRenderedNativeBlackShadowsAccepted=True,
  currentFriendshipP1OriginalIntermediateShadowRowsAccepted=True,currentFriendshipP1BubbleNoPublicationAfterPhysicalRetirementAccepted=True,
  currentFriendshipP1RenderedScanouts=3200,currentFriendshipP1SourceExactRenderedPixels=325120000,currentFriendshipP1SourceExactDrawingPasses=3074,
  currentFriendshipP1RenderAndRowSpecificCounterexamples=14,currentFriendshipP1RepeatedIndependentScalingControls=124,
  currentFriendshipRenderAcceptanceScope='Kano/Sonya player one, cross-character victims, one native arena plus actual native next-screen transition. Source-exact complete DMA/CPU/shift clear/VRAM/palette/rendered pixels from one initial base. Complete intermediate shadow sources/cadence and black rendered pens. Original stock scheduling comparison retained separately in both slots. Not P2 full rendering, absolute artistic shadow geometry, full child freelist/process lifecycle, other arenas/victims/mirrors or all finishers.',
  currentFriendshipCompleteSceneRasterShadowAudioAccepted=False,currentFriendshipChildObjectCleanupAccepted=False,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='Repeat full Friendship source/raster/continuous-erase/intermediate-row/black-shadow checks in P2; verify actual bubble unlink/freelist and owning process teardown, plus broader stock scene/victims/mirrors/arenas. Full natural Shao match clears and own ending art/audio/return remain both fighters/both slots. Retain all original move-phase/arena/CPU/repeated/KO/overlap/other-finisher/victim/morph/secret/cinematic/final integrated UI/ladder/names/audio/finished release gates. Protect historical native dependencies.',inputHashes=pins)
 return prior
if __name__=='__main__':
 need(not OUT.exists(),'Immutable complete original-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=r['goalStatus'],actualFilePins=len(r['inputHashes']),newP1RenderedScanouts=3200,sourceExactPixels=325120000,actualShaoMatchClears=r['currentRealShaoKahnMatchClears'],actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,gameChanged=False),indent=2),flush=True)
