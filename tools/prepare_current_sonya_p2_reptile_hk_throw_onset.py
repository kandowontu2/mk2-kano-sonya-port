"""Unchanged best HK/ring inputs; passive native throw start, not landing gap."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_hk_ring_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_hk_throw_onset_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='   local gap=math.abs(human.x-other.x)\n'
assert source.count(marker)==1
extra="""   if other.roster==9 and stage==5 then
    if not rt_taps[other.main] then
     local observed_main=other.main
     rt_taps[observed_main]=p:install_write_tap(observed_main+0x1f0,observed_main+0x1ff,'passive Reptile throw initiation',function(at,data,mask)
      if mask~=0xffff or data&0xffff~=1287 or p:read_u16(0x01061b30)~=5 then return end
      local h,c=sample(2),sample(1)
      if not h or not c or h.id~=18 or h.roster~=18 or c.id~=9 or c.roster~=9 or c.main~=observed_main or c.owner~=c.actor or h.owner~=h.actor then return end
      log('REPTILE_THROW_START',string.format('pc=%08X at=%08X a8=%08X a13=%08X cpu_actor=%08X cpu_main=%08X human_actor=%08X human_main=%08X gap=%d height=%d cpu_height=%d action=%d flags=%04X cpu_flags=%04X hardware=%04X lowhardware=%04X kick_age=%d ring_age=%d health=%d,%d',cpu.PC.value,at,cpu.A8.value,cpu.A13.value,c.actor,c.main,h.actor,h.main,math.abs(h.x-c.x),h.floor-h.y,c.floor-c.y,h.action,h.flags,c.flags,p:read_u16(0x01600000),p:read_u16(0x01600020),sh_start and frame-sh_start or -1,sr_start and frame-sr_start or -1,h.hp,c.hp))
     end)
     taps[#taps+1]=rt_taps[observed_main]
    end
   end
"""
source='local rt_taps={}\n'+source.replace(marker,marker+extra)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_hk_ring_runtime','audit_current_sonya_p2_reptile_hk_throw_onset_runtime')
(out/'run.ps1').write_text(runner)
print('Unchanged HK/ring controller plus passive throw onset;90sec/320MiB/10MiB/no media')
