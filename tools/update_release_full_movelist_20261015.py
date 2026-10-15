"""Documentation-only release update, with bounded streaming and exact verification."""
import hashlib
import json
import os
import shutil
import zipfile
import verify_native_source_sync as sync

R=sync.ROOT
D=R/'release_mk2_kano_sonya_20261015'
ARCHIVE=D/'MK2_Kano_Sonya_20261015.zip'
TEMP=D/'full_movelist_update.tmp.zip'
RECEIPT=D/'FULL_MOVELIST_UPDATE.json'
PREFIX='MK2_Kano_Sonya_Playtest/'
OLD_SHA='75442F99F22B210DF73C3D71F7C8E3D113DDB0B5ED3DEA1269FBA9FC6D0AE22B'
NAME='MK2_KANO_SONYA_MOVES.txt'
def digest(f):
    h=hashlib.sha256()
    while block:=f.read(1024*1024):h.update(block)
    return h.hexdigest().upper()
def main():
    assert not TEMP.exists() and not RECEIPT.exists()
    assert sync.sha(ARCHIVE)==OLD_SHA
    sync.verify()
    guide=(R/NAME).read_bytes()
    for section in (b'KANO - FINISHERS',b'SONYA - FINISHERS',b'SHANG TSUNG - ADDED MORPHS'):
        assert section in guide
    with zipfile.ZipFile(ARCHIVE) as old:
        names=old.namelist();assert len(names)==len(set(names))==86
        manifest=json.loads(old.read(PREFIX+'RELEASE.json'))
        before=dict(manifest['files'])
        for name,wanted in before.items():
            with old.open(PREFIX+name) as f:assert digest(f)==wanted
        manifest['files'][NAME]=hashlib.sha256(guide).hexdigest().upper()
        manifest['fullMoveListIncluded']=True
        manifest['documentationRevision']='2026-10-15 full finishers and Shang morphs'
        manifest['documentationOnlyPredecessorZIP_SHA256']=OLD_SHA
        with zipfile.ZipFile(TEMP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as new:
            for entry in old.infolist():
                if entry.filename in (PREFIX+NAME,PREFIX+'RELEASE.json'):continue
                with old.open(entry) as source,new.open(entry,'w') as target:
                    shutil.copyfileobj(source,target,1024*1024)
            new.writestr(PREFIX+NAME,guide)
            new.writestr(PREFIX+'RELEASE.json',json.dumps(manifest,indent=2).encode())
    with zipfile.ZipFile(TEMP) as new:
        assert new.namelist() and set(new.namelist())==set(names) and len(new.namelist())==86
        assert new.testzip() is None
        assert new.read(PREFIX+NAME)==guide
        for name,wanted in manifest['files'].items():
            with new.open(PREFIX+name) as f:assert digest(f)==wanted
            if name!=NAME:assert wanted==before[name]
        assert json.loads(new.read(PREFIX+'RELEASE.json'))==manifest
    assert sync.sha(ARCHIVE)==OLD_SHA
    assert not ARCHIVE.is_symlink() and not (ARCHIVE.stat().st_file_attributes & 0x400)
    assert ARCHIVE.resolve().parent==D.resolve()
    os.replace(TEMP,ARCHIVE)
    sync.verify()
    result=dict(documentationOnlyUpdatePassed=True,zip=str(ARCHIVE),zipSHA256=sync.sha(ARCHIVE),
        zipBytes=ARCHIVE.stat().st_size,previousZIP_SHA256=OLD_SHA,fullMoveList=NAME,
        moveListSHA256=manifest['files'][NAME],changedMembers=[NAME,'RELEASE.json'],
        unchangedOtherFileCount=len(before)-1,allMemberHashesAndCRCVerified=True,
        executableAssetsSourcesAndLauncherUnchanged=True,temporaryArchiveRemoved=not TEMP.exists(),
        priorIntegrationAcceptanceRetained=True,
        historicalReceiptPolicy='Earlier exact-archive receipts retain their predecessor hash; this receipt supersedes only the deliverable hash and movelist member. No gameplay change or new gameplay acceptance claim.')
    RECEIPT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
