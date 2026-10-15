local frame, css_frame = 0, 0
local fields, screen
local pending_snapshot = nil
local checks, failures = 0, 0
local custom_background, pose_background, first_pose = nil, nil, nil
local blink_colors = {}
local blink_trace = {native = {}, stock = {}}
local target = os.getenv("MK2KS_NAV_FIGHTER") or "sonya"
assert(target == "kano" or target == "sonya")
local routes = {
    kano = {{"left",12},{"right",72},{"left",96},{"right",120},
        {"left",144},{"right",168},{"left",192}},
    sonya = {{"right",12},{"right",24},{"right",36},{"right",48},
        {"left",72},{"right",96},{"left",120},{"left",144},
        {"right",168},{"right",192}}
}
local visits = {
    kano = {{60,"kano_1",19},{84,"liu_1",79},{108,"kano_2",19},
        {132,"liu_2",79},{156,"kano_3",19},{180,"liu_3",79},
        {204,"kano_4",19}},
    sonya = {{60,"sonya_1",319},{84,"reptile_1",259},
        {108,"sonya_2",319},{132,"reptile_2",259},
        {156,"cage",199},{180,"reptile_3",259},{204,"sonya_3",319}}
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

local function snapshot(label)
    if frame % 2 == 0 then
        print(string.format("MK2KS_NAV snapshot=%s frame=%d", label, frame))
        manager.machine.video:snapshot()
    else
        pending_snapshot = label
    end
end

local function pulse(field, age, first)
    if age >= first and age < first + 4 then field:set_value(1) end
end

local function check_cell(label, left)
    local border, number = 0, 0
    for y = 20, 97 do
        for x = left, left + 62 do
            local r, g, b = rgb(pixel(x, y))
            if g > 70 and g > r * 2 and g > b * 2 then
                if x < left + 4 or x > left + 58 or y < 24 or y > 93 then border = border + 1 end
                if x >= left + 25 and x <= left + 37 and y >= 32 and y <= 55 then number = number + 1 end
            end
        end
    end
    checks = checks + 1
    if border < 100 or number < 8 then failures = failures + 1 end
    print(string.format("MK2KS_NAV_CELL label=%s border=%d number=%d", label, border, number))
end

local function sample_background()
    local result = {}
    for y = 98, 105 do
        for x = 5, 73 do result[#result + 1] = {x, y, pixel(x, y)} end
    end
    return result
end

local function sample_pose_background()
    local result = {}
    -- Include the whole backdrop behind the select animation, not just
    -- the narrow strip above it. Most of these pixels are unchanged
    -- background; the different stock/native silhouettes are outliers.
    for y = 110, 240, 2 do
        for x = 5, 73, 2 do result[#result + 1] = {x, y, pixel(x, y)} end
    end
    return result
end

local function check_background()
    local best_shift, best_error = nil, math.huge
    for shift = -2, 2 do
        local total = 0
        for _, p in ipairs(custom_background) do
            local r, g, b = rgb(p[3])
            local nr, ng, nb = rgb(pixel(p[1] + shift, p[2]))
            total = total + math.abs(r - nr) + math.abs(g - ng) + math.abs(b - nb)
        end
        if total < best_error then best_shift, best_error = shift, total end
    end
    checks = checks + 1
    if best_shift ~= 0 then failures = failures + 1 end
    print(string.format("MK2KS_NAV_BACKGROUND best_shift=%d mean_channel_error=%.3f", best_shift, best_error / #custom_background / 3))

    local best_x, best_y, best_exact = nil, nil, -1
    local unshifted, runner_up = 0, 0
    for dy = -2, 2 do
        for dx = -2, 2 do
            local exact = 0
            for _, p in ipairs(pose_background) do
                if p[3] == pixel(p[1] + dx, p[2] + dy) then exact = exact + 1 end
            end
            if dx == 0 and dy == 0 then unshifted = exact
            else runner_up = math.max(runner_up, exact) end
            if exact > best_exact then best_x, best_y, best_exact = dx, dy, exact end
        end
    end
    if best_x ~= 0 or best_y ~= 0 or unshifted < 500 or
        unshifted <= runner_up * 2 then failures = failures + 1 end
    print(string.format("MK2KS_NAV_POSE_BACKGROUND best_shift=%d,%d exact=%d runner_up=%d sampled=%d",
        best_x, best_y, unshifted, runner_up, #pose_background))
end

local function check_pose(first)
    local pose, changed = {}, 0
    for y = 110, 240 do
        for x = 5, 75 do
            pose[#pose + 1] = pixel(x, y)
            if first_pose and pose[#pose] ~= first_pose[#pose] then changed = changed + 1 end
        end
    end
    if first then first_pose = pose else
        checks = checks + 1
        if changed < 10 then failures = failures + 1 end
        print(string.format("MK2KS_NAV_ANIMATION changed_pixels=%d", changed))
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
    end

    frame_pixels, pixel_width = screen:pixels()
    for _, field in pairs(fields) do field:clear_value() end
    if pending_snapshot and frame % 2 == 0 then
        local label = pending_snapshot
        pending_snapshot = nil
        snapshot(label)
    end

    if frame >= 300 and frame < 304 then fields.hp:set_value(1) end
    if css_frame == 0 and frame >= 600 then
        local cycle = (frame - 600) % 300
        if cycle < 4 then fields.coin:set_value(1) end
        if cycle >= 20 and cycle < 24 then fields.start:set_value(1) end
    end

    if css_frame == 0 and frame > 700 and frame % 5 == 0 then
        local yellow = yellow_header_pixels()
        if yellow >= 400 and yellow <= 430 then
            css_frame = frame
            snapshot("liu")
        end
    end

    if css_frame > 0 then
        local age = frame - css_frame
        for _, step in ipairs(routes[target]) do pulse(fields[step[1]], age, step[2]) end
        pulse(fields.hp, age, 216)
        for index, visit in ipairs(visits[target]) do
            if age == visit[1] then
                snapshot(visit[2])
                check_cell(visit[2], visit[3])
                if index == 1 then
                    custom_background = sample_background()
                    pose_background = sample_pose_background()
                    check_pose(true)
                end
                if index == 2 then check_background() end
            end
        end
        if age == 67 then check_pose(false); snapshot(target .. "_animated") end
        if age >= 54 and age <= 70 then
            local color = pixel(target == "kano" and 19 or 319, 25)
            blink_colors[color] = true
            blink_trace.native[#blink_trace.native + 1] = string.format("%08X", color)
        end
        if age >= 78 and age <= 94 then
            blink_trace.stock[#blink_trace.stock + 1] = string.format("%08X",
                pixel(target == "kano" and 79 or 259, 25))
        end
    end
end)

emu.register_stop(function()
    local colors = 0
    for _ in pairs(blink_colors) do colors = colors + 1 end
    local blink_mismatches = math.abs(#blink_trace.native - #blink_trace.stock)
    for index = 1, math.min(#blink_trace.native, #blink_trace.stock) do
        if blink_trace.native[index] ~= blink_trace.stock[index] then
            blink_mismatches = blink_mismatches + 1
        end
    end
    checks = checks + 1
    if colors < 2 or #blink_trace.native ~= 17 or blink_mismatches > 0 then
        failures = failures + 1
    end
    print(string.format("MK2KS_NAV_BLINK colors=%d samples=%d stock_mismatches=%d",
        colors, #blink_trace.native, blink_mismatches))
    print(string.format("MK2KS_NAV_BLINK_TRACE native=%s stock=%s",
        table.concat(blink_trace.native, ","), table.concat(blink_trace.stock, ",")))
    print(string.format("MK2KS_NAV_RESULT pass=%s checks=%d failures=%d css=%s frame=%d",
        tostring(css_frame > 0 and checks == 10 and failures == 0), checks, failures, tostring(css_frame > 0), frame))
end)
