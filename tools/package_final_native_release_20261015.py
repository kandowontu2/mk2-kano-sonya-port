"""Prepare local integration-release archive; final portable/root decision is separate."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
import verify_native_source_sync as sync

R=sync.ROOT
SEED=R/'release_current_native_playtest_20261015_updated_docs/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261015_updated_docs.zip'
SEEDHASH='2F4A961BD6C41199E312E5B731A32B64DEF05C05E259ABAC7B6A1373B4321FF0'
AUDIT=R/'audit_root_prepackage_acceptance_20261015/report.json'
AUDITHASH='36011407F0EFF909437795AD0ACE8D6A9C7DA8FA7B09342CF639A58A0B5C0083'
OUT=R/'release_mk2_kano_sonya_20261015'
PREFIX='MK2_Kano_Sonya_Playtest/'
CHECKER='tools/check_current_native_playtest.ps1'
OLD_CHECK_MESSAGE=b'Work-in-progress: full campaign, visual/audio and release acceptance remain unfinished.'
NEW_CHECK_MESSAGE=b'File checks passed. Release acceptance is documented separately in RELEASE.json.'
def digest(f):
    h=hashlib.sha256()
    while block:=f.read(1024*1024):h.update(block)
    return h.hexdigest().upper()
def current_path(name):
    if name=='PLAY.cmd':return R/'PLAY_CURRENT_NATIVE_CHECKED.cmd'
    if name=='COPYING':return R/'mame-mkp/COPYING'
    if name.startswith('source/'):return R/'mame-mkp'/name.removeprefix('source/')
    p=R/name
    if not p.exists() and name.startswith(sync.BUILD.name+'/samples/'):
        p=R/name.removeprefix(sync.BUILD.name+'/')
    return p
def main():
    assert not OUT.exists(),'Never overwrite a release'
    sync.verify();assert sync.sha(SEED)==SEEDHASH and sync.sha(AUDIT)==AUDITHASH
    audit=json.loads(AUDIT.read_text())
    assert audit['originalScopePreserved'] and audit['originalRequirementCount']==14
    assert len(audit['requirements'])==14 and audit['featureRequirementsAccepted']==12 and audit['storageAccepted']
    assert audit['requirements']['cmd_release']['classification']=='pending_final_package'
    assert sum(v['classification']=='accepted' for v in audit['requirements'].values())==13
    assert not audit['fullGoalComplete'] and not audit['finalPackageAccepted']
    for name,wanted in audit['inputHashes'].items():assert sync.sha(R/name)==wanted
    readme=(R/'audit_final_release_preparation_20261015/README_DRAFT.txt').read_text()
    banner=('RELEASE ACCEPTANCE PENDING. This is a preparation draft, not a release claim.\n'
            'Remove this line only after the root fourteen-requirement acceptance audit\n'
            'and final packaged portable verification both pass.\n\n')
    assert readme.count(banner)==1
    readme=readme.replace(banner,'')
    readme=readme.replace('package RELEASE.json records the release decision and its evidence digest.',
                          'package RELEASE.json records accepted integration features and the remaining\nportable/root release decision. The external final audit is authoritative.')
    with zipfile.ZipFile(SEED) as seed:
        names=seed.namelist();assert len(names)==len(set(names))==86
        prior=json.loads(seed.read(PREFIX+'RELEASE.json'));hashes=prior['files']
        assert len(hashes)==85
        assert set(names)=={PREFIX+k for k in hashes}|{PREFIX+'RELEASE.json'}
        pins={}
        for name,wanted in hashes.items():
            assert '..' not in Path(name).parts and ':' not in name and '\\' not in name
            with seed.open(PREFIX+name) as f:assert digest(f)==wanted
            if name in ('README.txt','MK2_KANO_SONYA_MOVES.txt'):continue
            if name==CHECKER:
                original=seed.read(PREFIX+name)
                checker=(R/CHECKER).read_bytes()
                assert original.count(OLD_CHECK_MESSAGE)==1
                assert original.replace(OLD_CHECK_MESSAGE,NEW_CHECK_MESSAGE)==checker
                pins[str(R/CHECKER)]=hashlib.sha256(checker).hexdigest().upper()
                continue
            p=current_path(name);assert p.is_file() and sync.sha(p)==wanted,(name,str(p))
            pins[str(p)]=wanted
        assert len(pins)==83
        guide=seed.read(PREFIX+'MK2_KANO_SONYA_MOVES.txt').decode()
        assert guide.count('MK2 Kano / Sonya - current native playtest move reference')==1
        assert guide.count('This is an unfinished playtest, not a final release.')==1
        guide=guide.replace('MK2 Kano / Sonya - current native playtest move reference','MK2 Kano / Sonya - native character move reference')
        guide=guide.replace('This is an unfinished playtest, not a final release.','See RELEASE.json for the integration evidence and release-verification status.')
        docs={'README.txt':readme.encode(),'MK2_KANO_SONYA_MOVES.txt':guide.encode(),CHECKER:checker}
        updated=dict(hashes)
        updated.update({n:hashlib.sha256(v).hexdigest().upper() for n,v in docs.items()})
        manifest=dict(build=sync.BUILD.name,files=updated,releaseStatus='NATIVE_INTEGRATION_RELEASE',
                      integrationFeaturesAccepted=True,featureRequirementsAccepted=12,storageAccepted=True,
                      finalPortableCheck='PENDING POST-PACKAGE CHECK',finalRootReleaseDecision='PENDING EXTERNAL ROOT AUDIT',
                      originalRequirementCount=14,requirements=audit['requirements'],
                      prepackageAuditSHA256=AUDITHASH,prepackageEvidenceHashes=audit['inputHashes'],
                      previousDocumentationPlaytestSHA256=SEEDHASH,samePlayableBuild=True,
                      acceptanceScope='Finite requested behavior and explicit source-bound retained component evidence; not universal all-RNG/input histories, four fresh current campaign wins or subjective speaker/mix judgment.',
                      compileCheckpoint=dict(buildInfoUnmodified=True,
                          historicalFullPortAcceptedFalse='Unmodified build-info.json describes its earlier compile checkpoint, not the later integration audit.'),
                      finalAcceptanceAuthority='Separate root final audit after this archive passes member integrity and extracted PLAY.cmd --check. This package does not preclaim that post-package result.')
        OUT.mkdir();archive=OUT/'MK2_Kano_Sonya_20261015.zip'
        with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as new:
            for entry in seed.infolist():
                leaf=entry.filename.removeprefix(PREFIX)
                if leaf in (*docs,'RELEASE.json'):continue
                with seed.open(entry) as reader,new.open(entry,'w') as writer:
                    shutil.copyfileobj(reader,writer,1024*1024)
            for name,data in docs.items():new.writestr(PREFIX+name,data)
            new.writestr(PREFIX+'RELEASE.json',json.dumps(manifest,indent=2).encode())
    with zipfile.ZipFile(archive) as new:
        assert len(new.namelist())==len(set(new.namelist()))==86 and new.testzip() is None
        assert len([n for n in new.namelist() if n.endswith('.wav')])==23
        assert len([n for n in new.namelist() if '/source/' in n])==15
        for name,wanted in updated.items():
            with new.open(PREFIX+name) as f:assert digest(f)==wanted
        assert json.loads(new.read(PREFIX+'RELEASE.json'))==manifest
    assert sync.sha(SEED)==SEEDHASH and sync.sha(AUDIT)==AUDITHASH
    assert all(sync.sha(Path(p))==wanted for p,wanted in pins.items())
    sync.verify()
    report=dict(passedArchiveIntegrity=True,zip=str(archive),zipBytes=archive.stat().st_size,
                zipSHA256=sync.sha(archive),members=86,files=85,soundAssets=23,
                unchangedPlayableAndSourceMemberCount=82,oldDocumentationPlaytestUnchanged=True,
                changedMembers=['README.txt','MK2_KANO_SONYA_MOVES.txt',CHECKER,'RELEASE.json'],
                checkerDiagnosticTextOnlyChanged=True,checkerHashAndROMLogicUnchanged=True,
                prepackageAuditSHA256=AUDITHASH,integrationFeaturesAccepted=True,
                finalPortableCheckPending=True,finalRootReleaseDecisionPending=True,
                fullGoalCompletionClaimed=False,newBuilds=0,stagingTrees=0,sourceGameFilesChanged=False)
    (OUT/'package-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
