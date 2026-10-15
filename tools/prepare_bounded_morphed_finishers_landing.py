"""Retain original KO settling before binding the physical finisher gap."""
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT/'audit_bounded_morphed_finishers_settle_preparation'
out = sync.ROOT/'audit_bounded_morphed_finishers_landing_preparation'
assert not out.exists()
source = (old/'finishers.lua').read_text()
before = '  if not approach_done then'
assert source.count(before) == 1
source = source.replace(before, '  if age>=65 and not approach_done then')
out.mkdir()
lua = out/'finishers.lua'
lua.write_text(source)
for target in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old/f'run_{target}_p{side}.ps1').read_text()
        runner = runner.replace(old.name+'/finishers.lua', out.name+'/finishers.lua')
        runner = runner.replace(sync.sha(old/'finishers.lua'), sync.sha(lua))
        runner = runner.replace('audit_bounded_morphed_finisher_settle_', 'audit_bounded_morphed_finisher_landing_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared original KO landing/spacing timing after true combat morph')
