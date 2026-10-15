"""Native recovery plus no live ROM callback; saved A6 may retain stale scratch."""
import verify_native_source_sync as sync
sync.verify()
old = sync.ROOT / 'audit_bounded_air_throw_live_recovery_preparation'
out = sync.ROOT / 'audit_bounded_air_throw_retirement_preparation'
assert not out.exists()
base = old / 'air_throw.lua'
source = base.read_text()
before = "if kind=='recovery'and regs.A6.value==0 then recovered_actors[a.actor]=frame end"
after = """if kind=='recovery'then
   -- At ordinary recovery A6 can be a small native scratch value. A live
   -- callback is a ROM address; later actual callback execution revokes this.
   if regs.A6.value<0xfe800000 then recovered_actors[a.actor]=frame
   else recovered_actors[a.actor]=nil end
  end"""
assert source.count(before) == 1
source = source.replace(before, after).replace('with live A6 zero.', 'without live ROM callback.')
out.mkdir()
target = out / 'air_throw.lua'
target.write_text(source)
for fighter in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old / f'run_{fighter}_p{side}.ps1').read_text()
        runner = runner.replace(old.name + '/air_throw.lua', out.name + '/air_throw.lua')
        runner = runner.replace(sync.sha(base), sync.sha(target))
        runner = runner.replace('audit_bounded_air_throw_live_recovery_', 'audit_bounded_air_throw_retirement_')
        (out / f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared native recovery/actual callback execution gate; no gameplay changes')
