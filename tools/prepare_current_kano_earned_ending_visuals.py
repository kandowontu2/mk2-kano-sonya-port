"""Four bounded native ending/return PNGs; proven physical route unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_backjump_charge_counter_preparation'
out=sync.ROOT/'audit_current_kano_earned_ending_visuals_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source+='''
local ending_visual_count=0
local ending_visual_frames={[73800]='ending_page1.png',[74700]='ending_page2.png',[75180]='ending_return.png',[75400]='after_ending.png'}
emu.register_frame_done(function()
 local name=ending_visual_frames[frame]
 if name then
  assert(ending and ending_visual_count<4)
  screen:snapshot(name);ending_visual_count=ending_visual_count+1
  log('ENDING_VISUAL_SAVED','name='..name..' count='..ending_visual_count)
 end
end)
'''
assert ':write_' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_backjump_charge_counter_runtime','audit_current_kano_earned_ending_visuals_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object Length -Sum).Sum\n if($taskMediaBytes -gt 512KB){$taskLimitReason='media_limit'}\n"+marker).replace("rawMedia='none'","rawMedia='four_png_max512KiB'")
(out/'run.ps1').write_text(runner)
print('Exactly4PNG/512KiB; unchangedearnedroute;180sec/320MiB/10MiB')
