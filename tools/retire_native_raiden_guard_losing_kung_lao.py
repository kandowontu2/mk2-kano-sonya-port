"""Preserve actual unsuccessful physical tactics; no game defect inferred."""
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path
import inspect_native_campaign_progress as progress
import capture_native_paired_stumble_raiden_guard_ready as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
GAME, PARENT = 122992, 183664
OUT = ROOT / 'audit_native_raiden_guard_losing_kung_lao_preserved'
RETIRED = ROOT / 'audit_native_raiden_guard_losing_kung_lao_retirement'


def stop():
    path = capture.OUT / 'explicit_unsuccessful_physical_policy_stop.json'
    need(not path.exists(), 'Fresh actual policy-stop record')
    stats = progress.inspect(capture.OUT.name)
    identity = json.loads((capture.OUT / 'native_identity.json').read_text())
    need(stats['originalNativeStillLive'] and stats['exactOriginalNativePID'] == GAME and
         identity['ParentProcessId'] == PARENT and stats['lossesByStage']['4'] >= 70 and
         stats['ownWinReadsByStage']['4'] == 0 and stats['latestNativeField']['stage'] == '4' and
         stats['latestNativeField']['human'] == '18:18' and stats['latestNativeField']['cpu'] == '0:0' and
         stats['nativeGlobalCacheFailureRows'] == 0,
         'Same actual live run, repeated earned Kung Lao losses and zero own round wins')
    need(next(q for q in progress.census.census() if q['ProcessId'] == GAME) == identity,
         'Complete process birth/path/command/parent still match before stopping')
    path.write_text(json.dumps(dict(stats, passed=False, physicalPolicyUnsuccessful=True,
        exactNativeIdentity=identity, exactRAMParent=PARENT,
        stopReason='70+ actual stage4 Kung Lao paid losses with zero own wins; improve ordinary physical guard/leg tactics.',
        stoppedSolelyForObservationTimeout=False, engineDefectNotInferredFromControllerLosses=True,
        inputHashes={str(Path(__file__).resolve()): sha(__file__), str(Path(progress.__file__).resolve()): sha(progress.__file__)},
        fullTowerAccepted=False, endingAccepted=False, freshJoinAccepted=False), indent=2) + '\n')
    answer = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
        f'Stop-Process -Id {GAME} -ErrorAction Stop'], capture_output=True, text=True)
    need(answer.returncode == 0 and not answer.stderr.strip(), 'Only exact losing-policy native stopped')
    print(json.dumps(dict(explicitStop=True, nativePID=GAME, actualKungLaoLosses=stats['lossesByStage']['4'])), flush=True)


def prepare(ram):
    need(os.getpid() == PARENT and not OUT.exists(), 'Same original RAM parent only')
    terminal = json.loads((capture.OUT / 'native_terminal.json').read_text())
    result = json.loads((capture.OUT / 'result.json').read_text())
    failure = json.loads((capture.OUT / 'current_capture_failure.json').read_text())
    stopped = json.loads((capture.OUT / 'explicit_unsuccessful_physical_policy_stop.json').read_text())
    proof = json.loads((capture.OUT / 'guest_memory_proof.json').read_text())
    need(terminal['identity'] == stopped['exactNativeIdentity'] and terminal['nativeExit'] == 0xffffffff and
         not result['passed'] and not failure['passed'] and stopped['physicalPolicyUnsuccessful'] and
         not stopped['stoppedSolelyForObservationTimeout'] and proof['everyActualByteComparedInRAM'] and
         hashlib.sha256(ram['guest']).hexdigest().upper() == proof['sha256'],
         'Actual failed transport and whole current guest preserved; no campaign acceptance')
    pins = json.loads((capture.OUT / 'input_hashes_before.json').read_text())
    need(all(sha(p) == h for p, h in pins.items()), 'Original executed inputs frozen')
    raw, rendered = ram['scope']['RAM_RAW'], ram['scope']['RAM_IMAGES']
    need(len(raw) == len(rendered) and set(raw) == set(rendered), 'Original native buffer inventory')
    stats = progress.inspect(capture.OUT.name)
    need(not stats['originalNativeStillLive'] and stats['lossesByStage']['4'] >= 70 and
         stats['ownWinReadsByStage']['4'] == 0 and stats['nativeGlobalCacheFailureRows'] == 0,
         'Same actual terminal chronology, no inferred gameplay success')
    OUT.mkdir()
    with gzip.open(OUT / 'original_executed_sources.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump(dict(wholeExecutedHost=ram['executedHost'], files={p:dict(sha256=h,text=Path(p).read_text())
            for p,h in pins.items() if Path(p).suffix.lower() in ('.py','.lua','.cpp','.h','.cmd')}), stream)
    bound = dict(pins)
    for folder in (capture.OUT, capture.SOURCE, capture.INIT, capture.OLD_INIT):
        for p in folder.rglob('*'):
            if p.is_file(): bound[str(p.resolve())] = sha(p)
    bound[str(OUT / 'original_executed_sources.json.gz')] = sha(OUT / 'original_executed_sources.json.gz')
    bound[str(Path(__file__).resolve())] = sha(__file__)
    source = json.loads((capture.SOURCE / 'report.json').read_text())
    report = dict(passed=False, preservationPassed=True, failedPhysicalPolicyPreserved=True,
        exactNativeGame=GAME, exactRAMParent=PARENT, statistics=stats, nativeExit=terminal['nativeExit'],
        originalRawRasterInventory={name:dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest().upper()) for name,data in raw.items()},
        originalRawBuffersToRelease=len(raw), originalPILBuffersToRelease=len(rendered),
        individuallyViewedInThisTrial=False, imagesNotUsedToInferGameplayAcceptance=True,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'], inputHashes=bound,
        fullTowerAccepted=False, endingAccepted=False, freshJoinAccepted=False, fullPortAcceptance=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(preserved=True, originalRawBuffers=len(raw), originalPILBuffers=len(rendered), fullPortAcceptance=False)),flush=True)


def retire():
    need(not RETIRED.exists(), 'Fresh actual retirement receipt')
    report = json.loads((OUT / 'report.json').read_text())
    need(report['preservationPassed'] and not report['passed'] and all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Original failed outcome and full executed inputs unchanged')
    answer = subprocess.run(['powershell.exe','-NoProfile','-Command',
        f'Get-CimInstance Win32_Process -Filter "ProcessId={GAME} OR ProcessId={PARENT}" | Select-Object ProcessId | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(answer.returncode == 0 and not answer.stdout.strip() and not answer.stderr.strip(), 'Both exact producers absent')
    RETIRED.mkdir()
    (RETIRED / 'report.json').write_text(json.dumps(dict(passed=True, exactNativeGameRetired=GAME,
        exactRAMParentRetired=PARENT, originalRawBuffersReleased=report['originalRawBuffersToRelease'],
        originalPILBuffersReleased=report['originalPILBuffersToRelease'], noReviewServerCreated=True,
        failedPhysicalPolicyPreserved=True, inputHashes={str(OUT/'report.json'):sha(OUT/'report.json'),str(Path(__file__).resolve()):sha(__file__)},
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(retired=True,failedPhysicalPolicyPreserved=True)),flush=True)


if __name__ == '__main__':
    import sys
    {'stop':stop,'retire':retire}[sys.argv[1]]()
