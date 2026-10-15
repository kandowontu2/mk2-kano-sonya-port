"""Finite progress and retained failures; never final port/build acceptance."""
import gzip
import hashlib
import json
import subprocess
from pathlib import Path
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
import qualify_stock_slideshow_row40 as diagnosis

ROOT=diagnosis.ROOT
OUT=ROOT/'audit_stock_slideshow_row40_progress'


def main():
    assert not OUT.exists() and not native.census()
    guard_path=diagnosis.OUT/'report.json'
    guard=json.loads(guard_path.read_text())
    assert guard['passed'] and guard['sourceOnlyAccepted'] and not guard['nativeFixAccepted']
    assert len(guard['actualRecordFaultsRejected'])==4 and guard['expectedGuestChangedBytes']==4
    assert diagnosis.check_sources()==guard['stagedSourceHashes']
    runs=[ROOT/('audit_natural_smoke_route_sonya_p2_'+label) for label in
          ('graphics_copy_pointer_provenance','graphics_picture_lookup_provenance',
           'graphics_picture_lookup_guarded')]
    all_files=set()
    for folder in runs:
        report=json.loads((folder/'report.json').read_text())
        assert not report['passed']
        with gzip.open(folder/'executed_sources.json.gz','rt',encoding='utf-8') as f: archive=json.load(f)
        for name,row in archive.items():
            assert row['sha256']==report['inputHashes'][name]==hashlib.sha256(row['text'].encode()).hexdigest().upper()
        handle=native.k.OpenProcess(0x1000,False,report['nativeTerminal']['actualWindowsIdentity']['ParentProcessId'])
        if handle:
            # A tool handle can keep an already-exited Windows process object
            # readable. OpenProcess success alone is not a liveness test.
            code=native.w.DWORD()
            native.k.GetExitCodeProcess.argtypes=[native.w.HANDLE,native.c.POINTER(native.w.DWORD)]
            native.k.GetExitCodeProcess.restype=native.w.BOOL
            try:
                assert native.k.GetExitCodeProcess(handle,native.c.byref(code))
                assert code.value!=259, 'Original RAM collector still active'
            finally:native.k.CloseHandle(handle)
        all_files.update(p for p in folder.rglob('*') if p.is_file())
    assert json.loads((runs[1]/'observer_failure.json').read_text())['operatorTerminatedExactProbePID']
    assert all(json.loads((runs[i]/'report.json').read_text())['nativeTerminal']['nativeExit']==0 for i in (0,2))
    command="Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'gmake.exe' -and $_.CommandLine -like '*SUBTARGET=mkport*'} | Select-Object ProcessId,ParentProcessId,ExecutablePath,CommandLine,CreationDate | ConvertTo-Json -Compress"
    proc=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True,check=True)
    live=json.loads(proc.stdout)
    live=live if isinstance(live,list) else [live]
    assert live and all('SUBTARGET=mkport' in r['CommandLine'] for r in live)
    assert not (ROOT/'diagnostic_stock_slideshow_row40/build-info.json').exists()
    assert (ROOT/'mame-mkp/build/mingw-gcc').is_dir()
    all_files.update((Path(__file__).resolve(),Path(diagnosis.__file__).resolve(),guard_path,
                      ROOT/'tools/build_stock_slideshow_row40.ps1',ROOT/'mk2ks_stock_slideshow_row40_regression.lua'))
    all_files.update(p for p in diagnosis.STAGE.iterdir() if p.is_file())
    storage=[]
    for path in sorted(all_files):
        assert path.resolve().is_relative_to(ROOT) and not path.is_symlink()
        assert path.suffix.lower() not in ('.exe','.zip','.bin','.mdata','.png','.rgb','.pcm','.wav')
        digest=diagnosis.sha(path);before=allocated(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
        assert diagnosis.sha(path)==digest
        storage.append(dict(path=str(path),sha256=digest,beforeAllocatedBytes=before,allocatedBytes=allocated(path)))
    remaining=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining']
    assert len(remaining)==6
    result=dict(goalStatus='active',fullPortAcceptance=False,publicPlayableChanged=False,
                previousGoalTurnClassification='no progress: acknowledgement; revalidated the still-live exact native probe',
                thisGoalTurnClassification='progress: actual registers/lookup establish omitted stock row40 causing runaway copy and reset; complete original photo decoded; minimal conservation source repair qualified and one real build started',
                originalRemainingScope=remaining,
                diagnosisSHA256=diagnosis.sha(guard_path),guestChangedBytes=4,
                originalFailedRunsPreserved=2,observerFailurePreservedSeparately=True,allNativeTestsTerminal=True,allRAMHostsReleased=True,
                actualLiveCompilerProcesses=live,compilerSessionID=47000,compilerCacheLive=True,
                newBuildsStarted=1,newBuildsAccepted=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
                storage=storage,allocatedBytes=sum(r['allocatedBytes'] for r in storage),
                nextAction='Drain exact live compiler session47000, no restart. Verify native exit/restoration/cache retirement and bind new candidate to entire four-byte-only guest. Then replay same unassisted physical secret/return/attract sequence with mk2ks_stock_slideshow_row40_regression.lua; prove real row40 header/native return/visible photo/no reset through terminal. Full current regression/public CMD/ZIP still required.')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(progress='actual root cause and minimal source correction',compilerSessionID=47000,
                         liveCompilerPIDs=[r['ProcessId'] for r in live],allRAMHostsReleased=True,
                         allocatedBytes=result['allocatedBytes'],fullPortAcceptance=False)))


if __name__=='__main__':main()
