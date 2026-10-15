local frame, pulses = 0, {}
local move = tonumber(os.getenv("MK2KS_TEST_MOVE") or "1")
local fighter = os.getenv("MK2KS_TEST_FIGHTER") or "kano"

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        local low = ports[":IN2"].fields

        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        if fighter == "kano" then
            pulse(high["P1 Left"], 780, 4)
        else
            pulse(high["P1 Right"], 750, 4)
            pulse(high["P1 Right"], 780, 4)
            pulse(high["P1 Right"], 810, 4)
            pulse(high["P1 Right"], 840, 4)
            pulse(high["P1 Right"], 870, 4)
        end
        pulse(high["P1 High Punch"], 920, 4)

        if move == 1 then
            pulse(high["P1 Block"], 1590, 6)
            pulse(high["P1 High Punch"], 1591, 3)
        elseif move == 2 then
            pulse(high["P1 Block"], 1590, 6)
            pulse(low["P1 Low Punch"], 1591, 3)
        elseif move == 3 then
            pulse(high["P1 Block"], 1590, 6)
            pulse(high["P1 High Kick"], 1591, 3)
        else
            pulse(low["P1 Low Kick"], 1490, 95)
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 1280 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        if frame >= 1500 and frame <= 1620 and frame % 15 == 0 then
            print(string.format("MK2KSPOS frame=%d p1=%04X p2=%04X p1n=%04X p2n=%04X",
                frame, space:read_u16(0x01034FC0), space:read_u16(0x010351D0),
                space:read_u16(0x01034FD0), space:read_u16(0x010351E0)))
        end
        if frame == 1620 then
            for offset = 0, 0x300, 0x10 do
                print(string.format("MK2KSOBJWORD off=%03X p1=%04X cpu=%04X fx=%04X",
                    offset, space:read_u16(0x01034E90 + offset),
                    space:read_u16(0x010350A0 + offset),
                    space:read_u16(0x010356D0 + offset)))
            end
        end
        space:write_u16(0x0105E500, 0x00A1)
        space:write_u16(0x010602F0, 0x00A1)
        -- Keep the CPU sparring partner at the far edge so isolated move
        -- captures are not overwritten by hit-stun before the input lands.
        space:write_u16(0x010351E0, 0x0350)
    end
    if frame >= 1380 and frame <= 1680 and frame % 2 == 0 then
        manager.machine.video:snapshot()
    end
end)
