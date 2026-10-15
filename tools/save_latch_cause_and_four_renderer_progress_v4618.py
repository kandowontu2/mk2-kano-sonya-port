"""Compact additive progress: four actual added-victim windows and latch cause."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'audit_v4557_secondary_state_video_full_scope_checkpoint/checkpoint.json'
PARENTS=[ROOT/'audit_v4591_render_failure_scene_progress/progress.json',
         ROOT/'audit_v4611_secondary_render_latch_probe_progress/progress.json']
OUT=ROOT/'audit_v4619_latch_cause_four_renderer_progress'
def sha(path):
    with Path(path).open('rb')as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()
def need(ok,message):
    if not ok:raise ValueError(message)
def main():
    need(not OUT.exists(),'Fresh immutable additive journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:inherited.update(json.loads(parent.read_text())['newInputHashes'])
    need(all(sha(p)==h for p,h in inherited.items()),'Every inherited full scope/public/source/input byte unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or actual==wanted)and(key not in inherited or inherited[key]==actual),'Exact actual original/current byte pins')
        pins[key]=actual
    for p in [BASE,*PARENTS,Path(__file__).resolve()]:pin(p)
    report_path=ROOT/'audit_v4615_ending_native_latch_timing_checked/report.json'
    cause=json.loads(report_path.read_text());pin(report_path)
    need(cause['passed']and cause['actualNativeVBLANKLatchCauseEstablished']and len(cause['actualHardwareFaultsRejected'])==4 and
      len(cause['hardwareDerivedVisibleFields'])==41 and cause['originalDelayedSwitchRoutineByteExact']and
      cause['originalColdNativeCampaignGuestRGBExactlyUnchanged']and not cause['fullEndingRendererVideoAccepted'],
      'Actual hardware/source/native-event cause qualified, never whole-ending video acceptance')
    for p,h in cause['inputHashes'].items():pin(p,h)
    completed=[]
    first_path=ROOT/'audit_v4593_scorpion_secondary_render_callback_phase_checked/report.json'
    first=json.loads(first_path.read_text());pin(first_path)
    need(first['passed']and first['completeNativeRendererWindowAccepted'],'Original complete actual KanoP1 callback proof retained')
    for p,h in first['inputHashes'].items():pin(p,h)
    completed.append(dict(fighter='kano',side=1,identity=17,fields=557,capture=first['capture'],report=str(first_path)))
    for fighter,side in [('sonya',1),('kano',2),('sonya',2)]:
        path=ROOT/f'audit_v4598_scorpion_secondary_{fighter}_p{side}_native_scene_checked/report.json'
        proof=json.loads(path.read_text());pin(path)
        need(proof['passed']and proof['native']['completeSceneFields']==557 and proof['native']['completeNativeRendererWindowAccepted']and
          len(proof['native']['nativeRasterFaults'])==2 and not proof['fullArtFloorShadowOrAudioAccepted'],
          'Actual full557 native fields, original bitmap faults and all broader art/floor/audio exclusions')
        for p,h in proof['inputHashes'].items():pin(p,h)
        completed.append(dict(fighter=fighter,side=side,identity=proof['native']['identity'],fields=557,capture=proof['capture'],report=str(path)))
    stock=ROOT/'audit_v4597_scorpion_secondary_kitana_p1_native_scene_ram'
    stock_path=ROOT/'audit_v4598_scorpion_secondary_kitana_p1_native_scene_checked/report.json';pin(stock_path)
    stock_meta=json.loads((stock/'result.json').read_text());records=json.loads((stock/'native_scene_records.json').read_text())
    need(not json.loads(stock_path.read_text())['passed']and stock_meta['exit_code']==0 and not stock_meta['sceneErrors']and len(records)==557,
      'Stock comparison has real complete matching pipeline targets but remains unaccepted at original compressed-shadow metadata gate')
    for folder in [stock,*[Path(r['capture'])for r in completed]]:
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_scorpion_secondary_native_scene_v4594.py|run_ending_latch_probe_ram_v4605.py|audit_v4597_|audit_v4608_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(census.returncode==0 and not census.stdout.strip(),'All actual scene/probe jobs terminal; recycled unrelated PIDs are not their jobs')
    result=dict(schema=1,baseFullScopeCheckpoint=str(BASE),baseFullScopeCheckpointSHA256=sha(BASE),
      parentAdditiveJournals=[dict(path=str(p),sha256=sha(p))for p in PARENTS],
      mergeRule='Read together with immutable4557/4591/4611; all original groups/pins/exclusions retained. This journal replaces stale job and ending-cause status only.',
      remaining=base['remaining'],newInputHashes=pins,
      currentBothTrueAddedVictimsBothSlotsScorpionSecondaryCompleteNativeRendererWindowsAccepted=True,
      completedNativeRendererContexts=completed,actualConsecutiveRendererFields=2228,exactVisiblePixels=2228*400*254,
      allNativeRendererJobsTerminal=True,allEndingProbeJobsTerminal=True,liveJobHandles=[],
      endingNativeHardwareLatchCauseEstablished=True,endingLatchCauseReport=str(report_path),endingFullRendererVideoAccepted=False,
      nativeEndingCause=cause['diagnosis'],
      stockKitanaComparison=dict(capture=str(stock),report=str(stock_path),nativeExit=0,exactPipelineFields=557,
        wholeStockComparisonAccepted=False,condition='Original stock shadows use source0150746A and commandE588/color15; compressed-own-art SHADOW_COMPONENT marker is inapplicable. Renderer has no pixel error. Inspect and preserve actual native stock-shadow DMA/source proof before qualification.'),
      nextAction='Implement fresh4612 ending model and4613 observer with actual DPYADR/VCOUNT/VEBLNK/VSBLNK/DUDATE metadata in every field. Derive latched start independently from source timing, never choose by pixel match. Retain entire original CPU/DMA/shift/graphics/pre-pass/flip/held/VRAM/RGB and actual fault gates; do not re-anchor. Qualify before boot, then observe whole ending/attract windows. Do not repeat the four accepted Scorpion added-victim render windows. Qualify stock Kitana archive using actual original shadow DMA rather than own-art marker, and observe missing stock LiuP2 only after fresh matching source preflight. Complete matrix faults, full art/alternate/arenas/audio and all other original groups, final combined regression/dependency cleanup/release.',
      currentFullArtAllArenasAlternateGroundAudioAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      thisGoalTurnClassification='progress: full added-victim second-fatality renderer windows now verified for both characters/both slots; actual hardware/source/41native fields prove ending discrepancy is a verifier immediate-switch assumption. Original stock shadows metadata distinction identified.',
      newBuilds=0,gameCodeAndPublicPlayableChanged=False,rawMediaGuestROMCopies=0,newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      cleanupAccounting='Only compressed source/text/digests; compact additive journal, no13k-pin duplication or historical cleanup saving counted.')
    need(len(result['remaining'])==5,'All original full-goal groups retained')
    need(all(sha(p)==h for p,h in pins.items()),'Every current/inherited source/capture/public byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),addedVictimRendererContexts=4,exactNativeFields=2228,
      endingHardwareCauseEstablished=True,allActualJobsTerminal=True,newInputPins=len(pins),fullPortAcceptance=False),indent=2),flush=True)
if __name__=='__main__':main()
