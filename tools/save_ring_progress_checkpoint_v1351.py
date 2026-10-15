"""Fresh incremental checkpoint; binds, but does not rehash all historical pins."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1351_native_ring_progress_checkpoint'

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb')as stream:
        for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest().upper()

def verify():
    pins={};reports={}
    def pin(path,wanted=None):
        path=Path(path);key=str(path);actual=pins.get(key)or digest(path)
        assert wanted is None or wanted==actual,'Changed evidence '+key;pins[key]=actual
    def report(name,candidate=None):
        path=ROOT/name/'report.json';value=json.loads(path.read_text(encoding='utf-8-sig'));assert value['passed'];pin(path)
        if candidate is not None:assert value['candidate']==candidate
        for file,wanted in value.get('inputHashes',{}).items():pin(file,wanted)
        reports[name]=dict(passed=True,candidate=value.get('candidate'),reportSHA256=digest(path))
        return value
    old_path=ROOT/'audit_v1279_current_presentation_checkpoint/checkpoint.json'
    old=json.loads(old_path.read_text());assert len(old['inputHashes'])==67162 and old['fullPortAccepted']is False
    pin(old_path)
    for move in('knife','ring'):
        for side in(1,2):
            report(f'audit_v1293_projectile_{move}_p{side}_render_checked','diagnostic_v1250_native_correct_rom_metadata')
            for scenario in('block','miss'):report(f'audit_v1297_projectile_{move}_{scenario}_p{side}_render_checked','diagnostic_v1250_native_correct_rom_metadata')
    report('audit_v1298_projectile_native_library_checked','diagnostic_v1250_native_correct_rom_metadata')
    counter=report('audit_v1301_projectile_lifetime_counterexamples','diagnostic_v1250_native_correct_rom_metadata');assert counter['count']==20
    report('audit_v1310_native_ring_glow_source_checked','diagnostic_v1306_native_sonya_ring_glow')
    for side in(1,2):
        report(f'audit_v1311_projectile_ring_p{side}_render_checked','diagnostic_v1306_native_sonya_ring_glow')
        for scenario in('block','miss'):report(f'audit_v1312_projectile_ring_{scenario}_p{side}_render_checked','diagnostic_v1306_native_sonya_ring_glow')
    candidate='diagnostic_v1340_native_ring_lookup'
    source=report('audit_v1342_native_ring_lookup_checked',candidate)
    assert source['wholeGuestIndependentlyReconstructed']and source['nativeROMAuditAccepted']and source['canonicalHistoricalSourceRestored']
    scopes={}
    for side in(1,2):
        data=report(f'audit_v1346_ring_interrupt_p{side}_render_checked',candidate)
        assert data['interruptedReleaseRestorationAccepted']and data['normalAndAlternateMirrorRestorationAccepted']and data['sourceCorrectCloseContactBeforeTravelAccepted']
        assert data['replayed']['frames']==334 and data['state']['fields']==1082
        scopes[str(side)]=dict(fields=data['state']['fields'],replayedFrames=data['replayed']['frames'],projectilePaletteSamples=data['fullProjectilePaletteSamples'],zeroChargeReferenceFieldsAfterInterrupt=len(data['zeroChargeReferenceFieldsAfterInterrupt']))
    counter=report('audit_v1349_ring_native_close_counterexamples',candidate)
    assert counter['count']==20 and counter['actualArtifactsUnchanged']and counter['inMemoryOnly']
    contacts_path=ROOT/'audit_v1344_ring_interrupt_contacts/report.json';contacts=json.loads(contacts_path.read_text());pin(contacts_path)
    assert contacts['candidate']==candidate and contacts['fullImagesNotCropped']and not contacts['productionArtChanged']
    reviewed=[]
    for case in contacts['cases'].values():
        pin(case['proof'],case['proofSHA256'])
        for sheet in case['sheets']:pin(sheet['file'],sheet['sha256']);reviewed.append(sheet)
        for image in case['entries']:pin(image['file'],image['sha256'])
    assert len(reviewed)==4
    # Bind every new raw/success/failure artifact and compiled snapshot. The
    # prior manifest is linked, not presented as a fresh audit of its67k pins.
    for folder in ROOT.iterdir():
        match=re.match(r'^(audit|diagnostic)_v(\d+)_',folder.name)
        if folder.is_dir()and match and 1280<=int(match[2])<=1349:
            for path in folder.rglob('*'):
                if path.is_file():pin(path)
    for parent in(ROOT,ROOT/'tools'):
        for path in parent.iterdir():
            match=re.search(r'_v(\d+)\.(?:lua|py|ps1)$',path.name)
            if path.is_file()and match and 1280<=int(match[1])<=1351:pin(path)
    for name in('PLAY_CURRENT_V1250_TEST_BUILD.cmd','tools/check_current_playtest_v1261.ps1','STATUS_2026-10-03_CURRENT_RING_STARTUP_AND_INTERRUPTION.md'):
        pin(ROOT/name)
    return dict(candidate=candidate,playableCandidate='diagnostic_v1250_native_correct_rom_metadata',currentTestLauncher='PLAY_CURRENT_V1250_TEST_BUILD.cmd',
        historicalCheckpoint=str(old_path),historicalCheckpointSHA256=digest(old_path),historicalPinsBoundByManifest=67162,historicalPinsIndividuallyRehashedThisCheckpoint=False,
        freshReports=reports,stagedNativeMirrorInterruptRetryScope=scopes,sourceCorrectPinkChargeAccepted=True,sourceCorrectCloseStartupContactAccepted=True,
        mainAgentReviewedContactSheets=reviewed,mainAgentReviewedActualFrames=sum(len(c['entries'])for c in contacts['cases'].values()),allRawFramesManuallyReviewed=False,
        broaderRegressionPending=True,launcherPromoted=False,releaseZIPUpdated=False,oldBuildFoldersDeleted=False,materialFilesDeleted=False,
        fullPortAccepted=False,inputHashes=pins)

if __name__=='__main__':
    assert not OUT.exists()
    try:
        record=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
        print('Incremental native ring checkpoint saved with '+str(len(record['inputHashes']))+' fresh pins; historical manifest linked, full goal open',flush=True)
    except Exception as error:
        OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(error=repr(error),fullPortAccepted=False),indent=2)+'\n');raise
