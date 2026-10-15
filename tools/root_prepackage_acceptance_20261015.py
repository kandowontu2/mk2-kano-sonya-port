"""Root evidence decision: original scope; package gate remains explicit, not inferred."""
import json
from pathlib import Path
import verify_native_source_sync as sync

R = sync.ROOT
OUT = R / 'audit_root_prepackage_acceptance_20261015'
assert not OUT.exists()
sync.verify()
pins = {}
def read(rel):
    p = R / rel
    pins[rel] = sync.sha(p)
    return json.loads(p.read_text())
def pin(rel):
    pins[rel] = sync.sha(R / rel)
original_rel = 'audit_native_guard_campaign_progress/report.json'
original = read(original_rel)['originalNaturalIntegrationRequirements']
assert pins[original_rel] == '70788CB905E4DAE1F2CD2A8C044B440363BA986D31570432C78FEA9A774F1254'
assert len(original) == 14
base_rel = 'audit_current_original14_finishline_checked/report.json'
base = read(base_rel)
assert base['originalScopePreserved']
for path, wanted in base['inputHashes'].items():
    assert sync.sha(Path(path)) == wanted, path
cpu_rel = 'audit_current_cpu_feature_composition_20261015_checked/report.json'
cpu = read(cpu_rel)
assert cpu['finiteCPURepertoireFeatureCompositionSupported']
assert cpu['oldSharedConstructionLines'] == 1321
assert len(cpu['effectiveFaultsRejected']) == 2
assert cpu['actualCurrentCPUEntries'] == {'kano':['knife','blade','choke','ball'], 'sonya':['ring','square','bicycle','leg']}
for path, wanted in cpu['sourceHashes'].items():
    assert sync.sha(Path(path)) == wanted
for e in cpu['evidence']:
    assert sync.sha(Path(e['report'])) == e['SHA256']
cin_rel = 'audit_current_cinematic_feature_closure_map/report.json'
cin = read(cin_rel)
assert cin['mappingPassed']
for rel, wanted in cin['inputHashes'].items():
    assert sync.sha(R / rel) == wanted, rel
laser_rel = 'audit_current_human_laser_four_png_v3_checked/report.json'
laser = read(laser_rel)
assert laser['finiteEarnedHumanLaserSceneBindingAccepted'] and len(laser['faultsRejected']) == 6
assert laser['contract']['earnedKORounds'] == 2 and laser['contract']['nativeDamage'] == 322
for path, wanted in laser['inputHashes'].items():
    assert sync.sha(Path(path)) == wanted
pin('audit_current_human_laser_four_png_v3_runtime/root_visual_review.txt')
census_rel = 'audit_after_cleanup_and_package_census_20261015/report.json'
census = read(census_rel)
assert census['complete'] and census['readOnly'] and census['files'] < 200000
removal_rels = ['audit_obsolete_capture_target_review_20261015/deletion_receipt.json',
                'audit_obsolete_combat_snapshot_review_20261015/deletion_receipt.json']
removed = 51660627
for rel in removal_rels:
    d = read(rel)
    assert not d['archiveCreated'] and d['permanentDeletion']
    removed += d['allocatedBytesFromCensus']
    for target in d['targets']:
        assert not (R / target).exists()
for name in ('roms_v19_clean','roms_v20_clean','roms_v21_clean'):
    assert not (R / name / 'mk2.zip').exists()
pin('audit_cleanup_rom_duplicate_review_20261015/deletion_receipt.txt')
assert removed == 222368752
rows = {}
for entry in base['requirements']:
    key = entry['requirement']
    assert entry['originalRequirement'] == original[key]
    if entry['classification'] == 'complete':
        rows[key] = dict(originalRequirement=original[key], classification='accepted',
                         positiveEvidence=[base_rel], basis=entry['assessment'])
assert len(rows) == 7
rows['cpu_moves'] = dict(originalRequirement=original['cpu_moves'], classification='accepted',
    positiveEvidence=[cpu_rel], basis='Eight actual current CPU entries plus unchanged shared native bodies, distinct changed dependencies and explicit current contact/effect/audio/cleanup coverage; not entry counts alone.')
for key, group in cin['requirements'].items():
    assert group['originalRequirement'] == original[key] and group['featureClosureSupported']
    assert group['actualRemainingIdentifiedDependency'] is None
    rows[key] = dict(originalRequirement=original[key], classification='accepted',
                     positiveEvidence=[cin_rel, *group['evidence']], basis=group['scope'])
assert len(rows) == 12
rows['storage'] = dict(originalRequirement=original['storage'], classification='accepted',
    positiveEvidence=[census_rel, *removal_rels, 'audit_cleanup_rom_duplicate_review_20261015/deletion_receipt.txt'],
    basis='Dependency-reviewed obsolete files removed permanently, exact guarded targets/receipts, one Git worktree and sole current game executable, fresh allocated-size census. Preserve source/reconstruction/accepted proof and original UI inputs; do not delete uncertain user data for an arbitrary space target.', removedBytes=removed)
rows['cmd_release'] = dict(originalRequirement=original['cmd_release'], classification='pending_final_package',
    positiveEvidence=['audit_updated_private_playtest_portable_check_20261015/report.json'],
    remaining='Final release documentation/manifest, streamed archive integrity and extracted standalone CMD verification; do not declare full goal complete before these pass.')
assert set(rows) == set(original)
report = dict(originalScopePreserved=True, originalRequirementCount=14, requirements=rows,
    featureRequirementsAccepted=12, storageAccepted=True, finalPackageAccepted=False, fullGoalComplete=False,
    rootDecisionBasis='Positive actual runtime/component evidence reviewed at matching scope, not mere absence of observed bugs. Historical incomplete/full-port flags retain their original meaning; explicit successor proofs close their identified gaps. No universal all-RNG/input criterion added.',
    inputHashes=pins, currentExecutableSHA256=sync.sha(sync.BUILD/'mkport_candidate.exe'))
OUT.mkdir()
(OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(dict(report=str(OUT/'report.json'), accepted=13, pending=['cmd_release'], fullGoalComplete=False)))
