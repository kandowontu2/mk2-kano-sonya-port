"""Keep all real audio results, failed models and source-exact native evidence."""
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

def seal(c):
    need(not native.census() and c['terminal']['nativeExit']==0 and c['guest']==current.expected(),
         'Same original native process terminal and entire compiled guest exact')
    out=c['folder']
    failed=json.loads((out/'native_attract_dcs_mix.json').read_text())
    passed=json.loads((out/'native_attract_dcs_mix_v2.json').read_text())
    faults=json.loads((out/'native_attract_audio_faults.json').read_text())
    need(not failed['passed'] and failed['differentChannelSamples']==92690 and passed['passed'] and
         passed['differentChannelSamples']==0 and faults['passed'] and len(faults['faultsRejected'])==11,
         'Real failed original checker, complete corrected PCM match and effective faults preserved')
    old=ROOT/'audit_native_ai_response_attract'
    previous=json.loads((old/'native_attract_audio_finite.json').read_text())
    need(passed['actualSHA256']==previous['actualSHA256'] and faults['wholePriorActualPCMUnchanged'],
         'Whole original speaker output unchanged; new source observations do not perturb it')
    need(not (out/'verified_progress.json').exists(),'Fresh immutable finite progress')
    data_path=out/'captured_native_dac.f32.gz'
    need(not data_path.exists(),'One new compact native DAC carrier, no duplicate PCM/media/ROM/build')
    with gzip.open(data_path,'wb') as f:
        for raw in c['dac']:f.write(raw)
    with gzip.open(data_path,'rb') as f:
        for raw,head in zip(c['dac'],c['dacHeaders']):
            need(f.read(len(raw))==raw and hashlib.sha256(raw).hexdigest().upper()==head['sha256'],'Every original float buffer archived exactly')
        need(not f.read(),'No extra or missing original native DAC bytes')
    sources={}
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            path=Path(file).resolve();sources[str(path)]=dict(sha256=sha(path),text=path.read_text())
    with gzip.open(out/'executed_qualification_sources.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f)
    receipt=dict(goalStatus='active',fullPortAcceptance=False,fullAttractAudioAccepted=False,
        publicBuildPromoted=False,previousGoalTurnClassification='progress: seven AI tables repaired and full native attract roster/combat verified; genuine name-only PCM discrepancy retained',
        thisGoalTurnClassification='progress: whole original retained PCM inspected; actual DCS output captured alongside all661 speaker callbacks; full native DCS/name float mix matches all634560 stereo frames exactly;11 effective corruption/source faults rejected and original PCM unchanged',
        nativeTerminal=c['terminal'],wholeGuestBytesCompared=1048576,finiteNativeAttractAudio=passed,
        failedFirstDCSMixPrediction=failed,actualFaults=faults,
        sourceObservations=['Original DCS contributes186471 nonzero serial samples in the captured native biography windows; that source was absent from the first names-only prediction.',
          'The first DCS-plus-name checker wrongly overwrote Kano with the future Sonya event zero segment. Its entire source and92690-sample failure are preserved; the corrected checker sums both original sources.',
          'The muted native Kano Ball and Sonya Square startup windows remain exactly silent. Full natural source-clock and native signed16 normalization checks include both silent windows.',
          'All634560 actual speaker frames match the earlier uninstrumented recording byte-for-byte. No game-audio or character code was changed.'],
        originalPCMReused=str(old/'captured_native_audio.pcm.gz'),newNativeDACCarrier=str(data_path),actualNativeDACHeaders=c['dacHeaders'],
        originalRemainingScope=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining'],
        nextAction='Inspect native enabled-demo sound setting and use normal settings/controller interaction to verify audible attract combat and scene-owned startup interruption/cleanup. Then broader true-ID CPU/arena interactions and remaining current campaign/finisher/UI/reset/morph integration, matching public CMD and finished portable ZIP. Preserve the full official-character objective.',
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,newCompressedDACProofCopies=1,newPCMProofCopies=0,
        compilerCacheAbsent=not (ROOT/'mame-mkp/build/mingw-gcc').exists())
    need(receipt['compilerCacheAbsent'],'No retained compiler cache')
    (out/'verified_progress.json').write_text(json.dumps(receipt,indent=2)+'\n')
    paths=[p for p in out.rglob('*') if p.is_file()]
    paths.extend(ROOT/'tools'/n for n in ('inspect_native_attract_audio_retained.py','capture_native_attract_dcs_audio.py',
       'qualify_native_attract_dcs_audio.py','qualify_native_attract_dcs_audio_v2.py','check_native_attract_dcs_audio_faults.py','seal_native_attract_dcs_audio.py'))
    paths.append(ROOT/'mk2ks_native_attract_dcs_audio.lua')
    storage=[]
    for path in paths:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(),'Explicit in-workspace original evidence file')
        digest=sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],check=True,capture_output=True)
        need(sha(path)==digest,'Every actual original evidence byte unchanged by compression')
        storage.append(dict(path=str(path),allocatedBytes=allocated(path),sha256=digest))
    (out/'storage_receipt.json').write_text(json.dumps(dict(passed=True,exactFiles=storage,newBuilds=0,newROMCopies=0,newZIPs=0,
         newCompressedDACProofCopies=1,newPCMProofCopies=0,compilerCacheAbsent=True),indent=2)+'\n')
    print(json.dumps(dict(finiteAudioAccepted=True,comparedStereoFrames=634560,effectiveFaults=11,originalPCMPerturbed=False,
        newEvidenceAllocatedBytes=sum(r['allocatedBytes'] for r in storage),fullPortAcceptance=False)),flush=True)
    return receipt
