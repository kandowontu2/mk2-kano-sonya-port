"""Four bounded native screenshots, unchanged physical earned-finisher controller."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_morphed_victims_secondary_preparation'
out=sync.ROOT/'audit_morphed_sonya_orb_visual_preparation';assert not out.exists()
source=(old/'finishers.lua').read_text()
source+='''
local visual_count=0
emu.register_frame_done(function()
 if not action_start then return end
 local age=frame-action_start
 if age==155 or age==185 then
  assert(visual_count<2)
  screen:snapshot('orb_'..age..'.png');visual_count=visual_count+1
  log('VISUAL_SAVED','age='..age..' count='..visual_count)
 end
end)
'''
out.mkdir();lua=out/'finishers.lua';lua.write_text(source)
for side in (1,2):
    runner=(old/f'run_sonya_sonya_p{side}.ps1').read_text()
    runner=runner.replace(old.name+'/finishers.lua',out.name+'/finishers.lua').replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_morphed_victim_secondary_sonya_sonya_p{side}_runtime',f'audit_morphed_sonya_orb_visual_p{side}_runtime')
    marker=" if($taskLimitReason){";assert runner.count(marker)==1
    runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object -Property Length -Sum).Sum\n if($taskMediaBytes -gt 512KB){$taskLimitReason='media_limit'}\n"+marker)
    runner=runner.replace("rawMedia='none'","rawMedia='two_bounded_png_max512KiB'")
    (out/f'run_p{side}.ps1').write_text(runner)
print('Prepared two cold runs, two screenshots each; combined1MiB cap')
