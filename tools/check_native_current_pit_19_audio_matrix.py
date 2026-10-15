"""Bind four current Pit19 waveform contexts and three owned sound contexts.

All original full per-case model/fault proofs and actual RAM retirements remain
mandatory. KanoP1 baseline has no direct owner/RNG taps: never infer those from
the other three cases. No broader stage, transition, campaign or port claim.
"""
import hashlib
import json
from pathlib import Path
import native_process_census_v6647 as census

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_native_current_pit_19_audio_matrix_checked'


def need(value,message):
    if not value:raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def read(path):
    return json.loads(path.read_text())


def run():
    need(not OUT.exists() and not census.census(),'Fresh matrix only after all real native terminals')
    scope_path=ROOT/'audit_native_paired_stumble_table_bounded_source/report.json'
    scope=read(scope_path)
    need(scope['passed'] and len(scope['originalNaturalIntegrationRequirements'])==14 and
         len(scope['originalRemainingWorkGroups'])==6,'Full original natural integration objective preserved')
    pins={}
    def bind(items):
        for p,h in items.items():
            need(sha(p)==h,'Actual unchanged source/native/proof '+p)
            need(p not in pins or pins[p]==h,'Consistent original input hashes')
            pins[p]=h
    bind(scope['inputHashes'])
    cases=[]
    for fighter in ('kano','sonya'):
        for side in (1,2):
            has_owners=(fighter,side)!=('kano',1)
            prefix='audit_native_current_cross_pit_19_owned_audio_'if has_owners else'audit_native_current_cross_pit_19_audio_'
            folder=ROOT/f'{prefix}{fighter}_p{side}_samples'
            report_path=folder/'current_19_audio_report.json'
            meta_path=folder/'result.json';retire_path=folder/'current_19_audio_ram_retirement.json'
            terminal_path=folder/'current_19_audio_terminal_faults.json';identity_path=folder/'native_identity.json'
            report,meta,retired,terminal,identity=map(read,(report_path,meta_path,retire_path,terminal_path,identity_path))
            accepted=report['accepted'];waveform=report['waveform'];own=17 if fighter=='kano'else 18
            native=report['nativeEarnedPitState'];winner=accepted['actualWinnerChannelClockAndRetirement']
            need(report['passed'] and report['currentCrossPit19ChannelFiniteAudioAccepted'] and retired['passed'] and
                 report['candidate']==meta['candidate']=='diagnostic_native_paired_stumble_table_ps7' and
                 meta['fighter']==accepted['fighter']==fighter and meta['side']==accepted['physicalSlot']==side and
                 accepted['identity']==own and meta['guestSHA256']==report['guestSHA256']==scope['proposedGuestSHA256'],
                 'Actual current candidate/whole guest/selected performer and physical slot')
            process=read(folder/'process.json');command=process['command']
            need(meta['exit_code']==0 and meta['samples_enabled'] and meta['guest_writes']==0 and meta['assistance']=='none' and
                 meta['rawAudioRasterVRAMROMCopiesWritten']==0 and meta['input_hashes']==read(folder/'input_hashes_before.json') and
                 (folder/'stderr.log').read_text()=='' and '-samples'in command and '-nosamples'not in command and '-nocheat'in command and
                 '-wavwrite'in command and command[command.index('-wavwrite')+1]=='NUL' and
                 identity==retired['exactNativeTerminal'] and identity['ProcessId']==process['pid'] and
                 identity['ParentProcessId']==process['hostPID'] and identity['createdUnix']>0,
                 'Exact real native birth/parent/command, normal terminal and no assistance/raw copies')
            need(native['passed'] and native['earned_matches']==7 and native['consecutive_fields']==801 and
                 native['native_action']=='FF8BDDE0' and native==accepted['nativePitPhysicalState'] and
                 native['action_frame']==accepted['origin'] and accepted['terminal']==accepted['origin']+1101 and
                 len(report['actualEarnedStateFaultsRejected'])==12 and
                 report['actualEarnedStateFaultsRejected']==accepted['actualEarnedStateFaultsRejected'] and
                 len(accepted['actualAudioSourceWindowFaultsRejected'])==29,
                 'Whole original seven earned matches/801 states/1101 terminal and all original window/state faults')
            callbacks=len(report['pcmHeaders'])
            need(callbacks==len(report['dacHeaders'])==meta['mixedPCMUpdates']==accepted['actualPCMCallbacks']==accepted['actualDACCallbacks']==1006 and
                 accepted['actualChannelStates']==winner['videoChannelStates']==19*1100 and
                 winner['preciseSourceChannelStates']==19*callbacks and winner['passed'] and
                 winner['allRepeatedDoublePositionBitsExact'] and winner['allOtherChannelsIdle'] and
                 winner['consecutiveActiveCallbacks']==100 and winner['fullNativeRetirementAccepted'] and
                 not winner['actualSavedGainSnapshotsAvailable'] and not accepted['actualSavedGainSnapshotsAvailable'],
                 'All19 precise callback/video states, finite winner lifetime and honest unavailable saved-gain coverage')
            need(waveform['passed'] and waveform['differentChannelSamples']==0 and
                 waveform['actualSHA256']==waveform['predictedSHA256']==meta['mixedPCMSHA256']==accepted['actualWholePCMSHA256'] and
                 waveform['comparedStereoFrames']==accepted['exactStereoPCMFrames']==retired['originalStereoFrames']==callbacks*960 and
                 waveform['actualMixedRawPCMByteFaultSuiteAccepted'] and
                 len(waveform['actualCallbackSourceClocks'])==len(waveform['expectedWinnerCallbackStates'])==callbacks and
                 waveform['maximumMixedMagnitude']<1 and waveform['sourceWinnerFrequency']==16000 and
                 waveform['sourceFloat32CompositeGain']==0.21000000834465027 and
                 len(waveform['actualRawMixedPCMFaultsRejected'])==4 and len(waveform['actualMixedSourceOperationFaultsRejected'])==4 and
                 report['actualNativeDACSourceProof']['passed'] and report['actualNativeDACSourceProof']['callbacks']==callbacks and
                 len(report['actualDACFaultsRejected'])==4 and len(report['actualSoundROMFaultsRejected'])==8 and
                 len(report['actualWholeSoundROMProof'])==2 and all(r['bytes']==12582912 and r['everyActualByteComparedInRAM'] and
                     r['wholeOriginalSoundRegionSourceExact']for r in report['actualWholeSoundROMProof']),
                 'Whole actually bound native float/DAC/ROM/source-clock PCM, no clipping/fit/trim and complete fault suites')
            need(retired['originalRAMBoundBeforeRelease'] and retired['originalCaptureRAMDictionaryCleared'] and
                 retired['all19ChannelsAndFivePriorityOwnersRetired'] and retired['originalDACCallbacks']==callbacks and
                 retired['wholeSoundROMBytesPerPhase']==12582912 and terminal['passed'] and
                 len(terminal['actualTerminalFaultsRejected'])==8 and
                 terminal['actualNativeTerminalProof']['terminalFrame']==accepted['terminal'] and
                 terminal['actualNativeTerminalProof']['channels']==19 and terminal['actualNativeTerminalProof']['prioritySlots']==5,
                 'Actual complete original RAM retirement and all added-channel/owner/priority terminal counterexamples')
            owned=None
            if has_owners:
                owned_path=folder/'current_19_owned_voice_queue_rng_report.json';owned=read(owned_path)
                movie=owned['actualNativeMovieAndVoiceOwnership'];queue=owned['wholeOriginalQueueRNG']
                need(owned['passed'] and owned['fighter']==fighter and owned['side']==side and movie['passed'] and
                     movie['ownID']==own and movie['victimID']==35-own and movie['origin']==accepted['origin'] and
                     movie['terminal']==accepted['terminal'] and movie['impact']==movie['enter']+59 and
                     movie['directOwnerFields']==59 and movie['ownMovieDraws']==22 and movie['trueGenderVoiceRoutes']==10 and
                     movie['initialNativeVoice']==(205 if own==17 else 203) and movie['cinematicNativeVoice']==(206 if own==17 else 204) and
                     len(owned['actualOwnerFaultsRejected'])==22 and owned['fullCurrent19WaveformAnd29FaultsRetained'],
                     'Three actual directly observed own cinematic actors and true native gender/voice routes, all owner faults')
                need(queue['passed'] and queue['nativeCoreCalls']==1121 and queue['nativeMainLoopCalls']==1101 and
                     queue['nativeBoundedRNGCalls']==20 and len(queue['actualSoundVariantSelectors'])==8 and
                     len(queue['actualQueueSelections'])==18 and len(queue['actualFaultsRejected'])==36 and
                     queue['allObservedNativeRNGWordsAndChoicesAccepted'] and queue['allObservedEmptyReplacementSlotDecisionsAccepted'] and
                     queue['actualPriorityBranches']['empty']>0 and queue['actualPriorityBranches']['replacement']>0 and
                     sum(queue['actualSelectedSlots'].values())==18 and not owned['allNativePitCuePriorityAndRNGAccepted'] and
                     not owned['nativeSuppressionAndSpecial71Accepted'] and not owned['allMirrorsAndStockVictimsAccepted'] and not owned['fullPortAcceptance'],
                     'Entire original bounded/core RNG and observed queue decisions retained, no unobserved branch coverage')
                bind(owned['inputHashes']);bind({str(owned_path):sha(owned_path)})
            else:
                need(not(folder/'current_19_owned_voice_queue_rng_report.json').exists() and
                     not report['cinematicVictimAudioOwnershipAccepted'] and not report['allNativePitCuePriorityAndRNGAccepted'],
                     'KanoP1 original waveform baseline is NOT direct owner/RNG observation')
            need(not report['fullPortAcceptance'] and not report['allStageFinishersAccepted'] and not report['fullStageArtAccepted'] and
                 not report['publicPlayableChanged'] and not retired['fullPortAcceptance'] and not retired['publicPlayableChanged'] and
                 not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in folder.rglob('*')if p.is_file()),
                 'Finite actual sound contexts, not wider stage/port/release acceptance or raw media copies')
            for collection in (meta['input_hashes'],report['mixedWaveformSourceInputHashes'],retired['inputHashes'],terminal['inputHashes'],report.get('additionalAnalysisInputHashes',{})):
                bind(collection)
            for p in(report_path,meta_path,retire_path,terminal_path,identity_path):bind({str(p):sha(p)})
            cases.append(dict(fighter=fighter,physicalSlot=side,capture=str(folder),stereoFrames=accepted['exactStereoPCMFrames'],
                              full19ChannelWaveformAccepted=True,directNativeMovieVoiceAndObservedRNGAccepted=has_owners,
                              actualWindowFaults=29,actualEarnedFaults=12,actualTerminalFaults=8))
    for p in(Path(__file__).resolve(),Path(census.__file__).resolve(),scope_path):bind({str(p):sha(p)})
    result=dict(passed=True,cases=cases,finiteBothCharactersBothSlotsCurrent19PitWaveformAccepted=True,
                exactStereoFrames=sum(c['stereoFrames']for c in cases),directOwnedAudioContexts=3,
                allFourDirectOwnerRNGContextsAccepted=False,actualWindowFaults=116,actualEarnedFaults=48,
                actualRawPCMFaults=16,actualSourceOperationFaults=16,actualTerminalFaults=32,
                actualDirectOwnerFaults=66,actualObservedQueueRNGFaults=108,
                laterVisualClearingAndRejoinAccepted=False,allMirrorsAndStockVictimsAccepted=False,
                allNativePitCuePriorityAndRNGAccepted=False,allStageFinishersAccepted=False,fullPortAcceptance=False,
                originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],inputHashes=pins,
                newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    report=run()
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','originalNaturalIntegrationRequirements','originalRemainingWorkGroups')},indent=2))
