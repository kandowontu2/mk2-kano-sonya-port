-- Same physical controller and retained observers; one initialized guest dump.
dofile('mk2ks_mileena_earned_fixed_v3824.lua')
local saved=false
emu.register_frame(function()
 if saved then return end
 saved=true
 local p=manager.machine.devices[':maincpu'].spaces.program
 local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
 local f=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'))
 f:write(raw);f:close()
 print('MK2_MILEENA_INITIAL_GUEST bytes=1048576 guest_writes=0 assistance=none')
end)
