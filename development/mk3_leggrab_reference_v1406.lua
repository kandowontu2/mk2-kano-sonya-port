-- Original MK3 leg-grab reference: ordinary controls, read-only memory taps.
local frame, pulses, taps = 0, {}, {}
local program, cpu
local target = os.getenv("MK3_LEG_TARGET") or "near"
local corner=target=="corner_left" or target=="corner_right"
local command_frame=corner and 4500 or 3900
local command = os.getenv("MK3_LEG_COMMAND") or "simultaneous"
assert(command=="simultaneous" or command=="block_first" or command=="lp_first" or command=="down_last",
    "Unknown original leg-grab command variant")
mk3_leg_subscriptions = {}
local function pulse(field, first, duration)
    pulses[#pulses + 1] = {field, first, first + (duration or 4)}
end
local function signed(n) return n >= 0x8000 and n - 0x10000 or n end
local function geometry(label)
    for side, pointer in ipairs({0x010609b0,0x01061560}) do
        local actor=program:read_u32(pointer)
        local cache=program:read_u32(actor+0x1a0)
        local x,y=signed(program:read_u16(actor+0x90)),signed(program:read_u16(actor+0xb0))
        print(string.format("MK3_LEG_GEOMETRY %s side=%d actor=%08X id=%d x=%d y=%d cache=%08X frame=%08X flags=%04X",
            label,side,actor,program:read_u16(actor+0x1f0),x,y,cache,program:read_u32(actor+0x1d0),program:read_u16(actor+0xf0)))
        for part=0,15 do
            local at=cache+part*0x70
            local source=program:read_u32(at)
            if source==0 then break end
            local w,h=program:read_u16(at+0x20),program:read_u16(at+0x30)
            local dx,dy=signed(program:read_u16(at+0x50)),signed(program:read_u16(at+0x60))
            print(string.format("MK3_LEG_PART side=%d part=%d source=%08X width=%d height=%d dx=%d dy=%d bounds=%d,%d,%d,%d",
                side,part,source,w,h,dx,dy,x-dx,y-dy,x-dx+w,y-dy+h))
        end
    end
end
mk3_leg_subscriptions.frame = emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        cpu = manager.machine.devices[":maincpu"]
        program = cpu.spaces.program
        local ports = manager.machine.ioport.ports
        local high, low, system = ports[":IN0"].fields, ports[":IN1"].fields, ports[":IN2"].fields
        for base = 360, 1320, 480 do
            pulse(system["Coin 1"], base)
            pulse(system["1 Player Start"], base + 20)
            pulse(high["P1 Down"], base + 240)
            pulse(high["P1 High Punch"], base + 320)
        end
        for _, first in ipairs({2960, 2980, 3000}) do pulse(system["Coin 2"], first) end
        pulse(system["2 Players Start"], 3020)
        pulse(high["P1 Down"], 3090)
        pulse(high["P1 High Punch"], 3160)
        if os.getenv("MK3_LEG_VICTIM") == "kano" then pulse(high["P2 Left"], 3148) end
        pulse(high["P2 High Punch"], 3180)
        if corner then
            local direction=target=="corner_left" and "Left" or "Right"
            pulse(high["P1 "..direction],3800,500)
            pulse(high["P2 "..direction],3800,500)
            pulse(high["P1 Right"],4400,30)
        elseif target ~= "far" then pulse(high["P1 Right"], 3800, 40) end
        local down,lp,block=command_frame,command_frame,command_frame
        if command=="block_first" then down,block=command_frame-4,command_frame-4 end
        if command=="lp_first" then down,lp=command_frame-4,command_frame-4 end
        if command=="down_last" then lp,block=command_frame-4,command_frame-4 end
        pulse(high["P1 Down"], down, command_frame+4-down)
        pulse(low["P1 Low Punch"], lp, command_frame+4-lp)
        pulse(high["P1 Block"], block, command_frame+4-block)
        print(string.format("MK3_LEG_COMMAND variant=%s target=%s down=%d lp=%d block=%d",command,target,down,lp,block))
        if target == "block" or target == "duck_block" then pulse(high["P2 Block"], 3890, 160) end
        if target == "duck" or target == "duck_block" then pulse(high["P2 Down"], 3890, 160) end
        if target == "air" then pulse(high["P2 Up"], 3890, 3) end
        for _, range in ipairs({{0xff8323a0, 0xff8323bf}, {0xff83b920, 0xff83bbdf}}) do
            taps[#taps + 1] = program:install_read_tap(range[1], range[2], "original leg animation",
                function(offset, data, mask)
                    if frame < command_frame-10 or frame > command_frame+220 or offset % 32 ~= 0 then return end
                    print(string.format("MK3_LEG_ROOT frame=%d offset=%08X data=%04X actor=%08X process=%08X action=%04X caller=%08X,%08X,%08X",
                        frame, offset, data, cpu.state.A8.value, cpu.state.A13.value,
                        program:read_u16(cpu.state.A13.value + 0x1f0), program:read_u32(cpu.state.SP.value),
                        program:read_u32(cpu.state.SP.value + 32), program:read_u32(cpu.state.SP.value + 64)))
                end)
        end
        local attack_table = program:read_u32(0xffa516f0)
        if os.getenv("MK3_LEG_GEOMETRY") == "1" then
            taps[#taps+1] = program:install_read_tap(0xffa5a8c0,0xffa5a8cf,"original leg geometry",
                function(offset,data,mask) if frame>=command_frame-10 and frame<=command_frame+220 then geometry("collision") end end)
        end
        print(string.format("MK3_LEG_ATTACK_TABLE %08X", attack_table))
        taps[#taps + 1] = program:install_read_tap(attack_table, attack_table + 32 * 24 - 1, "original Sonya attack index",
            function(offset, data, mask)
                if frame >= command_frame-10 and frame <= command_frame+220 and offset % 32 == 0 then
                    print(string.format("MK3_LEG_ATTACK frame=%d index=%d data=%04X actor=%08X action=%04X caller=%08X,%08X",
                        frame, (offset - attack_table) // 32, data, cpu.state.A8.value,
                        program:read_u16(cpu.state.A13.value + 0x1f0), program:read_u32(cpu.state.SP.value),
                        program:read_u32(cpu.state.SP.value + 32)))
                end
            end)
    end
    for _, p in ipairs(pulses) do
        if frame == p[2] then p[1]:set_value(1) end
        if frame == p[3] then p[1]:clear_value() end
    end
    if frame % 120 == 0 or (frame >= command_frame-10 and frame <= command_frame+180) then
        for side, ptr in ipairs({0x010609b0, 0x01061560}) do
            local actor = program:read_u32(ptr)
            if actor >= 0x01000000 and actor < 0x01400000 then
                print(string.format("MK3_LEG_STATE frame=%d side=%d actor=%08X id=%d x=%d y=%d vx=%08X vy=%08X gravity=%08X health=%d,%d",
                    frame, side, actor, program:read_u16(actor + 0x1f0), signed(program:read_u16(actor + 0x90)),
                    signed(program:read_u16(actor + 0xb0)), program:read_u32(actor + 0x40), program:read_u32(actor + 0x60),
                    program:read_u32(actor + 0x20), program:read_u16(0x01060a40), program:read_u16(0x010615f0)))
            end
        end
    end
    if frame == 3140 or frame == 3800 or (frame >= command_frame and frame <= command_frame+140 and frame % 3 == 0) then
        manager.machine.video:snapshot()
    end
    if os.getenv("MK3_LEG_GEOMETRY") == "1" and (frame==command_frame+43 or frame==command_frame+47 or frame==command_frame+51) then geometry("pose-"..frame) end
end)
mk3_leg_subscriptions.stop = emu.register_stop(function()
    for _, tap in ipairs(taps) do tap:remove() end
end)
