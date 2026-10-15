local frame = 0
local pulses = {}
local tap_script
local tap_frames
local seen = {}
local emitted = 0

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function trace(kind, offset, data, mask)
    if frame < 3880 or frame > 4020 or emitted >= 2000 then return end
    local state = manager.machine.devices[":maincpu"].state
    local key = string.format("%d:%s:%08X:%08X:%08X:%08X:%08X:%08X:%08X",
        frame, kind, offset, state["PC"].value,
        state["A0"].value, state["B0"].value,
        state["A8"].value, state["B8"].value,
        state["A9"].value ~ state["B9"].value)
    if not seen[key] then
        seen[key] = true
        emitted = emitted + 1
        print(string.format(
            "MK3TAP frame=%d kind=%s addr=%08X data=%08X mask=%08X pc=%08X A0=%08X B0=%08X A8=%08X B8=%08X A9=%08X B9=%08X",
            frame, kind, offset, data, mask, state["PC"].value,
            state["A0"].value, state["B0"].value,
            state["A8"].value, state["B8"].value,
            state["A9"].value, state["B9"].value))
    end
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN2"].fields
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        tap_script = space:install_read_tap(0xFF82E8A0, 0xFF82F2BF, "kano knife script",
            function(offset, data, mask) trace("script", offset, data, mask) end)
        tap_frames = space:install_read_tap(0xFFB16C80, 0xFFB17A0F, "kano knife frames",
            function(offset, data, mask) trace("frame", offset, data, mask) end)

        for base = 360, 1320, 480 do
            pulse(system["Coin 1"], base, 4)
            pulse(system["1 Player Start"], base + 20, 4)
            pulse(high["P1 Right"], base + 180, 4)
            pulse(high["P1 Right"], base + 220, 4)
            pulse(high["P1 Right"], base + 260, 4)
            pulse(high["P1 High Punch"], base + 320, 4)
        end

        pulse(system["Coin 2"], 3000, 4)
        pulse(system["2 Players Start"], 3020, 4)
        pulse(high["P1 Right"], 3060, 4)
        pulse(high["P1 Right"], 3090, 4)
        pulse(high["P1 Right"], 3120, 4)
        pulse(high["P1 High Punch"], 3160, 4)
        pulse(high["P2 High Punch"], 3180, 4)

        pulse(high["P1 Down"], 3900, 4)
        pulse(high["P1 Left"], 3905, 4)
        pulse(high["P1 High Punch"], 3910, 4)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 3500 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        space:write_u8(0x01060A40, 0xA6)
        space:write_u8(0x010615F0, 0xA6)
    end
end)
