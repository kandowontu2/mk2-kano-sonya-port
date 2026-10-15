"""Preserve full goal with actual3680 Friendship and qualified native UI gates."""
import json
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current

ROOT,need,sha,NAME=current.ROOT,current.need,current.sha,current.NAME
PREVIOUS=ROOT/'audit_v3721_complete_mirror_audio_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3741_guarded_friendship_ui_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh full-objective checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Full original goal remains, not UI/audio-only completion')
    def pin(file,wanted=None):
        file=Path(file).resolve();key=str(file);digest=sha(file)
        need(wanted is None or digest==wanted,'Relevant actual evidence changed '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh actual pins')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Never relabel inherited evidence')
        pins[key]=digest
    def report(path):
        record=json.loads(path.read_text());need(record['passed'],'Actual completed accepted report '+str(path))
        for file,wanted in record['inputHashes'].items():pin(file,wanted)
        pin(path);return record
    audio_path=ROOT/'audit_v3727_guarded_friendship_ram_audio_checked/report.json';audio=report(audio_path)
    need(audio['candidate']==NAME and audio['current3680BothHumanSlotFullRetainedFriendshipCueTailOverlapOwnershipAccepted']and
      audio['actualPhysicalCaptures']==8 and audio['actualAudibleCues']==80 and audio['actualQualifiedFaults']==36 and
      audio['wholeCurrentGuestAndPayloadIndependentlyReconstructed']and audio['rawAudioFilesWritten']==audio['newExecutableOrROMCopies']==0 and
      not audio['allFriendshipVictimsArenasCPUOrCompleteRasterAccepted']and not audio['fullPortAcceptance'],'Finite actual new-host Friendship scope only')
    delivered=0;native_records=0
    for case in audio['cases']:
        need(case['samplesNeverChangedGameplay']and case['samePathUnmodifiedPositive']and
          case['nativeScene']['observedOriginalOwnWinnerDispatches']==2,'Actual unchanged true-ID controls/earned native wins')
        need(case['fullCapture']['noNativePacketAliasedImportedCue']and case['fullCapture']['exactSilentGapOutputSamples']>2000000,'Full capture has zero unexplained imported audio')
        delivered+=len(case['fullCapture']['nativeBytesActuallyDelivered']);native_records+=case['physicalNativeRecords']
        for leaf in(case['capture'],case['baseline']):
            folder=ROOT/leaf;meta=json.loads((folder/'result.json').read_text())
            need(meta['exit_code']==0 and meta['candidate']==NAME and meta['rawAudioFilesWritten']==0 and
              sha(folder/'guest_maincpu.bin')=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Every actual terminal unchanged guest')
    need(delivered==1234,'Actual original native DCS byte consumption, not port-only inference')
    ui_path=ROOT/'audit_v3736_guarded_native_ui_qualified_ram_checked/report.json';ui=report(ui_path)
    need(ui['candidate']==NAME and ui['currentBothSlotSelectionLadderFirstMatchPixelsAccepted']and
      ui['actualCurrentRAMStatePixelQualificationMethods']==46 and ui['observedUITablesExactlyIndependentGuest']and
      ui['rawRasterFilesWritten']==0 and not ui['wholeActualGuestCapturedByThisUIProbe']and not ui['fullLaddersAccepted']and
      not ui['allCinematicsAccepted']and not ui['audioAccepted']and not ui['fullPortAcceptance'],'Actual complete source/native-stock UI contract, not all tower/raster/audio')
    frames=0;unique=0
    for case in ui['cases']:
        need(case['passed']and case['state']['true_id']==(17 if case['fighter']=='kano' else 18)and
          case['state']['first_match_participant_fields']==362 and case['rendered']['native_name_shadow_checks']>=4,'Both actual campaign slots, owned body identity and repeated actual names')
        frames+=case['actualNativeFrameCallbacks'];unique+=case['actualUniqueNativeFrames']
    need(frames==684 and unique==676 and {(c['fighter'],c['side'])for c in ui['cases']}=={(f,s)for f in('kano','sonya')for s in(1,2)},'Every declared actual current UI context and complete RAM frame corpus')
    initial_ui_path=ROOT/'audit_v3731_guarded_native_ui_ram_checked/report.json';report(initial_ui_path)
    failed_path=ROOT/'audit_v3733_guarded_ui_actual_pixel_qualification/report.json';failed=json.loads(failed_path.read_text())
    need(not failed['passed']and failed['methods']==0 and not failed['wholeActualCurrentPixelsEquivalentToSHAQualifiedBacking'],'Prior full old-frame byte equivalence remains unaccepted, never replaced with older pixels')
    for file,wanted in failed['inputHashes'].items():pin(file,wanted)
    pin(failed_path);pin(failed_path.parent/'unit-tests.log')
    storage_path=ROOT/'audit_v3740_guarded_friendship_ui_evidence_compression/report.json';storage=report(storage_path)
    need(storage['deletedFiles']==storage['newBuilds']==storage['rawAudioFiles']==0,'Only terminal logs losslessly sealed')
    candidate=ROOT/NAME;restore=json.loads((candidate/'restoration.json').read_text())
    need(restore['passed']and all(sha(p)==h for p,h in restore['restored_actual_preexisting_files'].items()),'Actual dirty user files/installed executable still exactly preserved')
    for file in(PREVIOUS,Path(__file__).resolve(),ROOT/'tools/save_guarded_friendship_ui_checkpoint_v3738.py',candidate/'restoration.json'):pin(file)
    pin(ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe','34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E')
    pin(ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip','994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA')
    pin(ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd')
    state.update(previousCheckpoint=str(PREVIOUS),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentSHA256=sha(PREVIOUS),mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Never flatten historical map.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: current3721 completed mirror proof and stopped process revalidated. Eight fresh3680 Friendship paired captures terminal0: original genuine controls unchanged, true own IDs/owners/2earnedKOs/wins/nativeposes/cleanup equal completed3172;80fulloriginal pop/cluck cues/all5sourcevariants/fulltails/independent overlaps and36actualPCM/owner/cuefaults accepted.1234actual originalDCSbytes consumed before nextwrite; complete samples-on/off nativeport/DSPread chronology equal; all14sourcesfinite/clear/noextraalias and exactzero unexplained PCM gaps. Four3729UIruns accept814whole independentpixel/physical contract inRAM. Attempt3732to use oldPNGwhole rawbyte backing fails, preserved (no old-image substitution accepted). Fourfresh3734UIruns keep currentRGBinRAM through46real state/pixel bugtests, allpass;684callbacks676unique whole nativeframes, every input/guest-table/trueID/ladder/first180combatfield retained. No newraster/VRAM/WAV/ROM/EXE copies; currentbuild/public/userfiles unchanged.3740lossless terminal-log compression preserves all bytes; original5remaininggroups retained, no broad completion.',
      developmentCandidate=NAME,gameSourceAndPlayableBytesChangedThisTurn=False,
      current3680BothHumanFriendshipOriginalCueTailOverlapOwnershipAccepted=True,
      current3680FriendshipOriginalAudioReport=str(audio_path),current3680FriendshipAudioCases=audio['cases'],
      current3680FriendshipActualNativeDCSBytesConsumed=delivered,current3680FriendshipAudibleCues=80,
      current3680FriendshipActualAudioFaults=36,current3680FriendshipRecordedNativeControlRows=native_records,
      current3680BothCampaignSlotsSelectionLadderFirstMatchPixelsAccepted=True,
      current3680QualifiedUIReport=str(ui_path),current3680QualifiedUICases=ui['cases'],
      current3680ActualCurrentUIPixelStateQualificationMethods=46,
      current3680ActualUIRAMCallbacks=frames,current3680ActualUIRAMUniqueFrames=unique,
      current3680WholeRawUIFrameEquivalenceToOlderPNGAccepted=False,
      preservedUIBackingEquivalenceFailure=str(failed_path),
      current3680AllDirectCueSelectionRegressionAccepted=False,current3680FullStageVictimAudioWaveformAccepted=False,
      current3680FullCampaignsCinematicsAndMoveArenaScopeAccepted=False,
      currentTurnSealedDiagnosticCompression=dict(report=str(storage_path),allocatedBytesFreed=storage['reclaimedAllocatedBytes'],deletedFiles=0),
      pendingFriendshipAudioExecSession=None,pendingUIExecSession=None,
      nextAction='Do not rerun accepted3680Friendship8captures/80cuefullmix/actualDCSdelivery or4qualifiedUIcaptures merelyfor metadata. Next substantive work: remaining nativePit/Tomb stageaudio/victim/mirror/branch cases and fullnativeDCSstage/victimwaveforms; fullmovephase/ground/nativefloor-shadow/cleanup acrossarenas and broaderCPU/repeated/KO/overlap; otherfinishers/victims/morph/secrets/cinematics; actualP2Kintaro/Shao campaign/ownendings/attract (both current3172P1natural campaigns/ownstory/photo/text/background/attract alreadyaccepted). New3680Square/Bicycle fullrelevant sound contexts beyond incidentalP1CPUlaunch remain distinct from legacy3172evidence. Finish combinedscope including allneedednames/audio/UI then dependency-awareobsoletecleanup and refreshedpublicZIP/CMD. Currentpublic1836unchanged; do not promote prematurely. Preserve dirtyusercheckout, recursivelyinheritedpins and retired/deleted exclusions. No unnecessary newbuild/raster/VRAM/WAVcopies; old wholePNGbacking mismatch remains unaccepted and currentUIpositive/negative tests use only actualcurrentinRAMpixels.')
    state['stagedNativeSoundPacketFix']['additionalFriendshipRegressionReport']=str(audio_path)
    state['stagedNativeSoundPacketFix']['additionalQualifiedNativeUIReport']=str(ui_path)
    state['stagedNativeSoundPacketFix']['allOtherDirectCuesSelectionAndFullStageWaveformRegressionPassed']=False
    need(state['remaining']==remaining and not state['fullPortAcceptance']and not state['finishedRelease'],'Full objective and all original remaining groups intact')
    OUT.mkdir();file=OUT/'checkpoint.json';file.write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(file),friendshipCaptures=8,originalAudibleFriendshipCues=80,actualDCSBytesConsumed=delivered,
      qualifiedCurrentUIPixelStateMethods=46,uniqueNativeUIFrames=unique,freshRelevantPins=len(pins),
      allocatedBytesFreed=storage['reclaimedAllocatedBytes'],publicBuildChanged=False,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
