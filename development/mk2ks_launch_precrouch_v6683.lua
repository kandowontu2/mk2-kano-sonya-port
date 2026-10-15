-- Same complete driver/audio/owner inventory. Start a real crouch before
-- launch, then press HP; no state/position/health assignments or forced hit.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local source=read('mk2ks_launch_interrupt_v6680.lua')
source=change(source,"assert(load(driver,'@whole_original5099_two_cycle_input_driver','t',_G))()",[[driver=change(driver,"log('COMMAND',string.format('gap=",
 "rawset(_G,'MK2PORT_INTERRUPT_COMMAND',frame);log('COMMAND',string.format('gap=")
assert(load(driver,'@whole_original5099_two_cycle_input_driver','t',_G))()]])
source=change(source,'local frame,entry,serial=0,nil,0','local frame,entry,serial,command=0,nil,0,nil')
source=change(source,' if entry then\n  local age=frame-entry',[[ local actual_command=rawget(_G,'MK2PORT_INTERRUPT_COMMAND')
 if actual_command and command~=actual_command then command=actual_command;entry=nil end
 if command and not entry and frame>=command+assert(({ball=79,square=1,bicycle=7})[move])then
  high['P'..(3-side)..' Down']:set_value(1)
  log('INPUT',string.format('serial=%d slot=%d button=Down precrouch=1',serial+1,3-side))
 end
 if entry then
  local age=frame-entry]])
source=change(source,"  for slot,address in ipairs({0x010602f0,0x01060ec0})do",[[  taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'actual original uppercut instruction entry',function(at,data,mask)
   if at~=0xff870dc0 or regs.PC.value~=at+16 or not rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then return end
   local a,m=regs.A8.value,regs.A13.value
   log('UPPERCUT',string.format('entry=%08X pc=%08X opcode=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d action=%04X',
    at,regs.PC.value,data&0xffff,mask,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(m+0x1f0)))
  end)
  taps[#taps+1]=p:install_read_tap(0x01d00000,0x01d0000f,'actual physical input port read',function(at,data,mask)
   if rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then log('IO',string.format('at=%08X value=%04X mask=%04X pc=%08X',at,data&0xffff,mask,regs.PC.value))end
  end)
  for slot,address in ipairs({0x010602f0,0x01060ec0})do]])
assert(load(source,'@whole_current_interruption_with_precrouch_and_actual_uppercut_entry','t',_G))()
