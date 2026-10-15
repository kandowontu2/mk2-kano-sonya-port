"""Release exactly the reviewed, terminal losing-policy RAM and preview."""
import hashlib
import json
import os
import socket
import subprocess
from pathlib import Path
import verify_native_paired_stumble_handoff as verified

ROOT, need, sha = verified.ROOT, verified.need, verified.sha
OUT = ROOT / 'audit_native_paired_stumble_handoff_retirement_prepare'
RETIRED = ROOT / 'audit_native_paired_stumble_handoff_retirement'


def prepare(ram, carrier, server):
    need(os.getpid() == verified.PARENT and not OUT.exists(), 'Original reviewed native RAM parent only')
    accepted = json.loads((verified.OUT / 'report.json').read_text())
    need(accepted['passed'] and accepted['finiteNativeSonyaRaidenHandoffAccepted'] and
         not accepted['originalCampaignTransportPassed'] and not accepted['fullPortAcceptance'] and
         len(accepted['nativeHandoffs']) == 3 and len(accepted['semanticFaultsRejected']) == 50 and
         accepted['exactNativeGame'] == verified.GAME and accepted['exactRAMParent'] == verified.PARENT and
         accepted['exactReviewPort'] == server.server_port and
         all(sha(p) == h for p, h in accepted['inputHashes'].items()),
         'Actual finite accepted fix, original failed tower and complete frozen inputs retained')
    raw, images = ram['scope']['RAM_RAW'], ram['scope']['RAM_IMAGES']
    need(len(raw) == len(images) == len(carrier['rgbFrames']) == 5 and
         all(record['pixels'] is raw[name] and hashlib.sha256(raw[name]).hexdigest().upper() == record['header']['sha256']
             for name, record in zip(raw, carrier['rgbFrames'])), 'Only original five reviewed buffers and zero-copy aliases')
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(dict(passed=True, exactNativeGame=verified.GAME,
        exactRAMParent=verified.PARENT, exactReviewPort=server.server_port,
        originalRawBuffersToRelease=5, originalPILBuffersToRelease=5,
        originalFailedCampaignRetained=True, finiteAcceptedHandoffRetained=True,
        inputHashes={str(Path(__file__).resolve()): sha(__file__), str(verified.OUT / 'report.json'): sha(verified.OUT / 'report.json')},
        fullPortAcceptance=False, goalStatus='active'), indent=2) + '\n')
    print(json.dumps(dict(prepared=True, originalRawBuffers=5, originalPILBuffers=5)), flush=True)


def retire():
    need(not RETIRED.exists(), 'Fresh exact terminal handoff retirement receipt')
    prepared = json.loads((OUT / 'report.json').read_text())
    accepted = json.loads((verified.OUT / 'report.json').read_text())
    need(prepared['passed'] and all(sha(p) == h for p, h in prepared['inputHashes'].items()) and
         all(sha(p) == h for p, h in accepted['inputHashes'].items()), 'Whole original failed/accepted outcomes unchanged')
    command = f'Get-CimInstance Win32_Process -Filter "ProcessId={verified.GAME} OR ProcessId={verified.PARENT}" | Select-Object ProcessId | ConvertTo-Json -Compress'
    query = subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(query.returncode == 0 and not query.stdout.strip() and not query.stderr.strip(), 'Both exact native/RAM producers absent')
    with socket.socket() as connection:
        connection.settimeout(1)
        need(connection.connect_ex(('127.0.0.1',prepared['exactReviewPort'])) != 0, 'Exact original preview listener closed')
    files = [p for folder in (verified.capture.OUT, verified.OUT, OUT) for p in folder.rglob('*') if p.is_file()]
    need(not any(p.suffix.lower() in ('.png','.wav','.bin','.exe','.zip') for p in files),
         'No raw media/ROM/build/archive in this finite verification batch')
    RETIRED.mkdir()
    (RETIRED / 'report.json').write_text(json.dumps(dict(passed=True, failedCampaignAndFiniteHandoffPreserved=True,
        exactNativeGameRetired=verified.GAME, exactRAMParentRetired=verified.PARENT,
        exactReviewPortClosed=prepared['exactReviewPort'], originalRawBuffersReleased=5, originalPILBuffersReleased=5,
        inputHashes={str(Path(__file__).resolve()): sha(__file__), **{str(p.resolve()): sha(p) for p in files}},
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,fullPortAcceptance=False,goalStatus='active'), indent=2) + '\n')
    print(json.dumps(dict(retired=True, originalBuffersReleased=10, reviewedHandoffPreserved=True)), flush=True)


if __name__ == '__main__':
    retire()
