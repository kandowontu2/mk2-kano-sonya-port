-- Historical diagnostic only. Its screen:pixel/palette-index assumptions are
-- invalid for this MAME build, so its old visual counters are NOT pass evidence.
-- Use mk2ks_selector_exit_test.lua and mk2ks_selector_navigation_test.lua instead.
print("MK2KS_LEGACY_WARNING: visual counters in this probe are invalid; use the RGB selector regressions")
local frame = 0
local css_frame = 0
local custom_frame = 0
local confirm_frame = 0
local fighter = os.getenv("MK2KS_TEST_FIGHTER") or "kano"
local dwell = tonumber(os.getenv("MK2KS_TEST_DWELL") or "120")
local confirm_hold = tonumber(os.getenv("MK2KS_TEST_CONFIRM_HOLD") or "4")
local fields, screen, program
local last_screen = "boot"
local battle_plan_seen = false
local fight_seen = false
local pending_snapshot = nil
local trace_css_objects = os.getenv("MK2KS_TRACE_CSS_OBJECTS") == "1"
local css_object_tap = nil
local css_object_seen = {}
local trace_identity = os.getenv("MK2KS_TRACE_IDENTITY") == "1"
local identity_tap = nil
local identity_seen = {}
local identity_write_tap = nil
local identity_write_seen = {}
local identity_write_count = 0
local trace_ladder = os.getenv("MK2KS_TRACE_LADDER") == "1"

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

local function custom_portrait_pixels()
    local count = 0
    for _, bounds in ipairs({ { 20, 77 }, { 320, 377 } }) do
        for y = 20, 97 do
            for x = bounds[1], bounds[2] do
                local index = screen:pixel(x, y) & 0x7fff
                if index >= 0x7e00 and index < 0x7e80 then count = count + 1 end
            end
        end
    end
    return count
end

local function trace_ladder_rows()
    if not trace_ladder then return end
    for y = 30, 220 do
        local nonzero, first, last_x = 0, -1, -1
        for x = 80, 220 do
            local index = screen:pixel(x, y) & 0x7fff
            if index ~= 0 then
                nonzero = nonzero + 1
                if first < 0 then first = x end
                last_x = x
            end
        end
        if nonzero >= 4 then
            print(string.format("MK2KS_LADDER_ROW y=%d nonzero=%d first=%d last=%d",
                y, nonzero, first, last_x))
        end
    end
end

local function active(first, duration)
    return frame >= first and frame < first + duration
end

local function capture_snapshot(label)
    local custom = screen and custom_portrait_pixels and custom_portrait_pixels() or -1
    print(string.format("MK2KS_ROSTER snapshot=%s frame=%d custom_pixels=%d", label, frame, custom))
    manager.machine.video:snapshot()
end

