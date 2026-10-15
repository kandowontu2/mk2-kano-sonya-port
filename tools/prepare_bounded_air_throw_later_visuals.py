"""Later finite throw phases; eight PNG total, unchanged physical controller."""
import verify_native_source_sync as sync
sync.verify()
old = sync.ROOT/'audit_bounded_air_throw_visuals_preparation'
out = sync.ROOT/'audit_bounded_air_throw_later_visuals_preparation'
assert not out.exists()
base = old/'air_throw.lua'
source = base.read_text()
before = "label:match('^air_[12]_phase24$')or label:match('^air_[12]_recovered$')"
assert source.count(before) == 1
source = source.replace(before,"label:match('^air_[12]_phase40$')or label:match('^air_[12]_phase56$')")
out.mkdir()
target = out/'air_throw.lua'
target.write_text(source)
for fighter in ('kano','sonya'):
    runner = (old/f'run_{fighter}_p1.ps1').read_text()
    runner = runner.replace(old.name+'/air_throw.lua',out.name+'/air_throw.lua')
    runner = runner.replace(sync.sha(base),sync.sha(target))
    runner = runner.replace('audit_bounded_air_throw_visual_','audit_bounded_air_throw_later_visual_')
    (out/f'run_{fighter}_p1.ps1').write_text(runner)
print('Eight later-phase PNG maximum; prior captures preserved')
