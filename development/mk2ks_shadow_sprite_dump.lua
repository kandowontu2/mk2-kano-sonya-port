-- Read-only one-frame DMA sprite capture; enable with -debug.
dofile("mk2ks_ground_alignment_test.lua")
local frame=0
local registers={}
local tap,enabled=nil,false
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local p=manager.machine.devices[":maincpu"].spaces.program
        tap=p:install_write_tap(0x01a80000,0x01a800ff,"sprite capture gate",function(offset,data,mask)
            local reg=(offset-0x01a80000)//16
            registers[reg]=((registers[reg] or 0)&(~mask))|(data&mask)
            if enabled or reg~=1 or (data&0x8000)==0 or frame~=1450 then return end
            local source=(registers[2] or 0)|((registers[3] or 0)<<16)
            if source~=tonumber(assert(os.getenv("MK2_SHADOW_TARGET_SOURCE")),16) then return end
            if (registers[7] or 0)<100 then return end
            manager.machine.debugger:command("midblit pngdma,1," ..
                assert(os.getenv("MK2_SHADOW_SPRITE_DIR")) .. ",0")
            enabled=true
            print(string.format("MK2_SHADOW_SPRITE_DUMP source=%08X width=%d height=%d",
                source,registers[6] or 0,registers[7] or 0))
        end)
    elseif frame==1451 and enabled then
        manager.machine.debugger:command("midblit pngdma,0")
    end
end)
