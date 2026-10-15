"""Preserve the real pre-game controller loader failure and retire its RAM."""
import gzip
import json
import os
import subprocess
from pathlib import Path
import run_native_sonya_subzero_forward_jump_campaign as original

ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT / 'audit_native_subzero_forward_jump_boot_failure_preserved'
RETIRED = ROOT / 'audit_native_subzero_forward_jump_boot_failure_retired'
PARENT, GAME = 25908, 11536


def prepare(ram):
    need(os.getpid() == PARENT and not OUT.exists(), 'Same original failed producer RAM')
    terminal = json.loads((original.OUT / 'native_terminal.json').read_text())
    failure = json.loads((original.OUT / 'current_capture_failure.json').read_text())
    errors = (original.OUT / 'stderr.log').read_text()
    identity = terminal['identity']
    need(terminal['nativeExit'] == 3 and identity['ProcessId'] == GAME and
         identity['ParentProcessId'] == PARENT and identity['createdUnix'] == 1791704398.65547 and
         not failure['passed'] and "attempt to call a nil value (global 'read')" in errors and
         identity not in original.core.base.census.census(), 'Actual loader failure, native terminal, not elapsed timeout')
    raw, images = ram['scope']['RAM_RAW'], ram['scope']['RAM_IMAGES']
    need(not raw and not images and 'capture' not in ram,
         'No guest verification or gameplay capture returned; no raster acceptance')
    pins = json.loads((original.OUT / 'input_hashes_before.json').read_text())
    need(all(sha(p) == h for p, h in pins.items()), 'Actual executed sources unchanged')
    source = json.loads((original.SOURCE / 'report.json').read_text())
    OUT.mkdir()
    with gzip.open(OUT / 'original_executed_host.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump(dict(host=ram['executedHost']), stream)
    for folder in (original.OUT, original.SOURCE, original.INIT, original.OLD_INIT, OUT):
        for path in folder.rglob('*'):
            if path.is_file(): pins[str(path.resolve())] = sha(path)
    pins[str(Path(__file__).resolve())] = sha(__file__)
    report = dict(passed=False, preservationPassed=True, actualNativeIdentity=identity,
                  actualRAMParent=PARENT, originalNativeExit=3, originalError=errors,
                  originalFailure=failure, originalRawBuffersToRelease=0, originalPILBuffersToRelease=0,
                  actualGuestNotVerified=True, nativeGameplayAccepted=False,
                  originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=source['originalRemainingWorkGroups'], inputHashes=pins,
                  fullPortAcceptance=False, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                  goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(preserved=True, nativeExit=3, rawBuffers=0, PILBuffers=0)), flush=True)


def retire():
    need(not RETIRED.exists(), 'Fresh exact failed producer retirement')
    path = OUT / 'report.json'
    saved = json.loads(path.read_text())
    need(saved['preservationPassed'] and not saved['passed'] and
         all(sha(p) == h for p, h in saved['inputHashes'].items()), 'Actual immutable pre-game failure')
    result = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
        f'Get-CimInstance Win32_Process -Filter "ProcessId={PARENT} OR ProcessId={GAME}" | '
        'Select-Object ProcessId,ParentProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress'],
        capture_output=True, text=True)
    need(result.returncode == 0 and not result.stderr.strip(), 'Actual read-only process census')
    actual = json.loads(result.stdout) if result.stdout.strip() else []
    if isinstance(actual, dict): actual = [actual]
    need(not any(q['ProcessId'] == PARENT for q in actual), 'Original RAM parent exited')
    need(all(q['ExecutablePath'] != saved['actualNativeIdentity']['ExecutablePath'] and
             q['ParentProcessId'] != PARENT for q in actual), 'Any reused native PID is unrelated; never touch it')
    RETIRED.mkdir()
    (RETIRED / 'report.json').write_text(json.dumps(dict(passed=True, retirementOnlyAccepted=True,
        exactOriginalParentRetired=PARENT, exactOriginalNativeRetired=GAME, noReviewServerCreated=True,
        originalRawBuffersReleased=0, originalPILBuffersReleased=0, reusedPIDProcessesNotTouched=actual,
        inputHashes={str(path):sha(path), str(Path(__file__).resolve()):sha(__file__)},
        fullPortAcceptance=False, goalStatus='active'), indent=2) + '\n')
    print(json.dumps(dict(retired=True, failedTrialStillFailed=True)), flush=True)


if __name__ == '__main__':
    retire()
