"""Retire only this pass's exact RAM parents/native handles and temporary snapshot.

Keep every executed rejection and finite diagnostic proof. Never terminate
other tasks, delete a ROM/build, or promote the public launcher/release.
"""
import json
import socket
import subprocess
from pathlib import Path
import capture_native_kano_laser_cpu_leg_repeat_p2 as capture

ROOT,need,sha,base=capture.ROOT,capture.need,capture.sha,capture.base
OUT=ROOT/'audit_native_kano_laser_cpu_leg_ram_retirement'
SCREEN=ROOT/'audit_native_kano_laser_cpu_leg_repeat_ram/leg_cpu_sonya_p1_human_kano_p2/snap/mk2ks/0000.png'
SCREEN_SHA='864C630578E7D035AA794E7305D00CA68DFD10B84F01BE213BFA08A989F33425'
PARENTS=(182520,105512)
PORTS=(54127,53260)
CMD_SHA='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5'


def record_snapshot():
    need(not OUT.exists(),'Fresh exact pass retirement')
    need(SCREEN.resolve().is_relative_to(ROOT.resolve()) and SCREEN.is_file()and sha(SCREEN)==SCREEN_SHA,
         'Exact this-pass timeout screenshot only, not another user asset')
    folder=SCREEN.parents[2]
    process=json.loads((folder/'process.json').read_text())
    need(process['pid']==188004 and '-str'in process['command']and
         process['command'][process['command'].index('-str')+1]=='100' and
         process['command'][process['command'].index('-snapshot_directory')+1]==str(folder/'snap'),
         'Exact actual native timeout/snapshot-directory arguments')
    report=json.loads((folder/'result.json').read_text())
    need(not report['passed']and report['nativeExit']==0,'Exact terminal rejected non-Sonya trial')
    core=ROOT/'mame-mkp/src/emu/video.cpp'
    source=core.read_text()
    need('if (m_seconds_to_run != 0 && emutime.seconds() >= m_seconds_to_run)'in source and
         '// create a final screenshot'in source,'Local framework source explains timeout-generated final snapshot')
    OUT.mkdir();base.save(OUT/'timeout_snapshot_before_cleanup.json',dict(path=str(SCREEN),sha256=SCREEN_SHA,
        bytes=SCREEN.stat().st_size,actualNativePID=188004,individuallyViewed=True,
        provenance='Native timed-run final screenshot in its exact recorded snapshot directory; not a Lua RAM media sink',
        generatedSnapshotRemovalAuthorizedByWorkspaceCleanup=True,priorZeroRawMediaTemplateNotVerified=True,
        frameworkSourceSHA256=sha(core),newROMCopies=0,newBuilds=0,fullPortAcceptance=False))
    print('Exact 51,674-byte native timeout screenshot recorded before cleanup.',flush=True)


def run():
    need(OUT.exists()and not(OUT/'report.json').exists(),'Snapshot pre-cleanup recorded; final retirement fresh')
    before=json.loads((OUT/'timeout_snapshot_before_cleanup.json').read_text())
    need(before['sha256']==SCREEN_SHA and not SCREEN.exists(),'Only exact generated timeout screenshot removed')
    diagnostic=ROOT/'audit_native_kano_laser_cpu_leg_diagnostic_review/report.json'
    first=ROOT/'audit_native_kano_laser_cpu_leg_first_diagnostic_review/report.json'
    compiler=ROOT/'audit_native_kano_laser_cpu_leg_children_source/report.json'
    reports=[json.loads(p.read_text())for p in (diagnostic,first,compiler)]
    need(all(r['passed']for r in reports) and reports[0]['selectedOriginalCompletedLegs']==2 and
         len(reports[0]['actualTypedLegFaultsRejected'])==16 and reports[0]['individuallyReviewedOriginalRasters']==42 and
         len(reports[1]['reviewedOriginalRasters'])==4 and reports[2]['actualNativeParserAccepted']and
         not reports[2]['childGameplayAccepted'],'Exact finite diagnostics and new passive compiler guard; broader acceptance still false')
    natives=[188004,90028,189160]
    for leaf in ('audit_native_kano_laser_cpu_leg_repeat_source','audit_native_kano_laser_cpu_leg_repeat_p2_source',
                 'audit_native_kano_laser_cpu_leg_children_source'):
        value=json.loads((ROOT/leaf/'native_terminal.json').read_text())
        need(value['nativeExit']==0,'Actual native parser terminal0');natives.append(value['pid'])
    ids=sorted(set([*PARENTS,*natives]))
    query='Get-CimInstance Win32_Process -Filter "'+' OR '.join('ProcessId='+str(pid)for pid in ids)+'" | Select-Object ProcessId,ParentProcessId,ExecutablePath | ConvertTo-Json -Compress'
    job=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(job.returncode==0 and not job.stderr.strip()and not job.stdout.strip(),'Only exact this-pass RAM/native handles authoritatively absent')
    for port in PORTS:
        with socket.socket()as connection:
            connection.settimeout(1);need(connection.connect_ex(('127.0.0.1',port))!=0,'Exact RAM review port closed')
    need(sha(ROOT/'PLAY_LATEST_KANO_SONYA.cmd')==CMD_SHA and not(ROOT/'mame-mkp/build/mingw-gcc').exists(),
         'Public launcher unchanged; generated build cache absent')
    files=[p for folder in ROOT.glob('audit_native_kano_laser_cpu_leg_*')if folder.is_dir()for p in folder.rglob('*')if p.is_file()]
    need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),
         'No raw media/ROM/build/archive remains in this pass evidence')
    pins={str(p.resolve()):sha(p)for p in (Path(__file__),diagnostic,first,compiler,OUT/'timeout_snapshot_before_cleanup.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd')}
    base.save(OUT/'report.json',dict(passed=True,exactRAMParentsRetired=list(PARENTS),exactNativeHandlesRetired=natives,
        exactReviewPortsClosed=list(PORTS),originalRAMRastersReleased=46,allActualNativeTerminalsPreserved=True,
        oneGeneratedNativeTimeoutScreenshotRemoved=True,removedSnapshotSHA256=SCREEN_SHA,removedSnapshotBytes=51674,
        removalRecovery='Discarded generated diagnostic screenshot; hash/provenance retained, no user source or ROM removed',
        passEvidenceLogicalBytesBeforeFinalRetirementReport=sum(p.stat().st_size for p in files),inputHashes=pins,
        wholeRepeatedTrialsStillRejected=True,extraDamageActorMainOwnershipPending=True,
        nextAction='Run current native mixed CPU leg/projectile tests with the seven-expansion qualified child/guard observer; fully bind child allocation, ownership, contact and retirement before accepting the mixed case.',
        fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newZIPs=0,
        rawMediaFilesRemaining=0,generatedBuildCachePresent=False,goalStatus='active'))
    print(json.dumps(dict(passed=True,originalRAMRastersReleased=46,allExactParentsAndPortsRetired=True,
                         generatedTimeoutScreenshotRemoved=True,publicPlayableChanged=False)),flush=True)


if __name__=='__main__':run()
