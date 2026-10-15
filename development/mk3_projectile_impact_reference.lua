-- Original-game input-only impact reference. No actor/health/position writes.
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local frame,collecting,actors,taps=0,false,{},{}
local sonya=os.getenv("MK3_PROJECTILE_TARGET")=="sonya"
local id=sonya and 1 or 0
local function signed(v) return v>=0x8000 and v-0x10000 or v end
taps[#taps+1]=p:install_read_tap(0xffa516c0,0xffa516cf,"impact reference child",function(at)
    if at~=0xffa516c0 or collecting or frame<3890 or frame>4400 then return end
    collecting=true
    local actor=cpu.A8.value
    if actor>=0x01000000 and actor<0x01400000 and p:read_u16(actor+0x1f0)==id and
       actor~=p:read_u32(0x010609b0) and actor~=p:read_u32(0x01061560) then
        if not actors[actor] then
            actors[actor]={process=cpu.A13.value,last=frame}
            print(string.format("MK3_IMPACT_CHILD frame=%d actor=%08X process=%08X id=%d writes=0",frame,actor,cpu.A13.value,id))
            taps[#taps+1]=p:install_write_tap(actor+0x1d0,actor+0x1ef,"impact reference pose",function(a,data)
                if collecting or frame<3890 or frame>4400 then return end
                print(string.format("MK3_IMPACT_POSE frame=%d actor=%08X address=%08X data=%04X pc=%08X writes=0",frame,actor,a,data&0xffff,cpu.PC.value))
            end)
        end
        actors[actor].last=frame
    end
    collecting=false
end)
emu.register_frame(function()
    collecting=true;frame=frame+1
    if frame>=3890 and frame<=4400 then
        for actor,v in pairs(actors) do
            if frame<=v.last+45 then
                print(string.format("MK3_IMPACT_FIELD frame=%d actor=%08X process=%08X id=%d x=%d y=%d pose=%08X flags=%04X writes=0",frame,actor,v.process,
                    p:read_u16(actor+0x1f0),signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),p:read_u32(actor+0x1d0),p:read_u16(actor+0x160)))
                if frame>=3935 and frame<=3990 then manager.machine.screens[":screen"]:snapshot("impact_ref_"..frame..".png") end
            end
        end
    end
    collecting=false
end)
emu.register_stop(function()for _,tap in ipairs(taps) do tap:remove() end end)
dofile("mk3_knife_geometry_reference.lua")
