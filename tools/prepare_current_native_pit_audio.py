"""Passive sound words and five channel0 scalars; no PCM, dumps or writes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_pit_longkick_preparation'
out=sync.ROOT/'audit_current_native_pit_audio_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
source+='''
local channel={}
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'native Pit sound words',function(at,data,mask)
 if not action or at~=0x01d01030 or mask~=0xffff then return end
 log('AUDIO_WORD',string.format('age=%d word=%04X pc=%08X mute=%d',frame-action,data&0xffff,cpu.PC.value,p:read_u16(0x01061990)))
end)
emu.register_frame_done(function()
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local n,field=name:match('^(%x+)/chan%.(.+)$')
   if n and tonumber(n,16)==0 then channel[field]=emu.item(index)end
  end
  assert(channel.source_num and channel.source_len and channel.pos and channel.loop and channel.paused)
 end
 if action and frame-action<=800 then
  log('AUDIO_CHANNEL',string.format('age=%d sample=%d length=%d pos=%.8f loop=%d paused=%d mute=%d',
   frame-action,channel.source_num:read(0),channel.source_len:read(0),string.unpack('<d',channel.pos:read_block(0,8)),channel.loop:read(0),channel.paused:read(0),p:read_u16(0x01061990)))
 end
end)
'''
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_pit_longkick_kano_p1_runtime','audit_current_native_pit_audio_kano_p1_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared actual Pit sound-word/channel0 passive trace; no PCM/media, unchanged controller/caps')
