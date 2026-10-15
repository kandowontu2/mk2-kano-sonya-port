-- Whole current two-cycle physical driver and passive source audio inventory.
-- The only new game input is the real opponent's crouching High Punch.
-- No guest, saved-item, health, position, RNG, or sound writes.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local getenv=os.getenv
os.getenv=function(key)
 local suffix=key:match('^MK2KS_HUMAN_SPECIAL_(.+)$')
 return suffix and getenv('MK2PORT_ACCEPT_'..suffix)or getenv(key)
end
local side=assert(tonumber(getenv('MK2PORT_ACCEPT_SIDE')))
local move=assert(getenv('MK2PORT_ACCEPT_MOVE'))
assert(side==1 or side==2)
local identity=assert(({ball=17,square=18,bicycle=18})[move])
local delay=assert(tonumber(getenv('MK2PORT_INTERRUPT_DELAY')))
assert(delay>=1 and delay<=30)
local driver=read('mk2ks_special_repeat_v5099.lua')
driver=change(driver,"then ready=frame;log('READY')end",
 "then ready=frame;rawset(_G,'MK2PORT_NATIVE_AUDIO_READY',frame);log('READY')end")
driver=change(driver,"if f==160 then completed=2;log('FINAL');",
 "if f==160 then rawset(_G,'MK2PORT_NATIVE_AUDIO_FINAL',frame);completed=2;log('FINAL');")
assert(load(driver,'@whole_original5099_two_cycle_input_driver','t',_G))()

local cpu=manager.machine.devices[':maincpu'];local p,regs=cpu.spaces.program,cpu.state
local high=manager.machine.ioport.ports[':IN0'].fields
local frame,entry,serial=0,nil,0
local channels,owners,taps={},{},{}
local function log(tag,text)
 print(string.format('MK2_INTERRUPT_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),text))
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then
    channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)
   end
  end
  for name,index in pairs(manager.machine.devices[':'].items)do
   local field=name:match('m_mk2ks_battle_(.+)$')
   if field then assert(not owners[field]);owners[field]=emu.item(index)end
  end
  assert(owners.actor and owners.main and owners.health and owners.id,'Actual compiled identity/health/actor/Main ownership items')
  for channel=10,13 do
   local c=assert(channels[channel]);assert(c.source_num and c.source_len and c.pos and c.loop and c.paused)
  end
  taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'native launch and real interruption timing',function(at,data,mask)
   if at~=0x01d01030 or mask~=0xffff or not(data==0x6b00 or data==0x6b01 or data==0x6b03)then return end
   local actor=p:read_u32(side==1 and 0x01060220 or 0x01060df0)
   local main=p:read_u32(side==1 and 0x01060260 or 0x01060e30)
   assert(regs.A8.value==actor and regs.A13.value==main and p:read_u16(actor+0x1f0)==identity and p:read_u32(main+0xc0)==actor)
   entry=frame;serial=serial+1
   log('ENTRY',string.format('serial=%d slot=%d command=%04X pc=%08X actor=%08X main=%08X id=%d',serial,side,data,regs.PC.value,actor,main,identity))
  end)
  for slot,address in ipairs({0x010602f0,0x01060ec0})do
   taps[#taps+1]=p:install_write_tap(address,address+15,'original physical incoming damage clock',function(at,data,mask)
    if not rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then return end
    local pc=regs.PC.value
    log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X op0=%04X op1=%04X op2=%04X',
     slot,at,p:read_u16(address),data&0xffff,mask,pc,regs.A8.value,regs.A13.value,p:read_u16(pc-48),p:read_u16(pc-32),p:read_u16(pc-16)))
   end)
  end
 end
 if entry then
  local age=frame-entry
  if age>=1 and age<delay+9 then
   high['P'..(3-side)..' Down']:set_value(1)
   log('INPUT',string.format('serial=%d slot=%d button=Down',serial,3-side))
  end
  if age>=delay and age<delay+5 then
   high['P'..(3-side)..' High Punch']:set_value(1)
   log('INPUT',string.format('serial=%d slot=%d button=High_Punch',serial,3-side))
  end
 end
 if rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then
  for slot=1,2 do
   log('OWNER',string.format('slot=%d actor=%08X main=%08X health=%d id=%d',slot,owners.actor:read(slot-1),owners.main:read(slot-1),owners.health:read(slot-1),owners.id:read(slot-1)))
  end
  for channel=10,13 do
   local c=channels[channel];local raw=c.pos:read_block(0,8);local pos=string.unpack('<d',raw)
   log('CHANNEL',string.format('channel=%d sample=%d length=%d position=%.17g bits=%s loop=%d paused=%d',
    channel,c.source_num:read(0),c.source_len:read(0),pos,raw:gsub('.',function(ch)return string.format('%02X',ch:byte())end),c.loop:read(0),c.paused:read(0)))
  end
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)

local source=read('mk2ks_current_tomb_winner_mix_observer_v5779.lua')
source=change(source,'local function active()return origin and frame<=origin+1100 end','local function active()return origin~=nil end')
source=change(source,'if at~=0xff8bdfe0 or cpu.PC.value~=at+16 or frame<=1 or origin then return end',
 'if at~=0xff8bdfe0 or cpu.PC.value~=at+16 or frame<=1 or origin or true then return end')
source=change(source,"assert(#taps==15,'Every audio observer retained')\n frame=frame+1",[[assert(#taps==15,'Every audio observer retained')
 frame=frame+1
 if not origin and rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then
  assert(frame==rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')and p:read_u16(0x010601d0)==2)
  local side=assert(tonumber(os.getenv('MK2PORT_ACCEPT_SIDE')))
  local id=assert(({ball=17,square=18,bicycle=18})[os.getenv('MK2PORT_ACCEPT_MOVE')])
  local a,m=p:read_u32(side==1 and 0x01060220 or 0x01060df0),p:read_u32(side==1 and 0x01060260 or 0x01060e30)
  assert(valid(a)and valid(m)and p:read_u16(a+0x1f0)==id and p:read_u32(m+0xc0)==a)
  origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X id=%d slot=%d',origin,a,m,id,side))
 end
 if active()then
  for slot=1,2 do
   local base=slot==1 and 0x010601f0 or 0x01060dc0
   local a,m=p:read_u32(base+0x30),p:read_u32(base+0x70)
   log('BINDING',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d',slot,a,m,
    valid(m)and p:read_u32(m+0xc0)or 0,valid(a)and p:read_u16(a+0x1f0)or-1,p:read_u16(base+0x90)))
  end
 end]])
source=change(source,"assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin,'Both entire native ROM inventories retained even if a physical attempt did not activate or recover')")
assert(load(source,'@whole_native5779_passive_interruption_audio','t',_G))()
