"""Verify exact special matrix processes/RAM retired; retain compact evidence."""
import json
import socket
import subprocess
from pathlib import Path
import capture_native_kano_laser_audio as current


def main():
    root = current.ROOT
    out = root / 'audit_native_kano_laser_special_ram_retirement'
    source = root / 'audit_native_kano_laser_special_shadow_checked/report.json'
    visual_path = root / 'audit_native_kano_laser_special_visual_review/report.json'
    current.need(not out.exists(), 'Fresh immutable retirement receipt')
    report, visual = [json.loads(p.read_text()) for p in (source, visual_path)]
    current.need(report['passed'] and visual['passed'] and len(visual['sampledNativeRasters']) == 64 and
                 visual['sourceReportSHA256'] == current.sha(source), 'Same accepted and reviewed native trials')
    for group in ('inputHashes', 'outputHashes'):
        current.need(all(current.sha(p) == h for p, h in report[group].items()), 'Executed evidence conserved')
    parents = {c['nativeTerminal']['actualWindowsIdentity']['ParentProcessId'] for c in report['cases']}
    current.need(parents == {188360}, 'Exact actual original RAM parent')
    pids = [188360] + [c['nativeTerminal']['pid'] for c in report['cases']]
    command = '$ids=@(' + ','.join(str(p) for p in pids) + '); @(Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in $ids } | Select-Object ProcessId,ParentProcessId,ExecutablePath) | ConvertTo-Json -Compress'
    result = subprocess.run(['powershell', '-NoProfile', '-Command', command], capture_output=True, text=True)
    current.need(result.returncode == 0 and not result.stderr and result.stdout.strip() in ('', '[]'),
                 'Exact RAM parent and all sixteen native handles absent')
    sock = socket.socket()
    sock.settimeout(1)
    try:
        current.need(sock.connect_ex(('127.0.0.1', 58919)) != 0, 'Exact RAM preview server retired')
    finally:
        sock.close()
    cmd = root / 'PLAY_LATEST_KANO_SONYA.cmd'
    current.need(current.sha(cmd) == 'D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
                 'Public playable CMD unchanged')
    current.need(not (root / 'mame-mkp/build/mingw-gcc').exists(), 'Generated compiler cache remains absent')
    files = [p for name in ('audit_native_kano_laser_special_shadow_ram',
                           'audit_native_kano_laser_special_shadow_checked',
                           'audit_native_kano_laser_special_matrix_checked',
                           'audit_native_kano_laser_special_visual_review')
             for p in (root / name).rglob('*') if p.is_file()]
    current.need(all(p.suffix.lower() not in ('.png', '.wav', '.bin', '.exe', '.zip') for p in files),
                 'No raw media, ROM, build, or ZIP copies')
    value = dict(passed=True, actualAbsentPIDs=pids, retiredRAMPorts=[58919],
                 original294NativeRastersReleasedFromRAM=True, individuallyReviewedRasters=64,
                 evidenceLogicalBytes=sum(p.stat().st_size for p in files),
                 inputHashes={str(p.resolve()): current.sha(p) for p in (Path(__file__), source, visual_path, cmd)},
                 actualSquareContactVerified=False, allArenasAccepted=False, fullPortAcceptance=False,
                 publicPlayableChanged=False, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                 generatedCompilerCacheAbsent=True, goalStatus='active')
    out.mkdir()
    (out / 'report.json').write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(dict(passed=True, nativeHandlesAndRAMRetired=True,
                         evidenceLogicalBytes=value['evidenceLogicalBytes'])), flush=True)


if __name__ == '__main__':
    main()
