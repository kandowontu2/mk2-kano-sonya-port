"""Preserve original scope and expose remaining gaps; never promote by counts."""
import json
import verify_native_source_sync as sync

EVIDENCE={
 'selection':['audit_bounded_css_cadence_checked','audit_bounded_css_backdrop_geometry_checked'],
 'transition':['audit_bounded_css_teardown_owner_checked','audit_bounded_cross_finisher_rejoin_p1_checked'],
 'identity':['audit_bounded_current_attract_actors_checked','audit_current_morph_complete_ledgers_checked'],
 'names':['audit_current_kano_winner_visual_checked','audit_current_sonya_winner_visual_screen_checked'],
 'human_moves':['audit_bounded_current_ball_cycles_checked','audit_bounded_current_blade_cycles_checked','audit_bounded_current_bicycle_followup_damage_checked'],
 'cpu_moves':['audit_current_sonya_cpu_router_complete_checked','audit_current_kano_cpu_mirror_long_checked'],
 'ordinary_combat':['audit_bounded_current_basic_controls_checked','audit_bounded_air_throw_roster_coverage_checked'],
 'ground_shadows':['audit_bounded_aerial_motion_points_checked','audit_bounded_campaign_shadows_checked'],
 'audio':['audit_bounded_current_bio_cues_checked'],
 'finishers_victims':['audit_morphed_victims_secondary_pairs_checked','audit_morphed_victims_sonya_primary_checked'],
 'stage_finishers':[],
 'campaign_cinematics':['audit_current_ending_asset_tables_checked','audit_current_sonya_reptile_crouch_counter_long_checked'],
 'cmd_release':['audit_current_launcher_routing'],
 'storage':[]}

def main():
    source=sync.verify()
    out=sync.ROOT/'audit_current_full_scope_frontier';assert not out.exists()
    original_path=sync.ROOT/'audit_native_guard_campaign_progress/report.json'
    assert original_path.stat().st_size<1000000
    original=json.loads(original_path.read_text())
    requirements=original['originalNaturalIntegrationRequirements']
    assert set(EVIDENCE)==set(requirements) and len(requirements)==14
    frontier={}
    for key,description in requirements.items():
        records=[]
        for name in EVIDENCE[key]:
            path=sync.ROOT/name/'report.json'
            assert path.stat().st_size<2000000
            report=json.loads(path.read_text())
            assert report.get('passed',report.get('passedObservationChecks',False)) is True
            records.append(dict(path=str(path),SHA256=sync.sha(path),
                                exactReportedScope=report.get('scope','See pinned original report'),
                                completedRunAccepted=report.get('completedRunAccepted'),
                                provesEntireRequirement=False))
        frontier[key]=dict(originalRequirement=description,
                           status='incomplete verification / finite evidence only' if records else 'not freshly verified in this audit',
                           evidence=records,entireRequirementAchieved=False)
    cleanup=sync.ROOT/'CLEANUP_OLD_SUBZERO_CAPTURE_JSON_2026-10-13.json'
    deletion=json.loads(cleanup.read_text())
    assert deletion['DeletedFiles']==14 and all(not __import__('pathlib').Path(t['Path']).exists() for t in deletion['Targets'])
    frontier['storage'].update(status='partial cleanup; physical-size discrepancy unresolved',
        cleanupReceipt=dict(path=str(cleanup),SHA256=sync.sha(cleanup),
                            logicalBytesRemoved=deletion['LogicalBytesRemoved'],
                            observedFreeSpaceDelta=deletion['ObservedFreeSpaceDelta']))
    report=dict(auditPerformed=True,goalStatus='active',fullPortAcceptance=False,
                originalScopePath=str(original_path),originalScopeSHA256=sync.sha(original_path),
                originalRemainingWorkGroups=original['originalRemainingWorkGroups'],
                acceptedPriorWorkNotReset=True,sourceSync=source,requirements=frontier,
                currentBuild=sync.BUILD.name,sourceSearchFoundNoExplicitTODO=True,
                noTODOIsNotCompletionProof=True,
                currentFullBossEndingClearProven=False,currentStandaloneZIPProduced=False,
                nextPriority='Current natural boss/ending campaign route and remaining stage-finisher/secret/cinematic runtime gaps; do not replay a proven losing controller policy unchanged.',
                scope='Evidence-linked frontier across all14original requirements, not an acceptance certificate. Representative current reports do not replace broader historical work, prove universal contexts, or erase missing combined final regression/release.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(requirementsAudited=14,fullPortAcceptance=False,currentLaunchRoutingVerified=True)))

if __name__=='__main__':main()
