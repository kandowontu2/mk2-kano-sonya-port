"""Sparse native name-cue/channel-state observation; no PCM or raw buffers."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_attract_long_preparation'
out=sync.ROOT/'audit_bounded_current_bio_cues_preparation';assert not out.exists()
source=(old/'attract.lua').read_text()
source+='''
local channel={},audio_until=0
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual own name cues',function(at,data,mask)
 if at~=0x01d01030 or mask~=0xffff or(data~=0xfffc and data~=0xfffb)then return end
 log('NAME_CUE',string.format('word=%04X pc=%08X counter=%d mode=%d mute=%d',data,cpu.PC.value,p:read_u16(0x01061ca0),p:read_u16(0x010601d0),p:read_u16(0x01061990)))
 audio_until=frame+120
end)
emu.register_frame(function()
 if frame==1 then
  for name,index in pairs(machine.devices[':mk2ksvoices'].items)do
   local n,field=name:match('^(%x+)/chan%.(.+)$')
   if n and tonumber(n,16)==0 then channel[field]=emu.item(index)end
  end
  assert(channel.source_num and channel.source_len and channel.pos and channel.loop and channel.paused)
 end
 if frame%60==0 then log('SOUND_GATE','mute='..p:read_u16(0x01061990)..' counter='..p:read_u16(0x01061ca0))end
 if frame<=audio_until then
  log('VOICE_CHANNEL',string.format('sample=%d length=%d pos=%.8f loop=%d paused=%d',channel.source_num:read(0),channel.source_len:read(0),string.unpack('<d',channel.pos:read_block(0,8)),channel.loop:read(0),channel.paused:read(0)))
 end
end)
'''
# Lua local declarations use one name list before the assignment.
source=source.replace('local channel={},audio_until=0','local channel,audio_until={},0')
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(old/'attract.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_current_attract_long_runtime','audit_bounded_current_bio_cues_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000field sparse bio cue/channel state trace, no PCM/media or changed game state')
