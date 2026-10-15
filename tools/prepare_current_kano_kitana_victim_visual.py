"""One discrete actual stock-counter victim checkpoint, no forced state."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kitana_confirmed_jump_preparation'
out=sync.ROOT/'audit_current_kano_kitana_victim_visual_preparation'
assert not out.exists();out.mkdir()
source=(base/'campaign.lua').read_text()+r'''
local victim_image=false
emu.register_frame_done(function()
 if victim_image or p:read_u16(0x01061b30)~=3 or p:read_u16(0x010601d0)~=2 then return end
 local own,other=sample(side),sample(opponent)
 if own and other and own.id==17 and own.roster==17 and other.id==4 and own.action==1556 and own.floor-own.y>20 then
  victim_image=true;screen:snapshot('kano_kitana_counter_victim.png')
  log('VICTIM_IMAGE',string.format('action=%d own_id=%d cpu_id=%d height=%d pose=%08X',own.action,own.id,other.id,own.floor-own.y,own.pose))
 end
end)
'''
lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kitana_confirmed_jump_runtime','audit_current_kano_kitana_victim_visual_runtime')
marker=' if($taskLimitReason){';assert runner.count(marker)==1
runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object Length -Sum).Sum\n if($taskMediaBytes -gt 60KB){$taskLimitReason='media_limit'}\n"+marker)
runner=runner.replace("rawMedia='none'","rawMedia='one_png_max60KiB_no_pcm'")
(out/'run.ps1').write_text(runner)
print('Prepared one actual victim screenshot,60KiB cap,no PCM,90sec/320MiB')
