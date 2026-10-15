"""One discrete native impact image, same earned controller,60KiB cap."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_stock_pit_initialized_selector_preparation'
out=sync.ROOT/'audit_current_stock_pit_sonya_impact_preparation'
assert not out.exists();out.mkdir()
source=(base/'sonya_p1_kitana.lua').read_text()+r'''
local impact_saved=false
emu.register_frame_done(function()
 if action and frame-action==260 then
  assert(not impact_saved);impact_saved=true
  screen:snapshot('sonya_p1_stock_pit_260.png')
  log('IMPACT_IMAGE','age=260 count=1')
 end
end)
'''
lua=out/'stage.lua';lua.write_text(source)
runner=(base/'sonya_p1_kitana.ps1').read_text().replace(base.name+'/sonya_p1_kitana.lua',out.name+'/stage.lua').replace(sync.sha(base/'sonya_p1_kitana.lua'),sync.sha(lua)).replace('audit_current_stock_pit_initialized_selector_sonya_p1_kitana_runtime','audit_current_stock_pit_sonya_impact_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object Length -Sum).Sum\n if($taskMediaBytes -gt 60KB){$taskLimitReason='media_limit'}\n"+marker)
runner=runner.replace("rawMedia='none'","rawMedia='one_png_max60KiB_no_pcm'")
(out/'run.ps1').write_text(runner)
print('Prepared one impact screenshot,max60KiB,90sec/320MiB')
