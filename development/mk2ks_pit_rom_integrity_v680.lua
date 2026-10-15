-- Read-only, before gameplay: retain the complete actual patched guest ROM.
local p=manager.machine.devices[':maincpu'].spaces.program
local output=assert(os.getenv('MK2KS_ROM_COMPARE_OUT'))
local frames=0
emu.register_frame(function()
 frames=frames+1
 if frames~=1 then return end
 local raw=p:read_range(0xff800000,0xffffffff,8,8)
 assert(#raw==1048576)
 local f=assert(io.open(output..'/guest_maincpu.bin','wb'));f:write(raw);f:close()
 print('MK2_PIT_ROM_CAPTURE bytes='..#raw..' writes=0 assistance=none')
end)
emu.register_stop(function()print('MK2_PIT_ROM_RESULT frames='..frames..' writes=0 assistance=none')end)
