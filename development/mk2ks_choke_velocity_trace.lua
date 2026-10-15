-- Read-only diagnostic: identify native writes to the released actor velocity.
dofile("mk2ks_choke_test.lua")
local frame,program,cpu=0,nil,nil
local taps={}
emu.register_frame(function()
    frame=frame+1
    if frame~=1400 then return end
    cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
    local side=tonumber(os.getenv("MK2KS_CHOKE_SIDE") or "2")
    local victim=program:read_u32(side==1 and 0x01060df0 or 0x01060220)
    taps[#taps+1]=program:install_write_tap(victim+0x40,victim+0x7f,"choke velocity writer",function(offset,data,mask)
        if frame<1550 or frame>1630 then return end
        print(string.format("MK2KS_CHOKE_VELOCITY frame=%d at=%08X data=%08X mask=%08X pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X stack=%08X,%08X,%08X",
            frame,offset,data,mask,cpu.state.PC.value,cpu.state.A0.value,cpu.state.A1.value,
            cpu.state.A8.value,cpu.state.A13.value,program:read_u32(cpu.state.SP.value),
            program:read_u32(cpu.state.SP.value+32),program:read_u32(cpu.state.SP.value+64)))
    end)
end)
emu.register_stop(function() for _,tap in ipairs(taps) do tap:remove() end end)
