-- Native MK3 cannonball reference: real inputs, read-only memory observation.
local frame, pulses, taps = 0, {}, {}
local program, cpu
mk3_ball_subscriptions = {}
local function pulse(field, first, duration)
    pulses[#pulses+1] = {field, first, first+(duration or 4)}
end
local function signed(n) return n >= 0x8000 and n - 0x10000 or n end
mk3_ball_subscriptions.frame = emu.add_machine_frame_notifier(function()
    frame = frame + 1
    if frame == 1 then
        cpu = manager.machine.devices[":maincpu"]
        program = cpu.spaces.program
        local ports = manager.machine.ioport.ports
        local high, low, system = ports[":IN0"].fields, ports[":IN1"].fields, ports[":IN2"].fields
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
        local victim=os.getenv("MK3_BALL_VICTIM")or"liu_kang"
        assert(victim=="liu_kang"or victim=="sub_zero")
        if victim=="sub_zero"then pulse(high["P2 Left"],3100);pulse(high["P2 Down"],3130)end
        print("MK3_BALL_ROLES own=kano victim="..victim.." writes=0")
        pulse(high["P2 High Punch"],3180)
        pulse(low["P1 Low Kick"],3900,tonumber(os.getenv("MK3_BALL_HOLD") or "185"))
        if os.getenv("MK3_BALL_TARGET") == "block" then pulse(high["P2 Block"],4000,200) end
        if os.getenv("MK3_BALL_TARGET") == "duck" then
            local first=tonumber(os.getenv("MK3_BALL_DUCK_START")or"4000")
            assert(first>=3960 and first<=4020)
            pulse(high["P2 Down"],first,260)
        end
        if os.getenv("MK3_BALL_TARGET") == "air" then pulse(high["P2 Up"],4084,3) end
        if os.getenv("MK3_BALL_TARGET") == "far" then pulse(high["P2 Right"],3900,50) end
        taps[#taps+1] = program:install_read_tap(0xff823fe0,0xff823fff,"native Kano roll animation",
            function(offset,data,mask)
                if frame < 3900 then return end
                print(string.format("MK3_BALL_ROOT frame=%d actor=%08X action=%04X caller=%08X,%08X,%08X",
                    frame,cpu.state.A8.value,program:read_u16(cpu.state.A13.value+0x1f0),
                    program:read_u32(cpu.state.SP.value),program:read_u32(cpu.state.SP.value+32),
                    program:read_u32(cpu.state.SP.value+64)))
            end)
        taps[#taps+1]=program:install_read_tap(0xffa5cc30,0xffa5cc3f,"original cannonball rectangles",function()
            local actor=program:read_u32(0x010609b0);local main=program:read_u32(0x010609f0)
            if frame>=4080 and frame<=4230 and cpu.state.PC.value==0xffa5cc40 and cpu.state.A8.value==actor and cpu.state.A13.value==main and program:read_u16(main+0x1f0)==0x20b then
                print(string.format("MK3_BALL_GEOMETRY frame=%d pc=%08X actor=%08X main=%08X victim_min=%08X victim_max=%08X attack_min=%08X attack_max=%08X bounds=%d writes=0",
                 frame,cpu.state.PC.value,actor,main,cpu.state.A2.value,cpu.state.A3.value,cpu.state.A4.value,cpu.state.A5.value,cpu.state.A6.value))
            end
        end)
        local attack_table = program:read_u32(0xffa516d0)
        print(string.format("MK3_BALL_ATTACK_TABLE %08X",attack_table))
        taps[#taps+1]=program:install_read_tap(0xff9e6350,0xff9e635f,"original ball actual action",function()
            if frame>=4080 and frame<=4230 and cpu.state.PC.value==0xff9e6360 then
                print(string.format("MK3_BALL_ENTRY frame=%d pc=%08X actor=%08X main=%08X writes=0",
                    frame,cpu.state.PC.value,cpu.state.A8.value,cpu.state.A13.value))
            end
        end)
        for side,address in ipairs({0x01060a40,0x010615f0})do
            taps[#taps+1]=program:install_write_tap(address,address+15,"original ball health",function(at,data,mask)
                if frame>=4080 and frame<=4230 then
                    print(string.format("MK3_BALL_HEALTH frame=%d slot=%d before=%d after=%d pc=%08X mask=%04X writes=0",
                        frame,side,program:read_u16(address),data&0xffff,cpu.state.PC.value,mask))
                end
            end)
        end
        taps[#taps+1] = program:install_read_tap(attack_table,attack_table+32*24-1,"native Kano attack index",
            function(offset,data,mask)
                if frame >= 4080 and frame <= 4250 and offset % 32 == 0 then
                    print(string.format("MK3_BALL_ATTACK frame=%d index=%d actor=%08X action=%04X caller=%08X,%08X",
                        frame,(offset-attack_table)//32,cpu.state.A8.value,program:read_u16(cpu.state.A13.value+0x1f0),
                        program:read_u32(cpu.state.SP.value),program:read_u32(cpu.state.SP.value+32)))
                end
            end)
    end
    for _,p in ipairs(pulses) do
        if frame == p[2] then p[1]:set_value(1);print(string.format("MK3_BALL_INPUT frame=%d field=%s value=1 writes=0",frame,p[1].name)) end
        if frame == p[3] then p[1]:clear_value() end
    end
    if frame % 120 == 0 or (frame >= 4075 and frame <= 4230) then
        for side,ptr in ipairs({0x010609b0,0x01061560}) do
            local actor=program:read_u32(ptr)
            local main=program:read_u32(ptr+0x40)
            if frame>=4075 and frame<=4230 and main>=0x01000000 and main<0x01400000 then
                print(string.format("MK3_BALL_DEFENSE frame=%d slot=%d action=%04X floor=%d hp=%d writes=0",frame,side,program:read_u16(main+0x1f0),signed(program:read_u16(main+0x200)),program:read_u16(side==1 and 0x01060a40 or 0x010615f0)))
            end
            if actor>=0x01000000 and actor<0x01400000 then
                print(string.format("MK3_BALL_STATE frame=%d side=%d actor=%08X id=%d x=%d y=%d vx=%08X vy=%08X gravity=%08X health=%d,%d",
                    frame,side,actor,program:read_u16(actor+0x1f0),signed(program:read_u16(actor+0x90)),
                    signed(program:read_u16(actor+0xb0)),program:read_u32(actor+0x40),program:read_u32(actor+0x60),
                    program:read_u32(actor+0x20),program:read_u16(0x01060a40),program:read_u16(0x010615f0)))
            end
        end
    end
    if frame==3140 or frame==3800 or (frame>=4080 and frame<=4200 and frame%4==0) then
        manager.machine.video:snapshot()
    end
end)
mk3_ball_subscriptions.stop = emu.add_machine_stop_notifier(function()
    for _,tap in ipairs(taps) do tap:remove() end
end)
