"""Verify the distributed ZIP itself, source diff application and runtime ROM provenance."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import sys
import zipfile

PORT=Path(__file__).resolve().parent
OUT=PORT/'development_patches'
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
PACKAGE=OUT/'MK2KS_NATIVE_DEVELOPMENT_IPS.zip'
PREFIX='MK2KS_NATIVE_DEVELOPMENT/'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
with zipfile.ZipFile(PACKAGE) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==len(set(archive.namelist()))
    assert all(n.startswith(PREFIX) and '..' not in Path(n).parts for n in archive.namelist())
    files={name[len(PREFIX):]:archive.read(name) for name in archive.namelist()}
pins=json.loads(files['FILES.json'])
assert set(files)==set(pins)|{'FILES.json'}
assert all(sha(files[name])==digest for name,digest in pins.items())
assert not any(Path(n).suffix.lower() in ('.exe','.dll','.rom','.bin','.zip') for n in files)
manifest=json.loads(files['PATCH_MANIFEST.json'])
assert not manifest['releaseReady'] and not manifest['fullPortVerified'] and not manifest['customDriver']
assert len(manifest['chips'])==26
assert sum(r['operation']=='ips' for r in manifest['chips'])==14
for name in ('ips_codec.py','patch_native_roms.py'):
    assert files[name]==(PORT/name).read_bytes()
modules=[name for name in files if name.startswith('source/asm/')]
expected_modules={p.name for p in BUILD.glob('*.ASM') if p.name.startswith(('KS','KANO','SONYA'))}
assert {Path(name).name for name in modules}==expected_modules
assert all(files[name]==(BUILD/Path(name).name).read_bytes() for name in modules)
patch=files['source/native_source.patch'].decode('latin-1')
names=re.findall(r'^--- a/src/([^\n]+)$',patch,re.M)
assert names and len(names)==len(set(names))
with tempfile.TemporaryDirectory(prefix='source-diff-check-',dir=OUT) as temporary:
    root=Path(temporary).resolve()
    assert root.is_relative_to(OUT.resolve())
    (root/'src').mkdir()
    with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as original:
        for name in names:
            assert Path(name).name==name
            text=original.read('mk2-rebuild-main/src/'+name).replace(b'\r\n',b'\n').rstrip(b'\n')+b'\n'
            (root/'src'/name).write_bytes(text)
    patch_path=root/'native_source.patch';patch_path.write_bytes(files['source/native_source.patch'])
    for check in (True,False):
        command=['git','apply','--whitespace=nowarn']+(['--check'] if check else [])+[str(patch_path)]
        process=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=30,
            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        assert process.returncode==0,process.stdout+process.stderr
    for name in names:
        actual=(root/'src'/name).read_bytes().replace(b'\r\n',b'\n').rstrip(b'\n')
        expected=(BUILD/name).read_bytes().replace(b'\r\n',b'\n').rstrip(b'\n')
        assert actual==expected,(name,len(actual),len(expected),next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),None))
runtime=[]
roundtrip=json.loads((OUT/'PACKAGING_VERIFICATION.json').read_text())
assert roundtrip['SHA256']==sha(PACKAGE.read_bytes())
assert len(sys.argv)>1,'Supply completed current runtime runs; historical fixed runs are not current proof'
for name in sys.argv[1:]:
    assert re.fullmatch(r'[A-Za-z0-9_-]+',name)
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    clap='--clap-victim' in receipt['testArguments']
    torso=any(flag in receipt['testArguments'] for flag in ('--torso-victim','--swipe-victim'))
    qualification='CLAP_RUNTIME_QUALIFICATION.json' if clap else ('TORSO_RUNTIME_QUALIFICATION.json' if torso else 'CAMPAIGN_AUDIT.json')
    assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']==manifest['testedEmulatorSHA256']
    assert receipt['replacementChips']=={r['target']:r['targetSHA256'] for r in manifest['chips']}
    assert receipt['controllerSHA256']==sha((folder/'autoboot.lua').read_bytes())
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        extras=set(archive.namelist())-set(receipt['replacementChips'])
        known_extras={'mk3p40/mk3p40.u54','mk3p40/mk3p40.u63',
                      'mk3r10/mk310u54.bin','mk3r10/mk310u63.bin',
                      'mk3r20/mk320u54.bin','mk3r20/mk320u63.bin'}
        assert extras<=known_extras
        with zipfile.ZipFile(PORT.parents[1]/'mk3.zip') as original:
            assert all(archive.read(extra)==original.read(extra) for extra in extras)
        assert all(sha(archive.read(chip))==digest for chip,digest in receipt['replacementChips'].items())
    result=json.loads((folder/qualification).read_text())
    if clap:
        assert result['currentAll26ChipsVerified'] and len(result['naturalKOFrames'])==2
        assert result['ownBodyPoses']==7 and result['groundedBodyObservations']>=50
        assert result['postFinishTransitionObserved'] and result['nativeComplete']>result['nativeStart']
        assert result['evidenceSHA256']=={p:sha((folder/p).read_bytes()) for p in result['evidenceSHA256']}
    elif torso:
        assert result['qualified'] and result['currentFull26ROMBytesVerified']
        assert len(result['naturalKOFrames'])==2 and result['nativeCompletionObserved']
        assert result['lowerOpaqueFootPlacementAccepted'] and result['lowerOpaqueGroundDelta']==0
        assert result['freshCombatFields']==600 and result['freshIdentitiesAndResetVerified']
        assert result['freshHardwarePaletteColorComparisons']>0
        assert all(sha(Path(path).read_bytes())==digest for path,digest in result['pins'].items())
    else:
        assert result['currentFullROMVerified'] and not result['missingMarkers'] and not result['illegalOpcodeRecoveryObserved']
    runtime.append(dict(test=name,qualification=qualification,qualificationSHA256=sha((folder/qualification).read_bytes()),
        same26ChipBytesAsPatchedArchive=True,
        unchangedUnselectedCloneEntries=sorted(extras),
        exactPatchedArchiveContainer=receipt['archiveStorage']['archiveSHA256']==roundtrip['roundtrip']['SHA256']))
report=dict(package=str(PACKAGE),packageSHA256=sha(PACKAGE.read_bytes()),packageFileHashesVerified=True,
    noCompleteROMsOrEmulatorIncluded=True,sourceDiffAppliedAndMatchedCurrent=True,
    changedOriginalFiles=len(names),ownASMModulesMatched=len(modules),runtimeWithMatchingPatchedChipBytes=runtime,
    cleanRebuildVerified=False,releaseReady=False,fullPortVerified=False)
(OUT/'PACKAGE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
