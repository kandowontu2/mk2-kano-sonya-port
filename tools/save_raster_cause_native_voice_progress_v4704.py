"""Additive full-goal journal: actual raster cause and four native voice gates."""
import json,subprocess
from pathlib import Path
import save_ending_clear_audio_progress_v4685 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4686_ending_clear_audio_progress/progress.json']
OUT=ROOT/'audit_v4705_raster_cause_native_voice_progress'

def main():
    need(not OUT.exists(),'Fresh immutable additive full-goal journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for path,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(path not in inherited or inherited[path]==h,'Consistent full-goal native/source pin chain');inherited[path]=h
    need(all(sha(path)==h for path,h in inherited.items()),'All original whole-goal source/native/public bytes unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);h=sha(path)
        need((wanted is None or h==wanted)and(key not in inherited or inherited[key]==h)and
             (key not in pins or pins[key]==h),'Exact unchanged additive source/evidence pin')
        if key not in inherited:pins[key]=h
    for path in[BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(path)
    audio_path=ROOT/'audit_v4701_scorpion_secondary_native_audio_checked/report.json'
    raster_path=ROOT/'audit_v4703_actual_ending_clear_raster_cause_checked/report.json'
    audio=json.loads(audio_path.read_text());raster=json.loads(raster_path.read_text())
    need(audio['passed']and audio['actualContexts']==4 and audio['actualSelectorsSourceBound']==96 and
         audio['actualNativeDCSBytesDelivered']==224 and audio['actualRowFaultsRejected']==72 and
         audio['bothTrueVictimNativeVoiceGendersBothSlotsAccepted']and audio['wholeGenericPCMChannelsPacketsDSPRetained']and
         not audio['directPacketCallerOriginsAccepted']and not audio['stockWholeWaveformReferenceAccepted']and
         not audio['allFinisherVictimAudioAccepted']and not audio['fullPortAcceptance'],
         'All four finite true17/18 native voice/effect/table/packet/DSP/pairedPCM contexts; broader exclusions retained')
    need(raster['passed']and raster['singleFieldSourceTimingCauseAccepted']and raster['actualBeamBuckets']==260 and
         raster['actualNativeCPUWrites']==67658 and raster['exactActualEndVRAMWords']==262144 and
         raster['exactActualRGBPixels']==101600 and len(raster['actualBeamAndContextFaultsRejected'])==25 and
         not raster['wholeEndingSingleInitialBaseAccepted']and not raster['fullEndingRendererVideoAccepted']and
         not raster['actualRawPixelBitFaultsQualified']and not raster['fullPortAcceptance'],
         'Actual finite raster cause independently explains all84pixels, not whole-ending acceptance or raw bit-fault proof')
    for path,proof in((audio_path,audio),(raster_path,raster)):
        pin(path)
        for p,h in proof['inputHashes'].items():pin(p,h)
    # Preserve the executed failed selector-interval assumption as failed;
    # fresh4700 fixes attribution only, not the native game or original logs.
    failed_path=ROOT/'audit_v4699_scorpion_secondary_native_audio_checked/report.json'
    failed=json.loads(failed_path.read_text());need(not failed['passed'],'Actual earlier audio checker failure retained');pin(failed_path)
    cleanup_path=ROOT/'workspace_cleanup_followup_2026-10-05/verified_summary.json'
    cleanup=json.loads(cleanup_path.read_text());pin(cleanup_path)
    need(cleanup['passed']and cleanup['removedObsoleteFolders']==267 and cleanup['reclaimedAllocatedBytes']==34889808066 and
         cleanup['currentCMDBootPassed']and cleanup['userSettingsUnchanged'],
         'User-requested prior32.49GiB cleanup verified, not recounted as new reclaim')
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_clear_projection_ram_v4693.py|audit_v4696_|verify_scorpion_secondary_native_audio_v4700.py' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0 and not census.stdout.strip(),'Actual fresh exact process census, both jobs terminal and not restarted')
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read together with the base4557 and all listed additive journals. No original requirement, prior finite result, exclusion or pin is replaced. Only prior live projection and voice-source pending statuses are resolved here.',
      remaining=base['remaining'],newInputHashes=pins,
      sourceQualifiedFiniteScorpionSecondaryAudio=dict(report=str(audio_path),contexts=4,sourceBoundSelectors=96,
        actualDCSBytesDelivered=224,actualRowFaultsRejected=72,trueKanoSonyaNativeGenderVoicesBothSlotsAccepted=True,
        wholeSamplesOnOffPCMBytesExactlyEqual=True,originalNativeStateAnd62RGBUnchanged=True,
        directlyDispatchedPacketCallerOriginsAccepted=False,stockWholeWaveformReferenceAccepted=False,
        allFinisherVictimAudioAccepted=False),
      actualSingleClearFieldCause=dict(report=str(raster_path),nativeExit=0,execSession=73378,execTerminalConsumed=True,
        frame=58183,staticEndVRAMMismatchPixels=84,exactSourceTimedRGBPixels=101600,exactReplayedEndVRAMWords=262144,
        nativeCPUWrites=67658,actualBeamAndContextFaultsRejected=25,
        sourceDerivedTails=raster['independentSourceTimingTails'],
        cause='Original CPUclear writes during scanout. Indexed screenshot retains44/28/12pixels from the first three earlier rows. End-of-frame VRAM crop is not the displayed indexed surface.',
        onePrecedingVRAMDiagnosticBaseOnly=True,wholeEndingOneInitialBaseAccepted=False,rawPixelBitFaultsQualified=False),
      preservedWholeEndingCounterexample=dict(report=str(ROOT/'audit_v4650_kano_p2_ending_display_actual_metadata_checked/report.json'),
        exactWholeFields=1887,allActualRendererFieldsObserved=3040,firstFailedFrame=58183,wholeKanoEndingAccepted=False,
        wholeSonyaEndingAccepted=False),
      priorRequestedCleanup=dict(report=str(cleanup_path),previouslyReclaimedAllocatedBytes=34889808066,
        removedObsoleteFolders=267,alreadyReportedGiB=32.49,currentCMDBootPassedAtCleanup=True,
        currentBuildsROMsSourceSettingsPreserved=True,reclaimRepeatedThisTurn=False),
      noRelevantLiveJobsAtJournal=True,candidateAndPublicBuildChanged=False,newBuilds=0,rawMediaFilesWritten=0,
      newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      thisGoalTurnClassification='progress: actual fresh native RAM projection reconstructs every pixel and end word of the later84pixel clear field; original beam timing independently explains44/28/12tailpixels and25actual context/beam faults are rejected. Four complete Scorpion-secondary native gender/effect/queue/PCM contexts source-qualified with72actual row faults. No game patch introduced for checker assumptions.',
      nextAction='Retain the whole3642/4645 one-initial-base CPU/DMA/shift/fullVRAM pipeline and original controls. Add generic actual per-operation raster clocks and source-bound indexed scanline replay, not58183 special-casing, target reanchor, buffer search, tolerance or omitted fields. Qualify real raw pixel/VRAM/clock faults in RAM, then observe the complete Kano and Sonya ending/attract windows. Four direct audio caller origins and independent stock waveforms remain unaccepted. Preserve all five original full-goal groups, final integrated selection/ladder/names/audio regression and dependency-aware final cleanup/release.',
      cleanupAccounting='Only small compressed source/text/digests/additive journal. No new raw media, game build, deletion, archive or historical reclaim recounted.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Every new pin unchanged and all original remaining groups retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),finiteNativeAudioContexts=4,
      singleClearFieldCauseAccepted=True,wholeEndingAccepted=False,fullPortAcceptance=False,newBuilds=0,newRawMedia=0),indent=2),flush=True)

if __name__=='__main__':main()
