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
