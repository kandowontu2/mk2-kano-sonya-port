"""Three bounded acid checkpoints, continuous physical held buttons unchanged."""
import verify_native_source_sync as sync

sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_gate_hold_preparation'
out=sync.ROOT/'audit_current_native_deadpool_visual_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()+'''
local visual_count=0
emu.register_frame_done(function()
 if not action then return end
 local age=frame-action
 if age==60 or age==120 or age==200 then
  assert(visual_count<3)
  screen:snapshot('acid_'..age..'.png');visual_count=visual_count+1
  log('VISUAL_SAVED','age='..age..' count='..visual_count)
 end
end)
'''
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_deadpool_gate_hold_kano_p1_runtime','audit_current_native_deadpool_visual_kano_p1_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object -Property Length -Sum).Sum\n if($taskMediaBytes -gt 512KB){$taskLimitReason='media_limit'}\n"+marker)
runner=runner.replace("rawMedia='none'","rawMedia='three_bounded_png_max512KiB'")
(out/'run.ps1').write_text(runner)
print('Prepared acid screenshots60/120/200, total cap512KiB')
