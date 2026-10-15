"""Compact additive full-scope progress, not a new completion boundary."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'audit_v4557_secondary_state_video_full_scope_checkpoint/checkpoint.json'
PARENT=ROOT/'audit_v4591_render_failure_scene_progress/progress.json'
OUT=ROOT/'audit_v4611_secondary_render_latch_probe_progress'
def sha(path):
    with Path(path).open('rb')as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()
def need(value,message):
    if not value:raise ValueError(message)
def main():
    need(not OUT.exists(),'Fresh immutable compact additive journal')
    base=json.loads(BASE.read_text());parent=json.loads(PARENT.read_text())
    inherited=dict(base['inputHashes']);inherited.update(parent['newInputHashes'])
    need(all(sha(p)==h for p,h in inherited.items()),'All inherited full scope/game/public/evidence bytes unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();actual=sha(path);key=str(path)
        need((wanted is None or actual==wanted)and(key not in inherited or inherited[key]==actual),'Exact actual new and inherited source/evidence')
        pins[key]=actual
    for p in (BASE,PARENT,Path(__file__)):pin(p)
    paths=[ROOT/'audit_v4593_scorpion_secondary_render_callback_phase_checked/report.json',
      ROOT/'audit_v4598_scorpion_secondary_sonya_p1_native_scene_checked/report.json',
      ROOT/'audit_v4598_scorpion_secondary_kano_p2_native_scene_checked/report.json',
      ROOT/'audit_v4596_scorpion_secondary_scene_source_checked/report.json',
      ROOT/'audit_v4607_ending_latch_probe_source_checked/report.json',
      ROOT/'audit_v4604_kano_ending_latch_probe_observed/report.json']
    reports=[]
    for path in paths:
        report=json.loads(path.read_text());pin(path);reports.append(report)
        for p,h in report.get('inputHashes',{}).items():pin(p,h)
    first=reports[0]
    need(first['passed']and first['completeNativeRendererWindowAccepted']and
      first['actualNativeCallbackPhase']['completeFields']==557 and first['actualNativeCallbackPhase']['postRetirementFields']==30 and
      len(first['actualPhaseFaultsRejected'])==6 and not first['fullPortAcceptance'],
      'KanoP1 actual full renderer/30laterfields and six actual phase faults qualified, exclusions retained')
    completed=[dict(fighter='kano',side=1,report=str(paths[0]),capture=first['capture'],fields=557)]
    for proof,path in zip(reports[1:3],paths[1:3]):
        need(proof['passed']and proof['native']['completeNativeRendererWindowAccepted']and
          proof['native']['completeSceneFields']==557 and len(proof['native']['nativeRasterFaults'])==2 and
          not proof['fullArtFloorShadowOrAudioAccepted'],'Actual missing full native context, original pixel fault and art/audio exclusions retained')
        completed.append(dict(fighter=proof['fighter'],side=proof['side'],report=str(path),capture=proof['capture'],fields=557))
    need({(r['fighter'],r['side'])for r in completed}=={('kano',1),('kano',2),('sonya',1)},'Exactly three actually completed contexts')
    for case in completed:
        folder=Path(case['capture'])
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
    need(reports[4]['passed']and reports[4]['generatedCurrentBuildModuleAndComparisonLocalDistinct']and
      not reports[4]['actualNativeRasterSwitchCauseEstablished']and not reports[5]['passed'],
      'Fresh diagnostic source gate and frozen original pre-boot module-shadow failure, never a video pass')
    for name in ('tools/verify_scorpion_secondary_render_callback_phase_v4592.py',
      'tools/run_scorpion_secondary_native_scene_v4594.py','tools/qualify_scorpion_secondary_scene_source_v4595.py',
      'tools/run_ending_latch_probe_ram_v4602.py','tools/qualify_ending_latch_probe_source_v4600.py',
      'tools/run_ending_latch_probe_ram_v4605.py','tools/qualify_ending_latch_probe_source_v4606.py',
      'mk2ks_kano_ending_latch_probe_ram_v4599.lua'):pin(ROOT/name)
    targets=[dict(kind='sonyaP2Renderer',session=92164,collector=75928,native=126760,
      leaf='audit_v4597_scorpion_secondary_sonya_p2_native_scene_ram',report='audit_v4598_scorpion_secondary_sonya_p2_native_scene_checked/report.json'),
      dict(kind='stockKitanaP1Renderer',session=37443,collector=113952,native=137620,
      leaf='audit_v4597_scorpion_secondary_kitana_p1_native_scene_ram',report='audit_v4598_scorpion_secondary_kitana_p1_native_scene_checked/report.json'),
      dict(kind='endingLatchDiagnosis',session=93973,collector=139172,native=137640,
      leaf='audit_v4608_kano_ending_latch_probe_ram',report='audit_v4609_kano_ending_latch_probe_observed/report.json')]
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.ProcessId -in @(75928,126760,113952,137620,139172,137640) } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(census.returncode==0,'Fresh actual process census')
    jobs=json.loads(census.stdout)if census.stdout.strip()else[];jobs=jobs if isinstance(jobs,list)else[jobs]
    status=[]
    for target in targets:
        own=[r for r in jobs if r['ProcessId']in(target['collector'],target['native'])]
        if own:
            need({r['ProcessId']for r in own}=={target['collector'],target['native']}and
              any(r['ProcessId']==target['native']and r['ParentProcessId']==target['collector']and target['leaf']in r['CommandLine']for r in own),
              'Exact still-live collector and native child; timeout never treated as terminal')
            status.append(dict(target,liveCIM=own,terminal=False,acceptancePending=True))
        else:
            report_path=ROOT/target['report'];result=json.loads(report_path.read_text());pin(report_path)
            status.append(dict(target,terminal=True,passed=result['passed'],terminalInspectionStillRequired=True))
    result=dict(schema=1,parentAdditiveJournal=str(PARENT),parentAdditiveJournalSHA256=sha(PARENT),
      baseFullScopeCheckpoint=str(BASE),baseFullScopeCheckpointSHA256=sha(BASE),inheritedFullScopeAndPinsRetained=True,
      mergeRule='Read together with immutable4557 and4591; inherited requirements/pins/exclusions are not removed. This journal replaces stale pending status only.',
      remaining=base['remaining'],completedNativeSecondaryRendererContexts=completed,
      currentBothAddedBothSlotsSecondaryRendererAccepted=False,currentFullArtAllArenasAlternateGroundAudioAccepted=False,
      callbackPhaseCorrection=dict(rendererRetirement=3691,stateNotifierRetirement=3692,postRendererRetirementFields=30,
        actual557FieldProof=str(paths[0]),actualFaultsRejected=6,oldExecutedSourceAndCapturePreserved=True),
      endingFullVideoAccepted=False,endingFailureFrame=57416,endingCauseEstablished=False,
      newActualJobStatus=status,
      nextAction='Poll exact92164/37443/93973 and their live CIM identities. Inspect actual terminal reports before acceptance. Complete missing stock LiuP2 renderer after current jobs; do not repeat accepted three contexts. Qualify entire added/stock scene matrix and actual faults. Ending latch probe is diagnosis only: bind DPYSTRT/DPYADR/VCOUNT/VBLANK source timing before repairing whole-video model, never choose a matching buffer as success. All five groups and final release/cleanup remain.',
      thisGoalTurnClassification='progress: real557-field renderer-phase proof qualified; two more full native contexts passed; new remaining contexts and hardware-latch diagnosis are genuinely live.',
      newInputHashes=pins,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      newBuilds=0,gameCodeAndPublicPlayableChanged=False,rawMediaGuestROMCopies=0,
      newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,cleanupAccounting='Only compressed source/text/digests; compact additive evidence, no inherited13k-pin duplication or historical reclaim recounted.')
    need(len(result['remaining'])==5 and result['remaining']==parent['remaining'],'All original five full objective groups unchanged')
    need(all(sha(p)==h for p,h in pins.items()),'Every current/inherited/public evidence byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),completedRendererContexts=3,newInputPins=len(pins),
      pendingActualJobs=status,fullPortAcceptance=False),indent=2),flush=True)
if __name__=='__main__':main()
