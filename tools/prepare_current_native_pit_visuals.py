"""Bounded actual Pit checkpoints on the proven physical earned route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_pit_longkick_preparation'
out=sync.ROOT/'audit_current_native_pit_visual_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
source+='''
local visual_count=0
emu.register_frame_done(function()
 if not action then return end
 local age=frame-action
 if age==15 or age==120 or age==600 then
  assert(visual_count<3)
  screen:snapshot('pit_'..age..'.png');visual_count=visual_count+1
  log('VISUAL_SAVED','age='..age..' count='..visual_count)
 end
end)
'''
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_pit_longkick_kano_p1_runtime','audit_current_native_pit_visual_kano_p1_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object -Property Length -Sum).Sum\n if($taskMediaBytes -gt 512KB){$taskLimitReason='media_limit'}\n"+marker)
runner=runner.replace("rawMedia='none'","rawMedia='three_bounded_png_max512KiB'")
(out/'run.ps1').write_text(runner)
print('Prepared three Pit checkpoints max512KiB; unchanged native controller')
