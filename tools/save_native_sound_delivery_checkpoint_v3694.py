"""Full objective retained with compiled sound guard/both-slot actual regression."""
import json
import subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as runtime
import compact_current_tomb_logs_v3654 as storage

ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
PREVIOUS=ROOT/'audit_v3686_native_sound_build_wait_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3695_native_sound_delivery_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh full objective checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining'])
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],
         'All original scope remains, not narrowed to sound routing')
    fresh={}
    def pin(file,wanted=None):
        key=str(Path(file).resolve());digest=sha(file)
        need(wanted is None or wanted==digest,'Actual relevant source/evidence unchanged')
        need(key not in fresh or fresh[key]==digest,'Consistent actual fresh pins')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Never relabel inherited evidence')
        fresh[key]=digest
    candidate=ROOT/runtime.NAME
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    restore=json.loads((candidate/'restoration.json').read_text(encoding='utf-8-sig'))
    need(restore['passed']and all(sha(p)==h for p,h in restore['restored_actual_preexisting_files'].items()),
         'Actual user source/header/installed executable restoration confirmed now')
    need(build['executable_sha256']=='BF5D90F90E6A254C4BCB63B4C0D3974C08DF9F28A817BD35A6F86FE68ABE6A41'and
         build['payload_sha256']=='ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3'and
         not build['game_data_changed']and not build['public_build_promoted'],'Actual compiled narrow host guard with unchanged payload, no public promotion')
    for p,h in build['input_hashes'].items():pin(p,h)
    pin(candidate/'mkport_candidate.exe',build['executable_sha256']);pin(candidate/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
    for file in('build-info.json','restoration.json','build.log'):pin(candidate/file)
    cases=[];logs=[];total_native=0;comparisons=[]
    old_paths={('kano',1):'audit_v3634_current_kano_tomb_p1_native_ram',
               ('sonya',1):'audit_v3649_current_sonya_tomb_p1_native_ram',
               ('kano',2):'audit_v3649_current_kano_tomb_p2_native_ram',
               ('sonya',2):'audit_v3649_current_sonya_tomb_p2_native_ram'}
    for file,key in((ROOT/'audit_v3684_native_sound_delivery_ram_checked/report.json','currentTombBothP1PerformersNativePacketDeliveryAndFullWinnerMixAccepted'),
                    (ROOT/'audit_v3691_native_sound_delivery_p2_checked/report.json','currentTombBothP2PerformersNativePacketDeliveryAndFullWinnerMixAccepted')):
        report=json.loads(file.read_text());need(report['passed']and report['candidate']==runtime.NAME and report[key]and
              not report['completeStageVictimAudioFidelityAccepted']and not report['allDirectCueAndSelectionRegressionAccepted'],
              'Actual finite regression scope, not all sound/finisher/selection acceptance')
        for p,h in report['inputHashes'].items():pin(p,h)
        pin(file)
        for case in report['cases']:
            mix=case['originalWinnerMix'];total_native+=len(case['nativeDCSActualDeliveries'])
            need(case['passed']and mix['outputSamples']==96000 and mix['correlation']>.9995 and mix['residualRMS']<2 and case['rawAudioFilesWritten']==0,
                 'Full actual original winner waveform at native interpolation/gain, no disk PCM')
            for leaf in(case['capture'],case['baseline']):
                folder=ROOT/leaf;terminal=json.loads((folder/'result.json').read_text())
                need(terminal['exit_code']==0 and terminal['candidate']==runtime.NAME and terminal['rawAudioFilesWritten']==0,'Every actual emulator child terminal success')
                need(sha(folder/'guest_maincpu.bin')=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Actual unchanged whole guest in all8captures')
                logs.append(folder/'run.log')
            select=lambda path:[line.strip()for line in path.open(encoding='utf-8-sig')if line.startswith('MK2_STAGE_')]
            oldlog=ROOT/old_paths[case['fighter'],case['side']]/'run.log'
            newlog=ROOT/case['capture']/'run.log'
            original,actual=select(oldlog),select(newlog)
            need(actual==original and len(actual)>8000,'All actual recorded native physical/provenance events equal prior3172, no state/branch normalization')
            comparisons.append(dict(fighter=case['fighter'],side=case['side'],oldCapture=str(oldlog),newCapture=str(newlog),exactRecordedNativeRows=len(actual)))
            pin(oldlog);cases.append(case)
    fault_file=ROOT/'audit_v3693_native_sound_delivery_faults_checked/report.json'
    fault=json.loads(fault_file.read_text());need(fault['passed']and fault['totalRejectedActualMetadataFaults']==40 and
          fault['noMissingExtraOrMisroutedObservedNativeBytes']and not fault['wholeNativeDCSWaveformAcceptance'],'Actual byte/channel fault qualification, not full DCS waveform')
    for p,h in fault['inputHashes'].items():pin(p,h)
    pin(fault_file)
    inventory_file=ROOT/'audit_v3688_native_sound_store_inventory_checked/report.json'
    inventory=json.loads(inventory_file.read_text());need(inventory['passed']and inventory['totalOriginalPortStores']==15 and
          inventory['dynamicNativePacketStores']==2 and inventory['noncollidingOriginalConstantStores']==13,'Whole original ROM sound-port site census')
    for p,h in inventory['inputHashes'].items():pin(p,h)
    pin(inventory_file)
    sealed=[]
    for file in [*logs,candidate/'mkport_candidate.exe']:
        before=storage.allocated(file);digest=sha(file);size=file.stat().st_size
        result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(file)],capture_output=True,text=True)
        need(result.returncode==0 and sha(file)==digest and file.stat().st_size==size,'Lossless terminal-log/unique-new-executable compression, no shared-payload mutation')
        sealed.append(dict(path=str(file),logicalBytes=size,beforeAllocatedBytes=before,afterAllocatedBytes=storage.allocated(file),sha256=digest))
    for file in(PREVIOUS,Path(__file__).resolve()):pin(file)
    state.update(previousCheckpoint=str(PREVIOUS),inputHashes=fresh,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentSHA256=sha(PREVIOUS),
        mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Never flatten historical map.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: authoritative live build56841 polled to terminal0, no duplicate restart.3680source-selected current guard executable compiled, exact original user/source/header/installed restoration verified.3688whole originalROM15port-store census proves2dynamic guardedPCs/13noncollidingconstant stores/4wrongPCfaults. Eight actual compiled3680 earned nativeTomb samples-on/off cases for Kano/Sonya bothslots terminal0, wholeguest unchanged; actual44/80byte DSP inputs delivered in order with no missing/extra imported delivery. Source-owned native victim gender correct for actual twoP1drop late screams; native heldP2takes originalbranch. Full96koutput winner clips original16k interpolation/gain correlation>.9999996/RMS<.77, finite channels and no false fire/residue.3693forty metadata/byte/channel faults qualified with exact positive restored. All34345recorded native physical/provenance rows equal prior3172Tomb captures, no raster/VRAM redo; not universal hiddenstate/audio proof. Compression preservesSHA/size of8sealedlogs+unique newexe. Original5groups/public1836/retired exclusions retained; otherdirectcue/selection/fullDCSwaveform gates open.',
      pendingNativeSoundBuild=None,
      completedNativeSoundBuild=dict(candidate=runtime.NAME,execSessionId=56841,terminalExitCode=0,executableSHA256=build['executable_sha256'],
        payloadSHA256=build['payload_sha256'],sourceSelectedTarget=build['source_selected_target'],exactActualUserFilesRestored=True,
        transientExecutableBackupRemoved=not(candidate/'restoration_backups/mkport.exe').exists(),publicPromoted=False),
      current3680TombBothCharactersBothSlotsNativePacketDeliveryWinnerMixAccepted=True,
      current3680NativeSoundDeliveryCases=cases,current3680NativeRecordedStateComparison=comparisons,
      current3680ActualNativeBytesDelivered=total_native,current3680NativeDeliveryFaultReport=str(fault_file),
      current3680FullStageVictimAudioWaveformAccepted=False,current3680AllDirectCueSelectionRegressionAccepted=False,
      currentStageAudioAcceptance=False,
      sealedNewSoundEvidenceCompression=sealed,
      nextAction='Do not repeat completed3680eightTomb/ADSPdelivery/winner/statecomparisons merelyfor metadata. Next test direct selection/name/kiss/extract/burn fire+victim cues and existingFriendship launch cues on actualnew3680host; originalFFnativepackets must never aliasimportedcues and authenticdirectmarkers must stillplay finite fulloriginalmix. Continue complete nativeDCSstage/victimwaveform fidelity, remainingstock/new/mirror/Pit/branch contexts, broadermovephase/CPU/repeated/KO/overlap/arenas, otherfinishers/morph/secrets/cinematics/full5groups. Retain prior3172visual/campaign/ending proof as recorded scope, not relabeled full3680runtime acceptance. Combinedselection/ladder/names/shadows/audio regression then refreshedreleaseZIP/CMD. Preserve public1836CMD/ZIP, dirty usercheckout and retired exclusions; newunchangedpayloadhardlink immutable, no repeatedbuild/raster/VRAM/WAVcopies. Necessarysinglefixedexe compressed; compilercache may be needed for subsequentactualchanges, not obsolete blindly.')
    need(state['remaining']==remaining and not state['fullPortAcceptance']and not state['finishedRelease'],'Full original objective unchanged')
    OUT.mkdir();file=OUT/'checkpoint.json';file.write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(file),candidate=runtime.NAME,trueCharacterPhysicalCases=4,nativeDeliveredBytes=total_native,
      exactRecordedPriorNativeRows=sum(c['exactRecordedNativeRows']for c in comparisons),rejectedActualMetadataFaults=40,
      allocatedBytesFreedByLosslessCompression=sum(r['beforeAllocatedBytes']-r['afterAllocatedBytes']for r in sealed),
      freshRelevantPins=len(fresh),fullPortAcceptance=False),indent=2))

if __name__=='__main__':main()
