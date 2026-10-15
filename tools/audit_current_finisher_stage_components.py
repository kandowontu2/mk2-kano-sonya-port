"""Finite teardown dependency matrix; historical comments are not defect proof."""
import json,hashlib,difflib,copy
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
current=root/'mame-mkp/src/mame/midway/midtunit_m.cpp';old=root/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
a=current.read_text();b=old.read_text()
regions={
 'Pit_fall_impact_camera_constructor':('// Pit II has a separate twelve-fighter front-facing falling/impact table.','if (memcmp(donor + effect_header, "KFX1", 4))'),
 'stage_command_gate':("// MKII's Pit/Tomb finishers are shared arena actions",'// Original MK3 physical-input traces select Kano0/Sonya1'),
 'Babality_gate_cleanup_handoff':('// Original MK3 physical-input traces select Kano0/Sonya1','// Individual finisher entry points'),
 'primary_own_finisher_choreography':('// Individual finisher entry points','// Character-owned Friendships.'),
 'Friendship_command_eligibility_choreography':('// Character-owned Friendships.', '// Kano/Sonya dim to 3/8 brightness'),
}
result={};expected={}
for name,(start,end)in regions.items():
    def extract(text):lo=text.index(start);return text[lo:text.index(end,lo)]
    x,y=extract(a),extract(b)
    result[name]=dict(normalizedSourceEqual=x==y,currentSHA256=hashlib.sha256(x.encode()).hexdigest(),historicalSHA256=hashlib.sha256(y.encode()).hexdigest(),currentCharacters=len(x),historicalCharacters=len(y),changedLines=[l for l in difflib.unified_diff(y.splitlines(),x.splitlines(),n=1)if l.startswith(('+','-'))][:40])
    expected[name]=result[name]['currentSHA256']
def gate(observed):assert observed==expected
gate(expected);faults=[]
for name in expected:
    bad=dict(expected);bad[name]='0'*64
    try:gate(bad)
    except AssertionError:faults.append(name)
    else:raise AssertionError('Altered component admitted')
reports=['audit_current_native_pit_roles_checked','audit_current_native_tomb_roles_checked','audit_current_native_tomb_pressed_checked','audit_current_native_deadpool_stock_victim_checked','audit_current_native_pit_stock_kunglao_checked','audit_current_native_tomb_stock_kunglao_checked','audit_current_native_pit_stock_jax_sonya_p2_checked','audit_current_native_tomb_stock_jax_sonya_p2_checked','audit_current_morph_complete_ledgers_checked','audit_current_laser_cleanup_cpp','audit_current_stock_stage_dcs_packet_conservation_v2_checked','audit_current_secret_native_code_checked']
evidence=[]
for name in reports:
    p=root/name/'report.json';d=json.loads(p.read_text());evidence.append(dict(report=str(p),SHA256=sync.sha(p),scope=d.get('scope'),runtimePassed=d.get('passed'),wholePortClaim=False))
out=root/'audit_current_finisher_stage_components_checked';assert not out.exists();out.mkdir()
report=dict(consolidationPassed=True,finiteGuestComponentRegions=result,effectiveDependencyFaultsRejected=faults,currentEvidence=evidence,historicalAcceptedOwnFinisherFriendshipBabalityStageProofsNotReset=True,currentWholeSourceSHA256=sync.sha(current),historicalWholeSourceSHA256=sync.sha(old),backendAndPayloadConservationReportSHA256=sync.sha(root/'audit_current_standing_renderer_dependencies_checked/report.json'),actualRemainingDistinctBranch='Current secondary laser/orb and transformed-finisher cinematic teardown are outside this primary/Babality/Friendship/Pit construction transfer and current morph20 standard ledgers. Exact current laserC++30case cleanup tested but runtimeInterruptionAccepted=false; choose an actual active-secondary-finisher ownership transition if existing current runtime proof does not already close it.',sourceCommentsNotUsedAsDefectProof=True,scope='Finite source construction/evidence composition, not a fresh wholeplay/wholePNG/wholePCM proof. Unchanged primary/Pit/baby/friend regions can retain historical acceptedfinite choreography and teardown with current owner/role/stock/morph/hostrenderer evidence. Nativecurrent stage801+1100followthrough retirement and realpressed/drop branches do not imply everyvictim/RNGtested. No changedcomponent is auto-labelled defect; no emulator/media/edits exceptthis smallaudit.',fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v['normalizedSourceEqual']for k,v in result.items()}));print(out)
