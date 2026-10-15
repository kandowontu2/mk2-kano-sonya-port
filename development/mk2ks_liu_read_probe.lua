local frame, pulses, tap, emitted = 0, {}, nil, 0

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high, system = ports[":IN0"].fields, ports[":IN1"].fields
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        tap = space:install_read_tap(0xFF91FC60, 0xFF92D70F, "Liu block probe",
            function(offset, data, mask)
                if frame >= 1180 and emitted < 180 then
                    local state = manager.machine.devices[":maincpu"].state
                    emitted = emitted + 1
                    print(string.format("LIUREAD frame=%d addr=%08X pc=%08X A0=%08X A8=%08X A9=%08X B0=%08X B8=%08X",
                        frame, offset, state["PC"].value, state["A0"].value,
                        state["A8"].value, state["A9"].value,
                        state["B0"].value, state["B8"].value))
                end
            end)
        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 Left"], 780, 4)
        pulse(high["P1 High Punch"], 850, 4)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame == 1200 or frame == 1300 or frame == 1400 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        for offset = 0, 0x300, 0x20 do
            print(string.format("P1OBJ frame=%d off=%03X value=%08X",
                frame, offset, space:read_u32(0x01034E90 + offset)))
        end
    end
end)
