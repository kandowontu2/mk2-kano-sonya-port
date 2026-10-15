"""Earned SonyaP2/stockJax Pit with sparse audio and exactly two images."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_pit_audio_preparation'
out=sync.ROOT/'audit_current_native_pit_stock_jax_sonya_p2_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old='local victim_id=id==17 and 18 or 17';assert source.count(old)==1
source=source.replace(old,'local victim_id=11 -- actual stock Jax selection')
source+='''
local visual_count=0
emu.register_frame_done(function()
 if not action then return end
 local age=frame-action
 if age==15 or age==120 then
  assert(visual_count<2)
  screen:snapshot('stock_pit_'..age..'.png');visual_count=visual_count+1
  log('VISUAL_SAVED','age='..age..' count='..visual_count)
 end
end)
'''
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(sync.ROOT/'audit_current_native_pit_sonya_audio_preparation/run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_native_pit_audio_sonya_p2_runtime','audit_current_native_pit_stock_jax_sonya_p2_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object Length -Sum).Sum\n if($taskMediaBytes -gt 120KB){$taskLimitReason='media_limit'}\n"+marker)
runner=runner.replace("rawMedia='none'","rawMedia='two_png_max120KiB_no_pcm'")
(out/'run.ps1').write_text(runner)
print('Prepared nativeSonyaP2/stockJax11Pit,7earnedmatches,2PNGmax120KiB,noPCM,90sec/320MiB')
