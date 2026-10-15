"""Stream a documentation-only private playtest successor; no extracted staging."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
import verify_native_source_sync as sync

R=sync.ROOT
PREP=R/'audit_updated_playtest_package_preparation_20261015'
OLD=R/'release_current_native_playtest_20261013_complete_roms/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip'
OUT=R/'release_current_native_playtest_20261015_updated_docs'
PREFIX='MK2_Kano_Sonya_Playtest/'
DOCS={'README.txt':('55CEF891E921B65F06A04ED0D9CC718A1C719487E0030096F79E3F844D6522A9'),
      'MK2_KANO_SONYA_MOVES.txt':('F6210647B00101FE11106DF6BE00AEE759418475B66B73252291979AC0F24CE5')}
OLDHASH='EDAC17A71DC7353ABC35C32D914E8248DB7804DCA6F9AA3A24B9B25EDF2797B7'
def digest(stream):
    h=hashlib.sha256()
    while chunk:=stream.read(1024*1024):h.update(chunk)
    return h.hexdigest().upper()
def current_path(name):
    if name=='PLAY.cmd':return R/'PLAY_CURRENT_NATIVE_CHECKED.cmd'
    if name.startswith('source/'):return R/'mame-mkp'/name.removeprefix('source/')
    p=R/name
    if not p.exists() and name.startswith(sync.BUILD.name+'/samples/'):
        p=R/name.removeprefix(sync.BUILD.name+'/')
    return p
def main():
    assert not OUT.exists(),'Never overwrite package'
    sync.verify();assert sync.sha(OLD)==OLDHASH
    for name,wanted in DOCS.items():assert sync.sha(PREP/name)==wanted
    with zipfile.ZipFile(OLD) as seed:
        names=seed.namelist();assert len(names)==len(set(names))==85
        assert all(n.startswith(PREFIX) and '..' not in Path(n).parts and '\\' not in n for n in names)
        prior=json.loads(seed.read(PREFIX+'RELEASE.json'));hashes=prior['files']
        assert set(names)=={PREFIX+k for k in hashes}|{PREFIX+'RELEASE.json'}
        assert len(hashes)==84 and len([k for k in hashes if k.endswith('.wav')])==23
        sourcepins={}
        for name,wanted in hashes.items():
            with seed.open(PREFIX+name) as f:assert digest(f)==wanted
            if name=='README.txt':continue
            p=current_path(name);assert p.is_file() and sync.sha(p)==wanted,(name,str(p))
            sourcepins[str(p)]=wanted
        updated=dict(hashes);updated.update(DOCS)
        manifest=dict(prior,files=updated,releaseStatus='UNFINISHED CURRENT PLAYTEST',
                      fullPortAccepted=False,documentationUpdated='2026-10-15',
                      samePlayableBuild=True,previousPackageSHA256=OLDHASH)
        OUT.mkdir()
        archive=OUT/'MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261015_updated_docs.zip'
        with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as new:
            for entry in seed.infolist():
                name=entry.filename.removeprefix(PREFIX)
                if name in ('README.txt','RELEASE.json'):continue
                with seed.open(entry) as reader,new.open(entry,'w') as writer:
                    shutil.copyfileobj(reader,writer,1024*1024)
            for name in DOCS:new.write(PREP/name,PREFIX+name)
            new.writestr(PREFIX+'RELEASE.json',json.dumps(manifest,indent=2).encode())
    with zipfile.ZipFile(archive) as new:
        assert len(new.namelist())==len(set(new.namelist()))==86
        assert new.testzip() is None
        for name,wanted in updated.items():
            with new.open(PREFIX+name) as f:assert digest(f)==wanted
        assert json.loads(new.read(PREFIX+'RELEASE.json'))==manifest
        assert len([n for n in new.namelist() if '/source/' in n])==15
    assert sync.sha(OLD)==OLDHASH
    assert all(sync.sha(Path(p))==wanted for p,wanted in sourcepins.items())
    sync.verify()
    report=dict(passedArchiveIntegrity=True,zip=str(archive),zipBytes=archive.stat().st_size,
                zipSHA256=sync.sha(archive),members=86,files=85,soundAssets=23,
                oldZIPUnchanged=True,oldZIP=str(OLD),oldZIPHash=OLDHASH,
                unchangedPlayableAndSourceMemberCount=83,
                changedMembers=['README.txt','MK2_KANO_SONYA_MOVES.txt','RELEASE.json'],
                currentRuntimeAndSourcesRechecked=True,newBuilds=0,stagingTrees=0,
                sourceGameFilesChanged=False,portableRuntimeCheckPending=True,
                releaseStatus='UNFINISHED CURRENT PLAYTEST',fullPortAccepted=False)
    (OUT/'package-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
