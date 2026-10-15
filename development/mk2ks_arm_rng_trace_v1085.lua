-- Read-only diagnosis: observe the ORIGINAL RNG's actual HCOUNT read/result.
-- Never reread HCOUNT, replace random values, or write guest state.
dofile('mk2ks_arm_palette_trace_v1073.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,serial=0,0
local taps,pending={},nil
local function active()
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 return start and frame-start<=650
end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_ARM_RNG_V1085_%s frame=%d writes=0 assistance=none %s',tag,frame,text))
end
taps[#taps+1]=p:install_read_tap(0xff80e980,0xff80e98f,'original RNG entry',function(at)
 if at~=0xff80e980 or not active()then return end
 assert(not pending,'Original RNG unexpectedly re-entered')
 serial=serial+1
 local sp=cpu.SP.value;local main=cpu.A13.value;local actor=cpu.A8.value
 pending={serial=serial,seed=p:read_u32(0x0105b950),caller=p:read_u32(sp),main=main,actor=actor}
 log('ENTRY',string.format('serial=%d seed=%08X caller=%08X main=%08X actor=%08X id=%d action=%08X',
  serial,pending.seed,pending.caller,main,actor,valid(actor)and p:read_u16(actor+0x1f0)or -1,
  valid(main)and p:read_u32(main+0x1f0)or 0))
end)
taps[#taps+1]=p:install_read_tap(0xc00001c0,0xc00001cf,'actual native HCOUNT entropy',function(at,data)
 if at~=0xc00001c0 or not pending then return end
 assert(not pending.hcount,'More than one HCOUNT read in original RNG')
 pending.hcount=data&0xffff;pending.before=cpu.A0.value
 log('HCOUNT',string.format('serial=%d pc=%08X count=%04X before=%08X stored_seed=%08X',
  pending.serial,cpu.PC.value,pending.hcount,pending.before,p:read_u32(0x0105b950)))
end)
taps[#taps+1]=p:install_read_tap(0xff80eaa0,0xff80eaaf,'original RNG rotated result',function(at)
 if at~=0xff80eaa0 or not pending then return end
 assert(pending.hcount,'Original RNG missed its HCOUNT read')
 log('RESULT',string.format('serial=%d count=%04X before=%08X result=%08X a1=%08X stored_seed=%08X',
  pending.serial,pending.hcount,pending.before,cpu.A0.value,cpu.A1.value,p:read_u32(0x0105b950)))
 pending=nil
end)
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'all native effects for RNG diagnosis',function(at)
 if at~=0xff804410 or not active()or cpu.PC.value~=0xff804420 then return end
 local actor=cpu.A0.value;if not valid(actor)then return end
 log('FIFO',string.format('actor=%08X source=%08X id=%d bank=%04X x=%d y=%d size=%08X xy=%08X command=%08X cursor=%08X',
  actor,cpu.A11.value,p:read_u16(actor+0x1f0),p:read_u16(actor+0x140),p:read_i16(actor+0x90),
  p:read_i16(actor+0xb0),cpu.A9.value,cpu.A10.value,cpu.A12.value,cpu.A1.value))
end)
emu.register_frame(function()frame=frame+1;assert(#taps==4)end)
