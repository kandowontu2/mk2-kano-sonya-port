"""Additive whole-goal journal: six-context renderer and actual ending schema."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'audit_v4557_secondary_state_video_full_scope_checkpoint/checkpoint.json'
PARENTS=[ROOT/'audit_v4591_render_failure_scene_progress/progress.json',
         ROOT/'audit_v4611_secondary_render_latch_probe_progress/progress.json',
         ROOT/'audit_v4619_latch_cause_four_renderer_progress/progress.json',
         ROOT/'audit_v4636_ending_hardware_stock_renderer_progress/progress.json']
OUT=ROOT/'audit_v4654_stock_matrix_ending_schema_progress'

def sha(path):
    with Path(path).open('rb')as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    need(not OUT.exists(),'Fresh immutable compact additive journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for p in PARENTS:
        for path,h in json.loads(p.read_text())['newInputHashes'].items():
            need(path not in inherited or inherited[path]==h,'Consistent inherited full-goal proof graph')
            inherited[path]=h
    need(all(sha(p)==h for p,h in inherited.items()),'Every original full-goal source/evidence/public input unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or wanted==actual)and(key not in inherited or inherited[key]==actual),'Consistent exact inherited/current byte pin')
        if key not in inherited:pins[key]=actual
    for p in [BASE,*PARENTS,Path(__file__).resolve()]:pin(p)
    matrix_path=ROOT/'audit_v4652_complete_scorpion_secondary_renderer_matrix_checked/report.json'
    matrix=json.loads(matrix_path.read_text());pin(matrix_path)
    need(matrix['passed']and matrix['wholeFiniteCurrentVsStockRendererMatrixAccepted']and matrix['actualContexts']==6 and
         matrix['actualConsecutiveNativeRendererFields']==3342 and len(matrix['actualMatrixFaultsRejected'])==43 and
         matrix['actualNativeBitmapFaultsRetained']==12 and matrix['everySameSlotOriginalNativeCooperativeCallbackSignatureEqual']and
         not matrix['independentArtAllArenaAlternateGroundAudioAccepted']and not matrix['fullPortAcceptance'],
         'Entire finite six-context renderer/current-stock callback/43actual matrix faults/12actual pixel faults, broad exclusions retained')
    for p,h in matrix['inputHashes'].items():pin(p,h)
    schema_path=ROOT/'audit_v4648_ending_display_actual_metadata_source_checked/report.json'
    schema=json.loads(schema_path.read_text());pin(schema_path)
    need(schema['passed']and schema['actualNativeMetadataControl']['actualTerminalNativeFields']==3040 and
         len(schema['actualNativeMetadataControl']['actualNativeContextFaultsRejected'])==7 and
         schema['actualNativeMetadataControl']['actualAttractRendererFields']==300 and
         len(schema['originalActualHardwareFaultControl']['actualHardwareFaultsRejected'])==4 and
         len(schema['actualObserverSourceFaultsRetained'])==7 and not schema['nativeEndingVideoAcceptance'],
         'All actual emitted metadata/context fields and complete source/hardware/fault gates, never native video from metadata')
    for p,h in schema['inputHashes'].items():pin(p,h)
    phase_path=ROOT/'audit_v4656_actual_ending_context_phase_checked/report.json'
    phase=json.loads(phase_path.read_text());pin(phase_path)
    need(phase['passed']and len(phase['actualRendererPhaseFaultsRejected'])==4 and phase['actualAttractRendererFields']==300 and
         phase['actualLastCompletedRendererField']==59335 and phase['actualNativeStop']==59336 and
         phase['everyOriginalColdNativeCampaignEventAndRGBExactlyUnchanged']and not phase['completeNativeEndingRendererVideoAccepted'],
         'Actual native stop/callback phase/order/four real faults and unchanged cold native events, no fabricated post-exit callback')
    for p,h in phase['inputHashes'].items():pin(p,h)
    failed_path=ROOT/'audit_v4623_kano_p2_ending_display_latch_checked/report.json';failed=json.loads(failed_path.read_text());pin(failed_path)
    old_case=ROOT/'audit_v4622_kano_p2_ending_display_latch_ram';old_meta=json.loads((old_case/'result.json').read_text())
    need(not failed['passed']and old_meta['exit_code']==0 and old_meta['observedEndingRGBFields']==3040 and
         old_meta['exactContinuousEndingFields']==0 and len(old_meta['endingModelErrors'])==1,
         'Actual old source-schema failure preserved; real emulator0 does not imply pixel acceptance')
    for p in (ROOT/'tools/qualify_stock_scorpion_secondary_native_scene_v4640.py',
              ROOT/'tools/qualify_stock_scorpion_secondary_native_scene_v4644.py'):
        pin(p)
    census_command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_display_latch_campaign_ram_v4646.py|audit_v4649_kano_p2_ending_display_actual_metadata_ram|run_stock_scorpion_secondary_native_scene_v4639.py|audit_v4642_|run_ending_display_latch_campaign_ram_v4617.py|audit_v4622_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',census_command],capture_output=True,text=True)
    need(census.returncode==0,'Exact current process census, no timeout terminal inference')
    live=json.loads(census.stdout)if census.stdout.strip()else []
    if isinstance(live,dict):live=[live]
    need(not any('4639.py'in r['CommandLine']or'audit_v4642_'in r['CommandLine']or
                 '4617.py'in r['CommandLine']or'audit_v4622_'in r['CommandLine']for r in live),
         'Actual prior stock and failed-schema ending jobs terminal, not restarted')
    ending_live=any('4646.py'in r['CommandLine']or'audit_v4649_'in r['CommandLine']for r in live)
    ending=dict(capture=str(ROOT/'audit_v4649_kano_p2_ending_display_actual_metadata_ram'),
                report=str(ROOT/'audit_v4650_kano_p2_ending_display_actual_metadata_checked/report.json'),
                execSession=19289,liveNow=ending_live,completeNativeEndingRendererVideoAccepted=False)
    new_report=Path(ending['report'])
    if not ending_live and new_report.exists():
        proof=json.loads(new_report.read_text());pin(new_report);ending['passed']=proof['passed']
        if proof['passed']:
            need(proof['completeCurrentP2EndingAttractNativeRendererVideoAccepted']and proof['everyVisibleStartDerivedFromActualHardware']and
                 proof['actualAttractRendererFields']==300 and not proof['fullPortAcceptance'], 'Whole actual renderer/video success only')
            for p,h in proof['inputHashes'].items():pin(p,h)
            ending.update(completeNativeEndingRendererVideoAccepted=True,exactFields=proof['exactConsecutiveNativeVideoFields'])
        else:ending['error']=proof['error']
    case=Path(ending['capture'])
    if (case/'input_hashes_before.json').exists():
        pin(case/'input_hashes_before.json');pin(case/'process.json')
        for p,h in json.loads((case/'input_hashes_before.json').read_text()).items():pin(p,h)
    result=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read together with4557/4591/4611/4619/4636. All original groups, pins, requirements and exclusions persist. This journal replaces stale stock/matrix and old ending-run status only.',
      remaining=base['remaining'],newInputHashes=pins,completedFiniteScorpionSecondaryRendererMatrix=str(matrix_path),
      actualNativeRendererContexts=6,actualConsecutiveNativeRendererFields=3342,actualMatrixFaultsRejected=43,actualNativePixelFaultsRetained=12,
      fullArtAllArenaAlternateGroundAudioAccepted=False,
      actualOldEndingSchemaFailure=dict(report=str(failed_path),nativeExit=0,firstFailedFrame=56296,observedHardwareRGBFields=3040,
        exactPipelineFields=0,fullEndingVideoAccepted=False,
        cause='4612 parser omitted original human_slot/fighter/writes/assistance fields. Fresh4645 admits precisely real schema, rejects duplicates/extras and binds every row to true physical/model identity.'),
      qualifiedActualEndingMetadataSource=str(schema_path),qualifiedActualEndingCallbackPhase=str(phase_path),
      endingCallbackScope='Original controller stops at next ordinary notifier59336 after final renderer field59335. All300 actual attract renderer fields59036..59335 retained. No missing target tolerated or post-exit callback fabricated.',
      freshKanoWholeEndingVideo=ending,liveJobsAuthoritativelyObservedNow=live,liveExecSessions=[19289]if ending_live else[],
      nextAction='Poll existing19289 and exact4646/4649 processes first; never restart on observation expiry. Preserve actual terminal and first pixel/source counterexamples. If corrected Kano whole ending passes, run missing Sonya with qualified4646 and unused4649/4650Sonya leaves. Do not repeat accepted six-context Scorpion renderer matrix. Continue whole native ending transition pixels/art/audio/all required contexts, all move-phase art/ground/floor shadows/arena/CPU/repeat/KO/overlap, broader native Pit/Tomb/victim/branch/finisher/morph/secret/cinematic/audio scope, final selection/ladder/names/audio regression, dependency-aware cleanup and refreshed final ZIP.',
      thisGoalTurnClassification='progress: missing current stock LiuP2 whole renderer window observed and accepted; all six finite renderer contexts qualified with43actual matrix faults plus12bitmap faults and unchanged stock/own controls. Actual terminal ending context-schema and callback endpoint diagnosed, corrected fresh full-pipeline source qualified against3040actual fields/7context/4hardware/4phase faults; fresh full Kano renderer job launched.',
      fullPortAcceptance=False,finishedRelease=False,goalStatus='active',gameCodeOrPublicReleaseChanged=False,newBuilds=0,
      rawMediaGuestROMCopies=0,newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      cleanupAccounting='Only compressed text/source/digests and small additive journal. No raw captures/build copies or historical reclaim recounted.')
    need(len(result['remaining'])==5,'All original full-objective requirement groups preserved')
    need(all(sha(p)==h for p,h in pins.items()),'All new actual source/evidence/native/public byte pins unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),actualRendererContexts=6,exactNativeFields=3342,
                         endingAccepted=ending['completeNativeEndingRendererVideoAccepted'],liveSessions=result['liveExecSessions'],
                         newPins=len(pins),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
