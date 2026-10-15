"""Preserve full goal scope and current live compile identity; never claim a runtime fix."""
import ctypes as c,json,subprocess
from ctypes import wintypes as w
from pathlib import Path
import native_process_census_v6647 as census
ROOT=Path(__file__).resolve().parents[1]
def need(v,m):
    if not v:raise ValueError(m)
if __name__=='__main__':
    out=ROOT/'audit_native_cpu_finisher_dispatch_progress'
    need(not out.exists(),'Fresh immutable progress snapshot')
    scope=json.loads((ROOT/'audit_native_guard_campaign_progress/report.json').read_text())
    cause=json.loads((ROOT/'audit_native_cpu_finisher_dispatch_cause_checked/report.json').read_text())
    source=json.loads((ROOT/'audit_native_cpu_finisher_dispatch_source/report.json').read_text())
    need(cause['passed'] and source['passed'] and not source['nativeRepairAccepted'],'Actual causal and source-only checks')
    k=census.k
    k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)];k.GetExitCodeProcess.restype=w.BOOL
    handle=k.OpenProcess(0x101000,False,165448);need(handle,'Actual known project compiler kernel handle')
    try:
        created,ended,kernel,user=(w.FILETIME()for _ in range(4))
        need(k.GetProcessTimes(handle,c.byref(created),c.byref(ended),c.byref(kernel),c.byref(user)),'Actual compiler creation time')
        creation=((created.dwHighDateTime<<32)|created.dwLowDateTime)/10**7-11644473600
        exitcode=w.DWORD();need(k.GetExitCodeProcess(handle,c.byref(exitcode))and exitcode.value==259,'Verified wait on same live native compiler, not a log/lock inference')
    finally:k.CloseHandle(handle)
    raw=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "Get-CimInstance Win32_Process -Filter 'ProcessId=165448 OR ProcessId=146220' | Select-Object ProcessId,ParentProcessId,ExecutablePath,CreationDate,CommandLine | ConvertTo-Json -Compress"],
        check=True,capture_output=True,text=True).stdout
    processes=json.loads(raw)
    make=next(p for p in processes if p['ProcessId']==165448)
    shell=next(p for p in processes if p['ProcessId']==146220)
    need(make['ParentProcessId']==146220 and make['ExecutablePath']==r'C:\Strawberry\c\bin\gmake.exe' and
         'SUBTARGET=mkport' in make['CommandLine'] and 'build_native_cpu_finisher_dispatch.ps1' in shell['CommandLine'],
         'Actual parent, executable and exact project build command')
    report=dict(passed=True,goalStatus='active',fullGoalComplete=False,fullPortAcceptance=False,
        previousGoalTurnClassification='no progress: status-only answer; revalidated failure and took causal replay/source correction next.',
        thisGoalTurnClassification='progress: two native-terminal identical physical replays establish exact CPU17 first-finisher table overread into Mileena choreography and actual global cache corruption; source-only two-table correction qualified. One real compiler live, runtime repair not yet proven.',
        originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],acceptedPriorWorkNotReset=scope['acceptedPriorWorkNotReset'],
        actualCausalNativeRuns=2,actualNativeCausalExitCodes=[0,0],
        actualCauseFaultsRejected=len(cause['actualFaultsRejected']),
        actualSourceFaultsRejected=len(source['actualFaultsRejected']),
        sourceOnlyCorrectionAccepted=True,nativeRepairAccepted=False,
        actualLiveCompiler=dict(processes=processes,kernelCreationUnix=creation,kernelExitCode=exitcode.value,sessionID=66804),
        compilerCacheTemporaryAndRetirementPending=True,newPrivateBuildPending=True,
        publicBuildPromoted=False,releaseZIPProduced=False,noLiveNativeGames=not census.census(),
        nextAction='Wait on exact live compiler, verify native source/executable restoration and temporary cache retirement, then cold-run capture_native_cpu_finisher_repair_regression.py; independently verify real finisher lookup/choreography/handoff, no overrun and retained RAM visuals. Keep all original goal requirements active.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(progress=True,compilerPID=165448,sourceOnlyAccepted=True,nativeRepairAccepted=False,fullGoalComplete=False)))
