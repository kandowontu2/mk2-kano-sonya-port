"""Require actual native recovery with cleared live A6, not stale saved scratch."""
import verify_native_source_sync as sync
sync.verify()
old = sync.ROOT / 'audit_bounded_air_throw_initial_ready_preparation'
out = sync.ROOT / 'audit_bounded_air_throw_live_recovery_preparation'
assert not out.exists()
base = old / 'air_throw.lua'
source = base.read_text()
source = source.replace('local air_follow_at=nil', 'local air_follow_at=nil\nlocal recovered_actors={}')
before = "  local a=sample(slot)\n  air_log('AIR_EVENT'"
after = """  local a=sample(slot)
  if kind=='action'then recovered_actors={}end
  if kind=='victim_callback'then recovered_actors[a.actor]=nil end
  if kind=='recovery'and regs.A6.value==0 then recovered_actors[a.actor]=frame end
  air_log('AIR_EVENT'"""
assert source.count(before) == 1
source = source.replace(before, after)
before = "(air_mode=='approach'and not air_caught or c.callback==0)"
after = "(air_mode=='approach'and not air_caught or recovered_actors[c.actor]~=nil)"
assert source.count(before) == 1
source = source.replace(before, after)
source = source.replace('-- recovery and followups retain the original exact-zero callback check.',
                        '-- recovery and followups require a native recovery event with live A6 zero.')
out.mkdir()
target = out / 'air_throw.lua'
target.write_text(source)
for fighter in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old / f'run_{fighter}_p{side}.ps1').read_text()
        runner = runner.replace(old.name + '/air_throw.lua', out.name + '/air_throw.lua')
        runner = runner.replace(sync.sha(base), sync.sha(target))
        runner = runner.replace('audit_bounded_air_throw_initial_ready_', 'audit_bounded_air_throw_live_recovery_')
        (out / f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Native recovery ledger; later actual callback invalidates retirement')
