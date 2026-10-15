"""Additive full-goal journal: real ending counterexample and native audio pairs."""
import json,subprocess
from pathlib import Path
import save_stock_matrix_ending_schema_progress_v4653 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4654_stock_matrix_ending_schema_progress/progress.json']
OUT=ROOT/'audit_v4686_ending_clear_audio_progress'

def main():
    need(not OUT.exists(),'Fresh immutable compact additive journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for path,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(path not in inherited or inherited[path]==h,'Consistent original whole-goal proof chain')
            inherited[path]=h
    need(all(sha(p)==h for p,h in inherited.items()),'Every inherited native/source/public/proof byte unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or actual==wanted)and(key not in inherited or inherited[key]==actual),'Exact consistent new/inherited logical-byte pin')
        if key not in inherited:pins[key]=actual
    for p in [BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(p)
    ending_case=ROOT/'audit_v4649_kano_p2_ending_display_actual_metadata_ram'
    ending_report=ROOT/'audit_v4650_kano_p2_ending_display_actual_metadata_checked/report.json'
    meta=json.loads((ending_case/'result.json').read_text());failed=json.loads(ending_report.read_text());pin(ending_report)
    records=json.loads((ending_case/'ending_continuous_records.json').read_text())
    need(meta['exit_code']==0 and meta['observedEndingRGBFields']==3040 and meta['exactContinuousEndingFields']==1887 and
         [r['frame']for r in records]==list(range(56296,58183))and len(meta['endingModelErrors'])==1 and
         'frame=58183 'in meta['endingModelErrors'][0]['line']and not failed['passed'],
         'Actual terminal0 complete native observation,1887 exact whole fields, late58183 pixel counterexample, no ending acceptance')
    for p,h in meta['input_hashes'].items():pin(p,h)
    for p in ending_case.rglob('*'):
        if p.is_file():pin(p)
    audio=[]
    for fighter,side in(('kano',1),('sonya',2),('kano',2),('sonya',1)):
        report_path=ROOT/f'audit_v4668_scorpion_secondary_{fighter}_p{side}_audio_observed/report.json'
        entry=dict(fighter=fighter,side=side,report=str(report_path),terminalQualifiedObservation=False,
                   voiceCallerFidelityAccepted=False,stockWholeWaveformReferenceAccepted=False)
        if report_path.exists():
            proof=json.loads(report_path.read_text());pin(report_path)
            entry['passed']=proof['passed']
            if proof['passed']:
                need(proof['completeMixedPCMEqualSamplesOnOff']and proof['everyOriginalColdStateAndRGBEventUnchanged']and
                     proof['actualPCMUpdates']==686 and proof['actualStereoFrames']==658560 and proof['nativeDeliveredBytes']==56 and
                     all(r['allIdle']and not r['activeStates']for r in proof['importedChannels'])and
                     proof['state']['identity']==(17 if fighter=='kano'else 18)and proof['state']['victimSlot']==side and
                     not proof['sourceQualifiedVoiceEffectCallerFidelity']and not proof['fullPortAcceptance'],
                     'Actual earned true17/18/960field/62RGB/full paired waveform/DCS observation with fidelity exclusions')
                for p,h in proof['inputHashes'].items():pin(p,h)
                entry.update(terminalQualifiedObservation=True,actualNativeOrigin=proof['nativeAudioOrigin'],
                             originalColdNativeStateAnd62RGBUnchanged=True,actualPCMUpdates=686,actualDCSBytesDelivered=56)
            else:entry['error']=proof['error']
        audio.append(entry)
    first=ROOT/'audit_v4662_scorpion_secondary_kano_p1_audio_observed/report.json'
    boot=ROOT/'audit_v4661_scorpion_secondary_kano_p1_audio_samples/result.json'
    invalid=json.loads(first.read_text());native=json.loads(boot.read_text())
    need(not invalid['passed']and native['exit_code']==3 and native['mixedPCMUpdates']==0,
         'First audio observer literal-assertion preboot failure retained, not relabelled as game/audio evidence')
    pin(first);pin(boot)
    for p,h in native['input_hashes'].items():pin(p,h)
    for p in boot.parent.rglob('*'):
        if p.is_file():pin(p)
    preflight=ROOT/'audit_v4666_scorpion_secondary_audio_guard_source_checked/report.json'
    guard=json.loads(preflight.read_text());pin(preflight)
    need(guard['passed']and guard['actualAudioTapsRetained']==15 and len(guard['actualSourceFaultsRejected'])==7 and
         guard['actualFailedNativeBootPreserved']and guard['onlyOneRuntimeLexicalGuardChanged']and not guard['nativeAudioAcceptance'],
         'Whole retained audio/controller source and corrected literal-vs-write-call guard; all seven source faults preserved')
    for p,h in guard['inputHashes'].items():pin(p,h)
    beam_preflight=ROOT/'audit_v4682_ending_clear_beam_source_checked/report.json'
    beam=json.loads(beam_preflight.read_text());pin(beam_preflight)
    need(beam['passed']and beam['actualPriorFailedFrame']==58183 and beam['sameOriginalColdCampaignAndWholeGuest']and
         beam['wholeOriginalCPUClearRoutineUnchanged']and beam['observationFields']==21 and not beam['nativeRasterCauseAccepted'],
         'Same earned cold policy and actual original clear code,21field read-only beam probe, no cause/pixel acceptance before observation')
    for p,h in beam['inputHashes'].items():pin(p,h)
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_clear_beam_probe_ram_v4681.py|audit_v4683_|run_scorpion_secondary_audio_ram_v4664.py|audit_v4667_|run_ending_display_latch_campaign_ram_v4646.py|audit_v4649_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Exact fresh authoritative process census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    need(not any('4646.py'in r['CommandLine']or'audit_v4649_'in r['CommandLine']for r in live),
         'Actual prior full ending terminal, not timeout-inferred or restarted')
    for fighter,side in(('kano',2),('sonya',1)):
        for suffix in('samples','nosamples'):
            folder=ROOT/f'audit_v4667_scorpion_secondary_{fighter}_p{side}_audio_{suffix}'
            for leaf in('input_hashes_before.json','process.json'):
                if (folder/leaf).exists():pin(folder/leaf)
            if (folder/'input_hashes_before.json').exists():
                for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
    probe=ROOT/'audit_v4683_kano_ending_clear_beam_probe_ram'
    for leaf in('input_hashes_before.json','process.json'):
        if (probe/leaf).exists():pin(probe/leaf)
    if (probe/'input_hashes_before.json').exists():
        for p,h in json.loads((probe/'input_hashes_before.json').read_text()).items():pin(p,h)
    beam_result=ROOT/'audit_v4684_kano_ending_clear_beam_probe_observed/report.json'
    beam_status=dict(capture=str(probe),report=str(beam_result),execSession=37176,
                     liveNow=any('4681.py'in r['CommandLine']or'audit_v4683_'in r['CommandLine']for r in live),
                     actualRasterCauseAccepted=False,fullEndingVideoAccepted=False)
    if beam_result.exists():
        result=json.loads(beam_result.read_text());pin(beam_result);beam_status['passed']=result['passed']
        if result['passed']:
            need(result['actualDiagnosticFields']==21 and result['everyOriginalColdNativeEventAndRGBUnchanged']and
                 not result['fullEndingRendererVideoAccepted']and not result['fullPortAcceptance'],'Terminal narrow diagnosis, never full renderer acceptance')
            for p,h in result['inputHashes'].items():pin(p,h)
        else:beam_status['error']=result['error']
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read together with4557/4591/4611/4619/4636/4654. All original requirements/pins/exclusions persist. This replaces stale live full-ending status and adds finite paired audio observations/clear-beam diagnosis only.',
      remaining=base['remaining'],newInputHashes=pins,
      fullEndingActualTerminal=dict(nativeExit=0,execSession=19289,execTerminalConsumed=True,observerFields=3040,
        consecutiveWholePixelVRAMFields=1887,firstPixelCounterexampleFrame=58183,lastExactFrame=58182,report=str(ending_report),wholeEndingAccepted=False,
        newEvidence='Earlier DPYADR-based start correction crosses old57416 failure. Later58183 held frame fails RGB after exact VRAM replay during original CPU clear. No pixel tolerance, field omission, buffer search, reanchor or game patch introduced.'),
      finiteScorpionSecondaryAudioObservations=audio,
      correctedAudioObserverSource=str(preflight),firstAudioObserverBootFailurePreserved=str(first),
      newEndingClearBeamProbe=beam_status,liveJobsAuthoritativelyObservedNow=live,
      candidateAndPublicBuildChanged=False,newBuilds=0,rawMediaGuestROMCopies=0,newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      thisGoalTurnClassification='progress: actual full ending terminal exposes new later58183 counterexample after1887 exact fields and changes next action to bounded original-clear beam diagnosis; KanoP1 and SonyaP2 full native paired audio observed, other required slots dispatched with unchanged controls; failed observer preboot guard corrected and actual7fault source proof retained.',
      nextAction='Poll exact37176 clear/beam job first, and missing-slot64985(KanoP2)/59180(SonyaP1) audio jobs if still live. Never restart for observation timeout. Source-qualify actual native voice/effect/queue/direct-caller routes and real row faults from completed audio, including missing slots. Resolve58183 raster-time versus end-VRAM hypothesis from actual21field CPU beam ledger and source, then retain entire one-initial-base integer CPU/DMA/shift/fullVRAM pipeline and add source-bound per-scanline RGB if needed. Do not rerun or call whole endings accepted until real counterexample is resolved; Sonya whole ending remains missing. Preserve all five full-goal groups, natural game/control semantics, final combined selection/ladder/names/audio regression, dependency-aware cleanup/refreshed final ZIP.',
      cleanupAccounting='New evidence/source/digests compressed before writes; raw guest/RGB/VRAM/PCM RAM-only. Small additive journal, no full checkpoint duplicate or build/raw-media copies. No historic disk reclaim recounted.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Full scope and every new logical source/evidence pin unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),endingWholeAccepted=False,
      endingExactFields=1887,firstFailedFrame=58183,completedFiniteAudioPairs=sum(c['terminalQualifiedObservation']for c in audio),
      liveJobs=live,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
