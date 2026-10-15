"""Do not interpret idle A6 scratch as active flight callback; retain recovery gate."""
import verify_native_source_sync as sync
sync.verify()
old = sync.ROOT / 'audit_bounded_air_throw_routes_preparation'
out = sync.ROOT / 'audit_bounded_air_throw_initial_ready_preparation'
assert not out.exists()
base = old / 'air_throw.lua'
source = base.read_text()
before = "local function fully_clean(c)return clean(c)and c.callback==0 and p:read_u16(0x010619d0)==0 end"
after = """local function fully_clean(c)
   -- Before any throw, native grounded idle/ownership/physics is the gate.
   -- A6's saved scratch is a callback only during flight. All post-catch
   -- recovery and followups retain the original exact-zero callback check.
   return clean(c)and (air_mode=='approach'and not air_caught or c.callback==0)
    and p:read_u16(0x010619d0)==0
  end"""
assert source.count(before) == 1
source = source.replace(before, after)
out.mkdir()
target = out / 'air_throw.lua'
target.write_text(source)
for fighter in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old / f'run_{fighter}_p{side}.ps1').read_text()
        runner = runner.replace(old.name + '/air_throw.lua', out.name + '/air_throw.lua')
        runner = runner.replace(sync.sha(base), sync.sha(target))
        runner = runner.replace('audit_bounded_air_throw_routes_', 'audit_bounded_air_throw_initial_ready_')
        (out / f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Initial grounded-ready predicate separated; all post-catch zero-callback gates retained')
