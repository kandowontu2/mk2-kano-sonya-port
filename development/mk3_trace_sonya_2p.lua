local frame, pulses = 0, {}
local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0, in1, in2 = ports[":IN0"].fields, ports[":IN1"].fields, ports[":IN2"].fields
        pulse(in2["Coin 1"], 360, 4); pulse(in2["Coin 2"], 360, 4)
        pulse(in2["2 Players Start"], 380, 4)
        pulse(in0["P1 Down"], 600, 4)
        pulse(in0["P1 High Punch"], 680, 4)
        pulse(in0["P2 High Punch"], 700, 4)

        pulse(in0["P1 Down"], 1250, 3); pulse(in0["P1 Right"], 1255, 3); pulse(in1["P1 Low Punch"], 1260, 3)
        pulse(in0["P1 Down"], 1450, 4); pulse(in1["P1 Low Punch"], 1450, 4); pulse(in0["P1 Block"], 1450, 4)
        pulse(in0["P1 Right"], 1650, 3); pulse(in0["P1 Left"], 1655, 3); pulse(in0["P1 High Punch"], 1660, 3)
        pulse(in0["P1 Left"], 1850, 3); pulse(in0["P1 Left"], 1857, 3); pulse(in0["P1 Down"], 1864, 3); pulse(in0["P1 High Kick"], 1871, 3)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    local shots = { [1100]=true, [1260]=true, [1275]=true, [1310]=true, [1450]=true, [1465]=true, [1510]=true, [1660]=true, [1675]=true, [1720]=true, [1871]=true, [1886]=true, [1930]=true }
    if shots[frame] then manager.machine.video:snapshot() end
end)
