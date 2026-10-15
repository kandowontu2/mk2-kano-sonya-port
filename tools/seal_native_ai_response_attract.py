"""Seal this real native AI/attract attempt without overstating integration."""
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def seal(c,reviewed_stages):
    need(not native.census(),'Same actual emulator terminal before sealing')
    need(c['guest']==current.expected(),'Entire compiled guest still exact source-derived implementation')
    out=c['folder']
    report=json.loads((out/'native_ai_attract_runtime.json').read_text())
    audio_probe=json.loads((out/'native_attract_audio_finite.json').read_text())
    need(report['nativeTerminal']==c['terminal'] and report['passed'] and
         report['originalSonyaFailureNativeDispatchRepaired'] and report['completeNativeAttractCycleAccepted'],
         'Actual terminal native regression passed; no aborted or narrower attempt substituted')
    required={'bio_17_delay_180','bio_18_delay_180','demo_1_17_delay_90','demo_1_18_delay_90'}
    need(set(reviewed_stages)==required,'All four original new biography/demo screens actually reviewed')
    reviewed=[]
    for stage in reviewed_stages:
        rows=[r for r in c['rgbFrames'] if r['header']['stage']==stage]
        need(len(rows)==1,'One exact full native reviewed raster per stage')
        row=rows[0]
        need(hashlib.sha256(row['pixels']).hexdigest().upper()==row['header']['sha256'],'Original native image unchanged')
        reviewed.append(row['header'])
    build=ROOT/current.NAME
    meta=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'Temporary build cache actually absent')
    sources={}
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            path=Path(file).resolve();sources[str(path)]=dict(sha256=sha(path),text=path.read_text())
    need(not (out/'verified_progress.json').exists() and not (out/'executed_qualification_sources.json.gz').exists(),'Fresh immutable attempt receipts')
    with gzip.open(out/'executed_qualification_sources.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f)
    # Preserve the actual failed waveform comparison, not just its first eight
    # differences. One compressed 2.5MiB logical PCM carrier avoids a new
    # emulator replay merely to retrieve these same original speaker bytes.
    pcm_path=out/'captured_native_audio.pcm.gz'
    need(not pcm_path.exists(),'Fresh original compressed audio evidence')
    digest=hashlib.sha256()
    with gzip.open(pcm_path,'wb') as f:
        for row in c['pcm']:
            raw=row['pixels'];digest.update(raw);f.write(raw)
    need(digest.hexdigest().upper()==audio_probe['actualSHA256'],'Every actual PCM byte retained in original callback order')
    with gzip.open(pcm_path,'rb') as f:
        need(hashlib.sha256(f.read()).hexdigest().upper()==audio_probe['actualSHA256'],'Lossless original PCM evidence, no inferred audio or missing samples')
    receipt=dict(goalStatus='active',fullPortAcceptance=False,publicBuildPromoted=False,
        previousGoalTurnClassification='no progress: user acknowledgement only; staged checker and build revalidated next turn',
        thisGoalTurnClassification='progress: actual Sonya illegal callback diagnosed; seven true-ID native AI tables compiled and entire initialized guest checked; complete natural attract roster and health-changing new CPU combat verified',
        candidate=current.NAME,executableSHA256=meta['executable_sha256'],guestSHA256=meta['expected_guest_sha256'],
        nativeTerminal=c['terminal'],nativeCompilerExit=0,preexistingFilesRestored=True,compilerCacheAbsent=True,
        nativeAttractRuntime=report,viewedFullNativeScreens=reviewed,
        visualObservations=['Both biographies use their own photos, correct names and native story layout.',
            'Both new P1 demos display the real character bodies and matching lifebar names; full natural frame ledger proves combat advances and scheduler continues beyond the old Sonya/Kitana error.'],
        allAttractAudioAccepted=False,combinedFinalRegressionAccepted=False,
        actualAttractAudioProbe=audio_probe,compressedOriginalAudioEvidence=str(pcm_path),
        originalRemainingScope=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining'],
        nextAction='The name-only exact PCM model did not match the whole natural attract mix. Preserve this failed comparison and actual compressed PCM; determine original DCS/mixer contributions and source clocks before changing audio code. Qualify scene-owned/muted/enabled attract audio and broader real-ID CPU/arena interactions, remaining campaign/finisher/selection/reset integration, matching public CMD and finished portable ZIP. Keep the complete official-character objective.',
        newBuilds=1,newROMCopies=0,newRawMedia=0,compressedNativeAudioEvidenceCopies=1,newZIPs=0)
    (out/'verified_progress.json').write_text(json.dumps(receipt,indent=2)+'\n')
    folders=[out,ROOT/'source_native_ai_response',ROOT/'audit_native_ai_response_source',
             ROOT/'audit_native_ai_response_checker_failure',ROOT/'audit_native_ai_response_checker_source_boundary_failure',
             ROOT/'audit_native_ai_response_checker_archive_failure']
    paths=[p for folder in folders for p in folder.rglob('*') if p.is_file()]
    paths.extend(p for p in build.rglob('*') if p.is_file() and 'roms' not in p.parts and 'samples' not in p.parts)
    paths.extend(ROOT/'tools'/n for n in ('qualify_native_ai_response.py','build_native_ai_response.ps1',
        'native_ai_response_context.py','capture_native_ai_response_attract.py','qualify_native_ai_response_attract.py',
        'qualify_native_ai_attract_audio.py','seal_native_ai_response_attract.py'))
    paths.append(ROOT/'mk2ks_native_ai_response_attract.lua')
    storage=[]
    for path in paths:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(),'Explicit safe in-workspace evidence file')
        digest=sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],check=True,capture_output=True)
        need(sha(path)==digest,'Lossless compression preserves every actual executed byte')
        storage.append(dict(path=str(path),sha256=digest,allocatedBytes=allocated(path)))
    (out/'storage_receipt.json').write_text(json.dumps(dict(passed=True,compilerCacheAbsent=True,
        newExecutableAllocatedBytes=allocated(build/'mkport_candidate.exe'),exactFiles=storage,newROMCopies=0,newRawMedia=0,newZIPs=0),indent=2)+'\n')
    print(json.dumps(dict(attractCycleAccepted=True,sonyaDemoErrorFixed=True,realCPUCombat=report['actualLiveCPUCombat'],
        newExecutableAllocatedBytes=allocated(build/'mkport_candidate.exe'),fullPortAcceptance=False)),flush=True)
    return receipt
