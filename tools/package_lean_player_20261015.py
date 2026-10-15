"""Eleven-file player ZIP, exact current EXE, consolidated ROM/samples; no source tree."""
import hashlib
import io
import json
import shutil
import zipfile
from pathlib import Path

R=Path(__file__).resolve().parent.parent
PREP=R/'audit_lean_player_preparation_20261015'
OLD=R/'release_mk2_kano_sonya_20261015/MK2_Kano_Sonya_20261015.zip'
OLDHASH='4B8288D0CC1E94D476D60D87C0EF4DF5B5BB22A0BD123D4943330A2CD223B9B2'
OUT=R/'release_mk2_kano_sonya_20261015_player'
OP='MK2_Kano_Sonya_Playtest/'
NP='MK2_Kano_Sonya/'
EXEHASH='EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A'
PAYLOADHASH='A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'
BUILD='diagnostic_native_selector_layers_long'
def digest(f):
    h=hashlib.sha256()
    while block:=f.read(1024*1024):h.update(block)
    return h.hexdigest().upper()
def sha(p):
    with p.open('rb') as f:return digest(f)
def datahash(data):return hashlib.sha256(data).hexdigest().upper()
def emit(new,name,reader):
    with new.open(NP+name,'w') as writer:shutil.copyfileobj(reader,writer,1024*1024)
