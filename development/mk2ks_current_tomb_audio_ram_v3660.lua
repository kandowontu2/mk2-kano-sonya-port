-- Read-only sound observer on the original physical controller/provenance.
-- Full mixed PCM travels to verifier RAM only; no audio/image/VRAM files.
dofile('mk2ks_current_stage_provenance_v3595.lua')
local device=manager.machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,origin,taps,channels=0,nil,{},{}
local function log(tag,s)
 print(string.format('MK2_TAUDIO_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),s))
end
local function active()return origin and frame<=origin+650 end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
taps[#taps+1]=p:install_read_tap(0xff8bdfe0,0xff8bdfef,'actual native Tomb audio origin',function(at)
 if at==0xff8bdfe0 and not origin then
  origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X',origin,cpu.A8.value,cpu.A13.value))
 end
end)
for _,entry in ipairs({0xffa11fd0,0xffa12220,0xffa122d0,0xffa123b0,0xffa123d0,0xffa12530})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual native victim voice routing',function(at)
  if at~=entry or not active()then return end
  local a=cpu.A8.value;local m=cpu.A13.value
  log('ROUTE',string.format('entry=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X id=%d owner=%08X return_pc=%08X',
   entry,cpu.A0.value,cpu.A1.value,cpu.A2.value,a,m,valid(a)and p:read_u16(a+0x1f0)or-1,
   valid(m)and p:read_u32(m+0xc0)or 0,p:read_u32(cpu.SP.value)))
 end)
end
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual native Tomb sound port',function(at,data,mask)
 if at==0x01d01030 and active()then
  log('SOUND',string.format('word=%04X mask=%04X pc=%08X a8=%08X a13=%08X',data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 end
end)
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for n=0,13 do local c=assert(channels[n]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)end
 end
 if active()then
  for n=0,13 do
   local c=channels[n]
   log('CHANNEL',string.format('channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d',n,c.source_num:read(0),c.source_len:read(0),
    string.unpack('<d',c.pos:read_block(0,8)),c.loop:read(0),c.paused:read(0)))
  end
 end
end)
emu.register_sound_update(function()
 if active()then
  local raw=manager.machine.sound:get_samples()
  print(string.format('MK2_BBAUDIO_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,emu.time(),#raw,
   raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('origin=%d raw_audio_files=0',origin or-1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
