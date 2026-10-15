local frame, css_frame, fight_age = 0, 0, 0
local css_seen = false
local two_player = os.getenv("MK2KS_TWO_PLAYER") == "1"
local direct = os.getenv("MK2KS_DIRECT_SEQUENCE") == "1"
local stock = os.getenv("MK2KS_STOCK") == "1"
local overlap = os.getenv("MK2KS_OVERLAP") == "1"
local isolate = os.getenv("MK2KS_ISOLATE") == "1"
local fields, screen, program, input_tap, root_tap
local last_input = -1

local function rgb(index)
    local value = screen.palette:pen_color(index & 0x7fff)
    return (value >> 16) & 0xff, (value >> 8) & 0xff, value & 0xff
end

local function yellow_header_pixels()
    local count = 0
    for y = 0, 24, 2 do
        for x = 40, 360, 2 do
            local r, g, b = rgb(screen:pixel(x, y))
            if r > 175 and g > 140 and b < 100 then count = count + 1 end
        end
    end
    return count
end

local function green_bar_pixels()
    local count = 0
    for x = 0, 399 do
        local r, g, b = rgb(screen:pixel(x, 30))
        if g > 120 and g > r * 3 // 2 and g > b * 3 // 2 then count = count + 1 end
    end
    return count
end

local function active(first, duration)
    return frame >= first and frame < first + duration
end

local function dump_player(label)
    local values = {}
    for offset = 0, 0x250, 0x10 do
        values[#values + 1] = string.format("%03X=%04X", offset,
            program:read_u16(0x01034e90 + offset))
    end
    print(string.format("MK2KS_PLAYER %s frame=%d age=%d %s",
        label, frame, fight_age, table.concat(values, " ")))
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        fields = {
            hp = high["P1 High Punch"], block = high["P1 Block"],
            right = high["P1 Right"], up = high["P1 Up"],
            p2hp = high["P2 High Punch"],
            coin = system["Coin 1"], coin2 = system["Coin 2"],
            start = system["1 Player Start"], start2 = system["2 Players Start"]
        }
        screen = manager.machine.screens[":screen"]
        program = manager.machine.devices[":maincpu"].spaces["program"]
        input_tap = program:install_read_tap(0x01600000, 0x0160000f,
            "MK2KS input probe", function(offset, data, mask)
                if fight_age > 0 and data ~= last_input then
                    print(string.format("MK2KS_INPUT frame=%d age=%d data=%04X mask=%04X",
                        frame, fight_age, data & 0xffff, mask & 0xffff))
                    last_input = data
                end
            end)
        root_tap = program:install_read_tap(0xff000000, 0xff02107f,
            "MK2KS root probe", function(offset, data, mask)
                if fight_age > 0 then
                    local relative = offset & 0x1ffff
                    if relative < 0x40 or (relative >= 0x840 and relative < 0x880) then
                        local state = manager.machine.devices[":maincpu"].state
                        print(string.format("MK2KS_ROOT frame=%d age=%d addr=%08X pc=%08X A8=%08X data=%04X",
                            frame, fight_age, offset, state["PC"].value,
                            state["A8"].value, data & 0xffff))
                    end
                end
            end)
        if stock then
            root_tap = program:install_read_tap(0xff91fc60, 0xff9205bf,
                "MK2 stock Liu root probe", function(offset, data, mask)
                    if fight_age > 0 and
                            ((offset >= 0xff91fc60 and offset < 0xff91fca0) or
                             (offset >= 0xff9204a0 and offset < 0xff9204e0)) then
                        local state = manager.machine.devices[":maincpu"].state
                        print(string.format("MK2KS_ROOT frame=%d age=%d addr=%08X pc=%08X A8=%08X data=%04X",
                            frame, fight_age, offset, state["PC"].value,
                            state["A8"].value, data & 0xffff))
                    end
                end)
        end
    end

    for _, field in pairs(fields) do field:clear_value() end
    if active(300, 4) then fields.hp:set_value(1) end
    if not css_seen and frame >= 600 then
        local cycle = (frame - 600) % 300
        if cycle < 4 then fields.coin:set_value(1) end
        if two_player and cycle >= 8 and cycle < 12 then fields.coin2:set_value(1) end
        if cycle >= 20 and cycle < 24 then
            fields[two_player and "start2" or "start"]:set_value(1)
        end
    end

    if not css_seen and frame > 700 and frame % 5 == 0 then
        local yellow = yellow_header_pixels()
        if yellow > 20 and yellow < 100 then
            css_seen = true
            css_frame = frame
            print(string.format("MK2KS_PROBE css frame=%d", frame))
        end
    end

    local css_age = css_seen and (frame - css_frame) or -1
    if css_age >= 0 then
        if two_player and css_age >= 1 and css_age <= 4 then fields.up:set_value(1) end
        if css_age >= 12 and css_age <= 17 then
            if not stock then fields.block:set_value(1) end
            fields.hp:set_value(1)
        end
        if two_player and css_age >= 28 and css_age <= 33 then fields.p2hp:set_value(1) end
    end

    if fight_age > 0 then
        fight_age = fight_age + 1
        if isolate then
            program:write_u16(0x0105e500, 0x00a1)
            program:write_u16(0x010602f0, 0x00a1)
            program:write_u16(0x010351e0, 0x0350)
        end
        local phase = fight_age % 120
        if direct then
            if (phase >= 2 and phase <= 4) or (phase >= 9 and phase <= 11) then
                fields.right:set_value(1)
            end
            if (overlap and phase >= 10 and phase <= 12) or
                    (not overlap and phase >= 16 and phase <= 18) then
                fields.hp:set_value(1)
            end
        elseif phase >= 1 and phase <= 6 then
            fields.block:set_value(1)
            fields.hp:set_value(1)
        end
        if fight_age == 2 or fight_age % 120 == 20 then dump_player("sample") end
    elseif css_seen and frame - css_frame > 500 and green_bar_pixels() > 60 then
        fight_age = 1
        dump_player("fight-start")
    end
end)
