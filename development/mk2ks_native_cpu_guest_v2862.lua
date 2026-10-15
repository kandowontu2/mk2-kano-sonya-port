-- Unchanged natural P1-human/P2-CPU driver. Read-only actual guest capture.
dofile('mk2ks_cpu_recovery_probe_v1438.lua')
local output=assert(os.getenv('MK2KS_FLOOR_OUT'))
local captured=false
emu.register_frame(function()
 if captured then return end
 local raw=manager.machine.devices[':maincpu'].spaces.program:read_range(0xff800000,0xffffffff,8,8)
 assert(#raw==1048576,'Complete actual native guest')
 local file=assert(io.open(output..'/guest_maincpu.bin','wb'))
 file:write(raw);file:close();captured=true
 print('MK2_NATIVE_CPU_GUEST bytes=1048576 writes=0 assistance=none')
end)
