-- Original MK3 Sonya bicycle reference: real selection/inputs; read-only taps.
local frame,pulses,taps=0,{},{}
local cpu,program
local target=os.getenv("MK3_BICYCLE_TARGET") or "near"
assert(({near=true,far=true,block=true,duck=true,duck_block=true,air=true})[target])
local command=3900
local seen_root=false
local function pulse(field,first,duration)
    assert(field,"Missing original-game input field")
    pulses[#pulses+1]={field,first,first+(duration or 4)}
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function state(side)
    local object=program:read_u32(side==1 and 0x010609b0 or 0x01061560)
    local process=program:read_u32(side==1 and 0x010609f0 or 0x010615a0)
    return {actor=object,process=process,id=program:read_u16(object+0x1f0),
        x=signed(program:read_u16(object+0x90)),y=signed(program:read_u16(object+0xb0)),
        vx=program:read_u32(object+0x40),vy=program:read_u32(object+0x60),
        gravity=program:read_u32(object+0x20),pose=program:read_u32(object+0x1d0),
        action=program:read_u16(process+0x1f0),
        health=program:read_u16(side==1 and 0x01060a40 or 0x010615f0)}
end
mk3_bicycle_subscriptions={}
mk3_bicycle_subscriptions.frame=emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        local ports=manager.machine.ioport.ports
        local high,system=ports[":IN0"].fields,ports[":IN2"].fields
        for base=360,1320,480 do
            pulse(system["Coin 1"],base);pulse(system["1 Player Start"],base+20)
            pulse(high["P1 Down"],base+240);pulse(high["P1 High Punch"],base+320)
        end
        for _,first in ipairs({2960,2980,3000}) do pulse(system["Coin 2"],first) end
        pulse(system["2 Players Start"],3020)
        pulse(high["P1 Down"],3090);pulse(high["P1 High Punch"],3160)
        pulse(high["P2 Left"],3148);pulse(high["P2 High Punch"],3180)
        if target~="far" then pulse(high["P1 Right"],3800,80) end
        pulse(high["P1 Left"],command,3)
        pulse(high["P1 Left"],command+6,3)
        pulse(high["P1 Down"],command+12,3)
        pulse(high["P1 High Kick"],command+13,3)
        if target=="block" or target=="duck_block" then pulse(high["P2 Block"],3880,250) end
        if target=="duck" or target=="duck_block" then pulse(high["P2 Down"],3880,250) end
        if target=="air" then pulse(high["P2 Up"],3900,3) end
        for _,range in ipairs({{0xff831b80,0xff83239f,"main"},{0xff8323a0,0xff832bbf,"special"},
            {0xff83e620,0xff83e9ff,"sequence"}}) do
            taps[#taps+1]=program:install_read_tap(range[1],range[2],"original bicycle animation",function(offset,data,mask)
                if frame<3890 or frame>4200 or offset%32~=0 then return end
                if range[3]=="special" and offset==0xff8323c0 then seen_root=true end
                print(string.format("MK3_BICYCLE_ROOT frame=%d kind=%s at=%08X index=%d data=%04X actor=%08X action=%04X callers=%08X,%08X,%08X",frame,range[3],offset,(offset-range[1])//32,data,cpu.state.A8.value,program:read_u16(cpu.state.A13.value+0x1f0),program:read_u32(cpu.state.SP.value),program:read_u32(cpu.state.SP.value+32),program:read_u32(cpu.state.SP.value+64)))
            end)
        end
        local attack_table=program:read_u32(0xffa516f0)
        for index=0,23 do
            local descriptor=program:read_u32(attack_table+index*32)
            if descriptor>=0xff800000 then
                local words={}
                for word=0,8 do words[#words+1]=string.format("%04X",program:read_u16(descriptor+word*16)) end
                print(string.format("MK3_BICYCLE_DESCRIPTOR index=%d at=%08X words=%s",index,descriptor,table.concat(words,",")))
            end
        end
        taps[#taps+1]=program:install_read_tap(attack_table,attack_table+24*32-1,"original bicycle collision",function(offset,data,mask)
            if frame>=3890 and frame<=4200 and offset%32==0 then
                print(string.format("MK3_BICYCLE_ATTACK frame=%d index=%d actor=%08X callers=%08X,%08X",frame,(offset-attack_table)//32,cpu.state.A8.value,program:read_u32(cpu.state.SP.value),program:read_u32(cpu.state.SP.value+32)))
            end
        end)
    end
    for _,input in ipairs(pulses) do
        if frame==input[2] then input[1]:set_value(1) end
        if frame==input[3] then input[1]:clear_value() end
    end
    if frame==3800 then
        assert(state(1).id==1 and state(2).id==0,"Original-game Sonya/Kano selection failed")
        print("MK3_BICYCLE_SELECTED p1=1 p2=0 target="..target.." command=B,B,D+HK")
    end
    if frame>=3890 and frame<=4200 then
        for side=1,2 do
            local s=state(side)
            print(string.format("MK3_BICYCLE_STATE frame=%d side=%d id=%d action=%04X x=%d y=%d vx=%08X vy=%08X gravity=%08X pose=%08X health=%d",frame,side,s.id,s.action,s.x,s.y,s.vx,s.vy,s.gravity,s.pose,s.health))
        end
    end
    if frame==3800 or (frame>=3910 and frame<=4110 and frame%10==0) then manager.machine.video:snapshot() end
    if frame==4201 then
        assert(seen_root,"Bicycle command did not reach Sonya special animation 1")
        print("MK3_BICYCLE_REFERENCE_RESULT pass=true target="..target)
    end
end)
mk3_bicycle_subscriptions.stop=emu.register_stop(function()
    print("MK3_BICYCLE_REFERENCE_END frame="..frame)
    for _,tap in ipairs(taps) do tap:remove() end
end)
