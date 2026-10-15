"""Preserve full scope with both true characters/slots current native Tomb proof."""
import json
import subprocess
from pathlib import Path

import run_current_tomb_ram_matrix_v3648 as current
import verify_current_tomb_matrix_faults_v3652 as faults
import compact_current_tomb_logs_v3654 as storage

ROOT,need,sha=current.ROOT,current.need,current.sha
PREVIOUS=ROOT/'audit_v3641_current_tomb_ram_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3659_current_tomb_matrix_full_scope_checkpoint'


def main():
    need(not OUT.exists(),'Fresh full-scope current matrix checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining'])
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and
         not state['finishedRelease']and state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted']and
         state['current3172NativeKanoP1TombDropVisualArtShadowEraseAccepted'],
         'Full objective/P1campaigns/accepted prior currentKanoP1 retained')
    fresh={}
    def pin(file,wanted=None):
        key=str(Path(file).resolve());value=sha(file)
        need(wanted is None or wanted==value,'Actual relevant source/evidence/public logical bytes unchanged')
        need(key not in fresh or fresh[key]==value,'Consistent fresh evidence')
        need(key not in state['inputHashes']or state['inputHashes'][key]==value,'Never relabel inherited evidence')
        fresh[key]=value
    # The integer raster/replay changes only declared physical-slot IDs; all
    # DMA/CPU/native clear/one-anchor/exact VRAM/RGB checks are unchanged.
    old_model=ROOT/'tools/current_tomb_ram_model_v3629.py'
    new_model=ROOT/'tools/current_tomb_ram_model_v3642.py'
    expected=old_model.read_text().replace('def __init__(self, guest, payload, graphics):',
        'def __init__(self, guest, payload, graphics, ids=(17,18)):').replace(
        'self.guest,self.payload,self.graphics = guest,payload,graphics',
        "self.guest,self.payload,self.graphics = guest,payload,graphics\n        self.ids=tuple(ids)\n        need(len(self.ids)==2 and set(self.ids)=={17,18}, 'Explicit true physical-slot IDs, no proxy or inferred identity')").replace(
        'check_owned_body_palette(q,colors,self.guest,(17,18),q',
        'check_owned_body_palette(q,colors,self.guest,self.ids,q')
    need(new_model.read_text().rstrip('\n')==expected.rstrip('\n'),'Entire unchanged native renderer, only explicit true slot palette IDs added')
    matrix_path=current.OUT/'report.json';matrix=json.loads(matrix_path.read_text())
    need(matrix['passed']and matrix['currentBothCharactersBothPhysicalSlotsNativeTombRenderShadowEraseAccepted']and
         matrix['priorKanoP1NotRerun']and matrix['newVisibleFields']==1611 and
         matrix['newExactVisibleRGBPixels']==163677600 and not matrix['stageAudioFidelityAccepted']and
         not matrix['allStockNewMirrorVictimBranchAcceptance']and not matrix['fullPortAcceptance'],
         'Actual terminal remaining character/physical-slot scene matrix, not universal stage/audio')
    cases=[];files=[]
    wanted_random={('sonya',1):20,('sonya',2):203,('kano',2):958}
    for fighter,side in current.CASES:
        folder,output=current.case_paths(fighter,side);path=output/'report.json';report=json.loads(path.read_text())
        terminal=json.loads((folder/'result.json').read_text());scene=report['nativeScene']
        identity=17 if fighter=='kano'else 18
        ids=[identity if slot==side else 35-identity for slot in(1,2)]
        need(report['passed']and report['fighter']==fighter and report['side']==side and
             report['truePhysicalIDs']==scene['truePhysicalIDs']==ids and report['sampledFrames']==537 and
             report['exactRGBPixels']==54559200 and report['continuousExactPreBuffers']==report['continuousExactFlips']==507 and
             report['continuouslyExactHeldScanouts']==30 and report['nativeShiftLoads']==report['nativeShiftFills']==503 and
             report['nativeShiftTransfers']==63881 and report['oneInitialBaseOnly']and
             report['laterTargetVRAMNeverUsedAsAnchors']and len(report['rejectedActualPixelTargetFaults'])==2 and
             scene['actualNativeRandomValue']==wanted_random[fighter,side]and
             scene['nativeDrop']==(wanted_random[fighter,side]<50)and scene['nativeInputState']['passed']and
             scene['nativeInputState']['consecutive_fields']==801 and scene['nativeShadowCopies']>3000 and
             report['sourceQualifiedFullNativeInputContractSHA256']==current.native.EXECUTED_CONTRACT_SHA256 and
             terminal['captureCompleted']and terminal['exit_code']==0 and terminal['modelExactFields']==537 and
             not terminal['modelErrors']and terminal['guest_writes']==0 and not terminal['cheats_enabled'],
             'Actual complete scene/source/controls/full health/trueIDs/native action/shadow/cleanup proof')
        if scene['nativeDrop']:
            need(scene['nativeMotion']['checkedConsecutiveCallbacks']==269 and
                 scene['nativeMotion']['floor']==86,'Own actual Kano victim floor and original269callback drop')
        pin(path)
        for file,wanted in report['inputHashes'].items():pin(file,wanted)
        leaf=[file for file in folder.rglob('*')if file.is_file()];files.extend(leaf)
        need(len(leaf)==14 and not any(file.suffix.lower()in('.exe','.wav','.png','.jpg','.bmp')for file in leaf)
             and not any(file.name.startswith(('display_pre_','display_vram_','display_palette_'))for file in leaf),
             'Small source/metadata logs only, one allowed guest diagnostic, no raw bulk capture copies')
        for file in leaf:pin(file)
        cases.append(dict(fighter=fighter,side=side,truePhysicalIDs=ids,report=str(path),
                          sampledFrames=537,exactRGBPixels=54559200,nativeRandom=scene['actualNativeRandomValue'],
                          nativeDrop=scene['nativeDrop'],nativeShadowCopies=scene['nativeShadowCopies'],
                          sourceBoundProjections=scene['sourceBoundProjections'],nativeInputState=scene['nativeInputState'],
                          oneInitialBaseOnly=True,exactNativeEraseTransfers=63881))
    fault_path=faults.OUT/'report.json';fault=json.loads(fault_path.read_text())
    need(fault['passed']and fault['qualifiedActualMetadataInputIdentityHealthFaults']==30 and
         len(fault['cases'])==3 and all(len(case['qualifiedActualFaults'])==10 and
         case['positivesRestoredAfterEveryFault']for case in fault['cases']),
         'Actual per-slot sprite/floor/projection/shadow/native-ID/paid-health faults rejected and positives restored')
    compression_path=storage.OUT/'report.json';compression=json.loads(compression_path.read_text())
    need(compression['passed']and compression['logicalHashesAndSizesUnchanged']and
         compression['deletedFiles']==0 and compression['reclaimedAllocatedBytes']==45686784 and
         compression['allocatedBytesAfter']==15687680,'Exact lossless sealed-log compression, no evidence deletion')
    for path,report in ((matrix_path,matrix),(fault_path,fault),(compression_path,compression)):
        pin(path)
        for file,wanted in report['inputHashes'].items():pin(file,wanted)
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        file=ROOT/relative;pin(file,state['inputHashes'][str(file.resolve())])
    for file in (old_model,new_model,ROOT/'tools/run_current_tomb_ram_matrix_v3644.py',
                 ROOT/'tools/native_tomb_drop_qualification_v3643.py',
                 ROOT/'tools/save_current_tomb_matrix_checkpoint_v3656.py',Path(__file__).resolve(),PREVIOUS):pin(file)
    capture_storage=dict(captureLeaves=3,files=len(files),logicalBytes=sum(file.stat().st_size for file in files),
                         allocatedBytes=sum(storage.allocated(file)for file in files),guestDiagnosticDumps=3,
                         executableROMPixelVRAMAudioCopies=0)
    state['inputHashes']=fresh
    state['currentScopeEvidenceAudit']['group1']=(
        'Current3172Tomb now source-replayed for both true characters/both physicalslots: prior3635KanoP1 '
        'drop7 plus3651newSonyaP1drop20/SonyaP2held203/KanoP2held958. Each537visiblefields/'
        '54,559,200RGBpixels/507pre+507fliptargets/30heldscanouts,oneinitialbase/503nativeclearloads/fills/'
        '63,881erase transfers,wholeinitializedguest/compiledinputs/sourcegraphics/originalcomposites/'
        'camera/FIFO/palettes/nativecompressedshadows. Current4scenes2148fields/218,236,800RGBpixels/'
        '16,319nativeShadowCopies. Entireoriginal1731physical coldboot/select/nativefullhealth322wins/'
        'paidrematch/distance/inputparser/action/history/801fields/retirementgates retained; nonheld '
        'currentbranch admitted only by exactoriginalTomb/RNG/fall/teardownguestbytes,owned/unpressed '
        'original5-percentbranch/269callbackdrop on actualvictimfloor85or86,notoldsinglefixture/RNGforce. '
        '3653rejects30actualart/floor/projection/shadow/identity/earnedhealthfaults across3newslots '
        'and restorespositives;live6VRAM/RGBbitfaults,new1611fields/163,677,600pixels. '
        '3639recordedstates/visibleobservercomparison remains bounded,notuniversal hiddenstate. '
        'Stock/new/mirrorvictim/Pit/remainingbranchcontexts and complete stageaudiofidelity stillopen. '
        'No public/game/build changes or PNG/WAV/VRAMcopies.3655LZXcompression preservesalllogSHA/size '
        'and frees45,686,784allocatedbytes;4neededlogsnow15,687,680allocatedbytes,no evidence deletion.')
    state.update(previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten historical map.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: inspected3641checkpoint/actualterminal3635/evidence/current dirty worktree before edits; no source/game edits. Fresh3642RAMmodel retains all originalmath and only adds explicitphysicalIDs to palettebinding. Fresh3643retains entirelegacy1731nativeinput/fullhealth/parser/action/801fieldcleanupgates, replacingoldSonyap2onlydropfixture solelywith actualoriginalguest/RNG/ownedunpressed269callbackdropqualification.3644purepreflightpasses;fresh3648adds properdependency/contractSHApins before fullruns. Threeactual3172physical earned Tomb casesrun in parallel,each childterminal0 and537fullRGBfields exact/oneinitialbase/507pre+507fliptargets/30held/63881erase transfers. SonyaP1naturaldrop20/floor86,SonyaP2nativeheld203,KanoP2nativeheld958;bothtruecharacters/bothslots currentTombsource/shadow/erase/cleanupaccepted across4scenes2148fields/218.24millionRGBpixels with priorKanoP1notrerun.3653qualifies30actualmetadata/identity/healthfaults,plus6livepixeltargetfaults.3655losslesslycompresses4sealeddiagnosticlogs,45.69MBallocatedfreed/allSHA/sizeunchanged/no deletion. New3compressed14filemetadata captures/3guestdiagnostics,no EXE/PNG/WAV/VRAMcopies;full5groups/P1campaigns/public/retiredexclusions intact.',
        rejectedPureCheckpointWriter=dict(tool=str(ROOT/'tools/save_current_tomb_matrix_checkpoint_v3656.py'),
            terminalExitCode=1,reason='Only an extra trailing newline in fresh generated model source; no renderer math changed. Freshwriter compares exact non-trailing-newline source while preserving complete actual byte SHA pins.'),
        current3172NativeTombBothCharactersBothPhysicalSlotsRenderShadowEraseAccepted=True,
        current3172NativeTombRemainingSlotMatrixReport=str(matrix_path),
        current3172NativeTombRemainingSlotScenes=cases,
        current3172NativeTombAllFourVerifiedVisibleFields=2148,
        current3172NativeTombAllFourVerifiedRGBPixels=218236800,
        current3172NativeTombAllFourNativeShadowCopies=16319,
        current3172NativeTombRemainingSlotActualFaultReport=str(fault_path),
        current3172NativeTombRemainingSlotQualifiedActualFaults=30,
        current3172NativeTombRemainingSlotQualifiedLivePixelTargetFaults=6,
        current3172NativeTombEntireOriginalInputStateContractPreserved=True,
        current3172NativeTombSourceQualifiedDropContractSHA256=current.native.EXECUTED_CONTRACT_SHA256,
        current3172NativeTombFullHiddenWorldStateObserverEquivalenceAccepted=False,
        current3172NativeTombCompleteStageAudioFidelityAccepted=False,
        current3172NativeTombAllStockNewMirrorVictimsAndEveryBranchAccepted=False,
        currentTombDiagnosticCompressionReport=str(compression_path),
        currentTombFourSealedLogsAllocatedBytes=15687680,
        losslessDiagnosticAllocatedBytesFreedThisTurn=45686784,
        currentTombRAMStorageThisTurn=capture_storage,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,newRuntimeCaptureLeavesThisTurn=3,
        acceptedVisibleScenarioCapturesThisTurn=3,rawPixelImageVRAMCopiesThisTurn=0,
        diagnosticGuestProgramDumpsThisTurn=3,deletedEvidenceOrUserFilesThisTurn=0,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
        nextAction='Do not repeat accepted current4Tomb true-character/physicalslot source-raster-shadow-erase/inputstate windows or priorP1campaigns/endings/Friendship merely for metadata. Next close complete native stageeffect/victim audio fidelity via RAMonly realaudio/ownedportcues with original source samples, and broader typed stock/new victim/mirror/Pit/branch coverage from3591finite inventory; no forcedRNG/health/arena. Current source/sprites/floor/shadows/cleanup for4Tombcases nowdone,not automatically allstageaudio/allvictims. Consolidate remaining movephase/arena/CPU/repeat/KO/overlap and otherfinisher/morph/secret/cinematic contexts, then combinedcurrentUI/ladder/names/audio gate and refreshedreleaseZIP/CMD. Preserve fulloriginal5groups,public1836CMD/ZIP,retiredexclusions; compresssealedmetadata ratherthannewbulkimage/VRAM/WAV/buildcopies.')
    need(state['remaining']==remaining and not state['fullPortAcceptance']and not state['finishedRelease'],
         'Original full objective/deliverables intact')
    OUT.mkdir();file=OUT/'checkpoint.json';file.write_text(json.dumps(state,indent=2)+'\n')
    before=sha(file);result=subprocess.run(['compact.exe','/C','/I','/Q',str(file)],capture_output=True,text=True)
    need(result.returncode==0 and sha(file)==before,'Lossless compact full-scope checkpoint')
    print(json.dumps(dict(saved=str(file),goalStatus='active',currentTombCases=4,
        currentVerifiedFields=2148,currentVerifiedRGBPixels=218236800,
        newQualifiedActualMetadataFaults=30,allocatedDiagnosticBytesFreed=45686784,
        captureStorageThisTurn=capture_storage,freshRelevantPins=len(fresh),fullPortAcceptance=False),indent=2))


if __name__=='__main__':main()

