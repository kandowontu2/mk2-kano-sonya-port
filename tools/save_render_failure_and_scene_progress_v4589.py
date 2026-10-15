"""Compact additive progress journal; immutable full-scope parent retained.

Do not duplicate the inherited13k-pin checkpoint. This journal adds observed
failures, fresh source repair and actual process status; it does not replace
or narrow any full-goal requirement or promote partial rendering acceptance.
"""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PARENT=ROOT/'audit_v4557_secondary_state_video_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4591_render_failure_scene_progress'
def sha(path):
    with Path(path).open('rb')as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()
def need(value,message):
    if not value:raise ValueError(message)
def main():
    need(not OUT.exists(),'Fresh immutable additive journal')
    parent=json.loads(PARENT.read_text());inherited=parent['inputHashes'];pins={}
    need(all(sha(p)==h for p,h in inherited.items()),'Every inherited scope/public/game/input byte unchanged')
    def pin(path,wanted=None):
        path=Path(path).resolve();actual=sha(path)
        need((wanted is None or actual==wanted)and(str(path)not in inherited or inherited[str(path)]==actual),
          'Every actual current/inherited source and evidence unchanged')
        pins[str(path)]=actual
    pin(PARENT);pin(__file__)
    ending=ROOT/'audit_v4547_kano_p2_ending_display_ram';scene=ROOT/'audit_v4576_scorpion_secondary_kano_p1_native_scene_ram'
    ending_meta=json.loads((ending/'result.json').read_text());scene_meta=json.loads((scene/'result.json').read_text())
    need(ending_meta['exit_code']==0 and ending_meta['exactContinuousEndingFields']==1120 and
      len(ending_meta['endingModelErrors'])==1 and 'frame=57416 'in ending_meta['endingModelErrors'][0]['line'],
      'Actual terminal ending native0,1120 exact fields then real scanout mismatch, not whole success')
    need(scene_meta['exit_code']==0 and len(scene_meta['sceneErrors'])==1 and
      'frame=3237 'in scene_meta['sceneErrors'][0]['line'],'Actual terminal native finisher0 with missing source-model upload')
    for case in (ending,scene,ROOT/'audit_v4571_scorpion_secondary_kano_p1_native_scene_ram'):
        for name in ('run.log','stderr.log','result.json','input_hashes_before.json','process.json'):
            pin(case/name)
    leaves=['audit_v4548_kano_p2_ending_display_checked','audit_v4572_scorpion_secondary_kano_p1_native_scene_checked',
      'audit_v4577_scorpion_secondary_kano_p1_native_scene_checked','audit_v4567_scorpion_secondary_scene_source_checked',
      'audit_v4570_scorpion_secondary_scene_source_checked','audit_v4578_scorpion_secondary_scene_source_checked',
      'audit_v4586_scorpion_secondary_scene_source_checked','audit_v4580_scorpion_secondary_graphics_digest_inspected',
      'audit_v4588_scorpion_secondary_graphics_digest_inspected']
    proofs={}
    for leaf in leaves:
        path=ROOT/leaf/'report.json';report=json.loads(path.read_text());pin(path);proofs[leaf]=report
        for p,h in report.get('inputHashes',{}).items():pin(p,h)
    fixed=proofs['audit_v4588_scorpion_secondary_graphics_digest_inspected']
    need(fixed['passed']and fixed['actualObservedGraphicsStreams']==467 and fixed['totalMismatches']==0 and
      not fixed['wholeNativeSceneAcceptance'],'Independent source upload diagnosis, not full native replay acceptance')
    source=proofs['audit_v4586_scorpion_secondary_scene_source_checked']
    need(source['passed']and len(source['actualSourceFaultsRejected'])==4 and
      source['generatedStderrAndSceneErrorLocalsDistinct']and source['requiredRendererRoleEnvironmentKeysPresent'],
      'Fresh unchanged-controller/render source and all actual negative gates qualified')
    for name in ('qualify_scorpion_secondary_scene_source_v4560.py','run_scorpion_secondary_native_scene_v4562.py',
      'qualify_scorpion_secondary_scene_source_v4565.py','qualify_scorpion_secondary_scene_source_v4569.py',
      'run_scorpion_secondary_native_scene_v4568.py','qualify_scorpion_secondary_scene_source_v4574.py',
      'run_scorpion_secondary_native_scene_v4575.py','scorpion_secondary_native_scene_model_v4559.py',
      'scorpion_secondary_native_scene_model_v4581.py','inspect_scorpion_secondary_graphics_digests_v4579.py',
      'inspect_scorpion_secondary_graphics_digests_v4587.py','qualify_scorpion_secondary_scene_source_v4582.py',
      'run_scorpion_secondary_native_scene_v4583.py'):
        pin(ROOT/'tools'/name)
    pin(ROOT/'mk2ks_scorpion_secondary_native_scene_ram_v4558.lua');pin(ROOT/'mk2ks_scorpion_secondary_native_scene_ram_v4573.lua')
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.ProcessId -in @(36624,135848,120636,97352,39500,91776,105504) } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(census.returncode==0,'Fresh authoritative job census')
    jobs=json.loads(census.stdout)if census.stdout.strip()else[];jobs=jobs if isinstance(jobs,list)else[jobs]
    need(not any(r['ProcessId']in(36624,135848,120636,97352,39500)for r in jobs),'Old failed/ending jobs terminal, not restarted on timeout')
    fresh=ROOT/'audit_v4584_scorpion_secondary_kano_p1_native_scene_ram'
    if jobs:
        need({r['ProcessId']for r in jobs}=={91776,105504}and
          any(r['ProcessId']==105504 and r['ParentProcessId']==91776 and fresh.name in r['CommandLine']for r in jobs),
          'Exact live repaired scene collector/native child')
        pending=dict(execSession=59913,collectorPID=91776,nativePID=105504,liveCIM=jobs,capture=str(fresh),wholeSceneAccepted=False)
    else:
        report_path=ROOT/'audit_v4585_scorpion_secondary_kano_p1_native_scene_checked/report.json'
        result=json.loads(report_path.read_text());pin(report_path)
        pending=dict(execSession=59913,terminalReport=str(report_path),passed=result['passed'],capture=str(fresh),requiresTerminalInspection=True)
    visible=json.loads((ending/'ending_visible_digests.json').read_text());pin(ending/'ending_visible_digests.json')
    transition=[r for r in visible if r['file']in('display_57415.png','display_57416.png','display_57417.png')]
    need(len(transition)==3 and transition[0]['rgbSHA256']==transition[1]['rgbSHA256']!=transition[2]['rgbSHA256'],
      'Actual mismatch field retains previous visible RGB; following field changes. Cause remains runtime-unverified')
    report=dict(schema=1,parentFullScopeCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
      inheritedFullScopeAndInputPinsRetained=True,inheritedInputPinCount=len(inherited),
      mergeRule='Read this additive journal together with immutable4557; no inherited requirement, pin, exclusion or acceptance removed.',
      remaining=parent['remaining'],goalObjective='Once again, the goal is clear: THey need to appear as a natural part of the game in all aspects.',
      previousGoalTurnClassification=parent['thisGoalTurnClassification'],thisGoalTurnClassification='progress: real complete ending and finisher renderer failures localized; independent missing KTR1 source-model upload corrected and467 actual graphics digests matched; new complete finisher scene is live.',
      currentEndingFullVideoAccepted=False,endingNativeExit=0,endingExactFieldsBeforeMismatch=1120,
      endingMismatch=ending_meta['endingModelErrors'][0],endingTransitionActualVisibleDigests=transition,
      endingCauseEstablished=False,endingNextDiagnosis='Observe actual TMS DPYSTRT versus VBLANK-latched DPYADR/scanline timing and complete failed-field RGB/VRAM/palette discrepancy. Never tolerate or skip the mismatched field or claim first1120 as full video.',
      currentScorpionWholeSceneAccepted=False,priorSceneFailure=scene_meta['sceneErrors'][0],
      currentScorpionSourceUploadDigestsRepaired=True,currentScorpionSourceDigestReport=str(ROOT/'audit_v4588_scorpion_secondary_graphics_digest_inspected/report.json'),
      newScorpionSceneObservation=pending,
      nextAction='Poll exec59913/collector91776/native105504, actual4584 result and4585 report after terminal. Do not repeat completed state-only contexts. If new whole scene passes, qualify same full window in remaining physical added/stock contexts; preserve all five groups and end-to-end regressions. Diagnose failed ending before Sonya video or release.',
      newInputHashes=pins,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      newBuilds=0,rawMediaGuestROMCopies=0,gameSourceAndPlayableBytesChanged=False,
      newDeletedFiles=0,newlyReclaimedAllocatedBytes=0,cleanupAccounting='No new deletions or historical reclaim counted; compact additive journal avoids duplicating inherited13k-pin checkpoint.')
    need(len(report['remaining'])==5 and report['remaining']==parent['remaining'],'Full original five groups retained')
    need(all(sha(p)==h for p,h in pins.items()),'All actual journal inputs unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),inheritedPins=len(inherited),additionalPins=len(pins),
      actualEndingMismatchFrame=57416,oldJobsTerminal=True,newSceneStatus=pending,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
