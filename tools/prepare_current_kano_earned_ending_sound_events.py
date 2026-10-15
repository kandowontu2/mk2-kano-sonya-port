"""Sparse native command/channel observation on unchanged earned-ending route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_postending_two_coin_join_preparation'
out=sync.ROOT/'audit_current_kano_earned_ending_sound_events_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source+='''
local ea_channels,ea_prior={},{}
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'passive earned ending sound words',function(at,data,mask)
 if frame<72000 or at~=0x01d01030 or mask~=0xffff then return end
 log('ENDING_SOUND_WORD',string.format('word=%04X pc=%08X mode=%d mute=%d',data&0xffff,cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061990)))
end)
emu.register_frame_done(function()
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local n,field=name:match('^(%x+)/chan%.(.+)$')
   if n then local k=tonumber(n,16);ea_channels[k]=ea_channels[k]or{};ea_channels[k][field]=emu.item(index)end
  end
  for k=0,18 do local c=assert(ea_channels[k]);assert(c.source_num and c.source_len and c.pos and c.loop and c.paused)end
 end
 if frame<72000 then return end
 for k=0,18 do
  local c=ea_channels[k];local num,len,loop,paused=c.source_num:read(0),c.source_len:read(0),c.loop:read(0),c.paused:read(0)
  local key=string.format('%d:%d:%d:%d',num,len,loop,paused)
  if key~=ea_prior[k] or (num>=0 and frame%120==0)then
   log('ENDING_SOUND_CHANNEL',string.format('channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d mode=%d mute=%d',k,num,len,string.unpack('<d',c.pos:read_block(0,8)),loop,paused,p:read_u16(0x010601d0),p:read_u16(0x01061990)))
   ea_prior[k]=key
  end
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_postending_two_coin_join_runtime','audit_current_kano_earned_ending_sound_events_runtime')
(out/'run.ps1').write_text(runner)
print('Unchanged K2 earned route; sparse passive sound events;180sec/320MiB/10MiB; no media')
