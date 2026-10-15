"""One age120 PNG per existing earned Tomb route; no controller changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_stock_tomb_other_sides_preparation'
out=sync.ROOT/'audit_current_stock_tomb_other_sides_visual_preparation'
assert not out.exists();out.mkdir()
for case in ('sonya_p1_kitana','kano_p2_subzero'):
    source=(base/(case+'.lua')).read_text()
    assert ':write_' not in source and ':snapshot(' not in source
    source+=r'''
local visual_count=0
emu.register_frame_done(function()
 if not action or frame-action~=120 then return end
 assert(visual_count==0)
 screen:snapshot('stock_tomb_120.png');visual_count=1
 log('VISUAL_SAVED','age=120 count=1')
end)
'''
    lua=out/(case+'.lua');lua.write_text(source)
    runner=(base/(case+'.ps1')).read_text().replace(base.name+'/'+case+'.lua',out.name+'/'+case+'.lua').replace(sync.sha(base/(case+'.lua')),sync.sha(lua))
    runner=runner.replace('audit_current_stock_tomb_'+case+'_runtime','audit_current_stock_tomb_other_sides_visual_'+case+'_runtime')
    marker=' if($taskLimitReason){';assert runner.count(marker)==1
    runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object Length -Sum).Sum\n if($taskMediaBytes -gt 60KB){$taskLimitReason='media_limit'}\n"+marker)
    runner=runner.replace("rawMedia='none'","rawMedia='one_png_max60KiB'")
    (out/(case+'.ps1')).write_text(runner)
print('Prepared two PNG totalmax120KiB, unchanged physical Tomb inputs')
