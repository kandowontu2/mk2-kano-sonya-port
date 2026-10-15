"""Mutation sensitivity of the pinned finite battle-cleanup harness."""
import json
import subprocess
import verify_native_source_sync as sync

sync.verify()
baseline = sync.ROOT / 'audit_current_battle_cleanup_cpp'
report = json.loads((baseline / 'report.json').read_text())
harness = baseline / 'cleanup.cpp'
assert sync.sha(harness) == report['harnessSHA256']
text = harness.read_text()
out = sync.ROOT / 'audit_current_battle_cleanup_mutations'
assert not out.exists()
out.mkdir()
mutations = {
    'ignore_health_change': ('space.read_word(health[slot]) != m_mk2ks_battle_health[slot]', 'false'),
    'ignore_owner_change': ('read32(main + 0xc0) != actor', 'false'),
    'ignore_character_change': ('space.read_word(actor + 0x1f0) != m_mk2ks_battle_id[slot]', 'false'),
    'ignore_attract_mute': ('mode == 1 && space.read_word(0x01061990) != 0', 'false'),
    'stop_other_player_timer': ('!m_mk2ks_battle_actor[0] && !m_mk2ks_battle_actor[1]', 'true'),
    'skip_second_channel': ('m_mk2ks_voices->stop(11 + slot * 2);', '(void)0;'),
}
results = []
for name, (before, after) in mutations.items():
    assert text.count(before) == 1, name
    cpp = out / (name + '.cpp')
    cpp.write_text(text.replace(before, after))
    exe = out / (name + '.exe')
    build = subprocess.run(['C:/Strawberry/c/bin/g++.exe', '-std=c++17', '-O0', str(cpp), '-o', str(exe)], capture_output=True, text=True, timeout=30)
    (out / (name + '_compile.log')).write_text(build.stdout + build.stderr)
    assert build.returncode == 0, build.stderr
    run = subprocess.run([str(exe)], capture_output=True, text=True, timeout=10)
    (out / (name + '_run.log')).write_text(run.stdout + run.stderr)
    assert run.returncode != 0, 'Undetected mutation: ' + name
    assert 'Assertion' in run.stderr or 'assertion' in run.stderr, run.stderr
    results.append(dict(name=name, compiled=True, rejectedByAssertions=True, exitCode=run.returncode, harnessSHA256=sync.sha(cpp)))
(out / 'report.json').write_text(json.dumps(dict(passed=True, baselineHarnessSHA256=sync.sha(harness), mutations=results, gameSourcesModified=False, runtimeInterruptionAccepted=False, heardMixAccepted=False, fullPortAccepted=False), indent=2))
print('PASS six compiled mutations rejected by finite cleanup assertions')
