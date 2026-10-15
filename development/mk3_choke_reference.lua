-- Original MK3 Kano D,F+LP reference. Real selection/inputs, read-only memory.
local frame,pulses,taps=0,{},{}
local cpu,program
local target=os.getenv("MK3_CHOKE_TARGET") or "near"
local victim=os.getenv("MK3_CHOKE_VICTIM") or "sonya"
local side=tonumber(os.getenv("MK3_CHOKE_SIDE") or "1")
assert(side==1 or side==2)
assert(side==1 or victim=="kano", "P2 original reference currently uses a Kano mirror")
assert(({near=true,far=true,block=true,duck=true,duck_block=true,air=true})[target])
assert(victim=="sonya" or victim=="kano" or victim=="liu_kang")
local command=3900
local approach=tonumber(os.getenv("MK3_CHOKE_APPROACH") or "80")
assert(approach>=0 and approach<=80,"Keep approach before the command window")
local function pulse(field,first,duration)
    assert(field,"Missing original-game input field")
    pulses[#pulses+1]={field,first,first+(duration or 4)}
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function state(index)
    local object=program:read_u32(index==1 and 0x010609b0 or 0x01061560)
    local process=program:read_u32(index==1 and 0x010609f0 or 0x010615a0)
    return {actor=object,process=process,id=program:read_u16(object+0x1f0),
        x=signed(program:read_u16(object+0x90)),y=signed(program:read_u16(object+0xb0)),
        vx=program:read_u32(object+0x40),vy=program:read_u32(object+0x60),
        pose=program:read_u32(object+0x1d0),action=program:read_u16(process+0x1f0),
        health=program:read_u16(index==1 and 0x01060a40 or 0x010615f0)}
end
mk3_choke_subscriptions={}
mk3_choke_subscriptions.frame=emu.add_machine_frame_notifier(function()
    frame=frame+1
    if frame==1 then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        local ports=manager.machine.ioport.ports
        local high,low,system=ports[":IN0"].fields,ports[":IN1"].fields,ports[":IN2"].fields
        for base=360,1320,480 do
            pulse(system["Coin 1"],base);pulse(system["1 Player Start"],base+20)
            for _,offset in ipairs({180,220,260}) do pulse(high["P1 Right"],base+offset) end
            pulse(high["P1 High Punch"],base+320)
        end
        for _,first in ipairs({2960,2980,3000}) do pulse(system["Coin 2"],first) end
        pulse(system["2 Players Start"],3020)
        for _,first in ipairs({3060,3090,3120}) do pulse(high["P1 Right"],first) end
        pulse(high["P1 High Punch"],3160)
        if victim=="kano" then pulse(high["P2 Left"],3148)
        elseif victim=="sonya" then
            for _,first in ipairs({3100,3160,3220,3280}) do pulse(high["P2 Left"],first) end
            pulse(high["P2 Down"],3340)
        end
        pulse(high["P2 High Punch"],victim=="sonya" and 3400 or 3180)
        local attacker="P"..side.." "
        local defender="P"..(3-side).." "
        local forward=side==1 and "Right" or "Left"
        if target~="far" then pulse(high[attacker..forward],3800,approach) end
        pulse(high[attacker.."Down"],command,3)
        pulse(high[attacker..forward],command+5,3)
        pulse(low[attacker.."Low Punch"],command+6,3)
        if target=="block" or target=="duck_block" then pulse(high[defender.."Block"],3880,220) end
        if target=="duck" or target=="duck_block" then pulse(high[defender.."Down"],3880,220) end
        if target=="air" then pulse(high[defender.."Up"],3895,3) end
        for _,range in ipairs({{0xff823ca0,0xff8244bf,"main"},{0xff8244c0,0xff824cdf,"special"}}) do
            taps[#taps+1]=program:install_read_tap(range[1],range[2],"original choke animation",function(offset,data,mask)
                if frame<3890 or frame>4200 or offset%32~=0 then return end
                print(string.format("MK3_CHOKE_ROOT frame=%d kind=%s index=%d actor=%08X process=%08X action=%04X callers=%08X,%08X,%08X",frame,range[3],(offset-range[1])//32,cpu.state.A8.value,cpu.state.A13.value,program:read_u16(cpu.state.A13.value+0x1f0),program:read_u32(cpu.state.SP.value),program:read_u32(cpu.state.SP.value+32),program:read_u32(cpu.state.SP.value+64)))
            end)
        end
        local attack_table=program:read_u32(0xffa516d0)
        for index=0,23 do
            local descriptor=program:read_u32(attack_table+index*32)
            if descriptor>=0xff800000 then
                local words={}
                for word=0,8 do words[#words+1]=string.format("%04X",program:read_u16(descriptor+word*16)) end
                print(string.format("MK3_CHOKE_DESCRIPTOR index=%d at=%08X words=%s",index,descriptor,table.concat(words,",")))
            end
        end
        taps[#taps+1]=program:install_read_tap(attack_table,attack_table+24*32-1,"original choke collision",function(offset,data,mask)
            if frame>=3890 and frame<=4200 and offset%32==0 then
                print(string.format("MK3_CHOKE_ATTACK frame=%d index=%d actor=%08X callers=%08X,%08X",frame,(offset-attack_table)//32,cpu.state.A8.value,program:read_u32(cpu.state.SP.value),program:read_u32(cpu.state.SP.value+32)))
            end
        end)
    end
    for _,input in ipairs(pulses) do
        if frame==input[2] then input[1]:set_value(1) end
        if frame==input[3] then input[1]:clear_value() end
    end
    if frame==3800 then
        local expected=victim=="sonya" and 1 or victim=="kano" and 0 or 13
        assert(state(1).id==0 and state(2).id==expected,"Original-game character selection failed")
        print(string.format("MK3_CHOKE_SELECTED p1=0 p2=%d target=%s",expected,target))
    end
    if frame>=3890 and frame<=4200 then
        for index=1,2 do
            local sample=state(index)
            print(string.format("MK3_CHOKE_STATE frame=%d side=%d id=%d action=%04X x=%d y=%d vx=%08X vy=%08X pose=%08X health=%d",frame,index,sample.id,sample.action,sample.x,sample.y,sample.vx,sample.vy,sample.pose,sample.health))
        end
    end
    if frame==3800 or (frame>=3910 and frame<=4080 and frame%10==0) then manager.machine.video:snapshot() end
end)
mk3_choke_subscriptions.stop=emu.add_machine_stop_notifier(function()
    print("MK3_CHOKE_REFERENCE_END frame="..frame)
    for _,tap in ipairs(taps) do tap:remove() end
end)
