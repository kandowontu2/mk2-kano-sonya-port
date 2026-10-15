"""Unchanged physical controller; sparse native paired HP/action/spacing trace."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_subzero_hk_ring_preparation'
out=sync.ROOT/'audit_current_sonya_p2_subzero_contact_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='for n,slot in ipairs(slots)do'
assert source.count(marker)==1
extra="""for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do
 taps[#taps+1]=p:install_write_tap(observed_hp,observed_hp+15,'passive actual Sonya Subzero damage',function(at,data,mask)
  if at~=observed_hp or mask~=0xffff or p:read_u16(0x01061b30)~=1 then return end
  local before,after=p:read_u16(at),data&0xffff
  if after>=before or before>161 then return end
  local h,c=sample(2),sample(1)
  if not h or not c or h.id~=18 or h.roster~=18 or c.id~=8 or c.roster~=8 or h.owner~=h.actor or c.owner~=c.actor then return end
  local caller=cpu.A13.value
  local creator=caller>=0x01000000 and caller<0x01100000 and p:read_u32(caller+0x230) or 0
  log('SONYA_SUBZERO_DAMAGE',string.format('victim_slot=%d at=%08X before=%d after=%d pc=%08X a8=%08X a13=%08X creator=%08X human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X ids=8,18 human_action=%d cpu_action=%d gap=%d height=%d cpu_height=%d hardware=%04X',observed_slot,at,before,after,cpu.PC.value,cpu.A8.value,caller,creator,h.actor,h.main,c.actor,c.main,h.action,c.action,math.abs(h.x-c.x),h.floor-h.y,c.floor-c.y,p:read_u16(0x01600000)))
 end)
end
"""
source=source.replace(marker,extra+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_subzero_hk_ring_runtime','audit_current_sonya_p2_subzero_contact_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Unchanged SonyaP2 HK/ring inputs;passive HP ownership/spacing trace;30k/90sec/320MiB/10MiB/no media')
