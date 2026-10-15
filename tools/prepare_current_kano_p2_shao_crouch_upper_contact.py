"""90sec controller-only Shao upper contact test; nativeHP writes observed passively."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_approved_180s_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_crouch_upper_contact_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local su_down,su_pulse,su_retry=nil,nil,-1000\nlocal su_hp_taps=nil\n'+source
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
branch="""    if stage==16 then
     if not su_hp_taps then
      su_hp_taps={}
      for victim,slot in ipairs(slots)do
       local address=slot.hp
       su_hp_taps[#su_hp_taps+1]=p:install_write_tap(address,address+15,'passive Shao upper nativeHP',function(at,data,mask)
        if at~=address or mask~=0xffff or p:read_u16(0x01061b30)~=16 or cpu.PC.value~=0xff836700 then return end
        local before,after=p:read_u16(at),data&0xffff
        if after>=before or before>161 then return end
        local h,c=sample(2),sample(1)
        if not h or not c or h.id~=17 or h.roster~=17 or c.id~=13 or c.roster~=13 or h.owner~=h.actor or c.owner~=c.actor then return end
        log('SHAO_UPPER_DAMAGE',string.format('victim_slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X human_action=%d cpu_action=%d gap=%d height=%d cpu_height=%d',victim,before,after,cpu.PC.value,cpu.A8.value,cpu.A13.value,h.actor,h.main,c.actor,c.main,h.action,c.action,math.abs(h.x-c.x),h.floor-h.y,c.floor-c.y))
       end)
      end
     end
     if gap>80 then
      su_down=nil;su_pulse=nil;press(forward)
     else
      su_down=su_down or frame;press('Down')
      if su_pulse and frame-su_pulse<3 then press('High Punch')
      elseif can_crouch and frame-su_down>=4 and frame-su_retry>=26 then
       su_pulse=frame;su_retry=frame;decision('shao_crouch_upper_attempt');press('High Punch')
      end
     end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_approved_180s_runtime','audit_current_kano_p2_shao_crouch_upper_contact_runtime').replace('TotalSeconds -gt 180','TotalSeconds -gt 90')
(out/'run.ps1').write_text(runner)
print('Shao only crouchlead4/HP3/retry26/gap80;90sec/320MiB/10MiB/no media/nativeHP read-only')
