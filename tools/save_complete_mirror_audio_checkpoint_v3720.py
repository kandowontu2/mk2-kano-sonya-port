"""Full objective retained; scope-bound completed3680 mirror audio evidence."""
import json
from pathlib import Path
import run_natural_mirror_complete_audio_v3715 as runtime

ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
PREVIOUS=ROOT/'audit_v3697_native_sound_terminal_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3721_complete_mirror_audio_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining']);fresh={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Original full goal not narrowed')
    def pin(file,wanted=None):
        file=Path(file).resolve();key=str(file);digest=sha(file)
        need(wanted is None or wanted==digest,'Actual relevant evidence unchanged '+key)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh source/evidence binding')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'No inherited evidence relabeling')
        fresh[key]=digest
    report_path=runtime.OUT/'report.json';report=json.loads(report_path.read_text())
    need(report['passed']and report['candidate']==runtime.NAME and report['naturalMirrorBothCharactersBothSlotsSelectionIndividualDirectCueMixAccepted']and
      not report['allVictimFinisherOrNativeDCSWaveformAcceptance']and not report['fullPortAcceptance'],'Actual bounded compiled mirror/audio acceptance')
    need({(c['fighter'],c['side'])for c in report['cases']}=={(f,s)for f in('kano','sonya')for s in(1,2)},'All four true mirror performer/slot contexts')
    for case in report['cases']:
        mix=case['mixedOriginalCueFidelity'];physical=case['physical']
        need(case['passed']and mix['correlation']>.9995 and mix['residualRMS']<2 and mix['exactSilentGapSamples']>3000000 and
          physical['nativeDamage']==322 and physical['nativeKOs']==2 and physical['terminalFrame']>=5198 and case['rawAudioFilesWritten']==0,'Actual full original cues/zero unexplained gaps/earned own action and long terminal run')
        for leaf in(case['capture'],case['baseline']):
            folder=ROOT/leaf;meta=json.loads((folder/'result.json').read_text())
            need(meta['exit_code']==0 and meta['candidate']==runtime.NAME and meta['rawAudioFilesWritten']==0,'All actual child runs terminal0, no disk PCM')
            need(sha(folder/'guest_maincpu.bin')=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Whole guest unchanged')
    for p,h in report['inputHashes'].items():pin(p,h)
    pin(report_path)
    fault_path=ROOT/'audit_v3714_natural_mirror_audio_state_faults_checked/report.json';fault=json.loads(fault_path.read_text())
    need(fault['passed']and fault['totalQualifiedActualStatePaletteFaults']==40 and fault['fullContractSHA256']==report['cases'][0]['physicalContractSHA256'],'Forty actual full-contract identity/owner/activation/palette/FIFO faults')
    for p,h in fault['inputHashes'].items():pin(p,h)
    pin(fault_path)
    storage_path=ROOT/'audit_v3719_sealed_mirror_diagnostic_compression/report.json';storage=json.loads(storage_path.read_text())
    need(storage['passed']and storage['deletedFiles']==0 and storage['newBuilds']==0 and storage['rawAudioFiles']==0,'Lossless sealed prior diagnostic compression only')
    for p,h in storage['inputHashes'].items():pin(p,h)
    pin(storage_path)
    checked_storage_path=ROOT/'audit_v3723_checked_mirror_evidence_compression/report.json';checked_storage=json.loads(checked_storage_path.read_text())
    need(checked_storage['passed']and checked_storage['deletedFiles']==0 and checked_storage['newBuilds']==0 and checked_storage['rawAudioFiles']==0,'New accepted mirror evidence losslessly sealed')
    for p,h in checked_storage['inputHashes'].items():pin(p,h)
    pin(checked_storage_path)
    storage_freed=storage['reclaimedAllocatedBytes']+checked_storage['reclaimedAllocatedBytes']
    for leaf in('audit_v3702_natural_mirror_audio_ram_checked','audit_v3707_mirror_pcm_gap_diagnosis_checked','audit_v3711_natural_mirror_complete_audio_checked'):
        file=ROOT/leaf/'report.json';value=json.loads(file.read_text());need(not value['passed'],'Preserved prior failure, not relabeled as accepted');pin(file)
    diagnosis=json.loads((ROOT/'audit_v3707_mirror_pcm_gap_diagnosis_checked/report.json').read_text())['diagnosis']
    need(diagnosis['outsideModelNonzeroSamples']==26283 and diagnosis['outsideModelSpans'][0]['firstSeconds']>94.4,'Actual failed-gate mismatch localized after own finisher to later CPU launch')
    for file in(PREVIOUS,Path(__file__).resolve(),ROOT/'tools/run_natural_mirror_audio_ram_v3700.py',ROOT/'tools/diagnose_mirror_pcm_gaps_v3705.py',ROOT/'tools/run_natural_mirror_complete_audio_v3709.py'):pin(file)
    candidate=ROOT/runtime.NAME;restore=json.loads((candidate/'restoration.json').read_text())
    need(restore['passed']and all(sha(p)==h for p,h in restore['restored_actual_preexisting_files'].items()),'Original dirty user files and installed executable still exactly restored')
    pin(candidate/'restoration.json')
    pin(ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe','34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E')
    pin(ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip','994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA')
    pin(ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd')
    state.update(previousCheckpoint=str(PREVIOUS),inputHashes=fresh,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentSHA256=sha(PREVIOUS),mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Never flatten historical map.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: actual3702failure revalidated. Fresh3706bothterminal0 PCM-only-inRAM diagnosis3707 localizes26283 unexplained output samples at94.450s, after own KanoP2finisher and next-fight CPU Sonya6B01/6B02 at94.417s, not nativeFFF8alias. Strict all-cue model keeps exactzero unexplained gaps, native ownership/cleanup, full source tails and gain/waveform correlation. First3709extension terminal0 fails only scheduled-exit callback accounting; failure preserved. Final3715/3717eight actual3680 mirror runs allterminal0 accept bothchar/bothslots ownidentity/nativehealth/KOs/action/full63-pen palettes/FIFO/continue and complete actual direct/name/kiss/extract/fire/victim/winner waveforms, including full genuine subsequentCPU launch and cleared owners.3714forty state/palette faults reject and restore exactpositive. No game/source/build/public change; all5remaining groups retained.3719lossless compression reclaimed35938304allocatedbytes with all evidence bytes unchanged; no audio/raster/build copies.',
      developmentCandidate=runtime.NAME,
      gameSourceAndPlayableBytesChangedThisTurn=False,
      current3680MirrorBothCharactersBothSlotsIndividualDirectCueMixAccepted=True,
      current3680MirrorIndividualDirectCueReport=str(report_path),current3680MirrorIndividualDirectCueCases=report['cases'],
      current3680MirrorStatePaletteFaultReport=str(fault_path),
      current3680AllDirectCueSelectionRegressionAccepted=False,current3680FullStageVictimAudioWaveformAccepted=False,
      currentMirrorFullFinisherRasterOrAllVictimAcceptance=False,
      preservedMirrorGateFailures=['audit_v3702_natural_mirror_audio_ram_checked','audit_v3707_mirror_pcm_gap_diagnosis_checked','audit_v3711_natural_mirror_complete_audio_checked'],
      currentTurnSealedDiagnosticCompression=dict(reports=[str(storage_path),str(checked_storage_path)],allocatedBytesFreed=storage_freed,deletedFiles=0),
      pendingMirrorAudioExecSession=None,
      nextAction='Do not repeat completed3680mirror8captures/individual directcue fullmix/state/fullpalette merelyfor metadata. Finish compiled3680Friendship source-cue regression and combinedselection/ladder/names/shadows/audio scope; full nativeDCSstage/victimwaveforms and broader nativePit/Tomb victims/mirror/branches remain. Keep original5groups: fullmovephase art/ground/shadows/cleanup acrossarenas and broaderCPU/repeated/KO/overlap; otherfinishers/victims/morph/secrets/cinematics; P2actualcampaign/ending contexts (both current3172P1naturalKintaro/Shaoownendings alreadyaccepted, notpending); finalcombinedUI/audio/dependency-awareobsoletecleanup/refreshedreleaseZIP/CMD. Public1836remainsunchanged. Preserve dirtyuserfiles, retired/deleted exclusions and recursivelyinheritedpins. No build/raster/VRAM/WAV redo without actualneedednew evidence.')
    state['stagedNativeSoundPacketFix']['allOtherDirectCuesSelectionAndFullStageWaveformRegressionPassed']=False
    state['thisGoalTurnClassification']+=' New3723accepted8capturelog sealing also preserves every logical byte; combined actual allocated bytes reclaimed='+str(storage_freed)+'. PublicEXE1836/ZIP verified unchanged.'
    state['stagedNativeSoundPacketFix']['additionalIndividualDirectCueRegressionReport']=str(report_path)
    need(state['remaining']==remaining and not state['fullPortAcceptance']and not state['finishedRelease'],'No diminished completion scope')
    OUT.mkdir();file=OUT/'checkpoint.json';file.write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(file),acceptedTrueMirrorContexts=4,qualifiedStatePaletteFaults=40,freshRelevantPins=len(fresh),
      gameOrPublicBuildChanged=False,allocatedBytesFreed=storage_freed,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
