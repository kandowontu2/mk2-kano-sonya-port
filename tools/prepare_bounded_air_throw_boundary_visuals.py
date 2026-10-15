"""Eight PNG cap: Kano and stock Jax, Sonya victim, both physical edges."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_air_throw_boundary_preparation'
out=sync.ROOT/'audit_bounded_air_throw_boundary_visuals_preparation'
assert not out.exists()
base=old/'air_throw.lua'
source=base.read_text()+'''
local edge_visual_count=0
emu.register_frame_done(function()
 local label=marks[frame]
 if label=='air_1_phase56'or label=='air_1_recovered'then
  assert(edge_visual_count<2,'TwoPNG per context')
  screen:snapshot(label..'.png');edge_visual_count=edge_visual_count+1
  log('VISUAL_SAVED','label='..label..' count='..edge_visual_count)
 end
end)
'''
out.mkdir()
target=out/'air_throw.lua'
target.write_text(source)
for thrower in ('kano','jax'):
    for direction in ('left','right'):
        runner=(old/f'run_{direction}_p1.ps1').read_text()
        runner=runner.replace(old.name+'/air_throw.lua',out.name+'/air_throw.lua').replace(sync.sha(base),sync.sha(target))
        if thrower=='jax':
            runner=runner.replace("SPECIAL_MOVE='knife'","SPECIAL_MOVE='ring'")
            runner=runner.replace("SPECIAL_VICTIM='sonya'","SPECIAL_VICTIM='jax'")
        runner=runner.replace(f'audit_bounded_air_throw_boundary_{direction}_p1_runtime',
            f'audit_bounded_air_throw_boundary_visual_{thrower}_{direction}_runtime')
        runner=runner.replace("rawMedia='none'","rawMedia='two_png_max'")
        (out/f'run_{thrower}_{direction}.ps1').write_text(runner)
print('Prepared four contexts, eight PNG total maximum')
