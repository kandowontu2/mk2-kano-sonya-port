"""Final original-scope audit, with direct final artifact and cleanup verification."""
import copy
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
import verify_native_source_sync as sync

R=sync.ROOT
OUT=R/'audit_root_final_acceptance_20261015'
RELEASE=R/'release_mk2_kano_sonya_20261015'
ARCHIVE=RELEASE/'MK2_Kano_Sonya_20261015.zip'
PREFIX='MK2_Kano_Sonya_Playtest/'
def digest(f):
    h=hashlib.sha256()
    while block:=f.read(1024*1024):h.update(block)
    return h.hexdigest().upper()
def main():
    assert not OUT.exists() and not (RELEASE/'FINAL_ACCEPTANCE.json').exists()
    sync.verify()
    pins={}
    def read(rel):
        p=R/rel;pins[rel]=sync.sha(p)
        return json.loads(p.read_text())
    original=read('audit_native_guard_campaign_progress/report.json')['originalNaturalIntegrationRequirements']
    pre=read('audit_root_prepackage_acceptance_20261015/report.json')
    assert pre['originalScopePreserved'] and set(pre['requirements'])==set(original) and len(original)==14
    assert sum(v['classification']=='accepted' for v in pre['requirements'].values())==13
    for rel,wanted in pre['inputHashes'].items():assert sync.sha(R/rel)==wanted
    verification=read('release_mk2_kano_sonya_20261015/release-verification.json')
    assert verification['releaseAccepted'] and verification['originalScopePreserved']
    assert verification['allPlayableCheckerAndSourceMembersIdenticalToPortableTest']
    assert sync.sha(ARCHIVE)==verification['zipSHA256']=='75442F99F22B210DF73C3D71F7C8E3D113DDB0B5ED3DEA1269FBA9FC6D0AE22B'
    portable=read('audit_final_native_release_portable_check_20261015/report.json')
    assert portable['passedPortableHashAndROMCheck'] and portable['extractedCMDChecked']
    assert portable['exitCode']==0 and portable['temporaryExtractionRemoved']
    assert not (R/'audit_final_native_release_portable_check_20261015/temporary_extracted_package').exists()
    assert not (R/'audit_final_native_release_portable_check_20261015/stderr.log').read_bytes()
    assert sync.sha(R/'audit_final_native_release_portable_check_20261015/report.json')==verification['portableReceiptSHA256']
    with zipfile.ZipFile(ARCHIVE) as z:
        names=z.namelist();assert len(names)==len(set(names))==86 and z.testzip() is None
        manifest=json.loads(z.read(PREFIX+'RELEASE.json'))
        assert manifest['fullPortAccepted'] and manifest['integrationFeaturesAccepted']
        assert manifest['finalPortableCheck'].startswith('PASSED:') and manifest['finalRootReleaseDecision'].startswith('ACCEPTED:')
        assert set(names)=={PREFIX+k for k in manifest['files']}|{PREFIX+'RELEASE.json'}
        assert len(manifest['files'])==85
        assert sum(n.endswith('.wav') for n in names)==23 and sum('/source/' in n for n in names)==15
        for name,wanted in manifest['files'].items():
            with z.open(PREFIX+name) as f:assert digest(f)==wanted
            if name in ('README.txt','MK2_KANO_SONYA_MOVES.txt'):continue
            if name=='PLAY.cmd':p=R/'PLAY_CURRENT_NATIVE_CHECKED.cmd'
            elif name=='COPYING':p=R/'mame-mkp/COPYING'
            elif name.startswith('source/'):p=R/'mame-mkp'/name.removeprefix('source/')
            else:
                p=R/name
                if not p.exists() and name.startswith(sync.BUILD.name+'/samples/'):
                    p=R/name.removeprefix(sync.BUILD.name+'/')
            assert p.is_file() and sync.sha(p)==wanted,(name,str(p))
        assert manifest['portableCheckReceiptSHA256']==verification['portableReceiptSHA256']
        assert portable['zipSHA256']==manifest['portableCheckArchiveBeforeMetadataPromotionSHA256']
        assert manifest['postCheckChanges'].startswith('README wording and RELEASE.json only')
        assert manifest['prepackageAuditSHA256']==pins['audit_root_prepackage_acceptance_20261015/report.json']
        for key,row in manifest['requirements'].items():
            assert row['originalRequirement']==original[key] and row['classification']=='accepted'
        play=z.read(PREFIX+'PLAY.cmd').decode()
        assert '-nocheat' in play and '-autoboot' not in play and 'python' not in play.lower()
        assert 'MK2KS_' in play and 'MK2_TRACE_' in play
        checker=z.read(PREFIX+'tools/check_current_native_playtest.ps1')
        with zipfile.ZipFile(R/'release_current_native_playtest_20261013_complete_roms/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip') as old:
            oldchecker=old.read(PREFIX+'tools/check_current_native_playtest.ps1')
        oldmessage=b'Work-in-progress: full campaign, visual/audio and release acceptance remain unfinished.'
        newmessage=b'File checks passed. Release acceptance is documented separately in RELEASE.json.'
        assert oldchecker.count(oldmessage)==1 and oldchecker.replace(oldmessage,newmessage)==checker
    removals=['audit_obsolete_capture_target_review_20261015/deletion_receipt.json',
              'audit_obsolete_combat_snapshot_review_20261015/deletion_receipt.json',
              'audit_old_rom_tree_duplicate_review_20261015/deletion_receipt.json']
    allocated_removed=51660627
    for rel in removals:
        d=read(rel);assert d['permanentDeletion'] and not d['archiveCreated']
        allocated_removed+=d['allocatedBytesFromCensus']
    assert allocated_removed==326196964
    romplan=read('audit_old_rom_tree_duplicate_review_20261015/deletion_plan.json')
    for row in romplan['targets']:
        assert not Path(row['path']).exists()
        assert sync.sha(Path(row['retainedIdenticalFile']))==row['SHA256']
    for row in romplan['preservedUnique'] if 'preservedUnique' in romplan else []:
        assert sync.sha(Path(row['path']))==row['SHA256']
    intermediary=R/'release_current_native_playtest_20261015_updated_docs/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261015_updated_docs.zip'
    assert not intermediary.exists()
    rel='release_current_native_playtest_20261015_updated_docs/retirement_receipt.txt'
    pins[rel]=sync.sha(R/rel)
    census=read('audit_final_release_storage_census_20261015/report.json')
    initial=read('audit_cleanup_candidate_census_20261015/report.json')
    assert census['complete'] and census['readOnly'] and census['files']<200000
    assert census['uniqueAllocatedBytes']<initial['uniqueAllocatedBytes']
    git=subprocess.run(['git','worktree','list','--porcelain'],cwd=R/'mame-mkp',capture_output=True,text=True,timeout=15,check=True)
    assert git.stdout.count('worktree ')==1
    games=list(R.rglob('mkport_candidate.exe'))
    assert games==[sync.BUILD/'mkport_candidate.exe']
    processes=subprocess.run(['powershell.exe','-NoProfile','-Command',"@(Get-Process -Name mkport_candidate -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True,timeout=15,check=True)
    assert processes.stdout.strip()=='0'
    sync.verify()
    decisions=copy.deepcopy(manifest['requirements'])
    decisions['storage'].update(finalCensus='audit_final_release_storage_census_20261015/report.json',
        finalAllocatedBytes=census['uniqueAllocatedBytes'],removedAllocatedBytesBeforeIntermediaryRetirement=allocated_removed,
        intermediaryRetired=True,oneGitWorktree=True,soleCurrentGameExecutable=True)
    report=dict(originalScopePreserved=True,originalRequirementCount=14,requirements=decisions,
        allFourteenRequirementsAccepted=True,fullGoalComplete=True,remainingRequiredWork=[],
        finalZIP=str(ARCHIVE),finalZIPSHA256=sync.sha(ARCHIVE),finalZIPBytes=ARCHIVE.stat().st_size,
        finalMemberHashesAndCRCVerified=True,extractedStandaloneCMDPassed=True,
        metadataOnlyAfterPortableTest=True,currentSourceAndExecutableSynchronized=True,
        noLiveGameProcess=True,temporaryExtractionRemoved=True,
        finalAllocatedBytes=census['uniqueAllocatedBytes'],finalLogicalBytes=census['logicalBytes'],
        measuredAllocationReductionThisPass=initial['uniqueAllocatedBytes']-census['uniqueAllocatedBytes'],
        supersedesPendingStorageAccountingInReleaseVerification=True,
        acceptanceScope='Full original requested integration features and local runnable deliverable. Positive finite runtime and exact relevant component conservation, not merely no observed bugs. No universal all-RNG/input histories or subjective hardware hearing claimed.',
        inputHashes=pins)
    text=json.dumps(report,indent=2)+'\n'
    OUT.mkdir();(OUT/'report.json').write_text(text)
    (RELEASE/'FINAL_ACCEPTANCE.json').write_text(text)
    print(json.dumps(dict(allFourteenRequirementsAccepted=True,fullGoalComplete=True,remainingRequiredWork=[],zipSHA256=report['finalZIPSHA256'],measuredAllocationReductionThisPass=report['measuredAllocationReductionThisPass'])))
if __name__=='__main__':main()
