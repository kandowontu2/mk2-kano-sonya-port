local frame, pulses = 0, {}
local move = tonumber(os.getenv("MK2KS_TEST_MOVE") or "1")
local trace = os.getenv("MK2KS_TRACE_ROOTS") == "1"
local input_tap, root_tap, last_input

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function two_forward(first, forward, button)
    pulse(forward, first, 3)
    pulse(forward, first + 5, 3)
    pulse(button, first + 6, 3)
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        local low = ports[":IN2"].fields
		if trace then
			local program = manager.machine.devices[":maincpu"].spaces["program"]
			input_tap = program:install_read_tap(0x01600000, 0x0160000f,
				"MK2 stock input probe", function(offset, data, mask)
					if frame >= 1500 and frame < 1560 and data ~= last_input then
						print(string.format("MK2_INPUT frame=%d data=%04X", frame, data & 0xffff))
						last_input = data
					end
				end)
			root_tap = program:install_read_tap(0xff91fc60, 0xff920d1f,
				"MK2 stock root probe", function(offset, data, mask)
					if frame >= 1500 and frame < 1600 then
						local state = manager.machine.devices[":maincpu"].state
						if state["PC"].value == 0xff906140 and state["A8"].value == 0x01034e90 then
							print(string.format("MK2_ROOT frame=%d addr=%08X data=%04X", frame, offset, data & 0xffff))
						end
					end
				end)
		end

        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 High Punch"], 850, 4)

        if move == 1 then
            two_forward(1520, high["P1 Right"], high["P1 High Punch"])
        elseif move == 2 then
            two_forward(1520, high["P1 Right"], low["P1 Low Punch"])
        elseif move == 3 then
            two_forward(1520, high["P1 Right"], high["P1 High Kick"])
        else
            pulse(low["P1 Low Kick"], 1400, 300)
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
    if frame >= 1380 and frame <= 1680 and frame % 2 == 0 then
        manager.machine.video:snapshot()
    end
end)
