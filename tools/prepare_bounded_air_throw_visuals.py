"""Eight PNG maximum across two unchanged physical air-role runs."""
import verify_native_source_sync as sync
sync.verify()
old = sync.ROOT / 'audit_bounded_air_throw_retirement_preparation'
out = sync.ROOT / 'audit_bounded_air_throw_visuals_preparation'
assert not out.exists()
base = old / 'air_throw.lua'
source = base.read_text()
source += '''
local visual_count=0
emu.register_frame_done(function()
 local label=marks[frame]
 if label and (label:match('^air_[12]_phase24$')or label:match('^air_[12]_recovered$'))then
  assert(visual_count<4,'Four PNG maximum per run')
  screen:snapshot(label..'.png');visual_count=visual_count+1
  log('VISUAL_SAVED','label='..label..' count='..visual_count)
 end
end)
'''
out.mkdir()
target = out / 'air_throw.lua'
target.write_text(source)
for fighter in ('kano', 'sonya'):
    runner = (old / f'run_{fighter}_p1.ps1').read_text()
    runner = runner.replace(old.name + '/air_throw.lua', out.name + '/air_throw.lua')
    runner = runner.replace(sync.sha(base), sync.sha(target))
    runner = runner.replace('audit_bounded_air_throw_retirement_', 'audit_bounded_air_throw_visual_')
    runner = runner.replace("rawMedia='none'", "rawMedia='four_png_max'")
    (out / f'run_{fighter}_p1.ps1').write_text(runner)
print('Prepared8PNG total cap; unchanged physical controllers')
