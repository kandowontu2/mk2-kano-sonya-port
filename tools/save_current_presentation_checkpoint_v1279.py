"""Preserve current source rebuild, fresh move/fatality/UI/shadow evidence."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1279_current_presentation_checkpoint'
assert not OUT.exists(),'Preserve previous evidence'
pins={}

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb')as stream:
        for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest().upper()

def pin(path,wanted=None):
    path=Path(path);key=str(path);actual=pins[key]if key in pins else digest(path)
    assert wanted is None or wanted==actual,'Changed evidence '+key;pins[key]=actual

def report(folder):
    path=ROOT/folder/'report.json';data=json.loads(path.read_text(encoding='utf-8-sig'));pin(path)
    assert data['passed'],'Passing proof required '+folder
    if folder=='audit_v1256_native_metadata_corruption_checks':
        # This immutable report has no candidate field. Bind its exact native
        # baseline proof and all nine actual rejected counterexamples instead
        # of inventing a candidate value or accepting arbitrary missing IDs.
        assert data['checks']['baseline']['passed'] and data['checks']['baseline']['proof']==metadata['executableProof']
        assert len(data['checks'])==10 and all(value['rejected']for key,value in data['checks'].items()if key!='baseline')
        assert data['inMemoryOnly'] and data['actualRuntimeEvidenceChanged']is False
        pin(ROOT/'tools/test_native_metadata_build_v1256.py')
    else:
        assert data['candidate']=='diagnostic_v1250_native_correct_rom_metadata','Current matching proof required '+folder
    for file,wanted in data.get('inputHashes',data.get('input_hashes',{})).items():pin(file,wanted)
    return data

previous_path=ROOT/'audit_v1248_current_launcher_checkpoint/checkpoint.json';previous=json.loads(previous_path.read_text())
print('Revalidating',len(previous['inputHashes']),'preceding checkpoint pins',flush=True)
for i,(file,wanted)in enumerate(previous['inputHashes'].items()):
    pin(file,wanted)
    if i and i%10000==0:print('Historical evidence revalidated',i,flush=True)
pin(previous_path)
metadata=report('audit_v1254_native_rom_metadata_checked')
assert metadata['nativeROMAuditAccepted'] and metadata['sourceROMMetadataOnlyRebuild'] and metadata['canonicalHistoricalSourceRestored']
assert metadata['executableProof']['actualChangedBytes']==52 and metadata['executableProof']['nativeInstructionBytesUnchanged']==38277120
report('audit_v1256_native_metadata_corruption_checks')
human=report('audit_v1255_current_human_matrix_checked');assert len(human['cases'])==52
report('audit_v1257_stock_secondary_state_checked')
for key in ('control_kitana_p1','control_liu_p2','kano_p1','kano_p2','sonya_p1','sonya_p2'):
    data=report(f'audit_v1258_secondary_{key}_render_checked');assert data['currentSecondarySampledFullNativeRenderAccepted']
launcher=report('audit_v1262_current_launcher_checked');assert launcher['exit_code']==0
ground=report('audit_v1269_current_ground_shadow_checked')
assert ground['samples']==148 and ground['nativeShadowCopies']==120162 and ground['currentBoundedMobilityGroundShadowAccepted']
ui=report('audit_v1271_current_ui_flow_checked');assert len(ui['cases'])==4 and ui['currentBothSlotSelectionLadderFirstMatchAccepted']
unit=report('audit_v1273_current_native_ui_units');assert unit['methods']==46
counter=report('audit_v1275_current_ground_shadow_counterexamples');assert counter['count']==8 and counter['actualArtifactsUnchanged']
review=report('audit_v1276_current_presentation_review');assert review['actualMobilityImagesReviewed']==148 and review['actualUIImagesReviewed']==24
compactions={}
for folder in ('audit_v1260_inactive_evidence_compaction','audit_v1277_current_evidence_compaction'):
    path=ROOT/folder/'report.json';data=json.loads(path.read_text(encoding='utf-8-sig'));pin(path)
    assert data['verifiedFiles']==data['plannedFiles'] and data['oldBuildFoldersDeleted']is False
    for row in data['files']:
        assert row['verified'] and row['exitCode']==0;pin(row['path'],row['sha256'])
    for file,wanted in data['protectedFileHashes'].items():pin(file,wanted)
    compactions[folder]=dict(verifiedFiles=data['verifiedFiles'],reclaimedBytes=data['reclaimedBytes'],materialDataDeleted=False)
# Include complete executed sources/results, failed metadata proof, current
# compiled snapshots, diagnostic images and immutable raw captures, not just
# the successful report summaries.
for folder in ROOT.iterdir():
    if folder.is_dir() and (re.match(r'^audit_v(?:125[1-8]|126[0-2]|1268|1269|127[0-7])_',folder.name)or folder.name=='diagnostic_v1250_native_correct_rom_metadata'):
        for path in folder.rglob('*'):
            if path.is_file():pin(path)
for filename in ('PLAY_CURRENT_V1250_TEST_BUILD.cmd','KNOWN_CURRENT_TEST_BUILD_WARNING.md',
    'STATUS_2026-10-03_CURRENT_GROUND_SHADOW_AND_UI.md','tools/build_metadata_candidate_v1249.ps1',
    'tools/verify_native_metadata_build_v1251.py','tools/verify_native_metadata_build_v1254.py',
    'tools/verify_current_human_matrix_v1255.py','tools/test_native_metadata_build_v1256.py',
    'tools/verify_stock_scorpion_secondary_v1257.py','tools/verify_stock_secondary_display_v1258.py',
    'tools/compact_inactive_builds_v1259.ps1','tools/compact_inactive_evidence_v1260.ps1',
    'tools/check_current_playtest_v1261.ps1','tools/test_current_launcher_v1262.ps1',
    'tools/verify_current_ground_shadow_v1269.py','tools/verify_current_ui_flow_v1271.py',
    'tools/make_current_ground_contacts_v1272.py','tools/test_current_native_ui_v1273.py',
    'tools/make_current_ui_contacts_v1274.py','tools/test_current_ground_shadow_v1275.py',
    'tools/save_current_presentation_review_v1276.py','tools/compact_current_evidence_v1277.ps1',
    'tools/save_current_presentation_checkpoint_v1278.py','tools/save_current_presentation_checkpoint_v1279.py',
    'audit_v1278_current_presentation_checkpoint/failure.json'):
    pin(ROOT/filename)
record=dict(candidate='diagnostic_v1250_native_correct_rom_metadata',historicalCheckpoint=str(previous_path),
    historicalPinsRevalidated=len(previous['inputHashes']),inputHashes=pins,currentTestLauncher='PLAY_CURRENT_V1250_TEST_BUILD.cmd',
    sourceROMMetadataOnlyRebuildAccepted=True,ordinaryHeadlessBootAccepted=True,interactiveVideoAudioAccepted=False,
    currentHumanSpecialStateCases=52,currentSecondarySampledNativeRenderCases=6,
    currentBothSlotSelectionLadderFirstMatchAccepted=True,currentBoundedMobilityGroundShadowAccepted=True,
    mobilitySamples=148,nativeShadowCopies=120162,UIUnitMethods=46,groundShadowCounterexamples=8,
    currentMainAgentPresentationReviewAccepted=True,compaction=compactions,
    allMoveChoreographyAccepted=False,allProjectileNativeRenderLifetimeAccepted=False,allFatalitiesAccepted=False,
    allArenaFloorShadowsAccepted=False,fullTowersBossesContinuesEndingsAccepted=False,audioAccepted=False,
    finalReleaseAccepted=False,oldBuildFoldersDeleted=False,materialDataDeleted=False,goalComplete=False,fullPortAccepted=False)
OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print('Current rebuilt UI/shadow checkpoint saved;',len(pins),'pins; full objective remains open',flush=True)
