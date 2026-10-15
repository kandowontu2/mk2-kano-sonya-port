local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function mark(name, at)
    print(string.format("MK2KS_ACTION frame=%d name=%s", at, name))
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0, in1, in2 = ports[":IN0"].fields, ports[":IN1"].fields, ports[":IN2"].fields
        local f = {
            up=in0["P1 Up"], down=in0["P1 Down"], left=in0["P1 Left"], right=in0["P1 Right"],
            hp=in0["P1 High Punch"], block=in0["P1 Block"], hk=in0["P1 High Kick"],
            lp=in2["P1 Low Punch"], lk=in2["P1 Low Kick"]
        }
        pulse(f.hp, 300, 4); pulse(in1["Coin 1"], 600, 4); pulse(in1["Coin 1"], 615, 4)
        pulse(in1["1 Player Start"], 640, 4); pulse(f.block, 810, 28); pulse(f.hp, 820, 4)

        local actions = {
            {"left", f.left, 18}, {"right", f.right, 18}, {"up", f.up, 5}, {"down", f.down, 5},
            {"hp", f.hp, 5}, {"lp", f.lp, 5}, {"hk", f.hk, 5}, {"lk", f.lk, 5}, {"block", f.block, 8}
        }
        local at = 1360
        for _, action in ipairs(actions) do
            mark(action[1], at); pulse(action[2], at, action[3]); at = at + 36
        end
        mark("forward_hp", at); pulse(f.right, at, 20); pulse(f.hp, at+5, 4); at=at+42
        mark("back_hk", at); pulse(f.left, at, 20); pulse(f.hk, at+5, 4); at=at+42
        mark("crouch_combo", at); pulse(f.down, at, 24); pulse(f.lp, at+5, 4); pulse(f.lk, at+12, 4); at=at+46
        mark("jump_combo", at); pulse(f.up, at, 5); pulse(f.hp, at+12, 4); pulse(f.hk, at+20, 4); at=at+50
        mark("block_lp", at); pulse(f.block, at, 28); pulse(f.lp, at+8, 4); at=at+42
        mark("ff_hp", at); pulse(f.right, at, 3); pulse(f.right, at+7, 3); pulse(f.hp, at+14, 3); at=at+42
        mark("bdf_lp", at); pulse(f.left, at, 3); pulse(f.down, at+7, 3); pulse(f.right, at+14, 3); pulse(f.lp, at+21, 3)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame >= 1320 and frame <= 2100 and frame % 12 == 0 then
        print(string.format("MK2KS_SNAPSHOT frame=%d", frame))
        manager.machine.video:snapshot()
    end
end)
