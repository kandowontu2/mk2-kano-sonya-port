"""Observe genuine earned Sonya round wins, physical controls only."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_p2_delayed_campaign_preparation'
out=sync.ROOT/'audit_current_sonya_native_winner_preparation'
assert not out.exists()
source=(old/'campaign.lua').read_text()
source=source.replace('frame>=12000','frame>=7000').replace('maximum_fields=12000','maximum_fields=7000')
source+='''
local winner_tap=p:install_read_tap(0xffff3620,0xffff365f,'own_winner_table',function(at,data,mask)
 if at==0xffff3620 or at==0xffff3630 or at==0xffff3640 or at==0xffff3650 then
  log('WINNER_TABLE',string.format('at=%08X data=%04X mask=%04X pc=%08X',at,data&0xffff,mask&0xffff,cpu.PC.value))
 end
end)
emu.register_frame_done(function()
 local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 if a>=0x01000000 and a<0x01100000 and m>=0x01000000 and m<0x01100000 and
 p:read_u16(0x01060e50)==18 and p:read_u16(0x01060ec0)>0 and p:read_u16(0x010602f0)==0 then
  log('WINNER_POSE',string.format('actor=%08X main=%08X owner=%08X id=%d roster=18 hp=%d cpu_hp=0 pose=%08X action=%d mode=%d stage=%d',
   a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(0x01060ec0),p:read_u32(a+0x1d0),p:read_u16(m+0x1f0),p:read_u16(0x010601d0),p:read_u16(0x01061b30)))
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(sync.ROOT/'audit_current_sonya_p2_leg_campaign_preparation/run.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_leg_campaign_runtime','audit_current_sonya_native_winner_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared7000fields native earned-win read-only observer, unchanged caps, no media')
