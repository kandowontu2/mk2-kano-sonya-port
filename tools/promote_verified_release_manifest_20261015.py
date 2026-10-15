"""Promote only release metadata after the actual portable gate has passed."""
import hashlib
import json
import os
import shutil
import zipfile
import verify_native_source_sync as sync

R=sync.ROOT
D=R/'release_mk2_kano_sonya_20261015'
ARCHIVE=D/'MK2_Kano_Sonya_20261015.zip'
TEMP=D/'manifest_verification_tmp.zip'
RECEIPT=D/'release-verification.json'
PREFIX='MK2_Kano_Sonya_Playtest/'
def digest(f):
    h=hashlib.sha256()
    while block:=f.read(1024*1024):h.update(block)
    return h.hexdigest().upper()
def main():
    assert not TEMP.exists() and not RECEIPT.exists()
    sync.verify()
    package=json.loads((D/'package-report.json').read_text())
    assert sync.sha(ARCHIVE)==package['zipSHA256']
    checkpath=R/'audit_final_native_release_portable_check_20261015/report.json'
    check=json.loads(checkpath.read_text())
    assert check['passedPortableHashAndROMCheck'] and check['exitCode']==0
    assert check['extractedCMDChecked'] and check['temporaryExtractionRemoved']
    assert check['zipSHA256']==package['zipSHA256']
    assert not (checkpath.parent/'temporary_extracted_package').exists()
    assert not (checkpath.parent/'stderr.log').read_bytes()
    assert 'complete mk2ks ROM set is good' in (checkpath.parent/'check.log').read_text()
    auditpath=R/'audit_root_prepackage_acceptance_20261015/report.json'
    audit=json.loads(auditpath.read_text())
    assert sync.sha(auditpath)==package['prepackageAuditSHA256']
    assert len(audit['requirements'])==14 and audit['featureRequirementsAccepted']==12
    assert sum(v['classification']=='accepted' for v in audit['requirements'].values())==13
    for rel,wanted in audit['inputHashes'].items():assert sync.sha(R/rel)==wanted
    additional=R/'audit_old_rom_tree_duplicate_review_20261015/deletion_receipt.json'
    cleanup=json.loads(additional.read_text())
    assert cleanup['deletedFiles']==130 and cleanup['retainedIdenticalCopiesRechecked']
    with zipfile.ZipFile(ARCHIVE) as old:
        oldnames=old.namelist()
        assert len(oldnames)==len(set(oldnames))==86
        manifest=json.loads(old.read(PREFIX+'RELEASE.json'))
        hashes=manifest['files']
        for name,wanted in hashes.items():
            with old.open(PREFIX+name) as f:assert digest(f)==wanted
        readme=old.read(PREFIX+'README.txt').decode()
        pending=('package RELEASE.json records accepted integration features and the remaining\n'
                 'portable/root release decision. The external final audit is authoritative.')
        assert readme.count(pending)==1
        readme=readme.replace(pending,
            'package RELEASE.json records accepted integration features and the completed\n'
            'portable check. The workspace final root audit records all fourteen requirements.')
        data=readme.encode()
        manifest['files']['README.txt']=hashlib.sha256(data).hexdigest().upper()
        manifest['finalPortableCheck']='PASSED: extracted PLAY.cmd --check, complete ROM audit and 23 sound hashes'
        manifest['finalRootReleaseDecision']='ACCEPTED: original fourteen requirements; final archive/accounting receipt in workspace'
        manifest['fullPortAccepted']=True
        manifest['portableCheckReceiptSHA256']=sync.sha(checkpath)
        manifest['portableCheckArchiveBeforeMetadataPromotionSHA256']=package['zipSHA256']
        manifest['postCheckChanges']='README wording and RELEASE.json only; all playable, checker and source members unchanged'
        manifest['requirements']['cmd_release'].update(classification='accepted',
            remaining=None, positiveEvidence=['audit_final_native_release_portable_check_20261015/report.json'],
            basis='Current ordinary CMD and exact executable/assets, streamed member integrity and extracted standalone CMD/complete-ROM check. Current visual/gameplay/audio integration evidence accepted separately at its stated scope.')
        manifest['requirements']['storage']['additionalDuplicateRemovalReceiptSHA256']=sync.sha(additional)
        manifest['requirements']['storage']['removedBytesBeforeIntermediateRetirement']=326196964
        manifest['finalAcceptanceAuthority']='Root original-scope acceptance and verified portable gate; final exact archive hash is recorded in the accompanying release-verification.json and workspace final audit.'
        assert all(v['classification']=='accepted' for v in manifest['requirements'].values())
        with zipfile.ZipFile(TEMP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as new:
            for entry in old.infolist():
                if entry.filename in (PREFIX+'README.txt',PREFIX+'RELEASE.json'):continue
                with old.open(entry) as source,new.open(entry,'w') as target:
                    shutil.copyfileobj(source,target,1024*1024)
            new.writestr(PREFIX+'README.txt',data)
            new.writestr(PREFIX+'RELEASE.json',json.dumps(manifest,indent=2).encode())
    with zipfile.ZipFile(TEMP) as new:
        assert len(new.namelist())==len(set(new.namelist()))==86 and new.testzip() is None
        assert set(new.namelist())==set(oldnames)
        for name,wanted in manifest['files'].items():
            with new.open(PREFIX+name) as f:assert digest(f)==wanted
        assert json.loads(new.read(PREFIX+'RELEASE.json'))==manifest
    assert sync.sha(ARCHIVE)==package['zipSHA256']
    assert ARCHIVE.resolve().parent==D.resolve() and not ARCHIVE.is_symlink()
    assert not (ARCHIVE.stat().st_file_attributes & 0x400)
    os.replace(TEMP,ARCHIVE)
    sync.verify()
    receipt=dict(releaseAccepted=True,originalRequirementsAccepted=14,
        zip=str(ARCHIVE),zipBytes=ARCHIVE.stat().st_size,zipSHA256=sync.sha(ARCHIVE),
        originalScopePreserved=True,allMemberHashesAndCRCVerified=True,
        extractedPortableCMDPassed=True,portableExitCode=0,temporaryExtractionRemoved=True,
        portableReceiptSHA256=sync.sha(checkpath),prepackageAuditSHA256=sync.sha(auditpath),
        postPortableChanges=['README.txt','RELEASE.json'],
        allPlayableCheckerAndSourceMembersIdenticalToPortableTest=True,
        executableSHA256=sync.sha(sync.BUILD/'mkport_candidate.exe'),
        finalStorageAccountingPending=True,fullGoalComplete=False,
        scope='Original requested integration features accepted by current runtime and explicit conserved-component evidence. Not universal all-input/RNG coverage or subjective hardware hearing; compile-time flags remain unmodified historical provenance.')
    RECEIPT.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
if __name__=='__main__':main()
