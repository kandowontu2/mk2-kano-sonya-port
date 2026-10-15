"""Finite CPU repertoire composition across actual entries and shared native bodies."""
import difflib
import hashlib
import json
from pathlib import Path

R=Path(__file__).resolve().parent.parent
out=R/'audit_current_cpu_feature_composition_20261015_checked'
assert not out.exists()
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest().upper()
current=R/'mame-mkp/src/mame/midway/midtunit_m.cpp'
old=R/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
a=current.read_text();b=old.read_text()
start='constexpr unsigned knife_action =';end="// MKII's Pit/Tomb finishers"
region=lambda s:s[s.index(start):s.index(end)].splitlines()
now,before=region(a),region(b)
def conservation(actual):
    changes=[(tag,i,j,k,l) for tag,i,j,k,l in difflib.SequenceMatcher(None,before,actual,autojunk=False).get_opcodes() if tag!='equal']
    assert len(changes)==3 and all(tag=='insert' for tag,*_ in changes)
    inserts=['\n'.join(actual[k:l]) for _,i,j,k,l in changes]
    assert len(inserts[0].splitlines())==25 and 'projectile_task_ids = 0xfd700' in inserts[0]
    assert len(inserts[1].splitlines())==1329 and '// PAIRED_STUMBLE_TABLE_BEGIN' in inserts[1]
    assert 'ground_throw_lookup' in inserts[1] and 'SHANG_OWNED_REACTION_BEGIN' in inserts[1]
    assert len(inserts[2].splitlines())==4 and 'ball_movi(0, 0x6b03)' in inserts[2]
    return changes
changes=conservation(now)
route=a[a.index('\t// CPU specials enter through'):a.index(end)]
assert 'route_cpu_special(ai_variety_router, native_address(knife_action),' in route
assert 'native_address(ball_action), native_address(blade_action)' in route
assert 'native_address(square_action), native_address(bike_action)' in route
assert 'route_cpu_close(ai_close_router+0x20,native_address(leg_action))' in route
assert 'route_cpu_close(ai_close_router+0x40,native_address(choke_action))' in route
assert '0x09c0,7,' in route
faults=[]
for label,bad in [('changed shared action', [line.replace('native_address(ball_action), native_address(blade_action)','native_address(ball_action), native_address(knife_action)') for line in now]),
                  ('changed shared victim contact', [line.replace('leg_movi(0,0x214)', 'leg_movi(0,0x215)') for line in now])]:
    assert bad!=now
    try:conservation(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Changed shared move body admitted')

names=['audit_current_sonya_cpu_router_complete_checked','audit_current_kano_cpu_mirror_long_checked',
       'audit_native_selector_special_matrix_checked','audit_native_selector_special_visuals_combined_checked',
       'audit_native_selector_sonya_cpu_air_contact_recovery_checked','audit_native_selector_cpu_startup_guard_knife_checked',
       'audit_v6328_current_cpu_blade_knife_body_shadow_checked','audit_v6359_current_cpu_effect_render_checked',
       'audit_v6373_current_cpu_blade_knife_audio_checked','audit_v6407_current_cpu_ring_mirror_audio_checked',
       'audit_v6417_current_cpu_ring_miss_phase_checked','audit_v6429_current_cpu_ring_miss_audio_checked',
       'audit_v6436_current_cpu_compound_render_checked','audit_v6447_current_cpu_compound_audio_checked',
       'audit_v6455_current_cpu_ball_render_checked','audit_v6462_current_cpu_ball_audio_checked',
       'audit_v6473_current_cpu_bicycle_render_checked','audit_current_loaded_dispatch_boundaries_checked',
       'audit_current_standing_renderer_dependencies_checked','audit_current_morph_complete_ledgers_checked',
       'audit_current_cpu_kano_ball_audio_checked','audit_current_cpu_sonya_bicycle_audio_checked',
       'audit_current_cpu_sonya_voice_earlier_upper_checked','audit_current_kano_cpu_health_voice_transfer_checked',
       'audit_current_battle_cleanup_cpp','audit_current_battle_audio_hit_cleanup_checked']
evidence=[]
for name in names:
    p=R/name/'report.json';d=json.loads(p.read_text())
    assert any(d.get(k) is True for k in ('passed','naturalCpuBallVoicePassed','naturalCpuBicycleVoicePassed','finiteObservationPassed','sharedWatcherComponentTransferSupported')),name
    evidence.append(dict(report=str(p),SHA256=sha(p),scope=d.get('scope') or d.get('scopeLimitation') or 'Finite named component only; consult pinned report.',
                         scalarAcceptance={k:v for k,v in d.items() if isinstance(v,bool) and k not in ('fullPortAccepted','fullPortAcceptance')}))
report=dict(finiteCPURepertoireFeatureCompositionSupported=True,
            basis='Current natural native routers actually enter all eight owned action bodies. CPU routes branch directly to the SAME native action addresses reached by human parsers; no separate CPU move animation/collision/physics/effect body exists. The entire old shared move/router construction survives in order with only three explicit insertions; preserved standard human contact/block/miss/recovery and CPU-specific compound contact/raster/audio cases compose with current dispatch and teardown proofs.',
            oldSharedConstructionLines=len(before),currentConstructionLines=len(now),
            conservation='No old shared action/router line replaced/deleted/reordered after newline normalization. This is source composition, not whole guest ROM equality.',
            changedDependencies=[dict(kind='packed projectile task/render identifiers',lines=25,currentProof='Current loaded dispatch boundaries plus actual blocked Knife pool pop/push and ordinary joined play'),
                                 dict(kind='separate paired/victim/finisher construction inserted between projectile and Square sections',lines=1329,currentProof='Current morph/victim/ordinary and finisher-specific ledgers, not implicitly called a CPU move body'),
                                 dict(kind='Kano Ball launch cue',lines=4,currentProof='Current genuine CPU17 owned Ball voice, shared both-slot health watcher and CPU18 active-hit interruption')],
            actualCurrentCPUEntries=dict(kano=['knife','blade','choke','ball'],sonya=['ring','square','bicycle','leg']),
            retainedSpecificCPUCases='Blocked Knife actual contact/6chip/body49fields/child50/pool retirement; Sonya Bicycle22contact/paired16float/separate recovery; native leg→Square compound; Ball/ring/knife/blade body/effect/raster/audio contexts. These are not inferred from router entry counts alone.',
            remainingCPUOnlyChangedRuntimeBranchIdentified=None,
            smallestRemainingCPUAction='No additional random CPU×outcome sweep justified. Keep finite source-bound composition separate from final integrated release/finisher/cinematic output signoff. Any new CPU test should target a concrete distinct changed dependency, not duplicate the shared human body matrix.',
            directCurrentCPU17ActiveHitRuntimeAccepted=False,
            universalAllCPUContextsAccepted=False,heardHardwareMixAccepted=False,fullPortAccepted=False,
            effectiveFaultsRejected=faults,evidence=evidence,
            sourceHashes={str(current):sha(current),str(old):sha(old)},
            newEmulatorRuns=0,newBuilds=0,newMedia=0)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(report=str(out/'report.json'),finiteCPUComposition=True,retainedReports=len(evidence),unchangedOldLines=len(before),faults=faults)))
