-- Cold native attract observation after ordinary factory-screen High Punch.
-- No state/RNG/HP/audio writes; no coins, selection or demo assistance.
local machine=manager.machine
local device=machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,taps,channels=0,{},{}
-- Host test configuration selects only when to press an ordinary button.
-- Neither setting below writes emulated game state.
local boot_start=rawget(_G,'mk2ks_boot_frame') or 360
local capture_winners=rawget(_G,'mk2ks_capture_winners')==true
local boot_button=assert(machine.ioport.ports[':IN0']).fields['P1 High Punch']
local observed_bios,pending,observed_demos,observed_audio={},{},{},{}
local audio_until=0
local demo_epoch=nil
local function log(tag,fields)
 print(string.format('MK2_ATTRACT_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),fields))
end
local function hex(raw)return raw:gsub('.',function(c)return string.format('%02X',c:byte())end)end
local function valid(a)return a>=0x01000000 and a<0x01400000 end
local function actor(slot)
 local a=p:read_u32(slot==1 and 0x01060220 or 0x01060df0)
 local m=p:read_u32(slot==1 and 0x01060260 or 0x01060e30)
 local r=p:read_u16(slot==1 and 0x01060280 or 0x01060e50)
 return string.format('p%d_roster=%d p%d_actor=%08X p%d_main=%08X p%d_id=%d p%d_owner=%08X p%d_action=%d p%d_hp=%d',
  slot,r,slot,a,slot,m,slot,valid(a)and p:read_u16(a+0x1f0)or-1,
  slot,valid(m)and p:read_u32(m+0xc0)or 0,slot,valid(m)and p:read_u16(m+0x1f0)or-1,
  slot,p:read_u16(slot==1 and 0x010602f0 or 0x01060ec0))
end
local function picture(stage)
 local raw,w,h=machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_ATTRACT_RGB frame=%d seconds=%.12f stage=%s width=%d height=%d bytes=%d hex=%s',frame,emu.time(),stage,w,h,#raw,hex(raw)))
end
local observing=false
taps[#taps+1]=p:install_write_tap(0x01061ca0,0x01061caf,'native shared biography counter',function(at,data,mask)
 if observing then return end
 observing=true
 log('COUNTER',string.format('pc=%08X id=%d mask=%04X',cpu.PC.value,data&0xffff,mask))
 if cpu.PC.value==0xff84a460 then
  demo_epoch=nil
  local id=data&0xffff
  if not observed_bios[id]then observed_bios[id]=true;pending[#pending+1]={id=id,start=frame,done={}} end
 end
 observing=false
end)
for _,where in ipairs({{0x01060280,1},{0x01060e50,2}})do
 taps[#taps+1]=p:install_write_tap(where[1],where[1]+15,'native attract roster publication',function(at,data,mask)
  if observing then return end
  if cpu.PC.value==0xff827970 or cpu.PC.value==0xff8279f0 then
   if where[2]==2 then demo_epoch=frame end
   log('DEMO_ROSTER',string.format('slot=%d pc=%08X id=%d mask=%04X',where[2],cpu.PC.value,data&0xffff,mask))
  end
 end)
end
local table_base=0xff800000+0xf4900*8
taps[#taps+1]=p:install_read_tap(table_base,table_base+56*32-1,'native biography picture lookup',function(at,data,mask)
 if observing then return end
 if cpu.PC.value==0xff8447e0 and (at-table_base)%32==0 then
  log('PICTURE',string.format('row=%d pc=%08X low=%04X',(at-table_base)//32,cpu.PC.value,data))
 end
end)
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual native announcer/startup port',function(at,data,mask)
 if at~=0x01d01030 or mask~=0xffff then return end
 if cpu.PC.value==0xffa13c90 or cpu.PC.value==0xffa13d60 then return end
 if data==0xfffc or data==0xfffb or capture_winners and (data==0xfffe or data==0xfffd) or data>=0x6b00 and data<=0x6b03 then
  local mode=p:read_u16(0x010601d0)
  log('SOUND',string.format('word=%04X pc=%08X mode=%d mute=%d a8=%08X a13=%08X %s %s',
   data,cpu.PC.value,mode,p:read_u16(0x01061990),cpu.A8.value,cpu.A13.value,actor(1),actor(2)))
  if not observed_audio[data] or capture_winners and (data==0xfffe or data==0xfffd) or data>=0x6b00 and data<=0x6b03 and mode==1 and p:read_u16(0x01061990)==0 then
   observed_audio[data]=true;audio_until=math.max(audio_until,frame+280)
  end
 end
end)
local response_seen={}
local response_base=0xff800000+0xf3910*8
taps[#taps+1]=p:install_read_tap(response_base+17*32,response_base+19*32-1,'actual extended response rows',function(at,data,mask)
 if observing or (at-response_base)%32~=0 or cpu.PC.value~=0xff83b850 then return end
 local id=(at-response_base)//32
 if response_seen[id]then return end
 response_seen[id]=true
 observing=true
 log('AI_RESPONSE',string.format('id=%d table=%08X at=%08X low=%04X mask=%04X pc=%08X a1=%08X a8=%08X a13=%08X %s %s',
  id,response_base,at,data,mask,cpu.PC.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,actor(1),actor(2)))
 observing=false
end)
local error_tap,error_seen=nil,false
error_tap=p:install_read_tap(0xffa1e800,0xffa1e80f,'single checked executed native error',function(at,data,mask)
 if error_seen or at~=0xffa1e800 or cpu.PC.value~=0xffa1e810 then return end
 error_seen=true
 log('ERROR_ENTRY',string.format('pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X %s %s',
  cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,actor(1),actor(2)))
 error_tap:remove()
end)
local last_demo_state=nil
local boots=0
emu.register_prestart(function()
 boots=boots+1;log('RESET',string.format('count=%d pc=%08X',boots,cpu.PC.value))
end)
emu.register_frame(function()
 frame=frame+1
 boot_button:clear_value()
 if frame>=boot_start and frame<boot_start+4 then
  boot_button:set_value(1)
  log('INPUT','slot=1 button=HighPunch value=1 reason=ordinary_cold_boot_ack')
 elseif frame==boot_start+4 then log('INPUT','slot=1 button=HighPunch value=0 reason=ordinary_cold_boot_release')end
 if frame==1 then
  log('CONFIG',string.format('boot_start=%d capture_winners=%d',boot_start,capture_winners and 1 or 0))
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  print('MK2_ATTRACT_GUEST bytes=1048576 hex='..hex(raw))
  local g=assert(machine.memory.regions[':gfxrom']);local bytes={}
  for i=0,65535 do bytes[#bytes+1]=string.char(g:read_u8(0x1e40000+i))end
  print('MK2_ATTRACT_BATTLE_GFX bytes=65536 hex='..hex(table.concat(bytes)))
  for name,index in pairs(machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for n=0,13 do assert(channels[n] and channels[n].source_num and channels[n].pos)end
  log('BEGIN','input=ordinary_cold_boot_ack_only')
 end
 local mode=p:read_u16(0x010601d0)
 local r1,r2=p:read_u16(0x01060280),p:read_u16(0x01060e50)
 if mode==1 and (r1==17 or r1==18 or r2==17 or r2==18) then
  local state=actor(1)..' '..actor(2)
  if state~=last_demo_state then
   log('DEMO_STATE',string.format('mode=%d counter=%d pc=%08X %s',mode,p:read_u16(0x01061ca0),cpu.PC.value,state))
   last_demo_state=state
  end
 else last_demo_state=nil end
 if frame%60==0 then log('FIELD',string.format('mode=%d mute=%d counter=%d %s %s',mode,p:read_u16(0x01061990),p:read_u16(0x01061ca0),actor(1),actor(2)))end
 if frame<=audio_until then
  log('AUDIO_OWNER',string.format('mode=%d mute=%d %s %s',mode,p:read_u16(0x01061990),actor(1),actor(2)))
  for n=0,13 do
   local c=channels[n]
   log('CHANNEL',string.format('channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d',n,c.source_num:read(0),c.source_len:read(0),
    string.unpack('<d',c.pos:read_block(0,8)),c.loop:read(0),c.paused:read(0)))
  end
 end
end)
emu.register_frame_done(function()
 if frame==240 or frame==600 then picture('startup_'..frame)end
 for _,bio in ipairs(pending)do
  for _,delay in ipairs({60,180})do
   if not bio.done[delay] and frame>=bio.start+delay then
    bio.done[delay]=true
    picture(string.format('bio_%d_delay_%d',bio.id,delay))
   end
  end
 end
 if p:read_u16(0x010601d0)==1 and demo_epoch and frame>=demo_epoch+60 then
  for slot=1,2 do
   local roster=p:read_u16(slot==1 and 0x01060280 or 0x01060e50)
   local a=p:read_u32(slot==1 and 0x01060220 or 0x01060df0)
   local m=p:read_u32(slot==1 and 0x01060260 or 0x01060e30)
   local key=slot..'_'..roster
   if (roster==17 or roster==18) and not observed_demos[key] and valid(a) and valid(m) and
     p:read_u16(a+0x1f0)==roster and p:read_u32(m+0xc0)==a and
     p:read_u16(slot==1 and 0x010602f0 or 0x01060ec0)>0 then
    -- Live demo ownership, not stale attract global fields alone.
    observed_demos[key]={start=frame}
    log('DEMO_OWNER',string.format('slot=%d id=%d %s %s',slot,roster,actor(1),actor(2)))
   end
  end
  for key,demo in pairs(observed_demos)do
   if not demo.captured and frame>=demo.start+90 then
    demo.captured=true;picture('demo_'..key..'_delay_90')
   end
  end
 end
end)
emu.register_sound_update(function()
 if frame<=audio_until then
  local raw=machine.sound:get_samples()
  print(string.format('MK2_ATTRACT_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,emu.time(),#raw,hex(raw)))
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('boots=%d frames=%d input=ordinary_cold_boot_ack_only',boots,frame))
 if not error_seen then error_tap:remove()end
 for _,tap in ipairs(taps)do tap:remove()end
end)



-- Original native DCS/DAC observer, separate names and stock packets.
local function active()return frame<=audio_until end
local dsp=assert(machine.devices[':dcs:dcs'])
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'all actual attract sound packets',function(at,data,mask)
 if at==0x01d01030 and active()then
  log('PORT',string.format('word=%04X mask=%04X pc=%08X a8=%08X a13=%08X mode=%d mute=%d',
   data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(0x010601d0),p:read_u16(0x01061990)))
 end
end)
taps[#taps+1]=dsp.spaces.data:install_read_tap(0x3400,0x37ff,'actual native attract DCS input latch',function(at,value,mask)
 if active()then log('DCS_DELIVERY',string.format('at=%04X word=%04X mask=%04X dsp_pc=%04X',at,value,mask,dsp.state.PC.value))end
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

if capture_winners then
 taps[#taps+1]=p:install_read_tap(0xff820a20,0xff820a2f,'actual native winner call opcode',function(at,data,mask)
  if at~=0xff820a20 or cpu.PC.value~=0xff820a30 then return end
  log('WINNER_CALL',string.format('pc=%08X a0=%08X mode=%d mute=%d %s %s',cpu.PC.value,cpu.A0.value,
   p:read_u16(0x010601d0),p:read_u16(0x01061990),actor(1),actor(2)))
  if cpu.A0.value==0xfe or cpu.A0.value==0xfd then audio_until=math.max(audio_until,frame+280)end
 end)
end
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
-- Additional passive exact sample-clock/gain snapshots at actual sound callbacks.
local mix_frame,mix_channels,mix_items,mix_serial=0,{},{},0
local function mix_bind(tag)
 local device=assert(manager.machine.devices[tag])
 for name,index in pairs(device.items)do
  local channel,field=name:match('^(%x+)/chan%.(.+)$')
  if tag==':mk2ksvoices'and channel then
   channel=tonumber(channel,16);mix_channels[channel]=mix_channels[channel]or{}
   mix_channels[channel][field]=emu.item(index)
  end
  if name:match('/m_gain$')or name:match('/m_user_gain$')then
   local item=emu.item(index);assert(item.size==4 and item.count==1)
   mix_items[#mix_items+1]={device=tag,name=name,item=item}
  end
 end
end
emu.register_frame(function()
 mix_frame=mix_frame+1
 if mix_frame==1 then
  mix_bind(':mk2ksvoices');mix_bind(':mk2ksvoice')
  for channel=0,13 do
   local c=assert(mix_channels[channel])
   assert(c.source_num and c.source_len and c.pos and c.loop and c.paused)
  end
  table.sort(mix_items,function(a,b)return a.device..a.name<b.device..b.name end)
  for i,entry in ipairs(mix_items)do
   print(string.format('MK2_TOMB_MIX_ITEM frame=%d index=%d device=%s name=%s bytes=4 count=1 writes=0 assistance=none',
    mix_frame,i,entry.device,entry.name))
  end
 end
end)
emu.register_sound_update(function()
 if not active()then return end
 mix_serial=mix_serial+1
 for channel=0,13 do
  local c=mix_channels[channel]
  local raw=c.pos:read_block(0,8);assert(#raw==8)
  print(string.format('MK2_TOMB_MIX_CHANNEL frame=%d seconds=%.12f index=%d channel=%d sample=%d length=%d position=%.17g bits=%s loop=%d paused=%d writes=0 assistance=none',
   mix_frame,emu.time(),mix_serial,channel,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',raw),
   raw:gsub('.',function(value)return string.format('%02X',value:byte())end),c.loop:read(0),c.paused:read(0)))
 end
 for i,entry in ipairs(mix_items)do
  print(string.format('MK2_TOMB_MIX_GAIN frame=%d seconds=%.12f index=%d item=%d bits=%08X writes=0 assistance=none',
   mix_frame,emu.time(),mix_serial,i,entry.item:read(0)))
 end
end)




-- Native policy read/write provenance; physical switches and guest words read only.
local policy_reading=false
taps[#taps+1]=p:install_write_tap(0x01061990,0x0106199f,'actual native attract mute policy',function(at,data,mask)
 if policy_reading then return end
 policy_reading=true
 log('MUTE_POLICY',string.format('pc=%08X value=%d mask=%04X a0=%08X a13=%08X mode=%d counter=%d',
  cpu.PC.value,data,mask,cpu.A0.value,cpu.A13.value,p:read_u16(0x010601d0),p:read_u16(0x01061ca0)))
 policy_reading=false
end)
taps[#taps+1]=p:install_read_tap(0xff8474a0,0xff8474af,'actual native switch-policy return',function(at,data,mask)
 if at~=0xff8474a0 or cpu.PC.value~=0xff8474b0 then return end
 log('SWITCH_POLICY',string.format('pc=%08X a0=%08X dsw=%04X',cpu.PC.value,cpu.A0.value,machine.ioport.ports[':DSW']:read()))
end)
emu.register_frame(function()
 if frame==1 then
  local field=assert(machine.ioport.ports[':DSW'].fields['Attract Sound'])
  log('DIP',string.format('name=AttractSound mask=%04X default=%04X configured=%04X actual=%04X',field.mask,field.defvalue,field.user_value,machine.ioport.ports[':DSW']:read()))
 end
end)
