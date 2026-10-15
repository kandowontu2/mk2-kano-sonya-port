"""Four bounded rendered samples per P1 secondary action; no gameplay changes."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_secondary_finishers_preparation'
out=sync.ROOT/'audit_bounded_secondary_visual_samples_preparation'
assert not out.exists()
out.mkdir()
source=(old/'finishers.lua').read_text()
source+='''
local visual_count=0
emu.register_frame_done(function()
 if not action_start then return end
 local age=frame-action_start
 local label=({[30]='startup',[100]='active',[180]='late'})[age]
 if wrap and frame-wrap==100 then label='post_wrap' end
 if label then
  visual_count=visual_count+1;assert(visual_count<=4)
  screen:snapshot('secondary_'..label..'.png')
  log('VISUAL_SAVED','sample='..label..' count='..visual_count)
 end
end)
'''
lua=out/'visuals.lua'
lua.write_text(source)
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}_p1.ps1').read_text()
    runner=runner.replace(old.name+'/finishers.lua',out.name+'/visuals.lua').replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_secondary_finisher_{fighter}_p1_runtime',f'audit_bounded_secondary_visual_{fighter}_p1_runtime')
    runner=runner.replace("rawMedia='none'","rawMedia='bounded_four_png'")
    (out/f'run_{fighter}.ps1').write_text(runner)
