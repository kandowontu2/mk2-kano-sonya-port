-- Extra read-only full-component/render evidence around the cold join driver.
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local frame,collecting,taps,children=0,false,{},{}
local function signed(v)return v>=0x8000 and v-0x10000 or v end
local function valid(v)return v>=0x01000000 and v<0x01100000 end
local choreography=os.getenv("MK2KS_PROJECTILE_CHOREOGRAPHY")=="1"
local function armed()
    return os.getenv("MK2KS_PROJECTILE_OBSERVER_ONLY")~="1" or _G.MK2KS_PROJECTILE_OBSERVER_ARMED==true
end
local child_entries=choreography and {0xfffc6000,0xfffc7000} or {0xff8afc10}
for _,entry in ipairs(child_entries) do
taps[#taps+1]=p:install_read_tap(entry,entry+15,"full projectile render child",function(at)
    if at~=entry or collecting or not armed() then return end
    collecting=true
    local child,process=cpu.A8.value,cpu.A13.value
    if valid(child) and valid(process) then
        children[child]={process=process}
        print(string.format("MK2_IMPACT_CHILD frame=%d child=%08X process=%08X id=%d writes=0",frame,child,process,p:read_u16(child+0x1f0)))
    end
    collecting=false
end)
end
local dma={}
taps[#taps+1]=p:install_read_tap(0xff804570,0xff80457f,"native effect component culling",function(at)
    if at~=0xff804570 or collecting or not armed() then return end
    local source=cpu.A11.value
    if not (choreography and source>=0x0f020000 and source<0x0f040000 or
            source>=0x0f280000 and source<(choreography and 0x0f310000 or 0x0f300000)) then return end
    print(string.format("MK2_IMPACT_CULL frame=%d pc=%08X graphic=%08X position=%08X size=%08X clip_min=%08X clip_max=%08X buffer=%08X writes=0",
        frame,cpu.PC.value,source,cpu.A10.value,cpu.A9.value,cpu.A14.value,cpu.A13.value,cpu.A5.value))
end)
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,"native projectile DMA evidence",function(at,data)
    if collecting then return end
    local reg=(at-0x01a80000)//16
    dma[reg]=data&0xffff
    if reg~=1 or (data&0x8000)==0 or not armed() then return end
    local source=(dma[2] or 0)|((dma[3] or 0)<<16)
    if not (source>=0x0f020000 and source<0x0f040000 or source>=0x0f280000 and source<(choreography and 0x0f310000 or 0x0f300000)) then return end
    print(string.format("MK2_IMPACT_DMA frame=%d pc=%08X graphic=%08X command=%04X x=%d y=%d width=%d height=%d palette=%04X color=%04X scale_x=%04X scale_y=%04X writes=0",
        frame,cpu.PC.value,source,data&0xffff,signed(dma[4] or 0),signed(dma[5] or 0),dma[6] or 0,dma[7] or 0,dma[8] or 0,dma[9] or 0,dma[10] or 0,dma[11] or 0))
end)
taps[#taps+1]=p:install_read_tap(0xff8b6820,0xff8b682f,"full projectile render retirement",function(at)
    if at~=0xff8b6820 or collecting or not armed() then return end
    local child=cpu.A8.value
    if children[child] then
        print(string.format("MK2_IMPACT_RETIRE frame=%d child=%08X process=%08X writes=0",frame,child,cpu.A13.value))
        children[child]=nil
    end
end)
emu.register_frame(function()
    collecting=true;frame=frame+1
    if not armed() then collecting=false;return end
    for child,v in pairs(children) do
        local pose=p:read_u32(child+0x1d0)
        local id=p:read_u16(child+0x1f0)
        local list=p:read_u32(child+0x1a0)
        local count=0
        if pose>=0xfe800000 then
            for i=0,15 do
                local descriptor=p:read_u32(pose+i*32)
                if descriptor==0 then break end
                count=count+1
                local component=list+i*0x70
                print(string.format("MK2_IMPACT_COMPONENT frame=%d child=%08X pose=%08X index=%d descriptor=%08X graphic=%08X command=%04X width=%d height=%d dx=%d dy=%d colors=%04X writes=0",
                    frame,child,pose,i,descriptor,p:read_u32(component),p:read_u16(component+0x40),p:read_u16(component+0x20),p:read_u16(component+0x30),
                    signed(p:read_u16(component+0x50)),signed(p:read_u16(component+0x60)),p:read_u16(component+0x40)))
            end
        end
        print(string.format("MK2_IMPACT_FIELD frame=%d child=%08X process=%08X id=%d action=%04X pose=%08X components=%d x=%d y=%d vx=%08X vy=%08X flags=%04X snapshot=impact_%d.png writes=0",
            frame,child,v.process,id,p:read_u16(v.process+0x1f0),pose,count,signed(p:read_u16(child+0x90)),signed(p:read_u16(child+0xb0)),
            p:read_u32(child+0x40),p:read_u32(child+0x60),p:read_u16(child+0xf0),frame))
        manager.machine.screens[":screen"]:snapshot("impact_"..frame..".png")
    end
    collecting=false
end)
emu.register_stop(function()for _,tap in ipairs(taps) do tap:remove() end end)
if os.getenv("MK2KS_PROJECTILE_OBSERVER_ONLY")~="1" then dofile("mk2ks_join_projectile_probe.lua") end
