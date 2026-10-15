"""Normal paid challenger during actual CPU Sonya launch audio; passive scalars."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_native_start_preparation'
out=sync.ROOT/'audit_current_native_battle_audio_join_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text().replace('frame>=30000','frame>=12000').replace('maximum_fields=30000','maximum_fields=12000')
source+='''
local join_start,join_selection=nil,nil
local join_saved,join_channels={},{}
local join_coin=manager.machine.ioport.ports[':IN1'].fields['Coin 1']
local join_button=manager.machine.ioport.ports[':IN1'].fields['1 Player Start']
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'paid join actual CPU launch',function(at,data,mask)
 if join_start or at~=0x01d01030 or mask~=0xffff or data<0x6b00 or data>0x6b02 then return end
 local actual=sample(1)
 if not actual or actual.id~=18 or actual.roster~=18 or actual.owner~=actual.actor or actual.state~=0 or cpu.A8.value~=actual.actor then return end
 join_start=frame
 log('JOIN_TRIGGER',string.format('cue=%04X pc=%08X actor=%08X main=%08X id=%d',data,cpu.PC.value,actual.actor,actual.main,actual.id))
end)
emu.register_frame(function()
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':'].items)do
   for _,field in ipairs({'actor','main','health','id','mode'})do
    if name:match('/m_mk2ks_battle_'..field..'$')then join_saved[field]=emu.item(index)end
   end
  end
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local n,field=name:match('^(%x+)/chan%.(.+)$')
   if n and tonumber(n,16)>=10 and tonumber(n,16)<=13 then
    n=tonumber(n,16);join_channels[n]=join_channels[n]or{};join_channels[n][field]=emu.item(index)
   end
  end
  assert(join_saved.actor and join_saved.main)
 end
 join_coin:clear_value();join_button:clear_value()
 if not join_start then return end
 local age=frame-join_start
 if age>=1 and age<5 then join_coin:set_value(1);log('JOIN_INPUT','button=Coin_1 age='..age)end
 if age>=8 and age<12 then join_button:set_value(1);log('JOIN_INPUT','button=Start_1 age='..age)end
end)
emu.register_frame_done(function()
 if not join_start then return end
 local age=frame-join_start
 local mode=p:read_u16(0x010601d0)
 if mode==4 and not join_selection then join_selection=frame;log('JOIN_SELECTION','age='..age)end
 if age<=300 then
  for n=0,1 do
   log('JOIN_OWNER',string.format('age=%d slot=%d actor=%08X main=%08X id=%d mode=%d',age,n+1,join_saved.actor:read(n),join_saved.main:read(n),join_saved.id:read(n),mode))
  end
  for n=10,13 do
   local c=join_channels[n]
   log('JOIN_CHANNEL',string.format('age=%d channel=%d sample=%d length=%d pos=%.8f paused=%d loop=%d mode=%d',age,n,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.paused:read(0),c.loop:read(0),mode))
  end
 end
 if join_selection and frame-join_selection>=160 then log('JOIN_COMPLETE','selection_fields=160');manager.machine:exit()end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_native_start_runtime','audit_current_native_battle_audio_join_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared normal paid P1 join on actual CPU Sonya cue; passive audio ownership only')
