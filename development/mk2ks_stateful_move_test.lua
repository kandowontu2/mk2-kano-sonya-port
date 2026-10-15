local frame, css_selected, css_frame, selector_age, fight_age = 0, false, 0, 0, 0
local combat_root_frame = 0
local fighter = os.getenv("MK2KS_TEST_FIGHTER") or "kano"
local move = tonumber(os.getenv("MK2KS_TEST_MOVE") or "1")
local confirm = os.getenv("MK2KS_TEST_CONFIRM") or "hp"
local trace_roots = os.getenv("MK2KS_TRACE_ROOTS") == "1"
local pin_fighters = os.getenv("MK2KS_PIN_FIGHTERS") == "1"
local two_player = os.getenv("MK2KS_TWO_PLAYER") == "1"
local join_p2 = os.getenv("MK2KS_JOIN_P2") == "1"
local direct_sequence = os.getenv("MK2KS_DIRECT_SEQUENCE") == "1"
local trace_palette = os.getenv("MK2KS_TRACE_PALETTE") == "1"
local capture_combat = os.getenv("MK2KS_CAPTURE_COMBAT") ~= "0"
local capture_transition = os.getenv("MK2KS_CAPTURE_TRANSITION") == "1"
local transition_capture_frame = 0
local fields, screen, root_taps, input_tap, program
local task_tap, reaction_tap
local last_input = -1
local palette_tap, palette_queue_tap, palette_samples = nil, nil, 0
local bad_palette_dumped = false
local queue_reg_samples = 0
local root_hits = {}
local native_effect_reads = 0
local move_root_offsets = {}
local previous_pixels, unchanged_frames = nil, 0
local stalled_frames, trap_frames = 0, 0
local roster_errors, identity_errors = 0, 0
local basic_actions = os.getenv("MK2KS_BASIC_ACTIONS") == "1"
-- Diagnostic only: exercise the canonical roster ID independently of the
-- current selection bridge. Results from this mode are NOT selection proof.
local probe_native_roster = os.getenv("MK2KS_PROBE_NATIVE_ROSTER") == "1"
local basic_index, basic_checks, basic_errors = 0, 0, 0
local basic_seen = {}
local actions = {
    {"forward walk", {"right"}, {1, 2}},
    {"backward walk", {"left"}, {3, 4}},
    {"vertical jump", {"up"}, {6}},
    {"forward flip", {"up", "right"}, {7, 8}},
    {"backward flip", {"up", "left"}, {7, 8}},
    {"crouch", {"down"}, {5}},
    {"standing block", {"block"}, {11}},
    {"crouching block", {"down", "block"}, {12}},
    {"high punch", {"hp"}, {19, 34}},
    {"low punch", {"lp"}, {20, 34}},
    {"high kick", {"hk"}, {13, 33}},
    {"low kick", {"lk"}, {14, 33}},
    {"crouching punch", {"down", "lp"}, {24}},
    {"crouching high kick", {"down", "hk"}, {25}},
    {"crouching low kick", {"down", "lk"}, {26}},
    {"uppercut", {"down", "hp"}, {28}},
    {"sweep", {"left", "lk"}, {21}},
    {"roundhouse", {"left", "hk"}, {32}},
    {"jump punch", {"up"}, {31}, "hp"},
    {"jump kick", {"up"}, {29}, "hk"},
}

local frame_pixels, pixel_width
local function pixel(x, y)
    return string.unpack("<I4", frame_pixels, (y * pixel_width + x) * 4 + 1)
end

local function rgb(value)
    return (value >> 16) & 0xff, (value >> 8) & 0xff, value & 0xff
end

local function yellow_header_pixels()
    local count = 0
    for y = 0, 24, 2 do
        for x = 40, 360, 2 do
            local r, g, b = rgb(pixel(x, y))
            if r > 175 and g > 140 and b < 100 then count = count + 1 end
        end
    end
    return count
end

local function green_bar_pixels()
    local count = 0
    for x = 0, 399 do
        local r, g, b = rgb(pixel(x, 30))
        if g > 120 and g > r * 3 // 2 and g > b * 3 // 2 then count = count + 1 end
    end
    return count
