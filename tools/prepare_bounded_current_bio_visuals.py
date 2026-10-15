"""Four bounded natural biography screenshots; same scalar cold observer."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_attract_long_preparation'
out=sync.ROOT/'audit_bounded_current_bio_visual_preparation';assert not out.exists()
source=(old/'attract.lua').read_text()
marker="local frame,taps=0,{}";assert source.count(marker)==1
source=source.replace(marker,marker+"\nlocal visual_marks,visual_count={},0")
marker=" log('COUNTER',string.format('id=%d pc=%08X mask=%04X',data&0xffff,cpu.PC.value,mask))"
assert source.count(marker)==1
source=source.replace(marker,marker+'''
 local id=data&0xffff
 if cpu.PC.value==0xff84a460 and(id==17 or id==18)then
  visual_marks[frame+100]=tostring(id)..'_early'
  visual_marks[frame+1100]=tostring(id)..'_late'
 end
''')
source+='''
emu.register_frame_done(function()
 local label=visual_marks[frame]
 if label then
  assert(visual_count<4)
  machine.screens[':screen']:snapshot('bio_'..label..'.png')
  visual_count=visual_count+1;visual_marks[frame]=nil
  log('VISUAL_SAVED','label='..label..' count='..visual_count)
 end
end)
'''
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(old/'attract.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_current_attract_long_runtime','audit_bounded_current_bio_visual_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object -Property Length -Sum).Sum\n if($taskMediaBytes -gt 1MB){$taskLimitReason='media_limit'}\n"+marker)
runner=runner.replace("rawMedia='none'","rawMedia='four_bounded_png_max1MiB'")
(out/'run.ps1').write_text(runner)
print('Prepared four native bio checkpoints, total1MiB cap; original resource caps retained')
