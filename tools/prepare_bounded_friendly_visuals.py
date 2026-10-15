"""Three PNG maximum per action; controller policy stays unchanged."""
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_friendly_visuals_preparation'
assert not out.exists()
out.mkdir()
for kind in ('friendship','babality'):
    folder='friendships' if kind=='friendship' else 'babalities'
    old=sync.ROOT/f'audit_bounded_current_{folder}_preparation'
    filename=folder+'.lua'
    source=(old/filename).read_text()
    source+='''
local bounded_visual_count=0
emu.register_frame_done(function()
 if not action or not window then return end
 local label=({[80]='active_early',[160]='active_late'})[frame-action]
 if frame-window==700 then label='post_scene' end
 if label then
  bounded_visual_count=bounded_visual_count+1;assert(bounded_visual_count<=3)
  screen:snapshot('friendly_'..label..'.png')
  log('VISUAL_SAVED','sample='..label..' count='..bounded_visual_count)
 end
end)
'''
    lua=out/(kind+'.lua')
    lua.write_text(source)
    for fighter in ('kano','sonya'):
        runner=(old/f'run_{fighter}_p1.ps1').read_text()
        runner=runner.replace(old.name+'/'+filename,out.name+'/'+lua.name)
        runner=runner.replace(sync.sha(old/filename),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_current_{kind}_{fighter}_p1_runtime',f'audit_bounded_visual_{kind}_{fighter}_p1_runtime')
        runner=runner.replace("rawMedia='none'","rawMedia='bounded_three_png'")
        (out/f'run_{kind}_{fighter}.ps1').write_text(runner)
print('Prepared four runs, three PNG cap each, twelve total')
