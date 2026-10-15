"""Retain the entire original port scope with bounded P2 Friendship evidence.
No whole-port, boss-match, ending, complete auxiliary/palette lifecycle,
all-finisher/victim/arena, final integrated regression or release acceptance.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2714_current_friendship_p1_render_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2725_current_friendship_p2_render_full_scope_checkpoint'
def need(ok,label):
 if not ok:raise ValueError(label)
def correction_sources():
 old=(ROOT/'tools/inspect_current_friendship_lifecycle_v2717.py').read_text()
 new=(ROOT/'tools/inspect_current_friendship_lifecycle_v2722.py').read_text()
 constants='\nPOOL_FIRST,POOL_STRIDE,POOL_COUNT=0x0102d6f0,0x210,0x166\nPOOL_END=POOL_FIRST+POOL_STRIDE*POOL_COUNT'
 restored=new.replace(constants,'')
 start=restored.index('def pool_nodes(row):');end=restored.index('def parse(path):',start)
 restored=restored[:start]+restored[end:]
 restored=restored.replace("groups={key:pool_nodes(row) if key=='freeObjects' else nodes(row,key) for key in LISTS}","groups={key:nodes(row,key) for key in LISTS}")
 restored=restored.replace("    if key=='freeObjects':continue\n",'')
 restored=restored.replace("pool_nodes(before[0])[0]==object and pool_nodes(done[0])==pool_nodes(before[0])[1:]","nodes(before[0],'freeObjects')[0]==object and nodes(done[0],'freeObjects')==nodes(before[0],'freeObjects')[1:]")
 restored=restored.replace("objectFree=object in pool_nodes(row)","objectFree=object in nodes(row,'freeObjects')")
 restored=restored.replace('((0xff8087b0,0xff808a20),(0xff83f0a0,0xff83f200),(0xff840310,0xff840450),(0xff83ae20,0xff83b3f0)','((0xff83ae20,0xff83b3f0)')
 first=restored.index(" failed=ROOT/f'audit_v2723_");last=restored.index(" for path in folder.rglob('*'):",first)
 restored=restored[:first]+restored[last:]
 need(restored==old,'Only source-bounded free-pool interpretation, original extra source intervals and retained failed-report pins changed; all prior lifecycle/identity/control/allocation checks retained')
 rows_old=(ROOT/'tools/verify_current_friendship_shadow_rows_v2707.py').read_text()
 rows_new=(ROOT/'tools/verify_current_friendship_shadow_rows_v2720.py').read_text()
 need(rows_old.replace('audit_v2706_current_{fighter}_friendship_full_render_p{side}_diagnostic/report.json','audit_v2719_current_{fighter}_friendship_lifecycle_render_p{side}_diagnostic/report.json')==rows_new,'All original intermediate-row and counterexample checks unchanged; actual P2 full-render proof path only')
def save():
 prior=json.loads(PREVIOUS.read_text())
 need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and len(prior['remaining'])==5 and len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],'Entire original unfinished goal remains intact')
 correction_sources()
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 def include(relative):
  path=ROOT/relative;r=json.loads(path.read_text());need(r['passed'] and not r['fullPortAcceptance'],'Actual scoped evidence '+relative)
  for file,wanted in r['inputHashes'].items():
   need(file not in pins or pins[file]==wanted,'Consistent actual full-goal dependency '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);return r,str(path)
 boundary,path=include('audit_v2728_current_friendship_p2_lifecycle_boundary_checked/report.json')
 need(boundary['completeActualP2RenderAndContinuousErasureAccepted'] and boundary['originalP2IntermediateShadowRowsAndBlackRenderedPensAccepted'] and boundary['kanoP2NativeAuxiliaryTaskReturnAndSpriteReuseAccepted'] and boundary['rejectedActualLifecycleCounterexamples']==12 and boundary['entirePriorP2ScreenshotsByteIdentical']>600 and boundary['executedSourcesCapturesAndFailuresRetained'] and not boundary['gameChanged'] and not boundary['fullChildLifecycleBothSlotsAccepted'],'Actual P2 render/shadow/old screenshot controls and bounded native auxiliary return/reuse; broad lifecycle remains open')
 cases={}
 for fighter in ('kano','sonya'):
  render,render_path=include(f'audit_v2719_current_{fighter}_friendship_lifecycle_render_p2_diagnostic/report.json')
  need(render['fighter']==fighter and render['side']==2 and render['physicalInputAndNativeChronologyUnchanged'] and render['wholeActualGuestAndPayloadReconstructed'] and render['allActualGraphicsBuffersROMBound'] and render['actualConsecutiveScanouts']==1600 and render['actualBoundPixels']==162560000 and render['fullDrawingAndContinuousErasureAccepted'] and render['heldOriginalScanouts']==63 and len(render['actualRenderedPixelCounterexamples'])==1 and not render['childObjectCleanupAccepted'] and not render['completeSceneRasterShadowAudioAccepted'],'All actual P2 source-bound rendered scanouts and broad boundaries')
  drawing=render['diagnostics']['drawing'];erase=render['diagnostics']['continuousErasure']
  need(drawing['passed'] and drawing['frames']==1537 and all(row['vram_mismatches']==row['displayed_mismatches']==row['shadow_mismatches']==0 for row in drawing['records']) and erase['passed'] and erase['continuousExactFlips']==1537 and erase['oneInitialBaseOnly'] and not erase['laterBuffersUsedAsAnchors'],'Every actual complete P2 drawing/erase pass exact from one initial base')
  shadow,shadow_path=include(f'audit_v2721_current_{fighter}_friendship_shadow_rows_p2_checked/report.json')
  need(shadow['fighter']==fighter and shadow['side']==2 and shadow['originalSourcePoseCacheAndAllIntermediateRowsAccepted'] and shadow['rejectedSpecificCounterexamples']==6 and shadow['finalUnmodifiedControlPassed'] and not shadow['absoluteShadowGeometryAccepted'],'Every actual original P2 intermediate shadow row accepted, not universal artistic geometry')
  diagnostic,diagnostic_path=include(f'audit_v2726_current_{fighter}_friendship_bounded_lifecycle_p2_diagnostic/report.json')
  need(diagnostic['originalFailedDiagnosticRetained'] and diagnostic['originalFixedStrideSpritePoolBounded'] and not diagnostic['unboundedSpriteFreeListIntegrityAccepted'] and diagnostic['control']==render['control'],'Actual original pool-bound correction, unsupported unbounded traversal retained')
  observed=boundary['cases'][fighter]
  need(observed['sourceExactBlackShadowFrames']>=10 and observed['noBubblePublicationAfterPhysicalRetirement'] and observed['allQueuePublicationsAfterRetirement']>1000,'Actual black raster shadows and whole native renderer through scene transition')
  cases[fighter]=dict(observed,renderReport=render_path,shadowRowsReport=shadow_path,lifecycleDiagnostic=diagnostic_path,nativeShiftTransfers=erase['nativeShiftTransfers'],rejectedActualRenderedPixelCounterexamples=1,rejectedActualIntermediateRowCounterexamples=6)
  if fighter=='kano':need(observed['nativeTaskReturnAndSpriteReuseAccepted'] and observed['taskReturnFrame']<observed['spriteReuseFrame']==render['control']['actualPointerRetirement'] and not observed['paletteLifetimeAccepted'],'Independent actual auxiliary task sweep and sprite allocation reuse, not palette-lifetime proof')
 for source in ('tools/inspect_current_friendship_lifecycle_v2717.py','tools/inspect_current_friendship_lifecycle_v2722.py','tools/verify_current_friendship_shadow_rows_v2707.py','tools/verify_current_friendship_shadow_rows_v2720.py'):
  file=str(ROOT/source);actual=launch.sha(file);need(file not in pins or pins[file]==actual,'Correction source unchanged '+file);pins[file]=actual
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 print('Revalidating entire preserved/current full-goal graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4) as pool:
  for index,((file,wanted),actual) in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed actual full-goal dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: user-requested status response only; existing latest checkpoint inspected before continuation',
  thisGoalTurnClassification='progress: both current physical P2 Friendship captures independently source-reconstructed through 3200 consecutive scanouts/325120000 pixels and 3074 drawing/erase passes. Complete shadow rows and rendered black pens checked. Actual Kano auxiliary task returns through original masked sweep and sprite address is reclaimed/reallocated by original next-screen allocator. Original unsupported zero-terminated free-list diagnostic retained, exact source-bounded correction verified. Twelve real lifecycle, twelve intermediate row and two rendered-pixel corruptions rejected. No gameplay/build/public setting changes; full original scope retained.',
  currentFriendshipP2RenderCases=cases,currentFriendshipP2RenderLifecycleBoundaryReport=path,
  currentFriendshipP2SourceExactConsecutiveRasterAndContinuousErasureAccepted=True,currentFriendshipP2OriginalIntermediateShadowRowsAccepted=True,currentFriendshipP2SourceExactRenderedNativeBlackShadowsAccepted=True,
  currentFriendshipP2RenderedScanouts=3200,currentFriendshipP2SourceExactRenderedPixels=325120000,currentFriendshipP2SourceExactDrawingPasses=3074,currentFriendshipP2RenderAndRowSpecificCounterexamples=14,currentFriendshipP2ActualLifecycleCounterexamples=12,
  currentKanoFriendshipP2NativeAuxiliaryTaskReturnAndSpriteReuseAccepted=True,currentFriendshipP2BubbleNoPublicationAfterPhysicalRetirementAccepted=True,
  currentFriendshipBothSlotsSourceExactConsecutiveRasterAndContinuousErasureAccepted=True,currentFriendshipBothSlotsOriginalIntermediateShadowRowsAndBlackRenderedPensAccepted=True,currentFriendshipBothSlotsRenderedScanouts=6400,currentFriendshipBothSlotsSourceExactRenderedPixels=650240000,
  currentFriendshipP2RenderAcceptanceScope='Both new fighters in player two, cross-character victims, one native arena and real next-screen transition. Exact full DMA/shift/VRAM/palette/rendered pixels from one initial base. Complete source-derived shadow rows and black pens. Kano auxiliary task actual free-list return and sprite actual allocator reuse accepted in P2 only. Not palette lifetime, P1 child task teardown, all auxiliary effects or other arenas/victims/mirrors/finishers.',
  currentFriendshipCompleteSceneRasterShadowAudioAccepted=False,currentFriendshipChildObjectCleanupAccepted=False,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='Verify P1 actual bubble task allocation/free-list return and native sprite reclaim/reuse plus palette lifetime; extend stock/new native Friendship scenes across victims/mirrors/arenas. Full natural Shao match clears and own ending art/audio/return remain both fighters/both slots. Keep all original move-phase/arena/CPU/repeated/KO/overlap/other-finisher/victim/morph/secret/cinematic/final integrated UI/ladder/names/audio/finished-release gates. Protect historical dependencies.',inputHashes=pins)
 return prior
if __name__=='__main__':
 need(not OUT.exists(),'Immutable entire original-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=r['goalStatus'],actualFilePins=len(r['inputHashes']),newP2RenderedScanouts=3200,sourceExactPixels=325120000,actualShaoMatchClears=r['currentRealShaoKahnMatchClears'],actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,gameChanged=False),indent=2),flush=True)
