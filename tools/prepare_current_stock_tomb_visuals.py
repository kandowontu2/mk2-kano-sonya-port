"""Exactly four small snapshots across two already-earned stock-victim cases."""
import verify_native_source_sync as sync
sync.verify()
cases=('kunglao','jax_sonya_p2')
out=sync.ROOT/'audit_current_stock_tomb_visual_preparation'
assert not out.exists();out.mkdir()
for case in cases:
    base=sync.ROOT/('audit_current_native_tomb_stock_'+case+'_preparation')
    source=(base/'stage.lua').read_text()+'''
local visual_count=0
emu.register_frame_done(function()
 if not action then return end
 local age=frame-action
 if age==120 or age==600 then
  assert(visual_count<2)
  screen:snapshot('stock_tomb_'..age..'.png');visual_count=visual_count+1
  log('VISUAL_SAVED','age='..age..' count='..visual_count)
 end
end)
'''
    lua=out/(case+'.lua');lua.write_text(source)
    runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/'+case+'.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
    runner=runner.replace('audit_current_native_tomb_stock_'+case+'_runtime','audit_current_stock_tomb_visual_'+case+'_runtime')
    marker=' if($taskLimitReason){';assert runner.count(marker)==1
    runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object Length -Sum).Sum\n if($taskMediaBytes -gt 120KB){$taskLimitReason='media_limit'}\n"+marker)
    runner=runner.replace("rawMedia='none'","rawMedia='two_png_max120KiB'")
    (out/(case+'.ps1')).write_text(runner)
print('Prepared4PNG totalmax240KiB,unchanged earned native Tomb inputs')
