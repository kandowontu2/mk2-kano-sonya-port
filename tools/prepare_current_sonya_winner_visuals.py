"""Two tiny earned Sonya winner checkpoints, no recording."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_native_winner_preparation'
out=sync.ROOT/'audit_current_sonya_winner_visual_preparation'
assert not out.exists()
source=(old/'campaign.lua').read_text()
source=source.replace('frame>=7000','frame>=5400').replace('maximum_fields=7000','maximum_fields=5400')
source+='''
local winner_visuals=0
emu.register_frame_done(function()
 if frame==4979 or frame==5020 then
  assert(winner_visuals<2)
  machine.screens[':screen']:snapshot('winner_'..frame..'.png')
  winner_visuals=winner_visuals+1
  log('VISUAL_SAVED','checkpoint='..frame..' count='..winner_visuals)
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_native_winner_runtime','audit_current_sonya_winner_visual_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object -Property Length -Sum).Sum\n if($taskMediaBytes -gt 512KB){$taskLimitReason='media_limit'}\n"+marker)
runner=runner.replace("rawMedia='none'","rawMedia='two_bounded_png_max512KiB'")
(out/'run.ps1').write_text(runner)
print('Prepared5400fields, two screenshots max512KiB, existing90sec/320MiB/10MiB limits')
