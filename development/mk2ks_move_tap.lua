local frame, pulses = 0, {}
local taps, seen, emitted = {}, {}, 0

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function trace(kind, offset, data, mask)
    if frame < 1580 or frame > 1680 or emitted >= 1200 then return end
    local state = manager.machine.devices[":maincpu"].state
    local key = string.format("%d:%s:%08X:%08X:%08X:%08X:%08X",
        frame, kind, offset, state["PC"].value,
        state["A8"].value, state["B8"].value,
        state["A9"].value ~ state["B9"].value)
    if seen[key] then return end
    seen[key] = true
    emitted = emitted + 1
    print(string.format(
        "MK2TAP frame=%d kind=%s addr=%08X data=%08X mask=%08X pc=%08X A0=%08X B0=%08X A8=%08X B8=%08X A9=%08X B9=%08X",
        frame, kind, offset, data, mask, state["PC"].value,
        state["A0"].value, state["B0"].value,
        state["A8"].value, state["B8"].value,
        state["A9"].value, state["B9"].value))
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1580 or frame == 1600 or frame == 1640 then
        print(string.format("MK2TAPHEARTBEAT frame=%d", frame))
    end
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        taps[#taps + 1] = space:install_read_tap(0xFF006000, 0xFF0062FF, "hybrid main27",
            function(offset, data, mask) trace("script", offset, data, mask) end)
        taps[#taps + 1] = space:install_read_tap(0xFF010600, 0xFF0107FF, "hybrid aux",
            function(offset, data, mask) trace("aux", offset, data, mask) end)
        taps[#taps + 1] = space:install_read_tap(0xFEB16000, 0xFEB17FFF, "donor frames",
            function(offset, data, mask) trace("donor", offset, data, mask) end)
        taps[#taps + 1] = space:install_read_tap(0xFEC8F000, 0xFEC91FFF, "shared frames",
            function(offset, data, mask) trace("shared", offset, data, mask) end)
        taps[#taps + 1] = space:install_read_tap(0xFFB40000, 0xFFB41FFF, "stock frames",
            function(offset, data, mask) trace("stock", offset, data, mask) end)

        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 Left"], 780, 4)
        pulse(high["P1 High Punch"], 920, 4)
        pulse(high["P1 Block"], 1590, 6)
        pulse(high["P1 High Punch"], 1591, 3)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 1280 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        space:write_u16(0x0105E500, 0x00A1)
        space:write_u16(0x010602F0, 0x00A1)
        space:write_u16(0x010351E0, 0x0350)
    end
end)