end

local function active(first, duration)
    return frame >= first and frame < first + duration
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        local low = ports[":IN2"].fields
        fields = {
            hp = high["P1 High Punch"], hk = high["P1 High Kick"],
            block = high["P1 Block"], lp = low["P1 Low Punch"],
            left = high["P1 Left"], right = high["P1 Right"],
            down = high["P1 Down"],
            lk = low["P1 Low Kick"], coin = system["Coin 1"],
            up = high["P1 Up"], p2hp = high["P2 High Punch"],
            p2block = high["P2 Block"], coin2 = system["Coin 2"],
            start = system["1 Player Start"], start2 = system["2 Players Start"]
        }
        screen = manager.machine.screens[":screen"]
        program = manager.machine.devices[":maincpu"].spaces["program"]
        if os.getenv("MK2KS_TRACE_TASKS") == "1" then
            task_tap = program:install_write_tap(0x01068e30, 0x0106bfff, "task callback probe", function(offset, data, mask)
                if fight_age > 0 and (data & 0xffff) == 0x09e0 then
                    local state = manager.machine.devices[":maincpu"].state
                    print(string.format("MK2KS_BAD_TASK frame=%d addr=%08X pc=%08X A0=%08X A1=%08X A7=%08X A8=%08X A13=%08X return=%08X",
                        frame, offset, state["PC"].value, state["A0"].value, state["A1"].value, state["A7"].value,
                        state["A8"].value, state["A13"].value, program:read_u32(state["SP"].value)))
                    local values = {}
                    for delta = 0, 0xc0, 0x20 do
                        values[#values + 1] = string.format("+%X=%08X", delta, program:read_u32(state["SP"].value + delta))
                    end
                    print("MK2KS_BAD_TASK_CALLER " .. table.concat(values, " "))
                end
            end)
            reaction_tap = program:install_read_tap(0xfffe4800, 0xfffe6fff, "reaction callback probe", function(offset, data, mask)
                if fight_age > 0 then
                    local state = manager.machine.devices[":maincpu"].state
                    print(string.format("MK2KS_REACTION frame=%d addr=%08X data=%04X pc=%08X A0=%08X A11=%08X", frame, offset, data & 0xffff, state["PC"].value, state["A0"].value, state["A11"].value))
                end
            end)
        end
        if trace_palette then
            palette_queue_tap = program:install_write_tap(0x01068000, 0x01069fff,
                "MK2KS state palette queue probe", function(offset, data, mask)
                    local state = manager.machine.devices[":maincpu"].state
					if fight_age >= 5 and fight_age <= 25 and state["PC"].value == 0xff80c720 and
						queue_reg_samples < 12 then
						print(string.format("MK2KS_QUEUE_SAMPLE frame=%d age=%d addr=%08X data=%04X A0=%08X A1=%08X A2=%08X A5=%08X A8=%08X A9=%08X",
							frame, fight_age, offset, data & 0xffff, state["A0"].value,
							state["A1"].value, state["A2"].value, state["A5"].value,
							state["A8"].value, state["A9"].value))
						queue_reg_samples = queue_reg_samples + 1
					end
                    if fight_age >= 15 and fight_age <= 25 and (data == 0xffff or data == 0x0400) then
                        print(string.format("MK2KS_QUEUE_WRITE frame=%d age=%d addr=%08X data=%04X pc=%08X A0=%08X A1=%08X A4=%08X A8=%08X B0=%08X B1=%08X",
                            frame, fight_age, offset, data & 0xffff, state["PC"].value,
                            state["A0"].value, state["A1"].value, state["A4"].value,
                            state["A8"].value, state["B0"].value, state["B1"].value))
						if data == 0xffff then
							local regs = {}
							for _, bank in ipairs({ "A", "B" }) do
								for index = 0, 14 do
									local name = bank .. index
									regs[#regs + 1] = string.format("%s=%08X", name, state[name].value)
								end
							end
							print("MK2KS_QUEUE_REGS " .. table.concat(regs, " "))
						end
                    end
                end)
            palette_tap = program:install_write_tap(0x01800000, 0x0187ffff,
                "MK2KS state palette probe", function(offset, data, mask)
                    if fight_age >= 5 and fight_age <= 45 and palette_samples < 120 then
                        local state = manager.machine.devices[":maincpu"].state
                        print(string.format("MK2KS_PALETTE frame=%d age=%d addr=%08X data=%04X pc=%08X A0=%08X A8=%08X B0=%08X",
                            frame, fight_age, offset, data & 0xffff, state["PC"].value,
                            state["A0"].value, state["A8"].value, state["B0"].value))
                        palette_samples = palette_samples + 1
						if data == 0xffff and not bad_palette_dumped then
							bad_palette_dumped = true
							local base = state["A0"].value
							local values = {}
							for delta = -0x80, 0x100, 0x10 do
								values[#values + 1] = string.format("%+04X=%04X", delta, program:read_u16(base + delta))
							end
							print("MK2KS_PALETTE_QUEUE " .. table.concat(values, " "))
						end
                    end
                end)
        end
        if trace_roots then
            input_tap = program:install_read_tap(0x01600000, 0x0160000f,
                "MK2KS input state probe", function(offset, data, mask)
                    if ((fight_age > 0 and fight_age < 50) or
                            (two_player and selector_age >= 70 and selector_age <= 88)) and
                            data ~= last_input then
                        print(string.format("MK2KS_INPUT frame=%d age=%d selector=%d data=%04X mask=%04X",
                            frame, fight_age, selector_age, data & 0xffff, mask & 0xffff))
                        last_input = data
                    end
                end)
        end
        do
            local space = manager.machine.devices[":maincpu"].spaces["program"]
            local root_base = fighter == "kano" and 0xff000000 or 0xff020000
            local variant_base = fighter == "kano" and 0xff040000 or 0xff060000
            local projectile_variant_base = fighter == "kano" and 0xff080000 or 0xff0a0000
            root_taps = {}
            local function install_root_tap(base, label)
				root_hits[label] = 0
                root_taps[#root_taps + 1] = space:install_read_tap(base, base + 0x107f, label,
                    function(offset, data, mask)
                    local state = manager.machine.devices[":maincpu"].state
                    local relative = offset - base
					if basic_actions and basic_index > 0 and relative < 0x820 and
						state["PC"].value == 0xff906140 and state["A8"].value == 0x01034e90 then
						basic_seen[relative // 32] = true
					end
					if fight_age > 0 then root_hits[label] = root_hits[label] + 1 end
					if fight_age > 0 and label == "MK2KS root probe" then
						local phase = ((fight_age - 1) % 240) + 1
						if phase >= 55 and phase <= 180 then move_root_offsets[relative] = true end
					end
                    if combat_root_frame == 0 and
                            base == root_base and
                            (relative < 0x820 or (relative >= 0x840 and relative < 0x1060)) and
                            state["PC"].value == 0xff906140 and state["A8"].value == 0x01034e90 then
                        combat_root_frame = frame
                        print(string.format("MK2KS_STATE combat-root frame=%d offset=%03X", frame, relative))
                    end
                    if trace_roots and (relative < 0x820 or (relative >= 0x840 and relative < 0x1060)) then
                        print(string.format("MK2KS_ROOT frame=%d age=%d addr=%08X pc=%08X A8=%08X data=%04X",
                            frame, fight_age, offset, state["PC"].value,
                            state["A8"].value, data & 0xffff))
                    end
                    end)
            end
            install_root_tap(root_base, "MK2KS root probe")
            install_root_tap(variant_base, "MK2KS variant root probe")
            install_root_tap(projectile_variant_base, "MK2KS projectile variant root probe")
            root_taps[#root_taps + 1] = space:install_read_tap(0xff602000, 0xff6028df,
                "native effect frames", function(offset, data, mask)
                    if fight_age > 0 then native_effect_reads = native_effect_reads + 1 end
                end)
        end
    end

    frame_pixels, pixel_width = screen:pixels()
    for _, field in pairs(fields) do field:clear_value() end

    if active(300, 4) then fields.hp:set_value(1) end
    if not css_selected and frame >= 600 then
        local cycle = (frame - 600) % 300
        if cycle < 4 then fields.coin:set_value(1) end
        if two_player and cycle >= 8 and cycle < 12 then fields.coin2:set_value(1) end
        if cycle >= 20 and cycle < 24 then
            fields.start:set_value(1)
        end
    end

    local yellow = 0
    if frame % 5 == 0 or capture_transition then yellow = yellow_header_pixels() end
    -- Read RGB in visible-area coordinates. The select header has about 415
    -- sampled yellow pixels; the ladder header has about 370.
    if not css_selected and frame > 700 and yellow >= 400 and yellow <= 430 then
        css_selected = true
        css_frame = frame
        selector_age = 1
        print(string.format("MK2KS_STATE css frame=%d yellow=%d", frame, yellow))
        manager.machine.video:snapshot()
    end

    if selector_age > 0 and selector_age <= (two_player and 232 or 110) then
        if two_player then
            if selector_age <= 4 then fields.coin:set_value(1) end
            if selector_age >= 8 and selector_age <= 11 then fields.coin2:set_value(1) end
            if selector_age >= 20 and selector_age <= 23 then fields.start2:set_value(1) end
        end

        if fighter == "kano" then
            if selector_age >= 12 and selector_age <= 15 then fields.left:set_value(1) end
        else
            if (selector_age >= 12 and selector_age <= 15) or
                    (selector_age >= 24 and selector_age <= 27) or
                    (selector_age >= 36 and selector_age <= 39) or
                    (selector_age >= 48 and selector_age <= 51) then
                fields.right:set_value(1)
            end
        end
        if selector_age >= 96 and selector_age <= 103 then fields[confirm]:set_value(1) end

        if two_player and selector_age >= 220 and selector_age <= 227 then
            fields.p2hp:set_value(1)
        end
        if selector_age == 16 or selector_age == 32 or selector_age == 60 or selector_age == 86 then
            manager.machine.video:snapshot()
        end
        selector_age = selector_age + 1
    end

    if capture_transition and css_selected and selector_age > (two_player and 232 or 110) then
        if transition_capture_frame == 0 and (yellow < 400 or yellow > 430) then
            transition_capture_frame = frame
            print(string.format("MK2KS_TRANSITION first_non_css=%d yellow=%d", frame, yellow))
        end
        if transition_capture_frame > 0 and frame < transition_capture_frame + 12 then
            print(string.format("MK2KS_TRANSITION snapshot frame=%d age=%d", frame,
                frame - transition_capture_frame))
            manager.machine.video:snapshot()
        end
    end

    local green = green_bar_pixels()
    if fight_age > 0 then
        local expected_identity = fighter == "kano" and 0x11 or 0x12
        if program:read_u16(0x01060280) ~= expected_identity then roster_errors = roster_errors + 1 end
        if program:read_u16(0x01035080) ~= expected_identity then identity_errors = identity_errors + 1 end
        if two_player then fields.p2block:set_value(1) end
        fight_age = fight_age + 1
    elseif combat_root_frame > 0 and frame - combat_root_frame >= 120 then
        -- A read of the custom main root by the live P1 object proves that the
        -- native selection/ladder transition completed.  Delay through the
        -- ROUND/FIGHT intro before sending any move inputs.
        fight_age = 1
    end

    if fight_age > 0 then
        if fight_age == 1 and probe_native_roster then
            local identity = fighter == "kano" and 0x11 or 0x12
            print(string.format("MK2KS_ROSTER_PROBE diagnostic=true old=%04X requested=%04X frame=%d",
                program:read_u16(0x01060280), identity, frame))
            program:write_u16(0x01060280, identity)
        end
        if fight_age > 180 and frame_pixels == previous_pixels then
            unchanged_frames = unchanged_frames + 1
        else
            unchanged_frames = 0
        end
        if unchanged_frames > 180 then stalled_frames = stalled_frames + 1 end
        local pc = manager.machine.devices[":maincpu"].state["PC"].value
        if pc == 0xffa1e800 or pc == 0xffa1e880 then trap_frames = trap_frames + 1 end
        previous_pixels = frame_pixels
        if join_p2 then
            if fight_age >= 300 and fight_age <= 303 then fields.coin:set_value(1) end
            if fight_age >= 330 and fight_age <= 333 then fields.start2:set_value(1) end
            -- MKII may spend a stage-dependent amount of time on the challenger
            -- transition.  Short, separated P2 confirm taps select the default
            -- fighter as soon as the real P2 cursor becomes active.
            if fight_age >= 450 and fight_age <= 900 and
                    ((fight_age - 450) % 60) < 4 then
                fields.p2hp:set_value(1)
            end
        end
        if pin_fighters then
            program:write_u16(0x01034f20, 0x0090)
            program:write_u16(0x01035130, 0x0140)
            program:write_u16(0x0105e500, 0x00a1)
            program:write_u16(0x010602f0, 0x00a1)
        end
        -- Give every attempt a clean idle window.  The first input begins 60
        -- frames after ROUND/FIGHT, and the 240-frame cadence leaves even the
        -- long grab/bicycle move enough time to recover before another try.
        local phase = ((fight_age - 1) % 240) + 1
        if basic_actions then
            local action_number = (fight_age - 1) // 90 + 1
            local action_phase = (fight_age - 1) % 90 + 1
            if action_phase == 1 and action_number <= #actions then
                basic_index, basic_seen = action_number, {}
                print(string.format("MK2KS_BASIC_BEGIN action=%d name=%s frame=%d", basic_index, actions[basic_index][1], frame))
            end
            if action_number <= #actions then
                local action = actions[action_number]
                -- Crouch is established before the attack/block button; jump
                -- attacks are delayed into the air. No gameplay RAM is pinned.
                for _, button in ipairs(action[2]) do
                    local direction = button == "left" or button == "right" or button == "up" or button == "down"
                    local first = direction and 10 or 16
                    local duration = button == "down" and 30 or (direction and 8 or 4)
                    if action_phase >= first and action_phase < first + duration then fields[button]:set_value(1) end
                end
                if action[4] and action_phase >= 24 and action_phase <= 27 then fields[action[4]]:set_value(1) end
                if action_phase == 25 or action_phase == 40 then
                    screen:snapshot(string.format("basic_%02d_%s_%02d.png", action_number,
                        action[1]:gsub(" ", "_"), action_phase))
                end
                if action_phase == 85 then
                    local passed, observed = false, {}
                    for _, expected in ipairs(action[3]) do if basic_seen[expected] then passed = true end end
                    for index in pairs(basic_seen) do observed[#observed + 1] = index end
                    table.sort(observed)
                    basic_checks = basic_checks + 1
                    if not passed then basic_errors = basic_errors + 1 end
                    print(string.format("MK2KS_BASIC_CHECK pass=%s action=%d name=%s animations=%s",
                        tostring(passed), action_number, action[1], table.concat(observed, ",")))
                end
            end
        elseif direct_sequence and move >= 1 and move <= 3 then
            if (phase >= 62 and phase <= 64) or (phase >= 67 and phase <= 69) then
                fields.right:set_value(1)
            end
            if phase >= 68 and phase <= 70 then
                fields[move == 1 and "hp" or (move == 2 and "lp" or "hk")]:set_value(1)
            end
        elseif move == 0 then
            -- Let the CPU opponent exercise hit, knockdown and recovery states.
        elseif move == 4 and phase >= 61 and phase <= 66 then
			fields.block:set_value(1)
			fields.lk:set_value(1)
		elseif phase >= 61 and phase <= 66 then
            fields.block:set_value(1)
            if move == 1 then fields.hp:set_value(1)
            elseif move == 2 then fields.lp:set_value(1)
            else fields.hk:set_value(1) end
        end
        if capture_combat and fight_age <= 600 and fight_age % 2 == 0 then
            manager.machine.video:snapshot()
        end
    end

    if frame % 300 == 0 then
        local p1x = program and program:read_u16(0x01034f20) or 0
        local p2x = program and program:read_u16(0x01035130) or 0
        local p1id = program and program:read_u16(0x01035080) or 0
        print(string.format("MK2KS_STATE frame=%d css=%s yellow=%d green=%d fight_age=%d p1x=%04X p2x=%04X p1id=%04X",
            frame, tostring(css_selected), yellow, green, fight_age, p1x, p2x, p1id))
		if frame == 1200 or frame == 1500 or frame == 1800 or
				frame == 2400 or frame == 3000 or frame == 3600 or frame == 4200 then
			manager.machine.video:snapshot()
		end
    end
end)

emu.register_stop(function()
    local cpu = manager.machine.devices[":maincpu"]
    if cpu then
        local state = cpu.state
        print(string.format(
            "MK2KS_STOP frame=%d age=%d pc=%08X A0=%08X A1=%08X A2=%08X A3=%08X A4=%08X A8=%08X A9=%08X A10=%08X A11=%08X B0=%08X B1=%08X B8=%08X",
            frame, fight_age, state["PC"].value, state["A0"].value,
            state["A1"].value, state["A2"].value, state["A3"].value,
            state["A4"].value, state["A8"].value, state["A9"].value,
            state["A10"].value, state["A11"].value, state["B0"].value,
            state["B1"].value, state["B8"].value))
		if program then
			local stack = {}
			local sp = state["SP"].value
			for delta = 0, 0x100, 0x20 do
				stack[#stack + 1] = string.format("%08X=%08X", sp + delta, program:read_u32(sp + delta))
			end
			print("MK2KS_STOP_STACK " .. table.concat(stack, " "))
			local matches, nonzero = {}, 0
			for index = 0, 60 do
				local value = program:read_u32(0x0105bb30 + index * 0x40)
				if value ~= 0 then nonzero = nonzero + 1 end
				if value == 0xffafe5a0 then matches[#matches + 1] = index end
			end
			print(string.format("MK2KS_TABLE nonzero=%d target_indices=%s",
				nonzero, table.concat(matches, ",")))
			print(string.format("MK2KS_ROOT_HITS fighter=%s move=%d main=%d variant=%d effect=%d",
				fighter, move, root_hits["MK2KS root probe"] or 0,
				root_hits["MK2KS variant root probe"] or 0,
				root_hits["MK2KS projectile variant root probe"] or 0))
			local offsets = {}
			for offset in pairs(move_root_offsets) do offsets[#offsets + 1] = offset end
			table.sort(offsets)
			for index, offset in ipairs(offsets) do offsets[index] = string.format("%03X", offset) end
			print("MK2KS_MOVE_ROOT_OFFSETS " .. table.concat(offsets, ","))
			local activated = (root_hits["MK2KS root probe"] or 0) > 0
			-- A real native projectile must consume its own DMA frame. An unused
			-- animation-skin variant is no longer evidence of move activation.
			if move == 1 and not basic_actions then activated = activated and native_effect_reads > 0 end
			print(string.format("MK2KS_EFFECT_RESULT native_frame_reads=%d", native_effect_reads))
			local passed = fight_age > 600 and activated and stalled_frames == 0 and trap_frames == 0 and
				roster_errors == 0 and identity_errors == 0
			print(string.format("MK2KS_ROSTER_RESULT roster_errors=%d identity_errors=%d", roster_errors, identity_errors))
			if basic_actions then
				passed = passed and basic_checks == #actions and basic_errors == 0
				print(string.format("MK2KS_BASIC_RESULT pass=%s checks=%d errors=%d", tostring(passed), basic_checks, basic_errors))
			end
			print(string.format("MK2KS_MOVE_RESULT pass=%s fighter=%s move=%d fight_frames=%d stalled_frames=%d trap_frames=%d",
				tostring(passed), fighter, move, fight_age, stalled_frames, trap_frames))
		end
    end
end)
