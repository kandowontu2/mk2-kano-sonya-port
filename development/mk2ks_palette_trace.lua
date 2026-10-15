local frame, pulses, taps = 0, {}, {}
local custom = os.getenv("MK2KS_CUSTOM") == "1"
local palette_counts, palette_samples = {}, {}
local first_white = false

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function record_palette(offset, data)
    if frame < 1610 or frame > 1620 then return end
    if data == 0xFFFF and not first_white then
        first_white = true
        local state = manager.machine.devices[":maincpu"].state
        print(string.format("MK2KSWHITE frame=%d addr=%08X pc=%08X A0=%08X A1=%08X A2=%08X A3=%08X A4=%08X A8=%08X B0=%08X B1=%08X B8=%08X",
            frame, offset, state["PC"].value, state["A0"].value,
            state["A1"].value, state["A2"].value, state["A3"].value,
            state["A4"].value, state["A8"].value, state["B0"].value,
            state["B1"].value, state["B8"].value))
    end
    local index = math.floor((offset - 0x01800000) / 16)
    local bank = math.floor(index / 256)
    palette_counts[bank] = (palette_counts[bank] or 0) + 1
    local samples = palette_samples[bank]
    if not samples then samples = {}; palette_samples[bank] = samples end
    if #samples < 6 then samples[#samples + 1] = string.format("%02X:%04X", index % 256, data) end
end

local function flush_palette()
    if frame < 1610 or frame > 1621 then return end
    local banks = {}
    for bank, _ in pairs(palette_counts) do banks[#banks + 1] = bank end
    table.sort(banks)
    if #banks > 0 then
        local parts = {}
        for _, bank in ipairs(banks) do
            parts[#parts + 1] = string.format("%02X=%d[%s]", bank,
                palette_counts[bank], table.concat(palette_samples[bank], ","))
        end
        print(string.format("MK2KSPAL frame=%d %s", frame - 1, table.concat(parts, " ")))
    end
    palette_counts, palette_samples = {}, {}
end

emu.register_frame(function()
    flush_palette()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        taps[#taps + 1] = space:install_write_tap(0x01800000, 0x0187FFFF,
            "mk2ks palette trace", function(offset, data, mask) record_palette(offset, data) end)
        taps[#taps + 1] = space:install_write_tap(0x010685F0, 0x01068E0F,
            "mk2ks palette queue", function(offset, data, mask)
                if frame == 1615 then
                    local state = manager.machine.devices[":maincpu"].state
                    local sp = state["SP"].value
                    print(string.format("MK2KSPALQ frame=%d addr=%08X data=%04X mask=%04X pc=%08X A0=%08X A1=%08X A2=%08X A3=%08X A4=%08X A8=%08X SP=%08X SM60=%08X SM40=%08X SM20=%08X S0=%08X S20=%08X S40=%08X S60=%08X S80=%08X SA0=%08X SC0=%08X",
                        frame, offset, data, mask, state["PC"].value,
                        state["A0"].value, state["A1"].value, state["A2"].value,
                        state["A3"].value, state["A4"].value, state["A8"].value,
                        sp, space:read_u32(sp - 0x60), space:read_u32(sp - 0x40),
                        space:read_u32(sp - 0x20), space:read_u32(sp),
                        space:read_u32(sp + 0x20), space:read_u32(sp + 0x40),
                        space:read_u32(sp + 0x60), space:read_u32(sp + 0x80),
                        space:read_u32(sp + 0xA0), space:read_u32(sp + 0xC0)))
                end
            end)

        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        if custom then pulse(high["P1 Left"], 780, 4) end
        pulse(high["P1 High Punch"], 920, 4)
        if custom then
            pulse(high["P1 Block"], 1590, 6)
            pulse(high["P1 High Punch"], 1591, 3)
        else
            pulse(high["P1 Right"], 1590, 3)
            pulse(high["P1 Right"], 1595, 3)
            pulse(high["P1 High Punch"], 1596, 3)
        end
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
