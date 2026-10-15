local frame = 0
local pulses = {}
local fields = nil

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function sequence(first, names)
    local at = first
    for _, name in ipairs(names) do
        pulse(fields[name], at, 3)
        at = at + 6
    end
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0 = ports[":IN0"].fields
        local in1 = ports[":IN1"].fields
        local in2 = ports[":IN2"].fields
        fields = {
            up = in0["P1 Up"], down = in0["P1 Down"],
            left = in0["P1 Left"], right = in0["P1 Right"],
            hp = in0["P1 High Punch"], block = in0["P1 Block"],
            hk = in0["P1 High Kick"], lp = in2["P1 Low Punch"],
            lk = in2["P1 Low Kick"]
        }

        pulse(fields.hp, 300, 4)
        pulse(in1["Coin 1"], 600, 4)
        pulse(in1["Coin 1"], 615, 4)
        pulse(in1["1 Player Start"], 640, 4)
        pulse(fields.right, 730, 4); pulse(fields.right, 755, 4)
        pulse(fields.right, 780, 4); pulse(fields.right, 805, 4)
        pulse(fields.hp, 850, 4)

        local at = 1360
        local actions = { "left", "right", "up", "down", "hp", "lp", "hk", "lk", "block" }
        for pass = 1, 8 do
            for _, name in ipairs(actions) do
                pulse(fields[name], at, (name == "left" or name == "right") and 18 or 5)
                at = at + 24
            end
            pulse(fields.right, at, 20); pulse(fields.hp, at + 5, 4); at = at + 30
            pulse(fields.left, at, 20); pulse(fields.hk, at + 5, 4); at = at + 30
            pulse(fields.down, at, 24); pulse(fields.lp, at + 5, 4); pulse(fields.lk, at + 12, 4); at = at + 34
            pulse(fields.up, at, 5); pulse(fields.hp, at + 12, 4); pulse(fields.hk, at + 20, 4); at = at + 38
            pulse(fields.block, at, 28); pulse(fields.lp, at + 8, 4); at = at + 36

            sequence(at, { "right", "right", "hp" }); at = at + 34
            sequence(at, { "down", "left", "hp" }); at = at + 34
            sequence(at, { "left", "right", "lk" }); at = at + 34
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 1300 and frame % 300 == 0 then
        print(string.format("MK2KS_FUZZ frame=%d", frame))
        manager.machine.video:snapshot()
    end
end)
