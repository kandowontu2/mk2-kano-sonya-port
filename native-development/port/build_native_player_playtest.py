"""Minimal LOCAL playtest with unmodified MAME; never a final/public release."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile
from audit_stock_mame_distribution import main as audit_distribution, file_digest, player_member, EMULATOR_SHA
from inspect_normal_runtime import PORT
from refresh_special_videos import FLAGS

README='''MKII KANO / SONYA - UNFINISHED NATIVE PLAYTEST
Not a final/public release. Kano's full campaign and final audiovisual/release
acceptance remain open. Do not confuse this with the withdrawn driver hack.

This bundle includes UNMODIFIED stock MAME0.289, per-chip IPS patches, the
standard-library Python patcher, movelist and launch instructions. It contains
NO complete game ROMs, custom driver, test controller, samples or recordings.

1. Extract to a writable folder. Supply your own MKII and MK3 revision2.1
   archives with chip hashes/names matching PATCH_MANIFEST.json.
2. Install Python3.10+ if needed. From Command Prompt run:
     PATCH.cmd "C:\\path\\mk2.zip" "C:\\path\\mk3.zip"
   Existing output is never overwritten; original archives are not modified.
3. Double-click PLAY.cmd. The bundled mame.exe uses an isolated configuration.
   This is MKII game code on the existing mk3 Wolf hardware/socket definition,
   not MK3 gameplay. Patched-ROM checksum warnings are expected.
   For a basic Windows renderer fallback, from this folder run:
     mame.exe mk3 -rompath .\\roms -window -video gdi

MOVELIST_NATIVE.txt includes both characters, finishers and Shang morphs.
Readable59-module ASM and40-file original-source diff are in the SEPARATE
MK2KS_NATIVE_DEVELOPMENT_IPS.zip and public native-rom/source directory:
https://github.com/kandowontu2/mk2-kano-sonya-port/tree/main/native-rom/source
They are not duplicated inside this smaller player ZIP. Rebuilding requires
the original licensed/proprietary inputs described in that source guide.

MAME copyright/notices: COPYING and docs/legal. This is an unchanged official
binary, not a custom MAME build. Corresponding upstream source is the separate
mame0289s.exe asset, SHA256
6243EAC3A80DF6BE602BF0AF7889305691737BC26C2DED1433EC11B7C6A3C7B9
https://github.com/mamedev/mame/releases/tag/mame0289
Keep source/notices available as required before any redistribution. Final
redistribution review and a public GitHub release are NOT approved by creating
this local playtest. FILES.json records only this bundle's own members.
'''


def digest_stream(stream):
    digest=hashlib.sha256()
    for chunk in iter(lambda:stream.read(65536),b''):digest.update(chunk)
    return digest.hexdigest().upper()


def isolated_launcher(data):
    marker=b' mk3 -rompath '
    assert data.count(marker)==1, 'Unexpected launcher shape'
    assert b'-noreadconfig' not in data, 'Already transformed launcher'
    return data.replace(marker,b' mk3 -noreadconfig -rompath ')


def main():
    assert len(sys.argv)==1
    out=PORT/'development_patches'
    destination=out/'MK2KS_NATIVE_PLAYTEST_WITH_STOCK_MAME_V2.zip'
    partial=destination.with_suffix('.zip.partial')
    assert not destination.exists() and not partial.exists(),'Never overwrite a playtest or partial'
    assert shutil.disk_usage(out).free>1024**3,'Reserve1GiB working space'
    audit_distribution()
    proof=json.loads((PORT/'STOCK_MAME_DISTRIBUTION_0289.json').read_text())
    assert proof['correspondingSourceAsset']['presentAndHashVerified']
    package=out/'MK2KS_NATIVE_DEVELOPMENT_IPS.zip'
    qualification=json.loads((out/'PACKAGE_QUALIFICATION.json').read_text())
    assert file_digest(package)==qualification['packageSHA256']
    files={}
    with zipfile.ZipFile(package) as archive:
        prefix='MK2KS_NATIVE_DEVELOPMENT/'
        for entry in archive.infolist():
            assert entry.filename.startswith(prefix)
            name=entry.filename[len(prefix):]
            if player_member(name):files[name]=archive.read(entry)
    assert len(files)==21
    files['README_PATCHING.txt']=README.encode('ascii')
    files['PLAY.cmd']=isolated_launcher(files['PLAY.cmd'])
    mame=PORT.parents[1].parent/'mame0289'
    for member in proof['verifiedMembers']:files[member['member']]=mame/member['member']
    assert len(files)==32 and file_digest(files['mame.exe'])==EMULATOR_SHA
    pins={name:(file_digest(data) if isinstance(data,Path) else hashlib.sha256(data).hexdigest().upper())
          for name,data in sorted(files.items())}
    files['FILES.json']=(json.dumps(pins,indent=2)+'\n').encode()
    created=False
    try:
        with partial.open('xb') as output:
            created=True
            with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
                for name,data in sorted(files.items()):
                    info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                    with archive.open(info,'w') as target:
                        if isinstance(data,Path):
                            with data.open('rb') as source:shutil.copyfileobj(source,target,65536)
                        else:target.write(data)
        with zipfile.ZipFile(partial) as archive:
            assert set(archive.namelist())==set(files) and len(archive.infolist())==33
            for name,digest in pins.items():
                with archive.open(name) as stream:assert digest_stream(stream)==digest,name
            with tempfile.TemporaryDirectory(prefix='player-patch-check-',dir=out) as folder:
                work=Path(folder)
                for name in files:
                    if player_member(name):
                        target=work/name;target.parent.mkdir(parents=True,exist_ok=True)
                        target.write_bytes(archive.read(name))
                environment=os.environ.copy();environment.pop('PYTHONPATH',None)
                environment['PYTHONNOUSERSITE']='1';environment['PYTHONDONTWRITEBYTECODE']='1'
                root=PORT.parents[1];rom=work/'roms/mk3.zip'
                subprocess.run([sys.executable,str(work/'patch_native_roms.py'),'--mk2',str(root/'roms/mk2.zip'),
                    '--mk3',str(root/'mk3.zip'),'--output',str(rom)],cwd=work,env=environment,
                    capture_output=True,check=True,timeout=60,creationflags=FLAGS)
                assert file_digest(rom)==file_digest(out/'roundtrip/roms/mk3.zip')
        assert not work.exists(),'Temporary generated game ROM must be removed'
        os.link(partial,destination)
    finally:
        if created and partial.exists():partial.unlink()
    report=dict(scope='Minimal local native playtest ZIP, not final/public release',file=str(destination),
        bytes=destination.stat().st_size,SHA256=file_digest(destination),members=33,
        stockEmulatorSHA256=EMULATOR_SHA,allMemberHashesVerified=True,
        isolatedPatcherReproducedExactTestedROM=True,temporaryROMRemoved=True,
        completeGameROMsIncluded=False,sourceASMDuplicated=False,headlessGameplayRerun=False,
        interactiveRendererAcceptance=False,fullPortVerified=False,releaseApproved=False)
    (out/'PLAYER_PLAYTEST_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
