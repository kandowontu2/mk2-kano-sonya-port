-- Read-only actor/object comparison at the same grounded combat frame.
dofile("mk2ks_ground_alignment_test.lua")
local frame=0
emu.register_frame(function()
    frame=frame+1
    if frame~=1450 then return end
    local p=manager.machine.devices[":maincpu"].spaces.program
    print(string.format("MK2_FLOOR_CAMERA a=%04X b=%04X c=%04X d=%04X stage=%04X",
        p:read_u16(0x0105d120),p:read_u16(0x0105d130),
        p:read_u16(0x0105d140),p:read_u16(0x0105d150),p:read_u16(0x0105ecd0)))
    for side,pointer in ipairs({0x01060220,0x01060df0}) do
        local actor=p:read_u32(pointer)
        print(string.format("MK2_FLOOR_ACTOR side=%d base=%08X id=%04X pose=%08X x=%d y=%d",
            side,actor,p:read_u16(actor+0x1f0),p:read_u32(actor+0x1d0),
            p:read_u16(actor+0x90),p:read_u16(actor+0xb0)))
        for offset=0x80,0x210,0x20 do
            print(string.format("MK2_FLOOR_ACTOR_WORDS side=%d offset=%03X value=%08X",
                side,offset,p:read_u32(actor+offset)))
        end
        local cache=p:read_u32(actor+0x1a0)
        for part=0,7 do
            local at=cache+part*0x70
            local source=p:read_u32(at)
            if source==0 then break end
            print(string.format("MK2_FLOOR_PART side=%d part=%d source=%08X xoff=%d yoff=%d width=%d height=%d",
                side,part,source,p:read_u16(at+0x50),p:read_u16(at+0x60),
                p:read_u16(at+0x20),p:read_u16(at+0x30)))
        end
    end
    local found=0
    for base=0x01020000,0x01060000,0x10 do
        local pose=p:read_u32(base+0x1d0)
        local gfx=p:read_u32(base+0x1a0)
        if gfx>=0x01000000 and gfx<0x01100000 then
            local id=p:read_u16(base+0x1f0)
            local x=p:read_u16(base+0x90)
            local y=p:read_u16(base+0xb0)
            if x>=200 and x<=1400 and y>=0 and y<=300 then
                found=found+1
                if found<=80 then
                    print(string.format("MK2_FLOOR_OBJECT base=%08X id=%04X pose=%08X x=%d y=%d gfx=%08X flags=%08X owner=%08X",
                        base,id,pose,x,y,gfx,p:read_u32(base+0xf0),p:read_u32(base+0x190)))
                end
            end
        end
    end
    print(string.format("MK2_FLOOR_OBJECT_COUNT count=%d",found))
end)
