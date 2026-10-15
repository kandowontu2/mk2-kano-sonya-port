"""Retain whole verified finite repair and original integration/release scope."""
import gzip
import json
import subprocess
from pathlib import Path
import stock_slideshow_row40_context as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated

ROOT=current.ROOT
OUT=ROOT/'audit_stock_slideshow_row40_verified_progress'
RUN=ROOT/'audit_natural_smoke_route_sonya_p2_stock_row40_repair_full_route'


def main():
    assert not OUT.exists() and not native.census()
    current.expected()
    report=json.loads((RUN/'native_stock_row40_regression.json').read_text())
    visual=json.loads((RUN/'native_stock_row40_visual_geometry.json').read_text())
    transport=json.loads((RUN/'report.json').read_text())
    compiled=json.loads((ROOT/'audit_stock_slideshow_row40_compiled/report.json').read_text())
    assert report['passed'] and report['resetRouteAccepted'] and transport['passed'] and visual['passed']
    assert report['postReturnFields']==4781 and len(report['actualFaultsRejected'])==4
    assert len(report['unchangedOriginalNativeScreens'])==41 and len(report['exactOriginalPhotoFrames'])==2
    assert all(frame['exactPhotoPosition']==[29,22] and frame['matchedSourcePixels']==21804
               for frame in report['exactOriginalPhotoFrames'])
    assert len(visual['exactNativeGeometryFaultsRejected'])==2
    assert not report['fullPortAcceptance'] and not visual['fullPortAcceptance'] and compiled['compiledIdentityAccepted']
    for filename in ('executed_sources.json.gz','executed_runtime_qualification_sources.json.gz'):
        with gzip.open(RUN/filename,'rt',encoding='utf-8') as f: sources=json.load(f)
        for path,row in sources.items():
            import hashlib
            assert hashlib.sha256(row['text'].encode()).hexdigest().upper()==row['sha256']
    handle=native.k.OpenProcess(0x1000,False,transport['nativeTerminal']['actualWindowsIdentity']['ParentProcessId'])
    if handle:
        code=native.w.DWORD()
        native.k.GetExitCodeProcess.argtypes=[native.w.HANDLE,native.c.POINTER(native.w.DWORD)]
        native.k.GetExitCodeProcess.restype=native.w.BOOL
        try:
            assert native.k.GetExitCodeProcess(handle,native.c.byref(code)) and code.value!=259
        finally:native.k.CloseHandle(handle)
    assert not (ROOT/'mame-mkp/build/mingw-gcc').exists()
    files={p for folder in (RUN,ROOT/'audit_stock_slideshow_row40_compiled')
           for p in folder.rglob('*') if p.is_file()}
    files.update(Path(__file__).resolve().parent/name for name in
        ('stock_slideshow_row40_context.py','qualify_stock_slideshow_row40_compiled.py',
         'capture_stock_slideshow_row40.py','qualify_stock_slideshow_row40_runtime.py',
         'seal_stock_slideshow_row40_runtime.py'))
    files.update((Path(__file__).resolve(),ROOT/'mk2ks_stock_slideshow_row40_regression.lua',
                  ROOT/'diagnostic_stock_slideshow_row40/build.log',ROOT/'diagnostic_stock_slideshow_row40/build-info.json',
                  ROOT/'diagnostic_stock_slideshow_row40/restoration.json',ROOT/'diagnostic_stock_slideshow_row40/cache_retirement.json'))
    storage=[]
    for path in sorted(files):
        assert path.resolve().is_relative_to(ROOT) and not path.is_symlink()
        assert path.suffix.lower() not in ('.exe','.zip','.bin','.mdata','.png','.rgb','.pcm','.wav')
        before,digest=allocated(path),current.sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
        assert current.sha(path)==digest
        storage.append(dict(path=str(path),sha256=digest,beforeAllocatedBytes=before,allocatedBytes=allocated(path)))
    scope=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining']
    assert len(scope)==6
    result=dict(goalStatus='active',fullPortAcceptance=False,publicPlayableChanged=False,
                previousGoalTurnClassification='progress: actual failed stock lookup localized and four-byte source conservation repair staged; one specific native compile started',
                thisGoalTurnClassification='progress: same compiler drained to actual success/restoration/cache removal; compiled whole guest identity checked; same physical replay ends without reset, genuine original photo exactly rendered; whole pre-failure field/input/HP/raster history conserved',
                candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,
                guestChangedBytes=4,originalStockPicturePointersPreserved=41,
                nativePictureReturnedAtField=125422,wholeOriginalPhysicalLedgerRecords=report['wholeUnchangedPreFailureRecords'],
                originalWholeNativeScreensConserved=41,wholeNativePixelsConserved=41*400*254,
                actualOriginalPhotoPixelsMatched=2*21804,postReturnFieldsWithoutReset=4781,
                actualRouteFaultsRejected=4,actualNativeRasterFaultsRejected=2,
                actualNativeTerminal=transport['nativeTerminal'],allRAMHostsReleased=True,
                compilerCacheAbsent=True,newBuilds=1,newROMCopies=0,newRawMedia=0,newZIPs=0,
                retainedCompiledCandidates=len(list(ROOT.glob('*/mkport_candidate.exe'))),
                newExecutableAllocatedBytes=compiled['singleNewExecutableAllocatedBytes'],
                exactCompressedTargets=storage,allocatedBytes=sum(r['allocatedBytes'] for r in storage),
                originalRemainingScope=scope,
                observationLimit='Full same-round Sonya Smoke survival was not accepted; actual walking/jump/punch/recovery, genuine loss and return were observed. Generic battle-global fields in mode1 attract are not automatically live-demo ownership proof.',
                nextAction='Review concrete current remaining integration/audio/UI/stage/finisher/secret/morph/cinematic evidence against the entire original objective. The late biography reset is now resolved, not a reason to repeat this unchanged route. Finish relevant combined current regression and matching public CMD/portable ZIP; do not promote as final while requirements remain unverified.')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(resetRouteAccepted=True,originalPhotoPixels=43608,
                         originalWholeScreensConserved=41,postReturnFields=4781,
                         allocatedBytes=result['allocatedBytes'],allRAMHostsReleased=True,fullPortAcceptance=False)))


if __name__=='__main__':main()
