"""Passive original taunt entry/tail observation with unchanged inputs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_recovered_knife_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_taunt_observer_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source+='''
for _,entry in ipairs({0xff9d0fd0,0xff9d12f0})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'passive original Shao taunt',function(at)
  if at~=entry or cpu.PC.value~=entry+16 or p:read_u16(0x01061b30)~=16 then return end
  local h,c=sample(2),sample(1)
  if not h or not c or h.id~=17 or c.id~=13 or c.owner~=c.actor or cpu.A8.value~=c.actor or cpu.A13.value~=c.main then return end
  log('SHAO_TAUNT_TRACE',string.format('entry=%08X pc=%08X human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X human_id=%d cpu_id=%d human_action=%d cpu_action=%d cpu_flags=%04X health=%d,%d gap=%d',entry,cpu.PC.value,h.actor,h.main,c.actor,c.main,h.id,c.id,h.action,c.action,c.flags,h.hp,c.hp,math.abs(h.x-c.x)))
 end)
end
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_recovered_knife_runtime','audit_current_kano_p2_shao_taunt_observer_runtime')
(out/'run.ps1').write_text(runner)
print('Passiveoriginaltaunttiming;unchangedinputs;180sec/320MiB/10MiB/no media')
