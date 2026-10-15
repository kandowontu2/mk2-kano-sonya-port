-- Read-only original MK3 command-routing reference, never loaded by mk2ks.
-- Both fighters are genuinely selected by the existing physical-input route.
dofile("mk3_finish_input_selection.lua")
local frame, cpu, space, fields = 0, nil, nil, {}
local taps, seen, entered = {}, {}, false
local buttons = {"P1 High Kick", "P2 High Kick", "P1 Low Kick", "P2 Low Kick",
                 "P1 Block", "P2 Block", "P1 High Punch", "P2 High Punch",
                 "P1 Low Punch", "P2 Low Punch", "P1 Up", "P1 Down", "P1 Left", "P1 Right",
                 "P2 Up", "P2 Down", "P2 Left", "P2 Right"}
local function actor_info(actor)
    if actor < 0x01000000 or actor >= 0x01400000 then return "invalid" end
    return string.format("%08X:id%d:slotflag%d", actor,
        space:read_u16(actor + 0x1f0), space:read_u16(actor + 0x1c0))
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        cpu = manager.machine.devices[":maincpu"]
        space = cpu.spaces.program
        for _,port in ipairs({":IN0", ":IN1"}) do
            for _,name in ipairs(buttons) do
                if manager.machine.ioport.ports[port].fields[name] then
                    fields[name] = manager.machine.ioport.ports[port].fields[name]
                end
            end
        end
        for _,address in ipairs({0xff991f70, 0xff982880}) do
            taps[#taps+1] = space:install_read_tap(address,address+15,
                "original command routing read only",function(offset)
                if offset ~= address or frame < 3850 or frame > 5400 then return end
                local record = address == 0xff991f70 and cpu.state.A14.value or
                    cpu.state.A11.value - 0x90
                if record < 0xff800000 or record >= 0xffa00000 then return end
                local actor = cpu.state.A8.value
                local key = string.format("%08X:%08X:%08X",address,actor,record)
                if seen[key] then return end
                seen[key] = true
                local words = {}
                for i=0,12 do words[#words+1] = tostring(space:read_u16(record+0x90+i*0x10)) end
                print(string.format("MK3_BABA_RECORD frame=%d at=%08X actor=%s record=%08X masks=%08X,%08X type=%d gate=%08X action=%08X history=%s",
                    frame,address,actor_info(actor),record,space:read_u32(record),
                    space:read_u32(record+0x20),space:read_u16(record+0x40),
                    space:read_u32(record+0x50),space:read_u32(record+0x70),table.concat(words,",")))
            end)
        end
    end
    if frame == 3800 then
        local a,b=space:read_u32(0x010609b0),space:read_u32(0x01061560)
        print("MK3_BABA_SELECTION actors="..actor_info(a)..","..actor_info(b))
        assert(space:read_u16(a+0x1f0)==0 and space:read_u16(b+0x1f0)==1,
            "Original reference must select Kano and Sonya")
        entered=true
        manager.machine.video:snapshot()
    end
    if frame >= 3850 then
        for _,field in pairs(fields) do field:clear_value() end
        for index,name in ipairs(buttons) do
            local first=3900+(index-1)*120
            if frame==first then print("MK3_BABA_BUTTON frame="..frame.." name="..name) end
            if frame>=first and frame<first+4 then assert(fields[name]):set_value(1) end
        end
    end
    if frame >= 5100 and frame % 120 == 70 then
        for side,base in ipairs({0x01060d50,0x01061900}) do
            local head=space:read_u32(base)
            local previous=head-32
            if previous<=base then previous=previous+0x280 end
            print(string.format("MK3_BABA_DIRECTION frame=%d slot=%d head=%08X latest=%08X",frame,side,head,space:read_u32(previous)))
        end
    end
    if frame == 6100 then
        assert(entered,"Selection never verified")
        print("MK3_BABA_REFERENCE_RESULT ram_writes=0 cheats=false finished=true")
        manager.machine:exit()
    end
end)
