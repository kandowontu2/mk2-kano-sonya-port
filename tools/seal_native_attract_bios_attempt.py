"""Retain real rendered biography progress and the unresolved native demo stall."""
import gzip
import hashlib
import json
import subprocess
from pathlib import Path
import native_attract_bios_context as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def seal(c):
    need(not native.census(),'Actual original native job terminal before sealing')
    guest=current.expected()
    report=json.loads((c['folder']/'native_attract_identity_and_pictures.json').read_text())
    need(c['guest']==guest and report['nativeBiographyAndPublishedDemoIDsAccepted'] and
         report['nativeOwnBiographyPhotosAccepted'] and not report['passed'] and
         not report['completeNativeAttractCycleAccepted'] and report['actualSonyaP1DemoStall']['observed'],
         'Do not turn genuine rendered/identity progress into an attract-stability pass')
    reviewed=[c['rgbFrames'][i] for i in (0,10,13,11,14)]
    need([r['header']['stage'] for r in reviewed]==['startup_240','bio_17_delay_180','bio_18_delay_180','demo_1_17_delay_90','demo_1_18_delay_90'], 'Exact original screens actually inspected in this attempt')
    for row in reviewed:need(hashlib.sha256(row['pixels']).hexdigest().upper()==row['header']['sha256'],'Whole unchanged original raster reviewed')
    build=ROOT/current.NAME
    meta=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
    receipt=dict(goalStatus='active',fullPortAcceptance=False,publicPlayableChanged=False,
      previousGoalTurnClassification='progress: stock biography row40 reset repaired and native route/rendering verified',
      thisGoalTurnClassification='progress: original attract proxy/omission found, native biography/demo additions compiled, entire initialized guest checked, genuine own photographs and IDs proven, actual Sonya P1 demo-start stall exposed by full40-minute logical run',
      candidate=current.NAME,executableSHA256=meta['executable_sha256'],guestSHA256=meta['expected_guest_sha256'],
      nativeCompilerExit=0,preexistingWorkingFilesRestored=True,compilerCacheAbsent=not (ROOT/'mame-mkp/build/mingw-gcc').exists(),
      executableAllocatedBytes=allocated(build/'mkport_candidate.exe'),
      exactOwnBiographyPhotoPixelsMatched=43608,ownBiographyNamesAndBodiesVisuallyReviewed=True,
      nativePublishedDemoOwners=report['actualTrueDemoOwners'],nativeTerminal=c['terminal'],
      actualSonyaP1DemoStall=report['actualSonyaP1DemoStall'],
      visualObservations=['Native fresh CMOS screen explicitly requests any button to continue; ordinary High Punch clears it.',
       'KANO/SONYA names and original donor photos render in original biography frames with complete native-layout story text.',
       'Kano demo displays his real body and lifebar, with Cage performing a native projectile.',
       'Sonya demo displays her real body and lifebar versus Kitana, but full field ledger proves the new P1 demo never leaves its start state. This is not accepted stability.'],
      viewedOriginalScreens=[r['header'] for r in reviewed],fullAttractAudioAccepted=False,
      originalRemainingScope=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining'],
      nextAction='Trace the same natural Sonya/Kitana demo-start using passive native attract controller, fight-start task and timer provenance. Correct the real blocked path, never proxy the character or force guest state. Then verify full native roster/demo rotation and mode-owned audio, all original remaining integration requirements, matching public CMD and finished portable ZIP.',
      newBuilds=1,newROMCopies=0,newRawMedia=0,newZIPs=0)
    for leaf in ('executed_qualification_sources.json.gz','verified_progress.json'):
        need(not (c['folder']/leaf).exists(),'Fresh immutable qualification and progress receipts')
    import sys
    sources={}
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            path=Path(file).resolve();sources[str(path)]=dict(sha256=sha(path),text=path.read_text())
    with gzip.open(c['folder']/'executed_qualification_sources.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f)
    (c['folder']/'verified_progress.json').write_text(json.dumps(receipt,indent=2)+'\n')
    paths=[p for folder in (c['folder'],ROOT/'audit_native_attract_bios_cold',ROOT/'audit_native_attract_bios_source',ROOT/'audit_native_attract_bios_checker_failure',ROOT/'source_native_attract_bios') for p in folder.rglob('*') if p.is_file()]
    paths.extend(build/leaf for leaf in ('build.log','build-info.json','restoration.json','cache_retirement.json'))
    storage=[]
    for path in paths:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(),'Explicit in-workspace evidence file')
        digest=sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],check=True,capture_output=True)
        need(sha(path)==digest,'Storage compression preserves every actually executed evidence byte')
        storage.append(dict(path=str(path),allocatedBytes=allocated(path),sha256=digest))
    (c['folder']/'storage_receipt.json').write_text(json.dumps(dict(passed=True,compilerCacheAbsent=True,exactFiles=storage,newExecutableAllocatedBytes=receipt['executableAllocatedBytes'],newROMCopies=0,newZIPs=0),indent=2)+'\n')
    print(json.dumps(dict(actualBiographiesVerified=True,exactOwnPhotoPixels=43608,sonyaDemoStallUnresolved=True,compilerCacheAbsent=receipt['compilerCacheAbsent'],newExecutableAllocatedBytes=receipt['executableAllocatedBytes'],evidenceAllocatedBytes=sum(r['allocatedBytes'] for r in storage),fullPortAcceptance=False)))
    return receipt
