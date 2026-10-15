"""Actual finite repair/art review and next source correction; full goal retained."""
import ctypes as c,hashlib,json,subprocess
from ctypes import wintypes as w
from pathlib import Path
import native_process_census_v6647 as census
ROOT=Path(__file__).resolve().parents[1]
def need(v,m):
    if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
if __name__=='__main__':
    out=ROOT/'audit_native_cpu_finisher_spacing_progress'
    need(not out.exists(),'Fresh immutable progress/art review')
    scope=json.loads((ROOT/'audit_native_guard_campaign_progress/report.json').read_text())
    runtimepath=ROOT/'audit_native_cpu_finisher_repair_regression_checked/report.json'
    sourcepath=ROOT/'audit_native_cpu_finisher_spacing_source/report.json'
    runtime=json.loads(runtimepath.read_text());source=json.loads(sourcepath.read_text())
    need(runtime['passed'] and runtime['noCacheOverrun'] and source['passed'] and
         source['initializedGuestByteDelta']==6 and not source['nativeRepairAccepted'] and
         all(sha(p)==h for p,h in runtime['inputHashes'].items()) and
         all(sha(p)==h for p,h in source['inputHashes'].items()),
         'Whole executed finite repair and independently qualified staged distance inputs unchanged')
    expected={
        1:'BD4A4C924A101FAA595F3C50E068B837688E1FE160E86306F546F700825DD9A1',
        30:'06A9B08DAFFADF4600A7A183630D7C4577A63529D64E24B53582257840AA9E0F',
        90:'C16B6003E6B57C6B1B6B9D440263C7DDDF12FB23F3232DE1BEEAE44BBF6018DB',
        180:'E1024FDC0A506A4B81A36162EE68D088A094434696FE46374045AC64B3E2A80E',
        330:'541B343518FAD4ECD9520FBD8FD63430D35A60E7C5A2CB174D0775FF0A684144',
        900:'FD23748C1960AA55913186F414ECB85B9DFFF1B2CA2FBFD2034D91F33033EA5C'}
    images={r['filename']:r for r in runtime['actualNativeRGBScenes']}
    need(all(len(h)==64 and images[f'postjoin_finisher_regression_age{age}.png']['sha256']==h for age,h in expected.items()),
         'All six actual native RAM fields displayed as800x834 atlas and visually inspected')
    raw=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "Get-CimInstance Win32_Process -Filter 'ProcessId=157292 OR ProcessId=160068' | Select-Object ProcessId,ParentProcessId,ExecutablePath,CreationDate,CommandLine | ConvertTo-Json -Compress"],
        check=True,capture_output=True,text=True).stdout
    processes=json.loads(raw);make=next(p for p in processes if p['ProcessId']==157292)
    shell=next(p for p in processes if p['ProcessId']==160068)
    need(make['ParentProcessId']==160068 and make['ExecutablePath']==r'C:\Strawberry\c\bin\gmake.exe' and
         'SUBTARGET=mkport' in make['CommandLine'] and 'build_native_cpu_finisher_spacing.ps1' in shell['CommandLine'],
         'Exact actual live compiler PID/parent/path/command, not inferred from log or lock')
    k=census.k;k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)];k.GetExitCodeProcess.restype=w.BOOL
    handle=k.OpenProcess(0x101000,False,157292);need(handle,'Known actual compiler kernel handle')
    try:
        created,ended,kernel,user=(w.FILETIME() for _ in range(4))
        need(k.GetProcessTimes(handle,c.byref(created),c.byref(ended),c.byref(kernel),c.byref(user)),'Actual kernel creation')
        creation=((created.dwHighDateTime<<32)|created.dwLowDateTime)/10**7-11644473600
        exitcode=w.DWORD();need(k.GetExitCodeProcess(handle,c.byref(exitcode)) and exitcode.value==259,'Actual same compiler live now')
    finally:k.CloseHandle(handle)
    need(not census.census(),'All native games terminal; old RAM review host also exited normally')
    public=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(public)=='90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE','No premature public launcher promotion')
    paths=[Path(__file__),runtimepath,sourcepath,public,
        ROOT/'tools/build_native_cpu_finisher_spacing.ps1',ROOT/'tools/native_cpu_finisher_spacing_context.py',
        ROOT/'tools/capture_native_cpu_finisher_spacing.py',ROOT/'mk2ks_native_cpu_finisher_spacing.lua',
        ROOT/'audit_native_cpu_finisher_handoff_checker_failure/report.json',
        ROOT/'audit_native_cpu_finisher_handoff_register_checker_failure/report.json',
        ROOT/'audit_native_cpu_finisher_view_digest_journal_failure/report.json']
    report=dict(passed=True,goalStatus='active',fullGoalComplete=False,fullPortAcceptance=False,
        previousGoalTurnClassification='no progress: user-requested status answer only; resumed actual retained replay review and source work.',
        thisGoalTurnClassification='progress: actual cold finite repaired finisher/clean winner/loss/continue qualified; six native RAM images viewed; real111pixel CPU gap exceeds own80pixel command range; dedicated six-byte17/18 approach profiles independently source-qualified and compiling.',
        originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],acceptedPriorWorkNotReset=scope['acceptedPriorWorkNotReset'],
        actualNativeReplayExit=0,ownCPUKanoHandoffFrame=36401,actualLaterLossFrame=36709,
        subsequentGenuineSelectionAtExit=True,finiteRuntimeFaultsRejected=len(runtime['actualFaultsRejected']),
        actualViewedNativeFrameSHA256={str(age):h for age,h in expected.items()},
        visualReview=dict(actualAtlasViewed=True,rawImagesWritten=0,
            observations=['Own Kano skeleton extraction phases, Sonya own victim body and native Kano winner name visible.',
                'No selector portrait/pose persists in the five displayed gameplay/finisher/winner phases.',
                'Age900 is a genuine new paid-continue CSS, corroborated by native loss/selection state.',
                'Reach is too wide: native finisher field records111pixel gap; own human command allows80.'],
            completeFinisherNaturalnessAccepted=False,completeSceneAudioOrRasterAccepted=False),
        dedicatedProfiles=source['ownDistanceProfiles'],spacingSourceOnlyAccepted=True,spacingRuntimeAccepted=False,
        spacingSourceFaultsRejected=len(source['actualFaultsRejected']),
        actualLiveCompiler=dict(processes=processes,kernelCreationUnix=creation,kernelExitCode=exitcode.value,sessionID=68933),
        compilerCacheTemporaryAndRetirementPending=True,oldCompilerCacheAlreadyRetired=True,
        payloadAndWAVSharedHardlinksPlanned=True,noNewROMOrRawMediaCopies=True,
        allRAMReviewHostsReleased=True,publicBuildPromoted=False,finishedReleaseZIPProduced=False,
        inputHashes={str(p.resolve()):sha(p) for p in paths},
        nextAction='Poll exact compiler session68933; after actual terminal0 validate whole new guest/source/executable restore and cache retirement. Then cold-run capture_native_cpu_finisher_spacing.py in a RAM-retaining console and independently inspect real returned packed profile/entry gap/continuous actor geometry, cache writes, winner/loss/continue and actual RGB. No second choreography or full goal claim; preserve all original14 requirements and6 remaining groups.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(progress=True,finiteRepairedNativeRunQualified=True,nativeImagesActuallyReviewed=6,
        spacingSourceQualified=True,compilerPID=157292,compilerSession=68933,
        publicUnchanged=True,fullGoalComplete=False)))
