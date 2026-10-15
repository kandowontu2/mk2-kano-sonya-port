-- Native original-game release/intro/flight reference. Inputs only, no writes.
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local frame,collecting,objects,taps=0,false,{},{}
local sonya=os.getenv("MK3_PROJECTILE_TARGET")=="sonya"
local id=sonya and 1 or 0
local function signed(v)return v>=0x8000 and v-0x10000 or v end
local function valid(v)return v>=0x01000000 and v<0x01400000 end
taps[#taps+1]=p:install_read_tap(0xff963200,0xff96320f,"original release group",function(at)
    if at~=0xff963200 or collecting or frame<3890 or frame>4400 then return end
    collecting=true
    local actor,group,process=cpu.A8.value,cpu.A0.value,cpu.A13.value
    if valid(actor) and p:read_u16(actor+0x1f0)==id and
       (sonya and group>=0xff83dbe0 and group<=0xff83e5c0 or not sonya and group>=0xff82ec40 and group<=0xff82f6a0) then
        local body=actor==p:read_u32(0x010609b0)
        objects[actor]={process=process,last=frame,body=body}
        print(string.format("MK3_CHOREO_GROUP frame=%d pc=%08X actor=%08X process=%08X id=%d body=%d group=%08X x=%d y=%d vx=%08X vy=%08X flags=%04X writes=0",
            frame,cpu.PC.value,actor,process,id,body and 1 or 0,group,signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),
            p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u16(actor+0xf0)))
    end
    collecting=false
end)
emu.register_frame(function()
    collecting=true;frame=frame+1
    if frame>=3890 and frame<=4400 then
        local actor,process=p:read_u32(0x010609b0),p:read_u32(0x010609f0)
        if valid(actor) and valid(process) then
            print(string.format("MK3_CHOREO_HUMAN frame=%d actor=%08X process=%08X id=%d action=%04X pose=%08X x=%d y=%d vx=%08X vy=%08X writes=0",
                frame,actor,process,p:read_u16(actor+0x1f0),p:read_u16(process+0x1f0),p:read_u32(actor+0x1d0),signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),
                p:read_u32(actor+0x40),p:read_u32(actor+0x60)))
        end
        for actor,v in pairs(objects) do
            if frame<=v.last+5 then
                print(string.format("MK3_CHOREO_FIELD frame=%d actor=%08X process=%08X id=%d body=%d pose=%08X x=%d y=%d vx=%08X vy=%08X flags=%04X writes=0",
                    frame,actor,v.process,p:read_u16(actor+0x1f0),v.body and 1 or 0,p:read_u32(actor+0x1d0),signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),
                    p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u16(actor+0xf0)))
            end
        end
        if frame>=3906 and frame<=3970 then manager.machine.screens[":screen"]:snapshot("choreo_ref_"..frame..".png") end
    end
    collecting=false
end)
emu.register_stop(function()for _,tap in ipairs(taps) do tap:remove() end end)
dofile("mk3_knife_geometry_reference.lua")
