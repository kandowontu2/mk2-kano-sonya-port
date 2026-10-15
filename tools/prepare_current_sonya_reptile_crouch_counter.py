"""Physical crouch timing correction; actual action263 observer, no writes."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_reptile_uppercut_preparation'
out=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_preparation';assert not out.exists()
source=(old/'campaign.lua').read_text()
before="""   elseif strategy=='uppercut' then
    if gap>65 then press(human.x<other.x and'Right'or'Left')
    else press('Down');if frame%22<4 then press('High Punch')end end
"""
after="""   elseif strategy=='uppercut' then
    if gap>105 then press(human.x<other.x and'Right'or'Left')
    else
     press('Down')
     if human.action==770 and gap<95 and frame-last_uppercut>=22 then
      press('High Punch');last_uppercut=frame
      log('COUNTER_ATTEMPT',string.format('native_action=%d gap=%d cpu_id=%d hp=%d',human.action,gap,other.id,human.hp))
     end
    end
"""
assert source.count(before)==1;source=source.replace(before,after)
source+='''
local previous_counter_action=-1
emu.register_frame_done(function()
 local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 if a<0x01000000 or a>=0x01100000 or m<0x01000000 or m>=0x01100000 then previous_counter_action=-1;return end
 local action=p:read_u16(m+0x1f0)
 if action==263 and previous_counter_action~=263 and p:read_u16(0x01060e50)==18 and p:read_u16(0x01060280)==9 then
  log('COUNTER_ACTIVATION',string.format('actor=%08X main=%08X owner=%08X id=%d roster=18 native_action=263 hp=%d cpu_hp=%d stage=%d',
   a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(0x01060ec0),p:read_u16(0x010602f0),p:read_u16(0x01061b30)))
 end
 previous_counter_action=action
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text().replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_reptile_uppercut_runtime','audit_current_sonya_reptile_crouch_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared12000fields: real crouch action770 before HP, observe actual uppercut263; no media')
