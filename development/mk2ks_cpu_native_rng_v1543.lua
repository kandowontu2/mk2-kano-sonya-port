-- Genuine unchanged cold scenario. Observe original RNG/hardware timing only.
-- No guest writes, item writes, state loads, RNG overrides or CPU decisions.
dofile('mk2ks_cpu_pair_display_probe_v1459.lua')
local cpu=manager.machine.devices[':maincpu'];local p=cpu.spaces.program
local frame,index,pending,taps=0,0,nil,{}
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local file=assert(io.open(assert(os.getenv('MK2KS_FLOOR_OUT'))..'/guest_maincpu.bin','wb'))
  for block=0,63 do
   local words={};for i=0,4095 do words[#words+1]=string.pack('<I4',p:read_u32(0xff800000+(block*4096+i)*32))end
   file:write(table.concat(words))
  end
  file:close()
  taps[#taps+1]=p:install_read_tap(0xc00001c0,0xc00001cf,'native RNG actual HCOUNT',function(at,data,mask)
   if cpu.state.PC.value~=0xff80ea90 then return end
   assert(not pending,'Original RNG read/return pairing')
   index=index+1;pending=index
   local a0=cpu.state.A0.value&0xffffffff
   local count=data&31
   local rotated=count==0 and a0 or ((a0<<count)|(a0>>(32-count)))&0xffffffff
   print(string.format('MK2_NATIVE_RNG_READ frame=%d index=%d seconds=%.12f pc=%08X mask=%04X seed=%08X a0=%08X hcount=%d rotation=%d expected=%08X actor=%08X main=%08X mode=%d caller=%08X writes=0 assistance=none',
    frame,index,emu.time(),cpu.state.PC.value,mask,p:read_u32(0x0105b950),a0,data,count,rotated,cpu.state.A8.value,cpu.state.A13.value,p:read_u16(0x010601d0),p:read_u32(cpu.state.SP.value+32)))
  end)
  taps[#taps+1]=p:install_read_tap(0xff80eab0,0xff80eabf,'native RNG actual result',function(at)
   if cpu.state.PC.value~=0xff80eac0 then return end
   assert(pending,'Original RNG result follows its hardware read')
   print(string.format('MK2_NATIVE_RNG_RESULT frame=%d index=%d seconds=%.12f pc=%08X value=%08X actor=%08X main=%08X writes=0 assistance=none',
    frame,pending,emu.time(),cpu.state.PC.value,cpu.state.A0.value,cpu.state.A8.value,cpu.state.A13.value))
   pending=nil
  end)
 end
end)
emu.register_stop(function()
 for _,tap in ipairs(taps)do tap:remove()end
 print(string.format('MK2_NATIVE_RNG_TERMINAL frame=%d calls=%d pending=%d writes=0 assistance=none',frame,index,pending or 0))
end)
