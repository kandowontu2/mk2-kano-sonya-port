"""Read-only requirement/component mapping; no new gameplay acceptance tests."""
import hashlib
import json
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
out=root/'audit_current_cinematic_feature_closure_map'
assert not out.exists()
original=json.loads((root/'audit_native_guard_campaign_progress/report.json').read_text())['originalNaturalIntegrationRequirements']
groups={
 'finishers_victims': dict(
  evidence=['audit_current_finisher_stage_components_checked/report.json','audit_current_secondary_laser_components_checked/report.json','audit_current_human_laser_four_png_v3_checked/report.json','audit_current_human_laser_four_png_v3_runtime/root_visual_review.txt','audit_morphed_sonya_orb_visual_checked/report.json','audit_morphed_victims_secondary_pairs_checked/report.json','audit_bounded_morphed_secondary_finishers_checked/report.json'],
  scope='Five exact conserved primary/Friend/Baby/Pit guest construction regions retain accepted choreography. Secondary whole typed construction/renderer/payload and four finish-audio functions conserved. Current earned true17 versus18 laser now has phase/body/nativewinner and paid nextscene visible clearance; root reviewed charge/beam/postflashburst/selection. Current transformedSonya orb both-slot body-hide PNGs and eight genuine morphed-victim secondary paired ledgers plus four transformed-performer secondary cases support form integration. No newly identified changed finisher dependency remains.',
  notClaimed='Every allocation/interrupt/victim/arena combination; those universal criteria were not requested.'),
 'stage_finishers':dict(
  evidence=['audit_current_finisher_stage_components_checked/report.json','audit_current_native_pit_roles_checked/report.json','audit_current_native_tomb_roles_checked/report.json','audit_current_native_tomb_pressed_checked/report.json','audit_current_native_deadpool_stock_victim_checked/report.json','audit_current_stock_stage_dcs_packet_conservation_v2_checked/report.json'],
  scope='Exact conserved Pit constructor/stage command gate retains accepted stage choreography; current both-slot performer/victim roles and 801 scene plus1100 followthrough, pressed-drop and stockvictim/nativeDeadPool retirement cover actual integration. Entire normalized native DCS transport conserved with complete current earned stockvictim Pit/Tomb packets. Earlier accepted finite art/audio/RNG proof retained rather than reset by wholeEXE inequality.',
  notClaimed='Every random outcome or stockvictim exhaustive matrix.'),
 'campaign_cinematics':dict(
  evidence=['audit_current_campaign_change_proof_matrix_v2_checked/report.json','audit_current_loaded_campaign_transitions_checked/report.json','audit_current_historical_sonya_ending_scope_v2_checked/report.json','audit_current_loaded_sonya_ending_components_checked/report.json','audit_current_stock_row40_lifecycle_transfer_checked/report.json','audit_current_kano_ending_sonya_crossjoin_v3_checked/report.json','audit_current_kano_smoke_return_faults_checked/report.json','audit_current_sonya_smoke_return_faults_checked/report.json','audit_current_native_smoke_visuals_checked/report.json','audit_current_native_smoke_visuals_checked/visual-review.txt','audit_current_long_attract_reset_notifier_checked/report.json'],
  scope='Campaign matrix v2 finds no uncovered changed transition dependency: seven components, current208 loaded boss/schedule/context values, repaired41 stock photo pointers and ownending assets, historical four earned campaigns and independent ending pages/nativeaudio, currentKano full earned ending and Sonya fresh join. Current naturalSmoke entry/normalKO/paidreselection/181returnfields both addedfighters; separate four-image reviewed receipt supersedes pendingvisual flag. Corrected biography decode/return/photo transfer and current135k noreset attract are distinct supporting evidence. No new four-cold-wins prerequisite.',
  notClaimed='Four fresh current full campaign replays or universal secret routes; bot losses are not transition defects.'),
 'audio':dict(
  evidence=['audit_current_historical_sonya_ending_scope_v2_checked/report.json','audit_current_ending_stock_route_invariants_checked/report.json','audit_current_stock_stage_dcs_packet_conservation_v2_checked/report.json','audit_current_secondary_laser_components_checked/report.json','audit_native_kano_laser_cpu_motion_audio_review/report.json','audit_current_cpu_sonya_voice_earlier_upper_checked/report.json','audit_current_kano_cpu_health_voice_transfer_checked/report.json','audit_current_battle_audio_hit_cleanup_checked/report.json','audit_current_os_audio_admission_partial_checked/report.json'],
  scope='Original requirement concerns native sounds/priority/RNG/finite lifetime/no stale playback, not hardware hearing. Retained exact finite PCM/native mixed waveforms and decoder/mixer/clock/payload dependencies compose with current originalROM caller/cue/queue-priority invariants, protected native DCS packet stores and current phase/owner/startup cleanup evidence. Genuine currentCPU18 hit stops activecry beforeEOF; identical shared watcher with retained both-slotKano hit provides CPU17 component transfer (no CPU-specific branch). DefaultDirectSound48000/16bit/stereo exactPID render session has34 active nonzero/unmuted readings, peak0.08288494; closes output admission despite wall-capped probe not reaching1850field normal exit.',
  notClaimed='Hardware hearing, subjective mix judgement, all RNG outcomes or all contexts. No identified changed dependency demands a new all-waveform recording.')
}
pins={}
for key,g in groups.items():
 g['originalRequirement']=original[key]
 g['featureClosureSupported']=True
 g['actualRemainingIdentifiedDependency']=None
 for rel in g['evidence']:
  p=root/rel;assert p.is_file(),p
  pins[rel]=hashlib.sha256(p.read_bytes()).hexdigest().upper()
for rel in ['audit_native_guard_campaign_progress/report.json','mame-mkp/src/mame/midway/midtunit_m.cpp','mame-mkp/src/mame/midway/midtunit.cpp','mame-mkp/src/mame/midway/midtunit_v.cpp','mame-mkp/src/mame/midway/midtunit_v.h']:
 p=root/rel;pins[rel]=hashlib.sha256(p.read_bytes()).hexdigest().upper()
report=dict(mappingPassed=True,requirements=groups,inputHashes=pins,
 conclusion='No concrete uncovered changed cinematic/finisher/stage/audio dependency identified in this review. Supports feature closure by component/current-runtime composition, not standalone final wholeport promotion. Immutable old fullport/pending flags describe original finite scopes, not missing implemented features; separate reviewed receipts retained.',
 actualRemainingDeliverables='Root final integrated requirement decision, matching updated standalone release/CMD/docs and fresh dependency-aware workspace cleanup census.',
 newEmulatorRuns=0,newMedia=0,newGameChanges=0,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(out,len(pins))
