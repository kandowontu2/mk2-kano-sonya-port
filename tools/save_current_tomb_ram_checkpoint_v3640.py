"""Preserve full objective and actual current Tomb render/observer evidence."""
import ctypes
import json
import subprocess
from pathlib import Path

import run_current_tomb_ram_v3633 as render
import verify_current_tomb_ram_faults_v3636 as faults
import verify_current_tomb_observer_equivalence_v3638 as comparison

ROOT,need,sha=render.ROOT,render.need,render.sha
PREVIOUS=ROOT/'audit_v3623_current_tomb_drop_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3641_current_tomb_ram_full_scope_checkpoint'


def allocated(file):
    api=ctypes.windll.kernel32.GetCompressedFileSizeW
    api.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong)];api.restype=ctypes.c_ulong
    high=ctypes.c_ulong();low=api(str(file.resolve()),ctypes.byref(high))
    need(low!=0xffffffff,'Actual allocated bytes for exact diagnostic file')
    return (high.value<<32)|low


def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining'])
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and
         not state['finishedRelease']and state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted'],
         'Full original scope and actual completed P1 campaigns preserved')
    fresh={}
    def pin(file,wanted=None):
        key=str(Path(file).resolve());value=sha(file)
        need(wanted is None or wanted==value,'Actual relevant source/evidence/public bytes unchanged')
        need(key not in fresh or fresh[key]==value,'Consistent relevant evidence')
        need(key not in state['inputHashes']or state['inputHashes'][key]==value,'Never relabel inherited evidence')
        fresh[key]=value
    path=render.OUT/'report.json';proof=json.loads(path.read_text())
    need(proof['passed']and proof['currentActualEarnedKanoP1TombWholeSceneRenderShadowEraseAccepted']and
         proof['sampledFrames']==537 and proof['exactRGBPixels']==54559200 and
         proof['continuousExactPreBuffers']==proof['continuousExactFlips']==507 and
         proof['continuouslyExactHeldScanouts']==30 and proof['oneInitialBaseOnly']and
         proof['laterTargetVRAMNeverUsedAsAnchors']and proof['nativeShiftLoads']==proof['nativeShiftFills']==503
         and proof['nativeShiftTransfers']==63881 and proof['fullPhysicalPaletteChecks']==2159 and
         proof['nativeScene']['nativeDrop']and proof['nativeScene']['actualNativeRandomValue']==7 and
         proof['nativeScene']['nativeShadowCopies']==3987 and len(proof['rejectedActualPixelTargetFaults'])==2 and
         not proof['stageAudioFidelityAccepted']and not proof['allVictimMirrorBranchAudioAcceptance']and
         not proof['fullPortAcceptance'],'Actual whole source/replay/shadow/erase scene, not stage audio/universal acceptance')
    terminal=json.loads((render.CASE/'result.json').read_text())
    need(terminal['exit_code']==0 and terminal['captureCompleted']and terminal['modelExactFields']==537
         and terminal['observedRGBFields']==537 and not terminal['modelErrors']and
         terminal['guest_writes']==0 and not terminal['cheats_enabled']and terminal['diagnosticGuestDumps']==1,
         'Actual current completed native child and persisted checked metadata')
    fault_path=faults.OUT/'report.json';fault=json.loads(fault_path.read_text())
    need(fault['passed']and len(fault['qualifiedActualMetadataFaults'])==6 and
         fault['positiveContractRestoredAfterEveryFault']and fault['actualNativeShadowCopies']==3987,
         'Six qualified actual sprite/ground/projection/shadow faults, restored positives')
    comparison_path=comparison.OUT/'report.json';equivalence=json.loads(comparison_path.read_text())
    need(equivalence['passed']and equivalence['exactActualNativeControlAndProvenanceRecords']==8811 and
         equivalence['exactCurrentHeavyAndLightVisibleFields']==537 and
         equivalence['qualifiedComparisonFaults']==2 and len(equivalence['transport']['qualifiedFaults'])==4 and
         not equivalence['fullHiddenWorldStateObserverEquivalenceAccepted']and
         not equivalence['universalHookNoninterferenceAccepted'],
         'Bounded actual recorded states/visible fields, not universal hidden-state noninterference')
    for file,value in ((path,proof),(fault_path,fault),(comparison_path,equivalence)):
        pin(file)
        for source,wanted in value['inputHashes'].items():pin(source,wanted)
    files=[file for file in render.CASE.rglob('*')if file.is_file()]
    need(len(files)==14 and not any(file.suffix.lower()in('.exe','.wav','.png','.jpg','.bmp')for file in files)
         and len([file for file in files if file.name=='guest_maincpu.bin'])==1 and
         not any(file.name.startswith(('display_pre_','display_vram_','display_palette_'))for file in files),
         'Only compressed metadata/source logs and one allowed guest diagnostic dump, no bulk captures')
    storage=dict(captureLeaves=1,files=len(files),logicalBytes=sum(file.stat().st_size for file in files),
                 allocatedBytes=sum(allocated(file)for file in files),newPlayableBuilds=0,
                 rawPixelImageVRAMAudioCopies=0,diagnosticGuestDumps=1)
    for file in files:pin(file)
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        file=ROOT/relative;pin(file,state['inputHashes'][str(file.resolve())])
    for relative in ('tools/current_tomb_ram_model_v3625.py','tools/run_current_tomb_ram_v3626.py',
                     'tools/run_current_tomb_ram_v3630.py','mk2ks_native_tomb_ram_v3624.lua'):
        pin(ROOT/relative)
    pin(PREVIOUS);pin(__file__)
    state['inputHashes']=fresh
    state['currentScopeEvidenceAudit']['group1']=(
        '3635now independently source-replays actual3172 KanoP1->Sonya18 native Tomb random7drop: '
        'whole initialized guest/actual compiled inputs, original physical controls/earned damage/native '
        'branch/fall/own-floor/retirement,2159original composite/cache/camera/FIFO projections and full '
        'palettes,1056source-bound graphics streams,3987native compressed shadow copies,537whole RGB '
        'fields/54,559,200pixels,507pre/fliptargets+30heldscanouts,oneinitialbase/503native clears/'
        '63,881shifttransfers. No later VRAM anchors, no PNG/WAV/VRAM dumps or new build. '
        '3637rejects6actual sprite-offset/floor/projection/shadow-source/black-pen/row-coordinate faults; '
        'live replayer rejects2actual VRAM/RGB bit faults.3639matches8,811actual native/control/provenance '
        'records exactly to completed no-hook current3611 and all537visible RGB digests to lightweight '
        'palette/reset3598;2comparison faults/4qualified native-byte transport faults. This bounds recorded '
        'states/visible scene, not all hidden-world-state/universal hook equivalence. Original rejected '
        'held-oracle3603/3607/3612 remain failed,3619physics accepted. Stage-audio fidelity, current other '
        'physical slot/character native Tomb/Pit/stock/new victim/mirror branches remain uncompleted gates.')
    state.update(previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten historical map.'),
        previousGoalTurnClassification='no progress: preceding acknowledgement/rendering-source inspection produced no new gate or live job. Revalidated actual3623checkpoint/current compiled and executable/payload state, then took the available source-replay action.',
        thisGoalTurnClassification='progress: current source/retained native renderer inspected before edits; no game edits. RAM sink-only wrapper preserves entire2062observer and original3594physical controller.3626positive control fails missing entryhex schema;3630positive fails incorrect3-vs-actual4pretarget count; both executed sources retained. Fresh3629schema mirrors original1231field schema;3633uses actual4pretargets/source-perfect3nativefields and original bytes. One actual3172native capture3634terminal0 naturally takes7drop;3635full source/FIFO/palette/shadow/continuousCPU/shift/DMA/heldRGB replay passes all537fields/54.56millionpixels,507pre+507fliptargets/30held,onebase/63881erase transfers.3637sixactualmetadatafaults qualify sourceart/floor/projection/shadows; live2pixel-targetfaults retained.3639all8811recorded control/native/provenance rows equal prior3611nohooks and all537RGBdigests equal3598lightobserver;2comparison/4actualnative-byte transportfaults reject as intended. Full5groups/realP1campaigns/public/retiredexclusions preserved. New1smallcompressed14filemetadata capture/1guestdump,zeroEXE/PNG/WAV/VRAMcopies; no source/game/playable/public changes.',
        current3172NativeKanoP1TombDropVisualArtShadowEraseReport=str(path),
        current3172NativeKanoP1TombDropVisualArtShadowEraseAccepted=True,
        current3172NativeKanoP1TombDropStandaloneCaptureExitCode=0,
        current3172NativeKanoP1TombDropVerifiedVisibleFields=537,
        current3172NativeKanoP1TombDropVerifiedRGBPixels=54559200,
        current3172NativeKanoP1TombDropNativeShadowCopies=3987,
        current3172NativeKanoP1TombDropQualifiedArtGroundShadowFaultReport=str(fault_path),
        current3172NativeKanoP1TombRecordedStateVisibleObserverComparisonReport=str(comparison_path),
        current3172NativeKanoP1TombHeavyObserverRecordedStatesMatchPriorNoHookCapture=True,
        current3172NativeKanoP1TombHeavyObserverVisibleFramesMatchPriorLightHookCapture=True,
        current3172NativeKanoP1TombFullHiddenWorldStateObserverEquivalenceAccepted=False,
        current3172NativeKanoP1TombDropAudioFidelityAccepted=False,
        current3172NativeKanoP1TombDropSceneVisualArtShadowEraseAudioAccepted=False,
        current3172RemainingPhysicalSlotCharacterTombPitVictimMirrorBranchAudioAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,newRuntimeCaptureLeavesThisTurn=1,
        acceptedVisibleScenarioCapturesThisTurn=1,rawPixelImageVRAMCopiesThisTurn=0,
        diagnosticGuestProgramDumpsThisTurn=1,currentTombRAMStorage=storage,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
        rejectedNewPureControlInvocations=[dict(tool=str(ROOT/'tools/run_current_tomb_ram_v3626.py'),
            terminalExitCode=1,reason='Exact original observer entry field is hexadecimal; missing schema entry rejected before any new runtime.'),
            dict(tool=str(ROOT/'tools/run_current_tomb_ram_v3630.py'),terminalExitCode=1,
            reason='Native callback already begins the next pass before snapshot:3savedflips have4actualpretargets, not3. No new runtime. Corrected fresh runner preserves all actual pretargets.')],
        nextAction='Do not repeat accepted3634/3635currentKanoP1Tomb drop rendering/3619physics/8811record comparison/537RGB comparison merely for metadata. In fresh typed RAM adapter/runner, derive winner/victim IDs by actual physical side instead of hardcoded17,18, then source-replay currentSonyaP1/P2 andKanoP2 nativeTomb with unchanged physical controls and observed original RNG outcomes, not held/drop prescription. Use3591typed finite native move/finisher/victim/branch inventory for remaining stock/new victim/mirror/Pit/stageaudio and movephase/KO/repeat/CPU gates. P1 naturalKintaro/Shao/ownstory/attract already done for both. Finish remaining finisher/cinematic/audio contexts and combinedUI/ladder/names/audio gate, dependency-aware cleanup and refreshedreleaseZIP. Keep all original5groups/public1836CMD/ZIP and retired exclusions; fullportnotdone.')
    need(state['remaining']==remaining and not state['fullPortAcceptance']and not state['finishedRelease'],
         'Original full objective/deliverables intact')
    OUT.mkdir();file=OUT/'checkpoint.json';file.write_text(json.dumps(state,indent=2)+'\n')
    before=sha(file);result=subprocess.run(['compact.exe','/C','/I','/Q',str(file)],capture_output=True,text=True)
    need(result.returncode==0 and sha(file)==before,'Lossless compact full-scope checkpoint')
    print(json.dumps(dict(saved=str(file),goalStatus='active',nativeDropVisualFields=537,
        nativeShadowCopies=3987,actualNativeStateRowsCompared=8811,freshRelevantPins=len(fresh),
        storage=storage,fullPortAcceptance=False),indent=2))


if __name__=='__main__':main()