def main():
    assert not OUT.exists(),'Never overwrite player package'
    assert sha(OLD)==OLDHASH
    with zipfile.ZipFile(OLD) as old:
        prior=json.loads(old.read(OP+'RELEASE.json'));pins=prior['files']
        assert len(old.namelist())==86
        for name,wanted in pins.items():
            with old.open(OP+name) as f:assert digest(f)==wanted
        assert pins[BUILD+'/mkport_candidate.exe']==EXEHASH
        assert pins[BUILD+'/roms/mk2ks/mk2ks.mdata']==PAYLOADHASH
        assert old.getinfo(OP+'roms/mk2ks.zip').file_size<=32*1024**2
        # The seed contains stale inner UI/mdata. The complete loose ROM set
        # MUST supersede every matching inner member; canonical mdata last.
        inner_bytes=old.read(OP+'roms/mk2ks.zip')
        rom_sources={}
        with zipfile.ZipFile(io.BytesIO(inner_bytes)) as inner:
            for entry in inner.infolist():
                assert '/' not in entry.filename and '\\' not in entry.filename
                rom_sources[entry.filename]=('inner',entry.filename)
            for name in pins:
                if name.startswith('roms/mk2ks/'):
                    leaf=name.removeprefix('roms/mk2ks/')
                    assert '/' not in leaf
                    rom_sources[leaf]=('outer',name)
            rom_sources['mk2ks.mdata']=('outer',BUILD+'/roms/mk2ks/mk2ks.mdata')
            rom_buffer=io.BytesIO();rom_hashes={}
            with zipfile.ZipFile(rom_buffer,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as romzip:
                for leaf,(source,name) in sorted(rom_sources.items()):
                    context=inner.open(name) if source=='inner' else old.open(OP+name)
                    with context as reader,romzip.open(leaf,'w') as writer:
                        h=hashlib.sha256()
                        while block:=reader.read(1024*1024):h.update(block);writer.write(block)
                    rom_hashes[leaf]=h.hexdigest().upper()
            assert rom_buffer.tell()<=32*1024**2
        assert rom_hashes['mk2ks.mdata']==PAYLOADHASH
        ui_name=OP+'roms/mk2ks/mk2ks.ui'
        assert old.getinfo(ui_name).file_size==242495
        assert rom_hashes['mk2ks.ui']==pins['roms/mk2ks/mk2ks.ui']
        with zipfile.ZipFile(rom_buffer) as romzip:
            assert len(romzip.namelist())==len(set(romzip.namelist()))==len(rom_sources)
            assert romzip.testzip() is None
            for leaf,wanted in rom_hashes.items():
                with romzip.open(leaf) as reader:assert digest(reader)==wanted
        waves={n.rsplit('/',1)[-1]:n for n in pins if n.endswith('.wav')}
        assert len(waves)==23
        sample_buffer=io.BytesIO();sample_hashes={}
        with zipfile.ZipFile(sample_buffer,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as samples:
            for leaf,name in sorted(waves.items()):
                with old.open(OP+name) as reader,samples.open(leaf,'w') as writer:
                    shutil.copyfileobj(reader,writer,1024*1024)
                sample_hashes[leaf]=pins[name]
        assert sample_buffer.tell()<=16*1024**2
        with zipfile.ZipFile(sample_buffer) as samples:
            assert samples.testzip() is None and len(samples.namelist())==23
            for leaf,wanted in sample_hashes.items():
                with samples.open(leaf) as reader:assert digest(reader)==wanted
        guide=old.read(OP+'MK2_KANO_SONYA_MOVES.txt')
        assert b'Friendship' in guide and b'Babality' in guide and b'Shang' in guide
        loose={'PLAY.cmd':(PREP/'PLAY.cmd').read_bytes(),'CHECK.ps1':(PREP/'CHECK.ps1').read_bytes(),
               'README.txt':(PREP/'README.txt').read_bytes(),'MK2_KANO_SONYA_MOVES.txt':guide,
               'COPYING':old.read(OP+'COPYING'),'artwork/mk2ks/default.lay':old.read(OP+'artwork/mk2ks/default.lay')}
        assert b'width="4" height="3"' in loose['artwork/mk2ks/default.lay']
        player_hashes={k:datahash(v) for k,v in loose.items()}
        player_hashes['MK2_Kano_Sonya.exe']=EXEHASH
        player_hashes['roms/mk2.zip']=pins['roms/mk2.zip']
        for name,buffer in [('roms/mk2ks.zip',rom_buffer),('samples/mk2ks.zip',sample_buffer)]:
            buffer.seek(0);player_hashes[name]=digest(buffer);buffer.seek(0)
        assert len(player_hashes)==10
        files=dict(package='MK2 Kano/Sonya player',executableSHA256=EXEHASH,payloadSHA256=PAYLOADHASH,
                   soundAssets=23,files=player_hashes,romMembers=rom_hashes,sampleMembers=sample_hashes)
        OUT.mkdir();archive=OUT/'MK2_Kano_Sonya_20261015_PLAYER.zip'
        with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as new:
            for name,data in loose.items():new.writestr(NP+name,data)
            with old.open(OP+BUILD+'/mkport_candidate.exe') as f:emit(new,'MK2_Kano_Sonya.exe',f)
            with old.open(OP+'roms/mk2.zip') as f:emit(new,'roms/mk2.zip',f)
            emit(new,'roms/mk2ks.zip',rom_buffer);emit(new,'samples/mk2ks.zip',sample_buffer)
            new.writestr(NP+'FILES.json',json.dumps(files,indent=2).encode())
    with zipfile.ZipFile(archive) as new:
        assert len(new.namelist())==len(set(new.namelist()))==11 and new.testzip() is None
        assert not any('/source/' in n or 'build-info' in n or 'diagnostic_' in n for n in new.namelist())
        for name,wanted in player_hashes.items():
            with new.open(NP+name) as reader:assert digest(reader)==wanted
    assert sha(OLD)==OLDHASH
    report=dict(passedArchiveIntegrity=True,zip=str(archive),zipSHA256=sha(archive),zipBytes=archive.stat().st_size,
                files=11,executableSHA256=EXEHASH,payloadSHA256=PAYLOADHASH,soundAssets=23,
                sourceArchiveUnchanged=True,sourceArchiveSHA256=OLDHASH,romMembers=len(rom_sources),
                looseUIOverridesStaleInner=True,canonicalPayloadOverridesStaleInner=True,
                allROMAndSampleMemberHashesVerified=True,developerFilesIncluded=False,
                nativeROMSampleAuditPending=True,actualBootSampleLoadingPending=True,
                stagingTrees=0,newBuilds=0,currentWorkspaceRebuildInputsChanged=False)
    (OUT/'package-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
