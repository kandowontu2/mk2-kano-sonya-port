"""Retirement receipt by original identity, safe against Windows PID reuse."""
import json
import subprocess
from pathlib import Path
import retire_native_regular_guard_losing_scorpion as prior


def run():
    need, sha = prior.need, prior.sha
    need(not prior.RETIRED.exists(), 'Fresh exact original identity retirement')
    saved_path = prior.OUT / 'report.json'
    saved = json.loads(saved_path.read_text())
    terminal_path = prior.capture.OUT / 'native_terminal.json'
    terminal = json.loads(terminal_path.read_text())
    need(saved['preservationPassed'] and not saved['passed'] and
         terminal['nativeExit'] == 0xffffffff and
         all(sha(p) == h for p, h in saved['inputHashes'].items()),
         'Original failed run, entire sources and buffer inventory preserved')
    need(not any(q == terminal['identity'] for q in prior.progress.census.census()),
         'Exact native birth/path/command/parent identity no longer exists')
    answer = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
        f'Get-CimInstance Win32_Process -Filter "ProcessId={prior.GAME} OR ProcessId={prior.PARENT}" | '
        'Select-Object ProcessId,ParentProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress'],
        capture_output=True, text=True)
    need(answer.returncode == 0 and not answer.stderr.strip(), 'Read-only actual process identity inventory')
    actual = json.loads(answer.stdout) if answer.stdout.strip() else []
    if isinstance(actual, dict): actual = [actual]
    need(not any(q['ProcessId'] == prior.PARENT for q in actual), 'Original RAM parent exited after buffer clear')
    reused = [q for q in actual if q['ProcessId'] == prior.GAME]
    need(all(q['ExecutablePath'] != terminal['identity']['ExecutablePath'] and
             q['ParentProcessId'] != terminal['identity']['ParentProcessId'] for q in reused),
         'A reused PID belongs to an unrelated executable and parent; leave it untouched')
    prior.RETIRED.mkdir()
    receipt = dict(passed=True, exactNativeGameRetired=prior.GAME, exactRAMParentRetired=prior.PARENT,
        originalRawBuffersReleased=saved['originalRawBuffersToRelease'],
        originalPILBuffersReleased=saved['originalPILBuffersToRelease'],
        noReviewServerCreated=True, failedPhysicalPolicyPreserved=True,
        originalIdentityTerminal=terminal, reusedPIDProcessesNotTouched=reused,
        inputHashes={str(saved_path): sha(saved_path), str(terminal_path): sha(terminal_path),
                     str(Path(__file__).resolve()): sha(__file__), str(Path(prior.__file__).resolve()): sha(prior.__file__)},
        fullPortAcceptance=False, goalStatus='active')
    (prior.RETIRED / 'report.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(retired=True, originalBuffersReleased=saved['originalRawBuffersToRelease'],
                         unrelatedReusedPIDUntouched=bool(reused))), flush=True)


if __name__ == '__main__': run()
