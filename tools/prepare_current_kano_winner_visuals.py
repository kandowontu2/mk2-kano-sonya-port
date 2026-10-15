"""Two bounded current Kano earned-win screenshots."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_kano_native_winner_preparation'
out=sync.ROOT/'audit_current_kano_winner_visual_preparation'
assert not out.exists()
source=(old/'campaign.lua').read_text().replace('frame>=10200','frame>=9100').replace('maximum_fields=10200','maximum_fields=9100')
source+='''
local winner_visuals=0
emu.register_frame_done(function()
 if frame==8782 or frame==8823 then
  assert(winner_visuals<2)
  screen:snapshot('winner_'..frame..'.png')
  winner_visuals=winner_visuals+1
  log('VISUAL_SAVED','checkpoint='..frame..' count='..winner_visuals)
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text().replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_kano_native_winner_runtime','audit_current_kano_winner_visual_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object -Property Length -Sum).Sum\n if($taskMediaBytes -gt 512KB){$taskLimitReason='media_limit'}\n"+marker)
runner=runner.replace("rawMedia='none'","rawMedia='two_bounded_png_max512KiB'")
(out/'run.ps1').write_text(runner)
print('Prepared9100fields, two bounded PNGs max512KiB, normal caps retained')
