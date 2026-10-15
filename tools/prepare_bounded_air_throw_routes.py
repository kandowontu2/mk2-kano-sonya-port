"""Restore original read-only CSS BFS omitted with raw observer block."""
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT / 'audit_bounded_air_throw_roles_preparation'
out = sync.ROOT / 'audit_bounded_air_throw_routes_preparation'
assert not out.exists()
original = (sync.ROOT / 'mk2ks_special_shadow_v5131.lua').read_text()
start = original.index('local function route(start,target)')
end = original.index('emu.register_frame_done(function()', start)
helper = original[start:end]
base = old / 'air_throw.lua'
source = base.read_text()
marker = "assert(spec[1]==17 or victim_id==11"
assert source.count(marker) == 1
source = source.replace(marker, helper + marker)
out.mkdir()
target = out / 'air_throw.lua'
target.write_text(source)
for fighter in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old / f'run_{fighter}_p{side}.ps1').read_text()
        runner = runner.replace(old.name + '/air_throw.lua', out.name + '/air_throw.lua')
        runner = runner.replace(sync.sha(base), sync.sha(target))
        runner = runner.replace('audit_bounded_air_throw_roles_', 'audit_bounded_air_throw_routes_')
        (out / f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Restored native CSS BFS only; failed predecessor preserved')
