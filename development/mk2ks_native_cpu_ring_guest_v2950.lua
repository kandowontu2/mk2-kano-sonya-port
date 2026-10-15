-- Existing physical extended-match inputs and native observations unchanged.
-- Capture complete actual guest independently; never write game state.
dofile('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')
local captured=false
emu.register_frame(function()
 if captured then return end
 local raw=manager.machine.devices[':maincpu'].spaces.program:read_range(0xff800000,0xffffffff,8,8)
 assert(#raw==1048576,'Complete actual guest')
 local file=assert(io.open(assert(os.getenv('MK2KS_FLOOR_OUT'))..'/guest_maincpu.bin','wb'))
 file:write(raw);file:close();captured=true
 print('MK2_NATIVE_CPU_GUEST bytes=1048576 writes=0 assistance=none')
end)
