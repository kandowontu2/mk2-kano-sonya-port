"""Full-objective checkpoint after complete bounded native Jax clap audio proof."""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v4051_jax_complete_scene_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4072_jax_native_audio_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Complete original objective remains active and unproven')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Exact accepted bytes unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent exact fresh pins')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Shared inherited bytes unchanged')
        pins[key]=digest
    pin(PARENT);reports={}
    for leaf in('audit_v4056_jax_clap_native_audio_queue_observed','audit_v4061_jax_clap_native_audio_routes_observed','audit_v4067_jax_clap_native_audio_routes_checked','audit_v4070_jax_clap_audio_compression'):
        p=ROOT/leaf/'report.json';value=json.loads(p.read_text())
        need(value['passed']and not value['fullPortAcceptance'],'Actual terminal bounded audio/storage proof '+leaf);reports[leaf]=value;pin(p)
        for p,h in value['inputHashes'].items():pin(p,h)
    audio=reports['audit_v4067_jax_clap_native_audio_routes_checked'];storage=reports['audit_v4070_jax_clap_audio_compression']
    need(audio['actualContexts']==4 and audio['actualRowCounterexamplesRejected']==120 and audio['actualOriginalSelectorCommands']==128 and
         audio['actualNativeDCSBytesDelivered']==280 and audio['originalCompleteEarnedStateAlgorithmRetained']and
         audio['completeGenericNativePCMPacketADSPAlgorithmRetained']and audio['allObservedSelectorCommandsSourceBound']and
         not audio['stockReferenceWholeWaveformFidelityAccepted']and not audio['allVictimFinisherAudioAccepted'],'Complete own native Jax clap audio contract, not stock/all-finisher fidelity')
    for case in audio['cases']:
        a=case['nativeAudio']
        need(a['completeNativePCMFrames']==657600 and a['completeNativePCMUpdates']>0 and len(a['actualCommands'])==32 and
             a['nativePacketBytesDelivered']==70 and a['allDispatchPacketsAndOwnersBound']and len(case['actualRowCounterexamplesRejected'])==30,'All four actual dual-table, voice, packet, PCM and earned-state fault contexts')
    need(storage['captureFolders']==16 and storage['deletedFiles']==storage['newPlayableCopies']==0,'All actual terminal leaves preserved losslessly, no new build/deletion')
    missing=storage['captureChildrenMissing']+[134688]
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,missing))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'All exact native capture and independent qualifier processes terminal/missing now')
    for name in('mk2ks_jax_clap_audio_queue_ram_v4052.lua','tools/verify_jax_clap_audio_state_v4053.py','tools/run_jax_clap_native_audio_queue_v4054.py',
                 'mk2ks_jax_clap_audio_routes_ram_v4057.lua','tools/verify_jax_clap_audio_routes_state_v4058.py','tools/run_jax_clap_native_audio_routes_v4059.py',
                 'tools/verify_jax_clap_native_audio_routes_v4062.py','tools/verify_jax_clap_native_audio_routes_v4064.py','tools/verify_jax_clap_native_audio_routes_v4066.py',
                 'tools/compact_jax_clap_audio_v4069.py','tools/save_jax_native_audio_checkpoint_v4071.py','tools/verify_native_arm_palette_v1074.py','tools/verify_native_arm_rip_v1051.py'):
        pin(ROOT/name)
    for relative,wanted in {
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/relative,wanted)
    pin(ROOT/state['currentCMD'])
    state.update(inputHashes=pins,inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
        previousGoalTurnClassification='progress:4051 four complete original Jax head-clap scenes, full earned-state/FIFO/floor/compressed shadow proofs and lossless73MiB terminal seal.',
        thisGoalTurnClassification='progress: initial4052 full native Jax clap audio four contexts/eight paired captures prove complete PCM, actual initialized guest and port/ADSP delivery. Read-only route inventory showed two missing entry taps; fresh4057 records original separate selector and death-voice calls. Corrected eight captures retain complete physical state and full PCM on/off exactly. Initial4062 preflight rejected mistaken one-special-call expectation because seven real post-win selectors are in the full window;4064 rejected fictitious MOVI11 at the existing name trampoline, whose real Jax11 falls through original selector after254/253 comparisons. Both failed sources preserved unchanged.4066 complete generic PCM/channel/packet/ADSP plus original1036 earned-state grammar passes all four own victim/slot contexts and120 actual faults.128 actual dual-table selector commands and280 delivered sound bytes source-bound;21 original randomized blood calls per context retained and true player/gender death voices45/46/48. No game/build/playable byte changes or full stock waveform claim.16 terminal leaves losslessly compressed without deletion.',
        currentDevelopmentNativeJaxClapAudioReport=str(ROOT/'audit_v4067_jax_clap_native_audio_routes_checked/report.json'),
        currentDevelopmentNativeJaxClapAudioQualified=dict(ownVictimContexts=4,actualPairedCaptures=8,completeNativePCMFramesPerPrimary=657600,actualOriginalDualTableCommands=128,actualDeliveredDCSBytes=280,actualAudioAndStateFaultsRejected=120,
            sourceBoundDeathVoice=dict(kanoP1='45',kanoP2='46',sonyaBothSlots='48'),allOriginalJaxClapSelectorsAndBloodTasksBound=True,samplesOnOffEveryPCMByteEqual=True,scope='Normal costume Dead Pool, original earned Jax head-clap; complete749 sound fields through native WIN page/continuation. No original-stock full-waveform, all-finisher/audio/arena/alternate-costume/ending acceptance.'),
        preservedJaxAudioPreflightFailures=[dict(source='tools/verify_jax_clap_native_audio_routes_v4062.py',failure='All24 general native calls and one separate Jax selector',actualReason='Eight special calls include seven genuine post-win/continuation commands; fresh4066 checks all32 selector calls.'),
            dict(source='tools/verify_jax_clap_native_audio_routes_v4064.py',failure='Exact literal original/Jax-name selector and native call0xfffb70d0',actualReason='Existing name trampoline compares254/253 then falls through CALLA for real Jax11; no fictitious MOVI11. Fresh4066 binds entire24-word trampoline.')],
        pendingJaxClapAudio=None,currentTurnReclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,confirmedMissingThisTurnCapturePIDs=missing,
        nextImplementationAction='Jax head-clap native scene/state/floor/shadow and full native audio are now independently qualified in four normal Dead Pool own-victim/slot contexts, not all stock full-waveform fidelity. Continue original Jax arm-rip bbbb_lp Block+LP gap96 originFF8BE240 variant2: actual original palette-router prop entries point to true victim via main+140 while props have ID0, and six19-row native body/arm/position tables are already present. Do not load optional1063 controlled-alt guest-write observer or resurrect retired1046/1071 folders; use original1021 physical controller and current RAM-only CPU/DMA/scan/audio observers. Genuine SonyaP2 whole-tower clear remains missing; next physical controller should respond to observed failing Mileena encounter rather than repeat identical zoning Start600/700/900 or alter game state/AI/schedule. Remaining multi-arena move/ground/shadow/cleanup, broader finisher/victim/morph/secret/cinematic/audio fidelity, actual own endings, combined final UI/ladder/names/audio, dependency-aware obsolete-folder cleanup and refreshed ZIP all remain required.',
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','No original-scope shrink or release substitution')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),ownContexts=4,actualNativeAudioAndStateFaults=120,actualSourceBoundCommands=128,deliveredDCSBytes=280,reclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],goalStatus='active',fullPortAcceptance=False)),flush=True)

if __name__=='__main__':main()
