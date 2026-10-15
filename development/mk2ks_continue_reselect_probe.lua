-- Input-only probe: buy CONTINUE, reselect, and enter a real second match.
dofile("mk2ks_selector_exit_test.lua")

local target = os.getenv("MK2KS_RESELECT_TARGET") or "sub_zero"
local targets = {sub_zero={id=8,route={"down"}},
    kano={id=17,route={"left"}},
    sonya={id=18,route={"right","right","right","right"}}}
assert(targets[target], "Unsupported continue-reselect target")
local expected = targets[target]
local frame, loss, reselect, match, last_mode = 0, nil, nil, nil, nil
local fields
local function check_native_shadow()
    if target == "sub_zero" then return end
    local ui = manager.machine.memory.regions[":ksui"]
    local colors = ui:read_u8(6) | (ui:read_u8(7) << 8)
    local names = 8 + 2 * (colors * 2 + ui:read_u8(4) * ui:read_u8(5))
    local w, h = ui:read_u8(names), ui:read_u8(names + 1)
    local base = names + 2 + (target == "kano" and 0 or w * h)
    local first, last, face = w, -1, {}
    for y = 0, 9 do
        for x = 0, w - 1 do
            if ui:read_u8(base + y * w + x) > 48 then
                first, last = math.min(first, x), math.max(last, x)
                face[y * w + x] = true
            end
        end
    end
    local expected_pixels, matched = 0, 0
    local pixels, width = manager.machine.screens[":screen"]:pixels()
    for y = 0, 9 do
        for x = first + 1, last + 1 do
            if not face[y * w + x] and (face[y * w + x - 1] or
                (y > 0 and face[(y - 1) * w + x - 1])) then
                expected_pixels = expected_pixels + 1
                local px = 29 + x - first
                local actual = string.unpack("<I4", pixels, ((30 + y) * width + px) * 4 + 1) & 0xffffff
                if actual == 0x420000 then matched = matched + 1 end
            end
        end
    end
    print(string.format("MK2KS_RESELECT_SHADOW target=%s matched=%d expected=%d pass=%s",
        target, matched, expected_pixels, tostring(expected_pixels > 20 and matched == expected_pixels)))
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local system = manager.machine.ioport.ports[":IN1"].fields
        local high = manager.machine.ioport.ports[":IN0"].fields
        fields = {coin=system["Coin 1"], start=system["1 Player Start"],
            down=high["P1 Down"], left=high["P1 Left"],
            right=high["P1 Right"], hp=high["P1 High Punch"]}
    end
    if frame < 2000 then return end
    local program = manager.machine.devices[":maincpu"].spaces.program
    local mode = program:read_u16(0x010601d0)
    local state = program:read_u16(0x010601f0)
    local hp = program:read_u16(0x010602f0)
    local stage = program:read_u16(0x01061b30)
    if mode ~= last_mode then
        print(string.format("MK2KS_CONTINUE_MODE frame=%d mode=%d state=%d stage=%d hp=%d roster=%d actor=%08X",
            frame, mode, state, stage, hp, program:read_u16(0x01060280),
            program:read_u32(0x01060220)))
        last_mode = mode
    end
    if not loss and stage <= 1 and mode == 3 and state == 2 and hp == 0 and
        program:read_u32(0x01060220) == 0 then
        loss = frame
        print(string.format("MK2KS_CONTINUE_LOSS frame=%d stage=%d", frame, stage))
    end
    if loss then
        local age = frame - loss
        -- The cabinet's CONTINUE screen charges two credits; the first
        -- early coin survives, but START is ignored until the screen opens.
        if (age >= 20 and age < 25) or (age >= 270 and age < 275) then
            fields.coin:set_value(1)
        end
        if age >= 310 and age < 315 then fields.start:set_value(1) end
        if age == 0 or age == 30 or age == 60 or age == 120 or
            age == 240 or age == 300 or age == 330 or age == 360 or
            age == 480 or age == 600 then
            print(string.format("MK2KS_CONTINUE_FRAME frame=%d age=%d mode=%d state=%d stage=%d hp=%d roster=%d",
                frame, age, mode, state, stage, hp, program:read_u16(0x01060280)))
            manager.machine.video:snapshot()
        end
    end
    if loss and not reselect and mode == 4 and state == 3 then
        reselect = frame
        print(string.format("MK2KS_RESELECT frame=%d initial_roster=%d",
            frame, program:read_u16(0x01060280)))
    end
    if reselect then
        local age = frame - reselect
        -- Liu Kang is the initial cursor on a continuation. Follow the
        -- actual roster grid to the requested stock or added fighter.
        for index, direction in ipairs(expected.route) do
            local begin = 56 + (index - 1) * 12
            if age >= begin and age < begin + 5 then fields[direction]:set_value(1) end
        end
        if age >= 148 and age < 156 then fields.hp:set_value(1) end
        if age == 0 or age == 65 or age == 105 or age == 145 or
            age == 170 or age == 270 then
            print(string.format("MK2KS_RESELECT_FRAME frame=%d age=%d mode=%d roster=%d",
                frame, age, mode, program:read_u16(0x01060280)))
            manager.machine.video:snapshot()
        end
        local actor = program:read_u32(0x01060220)
        if not match and mode == 2 and
            program:read_u16(0x01060280) == expected.id and
            actor >= 0x01000000 and actor < 0x01100000 and
            program:read_u16(actor + 0x1f0) == expected.id and hp == 161 then
            match = frame
            print(string.format("MK2KS_RESELECT_MATCH frame=%d target=%s id=%d actor=%08X",
                frame, target, expected.id, actor))
            manager.machine.video:snapshot()
        end
        if match and frame == match + 120 then
            check_native_shadow()
            print(string.format("MK2KS_RESELECT_COMBAT frame=%d target=%s id=%d actor=%d",
                frame, target, program:read_u16(0x01060280),
                actor >= 0x01000000 and actor < 0x01100000 and
                    program:read_u16(actor + 0x1f0) or 0xffff))
            manager.machine.video:snapshot()
        end
    end
end)
