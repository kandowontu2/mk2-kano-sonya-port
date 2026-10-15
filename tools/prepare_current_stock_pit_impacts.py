"""Two late Pit checkpoints, unchanged earned native routes, no PCM."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_stock_pit_impact_preparation'
assert not out.exists();out.mkdir()
for name in ('kunglao','jax_sonya_p2'):
    base=sync.ROOT/('audit_current_native_pit_stock_'+name+'_preparation')
    source=(base/'stage.lua').read_text()
    if name=='jax_sonya_p2':
        source=source[:source.index('\nlocal visual_count=0')]
    source+='''
local impact_image=false
emu.register_frame_done(function()
 if action and frame-action==260 then
  assert(not impact_image);impact_image=true
  screen:snapshot('stock_pit_impact_260.png')
  log('IMPACT_IMAGE','age=260 count=1')
 end
end)
'''
    lua=out/(name+'.lua');lua.write_text(source)
    runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/'+name+'.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_native_pit_stock_'+name+'_runtime','audit_current_stock_pit_impact_'+name+'_runtime')
    if name=='jax_sonya_p2':
        runner=runner.replace('120KB','60KB').replace('two_png_max120KiB_no_pcm','one_png_max60KiB_no_pcm')
    else:
        marker=' if($taskLimitReason){';assert runner.count(marker)==1
        runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object Length -Sum).Sum\n if($taskMediaBytes -gt 60KB){$taskLimitReason='media_limit'}\n"+marker)
        runner=runner.replace("rawMedia='none'","rawMedia='one_png_max60KiB_no_pcm'")
    (out/(name+'.ps1')).write_text(runner)
print('Prepared2impactPNG totalmax120KiB; unchanged earned7matchroutes,caps90sec/320MiB,noPCM')
