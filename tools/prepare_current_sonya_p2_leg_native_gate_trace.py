"""Unchanged physical controls, passive parser/scheduler checkpoints only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_leg_attack_guard_preparation'
out=sync.ROOT/'audit_current_sonya_p2_leg_native_gate_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='-- Observe actual own special entries independently of intended button plans.'
extra="""-- Passive fetch checkpoints; never modify opcode, registers or guest state.
for _,checkpoint in ipairs({0xfff80000,0xff8771f0,0xff877270,0xff8772f0,0xff877340,0xff877350,0xff877420})do
 local address=checkpoint
 taps[#taps+1]=p:install_read_tap(address,address+15,'passive Sonya input gate',function(at)
  if at~=address or p:read_u16(0x01061b30)~=3 then return end
  local h,c=sample(2),sample(1)
  if not h or not c or h.id~=18 or h.roster~=18 or c.id~=0 or c.roster~=0 or cpu.A8.value~=h.actor then return end
  local task=cpu.A13.value
  local link=valid(task) and p:read_u32(task+0x290) or 0
  log('SONYA_NATIVE_GATE',string.format('checkpoint=%08X pc=%08X a0=%08X a4=%08X a7=%08X a8=%08X a13=%08X task_link=%08X human_actor=%08X human_main=%08X human_action=%d flags=%04X height=%d hardware=%04X lowhardware=%04X gap=%d',address,cpu.PC.value,cpu.A0.value,cpu.A4.value,cpu.A7.value,cpu.A8.value,task,link,h.actor,h.main,h.action,h.flags,h.floor-h.y,p:read_u16(0x01600000),p:read_u16(0x01600020),math.abs(h.x-c.x)))
 end)
end
"""
assert source.count(marker)==1
source=source.replace(marker,extra+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_leg_attack_guard_runtime','audit_current_sonya_p2_leg_native_gate_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared unchanged inputs plus passive native gate trace;90sec/320MiB/10MiB/no media')
