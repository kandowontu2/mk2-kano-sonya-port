-- Read-only DMA audit during the grounded stance screenshot.
dofile("mk2ks_floor_shadow_audit.lua")
local frame,tap=0,nil
local registers={}
emu.register_frame(function()
    frame=frame+1
    if frame~=1 then return end
    local p=manager.machine.devices[":maincpu"].spaces.program
    tap=p:install_write_tap(0x01a80000,0x01a800ff,"ground shadow DMA",function(offset,data,mask)
        local reg=(offset-0x01a80000)//16
        registers[reg]=((registers[reg] or 0)&(~mask))|(data&mask)
        if reg~=1 or (data&0x8000)==0 or not ({[1450]=true,[1510]=true,[1540]=true,[1600]=true,[1850]=true})[frame] then return end
        local x,y,w,h=registers[4] or 0,registers[5] or 0,
            registers[6] or 0,registers[7] or 0
        local source=(registers[2] or 0)|((registers[3] or 0)<<16)
        if source<0x10000000 or source>=0x1a000000 or h<80 then return end
        local p=manager.machine.devices[":maincpu"].spaces.program
        local actor=p:read_u32(0x01060220)
        local task=p:read_u32(0x01060260)
        print(string.format("MK2_SHADOW_DMA frame=%d xy=%d,%d wh=%d,%d source=%08X command=%04X palette=%04X actorY=%d floor=%d stage=%d mode=%d",
            frame,x,y,w,h,source,data,registers[8] or 0,
            p:read_u16(actor+0xb0),p:read_u16(task+0x200),p:read_u16(0x0105ecd0),p:read_u16(0x01061b00)))
    end)
end)
