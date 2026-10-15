-- Original genuine mirror controller plus read-only PCM/actual owner observer.
-- Keep at least the original5198fields, extending only the host capture so a
-- legitimate subsequent CPU launch has its full finite source lifetime.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
dofile(root..'/mk2ks_natural_mirror_no_raster_v3712.lua')
local device=manager.machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,channels,owners,taps=0,{},{},{}
local deadline=95
local slots={{actor=0x01060220,main=0x01060260,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,hp=0x01060ec0}}
local duration={[0xfffc]=1.15,[0xfffb]=1.15,[0xfffe]=2,[0xfffd]=2,
 [0xfffa]=1.4,[0xfff9]=0.85,[0xfff8]=3.85,[0xfff7]=2.75,
 [0x6b00]=45512/48000,[0x6b01]=40720/48000,[0x6b02]=66523/48000}
local function valid(a)return a>=0x01000000 and a<0x01400000 end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for name,index in pairs(manager.machine.devices[':'].items)do
   local field=name:match('m_mk2ks_battle_(.+)$')
   if field then owners[field]=emu.item(index)end
  end
  assert(owners.actor and owners.main and owners.health)
  for n=0,13 do local c=assert(channels[n]);assert(c.source_len and c.source_num and c.pos and c.loop and c.paused)end
 end
 if frame>=700 then
  for n=0,13 do
   local c=channels[n]
   print(string.format('MK2_MAUDIO_CHANNEL frame=%d seconds=%.12f channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
    frame,emu.time(),n,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.loop:read(0),c.paused:read(0)))
  end
  for n=1,2 do
   print(string.format('MK2_MAUDIO_OWNER frame=%d seconds=%.12f slot=%d actor=%08X main=%08X health=%d writes=0',
    frame,emu.time(),n,owners.actor:read(n-1),owners.main:read(n-1),owners.health:read(n-1)))
  end
 end
end)
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual physical mirror sound commands',function(at,value,mask)
 if at~=0x01d01030 or frame<700 then return end
 print(string.format('MK2_MAUDIO_SOUND frame=%d seconds=%.12f word=%04X mask=%04X pc=%08X a8=%08X a13=%08X writes=0 assistance=none',
  frame,emu.time(),value,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 local native=cpu.PC.value==0xffa13c90 or cpu.PC.value==0xffa13d60
 if duration[value]and not native then deadline=math.max(deadline,emu.time()+duration[value]+0.08)end
 if value>=0x6b00 and value<=0x6b02 then
  local a,m=cpu.A8.value,cpu.A13.value
  for n,s in ipairs(slots)do
   local actor,main=p:read_u32(s.actor),p:read_u32(s.main)
   if a==actor and m==main and valid(a)and valid(m)then
    print(string.format('MK2_MAUDIO_REQUEST frame=%d seconds=%.12f word=%04X slot=%d actor=%08X main=%08X owner=%08X id=%d state=%04X mode=%d health=%d writes=0',
     frame,emu.time(),value,n,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(m+0x1f0),p:read_u16(0x010601d0),p:read_u16(s.hp)))
   end
  end
 end
end)
emu.register_sound_update(function()
 if frame>=700 then
  local raw=manager.machine.sound:get_samples()
  print(string.format('MK2_BBAUDIO_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,emu.time(),#raw,
   raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
end)
emu.register_frame_done(function()
 if frame>=5198 and emu.time()>=deadline then
  print(string.format('MK2_MAUDIO_CAPTURE_END frame=%d seconds=%.12f not_before=%.12f writes=0',frame,emu.time(),deadline))
  manager.machine:exit()
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
