-- Current native full-release/intro/travel tap. Inputs supplied by the ordinary
-- real-join driver; no memory, position, health, identity or animation writes.
assert(os.getenv("MK2KS_PROJECTILE_CHOREOGRAPHY")=="1")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local frame,collecting,taps,active=0,false,{},{}
local slots={{actor=0x01060220,main=0x01060260,state=0x010601f0},
             {actor=0x01060df0,main=0x01060e30,state=0x01060dc0}}
local function valid(v)return v>=0x01000000 and v<0x01100000 end
local function signed(v)return v>=0x8000 and v-0x10000 or v end
local function armed()
    return os.getenv("MK2KS_PROJECTILE_OBSERVER_ONLY")~="1" or _G.MK2KS_PROJECTILE_OBSERVER_ARMED==true
end
taps[#taps+1]=p:install_read_tap(0xff838790,0xff83879f,"native full projectile groups",function(at)
    if at~=0xff838790 or collecting or not armed() or p:read_u16(slots[1].state)~=1 or p:read_u16(slots[2].state)~=1 then return end
    collecting=true
    local actor,group,process=cpu.A8.value,cpu.A0.value,cpu.A13.value
    if valid(actor) and valid(process) then
        local id=p:read_u16(actor+0x1f0)
        local body=false
        for side,slot in ipairs(slots) do
            if actor==p:read_u32(slot.actor) then
                body=true
                if group==0xfe82f400 or group==0xfe83dbe0 then active[side]=frame end
            end
        end
        if (id==17 or id==18) and (group>=0xfe82f400 and group<=0xfe82f6a0 or
            group>=0xfe83dbe0 and group<=0xfe83dec0 or group>=0xff614000 and group<0xff614900+0x300 or
            group>=0xff60c000 and group<0xff60c700) then
            print(string.format("MK2_CHOREO_GROUP frame=%d pc=%08X actor=%08X process=%08X id=%d body=%d group=%08X x=%d y=%d vx=%08X vy=%08X flags=%04X writes=0",
                frame,cpu.PC.value,actor,process,id,body and 1 or 0,group,signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),
                p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u16(actor+0xf0)))
        end
    end
    collecting=false
end)
emu.register_frame(function()
    collecting=true;frame=frame+1
    for side,start in pairs(active) do
        if frame>start and frame<=start+65 then
            local slot=slots[side]
            local actor,process=p:read_u32(slot.actor),p:read_u32(slot.main)
            if valid(actor) and valid(process) then
                print(string.format("MK2_CHOREO_HUMAN frame=%d side=%d actor=%08X process=%08X id=%d action=%04X pose=%08X x=%d y=%d floor=%d vx=%08X vy=%08X flags=%04X writes=0",
                    frame,side,actor,process,p:read_u16(actor+0x1f0),p:read_u16(process+0x1f0),p:read_u32(actor+0x1d0),
                    signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),signed(p:read_u16(process+0x200)),
                    p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u16(process+0x210)))
                manager.machine.screens[":screen"]:snapshot("choreo_"..frame..".png")
            end
        end
    end
    collecting=false
end)
emu.register_stop(function()for _,tap in ipairs(taps) do tap:remove() end end)
dofile("mk2ks_projectile_impact_probe.lua")
