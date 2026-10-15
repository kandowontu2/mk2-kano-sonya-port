-- Cold native attract observation after ordinary factory-screen High Punch.
-- No state/RNG/HP/audio writes; no coins, selection or demo assistance.
local machine=manager.machine
local device=machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,taps,channels=0,{},{}
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
 if data==0xfffc or data==0xfffb or data>=0x6b00 and data<=0x6b03 then
  local mode=p:read_u16(0x010601d0)
  log('SOUND',string.format('word=%04X pc=%08X mode=%d mute=%d a8=%08X a13=%08X %s %s',
   data,cpu.PC.value,mode,p:read_u16(0x01061990),cpu.A8.value,cpu.A13.value,actor(1),actor(2)))
  if not observed_audio[data]then observed_audio[data]=true;audio_until=math.max(audio_until,frame+180)end
 end
end)
local boots=0
emu.register_prestart(function()
 boots=boots+1;log('RESET',string.format('count=%d pc=%08X',boots,cpu.PC.value))
end)
emu.register_frame(function()
 frame=frame+1
 boot_button:clear_value()
 if frame>=300 and frame<304 then
  boot_button:set_value(1)
  log('INPUT','slot=1 button=HighPunch value=1 reason=ordinary_cold_boot_ack')
 elseif frame==304 then log('INPUT','slot=1 button=HighPunch value=0 reason=ordinary_cold_boot_release')end
 if frame==1 then
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
 for _,tap in ipairs(taps)do tap:remove()end
end)

-- Bounded passive provenance of the stock attract collision-bounds walker.
-- Installed only at the naturally reached Sonya P1 start; never change state.
local probe_taps,probe_installed,probe_removed={},false,false
local probe_origin,probe_records,last_probe=nil,0,{}
local probe_observing=false
local function probe_words(a,count)
 if not (a>=0x01000000 and a<=0x013ff000 or a>=0xff800000 and a<=0xfffff000)then return 'unmapped' end
 local out={}
 for i=0,count-1 do out[#out+1]=string.format('%04X',p:read_u16(a+i*16))end
 return table.concat(out)
end
local function probe_snapshot(entry)
 probe_observing=true
 local out={string.format('entry=%08X pc=%08X mode=%d counter=%d timer=%d',entry,cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061ca0),p:read_u16(0x010619d0))}
 for _,bank in ipairs({'A','B'})do
  for n=0,14 do local name=bank..n;out[#out+1]=string.format('%s=%08X',name,cpu[name].value)end
 end
 out[#out+1]=string.format('SP=%08X task=%s stack=%s A4words=%s',cpu.SP.value,probe_words(cpu.A13.value,24),probe_words(cpu.SP.value,16),probe_words(cpu.A4.value,24))
 for slot=1,2 do
  local a=p:read_u32(slot==1 and 0x01060220 or 0x01060df0)
  if valid(a)then out[#out+1]=string.format('p%d_box=%08X p%d_actor_words=%s',slot,p:read_u32(a+0x1a0),slot,probe_words(a,32))end
 end
 log('PROBE',table.concat(out,' '))
 probe_observing=false
end
emu.register_frame_done(function()
 if not probe_installed and p:read_u16(0x01060280)==18 and p:read_u16(0x010601d0)==1 and p:read_u16(0x010602f0)==161 and frame>22000 then
  probe_installed=true;probe_origin=frame
  log('PROBE_BEGIN',actor(1)..' '..actor(2))
  for _,entry in ipairs({0xff827c40,0xff827c90,0xff827da0,0xff828910,0xff828990,0xff8289d0,0xff828ae0,0xff80dcc0,0xff841ec0})do
   probe_taps[#probe_taps+1]=p:install_read_tap(entry,entry+15,'bounded native demo-start provenance',function(at)
    if probe_observing or at~=entry or probe_records>=120 or last_probe[entry]==frame then return end
    last_probe[entry]=frame;probe_records=probe_records+1;probe_snapshot(entry)
   end)
  end
 end
 if probe_installed and not probe_removed and (probe_records>=120 or frame>=probe_origin+300)then
  probe_removed=true
  for _,tap in ipairs(probe_taps)do tap:remove()end
  log('PROBE_END',string.format('records=%d origin=%d',probe_records,probe_origin))
 end
 if frame==23000 or frame==24000 or frame==28000 then
  log('PROBE_FIELD',string.format('pc=%08X timer=%d %s %s',cpu.PC.value,p:read_u16(0x010619d0),actor(1),actor(2)))
  picture('stalled_demo_field_'..frame)
 end
end)
emu.register_stop(function()for _,tap in ipairs(probe_taps)do tap:remove()end end)

local error_seen=false
local error_tap=p:install_read_tap(0xffa1e800,0xffa1e80f,'first real native error-loop entry',function(at)
 if at~=0xffa1e800 or cpu.PC.value~=0xffa1e810 or error_seen or probe_observing then return end
 error_seen=true
 probe_snapshot(0xffa1e800)
 log('ERROR_ENTRY',string.format('pc=%08X SP=%08X stack=%s task=%s',cpu.PC.value,cpu.SP.value,probe_words(cpu.SP.value,64),probe_words(cpu.A13.value,64)))
end)
emu.register_stop(function()error_tap:remove()end)



local fatal_seen=false
local fatal_tap=p:install_read_tap(0xffa1d860,0xffa1d86f,'actual first native fatal caller provenance',function(at)
 if at~=0xffa1d860 or cpu.PC.value~=0xffa1d870 or fatal_seen or probe_observing then return end
 fatal_seen=true
 probe_snapshot(0xffa1d860)
 log('FATAL_CALLER',string.format('code=%08X caller=%08X pc=%08X SP=%08X stack=%s task=%s',cpu.A0.value,p:read_u32(cpu.SP.value),cpu.PC.value,cpu.SP.value,probe_words(cpu.SP.value,64),probe_words(cpu.A13.value,64)))
end)
emu.register_stop(function()fatal_tap:remove()end)
