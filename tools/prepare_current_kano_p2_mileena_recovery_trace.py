"""Passive native upper entry and own flag-bit4 onset, unchanged controls."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_crouch_spacing_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_recovery_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   if other.roster==5 and stage==10 then\n"
assert source.count(marker)==1
extra="""    mr_taps=mr_taps or {}
    if not mr_taps[human.main] then
     local observed=human.main
     mr_taps[observed]=p:install_write_tap(observed+0x210,observed+0x21f,'passive own bit4 onset',function(at,data,mask)
      if mask~=0xffff or data&4==0 or p:read_u16(at)&4~=0 or p:read_u16(0x01061b30)~=10 then return end
      local h,c=sample(2),sample(1)
      if not h or not c or h.id~=17 or h.roster~=17 or c.id~=5 or c.roster~=5 or h.main~=observed or h.owner~=h.actor or c.owner~=c.actor then return end
      log('MILEENA_RECOVERY_ONSET',string.format('at=%08X before=%04X after=%04X pc=%08X a8=%08X a13=%08X actor=%08X main=%08X cpu_actor=%08X cpu_main=%08X action=%d cpu_action=%d gap=%d height=%d hardware=%04X health=%d,%d',at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value,h.actor,h.main,c.actor,c.main,h.action,c.action,math.abs(h.x-c.x),h.floor-h.y,p:read_u16(0x01600000),h.hp,c.hp))
     end)
     taps[#taps+1]=mr_taps[observed]
    end
"""
source=source.replace(marker,marker+extra)
marker2='for n,slot in ipairs(slots)do'
assert source.count(marker2)==1
tap="""taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'passive actual Mileena fight upper entry',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=0xff870dd0 or p:read_u16(0x01061b30)~=10 then return end
 local h,c=sample(2),sample(1)
 if not h or not c or h.id~=17 or h.roster~=17 or c.id~=5 or c.roster~=5 or h.owner~=h.actor or cpu.A8.value~=h.actor or cpu.A13.value~=h.main then return end
 log('MILEENA_UPPER_ENTRY',string.format('actor=%08X main=%08X owner=%08X a8=%08X a13=%08X pc=%08X gap=%d height=%d action=%d flags=%04X native_counter=%d hardware=%04X health=%d,%d',h.actor,h.main,h.owner,cpu.A8.value,cpu.A13.value,cpu.PC.value,math.abs(h.x-c.x),h.floor-h.y,h.action,h.flags,p:read_u16(h.main+0x220),p:read_u16(0x01600000),h.hp,c.hp))
end)
"""
source=source.replace(marker2,tap+marker2)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_crouch_spacing_runtime','audit_current_kano_p2_mileena_recovery_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Unchanged physical controller;passive upper/flag onset;90sec/320MiB/10MiB/no media')
