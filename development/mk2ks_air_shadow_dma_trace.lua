-- Read-only full DMA commands during a stock fighter's jump.
dofile("mk2ks_ground_alignment_test.lua")
local frame,tap=0,nil
local registers={}
local shadow_rows={}
emu.register_frame(function()
    frame=frame+1
    if frame==1711 then
        for key,item in pairs(shadow_rows) do
            print(string.format("MK2_AIR_SHADOW_ROWS key=%s count=%d min=%d max=%d source=%08X",
                key,item.count,item.min,item.max,item.source))
        end
    end
    if frame~=1 then return end
    local p=manager.machine.devices[":maincpu"].spaces.program
    tap=p:install_write_tap(0x01a80000,0x01a800ff,"air shadow DMA",function(offset,data,mask)
        local reg=(offset-0x01a80000)//16
        registers[reg]=((registers[reg] or 0)&(~mask))|(data&mask)
        if reg~=1 or (data&0x8000)==0 or (frame~=1510 and frame~=1710) then return end
        local x,y,w,h=registers[4] or 0,registers[5] or 0,registers[6] or 0,registers[7] or 0
        local source=(registers[2] or 0)|((registers[3] or 0)<<16)
        if frame==1710 and h==1 and w>=16 and y>=350 and y<=510 and (data&0x000f)==8 then
            local key=string.format("x=%d w=%d cmd=%04X",x,w,data)
            local item=shadow_rows[key] or {count=0,min=999,max=0,source=source}
            item.count=item.count+1;item.min=math.min(item.min,y);item.max=math.max(item.max,y)
            shadow_rows[key]=item
        end
        if h<30 or w<10 or x>420 or y<240 then return end
        print(string.format("MK2_AIR_DMA frame=%d xy=%d,%d wh=%d,%d source=%08X cmd=%04X pal=%04X color=%04X",
            frame,x,y,w,h,source,data,registers[8] or 0,registers[9] or 0))
    end)
end)
