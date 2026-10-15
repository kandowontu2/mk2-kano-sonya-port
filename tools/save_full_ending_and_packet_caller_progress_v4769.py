"""Additive whole-goal checkpoint: full ending pixels and native sound callers.

All original scope and immutable evidence persist. Finite P2 video and four
finisher audio contexts never become all-context or finished-release claims.
"""
import json,subprocess
from pathlib import Path
import save_both_ending_clock_progress_v4759 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4760_both_ending_clock_progress/progress.json']
OUT=ROOT/'audit_v4770_full_ending_and_packet_caller_progress'

def main():
    need(not OUT.exists(),'Fresh immutable full-goal additive journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for p,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent original entire-goal source/evidence chain');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'Every inherited native/source/public/playable evidence byte unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or wanted==actual)and(key not in inherited or inherited[key]==actual)and
             (key not in pins or pins[key]==actual),'Exact immutable additive source/evidence byte')
        if key not in inherited:pins[key]=actual
    for p in[BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(p)
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_cpu_cycle_campaign_ram_v4752.py|audit_v4753_|run_scorpion_packet_caller_ram_v4762.py|audit_v4765_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh authoritative native/collector command census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    endings=[]
    for fighter,fields,clocks,stores,cold,session in(('kano',3040,139566,4407,58,22694),('sonya',3043,141631,4410,78,53444)):
        folder=ROOT/f'audit_v4753_{fighter}_p2_ending_cpu_cycle_ram'
        reportpath=ROOT/f'audit_v4754_{fighter}_p2_ending_cpu_cycle_checked/report.json'
        bridgepath=ROOT/f'audit_v4758_{fighter}_complete_native_ending_pixels_and_hardware_checked/report.json'
        process=json.loads((folder/'process.json').read_text());pin(folder/'process.json');pin(folder/'input_hashes_before.json')
        for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
        entry=dict(fighter=fighter,physicalSlot=2,identity=17 if fighter=='kano'else 18,execSession=session,
          nativePID=process['pid'],capture=str(folder),pixelReport=str(reportpath),hardwareBridge=str(bridgepath),
          completeWholeNativeVideoAccepted=False,independentCompleteHardwareBridgeAccepted=False,
          allP1P2EndingContextsAccepted=False,independentStockChoreographyAccepted=False)
        if reportpath.exists():
            r=json.loads(reportpath.read_text());meta=json.loads((folder/'result.json').read_text());pin(reportpath)
            need(r['passed']and meta['exit_code']==0 and not meta['endingModelErrors']and
                 r['exactConsecutiveNativeVideoFields']==meta['observedEndingRGBFields']==meta['exactContinuousEndingFields']==fields and
                 r['exactRGBPixels']==fields*101600 and r['exactVRAMWords']==fields*262144 and
                 r['actualAttractRendererFields']==300 and r['actualRasterClocks']==clocks-1 and
                 r['actualOriginalDisplayIOStores']==stores and meta['actualNativeFrameCallbacks']==cold and
                 r['oneInitialBaseOnly']and r['comparisonTargetsNeverReanchor']and r['originalColdNativeCampaignExactlyUnchanged']and
                 r['originalQualifiedEarlyLatePagesPresent']and len(r['actualNativePixelFaultsRejected'])==2 and
                 r['completeCurrentP2EndingAttractNativeRendererVideoAccepted']and not r['fullPortAcceptance'],
                 'Actual terminal0, every complete ending/all300attract RAM VRAM/RGB field, cold native campaign and two real raw-bit faults')
            for p,h in r['inputHashes'].items():pin(p,h)
            entry.update(completeWholeNativeVideoAccepted=True,actualTerminalExit=0,actualNativeVideoFields=fields,
              exactRGBPixels=fields*101600,exactVRAMWords=fields*262144,actualAttractFields=300,
              actualColdRGBEvents=cold,actualRawBitFaultsRejected=2,noComparisonTargetReanchor=True)
            if bridgepath.exists():
                bridge=json.loads(bridgepath.read_text());pin(bridgepath)
                need(bridge['passed']and bridge['completeActualMetadataFields']==fields and
                     bridge['actualNativeClockRecords']==clocks and bridge['completedRendererClockRecords']==clocks-1 and
                     bridge['actualNativeDisplayIOStores']==stores and bridge['actualAttractFields']==300 and
                     len(bridge['actualMetadataFaultsRejected'])==27 and len(bridge['actualTerminalFaultsRejected'])==8 and
                     len(bridge['actualNativePixelBitFaultsRejected'])==2 and bridge['everyRawVRAMWordAndRGBPixelAccepted']and
                     bridge['everyQualifiedOriginalEndingPageRetained']and bridge['metadataNeverSubstitutedForPixels']and
                     bridge['fullEndingVRAMRGBPixelsAccepted']and not bridge['dummyVRAMUsed']and not bridge['fullPortAcceptance'],
                     'Independent complete original hardware/instruction/IO ledger and35real metadata faults agree with every actual raw field')
                for p,h in bridge['inputHashes'].items():pin(p,h)
                entry.update(independentCompleteHardwareBridgeAccepted=True,actualNativeClocks=clocks,
                  actualOriginalIOStores=stores,actualMetadataAndTerminalFaultsRejected=35)
        else:
            native=any(row['ProcessId']==process['pid']and str(folder)in row['CommandLine']for row in live)
            collector=any(row['Name']=='python.exe'and '4752.py'in row['CommandLine']and f'--fighter {fighter}'in row['CommandLine']for row in live)
            need(native and collector,'Pending native video only after exact currently live native/collector process commands')
            entry.update(nativeLiveNow=True,collectorLiveNow=True)
        endings.append(entry)
    need(endings[0]['completeWholeNativeVideoAccepted']and endings[0]['independentCompleteHardwareBridgeAccepted'],
         'Actual Kano full video and independent whole hardware bridge are mandatory, not inherited metadata alone')
    sourcepath=ROOT/'audit_v4764_scorpion_packet_caller_source_checked/report.json'
    source=json.loads(sourcepath.read_text());pin(sourcepath)
    need(source['passed']and source['actualAudioTapsRetained']==15 and source['addedReadOnlyPacketStackTaps']==1 and
         source['totalNativeObserverTaps']==16 and source['originalNativeAudioRecordSchemasUnchanged']and
         len(source['actualSourceFaultsRejected'])==9 and source['originalSourceFaultsRetained']==7,
         'Every original observer/controller retained; actual read-only stack tap and nine source faults qualified')
    for p,h in source['inputHashes'].items():pin(p,h)
    audiopath=ROOT/'audit_v4768_scorpion_packet_callers_checked/report.json'
    audio=json.loads(audiopath.read_text());pin(audiopath)
    need(audio['passed']and audio['actualContexts']==4 and audio['actualNativeStackWitnesses']==112 and
         audio['actualDirectOriginalPacketCallers']==16 and audio['actualQueueOriginalPacketCallers']==96 and
         audio['actualCallerFaultsRejected']==76 and audio['directPacketCallerOriginsAccepted']and
         audio['wholeOriginal72AudioFaultsRetained']and audio['everyOriginalAudioAndPCMRecordUnchanged']and
         not audio['stockWholeWaveformReferenceAccepted']and not audio['allFinisherVictimAudioAccepted']and not audio['fullPortAcceptance'],
         'All four actual caller contexts, original CALLA/CALLR instructions, full prior audio gates and76real native caller faults; no universal audio claim')
    for p,h in audio['inputHashes'].items():pin(p,h)
    cases=[]
    for case in audio['cases']:
        fighter,side=case['fighter'],case['side']
        proofpath=ROOT/f'audit_v4766_scorpion_secondary_{fighter}_p{side}_packet_caller_observed/report.json'
        proof=json.loads(proofpath.read_text());pin(proofpath)
        need(proof['passed']and proof['completeMixedPCMEqualSamplesOnOff']and proof['everyOriginalColdStateAndRGBEventUnchanged']and
             proof['everyNativePacketCallerObserved']and len(proof['actualPacketCallerWitnesses'])==28 and
             proof['actualPCMUpdates']==686 and proof['nativeDeliveredBytes']==56,
             'Every actual samples-on/off non-silent full-RAM stereo waveform, cold states/RGB and all28native stack witnesses')
        for p,h in proof['inputHashes'].items():pin(p,h)
        cases.append(dict(fighter=fighter,physicalVictimSlot=side,identity=case['identity'],report=str(proofpath),
          actualNativePairTerminalExit=[0,0],actualStackWitnesses=28,actualDirectCallerInstructions=case['callerProof']['sourceQualifiedOriginalCallInstructions'],
          actualCallerFaultsRejected=len(case['actualCallerFaultsRejected']),wholeMixedPCMEqualSamplesOnOff=True,
          everyPriorNativeAudioAndPCMDigestRecordUnchanged=True,allIndependentStockAudioContextsAccepted=False))
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read with4557 and every additive journal; every original full-scope requirement, source/evidence pin, finite acceptance, exclusion and public playable artifact persists. This adds actual full ending video and complete original sound caller witnesses; it does not complete the port.',
      remaining=base['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      previousGoalTurnClassification='no progress: acknowledgment-only reply. Revalidated actual current process commands and complete Kano video/hardware result before the next safe native verification work.',
      thisGoalTurnClassification='progress: added one strictly read-only packet caller stack observer while retaining all15 original audio taps, original physical controls, full PCM/state/guest/RGB transport and all prior source/fault gates. All eight new native captures terminal0 and all four paired full-RAM waveforms passed. Source-qualified every112actual CALLA/CALLR packet origin including16previously unqualified direct packets; every original voice/channel/queue/packet/DCS/PCM digest record unchanged. Rejected76actual caller/instruction faults, retaining72original audio faults and nine new source faults. Full Kano3040field ending/attract RAM video and independent139566clock/4407IOstore hardware bridge accepted; Sonya exact process/capture status recorded below.',
      actualEndingVideoAndHardware=endings,actualPacketCallerAudio=dict(report=str(audiopath),cases=cases,
        actualContexts=4,actualNativeStackWitnesses=112,actualDirectNativeCallers=16,actualQueueNativeCallers=96,
        realCallerInstructionFaultsRejected=76,wholeOriginalAudioFaultsRetained=72,originalColdPhysicalControlsAnd62RGBUnchanged=True,
        allOriginalVoiceSelectorQueueOwnedPacketDSPAndPCMRecordsUnchanged=True,directPacketCallerOriginsAccepted=True,
        independentStockWholeWaveformAccepted=False,allFinisherVictimAudioAccepted=False),
      liveJobsAuthoritativelyObservedNow=live,candidateAndPublicBuildChanged=False,newBuilds=0,rawMediaFilesWritten=0,
      newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      nextAction='If Sonya4752 is pending, poll exact53444 and its current native process, never restart for timeout. Require actual native terminal0/all3043whole VRAM/RGB fields and both rawbit faults before running4757 --fighter sonya into unused4758S. Both finite current P2 ending videos must remain distinct from allP1/full stock choreography/all cinematics. Complete caller proof4768 now closes all four direct native packet origins for the existing four Scorpion secondary contexts; independent stock waveform, broader finisher/victim/stage audio and all other original scope groups remain. Continue the original Pit/Tomb/move art/grounding/shadows/CPU/repeated/KO/otherfinisher/morph/secret/cinematic/selection/ladder/names/release work; no public candidate promotion from these finite results.',
      cleanupAccounting='Only compressed source/text/digests and journal; raw ROM/VRAM/RGB/PCM remains RAM-only. No new build/playable/ROM/archive copies or deletion; prior32.49GiB reclamation is not recounted.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'All original full-goal groups and additive actual source/evidence bytes retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),
      completeWholeNativeEndingVideo=[r['fighter']for r in endings if r['completeWholeNativeVideoAccepted']],
      completeIndependentEndingHardwareBridge=[r['fighter']for r in endings if r['independentCompleteHardwareBridgeAccepted']],
      actualNativePacketCallerContexts=4,actualSourceQualifiedStackWitnesses=112,actualCallerFaults=76,
      newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
