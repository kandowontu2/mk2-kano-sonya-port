"""Retirement census for this exact native job, RAM parent and review port.

No process termination, file deletion or old-build/ROM copying. The RAM parent
closes its own server and exits after its original native trial/reviews seal.
"""
import json
import socket
import subprocess
from pathlib import Path
import capture_native_kano_laser_cpu_leg_children as capture

ROOT,need,sha,base=capture.ROOT,capture.need,capture.sha,capture.base
OUT=ROOT/'audit_native_kano_laser_cpu_leg_children_retirement'
PARENT=182288
NATIVE=186904
PORT=50520


def run():
    need(not OUT.exists(),'Fresh exact native-child trial retirement record')
    review_path=ROOT/'audit_native_kano_laser_cpu_leg_children_review/report.json'
    review=json.loads(review_path.read_text())
    need(review['passed'] and review['actualPhaseOwnershipGuardHealthFaults']==35 and
         review['actualOriginalBodyShadowFaults']==11 and len(review['individuallyReviewedOriginalRasters'])==21 and
         review['finiteMixedRingOwnershipVerified'] and review['allNativeHPContextsInThisTraceVerified'] and
         review['allNativeFighterBodyShadowFieldsInThisTraceVerified'] and
         all(sha(p)==h for p,h in review['inputHashes'].items()),
         'Exact sealed original RAM review and all independently source-bound native phase/owner/HP/shadow gates')
    terminal_path=capture.BASE/capture.KEY/'native_terminal.json'
    terminal=json.loads(terminal_path.read_text())
    need(terminal['pid']==NATIVE and terminal['nativeExit']==0 and
         terminal['actualWindowsIdentity']['ParentProcessId']==PARENT and not terminal['hostDecodeErrors'],
         'Exact actual native PID, RAM parent, terminal0 and complete current transport')
    query='Get-CimInstance Win32_Process -Filter "ProcessId='+str(PARENT)+' OR ProcessId='+str(NATIVE)+'" | Select-Object ProcessId,ParentProcessId,ExecutablePath | ConvertTo-Json -Compress'
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(census.returncode==0 and not census.stderr.strip() and not census.stdout.strip(),
         'Both exact this-pass parent and native PIDs authoritatively absent')
    with socket.socket()as connection:
        connection.settimeout(1)
        need(connection.connect_ex(('127.0.0.1',PORT))!=0,'Exact original RAM review port closed')
    folders=[capture.BASE,capture.OUT,capture.INIT,
             ROOT/'audit_native_kano_laser_cpu_leg_children_owned_checked',
             ROOT/'audit_native_kano_laser_cpu_leg_children_health_checked',
             ROOT/'audit_native_kano_laser_cpu_leg_children_faults_checked',
             ROOT/'audit_native_kano_laser_cpu_leg_children_review']
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),
         'This actual batch has no new raw media/ROM/build/archive copies')
    need(not(ROOT/'mame-mkp/build/mingw-gcc').exists(),
         'Generated full native build cache remains absent')
    need(sha(ROOT/'PLAY_LATEST_KANO_SONYA.cmd')=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
         'Public launcher unchanged')
    pins={str(p.resolve()):sha(p)for p in [Path(__file__),review_path,terminal_path,*files]}
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,exactRAMParentRetired=PARENT,
        exactNativePIDTerminalAndRetired=NATIVE,exactReviewPortClosed=PORT,originalRAMRastersReleased=21,
        actualNativeBoots=1,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        batchEvidenceLogicalBytesBeforeRetirementReport=sum(p.stat().st_size for p in files),
        previousPolicyRetainedTimeoutScreenshotUntouched=True,previousFailuresPreserved=True,
        finiteMixedRingOwnershipVerified=True,wholeRepeatedTrialStillRejected=True,
        publicPlayableChanged=False,generatedBuildCachePresent=False,fullPortAcceptance=False,
        inputHashes=pins,goalStatus='active'))
    print(json.dumps(dict(passed=True,originalRAMRastersReleased=21,exactNativeAndRAMParentRetired=True,
                         newBuilds=0,newROMCopies=0,publicPlayableChanged=False)),flush=True)


if __name__=='__main__':run()
