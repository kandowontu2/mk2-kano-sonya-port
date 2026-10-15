-- Preserve the whole grounded controller. Correct the passive IN0 hook:
-- 01D00000 is DCS status; real MK2 IN0/IN2 are 01600000/01600020.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local adapter=read('mk2ks_launch_ground_counter_v6703.lua')
local correction=[=[
source=change(source,[[p:install_read_tap(0x01d00000,0x01d0000f,'actual physical input port read']],
 [[p:install_read_tap(0x01600000,0x0160000f,'actual physical input port read']])
source=change(source,[[  for slot,address in ipairs({0x010602f0,0x01060ec0})do]],[[  taps[#taps+1]=p:install_read_tap(0x01600020,0x0160002f,'actual physical low-button port read',function(at,data,mask)
   if rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then log('LOW_IO',string.format('at=%08X value=%04X mask=%04X pc=%08X',at,data&0xffff,mask,regs.PC.value))end
  end)
  for slot,address in ipairs({0x010602f0,0x01060ec0})do]])
]=]
adapter=change(adapter,'extra.."assert(load(source,', 'extra..'+string.format('%q',correction)..'.."assert(load(source,')
assert(load(adapter,'@whole_ground_controller_actual_native_IN0_IN2_hooks','t',_G))()
