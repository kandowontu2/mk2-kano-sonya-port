"""Lossless seal of terminal native guard run and stopped wrong-timing experiment.

The old whole-campaign qualifier may still read immutable logical bytes. This
storage operation never claims its pending state/ending proof has completed.
"""
import json
import subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_sonya_guard_uppercut_ready_campaign_v4145 as current

ROOT, need, sha = current.ROOT, current.need, current.sha
OUT = ROOT / 'audit_v4153_guard_terminal_log_compression'


def main():
    need(not OUT.exists(), 'Fresh immutable storage report')
    folders = [ROOT / 'audit_v4120_sonya_guard_punish_p2_campaign',
               ROOT / 'audit_v4138_sonya_guard_uppercut_p2_campaign']
    pids = [json.loads((folder / 'process.json').read_text())['pid'] for folder in folders]
    q = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
        'Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @(' + ','.join(map(str, pids)) +
        ') } | Select-Object -ExpandProperty ProcessId'], capture_output=True, text=True)
    need(q.returncode == 0 and not q.stdout.strip(), 'Both exact native children terminal/missing now')
    pins = {str(Path(__file__).resolve()): sha(__file__), str(Path(storage.__file__).resolve()): sha(storage.__file__)}
    observed_path = ROOT / 'audit_v4121_sonya_guard_punish_campaign_observed/report.json'
    failed_path = ROOT / 'audit_v4139_sonya_guard_uppercut_campaign_observed/report.json'
    observed, failed = json.loads(observed_path.read_text()), json.loads(failed_path.read_text())
    need(observed['passed'] and observed['observations'][0]['terminal0'] and
         not observed['independentCampaignAcceptance'] and failed['passed'] is False,
         'Correct terminal observation and intentional failed test; no pending qualifier acceptance implied')
    for path in (observed_path, failed_path):
        pins[str(path)] = sha(path)
    files = []
    for index, folder in enumerate(folders):
        need(folder.resolve().is_relative_to(ROOT.resolve()) and not folder.is_symlink(), 'Exact bounded terminal leaf')
        result = json.loads((folder / 'result.json').read_text())
        need((result['exit_code'] == 0) == (index == 0) and result['candidate'] == current.NAME and
             result['rawRasterFilesWritten'] == result['raw_audio_files_written'] ==
             result['new_builds_or_rom_copies'] == result['guestDumpFilesWritten'] == 0,
             'Actual terminal capture disposition and RAM-only resource contract')
        for path in folder.iterdir():
            if not path.is_file() or path.suffix not in ('.log', '.json'):
                continue
            path = path.resolve()
            need(path.is_relative_to(folder.resolve()) and not path.is_symlink(), 'Bounded exact evidence file')
            digest, logical, before = sha(path), path.stat().st_size, storage.allocated(path)
            q = subprocess.run(['compact.exe', '/C', '/F', '/EXE:LZX', '/I', '/Q', str(path)], capture_output=True)
            need(q.returncode == 0 and sha(path) == digest and path.stat().st_size == logical, 'All logical evidence bytes/digests unchanged')
            after = storage.allocated(path)
            need(after <= before, 'No allocation growth')
            files.append(dict(path=str(path), sha256=digest, logicalBytes=logical, allocatedBefore=before,
                              allocatedAfter=after, reclaimed=before-after))
            pins[str(path)] = digest
    report = dict(passed=True, captureFolders=2, captureChildrenMissing=pids, files=files, inputHashes=pins,
                  reclaimedAllocatedBytes=sum(f['reclaimed'] for f in files), deletedFiles=0,
                  pendingWholeCampaignProofAccepted=False, failedCaptureAcceptance=False,
                  newPlayableCopies=0, fullPortAcceptance=False)
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)], capture_output=True).returncode == 0,
         'Compress report directory before writes')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('files', 'inputHashes')}), flush=True)


if __name__ == '__main__':
    main()
