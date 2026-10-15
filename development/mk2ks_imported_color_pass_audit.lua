-- Read-only inventory of imported graphics color-pass DMA commands.
dofile("mk2ks_selector_exit_test.lua")
local frame,tap=0,nil
local registers,groups={},{}
emu.register_frame(function()
    frame=frame+1
    if frame~=1 then return end
    local program=manager.machine.devices[":maincpu"].spaces.program
    tap=program:install_write_tap(0x01a80000,0x01a800ff,"MK3 port color pass inventory",function(offset,data,mask)
        local reg=(offset-0x01a80000)//16
        registers[reg]=((registers[reg] or 0)&(~mask))|(data&mask)
        if reg~=1 or (data&0x8000)==0 or (data&0x000f)~=8 then return end
        local source=(registers[2] or 0)|((registers[3] or 0)<<16)
        if source<0x10000000 or source>=0x1a000000 then return end
        local width,height=registers[6] or 0,registers[7] or 0
        local palette,color=registers[8] or 0,registers[9] or 0
        local key=string.format("cmd=%04X h=%d pal=%04X color=%04X",data,height,palette,color)
        local item=groups[key] or {count=0,first=frame,last=frame,source=source,width=width}
        item.count=item.count+1;item.last=frame
        groups[key]=item
    end)
end)
emu.register_stop(function()
    for key,item in pairs(groups) do
        print(string.format("MK2KS_IMPORTED_COLOR_PASS %s count=%d first=%d last=%d source=%08X width=%d",
            key,item.count,item.first,item.last,item.source,item.width))
    end
end)
