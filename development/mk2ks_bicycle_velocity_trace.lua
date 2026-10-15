-- Read-only diagnosis of requested versus published paired-body velocities.
dofile("mk2ks_bicycle_test.lua")
local frame,cpu,program=0,nil,nil
local taps={}
emu.register_frame(function()
    frame=frame+1
    if frame~=1400 then return end
    cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
    for _,address in ipairs({0xfff9de00,0xff831bd0,0xff828590,0xff8285b0,0xff828620}) do
        taps[#taps+1]=program:install_read_tap(address,address+15,"paired velocity diagnostic",function()
            if frame<1548 or frame>1567 then return end
            print(string.format("BIKE_VELOCITY frame=%d pc=%08X a0=%08X a1=%08X a6=%08X a7=%08X a8=%08X a9=%08X a10=%08X b4=%08X requests=%08X,%08X push=%d",frame,address,cpu.state.A0.value,cpu.state.A1.value,cpu.state.A6.value,cpu.state.A7.value,cpu.state.A8.value,cpu.state.A9.value,cpu.state.A10.value,cpu.state.B4.value,program:read_u32(0x010602d0),program:read_u32(0x01060ea0),program:read_u16(0x010619d0)))
        end)
    end
end)
emu.register_stop(function() for _,tap in ipairs(taps) do tap:remove() end end)
