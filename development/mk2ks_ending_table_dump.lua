-- Read-only census of MKII's native ending scene callback table.
local done=false
emu.register_frame(function()
    if done then return end
    done=true
    local program=manager.machine.devices[":maincpu"].spaces.program
    for scene=0,25 do
        local slot=0xff9f7cf0+scene*32
        local record=program:read_u32(slot)
        local a,b,c,d=0,0,0,0
        if record>=0xff800000 and record<0xffe00000 then
            a,b,c,d=program:read_u32(record),program:read_u32(record+32),
                program:read_u32(record+64),program:read_u32(record+96)
        end
        print(string.format("MK2KS_ENDING_TABLE scene=%d slot=%08X record=%08X values=%08X,%08X,%08X,%08X",
            scene,slot,record,a,b,c,d))
    end
end)
