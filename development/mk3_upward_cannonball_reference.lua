-- Negative-control probe for a purported F,D,F+HK Kano upward cannonball.
-- This later-game move is not part of original MK3 arcade rev 2.1; this
-- script records real controls without changing game memory. It does not
-- alone prove move absence, and is not a port acceptance test.
local frame,pulses=0,{}
local cpu,program
local command=3900
local function pulse(field,first,duration)
    assert(field,"Missing original-game input field")
    pulses[#pulses+1]={field,first,first+(duration or 3)}
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function state(side)
    local actor=program:read_u32(side==1 and 0x010609b0 or 0x01061560)
    local process=program:read_u32(side==1 and 0x010609f0 or 0x010615a0)
    return {actor=actor,id=program:read_u16(actor+0x1f0),
        x=signed(program:read_u16(actor+0x90)),
        y=signed(program:read_u16(actor+0xb0)),
        vx=program:read_u32(actor+0x40),
        vy=program:read_u32(actor+0x60),
        gravity=program:read_u32(actor+0x20),
        pose=program:read_u32(actor+0x1d0),
        action=program:read_u16(process+0x1f0),
        health=program:read_u16(side==1 and 0x01060a40 or 0x010615f0)}
end
mk3_upball_subscriptions={}
mk3_upball_subscriptions.frame=emu.add_machine_frame_notifier(function()
    frame=frame+1
    if frame==1 then
        cpu=manager.machine.devices[":maincpu"]
        program=cpu.spaces.program
        local ports=manager.machine.ioport.ports
        local high,system=ports[":IN0"].fields,ports[":IN2"].fields
        for base=360,1320,480 do
            pulse(system["Coin 1"],base)
            pulse(system["1 Player Start"],base+20)
            for _,offset in ipairs({180,220,260}) do pulse(high["P1 Right"],base+offset) end
            pulse(high["P1 High Punch"],base+320)
        end
        for _,first in ipairs({2960,2980,3000}) do pulse(system["Coin 2"],first) end
        pulse(system["2 Players Start"],3020)
        for _,first in ipairs({3060,3090,3120}) do pulse(high["P1 Right"],first) end
        pulse(high["P1 High Punch"],3160)
        pulse(high["P2 High Punch"],3180)
        pulse(high["P1 Right"],command,3)
        pulse(high["P1 Down"],command+6,3)
        pulse(high["P1 Right"],command+12,3)
        pulse(high["P1 High Kick"],command+13,3)
        if os.getenv("MK3_UPBALL_TARGET")=="air" then
            pulse(high["P2 Up"],command+12,3)
        elseif os.getenv("MK3_UPBALL_TARGET")=="block" then
            pulse(high["P2 Block"],command-20,180)
        end
    end
    for _,input in ipairs(pulses) do
        if frame==input[2] then input[1]:set_value(1) end
        if frame==input[3] then input[1]:clear_value() end
    end
    if frame==3800 then
        local a,b=state(1),state(2)
        assert(a.id==0,"Original-game Kano selection failed")
        print(string.format("MK3_UPBALL_SELECTED p1=%d p2=%d x=%d,%d",a.id,b.id,a.x,b.x))
    end
    if frame>=command-10 and frame<=command+200 then
        for side=1,2 do
            local s=state(side)
            if frame<=command+35 or frame%4==0 then
                print(string.format("MK3_UPBALL_STATE frame=%d side=%d id=%d action=%04X x=%d y=%d vx=%08X vy=%08X gravity=%08X pose=%08X health=%d",
                    frame,side,s.id,s.action,s.x,s.y,s.vx,s.vy,s.gravity,s.pose,s.health))
            end
        end
    end
    if frame==3800 or (frame>=command+15 and frame<=command+160 and frame%10==0) then
        manager.machine.video:snapshot()
    end
end)
mk3_upball_subscriptions.stop=emu.add_machine_stop_notifier(function()
    print("MK3_UPBALL_REFERENCE_END frame="..frame)
end)
