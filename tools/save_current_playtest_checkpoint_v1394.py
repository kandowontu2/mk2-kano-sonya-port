"""Bind prior manifest and freshly verify the current regression/playtest delta."""
import json,re
from pathlib import Path
import verify_ring_native_lookup_v1342 as current
ROOT=current.ROOT;OUT=ROOT/'audit_v1394_current_playtest_checkpoint'

def verify():
    pins={};reports={}
    def pin(path,wanted=None):
        path=Path(path);key=str(path);actual=pins.get(key)or current.digest(path)
        assert wanted is None or actual==wanted,'Changed evidence '+key;pins[key]=actual
    previous=ROOT/'audit_v1351_native_ring_progress_checkpoint/checkpoint.json'
    pin(previous,'9B4F0A729F87C06C87A64801F848116613E589003A36472DC0E6803275DC8E31')
    old=json.loads(previous.read_text());assert len(old['inputHashes'])==25783 and old['fullPortAccepted']is False
    names=['audit_v1368_current_ui_flow_checked','audit_v1373_current_ground_shadow_checked',
           'audit_v1389_current_human_matrix_checked','audit_v1392_current_launcher_checked']
    for side in(1,2):
        names += [f'audit_v1352_projectile_ring_p{side}_render_checked',
                  f'audit_v1360_ring_close_block_p{side}_render_checked',
                  f'audit_v1374_ring_close_miss_p{side}_render_checked',
                  f'audit_v1388_blade_native_gore_p{side}_checked']
        names += [f'audit_v1353_projectile_ring_{scenario}_p{side}_render_checked'for scenario in('block','miss')]
    for name in names:
        path=ROOT/name/'report.json';data=json.loads(path.read_text(encoding='utf-8-sig'))
        assert data['passed']and data['candidate']==current.CANDIDATE;pin(path)
        for file,wanted in data.get('inputHashes',{}).items():pin(file,wanted)
        reports[name]=dict(passed=True,reportSHA256=current.digest(path))
    dispatch=ROOT/'audit_v1364_human_matrix_dispatch/report.json';data=json.loads(dispatch.read_text())
    assert data['allRunnersTerminal']and data['allRunnerExitsZero']and len(data['cases'])==52;pin(dispatch)
    matrix=json.loads((ROOT/'audit_v1389_current_human_matrix_checked/report.json').read_text())
    assert len(matrix['cases'])==52 and matrix['exactPriorActualImagesMatched']==154
    assert matrix['sourceProvenNativeBloodVariationImages']==2 and matrix['everyPriorHumanEventMatched']
    contacts_path=ROOT/'audit_v1390_current_regression_contacts/report.json'
    contacts=json.loads(contacts_path.read_text());pin(contacts_path)
    assert contacts['fullImagesNotCropped']and not contacts['productionArtChanged']
    reviewed=[];frames=set()
    for case in contacts['cases'].values():
        for proof in case['proofs']:pin(proof['file'],proof['sha256'])
        for sheet in case['sheets']:pin(sheet['file'],sheet['sha256']);reviewed.append(sheet)
        for image in case['entries']:pin(image['file'],image['sha256']);frames.add(image['file'])
    assert len(reviewed)==8
    for folder in ROOT.iterdir():
        match=re.match(r'^audit_v(\d+)_',folder.name)
        if folder.is_dir()and match and 1352<=int(match[1])<=1392:
            for path in folder.rglob('*'):
                if path.is_file():pin(path)
    for parent in(ROOT,ROOT/'tools'):
        for path in parent.iterdir():
            match=re.search(r'_v(\d+)\.(?:lua|py|ps1)$',path.name)
            if path.is_file()and match and 1352<=int(match[1])<=1394:pin(path)
    for name in('PLAY_CURRENT_V1340_TEST_BUILD.cmd','STATUS_2026-10-03_CURRENT_V1340_PLAYTEST.md'):pin(ROOT/name)
    for name,wanted in(
        ('mame-mkp/src/mame/midway/midtunit_m.cpp','EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34'),
        ('mame-mkp/src/mame/midway/midtunit.cpp','07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85'),
        ('mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'),
        ('PLAY_CURRENT_V1250_TEST_BUILD.cmd','8327B3DF7DCB577B38EAB82F922FE84C3564FC2C0259ADC63045701A94A45826')):
        pin(ROOT/name,wanted)
    return dict(candidate=current.CANDIDATE,playableCandidate=current.CANDIDATE,
                currentTestLauncher='PLAY_CURRENT_V1340_TEST_BUILD.cmd',launcherPromoted=True,
                historicalCheckpoint=str(previous),historicalCheckpointSHA256=current.digest(previous),
                historicalPinsBoundByManifest=25783,historicalPinsIndividuallyRehashedThisCheckpoint=False,
                freshReports=reports,currentHumanCases=52,exactPriorActualImagesMatched=154,
                sourceProvenNativeBloodVariationImages=2,mainAgentReviewedContactSheets=reviewed,
                mainAgentReviewedUniqueActualFrames=len(frames),allRawFramesManuallyReviewed=False,
                canonicalHistoricalSourcesAndInstalledExeRestored=True,olderCurrentLauncherUnchanged=True,
                broaderFullGameIntegrationPending=True,releaseZIPUpdated=False,oldBuildFoldersDeleted=False,
                materialFilesDeleted=False,fullPortAccepted=False,inputHashes=pins)

if __name__=='__main__':
    assert not OUT.exists()
    try:
        data=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(data,indent=2)+'\n')
        print('Current v1340 playtest checkpoint saved with '+str(len(data['inputHashes']))+' fresh pins; full goal remains open',flush=True)
    except Exception as error:
        OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(error=repr(error),fullPortAccepted=False),indent=2)+'\n');raise
