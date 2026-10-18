"""Verify tested stock binary/notices against the official installer, streaming only."""
import hashlib
import json
from pathlib import Path
import subprocess
from inspect_normal_runtime import PORT
from refresh_special_videos import FLAGS

INSTALLER_SHA='A1AA7912168C9D1B05E611906BC21B8B9BE3935822AEAD36D12A1DA363150B7D'
EMULATOR_SHA='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
SOURCE_SHA='6243EAC3A80DF6BE602BF0AF7889305691737BC26C2DED1433EC11B7C6A3C7B9'
ROOT_FILES={'PATCH_MANIFEST.json','patch_native_roms.py','ips_codec.py','PATCH.cmd','PLAY.cmd',
            'MOVELIST_NATIVE.txt','README_PATCHING.txt'}


def player_member(name):
    parts=name.split('/')
    return name in ROOT_FILES or (len(parts)==2 and parts[0]=='patches' and
        parts[1] not in ('','.ips') and parts[1].endswith('.ips') and '\\' not in name and '..' not in parts)


def file_digest(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(65536),b''):digest.update(chunk)
    return digest.hexdigest().upper()


def main():
    mame=PORT.parents[1].parent/'mame0289'
    installer=mame/'mame0289b_x64.exe'
    assert file_digest(installer)==INSTALLER_SHA
    seven=Path('C:/Program Files/7-Zip/7z.exe');assert seven.is_file()
    members=['mame.exe','COPYING','uismall.bdf']+[
        'docs/legal/'+name for name in ('BSD-2-Clause','BSD-3-Clause','BSL-1.0','CC0','GPL-2.0','LGPL-2.1','MIT','Zlib')]
    records=[]
    for member in members:
        process=subprocess.Popen([str(seven),'x','-so','-bd','-mmt=1',str(installer),member.replace('/','\\')],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=FLAGS)
        digest=hashlib.sha256();size=0
        with process.stdout as stream:
            for chunk in iter(lambda:stream.read(65536),b''):
                digest.update(chunk);size+=len(chunk)
        error=process.stderr.read();assert process.wait(timeout=30)==0,error[-1000:]
        local=mame/member
        assert size==local.stat().st_size and digest.hexdigest().upper()==file_digest(local),member
        if member=='mame.exe':assert digest.hexdigest().upper()==EMULATOR_SHA
        records.append(dict(member=member,bytes=size,SHA256=digest.hexdigest().upper()))
        print('Verified official installer member',member,flush=True)
    package=PORT/'development_patches/MK2KS_NATIVE_DEVELOPMENT'
    manifest=json.loads((package/'FILES.json').read_text())
    player_files=sorted(name for name in manifest if player_member(name))
    assert len(player_files)==21 and sum(name.endswith('.ips') for name in player_files)==14
    source=mame/'mame0289s.exe'
    source_present=source.is_file()
    if source_present:assert file_digest(source)==SOURCE_SHA
    report=dict(scope='Unmodified stock MAME installer-member provenance and minimal player-file plan; not a release',
        officialMetadata='https://api.github.com/repos/mamedev/mame/releases/tags/mame0289',
        officialRelease='https://github.com/mamedev/mame/releases/tag/mame0289',
        installerSHA256=INSTALLER_SHA,emulatorSHA256=EMULATOR_SHA,verifiedMembers=records,
        playerPatchMembers=player_files,playerPatchUncompressedBytes=sum((package/name).stat().st_size for name in player_files),
        correspondingSourceAsset=dict(name='mame0289s.exe',bytes=159028505,SHA256=SOURCE_SHA,
            url='https://github.com/mamedev/mame/releases/download/mame0289/mame0289s.exe',
            presentAndHashVerified=source_present,plannedAsSeparateReleaseAsset=True),
        generatedGameROMsIncluded=False,testDumpsIncluded=False,emulatorDebugSymbolsIncluded=False,
        finalPlayerZIPBuilt=False,releaseApproved=False,
        openGates=['Earned Kano full campaign/video','Final audiovisual/release acceptance',
                   'Final release manifest/patcher validation','Corresponding emulator source asset and redistribution review'])
    (PORT/'STOCK_MAME_DISTRIBUTION_0289.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Verified stock binary/notices; planned21 patch/player files; no release ZIP or source download created.')


if __name__=='__main__':main()
