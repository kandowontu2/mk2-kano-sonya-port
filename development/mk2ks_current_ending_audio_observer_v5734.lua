-- Read-only native ending/attract sound observer. No controls or exit callback.
local device=manager.machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local identity=assert(({kano=17,sonya=18})[fighter])
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')));assert(side==1 or side==2);local other=3-side
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,window,origin,completed,seen_live,own_boss_wins=0,nil,nil,nil,false,0
local taps,channels={},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function active()return window~=nil end
local function log(tag,s)
 print(string.format('MK2_EAUDIO_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),s))
end
local winner_entry=0xfffef800+identity*32
taps[#taps+1]=p:install_read_tap(winner_entry,winner_entry+15,'actual original own boss winner table read',function(at,value,mask)
 if at~=winner_entry or cpu.PC.value~=0xff8296b0 or frame<=1 or p:read_u16(0x01061b30)~=16 or
  p:read_u16(0x01061b00)~=side or p:read_u16(slots[side].roster)~=identity or
  p:read_u16(slots[side].hp)<=0 or p:read_u16(slots[other].hp)~=0 then return end
 own_boss_wins=own_boss_wins+1
 log('WINNER',string.format('entry=%08X value=%04X mask=%04X pc=%08X identity=%d winner=%d',
  at,value,mask,cpu.PC.value,identity,side))
end)
taps[#taps+1]=p:install_write_tap(slots[other].hp,slots[other].hp+15,'actual original final boss collision KO',function(at,data,mask)
 if window or at~=slots[other].hp or mask~=0xffff or data~=0 or p:read_u16(at)<=0 or cpu.PC.value~=0xff836700 or
  not seen_live or own_boss_wins~=1 or p:read_u16(0x01061b30)~=16 or
  p:read_u16(slots[side].roster)~=identity or p:read_u16(slots[side].hp)<=0 then return end
 window=frame
 log('WINDOW',string.format('window=%d identity=%d at=%08X before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X own_boss_winner_reads=%d',
  window,identity,at,p:read_u16(at),data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,own_boss_wins))
end)
for _,entry in ipairs({0xffa11fd0,0xffa12070,0xffa12220,0xffa122d0,0xffa123b0,0xffa123d0,0xffa12430,0xffa12530})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual native ending voice/music route',function(at)
  if at~=entry or cpu.PC.value~=at+16 or not active()then return end
  local a,m=cpu.A8.value,cpu.A13.value
  log('ROUTE',string.format('entry=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X id=%d owner=%08X return_pc=%08X',
   entry,cpu.A0.value,cpu.A1.value,cpu.A2.value,a,m,valid(a)and p:read_u16(a+0x1f0)or-1,
   valid(m)and p:read_u32(m+0xc0)or 0,p:read_u32(cpu.SP.value)))
 end)
end
for _,entry in ipairs({0xffa12a10,0xffa12a80,0xffa12b00,0xffa13ba0})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual original ending sound queue/packet',function(at)
  if at~=entry or cpu.PC.value~=at+16 or not active()then return end
  log(entry==0xffa13ba0 and'PACKET'or'QUEUE',string.format('entry=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X',
   entry,cpu.A1.value,cpu.A3.value,cpu.A4.value,cpu.A8.value,cpu.A13.value))
 end)
end
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual original ending sound port',function(at,data,mask)
 if at==0x01d01030 and active()then
  log('SOUND',string.format('word=%04X mask=%04X pc=%08X a8=%08X a13=%08X',data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 end
end)
local dsp=assert(manager.machine.devices[':dcs:dcs'])
taps[#taps+1]=dsp.spaces.data:install_read_tap(0x3400,0x37ff,'actual original MKII ending DCS input latch',function(at,value,mask)
 if active()then log('DELIVERY',string.format('at=%04X word=%04X mask=%04X dsp_pc=%04X',at,value,mask,dsp.state.PC.value))end
end)
emu.register_frame(function()
 frame=frame+1;assert(#taps==16,'All fifteen audio/winner taps plus exact original final collision KO tap')
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for n=0,13 do local c=assert(channels[n]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)end
 end
 local mode,stage=p:read_u16(0x010601d0),p:read_u16(0x01061b30)
 local roster,winner=p:read_u16(slots[side].roster),p:read_u16(0x01061b00)
 local h1,h2=p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)
 local a1,a2=p:read_u32(slots[1].actor),p:read_u32(slots[2].actor)
 if mode==4 then own_boss_wins=0 end
 if p:read_u16(slots[side].state)==1 and roster==identity and valid(side==1 and a1 or a2)and(side==1 and h1 or h2)>0 then seen_live=true end
 if window and not origin and seen_live and own_boss_wins>0 and stage==16 and mode==11 and winner==side and
  roster==identity and p:read_u16(slots[other].hp)==0 and p:read_u16(slots[side].hp)>0 and a1==0 and a2==0 then
  origin=frame
  log('BEGIN',string.format('origin=%d identity=%d winner=%d roster=%d health=%d,%d actors=%08X,%08X own_boss_winner_reads=%d',
   origin,identity,winner,roster,h1,h2,a1,a2,own_boss_wins))
 end
 if active()then
  if origin and not completed and frame-origin>1200 and mode==11 and roster~=identity then
   completed=frame;log('ATTRACT',string.format('origin=%d age=%d mode=%d roster=%d,%d',origin,frame-origin,mode,
    p:read_u16(slots[1].roster),p:read_u16(slots[2].roster)))
  end
  log('FIELD',string.format('window=%d origin=%d stage=%d mode=%d winner=%d roster=%d,%d actors=%08X,%08X health=%d,%d',
   window,origin or-1,stage,mode,winner,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),a1,a2,h1,h2))
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
  print(string.format('MK2_EAUDIO_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,emu.time(),#raw,
   raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('window=%d origin=%d attract=%d raw_audio_files=0',window or-1,origin or-1,completed or-1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
-- Entire passive5592 DAC observer; only its ending admission changes.
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
-- Entire passive5585 ROM observer; only its actual native terminal changes.
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
 assert(checks==2 and origin and completed and frame==completed+300,'Both complete original sound ROM checks and genuine native terminal')
 print(string.format('MK2_NATIVE_DCS_ROM_RESULT frame=%d checks=%d writes=0 assistance=none',frame,checks))
end)
