"""Sparse voice-port/channel state observer, no PCM or controller changes."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_smoke_audio_preparation'
assert not out.exists();out.mkdir()
for fighter,base_name in [('kano','audit_current_kano_smoke_64_cadence_preparation'),('sonya','audit_current_sonya_smoke_transition_batched_preparation')]:
    base=sync.ROOT/base_name
    source=(base/'stage.lua').read_text()
    source+='''
local voice_channels,voice_signatures,voice_changes={},{},{}
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'secret native sound words',function(at,data,mask)
 if accepted and at==0x01d01030 and mask==0xffff then log('SMOKE_AUDIO_WORD',string.format('word=%04X pc=%08X mode=%d arena=%d mute=%d',data&0xffff,cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061ac0),p:read_u16(0x01061990)))end
end)
emu.register_frame_done(function()
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local n,field=name:match('^(%x+)/chan%.(.+)$')
   if n then n=tonumber(n,16);voice_channels[n]=voice_channels[n]or{};voice_channels[n][field]=emu.item(index)end
  end
  assert(voice_channels[0].source_num and voice_channels[18].source_len)
 end
 if not accepted then return end
 for n=0,18 do
  local c=voice_channels[n]
  local signature=string.format('%d:%d:%d:%d',c.source_num:read(0),c.source_len:read(0),c.paused:read(0),c.loop:read(0))
  if signature~=voice_signatures[n] then voice_signatures[n]=signature;voice_changes[n]=frame end
  local age=frame-voice_changes[n]
  if age==0 or age==1 or age==2 or age==20 or age==60 or frame==returned then
   log('SMOKE_AUDIO_CHANNEL',string.format('channel=%d sample=%d length=%d pos=%.8f paused=%d loop=%d changed=%d age=%d mode=%d arena=%d',n,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.paused:read(0),c.loop:read(0),voice_changes[n],age,p:read_u16(0x010601d0),p:read_u16(0x01061ac0)))
  end
 end
end)
'''
    assert ':write_' not in source and ':snapshot(' not in source
    lua=out/(fighter+'.lua');lua.write_text(source)
    runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/'+fighter+'.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
    prior='audit_current_'+fighter+('_smoke_64_cadence_runtime' if fighter=='kano' else '_smoke_transition_batched_runtime')
    runner=runner.replace(prior,'audit_current_smoke_audio_'+fighter+'_runtime')
    (out/(fighter+'.ps1')).write_text(runner)
print('Prepared sparse scalar audio observers; unchanged earned routes;90sec/320MiB/no media')
