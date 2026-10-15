local frame, css_frame = 0, 0
local fields, screen

local function rgb(index)
    local value = screen.palette:pen_color(index & 0x7fff)
    return (value >> 16) & 0xff, (value >> 8) & 0xff, value & 0xff
end

local function header_visible()
    local yellow = 0
    for y = 0, 24, 2 do
        for x = 40, 360, 2 do
            local r, g, b = rgb(screen:pixel(x, y))
            if r > 175 and g > 140 and b < 100 then yellow = yellow + 1 end
        end
    end
    return yellow > 20 and yellow < 100
end

local function active(first, duration)
    return frame >= first and frame < first + duration
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high, system = ports[":IN0"].fields, ports[":IN1"].fields
        fields = {
            hp = high["P1 High Punch"], p2hp = high["P2 High Punch"],
            up = high["P1 Up"], left = high["P1 Left"],
            coin = system["Coin 1"], coin2 = system["Coin 2"],
            start = system["1 Player Start"], start2 = system["2 Players Start"]
        }
        screen = manager.machine.screens[":screen"]
    end

    for _, field in pairs(fields) do field:clear_value() end
    if active(300, 4) then fields.hp:set_value(1) end
    if frame >= 600 and css_frame == 0 then
        local cycle = (frame - 600) % 300
        if cycle < 4 then fields.coin:set_value(1) end
        if cycle >= 8 and cycle < 12 then fields.coin2:set_value(1) end
        if cycle >= 20 and cycle < 24 then
            fields.start2:set_value(1)
        end
    end

    if css_frame == 0 and frame > 700 and frame % 5 == 0 and header_visible() then
        css_frame = frame
        print(string.format("MK2_CURSOR css=%d", frame))
        manager.machine.video:snapshot()
    end
    local age = css_frame > 0 and frame - css_frame or -1
    if age >= 8 and age <= 11 then fields.start:set_value(1) end
    if age >= 50 and age <= 55 then fields.hp:set_value(1) end
    if age >= 70 and age <= 75 then fields.p2hp:set_value(1) end
    if age == 2 or age == 6 or age == 10 or age == 14 or age == 18 or
            age == 32 or age == 48 or age == 64 or age == 80 or age == 100 then
        print(string.format("MK2_CURSOR sample age=%d frame=%d", age, frame))
        manager.machine.video:snapshot()
    end
end)
