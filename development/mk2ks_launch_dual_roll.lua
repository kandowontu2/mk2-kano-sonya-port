-- Two actual selected Kanos, simultaneous physical LK charge/release.
-- Preserve entire native selection/body/health/recovery/audio observation.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local source=read('mk2ks_launch_interrupt_v6680.lua')
source=change(source,"driver=change(driver,\"then ready=frame;log('READY')end\",",
 [[driver=change(driver,"log('COMMAND',string.format('gap=%d forward=%s expectedEntry=%08X',gap,forward,spec[2]));",
 "rawset(_G,'MK2PORT_DUAL_COMMAND',frame);log('COMMAND',string.format('gap=%d forward=%s expectedEntry=%08X',gap,forward,spec[2]));")
driver=change(driver,"then ready=frame;log('READY')end",]])
source=change(source,[[   local actor=p:read_u32(side==1 and 0x01060220 or 0x01060df0)
   local main=p:read_u32(side==1 and 0x01060260 or 0x01060e30)
   assert(regs.A8.value==actor and regs.A13.value==main and p:read_u16(actor+0x1f0)==identity and p:read_u32(main+0xc0)==actor)
   entry=frame;serial=serial+1
   log('ENTRY',string.format('serial=%d slot=%d command=%04X pc=%08X actor=%08X main=%08X id=%d',serial,side,data,regs.PC.value,actor,main,identity))]],
 [[   local slot=regs.A8.value==p:read_u32(0x01060220)and 1 or 2
   local actor=p:read_u32(slot==1 and 0x01060220 or 0x01060df0)
   local main=p:read_u32(slot==1 and 0x01060260 or 0x01060e30)
   assert(move=='ball'and data==0x6b03 and regs.A8.value==actor and regs.A13.value==main and p:read_u16(actor+0x1f0)==17 and p:read_u32(main+0xc0)==actor)
   if slot==side then entry=frame;serial=serial+1 end
   log('ENTRY',string.format('serial=%d slot=%d command=%04X pc=%08X actor=%08X main=%08X id=%d',serial,slot,data,regs.PC.value,actor,main,17))]])
source=change(source,[[ if entry then
  local age=frame-entry
  if age>=1 and age<delay+9 then
   high['P'..(3-side)..' Down']:set_value(1)
   log('INPUT',string.format('serial=%d slot=%d button=Down',serial,3-side))
  end
  if age>=delay and age<delay+5 then
   high['P'..(3-side)..' High Punch']:set_value(1)
   log('INPUT',string.format('serial=%d slot=%d button=High_Punch',serial,3-side))
  end
 end]],
 [[ local command=rawget(_G,'MK2PORT_DUAL_COMMAND')
 if command and frame>=command and frame<command+84 then
  manager.machine.ioport.ports[':IN2'].fields['P'..(3-side)..' Low Kick']:set_value(1)
  log('INPUT',string.format('slot=%d button=Low_Kick dual=1',3-side))
 end]])
source=change(source,[[  for slot,address in ipairs({0x010602f0,0x01060ec0})do]],
 [[  for _,port in ipairs({{0x01600000,'IO'},{0x01600020,'LOW_IO'}})do
   taps[#taps+1]=p:install_read_tap(port[1],port[1]+15,'actual native dual physical input read',function(at,data,mask)
    if rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then log(port[2],string.format('at=%08X value=%04X mask=%04X pc=%08X',at,data&0xffff,mask,regs.PC.value))end
   end)
  end
  for slot,address in ipairs({0x010602f0,0x01060ec0})do]])
assert(load(source,'@whole_native_two_slot_simultaneous_roll_controls','t',_G))()
