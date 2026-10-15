-- Full original true-mirror Tomb audio, native DAC and sound-ROM observers.
-- Passive only; original controller is loaded separately.
local device=manager.machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,origin,taps,channels=0,nil,{},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,s)
 print(string.format('MK2_MAUDIO_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),s))
end
local function active()return origin and frame<=origin+1100 end
taps[#taps+1]=p:install_read_tap(0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin',function(at)
 if at~=0xff8bdfe0 or cpu.PC.value~=at+16 or frame<=1 or origin then return end
 local a,m=cpu.A8.value,cpu.A13.value
 if not valid(a)or not valid(m)or p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')]) or p:read_u32(m+0xc0)~=a then return end
 origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X id=%d',origin,a,m,p:read_u16(a+0x1f0)))
end)
for _,entry in ipairs({0xffa11fd0,0xffa12070,0xffa12220,0xffa122d0,0xffa123b0,0xffa123d0,0xffa12430,0xffa12530})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual native swallowing voice routing',function(at)
  if at~=entry or cpu.PC.value~=at+16 or not active()then return end
  local a,m=cpu.A8.value,cpu.A13.value
  log('ROUTE',string.format('entry=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X id=%d owner=%08X return_pc=%08X',
   entry,cpu.A0.value,cpu.A1.value,cpu.A2.value,a,m,valid(a)and p:read_u16(a+0x1f0)or-1,
   valid(m)and p:read_u32(m+0xc0)or 0,p:read_u32(cpu.SP.value)))
 end)
end
-- Observe the actual original priority-slot branch and packed word before
-- DCS delivery. No channel number is inferred from the resulting sound.
for _,entry in ipairs({0xffa12a10,0xffa12a80,0xffa12b00,0xffa13ba0})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual original sound queue selection',function(at)
  if at~=entry or cpu.PC.value~=at+16 or not active()then return end
  local a,m=cpu.A8.value,cpu.A13.value
  log(entry==0xffa13ba0 and 'PACKET'or'QUEUE',string.format('entry=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X',
   entry,cpu.A1.value,cpu.A3.value,cpu.A4.value,a,m))
 end)
end
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual native swallowing sound port',function(at,data,mask)
 if at==0x01d01030 and active()then
  log('SOUND',string.format('word=%04X mask=%04X pc=%08X a8=%08X a13=%08X',data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 end
end)
local dsp=assert(manager.machine.devices[':dcs:dcs'])
taps[#taps+1]=dsp.spaces.data:install_read_tap(0x3400,0x37ff,'actual original MKII DCS input latch',function(at,value,mask)
 if active()then log('DELIVERY',string.format('at=%04X word=%04X mask=%04X dsp_pc=%04X',at,value,mask,dsp.state.PC.value))end
end)
emu.register_frame(function()
 assert(#taps==15,'Every audio observer retained')
 frame=frame+1
 if frame==1 then
  -- Native bit-addressed program reads, same initialized whole guest as the
  -- independently qualified state and continuous visual captures.
  local words={}
  for at=0xff800000,0xffffffe0,32 do words[#words+1]=string.pack('<I4',p:read_u32(at))end
  local raw=table.concat(words);assert(#raw==1048576)
  print(string.format('MK2_MAUDIO_GUEST bytes=%d hex=%s',#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
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
-- Entire qualified5592 DAC observer, only actual Tomb window adapter.
local frame,serial,previous,previous_time=0,0,nil,nil
local dac,dcs={},{}
local function bind(device,wanted)
 local result={}
 for name,index in pairs(assert(manager.machine.devices[device]).items)do
  for _,key in ipairs(wanted)do
   if name:match(key..'$')then assert(not result[key]);result[key]=emu.item(index)end
  end
 end
 for _,key in ipairs(wanted)do assert(result[key],'Missing original native item '..key)end
 return result
end
local function segment(first,count)
 assert(count>=0 and count<32768)
 local a=math.min(count,32768-first)
 local raw=dac.m_buffer:read_block(first*4,a*4)
 if a<count then raw=raw..dac.m_buffer:read_block(0,(count-a)*4)end
 assert(#raw==count*4);return raw
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  dac=bind(':dcs:dac',{'m_buffer','m_bufin','m_bufout','m_volume','m_enabled'})
  dcs=bind(':dcs',{'m_channels','m_size','m_incs','m_ireg','m_ireg_base','m_control_regs'})
  assert(dac.m_buffer.size==4 and dac.m_buffer.count==32768 and dcs.m_control_regs.size==2 and dcs.m_control_regs.count==32)
 end
end)
emu.register_sound_update(function()
 if not dac.m_bufout then return end
 local current=dac.m_bufout:read(0)
 local old,oldtime=previous,previous_time
 previous=current;previous_time=emu.time()
 if not active()then return end
 assert(old and oldtime and current<32768 and old<32768)
 local count=(current-old)%32768
 assert(count<4096,'No unaccounted native DAC reset or ring traversal')
 local raw=segment((old-4)%32768,count+4)
 serial=serial+1
 print(string.format('MK2_NATIVE_DAC_RAM frame=%d seconds=%.12f previous_seconds=%.12f index=%d writes=0 assistance=none previous_out=%d current_out=%d current_in=%d consumed=%d prefix=4 ring=32768 element_bytes=4 enabled=%d volume=%08X channels=%d size=%d incs=%d ireg=%d base=%d autobuffer=%04X syscontrol=%04X s1control=%04X sclkdiv=%04X bytes=%d hex=%s',
  frame,emu.time(),oldtime,serial,old,current,dac.m_bufin:read(0),count,dac.m_enabled:read(0),dac.m_volume:read(0),
  dcs.m_channels:read(0),dcs.m_size:read(0),dcs.m_incs:read(0),dcs.m_ireg:read(0),dcs.m_ireg_base:read(0),
  dcs.m_control_regs:read(15),dcs.m_control_regs:read(31),dcs.m_control_regs:read(18),dcs.m_control_regs:read(17),#raw,
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end)
emu.register_stop(function()
 print(string.format('MK2_NATIVE_DAC_RESULT frame=%d callbacks=%d writes=0 assistance=none',frame,serial))
end)
-- Entire qualified5585 ROM observer, only original Tomb terminal adapter.
local region=assert(manager.machine.memory.regions[':dcs'])
assert(region.size==0xc00000 and region.bytewidth==2 and region.bitwidth==16 and region.length==0x600000)
local frame,checks=0,0
local function dump(phase)
 for offset=0,region.size-1,65536 do
  local words={}
  for at=offset,offset+65532,4 do words[#words+1]=string.pack('<I4',region:read_u32(at))end
  local raw=table.concat(words)
  local hex=raw:gsub('.',function(c)return string.format('%02X',c:byte())end)
  print(string.format('MK2_NATIVE_DCS_ROM phase=%s frame=%d seconds=%.12f writes=0 assistance=none offset=%d bytes=%d size=%d bytewidth=%d bitwidth=%d hex=%s',
   phase,frame,emu.time(),offset,#raw,region.size,region.bytewidth,region.bitwidth,hex))
 end
 checks=checks+1
end
emu.register_frame(function()frame=frame+1;if frame==1 then dump('startup')end end)
emu.register_stop(function()
 dump('terminal')
 assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')
 print(string.format('MK2_NATIVE_DCS_ROM_RESULT frame=%d checks=%d writes=0 assistance=none',frame,checks))
end)
