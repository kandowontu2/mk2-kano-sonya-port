-- Existing physical interruption/KO driver is unchanged. Extra observer only
-- captures the complete actual guest program; no emulated state is written.
local allowed={
 ['mk2ks_blade_interrupt_v4.lua']=true,['mk2ks_bicycle_interrupt_v4.lua']=true,
 ['mk2ks_leg_interrupt_v4.lua']=true,['mk2ks_blade_lifecycle_test.lua']=true,
 ['mk2ks_bicycle_lifecycle_test.lua']=true}
local driver=assert(os.getenv('MK2KS_NATIVE_REGRESSION_DRIVER'))
assert(allowed[driver],'Exact established physical combat driver required')
local output=assert(os.getenv('MK2KS_NATIVE_REGRESSION_OUT'))
dofile(driver)
local captured=false
emu.register_frame(function()
 if captured then return end
 local p=manager.machine.devices[':maincpu'].spaces.program
 local raw=p:read_range(0xff800000,0xffffffff,8,8)
 assert(#raw==1048576,'Complete actual guest program')
 local file=assert(io.open(output..'/guest_maincpu.bin','wb'))
 file:write(raw);file:close();captured=true
 print('MK2_NATIVE_COMBAT_GUEST driver='..driver..' bytes='..#raw..' writes=0 assistance=none')
end)
