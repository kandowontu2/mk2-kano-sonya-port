"""Losslessly compact only the two exact terminal failed controller experiments."""
import json
import subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_sonya_guard_punish_campaign_v4119 as current

ROOT, need, sha = current.ROOT, current.need, current.sha
OUT = ROOT / 'audit_v4131_stopped_campaign_evidence_compression'


def main():
    need(not OUT.exists(), 'Fresh immutable storage report')
    folders = [ROOT / f'audit_v{v}_sonya_guard_punish_p2_campaign' for v in (4110, 4114)]
    pids = [json.loads((folder / 'process.json').read_text())['pid'] for folder in folders]
    q = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
        'Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @(' + ','.join(map(str, pids)) +
        ') } | Select-Object -ExpandProperty ProcessId'], capture_output=True, text=True)
    need(q.returncode == 0 and not q.stdout.strip(), 'Both exact failed test children terminal/missing now')
    pins = {str(Path(__file__).resolve()): sha(__file__), str(Path(storage.__file__).resolve()): sha(storage.__file__)}
    for version in (4111, 4115):
        path = ROOT / f'audit_v{version}_sonya_guard_punish_campaign_observed/report.json'
        report = json.loads(path.read_text())
        need(report['passed'] is False and not report['fullPortAcceptance'], 'Preserve false native failures, not green results')
        pins[str(path)] = sha(path)
    files = []
    for folder in folders:
        need(folder.resolve().is_relative_to(ROOT.resolve()) and not folder.is_symlink(), 'Exact bounded failed test leaf')
        result = json.loads((folder / 'result.json').read_text())
        need(result['exit_code'] != 0 and result['candidate'] == current.NAME and result['rawRasterFilesWritten'] ==
             result['raw_audio_files_written'] == result['new_builds_or_rom_copies'] == result['guestDumpFilesWritten'] == 0,
             'Terminal failed physical-controller capture, no dump/build files')
        for path in folder.iterdir():
            if not path.is_file() or path.suffix not in ('.log', '.json'):
                continue
            path = path.resolve()
            need(path.is_relative_to(folder.resolve()) and not path.is_symlink(), 'Bounded exact evidence file')
            digest, logical, before = sha(path), path.stat().st_size, storage.allocated(path)
            q = subprocess.run(['compact.exe', '/C', '/F', '/EXE:LZX', '/I', '/Q', str(path)], capture_output=True)
            need(q.returncode == 0 and sha(path) == digest and path.stat().st_size == logical, 'All logical failed evidence unchanged')
            after = storage.allocated(path)
            need(after <= before, 'No storage allocation growth')
            files.append(dict(path=str(path), sha256=digest, logicalBytes=logical, allocatedBefore=before,
                              allocatedAfter=after, reclaimed=before-after))
            pins[str(path)] = digest
    report = dict(passed=True, captureFolders=2, captureChildrenMissing=pids, files=files, inputHashes=pins,
                  reclaimedAllocatedBytes=sum(f['reclaimed'] for f in files), deletedFiles=0,
                  failedCaptureAcceptance=False, newPlayableCopies=0, fullPortAcceptance=False)
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)], capture_output=True).returncode == 0,
         'Compress report directory before writes')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('files', 'inputHashes')}), flush=True)


if __name__ == '__main__':
    main()
