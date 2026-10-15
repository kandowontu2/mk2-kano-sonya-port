"""Retire only the evidenced unsuccessful physical Scorpion test policy."""
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path
import inspect_native_campaign_progress as progress
import capture_native_paired_stumble_regular_guard as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
GAME,PARENT=183872,182104
OUT=ROOT/'audit_native_regular_guard_losing_scorpion_preserved'
RETIRED=ROOT/'audit_native_regular_guard_losing_scorpion_retirement'


def stop():
    path=capture.OUT/'explicit_unsuccessful_physical_policy_stop.json'
    need(not path.exists(),'Fresh actual losing-policy stop')
    stats=progress.inspect(capture.OUT.name)
    identity=json.loads((capture.OUT/'native_identity.json').read_text())
    need(stats['originalNativeStillLive'] and stats['exactOriginalNativePID']==GAME and identity['ParentProcessId']==PARENT and
         stats['lossesByStage']['9']>=30 and stats['ownWinReadsByStage']['9']==0 and
         stats['latestNativeField']['stage']=='9' and stats['latestNativeField']['human']=='18:18' and
         stats['latestNativeField']['cpu']=='10:10' and stats['nativeGlobalCacheFailureRows']==0,
         'Same actual native Scorpion fight;30+ paid losses without own wins, not an observation timeout')
    need(next(q for q in progress.census.census() if q['ProcessId']==GAME)==identity,
         'Actual process birth/path/command/parent still match before stop')
    path.write_text(json.dumps(dict(stats,passed=False,physicalPolicyUnsuccessful=True,exactNativeIdentity=identity,exactRAMParent=PARENT,
        stopReason='30+ actual paid Scorpion losses and zero own wins; replace the ordinary ranged test tactic with guard/leg inputs.',
        stoppedSolelyForObservationTimeout=False,engineDefectNotInferredFromControllerLosses=True,
        inputHashes={str(Path(__file__).resolve()):sha(__file__),str(Path(progress.__file__).resolve()):sha(progress.__file__)},
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False),indent=2)+'\n')
    answer=subprocess.run(['powershell.exe','-NoProfile','-Command',f'Stop-Process -Id {GAME} -ErrorAction Stop'],capture_output=True,text=True)
    need(answer.returncode==0 and not answer.stderr.strip(),'Only exact losing-policy native stopped')
    print(json.dumps(dict(explicitStop=True,nativePID=GAME,actualScorpionLosses=stats['lossesByStage']['9'])),flush=True)


def prepare(ram):
    need(os.getpid()==PARENT and not OUT.exists(),'Same original retained RAM parent')
    terminal=json.loads((capture.OUT/'native_terminal.json').read_text())
    result=json.loads((capture.OUT/'result.json').read_text())
    failure=json.loads((capture.OUT/'current_capture_failure.json').read_text())
    stopped=json.loads((capture.OUT/'explicit_unsuccessful_physical_policy_stop.json').read_text())
    proof=json.loads((capture.OUT/'guest_memory_proof.json').read_text())
    need(terminal['identity']==stopped['exactNativeIdentity'] and terminal['nativeExit']==0xffffffff and
         not result['passed'] and not failure['passed'] and stopped['physicalPolicyUnsuccessful'] and
         not stopped['stoppedSolelyForObservationTimeout'] and proof['everyActualByteComparedInRAM'] and
         hashlib.sha256(ram['guest']).hexdigest().upper()==proof['sha256'],
         'Entire actual native guest and original unsuccessful transport preserved')
    pins=json.loads((capture.OUT/'input_hashes_before.json').read_text())
    need(all(sha(p)==h for p,h in pins.items()),'All actual executed inputs unchanged')
    raw,images=ram['scope']['RAM_RAW'],ram['scope']['RAM_IMAGES']
    need(set(raw)==set(images),'Original retained raw/PIL inventory')
    stats=progress.inspect(capture.OUT.name)
    need(not stats['originalNativeStillLive'] and stats['lossesByStage']['9']>=30 and stats['ownWinReadsByStage']['9']==0 and
         stats['nativeGlobalCacheFailureRows']==0 and all(stats['ownWinReadsByStage'][str(s)]>=2 for s in range(9)),
         'Same terminal failed Scorpion policy preserves observed earlier nine-fight advancement')
    OUT.mkdir()
    with gzip.open(OUT/'original_executed_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(wholeExecutedHost=ram['executedHost'],files={p:dict(sha256=h,text=Path(p).read_text())
            for p,h in pins.items() if Path(p).suffix.lower() in ('.py','.lua','.cpp','.h','.cmd')}),stream)
    bound=dict(pins)
    for folder in (capture.OUT,capture.SOURCE,capture.INIT,capture.OLD_INIT):
        for p in folder.rglob('*'):
            if p.is_file():bound[str(p.resolve())]=sha(p)
    for p in (OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)
    source=json.loads((capture.SOURCE/'report.json').read_text())
    (OUT/'report.json').write_text(json.dumps(dict(passed=False,preservationPassed=True,failedPhysicalPolicyPreserved=True,
        exactNativeGame=GAME,exactRAMParent=PARENT,statistics=stats,nativeExit=terminal['nativeExit'],
        originalRawRasterInventory={name:dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest().upper()) for name,data in raw.items()},
        originalRawBuffersToRelease=len(raw),originalPILBuffersToRelease=len(images),individuallyViewedInThisTrial=False,
        imagesNotUsedToInferGameplayAcceptance=True,inputHashes=bound,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=source['originalRemainingWorkGroups'],
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(preserved=True,rawBuffersToRelease=len(raw),pilBuffersToRelease=len(images),fullPortAcceptance=False)),flush=True)


def retire():
    need(not RETIRED.exists(),'Fresh exact original producer retirement')
    saved=json.loads((OUT/'report.json').read_text())
    need(saved['preservationPassed'] and not saved['passed'] and all(sha(p)==h for p,h in saved['inputHashes'].items()),
         'Whole original failed outcomes and source inputs still frozen')
    query=subprocess.run(['powershell.exe','-NoProfile','-Command',
        f'Get-CimInstance Win32_Process -Filter "ProcessId={GAME} OR ProcessId={PARENT}" | Select-Object ProcessId | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(query.returncode==0 and not query.stdout.strip() and not query.stderr.strip(),'Both exact original native/RAM processes absent')
    RETIRED.mkdir()
    (RETIRED/'report.json').write_text(json.dumps(dict(passed=True,exactNativeGameRetired=GAME,exactRAMParentRetired=PARENT,
        originalRawBuffersReleased=saved['originalRawBuffersToRelease'],originalPILBuffersReleased=saved['originalPILBuffersToRelease'],
        noReviewServerCreated=True,failedPhysicalPolicyPreserved=True,
        inputHashes={str(OUT/'report.json'):sha(OUT/'report.json'),str(Path(__file__).resolve()):sha(__file__)},
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(retired=True,failedPhysicalPolicyPreserved=True)),flush=True)


if __name__=='__main__':
    import sys
    {'stop':stop,'retire':retire}[sys.argv[1]]()
