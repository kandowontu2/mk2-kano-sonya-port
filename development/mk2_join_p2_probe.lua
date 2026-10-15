local frame, pulses = 0, {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 High Punch"], 850, 4)
        -- Join only after the first match has reached live combat.  Earlier
        -- probes pressed P2 Start during the ladder/ROUND transition and did
        -- not exercise MKII's real challenger path.
        pulse(system["Coin 1"], 2020, 4)
        pulse(system["2 Players Start"], 2100, 4)
        pulse(high["P1 High Punch"], 2380, 4)
        pulse(high["P2 High Punch"], 2420, 4)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame >= 1280 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        space:write_u16(0x0105E500, 0x00A1)
        space:write_u16(0x010602F0, 0x00A1)
    end
    if frame >= 1350 and frame <= 2600 and frame % 10 == 0 then
        manager.machine.video:snapshot()
    end
end)
