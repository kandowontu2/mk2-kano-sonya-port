"""Actual crouch lead-in and passive native uppercut entry observation."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_native_uppercut_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_crouch_lead_upper_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local uc_down,uc_pulse,uc_retry=nil,nil,-1000\nlocal uc_taps={}\n'+source
start=source.index("   elseif fighter=='sonya' and side==2 and other.roster==3 then\n")
end=source.index('   elseif leg_tactic',start)
branch="""   elseif fighter=='sonya' and side==2 and other.roster==3 then
    if not uc_taps[human.main] then
     local at=human.main+0x1f0
     uc_taps[human.main]=p:install_write_tap(at,at+15,'physical upper entry observer',function(address,data,mask)
      if data&0xffff~=263 or cpu.PC.value~=0xff870dd0 then return end
      local h,c=sample(side),sample(opponent)
      if h.main+0x1f0~=address or h.id~=18 or c.roster~=3 then return end
      log('BARAKA_NATIVE_UPPER',string.format('pc=%08X actor=%08X main=%08X id=%d gap=%d height=%d hardware=%04X',cpu.PC.value,h.actor,h.main,h.id,math.abs(h.x-c.x),h.floor-h.y,p:read_u16(0x01600000)))
     end)
    end
    if gap>105 then
     uc_down=nil;uc_pulse=nil;press(human.x<other.x and 'Right' or 'Left')
    else
     uc_down=uc_down or frame;press('Down')
     if uc_pulse and frame-uc_pulse<3 then press('High Punch')
     elseif frame-uc_down>=4 and gap<90 and human.floor-human.y==0 and
       (human.action==770 or human.action==1793) and human.flags&0x1c==0 and frame-uc_retry>=26 then
      uc_pulse=frame;uc_retry=frame;press('High Punch')
     end
    end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_native_uppercut_runtime','audit_current_sonya_p2_baraka_crouch_lead_upper_runtime')
(out/'run.ps1').write_text(runner)
print('Crouch-lead physical upper:90sec/320MiB/10MiB/no media, native action263 passive tap')