local function snapshot(label)
    if frame % 2 == 0 then
        capture_snapshot(label)
    else
        pending_snapshot = label
    end
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        fields = {
            hp = high["P1 High Punch"], left = high["P1 Left"],
            right = high["P1 Right"], coin = system["Coin 1"],
            start = system["1 Player Start"]
        }
        screen = manager.machine.screens[":screen"]
        program = manager.machine.devices[":maincpu"].spaces["program"]
        if trace_identity then
            identity_tap = program:install_read_tap(0x01035080, 0x0103508f,
                "MK2KS identity read probe", function(offset, data, mask)
                    if data == 0x11 or data == 0x12 then
                        local state = manager.machine.devices[":maincpu"].state
                        local pc = state["PC"].value
                        local identity_key = pc == 0xff83b820 and
                            string.format("%08X:%08X", pc, state["A1"].value) or pc
                        if not identity_seen[identity_key] then
                            identity_seen[identity_key] = true
                            print(string.format(
                                "MK2KS_ID_READ frame=%d addr=%08X data=%04X pc=%08X A0=%08X A1=%08X A8=%08X A9=%08X A14=%08X",
                                frame, offset, data & 0xffff, pc, state["A0"].value,
                                state["A1"].value, state["A8"].value,
                                state["A9"].value, state["A14"].value))
                        end
                    end
                end)
            if os.getenv("MK2KS_TRACE_IDENTITY_WRITES") == "1" then
            identity_write_tap = program:install_write_tap(0x01000000, 0x011fffff,
                "MK2KS identity write probe", function(offset, data, mask)
                    if confirm_frame > 0 and frame <= confirm_frame + 120 and
                            (data == 1 or data == 0x11 or data == 0x12) and
                            identity_write_count < 240 then
                        local state = manager.machine.devices[":maincpu"].state
                        local key = string.format("%08X:%08X:%04X", offset,
                            state["PC"].value, data & 0xffff)
                        if not identity_write_seen[key] then
                            identity_write_seen[key] = true
                            identity_write_count = identity_write_count + 1
                            print(string.format(
                                "MK2KS_ID_WRITE frame=%d age=%d addr=%08X data=%04X pc=%08X A0=%08X A1=%08X A8=%08X A9=%08X",
                                frame, frame - confirm_frame, offset, data & 0xffff,
                                state["PC"].value, state["A0"].value,
                                state["A1"].value, state["A8"].value,
                                state["A9"].value))
                        end
                    end
                end)
            end
        end
        if trace_css_objects then
            css_object_tap = program:install_read_tap(0xff9138b0, 0xff91492f,
                "MK2KS CSS object probe", function(offset, data, mask)
                    if custom_frame > 0 and confirm_frame == 0 then
                        local state = manager.machine.devices[":maincpu"].state
                        local key = string.format("%08X:%08X:%08X", state["A8"].value,
                            state["PC"].value, offset)
                        if not css_object_seen[key] then
                            css_object_seen[key] = true
                            print(string.format("MK2KS_CSS_OBJECT frame=%d A8=%08X PC=%08X rootread=%08X A0=%08X A9=%08X",
                                frame, state["A8"].value, state["PC"].value, offset,
                                state["A0"].value, state["A9"].value))
                        end
                    end
                end)
        end
    end

    for _, field in pairs(fields) do field:clear_value() end

    if pending_snapshot and frame % 2 == 0 then
        local label = pending_snapshot
        pending_snapshot = nil
        capture_snapshot(label)
    end

    if active(300, 4) then fields.hp:set_value(1) end
    if css_frame == 0 and frame >= 600 then
        local cycle = (frame - 600) % 300
        if cycle < 4 then fields.coin:set_value(1) end
        if cycle >= 20 and cycle < 24 then fields.start:set_value(1) end
    end

    local yellow = ((confirm_frame > 0) or frame % 5 == 0) and yellow_header_pixels() or 0
    if css_frame == 0 and frame > 700 and yellow > 20 and yellow < 100 then
        css_frame = frame
        print(string.format("MK2KS_ROSTER css_yellow_pixels=%d", yellow))
        snapshot("css_initial")
    end

    if css_frame > 0 and custom_frame == 0 then
        local age = frame - css_frame
        if fighter == "kano" then
            if age >= 12 and age < 16 then fields.left:set_value(1) end
            if age == 24 then
                custom_frame = frame
                snapshot("kano_selected")
            end
        else
            for _, first in ipairs({ 12, 24, 36, 48 }) do
                if age >= first and age < first + 4 then fields.right:set_value(1) end
            end
            if age == 60 then
                custom_frame = frame
                snapshot("sonya_selected")
            end
        end
    end

    if custom_frame > 0 and confirm_frame == 0 then
        local age = frame - custom_frame
        if dwell >= 48 and age == 24 then snapshot("selected_anim_24") end
        if dwell >= 72 and age == 48 then snapshot("selected_anim_48") end
        if age == math.max(1, dwell - 1) then snapshot("before_confirm") end
        if age >= dwell and age < dwell + confirm_hold then fields.hp:set_value(1) end
        if age == dwell + confirm_hold then
            confirm_frame = frame
            print(string.format("MK2KS_ROSTER confirmed fighter=%s dwell=%d hold=%d frame=%d",
                fighter, dwell, confirm_hold, frame))
        end
    end

    if confirm_frame > 0 then
        local age = frame - confirm_frame
        if age == 45 then snapshot("after_confirm") end
        if age == 90 then snapshot("transition_90") end
        if age == 150 then snapshot("transition_150") end
        if age == 240 then snapshot("transition_240") end
        if yellow >= 100 and not battle_plan_seen then
            battle_plan_seen = true
            last_screen = "battle_plan"
            print(string.format("MK2KS_ROSTER battle_plan_custom_pixels=%d", custom_portrait_pixels()))
            trace_ladder_rows()
            snapshot("battle_plan")
        end
        if frame % 5 == 0 then
            local green = green_bar_pixels()
            local p1id = program:read_u16(0x01035080)
            local expected_id = fighter == "kano" and 0x11 or 0x12
            if age > 300 and p1id == expected_id and green > 100 and not fight_seen then
                fight_seen = true
                last_screen = "fight"
                snapshot("fight")
            end
        end
    end

    if frame % 300 == 0 then
        local p1id = program:read_u16(0x01035080)
        print(string.format(
            "MK2KS_ROSTER state frame=%d css=%d custom=%d confirm=%d screen=%s p1id=%04X pc=%08X",
            frame, css_frame, custom_frame, confirm_frame, last_screen, p1id,
            manager.machine.devices[":maincpu"].state["PC"].value))
    end
end)

emu.register_stop(function()
    print(string.format(
        "MK2KS_ROSTER_RESULT fighter=%s dwell=%d hold=%d css=%s battle_plan=%s fight=%s frame=%d pc=%08X",
        fighter, dwell, confirm_hold, tostring(css_frame > 0), tostring(battle_plan_seen),
        tostring(fight_seen), frame, manager.machine.devices[":maincpu"].state["PC"].value))
end)
