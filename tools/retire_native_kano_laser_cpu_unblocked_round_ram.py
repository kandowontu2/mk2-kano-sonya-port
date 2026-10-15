"""Exact two-game/one-parser native census and RAM-parent release receipt.

No deletion, process killing, alternate cleanup bypass or public promotion.
"""
import json
import socket
import subprocess
from pathlib import Path
import seal_native_kano_laser_cpu_unblocked_round_progress as seal

ROOT,need,sha,base=seal.ROOT,seal.need,seal.sha,seal.base
OUT=ROOT/'audit_native_kano_laser_cpu_unblocked_round_retirement'
PARENT=143748
NATIVES=[155996,188048,186940]
PORT=51559


def run():
    need(not OUT.exists(),'Fresh exact two-job/one-compiler RAM retirement')
    sealed_path=seal.OUT/'report.json';sealed=json.loads(sealed_path.read_text())
    need(sealed['passed'] and sealed['actualCounterexamplesRejected']==62 and
         sealed['originalRAMRastersToRelease']==42 and sealed['actualNativeFullHealthResetAndSixtyLiveFieldsVerified'] and
         all(sha(p)==h for p,h in sealed['inputHashes'].items()),'Exact immutable actual native ring and KO/reset progress sealed')
    folders=[ROOT/'audit_native_kano_laser_cpu_leg_children_guard_ram',
             ROOT/'audit_native_kano_laser_cpu_post_ko_ram']
    terminals=[]
    for folder in folders:
        files=list(folder.glob('*/native_terminal.json'));need(len(files)==1,'One exact native game terminal per fresh case')
        terminals.append(json.loads(files[0].read_text()))
    parser=ROOT/'audit_native_kano_laser_cpu_post_ko_source/native_terminal.json'
    terminals.append(json.loads(parser.read_text()))
    need([t['pid']for t in terminals]==NATIVES and all(t['nativeExit']==0 and t['actualWindowsIdentity']['ParentProcessId']==PARENT for t in terminals),
         'Exact two games and one native compiler belong to only this RAM parent and actually terminated0')
    query='Get-CimInstance Win32_Process -Filter "'+' OR '.join('ProcessId='+str(pid)for pid in [PARENT,*NATIVES])+'" | Select-Object ProcessId,ParentProcessId,ExecutablePath | ConvertTo-Json -Compress'
    job=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(job.returncode==0 and not job.stdout.strip() and not job.stderr.strip(),'All exact this-pass producer and RAM parent handles authoritatively absent')
    with socket.socket()as connection:
        connection.settimeout(1);need(connection.connect_ex(('127.0.0.1',PORT))!=0,'Exact original RAM image review port closed')
    names=['audit_native_kano_laser_cpu_leg_children_guard_ram','audit_native_kano_laser_cpu_leg_children_guard_repeat_checked',
           'audit_native_kano_laser_cpu_leg_children_guard_initializer_source','audit_native_kano_laser_cpu_leg_children_guard_health_checked',
           'audit_native_kano_laser_cpu_leg_children_guard_faults_checked','audit_native_kano_laser_cpu_leg_children_guard_review',
           'audit_native_kano_laser_cpu_post_ko_source','audit_native_kano_laser_cpu_post_ko_ram',
           'audit_native_kano_laser_cpu_post_ko_checked','audit_native_kano_laser_cpu_post_ko_ground_checked',
           'audit_native_kano_laser_cpu_unblocked_round_progress']
    files=[p for name in names for p in (ROOT/name).rglob('*')if p.is_file()]
    need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'No raw media/ROM/build/archive copies created by this batch')
    need(not(ROOT/'mame-mkp/build/mingw-gcc').exists() and
         sha(ROOT/'PLAY_LATEST_KANO_SONYA.cmd')=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
         'Generated buildcache absent; public CMD unchanged')
    pins={str(p.resolve()):sha(p)for p in [Path(__file__),sealed_path,*files]}
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,exactRAMParentRetired=PARENT,
        exactNativeGamesAndCompilerRetired=NATIVES,exactReviewPortClosed=PORT,originalRAMRastersReleased=42,
        actualNativeGameBoots=2,nativeCompilerOnlyBoots=1,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        batchEvidenceLogicalBytesBeforeRetirementReport=sum(p.stat().st_size for p in files),inputHashes=pins,
        earlierFailuresPreserved=True,previousPolicyRetainedTimeoutScreenshotUntouched=True,
        publicPlayableChanged=False,fullPortAcceptance=False,goalStatus='active'))
    print(json.dumps(dict(passed=True,allExactNativeAndRAMHandlesRetired=True,originalRAMRastersReleased=42,
                         newBuilds=0,newROMCopies=0,publicPlayableChanged=False)),flush=True)


if __name__=='__main__':run()
