"""Full original scope, actual both-slot task/sprite teardown and palette defect.
Guest ROM equality is not proof of unmodified native execution where the
compiled CPU hook changes registers. No palette cleanup or release promotion.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2725_current_friendship_p2_render_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2742_current_friendship_palette_router_full_scope_checkpoint'
def need(ok,label):
 if not ok:raise ValueError(label)
def save():
 prior=json.loads(PREVIOUS.read_text())
 need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and len(prior['remaining'])==5 and len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],'Entire original unfinished port scope retained')
 path=ROOT/'audit_v2740_current_friendship_palette_router_checked/report.json';report=json.loads(path.read_text())
 need(report['passed'] and report['actualNativeTaskAndSpriteReclamationBothSlotsAccepted'] and report['actualPaletteReplaySnapshots']==3055 and report['actualPaletteStoresReplayed']==656 and report['rejectedActualPaletteTaskAndRouterCounterexamples']==17 and report['legitimatePaletteMisclassifiedByCompiledHostHookConfirmed'] and report['nativePaletteOwnershipFixRequired'] and report['guestROMEqualityDoesNotProveUnmodifiedNativeExecution'] and not report['currentBubblePaletteOwnershipAndTeardownAccepted'] and not report['gameChanged'] and not report['fullPortAcceptance'],'Actual source/stack/register-traced palette defect with independently verified both-slot native task/sprite reclamation')
 old=(ROOT/'tools/verify_current_friendship_palette_router_v2737.py').read_text();new=(ROOT/'tools/verify_current_friendship_palette_router_v2739.py').read_text()
 expected=old.replace("OUT=ROOT/'audit_v2738_current_friendship_palette_router_checked'","OUT=ROOT/'audit_v2740_current_friendship_palette_router_checked'")
 expected=expected.replace("('missing_actual_table_store',first_store,'drop',None,'Each original palette store matches previous')","('missing_actual_table_store',first_store,'drop',None,'Every actual complete palette snapshot')")
 first=new.index(" failed=ROOT/'audit_v2738_");last=new.index(' frozen=ROOT/life.native.scene.current.NAME/',first)
 restored=new[:first]+new[last:]
 need(expected==restored,'Only actual correct omitted-store counterexample rejection label, new output leaf and retained failure pins changed; all original palette/lifecycle/source/path checks retained')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 for file,wanted in report['inputHashes'].items():
  need(file not in pins or pins[file]==wanted,'Consistent actual full-goal dependency '+file);pins[file]=wanted
 pins[str(path)]=launch.sha(path);pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 print('Revalidating entire preserved/current full-goal graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4) as pool:
  for index,((file,wanted),actual) in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed actual full-goal dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 cases=report['cases']
 need(cases['1']['actualNativeTaskReturnFrame']==4412 and cases['1']['actualSpriteResetFrame']==cases['1']['actualSpriteFreeMembershipFrame']==4420 and cases['1']['actualSpriteReuseFrame']==4436 and cases['2']['actualNativeTaskReturnFrame']==4365 and cases['2']['actualSpriteResetFrame']==cases['2']['actualSpriteReuseFrame']==4373,'Actual source-specific independent child task/sprite reclamation routes, not a forced same-field reuse assumption')
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='progress: actual P2 rendering/intermediate shadows and bounded bubble task return/sprite reuse checked; full original scope checkpoint saved, both-slot palette captures confirmed live',
  thisGoalTurnClassification='progress: both actual palette captures and smaller instruction trace completed unassisted. All 3055 complete palette tables replayed from single baselines through 656 real stores; all 454 native increments and 102 releases checked. P1 actual auxiliary task return, pool-free membership and later allocator reuse proven. Actual compiled CPU hook misclassifies legitimate FECDF710 bubble palette, substitutes stock row zero FFADBBD0 and leaves reference held into next screen; actual stack/register trace proves host rewrite despite unchanged guest instructions. Seventeen actual palette/task/router corruptions rejected. Wrong omitted-store error label retained/corrected without editing original executed source/captures. No playable/build/public-setting changes.',
  currentKanoFriendshipBothSlotsNativeAuxiliaryTaskReturnAndSpriteReclaimAccepted=True,currentKanoFriendshipBothSlotsLifecycleCases=cases,currentFriendshipPaletteRouterCauseReport=str(path),
  currentKanoFriendshipCompletePaletteTableReplayAccepted=True,currentKanoFriendshipActualPaletteReplaySnapshots=3055,currentKanoFriendshipActualPaletteStoresReplayed=656,currentKanoFriendshipPaletteTaskRouterSpecificCounterexamples=17,
  currentKanoFriendshipActualCompiledPaletteRouterDefectConfirmed=True,currentKanoFriendshipPaletteSourceOwnershipAccepted=False,currentKanoFriendshipPaletteReferenceCleanupAccepted=False,
  currentFriendshipGuestROMEqualityDoesNotProveUnmodifiedNativeExecution=True,currentFriendshipChildObjectCleanupAccepted=False,currentFriendshipCompleteSceneRasterShadowAudioAccepted=False,
  newConfirmedGameIssues=[dict(feature='Kano Friendship bubble palette ownership',compiledCause='CPU imported-root fallback at FF80D3C0 rewrites legitimate FECDF710 palette to stock auxiliary-ID-zero palette FFADBBD0 in both execution/debug paths',actualAssignedBank=4,actualHeldReferenceIntoNextScreen=1,provenSlots=[1,2],ownershipAndTeardownAcceptance=False)],
  currentFriendshipChildLifecycleAcceptanceScope='Kano, both slots, cross-character victims and one arena. Independent actual auxiliary task free-list return and sprite native reset/free membership/reallocation verified, including P1 delayed allocator reuse. Palette source identity and reference cleanup contradicted by actual current execution and remain failed. Not every child/effect/arena/victim/finisher.',
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='Fix actual bubble palette ownership in a fresh source-bound candidate without disabling imported-frame/null-sentinel protections, changing true IDs or disturbing working playable build. Give legitimate bubble palette an independently owned native record/bank and verify natural reference teardown through next screen/repeated matches; confirm exact art/colors/native fades and both-slot cleanup. Revalidate affected move/morph/selection/ladder/shaded-name/ordinary-combat regressions before changing launcher/release. All original stage/victim/mirror/arena/CPU/repeated/KO/overlap/other-finisher/secret/cinematic/natural full Shao matches/own endings/final integration/cleanup/release gates remain.',inputHashes=pins)
 return prior
if __name__=='__main__':
 need(not OUT.exists(),'Immutable actual full original-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(goalStatus=r['goalStatus'],actualFilePins=len(r['inputHashes']),nativeChildTaskAndSpriteReclamationBothSlotsAccepted=True,paletteOwnershipAndReferenceCleanupAccepted=False,actualPaletteDefectConfirmed=True,actualShaoMatchClears=0,actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,gameChanged=False),indent=2),flush=True)
