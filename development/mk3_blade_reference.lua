-- Original MK3 Kano blade swipe: ordinary controls and read-only observations.
local frame,pulses,taps=0,{},{}
local cpu,program
local target=os.getenv("MK3_BLADE_TARGET") or "near"
local victim=os.getenv("MK3_BLADE_VICTIM") or "liu_kang"
local command=3900
local function pulse(field,first,duration) pulses[#pulses+1]={field,first,first+(duration or 4)} end
local function signed(n) return n>=0x8000 and n-0x10000 or n end
mk3_blade_subscriptions={}
mk3_blade_subscriptions.frame=emu.add_machine_frame_notifier(function()
    frame=frame+1
    if frame==1 then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        local ports=manager.machine.ioport.ports
        local high,system=ports[":IN0"].fields,ports[":IN2"].fields
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
        else assert(victim=="liu_kang", "Unknown original blade victim") end
        pulse(high["P2 High Punch"],victim=="sonya" and 3400 or 3180)
        if target~="far" then pulse(high["P1 Right"],3800,40) end
        pulse(high["P1 Down"],command,3)
        pulse(high["P1 Right"],command+5,3)
        pulse(high["P1 High Punch"],command+6,3)
        if target=="block" or target=="duck_block" then pulse(high["P2 Block"],3880,200) end
        if target=="duck" or target=="duck_block" then pulse(high["P2 Down"],3880,200) end
        if target=="air" then pulse(high["P2 Up"],3895,3) end
        for _,range in ipairs({{0xff823ca0,0xff8244bf,"main"},{0xff8244c0,0xff824cdf,"special"}}) do
            taps[#taps+1]=program:install_read_tap(range[1],range[2],"original blade animation",
                function(offset,data,mask)
                    if frame<3890 or frame>4070 or offset%32~=0 then return end
                    print(string.format("MK3_BLADE_ROOT frame=%d kind=%s index=%d actor=%08X process=%08X action=%04X callers=%08X,%08X,%08X",
                        frame,range[3],(offset-range[1])//32,cpu.state.A8.value,cpu.state.A13.value,
                        program:read_u16(cpu.state.A13.value+0x1f0),program:read_u32(cpu.state.SP.value),
                        program:read_u32(cpu.state.SP.value+32),program:read_u32(cpu.state.SP.value+64)))
                end)
        end
        local attack_table=program:read_u32(0xffa516d0)
        for index=0,23 do
            local descriptor=program:read_u32(attack_table+index*32)
            if descriptor>=0xff800000 then
                local words={}
                for word=0,8 do words[#words+1]=string.format("%04X",program:read_u16(descriptor+word*16)) end
                print(string.format("MK3_BLADE_DESCRIPTOR index=%d at=%08X words=%s",index,descriptor,table.concat(words,",")))
            end
        end
        taps[#taps+1]=program:install_read_tap(attack_table,attack_table+24*32-1,"original blade attack index",
            function(offset,data,mask)
                if frame>=3890 and frame<=4070 and offset%32==0 then
                    print(string.format("MK3_BLADE_ATTACK frame=%d index=%d actor=%08X action=%04X callers=%08X,%08X",
                        frame,(offset-attack_table)//32,cpu.state.A8.value,program:read_u16(cpu.state.A13.value+0x1f0),
                        program:read_u32(cpu.state.SP.value),program:read_u32(cpu.state.SP.value+32)))
                end
            end)
    end
    for _,p in ipairs(pulses) do
        if frame==p[2] then p[1]:set_value(1) end
        if frame==p[3] then p[1]:clear_value() end
    end
    if frame==3800 or (frame>=3890 and frame<=4070) then
        for side,pointer in ipairs({0x010609b0,0x01061560}) do
            local actor=program:read_u32(pointer)
            print(string.format("MK3_BLADE_STATE frame=%d side=%d id=%d x=%d y=%d vx=%08X vy=%08X pose=%08X health=%d,%d",
                frame,side,program:read_u16(actor+0x1f0),signed(program:read_u16(actor+0x90)),
                signed(program:read_u16(actor+0xb0)),program:read_u32(actor+0x40),program:read_u32(actor+0x60),
                program:read_u32(actor+0x1d0),program:read_u16(0x01060a40),program:read_u16(0x010615f0)))
        end
        if frame==3800 then
            local actor=program:read_u32(0x01061560)
            local expected=victim=="sonya" and 1 or victim=="kano" and 0 or 13
            assert(program:read_u16(actor+0x1f0)==expected,"Original blade victim selection failed: "..victim)
        end
    end
    if frame==3800 or (frame>=3905 and frame<=3990 and frame%3==0) then manager.machine.video:snapshot() end
end)
mk3_blade_subscriptions.stop=emu.add_machine_stop_notifier(function()
    for _,tap in ipairs(taps) do tap:remove() end
end)
