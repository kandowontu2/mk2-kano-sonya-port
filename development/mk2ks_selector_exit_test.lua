-- Input-driven regression. RGB buffers are relative to the visible game area;
-- screen:pixel uses absolute screen coordinates and already returns RGB.
local frame, css_frame, exit_frame, hud_frame = 0, 0, 0, 0
local fighter = os.getenv("MK2KS_TEST_FIGHTER") or "stock"
local confirm = os.getenv("MK2KS_TEST_CONFIRM") or "lp"
local hold = tonumber(os.getenv("MK2KS_TEST_CONFIRM_HOLD") or "8")
local confirm_at_age = tonumber(os.getenv("MK2KS_TEST_CONFIRM_AT_AGE") or "96")
assert(confirm_at_age >= 96 and confirm_at_age <= 370)
local boot_frame = tonumber(os.getenv("MK2KS_TEST_BOOT_FRAME") or "600")
assert(boot_frame >= 600 and boot_frame <= 1500 and boot_frame % 1 == 0)
local two_player = os.getenv("MK2KS_TWO_PLAYER") == "1"
local p2_shang = two_player and dofile("mk2ks_native_shang_morph.lua")
local p2_fighter = os.getenv("MK2KS_P2_FIGHTER") or "stock"
local roster_ids = {kung_lao=0,liu_kang=1,cage=2,baraka=3,kitana=4,mileena=5,
    shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11,kano=17,sonya=18}
local selection_routes = {
    {kano={"left"},sonya={"right","right","right","right"},liu_kang={},kung_lao={"right"},
     cage={"right","right"},reptile={"right","right","right"},sub_zero={"down"},
     shang_tsung={"right","down"},kitana={"right","right","down"},jax={"right","right","right","down"},
     mileena={"down","down"},baraka={"right","down","down"},
     scorpion={"right","right","down","down"},raiden={"right","right","right","down","down"}},
    {sonya={"right"},kano={"left","left","left","left"},reptile={},cage={"left"},kung_lao={"left","left"},
     liu_kang={"left","left","left"},jax={"down"},kitana={"left","down"},shang_tsung={"left","left","down"},
     sub_zero={"left","left","left","down"},raiden={"down","down"},scorpion={"left","down","down"},
     baraka={"left","left","down","down"},mileena={"left","left","left","down","down"}}
}
local selection_checks, selection_errors, ladder_entries, p2_identity_errors = 0, 0, 0, 0
local p2_cpu_schedule_checks = 0
local p2_cpu_win_checks = 0
local p2_cpu_loss_checks = 0
local p1_cpu_schedule_checks = 0
local p2_joined = false
local fields, screen, program, pixels, width
local snapshots, outside_frames, leaks, identity_errors = 0, 0, 0, 0
local references, reference_count = {}, 0
local combat_frames = 0
local name_checks, name_errors, name_mask = 0, 0, nil
local name_masks = {}
local dma_tap, dma_regs, dma_seen = nil, {}, {}
local animation_taps, last_animation, reaction_task = {}, nil, nil
local position_tap, last_y, position_writes = nil, nil, 0
local assert_lifecycle = os.getenv("MK2KS_ASSERT_LIFECYCLE") == "1"
local allow_no_recovery = os.getenv("MK2KS_LIFECYCLE_ALLOW_NO_RECOVERY") == "1"
local recovery_start, recoveries, recovery_errors = nil, 0, 0
local object_resets, ground_errors, position_errors = 0, 0, 0
local roster_errors, native_names, native_wins, native_finishes = 0, 0, 0, 0
local native_p2_wins = 0
local released_actor_fields = 0
local last_native_hud_frame, constructing_actor_fields = -10, 0
local last_native_win_frame = -1000
local last_native_p2_win_frame = -1000
local last_hud_stage,stage_change_frame,transition_actor_fields=nil,-1000,0
local last_native_p2_hud_frame = -10
local native_taps, finish_tap, win_capture, finish_capture = {}, nil, nil, nil
local round_win = os.getenv("MK2KS_TEST_ROUND_WIN") == "1"
local allow_natural_loss = os.getenv("MK2KS_ALLOW_NATURAL_LOSS") == "1"
local allow_continue_reselect = os.getenv("MK2KS_ALLOW_CONTINUE_RESELECT") == "1"
local round_win_strategy = os.getenv("MK2KS_ROUND_WIN_STRATEGY") or "stock"
local round_win_late_strategy = os.getenv("MK2KS_ROUND_WIN_LATE_STRATEGY") or ""
local round_win_late_stage = tonumber(os.getenv("MK2KS_ROUND_WIN_LATE_STAGE") or "8")
local projectile_close = os.getenv("MK2KS_PROJECTILE_CLOSE") or "uppercut"
local projectile_late_close = os.getenv("MK2KS_PROJECTILE_LATE_CLOSE") or ""
local projectile_late_stage = tonumber(os.getenv("MK2KS_PROJECTILE_LATE_STAGE") or "8")
local round_loss = os.getenv("MK2KS_TEST_ROUND_LOSS") == "1"
local test_projectiles = os.getenv("MK2KS_TEST_PROJECTILES") == "1"
local projectile_command = os.getenv("MK2KS_PROJECTILE_COMMAND") or "native"
local projectile_entries, projectile_frames = {0, 0}, 0
local square_test = os.getenv("MK2KS_TEST_SQUARE") or ""
local square_entries, square_attack_reads = {0, 0}, 0
local square_trace_start, square_trace_fields = nil, 0
local square_samples, square_followup_entries, square_baseline = {}, 0, nil
local square_trace = os.getenv("MK2KS_TRACE_SQUARE") == "1"
local ball_test = os.getenv("MK2KS_TEST_BALL") or ""
local ball_holds = {short=30, boundary=80, minimum=81, held=10000, recharge=40}
local ball_hold = tonumber(os.getenv("MK2KS_BALL_HOLD") or "") or ball_holds[ball_test] or 185
local ball_negative = ball_test == "short" or ball_test == "boundary" or ball_test == "held" or
    ball_test == "airborne" or ball_test == "recharge" or ball_test == "wrong_button"
local ball_trace = os.getenv("MK2KS_TRACE_BALL") == "1"
local leg_test = os.getenv("MK2KS_TEST_LEG") or ""
local leg_corner=leg_test=="corner_left" or leg_test=="corner_right"
local leg_delay=leg_corner and 600 or 0
local leg_edge_start,leg_edge_end=nil,nil
local leg_boundary_checks,leg_boundary_errors,leg_release_clamps=0,0,0
local leg_boundary_pre,leg_release_boundary_age=nil,nil
local leg_entries, leg_attack_reads, leg_process, leg_baseline, leg_last = 0, 0, nil, nil, nil
local leg_start, leg_collision, leg_samples, leg_followups = nil, nil, {}, {0, 0}
local leg_side = tonumber(os.getenv("MK2KS_LEG_SIDE") or "") or (fighter == "sonya" and 1 or 2)
if leg_test~="" then assert(leg_side==1 or leg_side==2, "Invalid leg-grab player side") end
local leg_victim_name = leg_side == 1 and p2_fighter or fighter
local leg_victim_id = roster_ids[leg_victim_name]
local leg_victim_poses = {
    [0]={0xff916f90,0xff91a190,0xff91d860,0xff91d8e0,0xff91d9e0},
    [1]={0xff926750,0xff928410,0xff928470,0xff9284f0,0xff928550},
    [2]={0xff9307c0,0xff936c50,0xff936cb0,0xff936d30,0xff936d90},
    [3]={0xff93dff0,0xff945070,0xff9450d0,0xff945150,0xff9451d0},
    [4]={0xff94dce0,0xff94d900,0xff954f70,0xff955010,0xff955070},
    [6]={0xff95c080,0xff960100,0xff9631c0,0xff963220,0xff963260},
    [7]={0xff96a670,0xff9707f0,0xff970850,0xff9708f0,0xff970970},
    [8]={0xff97b850,0xff983db0,0xff983df0,0xff983e50,0xff983eb0},
    [11]={0xff992df0,0xff994e90,0xff994ed0,0xff994f30,0xff994f90},
    [17]={0xfe829800,0xfe82aa60,0xfe82aae0,0xfe82ab40,0xfe82ab80},
    [18]={0xfe836f00,0xfe83adc0,0xfe83ae60,0xfe83aec0,0xfe83af20}
}
leg_victim_poses[5]=leg_victim_poses[4]
leg_victim_poses[9]=leg_victim_poses[8]
leg_victim_poses[10]=leg_victim_poses[8]
local leg_stock_offsets = {
    [0]={{86,-4},{67,-53},{14,-50},{-48,5},{-94,33}},
    [1]={{84,1},{64,-42},{1,-49},{-48,-23},{-92,12}},
    [2]={{85,-8},{59,-33},{4,-50},{-53,-18},{-98,1}},
    [3]={{86,-10},{59,-23},{10,-61},{-68,-26},{-106,16}},
    [4]={{87,-3},{68,-41},{19,-62},{-56,-21},{-96,31}},
    [5]={{87,-3},{68,-41},{19,-62},{-56,-21},{-96,31}},
    [6]={{90,0},{68,-48},{10,-65},{-55,-50},{-99,13}},
    [7]={{91,-8},{66,-50},{2,-77},{-57,-32},{-107,30}},
    [8]={{83,-13},{62,-43},{8,-62},{-64,-41},{-107,16}},
    [9]={{83,-13},{62,-43},{8,-62},{-64,-41},{-107,16}},
    [10]={{83,-13},{62,-43},{8,-62},{-64,-41},{-107,16}},
    [11]={{86,-12},{63,-52},{4,-85},{-52,-35},{-96,25}}
}
local leg_modes = {near=true,far=true,block=true,duck=true,duck_block=true,air=true,
    no_down=true,no_block=true,no_lp=true,extra_button=true,airborne=true,held=true,block2=true,
    block_first=true,lp_first=true,down_last=true,block2_first=true,lp_first_block2=true,
    corner_left=true,corner_right=true}
if leg_test ~= "" then assert(leg_modes[leg_test], "Unknown leg-grab test: "..leg_test) end
local leg_negative = leg_test == "no_down" or leg_test == "no_block" or leg_test == "no_lp" or
    leg_test == "extra_button" or leg_test == "airborne" or leg_test == "down_last"
local ball_entries, ball_attack_reads, ball_followup_entries = 0, 0, 0
local ball_start, ball_first_collision, ball_samples = nil, nil, {}
local square_modes = {ground=true, air=true, block=true, air_block=true, far=true,
    reversed=true, expired=true, wrong_button=true, airborne=true, with_block=true}
if square_test ~= "" then assert(square_modes[square_test], "Unknown square test: " .. square_test) end
local assert_native_display = os.getenv("MK2KS_ASSERT_NATIVE_DISPLAY") == "1"
local display_checks, display_errors = 0, 0
local assert_hud_shadow = os.getenv("MK2KS_ASSERT_HUD_SHADOW") == "1"
local hud_shadow_masks, hud_shadow_checks, hud_shadow_errors = {}, 0, 0
local previous_pixels, unchanged_frames, stalled_frames, trap_frames = nil, 0, 0, 0
local campaign_high_stage, campaign_ended, campaign_lost, campaign_completed = 0, false, false, false
local p2_campaign_loss_seen = false
local p2_campaign_boss_win_seen = false
local p2_previous_stage,p2_previous_cpu,p2_stage_change_frame=nil,nil,-1000
local p2_pending_stage=nil
local unexpected_campaign_resets = 0

local function leg_geometry(label, actors)
    local function signed(n) return n >= 0x8000 and n - 0x10000 or n end
    for side, actor in ipairs(actors) do
        local cache = program:read_u32(actor + 0x1a0)
        local x, y = signed(program:read_u16(actor+0x90)), signed(program:read_u16(actor+0xb0))
        print(string.format("MK2KS_LEG_GEOMETRY %s side=%d actor=%08X id=%d x=%d y=%d cache=%08X frame=%08X flags=%04X",
            label,side,actor,program:read_u16(actor+0x1f0),x,y,cache,program:read_u32(actor+0x1d0),program:read_u16(actor+0xf0)))
        for part=0,15 do
            local at=cache+part*0x70
            local source=program:read_u32(at)
            if source==0 then break end
            local w,h=program:read_u16(at+0x20),program:read_u16(at+0x30)
            local dx,dy=signed(program:read_u16(at+0x50)),signed(program:read_u16(at+0x60))
            print(string.format("MK2KS_LEG_PART side=%d part=%d source=%08X width=%d height=%d dx=%d dy=%d bounds=%d,%d,%d,%d",
                side,part,source,w,h,dx,dy,x-dx,y-dy,x-dx+w,y-dy+h))
        end
    end
end

local function pixel(x, y)
    return string.unpack("<I4", pixels, (y * width + x) * 4 + 1) & 0xffffff
end

local function live_fighter_x(pointer_field)
    local actor = program:read_u32(pointer_field)
    if actor < 0x01000000 or actor >= 0x01100000 then return nil end
    local x = program:read_u16(actor + 0x90)
    return x >= 0x8000 and x - 0x10000 or x
end

local function rgb(x, y)
    local value = pixel(x, y)
    return (value >> 16) & 255, (value >> 8) & 255, value & 255
end

local function header()
    local count, early = 0, 0
    for y = 0, 24, 2 do
        for x = 40, 360, 2 do
            local r, g, b = rgb(x, y)
            if r > 175 and g > 140 and b < 100 then
                count = count + 1
                if y == 4 then early = early + 1 end
            end
        end
    end
    return count, early
end

local function hud()
    -- The middle of BOTH health bars is a continuous saturated run. Portrait
    -- pixels on the select screen must not count as a HUD.
    local counts = {}
    for i, left in ipairs({110, 220}) do
        local count = 0
        for x = left, left + 60 do
            local r, g, b = rgb(x, 30)
            if (g > 60 and g > r * 3 // 2 and g > b * 3 // 2) or
               (r > 60 and r > g * 3 // 2 and r > b * 3 // 2) then count = count + 1 end
        end
        counts[i] = count
    end
    return counts[1] >= 55 and counts[2] >= 55
end

local function snap(label)
    print(string.format("MK2KS_EXIT snapshot=%04d label=%s frame=%d", snapshots, label, frame))
    manager.machine.video:snapshot()
    snapshots = snapshots + 1
end

local function load_name_mask(name)
    name = name or fighter
    if name ~= "kano" and name ~= "sonya" then return nil end
    if name_masks[name] then return name_masks[name] end
    local ui = manager.machine.memory.regions[":ksui"]
    local colors = ui:read_u8(6) | (ui:read_u8(7) << 8)
    local names = 8 + 2 * (colors * 2 + ui:read_u8(4) * ui:read_u8(5))
    local w, h = ui:read_u8(names), ui:read_u8(names + 1)
    local base = names + 2 + (name == "kano" and 0 or w * h)
    local first_x, first_y = w, h
    for y = 0, h - 1 do
        for x = 0, w - 1 do
            if ui:read_u8(base + y * w + x) > 48 then
                first_x, first_y = math.min(first_x, x), math.min(first_y, y)
            end
        end
    end
    local mask = {}
    for y = 0, 9 do
        for x = 0, 71 do
            mask[#mask + 1] = x + first_x < w and y < h and
                ui:read_u8(base + y * w + x + first_x) > 48
        end
    end
    name_masks[name] = mask
    return mask
end

local function check_name(name)
    local mask = name and load_name_mask(name) or name_mask
    if not mask then return end
    local missing, extra, expected = 0, 0, 0
    for y = 0, 9 do
        for x = 0, 71 do
            local r, g, b = rgb(29 + x, 30 + y)
            local gold = r > 100 and g > 40 and r >= g * 4 // 5 and g > b * 2
            if mask[y * 72 + x + 1] then
                expected = expected + 1
                if not gold then missing = missing + 1 end
            elseif gold then extra = extra + 1 end
        end
    end
    name_checks = name_checks + 1
    if missing > expected * 0.05 or extra > 3 then
        name_errors = name_errors + 1
        print(string.format("MK2KS_NAME_ERROR frame=%d missing=%d extra=%d expected=%d", frame, missing, extra, expected))
        if name_errors <= 2 then snap("NAME_ERROR") end
    end
end

local function scheduled_p1_cpu(include_loss)
    -- P2's win/continue-expiry resumes a P2-human campaign, with P1 as CPU.
    -- Neither the departed P1 selection nor the P2 identity is the CPU ID.
    -- Require the actual native human states, a prior P2 victory, an unchanged
    -- P2 selection and membership of the chosen schedule in the ROM table.
    local p2_state=program:read_u16(0x01060dc0)
    local native_loss=include_loss and p2_state==2 and program:read_u16(0x010601d0)==3 and
        program:read_u16(0x01061b00)==1 and program:read_u16(0x01060ec0)==0 and
        program:read_u16(0x010602f0)>0 and frame-last_native_win_frame<=600
    if not two_player or not p2_joined or native_p2_wins < 2 or
        program:read_u16(0x010601f0) ~= 0 or (p2_state ~= 1 and not native_loss) or
        program:read_u16(0x01060e50) ~= roster_ids[p2_fighter] then return nil end
    local table = program:read_u32(0xff8a11f0)
    local schedule = program:read_u32(0x01061b10)
    local stage = program:read_u16(0x01061b30)
    if table ~= 0xfffa2c00 or stage > 16 then return nil end
    for order = 0,5 do
        if program:read_u32(table + order*32) == schedule then
            return program:read_u16(schedule + stage*16), stage, order
        end
    end
    return nil
end

local function load_shadow_masks()
    if not assert_hud_shadow then return end
    local ui = manager.machine.memory.regions[":ksui"]
    local colors = ui:read_u8(6) | (ui:read_u8(7) << 8)
    local names = 8 + 2 * (colors * 2 + ui:read_u8(4) * ui:read_u8(5))
    local w, h = ui:read_u8(names), ui:read_u8(names + 1)
    for side, name in ipairs({fighter, p2_fighter}) do
        if name == "kano" or name == "sonya" then
            local base = names + 2 + (name == "kano" and 0 or w * h)
            local first, last = w, -1
            local face = {}
            for y = 0, 9 do
                for x = 0, w - 1 do
                    if ui:read_u8(base + y * w + x) > 48 then
                        first, last = math.min(first, x), math.max(last, x)
                        face[y * w + x] = true
                    end
                end
            end
            assert(last >= first, "Empty HUD shadow reference")
            local width = last - first + 2
            local left = side == 1 and 29 or 367 - width
            local expected = {}
            for y = 0, 9 do
                for x = first + 1, last + 1 do
                    if not face[y * w + x] and (face[y * w + x - 1] or
                        (y > 0 and face[(y - 1) * w + x - 1])) then
                        expected[#expected + 1] = {left + x - first, 30 + y}
                    end
                end
            end
            assert(#expected > 20, "HUD shadow reference is too small")
            hud_shadow_masks[side] = expected
        end
    end
end

local function check_hud_shadows()
    for side, mask in pairs(hud_shadow_masks) do
        local matched = 0
        for _, xy in ipairs(mask) do
            -- Stock HUD palette pen 2 is the near-black maroon 0x420000.
            -- Transparent pen 0 would expose the green/red health bar here.
            if pixel(xy[1], xy[2]) == 0x420000 then matched = matched + 1 end
        end
        hud_shadow_checks = hud_shadow_checks + 1
        if matched ~= #mask then hud_shadow_errors = hud_shadow_errors + 1 end
        print(string.format("MK2KS_HUD_SHADOW side=%d frame=%d matched=%d expected=%d", side, frame, matched, #mask))
    end
end

local function remember_portraits()
    for _, left in ipairs({22, 322}) do
        for y = 28, 88, 4 do
            for x = left + 4, left + 48, 4 do
                references[#references + 1] = {x, y, pixel(x, y)}
            end
        end
    end
    reference_count = #references
end

local function portrait_matches()
    local counts = {0, 0}
    for i, reference in ipairs(references) do
        local side = i <= reference_count / 2 and 1 or 2
        if pixel(reference[1], reference[2]) == reference[3] then counts[side] = counts[side] + 1 end
    end
    return math.max(counts[1], counts[2])
end

local function pulse(field, age, first, duration)
    if age >= first and age < first + (duration or 4) then fields[field]:set_value(1) end
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high, system, low = ports[":IN0"].fields, ports[":IN1"].fields, ports[":IN2"].fields
        fields = {
            hp = high["P1 High Punch"], hk = high["P1 High Kick"],
            block = high["P1 Block"], lp = low["P1 Low Punch"],
            lk = low["P1 Low Kick"], block2 = low["P1 Block 2"],
            left = high["P1 Left"], right = high["P1 Right"], up = high["P1 Up"],
            down = high["P1 Down"],
            coin = system["Coin 1"], coin2 = system["Coin 2"],
            start = system["1 Player Start"], start2 = system["2 Players Start"],
            p2hp = high["P2 High Punch"], p2hk = high["P2 High Kick"],
            p2left = high["P2 Left"], p2right = high["P2 Right"],
            p2down = high["P2 Down"], p2lp = low["P2 Low Punch"],
            p2block = high["P2 Block"], p2up = high["P2 Up"]
        }
        fields.p2lk = low["P2 Low Kick"]
        fields.p2block2 = low["P2 Block 2"]
        screen = manager.machine.screens[":screen"]
        program = manager.machine.devices[":maincpu"].spaces["program"]
        for _, target in pairs(manager.machine.render.targets) do
            local view = target.current_view
            print(string.format("MK2KS_RENDER_TARGET index=%d hidden=%s view=%s has_art=%s screens=%d",
                target.index, tostring(target.hidden), view.name, tostring(view.has_art), view.visible_screen_count))
            if not target.hidden then
                display_checks = display_checks + 1
                if view.has_art or view.visible_screen_count ~= 1 then display_errors = display_errors + 1 end
            end
        end
        if os.getenv("MK2KS_TRACE_TABLES") == "1" then
            local seen = {}
            local sources = {0xff8333e0,0xff85cb40,0xff85e6b0,0xff8702c0,0xff87e3a0,0xff87f020,
                0xff880a70,0xff880d90,0xff8b5fc0,0xff8b66a0,0xff8b8440,0xff8ba390,0xff8bef70,
                0xff8cf110,0xff8d5340,0xff8d60d0,0xff8e5310,0xff907b30,0xff9109e0,0xff9599d0,
                0xff9a66a0,0xff9b1db0,0xff9b2210,0xff9b4930,0xff9b76d0,0xff9bc980,0xff9bde50,
                0xff9be7f0,0xff9bf750,0xff9c3310,0xff9c3c90,0xff9e9140,0xff9eca40,0xff9ecc30,
                0xff9ed0f0,0xff9f57b0,0xffa14980}
            for _, source in ipairs(sources) do
            native_taps[#native_taps + 1] = program:install_read_tap(source + 17 * 32, source + 19 * 32 - 1,
                "native character parameter audit", function(offset, data, mask)
                    if hud_frame == 0 or frame > hud_frame + 600 then return end
                    local state = manager.machine.devices[":maincpu"].state
                    local pc = state["PC"].value
                    local object = state["A8"].value
                    if pc < 0xff83b7f0 or pc > 0xff83b860 then return end
                    if object ~= 0x01034e90 and object ~= 0x010350a0 then return end
                    local key = string.format("%08x:%08x:%08x", offset, pc, object)
                    if seen[key] then return end
                    seen[key] = true
                    print(string.format("MK2KS_PARAMETER frame=%d pc=%08X address=%08X data=%04X A0=%08X A1=%08X A8=%08X caller=%08X",
                        frame, pc, offset, data & 0xffff, state["A0"].value, state["A1"].value,
                        object, program:read_u32(state["SP"].value)))
                end)
            end
        end
        if test_projectiles then
            for side, name in ipairs({fighter, p2_fighter}) do
                local root = name == "kano" and 0xff000000 or 0xff020000
                local expected_object = side == 1 and 0x01034e90 or 0x010350a0
                native_taps[#native_taps + 1] = program:install_read_tap(root + 39 * 32, root + 39 * 32 + 31,
                    "native projectile entry " .. side, function(offset, data, mask)
                        local state = manager.machine.devices[":maincpu"].state
                        if hud_frame > 0 and state["A8"].value == expected_object then
                            projectile_entries[side] = projectile_entries[side] + 1
                        end
                    end)
            end
            native_taps[#native_taps + 1] = program:install_read_tap(0xff602000, 0xff6028df,
                "native projectile DMA frames", function(offset, data, mask)
                    if hud_frame > 0 then projectile_frames = projectile_frames + 1 end
                end)
        end
        if square_test ~= "" then
            native_taps[#native_taps + 1] = program:install_read_tap(0xff0203c0, 0xff0203df,
                "Sonya square flight entry", function(offset, data, mask)
                    if hud_frame == 0 then return end
                    local object = manager.machine.devices[":maincpu"].state["A8"].value
                    local side = object == program:read_u32(0x01060220) and 1 or
                        (object == program:read_u32(0x01060df0) and 2 or nil)
                    if side then
                        square_entries[side] = square_entries[side] + 1
                        square_trace_start = square_trace_start or frame
                        print(string.format("MK2KS_SQUARE_ENTRY side=%d frame=%d", side, frame))
                    end
                end)
            native_taps[#native_taps + 1] = program:install_read_tap(0xffffda00, 0xffffda8f,
                "Sonya own square attack", function(offset, data, mask)
                    if hud_frame > 0 then square_attack_reads = square_attack_reads + 1 end
                end)
            native_taps[#native_taps + 1] = program:install_read_tap(0xff0204e0, 0xff0204ff,
                "Sonya post-square ring action", function(offset, data, mask)
                    local side = fighter == "sonya" and 1 or 2
                    if hud_frame > 0 and frame > hud_frame + 300 and
                        manager.machine.devices[":maincpu"].state["A8"].value ==
                            program:read_u32(side == 1 and 0x01060220 or 0x01060df0) then
                        square_followup_entries = square_followup_entries + 1
                    end
                end)
        end
        if ball_test ~= "" then
            native_taps[#native_taps + 1] = program:install_read_tap(0xff0000e0, 0xff0000ff,
                "Kano cannonball roll", function(offset, data, mask)
                    if hud_frame == 0 then return end
                    local cpu = manager.machine.devices[":maincpu"]
                    local action = program:read_u16(cpu.state["A13"].value + 0x1f0)
                    if action == 0x020b or action == 0x0602 then
                        ball_entries = ball_entries + 1
                        ball_start = ball_start or frame
                        print(string.format("MK2KS_BALL_ENTRY frame=%d action=%04X actor=%08X", frame, action, cpu.state["A8"].value))
                    end
                end)
            native_taps[#native_taps + 1] = program:install_read_tap(0xffffec00, 0xffffec8f,
                "Kano cannonball hitbox", function(offset, data, mask)
                    if hud_frame > 0 then
                        ball_attack_reads = ball_attack_reads + 1
                        ball_first_collision = ball_first_collision or frame
                    end
                end)
            native_taps[#native_taps + 1] = program:install_read_tap(0xff0004e0, 0xff0004ff,
                "Kano post-ball knife", function(offset, data, mask)
                    local side = fighter == "kano" and 1 or 2
                    if hud_frame > 0 and frame > hud_frame + 600 and
                        manager.machine.devices[":maincpu"].state["A8"].value ==
                            program:read_u32(side == 1 and 0x01060220 or 0x01060df0) then
                        ball_followup_entries = ball_followup_entries + 1
                    end
                end)
        end
        name_mask = load_name_mask()
        load_shadow_masks()
        if leg_test ~= "" then
            local cpu = manager.machine.devices[":maincpu"]
            native_taps[#native_taps + 1] = program:install_read_tap(0xfff83000, 0xfff830cf,
                "native leg entry", function(offset, data, mask)
                    if offset == 0xfff83000 then
                        leg_entries = leg_entries + 1
                        leg_start = leg_start or frame
                        leg_process = cpu.state.A13.value
                        print(string.format("MK2KS_LEG_ENTRY frame=%d actor=%08X process=%08X", frame, cpu.state.A8.value, leg_process))
                        if os.getenv("MK2KS_TRACE_LEG") == "1" then
                            for side, actor in ipairs({cpu.state.A8.value, program:read_u32(leg_process+0x140)}) do
                                native_taps[#native_taps+1] = program:install_write_tap(actor+0x40, actor+0x5f,
                                    "leg horizontal velocity observer", function(at, value, write_mask)
                                        if frame-hud_frame-leg_delay >= 300 and frame-hud_frame-leg_delay <= 380 then
                                            print(string.format("MK2KS_LEG_VX age=%d side=%d at=%08X value=%04X pc=%08X flags=%04X",
                                                frame-hud_frame,side,at,value,cpu.state.PC.value,program:read_u16(actor+0x160)))
                                        end
                                    end)
                            end
                        end
                    end
                end)
            native_taps[#native_taps + 1] = program:install_read_tap(0xfff83800, 0xfff8388f,
                "native leg collision", function(offset, data, mask)
                    leg_attack_reads = leg_attack_reads + 1
                    if offset == 0xfff83800 then
                        leg_collision = leg_collision or frame
                        print(string.format("MK2KS_LEG_COLLISION frame=%d", frame))
                        if os.getenv("MK2KS_TRACE_LEG") == "1" then
                            leg_geometry("collision", {cpu.state.A8.value,program:read_u32(cpu.state.A13.value+0x140)})
                        end
                    end
                end)
            assert(leg_victim_id and leg_victim_poses[leg_victim_id], "Unsupported leg victim: "..leg_victim_name)
            -- Observe the native boundary pass itself, not a frame sample that
            -- may precede VBLANK's clamp immediately after the release script.
            for _,entry in ipairs({0xff8054e0,0xff805630}) do
                native_taps[#native_taps+1]=program:install_read_tap(entry,entry+15,"leg boundary lifecycle",
                    function(offset,data,mask)
                        local age=frame-hud_frame
                        if hud_frame==0 or age<300+leg_delay or age>600+leg_delay then return end
                        local actor=program:read_u32(leg_side==1 and 0x01060df0 or 0x01060220)
                        if cpu.state.A2.value~=actor then return end
                        local process=program:read_u32(leg_side==1 and 0x01060e30 or 0x01060260)
                        local action=program:read_u16(process+0x1f0)
                        local function signed(n) n=n&0xffff;return n>=0x8000 and n-0x10000 or n end
                        local x=signed(program:read_u16(actor+0x90))
                        local left,right=signed(cpu.state.A0.value),signed(cpu.state.A1.value)
                        if entry==0xff8054e0 then
                            leg_boundary_pre={age=age,x=x,left=left,right=right}
                        elseif action==0x506 then
                            leg_boundary_checks=leg_boundary_checks+1
                            leg_release_boundary_age=leg_release_boundary_age or age
                            if x<left or x>right then leg_boundary_errors=leg_boundary_errors+1 end
                            if leg_boundary_pre and leg_boundary_pre.age==age and
                                (leg_boundary_pre.x<left or leg_boundary_pre.x>right) then
                                leg_release_clamps=leg_release_clamps+1
                                local expected=math.max(left,math.min(right,leg_boundary_pre.x))
                                if x~=expected or program:read_u32(actor+0x40)~=0 then
                                    leg_boundary_errors=leg_boundary_errors+1
                                end
                            end
                            if leg_boundary_checks<=2 then
                                print(string.format("MK2KS_LEG_BOUNDARY age=%d action=%04X x=%d bounds=%d,%d vx=%08X",
                                    age,action,x,left,right,program:read_u32(actor+0x40)))
                            end
                        elseif action==0x111 then
                            leg_boundary_errors=leg_boundary_errors+1
                        end
                    end)
            end
            local victim_root=program:read_u32(0xfffe4000+leg_victim_id*32)
            local followup_root=leg_victim_id>=17 and victim_root+39*32 or victim_root+6*32
            for index, definition in ipairs({{0xff0204e0,18,610,750},{followup_root,leg_victim_id,750,1000}}) do
                native_taps[#native_taps+1] = program:install_read_tap(definition[1],definition[1]+31,
                    "post-leg native projectile",function(offset,data,mask)
                        local age=frame-hud_frame-leg_delay
                        local actor=cpu.state.A8.value
                        if hud_frame>0 and age>=definition[3] and age<definition[4] and
                            (actor==program:read_u32(0x01060220) or actor==program:read_u32(0x01060df0)) and
                            program:read_u16(actor+0x1f0)==definition[2] then
                            leg_followups[index]=leg_followups[index]+1
                        end
                    end)
            end
        end
        local win_table = 0xff800000 + 0xfdf00 * 8
        native_taps[#native_taps + 1] = program:install_read_tap(win_table, win_table + 19 * 32 - 1,
            "native winner entry", function(offset, data, mask)
                if (offset - win_table) % 32 == 0 then
                    local id = (offset - win_table) // 32
                    if id == program:read_u16(0x01060280) then
                        native_wins = native_wins + 1
                        last_native_win_frame = frame
                    end
                    if id == program:read_u16(0x01060e50) then
                        last_native_p2_win_frame = frame
                    end
                    if id == roster_ids[p2_fighter] and id >= 17 then
                        native_p2_wins = native_p2_wins + 1
                        if program:read_u16(0x01061b30)==16 and program:read_u16(0x01060280)==13 and
                            program:read_u16(0x010601f0)==0 and program:read_u16(0x01060dc0)==1 and
                            program:read_u16(0x010602f0)==0 and program:read_u16(0x01060ec0)>0 then
                            p2_campaign_boss_win_seen=true
                        end
                    end
                    win_capture = frame + 80
                    print(string.format("MK2KS_NATIVE_WIN frame=%d winner=%04X roster=%04X entry=%08X", frame,
                        id, program:read_u16(0x01060280), offset))
                end
            end)
        if fighter == "kano" or fighter == "sonya" then
            local cpu = manager.machine.devices[":maincpu"]
            local expected = fighter == "kano" and 0x11 or 0x12
            local ladder_source = 0xff800000 + (0xfe600 + expected * 4) * 8
            native_taps[#native_taps + 1] = program:install_read_tap(ladder_source, ladder_source + 31,
                "native custom ladder entry", function(offset, data, mask)
                    if offset == ladder_source then
                        ladder_entries = ladder_entries + 1
                        print(string.format("MK2KS_NATIVE_LADDER frame=%d roster=%04X", frame, program:read_u16(0x01060280)))
                    end
                end)
            local hud_source = 0xff800000 + (0xfdc00 + expected * 8) * 8
            native_taps[#native_taps + 1] = program:install_read_tap(hud_source, hud_source + 31,
                "native custom HUD entry", function(offset, data, mask)
                    if offset == hud_source then
                        native_names = native_names + 1
                        last_native_hud_frame = frame
                        print(string.format("MK2KS_NATIVE_HUD frame=%d roster=%04X entry=%08X", frame,
                            program:read_u16(0x01060280), hud_source))
                    end
                end)
            native_taps[#native_taps + 1] = program:install_read_tap(0x01060280, 0x0106028f,
                "native finish prompt selection", function(offset, data, mask)
                    if cpu.state["PC"].value == 0xff829b40 and program:read_u16(0x010602f0) == 0 then
                        local process = cpu.state["A0"].value
                        finish_tap = program:install_write_tap(process + 0xc0, process + 0xdf,
                            "native finish prompt parameters", function(write_offset, value, write_mask)
                                if write_offset == process + 0xc0 and cpu.state["PC"].value == 0xff829c90 then
                                    if campaign_ended then return end
                                    local sound, message = value & 0xffff, cpu.state["A2"].value
                                    local cpu_id = scheduled_p1_cpu()
                                    local female = cpu_id and (cpu_id == 4 or cpu_id == 5 or cpu_id == 18) or
                                        not cpu_id and fighter == "sonya"
                                    local correct = sound == (female and 0x15 or 0x14) and message == (female and 2 or 1)
                                    if correct then native_finishes = native_finishes + 1 else roster_errors = roster_errors + 1 end
                                    print(string.format("MK2KS_NATIVE_FINISH pass=%s frame=%d sound=%X message=%X", tostring(correct), frame, sound, message))
                                    finish_capture = frame + 45
                                end
                            end)
                    end
                end)
        end
        -- P2's constructor event must be observed independently of P1's
        -- character. A stock P1 does not execute the custom P1 HUD entry.
        -- Preserve the existing two-field, full-health native setup bound.
        if roster_ids[p2_fighter] then
            local p1_hud_table=0xff800000+0xfdc00*8
            native_taps[#native_taps+1]=program:install_read_tap(p1_hud_table,p1_hud_table+19*64-1,
                "P1 native HUD constructor",function(offset)
                    if (offset-p1_hud_table)%64==0 then last_native_hud_frame=frame end
                end)
            local p2_hud_table=0xff800000+0xfdd00*8
            native_taps[#native_taps+1]=program:install_read_tap(p2_hud_table,p2_hud_table+19*64-1,
                "native P2 HUD construction",function(offset,data,mask)
                    if (offset-p2_hud_table)%64~=0 or
                        (offset-p2_hud_table)//64~=program:read_u16(0x01060e50) then return end
                    last_native_p2_hud_frame=frame
                    print(string.format("MK2KS_NATIVE_P2_HUD frame=%d roster=%04X entry=%08X",
                        frame,program:read_u16(0x01060e50),offset))
                end)
        end
        if os.getenv("MK2KS_TRACE_REACTIONS") == "1" or assert_lifecycle then
            local cpu = manager.machine.devices[":maincpu"]
            position_tap = program:install_write_tap(0x01034f40, 0x01034f4f, "P1 vertical position trace",
                function(offset, data, mask)
                    if hud_frame > 0 and frame > hud_frame + 400 and cpu.state["PC"].value == 0xff908000 then
                        object_resets = object_resets + 1
                        local expected_y = program:read_u16(0x0105ecd0) - (fighter == "kano" and 134 or 135)
                        if (data & 0xffff) ~= (expected_y & 0xffff) then ground_errors = ground_errors + 1 end
                        print(string.format("MK2KS_GROUND_RESET frame=%d y=%d expected=%d", frame, data & 0xffff, expected_y))
                    end
                    if hud_frame > 0 and frame > hud_frame + 400 and data ~= last_y and position_writes < 100 then
                        last_y, position_writes = data, position_writes + 1
                        print(string.format("MK2KS_POSITION frame=%d y=%04X PC=%08X A0=%08X A1=%08X A8=%08X return=%08X",
                            frame, data & 0xffff, cpu.state["PC"].value, cpu.state["A0"].value,
                            cpu.state["A1"].value, cpu.state["A8"].value, program:read_u32(cpu.state["SP"].value)))
                    end
                end)
            for _, root in ipairs({0xff000000, 0xff020000, 0xff91fc60}) do
                animation_taps[#animation_taps + 1] = program:install_read_tap(root, root + 0x105f,
                    "reaction animation trace", function(offset, data, mask)
                        if cpu.state["A8"].value == 0x01034e90 and cpu.state["PC"].value == 0xff906140 then
                            local relative = offset - root
                            local kind = relative < 0x840 and "main" or "special"
                            local index = (relative % 0x840) // 32
                            local key = kind .. ":" .. index
                            if key ~= last_animation then
                                if recovery_start and kind == "main" and index == 0 then
                                    local elapsed = frame - recovery_start
                                    recoveries = recoveries + 1
                                    if elapsed > 120 then recovery_errors = recovery_errors + 1 end
                                    print(string.format("MK2KS_RECOVERY_COMPLETE frame=%d elapsed=%d", frame, elapsed))
                                    recovery_start = nil
                                end
                                if kind == "main" and (index == 18 or index == 23) then recovery_start = frame end
                                last_animation = key
                                print(string.format("MK2KS_REACTION frame=%d animation=%s root=%08X xy=%d,%d id=%04X",
                                    frame, key, root, program:read_u16(0x01034f20), program:read_u16(0x01034f40),
                                    program:read_u16(0x01035080)))
                                reaction_task = cpu.state["A13"].value
                                print(string.format("MK2KS_REACTION_CALL task=%08X SP=%08X return=%08X next=%08X",
                                    reaction_task, cpu.state["SP"].value, program:read_u32(cpu.state["SP"].value),
                                    program:read_u32(cpu.state["SP"].value + 32)))
                            end
                        end
                    end)
            end
        end
        if os.getenv("MK2KS_TRACE_HUD_DMA") == "1" then
            dma_tap = program:install_write_tap(0x01a80000, 0x01a800ff, "HUD image probe", function(offset, data, mask)
                local reg = (offset - 0x01a80000) // 16
                dma_regs[reg] = ((dma_regs[reg] or 0) & (~mask)) | (data & mask)
                if reg == 1 and (data & 0x8000) ~= 0 then
                    local x, y, w, h = dma_regs[4] or 0, dma_regs[5] or 0, dma_regs[6] or 0, dma_regs[7] or 0
                    local is_name = exit_frame > 0 and frame > exit_frame + 200 and x < 110 and y % 256 < 45 and h <= 16
                    local is_pose = css_frame > 0 and exit_frame == 0 and x < 160 and y % 256 >= 98 and h > 20
                    if is_name or is_pose then
                        local source = (dma_regs[2] or 0) | ((dma_regs[3] or 0) << 16)
                        local key = string.format("%08X:%d:%d:%d:%d:%04X", source, x, y, w, h, data)
                        if not dma_seen[key] then
                            dma_seen[key] = true
                            print(string.format("HUD_DMA frame=%d source=%08X xy=%d,%d wh=%d,%d command=%04X palette=%04X pc=%08X",
                                frame, source, x, y, w, h, data, dma_regs[8] or 0, manager.machine.devices[":maincpu"].state["PC"].value))
                            if is_name and (source == 0x04122e42 or source == 0x0412b7e0) then
                                local palette = {}
                                for pen = 0, 15 do palette[#palette + 1] = string.format("%d=%06X", pen,
                                    screen.palette:pen_color(((dma_regs[8] or 0) & 0x7f00) + pen) & 0xffffff) end
                                print("HUD_NAME_PALETTE " .. table.concat(palette, " "))
                            end
                        end
                    end
                end
            end)
        end
    end

    for _, field in pairs(fields) do field:clear_value() end
    if frame >= 300 and frame < 304 then fields.hp:set_value(1) end
    pixels, width = screen:pixels()
    if width ~= 400 or #pixels < 400 * 254 * 4 then return end
    if win_capture == frame then snap("native_win"); win_capture = nil end
    if finish_capture == frame then snap("native_finish"); finish_capture = nil end

    if css_frame == 0 and frame >= boot_frame then
        local age = (frame - boot_frame) % 300
        pulse("coin", age, 0)
        if two_player then pulse("coin2", age, 8) end
        pulse("start", age, 20)
    end

    local yellow, early = header()
    local is_css = yellow >= 400 and yellow <= 430 and early >= 10
    if css_frame == 0 and frame > 700 and is_css then
        css_frame = frame
        print(string.format("MK2KS_EXIT css=%d fighter=%s confirm=%s yellow=%d early=%d",
            frame, fighter, confirm, yellow, early))
    end
    if frame % 300 == 0 then
        local p1actor = program:read_u32(0x01060220)
        local p1id = p1actor >= 0x01000000 and p1actor < 0x01100000 and
            program:read_u16(p1actor + 0x1f0) or 0xffff
        print(string.format("MK2KS_EXIT state frame=%d yellow=%d early=%d hud=%s id=%04X roster_id=%04X",
            frame, yellow, early, tostring(hud()), p1id, program:read_u16(0x01060280)))
        if round_win or round_loss then
            print(string.format("MK2KS_ROUND_INPUT x1=%d x2=%d health1=%d health2=%d",
                live_fighter_x(0x01060220) or -1, live_fighter_x(0x01060df0) or -1,
                program:read_u16(0x010602f0), program:read_u16(0x01060ec0)))
        end
        if reaction_task then
            local values = {}
            for delta = 0, 0x400, 0x20 do
                values[#values + 1] = string.format("%X=%08X", delta, program:read_u32(reaction_task + delta))
            end
            print("MK2KS_REACTION_TASK " .. table.concat(values, " "))
        end
    end

    if css_frame > 0 then
        local age = frame - css_frame
        if age == 8 then remember_portraits(); snap("css_initial") end
        if two_player then
            -- Default pricing requires two coins per player, not two total.
            pulse("coin", age, 0)
            pulse("coin2", age, 8)
            pulse("start2", age, 20)
        end
        for index,direction in ipairs(selection_routes[1][fighter] or {}) do
            pulse(direction,age,12+(index-1)*12)
        end
        if age == 65 then
            snap("highlight")
            if two_player then
                local red = 0
                for y = 20, 23 do
                    for x = 259, 317 do
                        local r, g, b = rgb(x, y)
                        if r > 80 and r > g * 2 and r > b * 2 then red = red + 1 end
                    end
                end
                print(string.format("MK2KS_P2_CURSOR red=%d", red))
            end
        end
        if age == 81 then snap("highlight_blink") end
        if os.getenv("MK2KS_TRACE_CURSOR_BLINK") == "1" and
            age >= 65 and age < 96 and (age - 65) % 4 == 0 then
            snap("cursor_trace")
        end
        if os.getenv("MK2KS_TRACE_CURSOR_LONG") == "1" and age >= 65 and age <= 253 and
            (age - 65) % 80 < 32 and (age - 65) % 4 == 0 then
            snap("cursor_trace_long")
        end
        if age >= 65 and hud_frame == 0 and (fighter == "kano" or fighter == "sonya") then
            selection_checks = selection_checks + 1
            if program:read_u16(0x01060280) ~= (fighter == "kano" and 17 or 18) then
                selection_errors = selection_errors + 1
            end
        end
        if confirm ~= "timeout" then pulse(confirm, age, confirm_at_age, hold) end
        if two_player then
            for index,direction in ipairs(selection_routes[2][p2_fighter] or {}) do
                pulse("p2"..direction,age,132+(index-1)*16)
            end
            if age == 204 and p2_fighter ~= "stock" then snap("p2_highlight") end
            pulse("p2hp", age, 220)
        end
        if exit_frame == 0 and age > 96 and not is_css then
            exit_frame = frame
            print(string.format("MK2KS_EXIT non_css=%d yellow=%d early=%d", frame, yellow, early))
        end
        if exit_frame > 0 and frame < exit_frame + 12 then snap("transition") end
        if exit_frame > 0 and not is_css and reference_count > 0 then
            outside_frames = outside_frames + 1
            local matches = portrait_matches()
            if matches > (reference_count / 2) * 0.85 then
                leaks = leaks + 1
                if leaks <= 3 then snap("LEAK") end
            end
        end
    -- A long one-player run can return to attract mode after GAME OVER.
    -- Attract fights use stock IDs and must not be graded as the selected
    -- campaign. Require both a prior ladder advance and a roster change so
    -- an unexpected reset of a still-live native fighter remains visible.
    if not two_player and exit_frame > 0 and hud_frame > 0 and
        (fighter == "kano" or fighter == "sonya") and not campaign_ended then
        local stage = program:read_u16(0x01061b30)
        if stage > campaign_high_stage and stage <= 16 then campaign_high_stage = stage end
        -- A timeout defeat can go straight to MKII's GAME OVER scene rather
        -- than the HP-zero continue state. Once both combat objects have
        -- retired, the old roster words/HUD no longer describe a live fight.
        local game_over_scene = stage < 16 and combat_frames > 1000 and
            program:read_u16(0x010601d0) == 11 and
            program:read_u32(0x01060220) == 0 and
            program:read_u32(0x01060df0) == 0
        if program:read_u16(0x010601d0) == 3 and
            program:read_u16(0x010601f0) == 2 and
            program:read_u16(0x01061b00) == 2 and
            program:read_u16(0x010602f0) == 0 then campaign_lost = true end
        -- Winning the final boss returns MKII to its stock attract sequence
        -- without resetting the retained ladder-stage word. Once the native
        -- winner tap has fired, the ending scene has run, and P1 changes to
        -- a stock attract fighter, stop grading the old selected identity.
        -- A lost boss fight cannot satisfy the native-win condition.
        local completed_ending = stage == 16 and not campaign_lost and
            native_wins > 0 and frame - last_native_win_frame > 1200 and
            program:read_u16(0x010601d0) == 11 and
            program:read_u16(0x01060280) ~= roster_ids[fighter]
        if allow_continue_reselect and campaign_lost and
            program:read_u16(0x010601d0) == 4 and
            program:read_u16(0x010601f0) == 3 then
            campaign_ended = true
            print(string.format("MK2KS_CAMPAIGN_CONTINUED frame=%d stage=%d", frame, stage))
        elseif completed_ending then
            campaign_completed = true
            campaign_ended = true
            print(string.format("MK2KS_CAMPAIGN_COMPLETED frame=%d high_stage=%d roster=%d",
                frame, campaign_high_stage, program:read_u16(0x01060280)))
        elseif game_over_scene then
            campaign_lost = true
            campaign_ended = true
            print(string.format("MK2KS_CAMPAIGN_GAME_OVER frame=%d stage=%d", frame, stage))
        elseif stage == 0 and campaign_high_stage > 0 and
            program:read_u16(0x01060280) ~= roster_ids[fighter] then
            campaign_ended = true
            if not campaign_lost then unexpected_campaign_resets = unexpected_campaign_resets + 1 end
            print(string.format("MK2KS_CAMPAIGN_ENDED frame=%d high_stage=%d roster=%d lost=%s unexpected_reset=%s",
                frame, campaign_high_stage, program:read_u16(0x01060280),
                tostring(campaign_lost), tostring(not campaign_lost)))
        end
    end
    -- A P2-human campaign can end naturally after the scheduled P1 CPU wins.
    -- Only stop checking the old campaign once the native GAME OVER scene
    -- has retired both actors and both human participation states are zero.
    -- An absent actor or changed identity during live combat still fails.
    local losing_cpu=not p2_campaign_loss_seen and p1_cpu_schedule_checks>500 and scheduled_p1_cpu(true)
    if losing_cpu and program:read_u16(0x01060dc0)==2 then
        local a1,a2=program:read_u32(0x01060220),program:read_u32(0x01060df0)
        if a1>=0x01000000 and a1<0x01100000 and a2>=0x01000000 and a2<0x01100000 and
            program:read_u16(a1+0x1f0)==losing_cpu and program:read_u16(a2+0x1f0)==roster_ids[p2_fighter] then
            p2_campaign_loss_seen=true
            print(string.format("MK2KS_P2_CAMPAIGN_CONTINUE frame=%d cpu=%d human=%d",frame,losing_cpu,roster_ids[p2_fighter]))
        end
    end
    if two_player and not campaign_ended and p2_campaign_loss_seen and program:read_u16(0x010601d0)==11 and
        program:read_u16(0x010601f0)==0 and program:read_u16(0x01060dc0)==0 and
        program:read_u16(0x01061b00)==1 and program:read_u16(0x01060ec0)==0 and
        program:read_u32(0x01060220)==0 and program:read_u32(0x01060df0)==0 then
        campaign_ended,campaign_lost=true,true
        print(string.format("MK2KS_P2_CAMPAIGN_GAME_OVER frame=%d stage=%d checks=%d",
            frame,program:read_u16(0x01061b30),p1_cpu_schedule_checks))
    end
    -- The full P2 ending owns retired combat objects, just like P1's ending.
    -- Require a real scheduled boss victory and the exact retained win state.
    local p2_ending_retired=two_player and p2_campaign_boss_win_seen and not p2_campaign_loss_seen and
        program:read_u16(0x01061b30)==16 and program:read_u16(0x010601d0)==11 and
        program:read_u16(0x010601f0)==0 and program:read_u16(0x01060dc0)==0 and
        program:read_u16(0x01061b00)==2 and program:read_u16(0x010602f0)==0 and
        program:read_u16(0x01060ec0)>0 and program:read_u16(0x01060e50)==roster_ids[p2_fighter] and
        program:read_u16(0x01060280)==13
    if two_player and not campaign_ended and p2_campaign_boss_win_seen and not p2_campaign_loss_seen and
        program:read_u16(0x01061b30)==16 and frame-last_native_p2_win_frame>1200 and
        program:read_u16(0x010601d0)==11 and program:read_u16(0x01060e50)~=roster_ids[p2_fighter] then
        campaign_ended,campaign_completed=true,true
        print(string.format("MK2KS_P2_CAMPAIGN_COMPLETED frame=%d roster=%d",frame,program:read_u16(0x01060e50)))
    end
    local is_hud = exit_frame > 0 and not is_css and not campaign_ended and not p2_ending_retired and hud()
        if is_hud then
            combat_frames = combat_frames + 1
            local p1_cpu_expected, p1_cpu_stage, p1_cpu_order = scheduled_p1_cpu(p2_campaign_loss_seen)
            if p1_cpu_expected then
                if p2_previous_stage and p1_cpu_stage~=p2_previous_stage and p2_pending_stage~=p1_cpu_stage then
                    p2_stage_change_frame=frame
                    p2_pending_stage=p1_cpu_stage
                end
                local prior_cpu=program:read_u16(0x01060280)
                -- Mode 10 advances the stage before retiring the PREVIOUS CPU.
                -- Its old HUD survives up to three fields, including actor
                -- retirement. Latch once; never renew this bounded interval.
                if frame-p2_stage_change_frame<=3 and program:read_u16(0x010601d0)==10 and
                    program:read_u16(0x01061b00)==2 and frame-last_native_p2_win_frame<=600 and
                    p2_previous_cpu==prior_cpu and p2_previous_stage and
                    (p1_cpu_stage==p2_previous_stage+1 or p1_cpu_stage==p2_previous_stage+2 and
                     program:read_u16(program:read_u32(0x01061b10)+(p2_previous_stage+1)*16)==14) then
                    p1_cpu_expected=prior_cpu
                else
                    p2_previous_stage,p2_previous_cpu=p1_cpu_stage,p1_cpu_expected
                    p2_pending_stage=nil
                end
            end
            if p1_cpu_expected then
                p1_cpu_schedule_checks = p1_cpu_schedule_checks + 1
                if p1_cpu_schedule_checks == 1 then
                    print(string.format("MK2KS_P1_CPU_RESUME frame=%d stage=%d order=%d expected=%04X roster=%04X states=0,1",
                        frame,p1_cpu_stage,p1_cpu_order,p1_cpu_expected,program:read_u16(0x01060280)))
                end
            end
            -- After a two-human fatality MKII retires both actors while the
            -- winning pose/HUD fades into the ladder. This mode-3 interval is
            -- longer than an ordinary win; bound it to a real native winner
            -- read and require both retired pointers and zero loser health.
            local two_player_finish_teardown = two_player and
                frame - last_native_win_frame <= 600 and
                program:read_u16(0x010601d0) == 3 and
                program:read_u16(0x010601f0) == 1 and
                program:read_u16(0x01060dc0) == 2 and
                program:read_u16(0x01061b00) == 1 and
                program:read_u16(0x01060ec0) == 0 and
                program:read_u32(0x01060220) == 0 and
                program:read_u32(0x01060df0) == 0
            -- An ordinary two-human match win has a different mode-3
            -- teardown: the winner is P2, both actor pointers are retired,
            -- but the round's health values and old HUD are still visible.
            -- Require a recent native winner-table read and the exact
            -- match-over state so active-fight actor loss remains a failure.
            local two_player_match_teardown = two_player and
                frame - last_native_p2_win_frame <= 600 and
                program:read_u16(0x010601d0) == 3 and
                program:read_u16(0x010601f0) == 2 and
                program:read_u16(0x01060dc0) == 1 and
                program:read_u16(0x01061b00) == 2 and
                program:read_u16(0x010602f0) > 0 and
                program:read_u16(0x01060ec0) > 0 and
                program:read_u32(0x01060220) == 0 and
                program:read_u32(0x01060df0) == 0
            -- P2 keeps its native slot while the defeated P1 CPU is replaced
            -- from the next schedule entry. The ladder owns this mode-7 HUD,
            -- not two missing combat actors. Keep the new CPU roster check.
            local p2_stage_teardown=program:read_u16(0x010601d0)==10 and
                p2_pending_stage==p1_cpu_stage and frame-p2_stage_change_frame<=3 and
                program:read_u16(0x01060280)==p2_previous_cpu
            local p2_campaign_between_fights = p1_cpu_expected ~= nil and
                frame-last_native_p2_win_frame <= 600 and (program:read_u16(0x010601d0)==7 or p2_stage_teardown) and
                program:read_u16(0x01061b00)==2 and
                program:read_u16(0x01060ec0)>0 and program:read_u32(0x01060220)==0 and
                program:read_u32(0x01060df0)==0
            -- The opposite exact continue state follows a scheduled CPU win.
            -- It must have been observed with both real actors before their
            -- retirement; this does not excuse missing actors in combat.
            local p2_campaign_continue_teardown = p1_cpu_expected ~= nil and p2_campaign_loss_seen and
                program:read_u16(0x010601d0)==3 and program:read_u16(0x01061b00)==1 and
                program:read_u16(0x01060dc0)==2 and program:read_u16(0x01060ec0)==0 and
                program:read_u16(0x010602f0)>0 and program:read_u32(0x01060220)==0 and
                program:read_u32(0x01060df0)==0
            if assert_hud_shadow and hud_frame > 0 and frame >= hud_frame + 150 and
                frame <= hud_frame + 600 and frame % 60 == 0 then check_hud_shadows() end
            if roster_ids[p2_fighter] then
                local expected = roster_ids[p2_fighter]
                local object = program:read_u32(0x01060df0)
				-- After P2's match loss/continue expires, P1 resumes the native
				-- single-player ladder. Validate the CPU against the actual chosen
				-- schedule, rather than retaining the departed human's character.
				local mode = program:read_u16(0x010601d0)
				-- A normally scheduled CPU can win after the departed human's
				-- continue expires. This exact native winner/health state still
				-- owns the scheduled CPU, not the old human opponent's ID.
				local resumed_cpu_win = mode == 5 and frame - last_native_p2_win_frame <= 600 and
					program:read_u16(0x01061b00) == 2 and
					program:read_u16(0x010602f0) == 0 and program:read_u16(0x01060ec0) > 0
				-- The same scheduled CPU can also lose a round to P1. Require
				-- the actual recent native P1 winner read and opposite exact
				-- health flags; the departed human's ID is not restored here.
				local resumed_cpu_loss = mode == 5 and frame - last_native_win_frame <= 600 and
					program:read_u16(0x01061b00) == 1 and
					program:read_u16(0x010602f0) > 0 and program:read_u16(0x01060ec0) == 0
				local resumed_cpu_constructing = mode==6 and object==0 and
					frame<=last_native_p2_hud_frame+2 and program:read_u16(0x01061b00)==0 and
					program:read_u16(0x010602f0)==161 and program:read_u16(0x01060ec0)==161
				local scheduled_cpu_valid=false
				if two_player and p2_joined and (mode == 2 or mode == 7 or resumed_cpu_win or resumed_cpu_loss or resumed_cpu_constructing) and
					program:read_u16(0x010601f0) == 1 and program:read_u16(0x01060dc0) == 0 then
					local table = program:read_u32(0xff8a11f0)
					local schedule = program:read_u32(0x01061b10)
					local stage = program:read_u16(0x01061b30)
					local valid = false
					if table == 0xfffa2c00 and stage <= 16 then
						for order = 0, 5 do
							valid = valid or program:read_u32(table + order * 32) == schedule
						end
					end
					if valid then
						scheduled_cpu_valid=true
						expected = program:read_u16(schedule + stage * 16)
						p2_cpu_schedule_checks = p2_cpu_schedule_checks + 1
						if resumed_cpu_win then
							p2_cpu_win_checks = p2_cpu_win_checks + 1
							if p2_cpu_win_checks == 1 then
								print(string.format("MK2KS_P2_CPU_WIN frame=%d stage=%d expected=%04X roster=%04X object=%08X",
									frame,stage,expected,program:read_u16(0x01060e50),object))
								manager.machine.screens[":screen"]:snapshot("resumed_cpu_winner.png")
							end
						end
						if resumed_cpu_loss then
							p2_cpu_loss_checks=p2_cpu_loss_checks+1
							if p2_cpu_loss_checks==1 then
								print(string.format("MK2KS_P2_CPU_LOSS frame=%d stage=%d expected=%04X roster=%04X object=%08X",
									frame,stage,expected,program:read_u16(0x01060e50),object))
								manager.machine.screens[":screen"]:snapshot("resumed_cpu_defeat.png")
							end
						end
						if p2_cpu_schedule_checks == 1 then
							print(string.format("MK2KS_P2_CPU_RESUME frame=%d stage=%d expected=%04X roster=%04X mode=%d state=0",
								frame,stage,expected,program:read_u16(0x01060e50),mode))
						end
					end
				end
                local constructing = (object == 0 and frame <= last_native_p2_hud_frame + 2 and
                    program:read_u16(0x010601d0) == 6 and program:read_u16(0x01060dc0) == 1 and
                    program:read_u16(0x01061b00) == 0 and program:read_u16(0x010602f0) == 161 and
                    program:read_u16(0x01060ec0) == 161) or
                    (resumed_cpu_constructing and scheduled_cpu_valid)
                -- The match-over scene retains the old HUD and roster word
                -- after retiring the P2 actor. Keep checking the roster ID,
                -- but do not treat that explicitly released object as a swap.
                local released = object == 0 and program:read_u16(0x010601d0) == 3 and
                    program:read_u16(0x01060dc0) == 1 and program:read_u16(0x01061b00) == 2 and
                    program:read_u16(0x010602f0) == 0
                if constructing then
                    print(string.format("MK2KS_P2_CONSTRUCTING frame=%d hud_read=%d mode=6 health=161,161",frame,last_native_p2_hud_frame))
                end
                if program:read_u16(0x01060e50) ~= expected or (not constructing and not released and
                    not two_player_finish_teardown and not two_player_match_teardown and
                    not p2_campaign_between_fights and not p2_campaign_continue_teardown and
                    (object < 0x01000000 or object >= 0x010fffff or program:read_u16(object + 0x1f0) ~= expected)) then
                    p2_identity_errors = p2_identity_errors + 1
                    if p2_identity_errors <= 3 then
                        print(string.format("MK2KS_P2_ID_ERROR frame=%d object=%08X roster=%04X mode=%d state=%d health=%d,%d",
                            frame,object,program:read_u16(0x01060e50),program:read_u16(0x010601d0),
                            program:read_u16(0x01060dc0),program:read_u16(0x010602f0),program:read_u16(0x01060ec0)))
                    end
                end
            end
            -- Continue/round-over screens can deliberately hold an unchanged
            -- image for seconds while keeping old HUD pixels visible. Count
            -- a visual stall only while both live fighters can still fight.
            local live_p1, live_p2 = program:read_u32(0x01060220), program:read_u32(0x01060df0)
            -- Native mode 2 is single-player combat; mode 6 is two-player.
            -- Check both so the visual-stall assertion covers CPU matches too.
            local mode = program:read_u16(0x010601d0)
            local active_combat = (mode == 2 or mode == 6) and
                live_p1 >= 0x01000000 and live_p1 < 0x01100000 and
                live_p2 >= 0x01000000 and live_p2 < 0x01100000 and
                program:read_u16(0x010602f0) > 0 and program:read_u16(0x01060ec0) > 0
            unchanged_frames = active_combat and pixels == previous_pixels and unchanged_frames + 1 or 0
            if unchanged_frames > 180 then stalled_frames = stalled_frames + 1 end
            local pc = manager.machine.devices[":maincpu"].state["PC"].value
            if pc == 0xffa1e800 or pc == 0xffa1e880 then trap_frames = trap_frames + 1 end
            previous_pixels = pixels
            if hud_frame == 0 then hud_frame = frame; snap("first_hud") end
            if fighter == "kano" or fighter == "sonya" then
                local expected = p1_cpu_expected or (fighter == "kano" and 0x11 or 0x12)
                if program:read_u16(0x01060280) ~= expected then
                    roster_errors = roster_errors + 1
                    if roster_errors <= 3 then
                        print(string.format("MK2KS_ROSTER_ERROR frame=%d mode=%d state=%d roster=%04X hp=%d,%d campaign_lost=%s",
                            frame, program:read_u16(0x010601d0), program:read_u16(0x010601f0),
                            program:read_u16(0x01060280), program:read_u16(0x010602f0),
                            program:read_u16(0x01060ec0), tostring(campaign_lost)))
                        snap("ROSTER_ERROR")
                    end
                end
            end
            if two_player and not p2_joined and frame >= hud_frame + 120 then
                local yellow = 0
                for y = 9, 24 do
                    for x = 300, 389 do
                        local r, g, b = rgb(x, y)
                        if r > 175 and g > 140 and b < 100 then yellow = yellow + 1 end
                    end
                end
                -- A live P2 has the yellow win counter. A CPU opponent has
                -- cream PUSH START lettering, which must not pass this check.
                p2_joined = yellow > 40
                if p2_joined then print(string.format("MK2KS_P2_JOINED pass=true win_counter_yellow=%d", yellow)) end
            end
            if frame > hud_frame + 120 and (fighter == "kano" or fighter == "sonya") then
                local expected = p1_cpu_expected or (fighter == "kano" and 0x11 or 0x12)
                local actor = program:read_u32(0x01060220)
                local ladder_stage=program:read_u16(0x01061b30)
                if ladder_stage~=last_hud_stage then
                    last_hud_stage=ladder_stage
                    stage_change_frame=frame
                end
                -- On CONTINUE, MKII clears its live P1 pointer and reuses the
                -- old object allocation for text before the old HUD fades.
                -- That is not a character change. Never pin or inspect the
                -- freed object's ID; require the native loss/continue state.
                local released = actor == 0 and program:read_u16(0x010601d0) == 3 and
                    program:read_u16(0x010601f0) == 2 and program:read_u16(0x01061b00) == 2 and
                    program:read_u16(0x010602f0) == 0
                if released then released_actor_fields = released_actor_fields + 1 end
                -- MKII also retires the actor while the winner pose and HUD
                -- remain on screen. On a P2 timeout win the loser can retain
                -- nonzero health, so the zero-health CONTINUE test above does
                -- not apply. Require a recent native winner read and the
                -- exact mode-3 loss state; a missing actor in combat fails.
                local victory_teardown = actor == 0 and
                    (frame - last_native_win_frame <= 300 or
                     frame - last_native_p2_win_frame <= 300) and
                    program:read_u16(0x010601d0) == 3 and
                    program:read_u16(0x010601f0) == 2 and
                    program:read_u16(0x01061b00) == 2 and
                    program:read_u16(0x01060280) == expected
                -- The victory/ladder and game-over transitions can retain HUD
                -- pixels after MKII has retired the fight objects. Neither is
                -- an active-fight identity failure; mode 6 still must publish
                -- the expected actor except for the two-field constructor gap.
                local between_fights = actor == 0 and program:read_u16(0x010601d0) == 7 and
                    program:read_u16(0x010601f0) == 1 and program:read_u16(0x01061b00) == 1 and
                    program:read_u16(0x01060ec0) == 0
                local game_over = actor == 0 and program:read_u16(0x010601d0) == 1 and
                    program:read_u16(0x010601f0) == 0 and program:read_u16(0x01061b00) == 2 and
                    program:read_u16(0x010602f0) == 0
                local post_boss = actor == 0 and program:read_u16(0x010601d0) == 11 and
                    program:read_u16(0x01061b00) == 1 and program:read_u16(0x01061b30) == 16 and
                    program:read_u16(0x01060ec0) == 0
                -- On a ladder advance, MKII updates the stage before publishing
                -- the next P1 object. The old HUD remains for at most three
                -- fields in mode 7 or 10 (the latter is used after some
                -- later opponents); a missing actor after that still fails.
                local stage_transition = actor == 0 and ladder_stage<=16 and
                    frame-stage_change_frame<=3 and
                    (program:read_u16(0x010601d0) == 7 or
                     program:read_u16(0x010601d0) == 10) and
                    program:read_u16(0x010601f0) == 1 and
                    program:read_u16(0x01061b00) == 1 and
                    program:read_u16(0x01060280) == expected
                if stage_transition then transition_actor_fields=transition_actor_fields+1 end
                -- The next-round HUD is constructed one field before MKII
                -- publishes its new P1 object. Bound this setup allowance to
                -- two fields after the actual native HUD-table read, not an
                -- arbitrary grace period that could conceal a lost actor.
                local constructing = actor == 0 and frame <= last_native_hud_frame + 2 and
                    program:read_u16(0x010601d0) == 6 and
                    (program:read_u16(0x010601f0) == 1 or p1_cpu_expected ~= nil) and
                    program:read_u16(0x01061b00) == 0 and program:read_u16(0x010602f0) == 161 and
                    program:read_u16(0x01060ec0) == 161
                if constructing then constructing_actor_fields = constructing_actor_fields + 1 end
                local valid_actor = actor >= 0x01000000 and actor < 0x010fffff
                if not released and not victory_teardown and not two_player_finish_teardown and
                    not two_player_match_teardown and
                    not p2_campaign_between_fights and not p2_campaign_continue_teardown and
                    not between_fights and not game_over and not post_boss and
                    not stage_transition and not constructing and
                    (not valid_actor or program:read_u16(actor + 0x1f0) ~= expected and
                     not (p2_shang and p2_shang.allowed(actor,expected))) then
                    identity_errors = identity_errors + 1
                    if identity_errors <= 3 then
                        print(string.format("MK2KS_ID_ERROR frame=%d id=%04X mode=%04X p1state=%04X winner=%04X p1object=%08X health=%d,%d", frame,
                            valid_actor and program:read_u16(actor + 0x1f0) or 0xffff,
                            program:read_u16(0x010601d0), program:read_u16(0x010601f0),
                            program:read_u16(0x01061b00), program:read_u32(0x01060220),
                            program:read_u16(0x010602f0), program:read_u16(0x01060ec0)))
                        snap("ID_ERROR")
                    end
                end
                -- After native actor release the continue-screen shutters wipe
                -- the old HUD from its edges. Do not require an unclipped name
                -- on that deliberately disappearing scene.
                if frame % 60 == 0 and not released and not victory_teardown and
                    not two_player_finish_teardown and not two_player_match_teardown and
                    not p2_campaign_between_fights and not p2_campaign_continue_teardown and
                    not between_fights and not game_over and not post_boss and
                    not stage_transition and
                    not constructing then
                    if p1_cpu_expected then
                        -- Added CPUs retain their own native HUD masks. Stock
                        -- names are covered by their native table, not either
                        -- custom mask belonging to a departed human player.
                        if p1_cpu_expected == 17 or p1_cpu_expected == 18 then
                            check_name(p1_cpu_expected == 17 and "kano" or "sonya")
                        end
                    else check_name() end
                end
                if valid_actor then
                    local y, floor_y = program:read_u16(actor + 0xb0), program:read_u16(0x0105ecd0)
                    if y >= 0x8000 then y = y - 0x10000 end
                    if floor_y >= 0x8000 then floor_y = floor_y - 0x10000 end
                    if y > floor_y + 8 or y < floor_y - 500 then position_errors = position_errors + 1 end
                end
            end
        end
        if hud_frame > 0 and (round_win or round_loss) then
            local age = frame - hud_frame
            local p1x, p2x = live_fighter_x(0x01060220), live_fighter_x(0x01060df0)
            if age >= 180 and is_hud and p1x and p2x then
                local prefix = round_win and "" or "p2"
                local stage = program:read_u16(0x01061b30)
                local strategy = round_win_late_strategy ~= "" and stage >= round_win_late_stage and
                    round_win_late_strategy or round_win_strategy
                local reach = strategy == "projectile_zone" and 125 or
                    (strategy == "guard_uppercut" or strategy == "sweep_lk") and 100 or
                    strategy == "standing_hk" and 120 or
                    strategy == "rapid_uppercut" and 75 or 85
                if math.abs(p1x - p2x) > reach then
                    if round_win and strategy == "projectile_zone" then
                        local phase = age % 55
                        local backward = p1x < p2x and "left" or "right"
                        pulse("down", phase, 0, 3)
                        if fighter == "sonya" then
                            pulse(backward == "left" and "right" or "left", phase, 5, 3)
                            pulse("lp", phase, 6, 3)
                        else
                            pulse(backward, phase, 5, 3)
                            pulse("hp", phase, 6, 3)
                        end
                    else
                        local move_right = round_win and p1x < p2x or round_loss and p2x < p1x
                        fields[prefix .. (move_right and "right" or "left")]:set_value(1)
                    end
                else
                    if round_win and strategy == "standing_hk" then
                        pulse(prefix .. "hk", age % 24, 0, 4)
                    elseif round_win and strategy == "sweep_lk" then
                        fields[prefix .. "down"]:set_value(1)
                        pulse(prefix .. "lk", age % 25, 0, 4)
                    elseif round_win and strategy == "rapid_uppercut" then
                        fields[prefix .. "down"]:set_value(1)
                        pulse(prefix .. "hp", age % 22, 0, 4)
                    elseif round_win and strategy == "guard_uppercut" then
                        fields[prefix .. "down"]:set_value(1)
                        local phase = age % 34
                        if phase < 4 then fields[prefix .. "hp"]:set_value(1)
                        else fields[prefix .. "block"]:set_value(1) end
                    elseif round_win and strategy == "projectile_zone" then
                        fields[prefix .. "down"]:set_value(1)
                        local stage = program:read_u16(0x01061b30)
                        local close = projectile_late_close ~= "" and stage >= projectile_late_stage and
                            projectile_late_close or projectile_close
                        if close == "guard" and stage >= 1 then
                            local phase = age % 34
                            if phase < 4 then fields[prefix .. "hp"]:set_value(1)
                            else fields[prefix .. "block"]:set_value(1) end
                        elseif close == "sweep" and stage >= 1 then
                            pulse(prefix .. "lk", age % 25, 0, 4)
                        else
                            pulse(prefix .. "hp", age % 42, 0, 4)
                        end
                    else
                        fields[prefix .. "down"]:set_value(1)
                        pulse(prefix .. "hp", age % 50, 0, 4)
                    end
                end
            end
        end
        if test_projectiles and hud_frame > 0 and is_hud then
            local age = frame - hud_frame
            if age >= 180 and age < 1500 then
                local phase = (age - 180) % 360
                local p1x, p2x = program:read_u16(0x01034f20), program:read_u16(0x01035130)
                for side, first in ipairs({0, 180}) do
                    local prefix = side == 1 and "" or "p2"
                    local right = side == 1 and p1x < p2x or side == 2 and p2x < p1x
                    local name = side == 1 and fighter or p2_fighter
                    local forward = prefix .. (right and "right" or "left")
                    local backward = prefix .. (right and "left" or "right")
                    local direction = name == "kano" and backward or forward
                    local button = prefix .. (name == "kano" and "hp" or "lp")
                    if projectile_command == "legacy" then
                        pulse(forward, phase, first, 3)
                        pulse(forward, phase, first + 5, 3)
                        pulse(button, phase, first + 6, 3)
                    elseif projectile_command == "chord" then
                        pulse(prefix .. "block", phase, first + 6, 4)
                        pulse(button, phase, first + 6, 4)
                    elseif projectile_command == "reversed" then
                        pulse(direction, phase, first, 3)
                        pulse(prefix .. "down", phase, first + 5, 3)
                        pulse(button, phase, first + 6, 3)
                    else
                        local delay = projectile_command == "expired" and 50 or 5
                        if projectile_command == "airborne" then
                            pulse(prefix .. "up", phase, first, 3)
                            first = first + 6
                        end
                        pulse(prefix .. "down", phase, first, 3)
                        pulse(direction, phase, first + delay, 3)
                        if projectile_command == "wrong_button" then
                            button = prefix .. (name == "kano" and "lp" or "hp")
                        end
                        pulse(button, phase, first + delay + 1, 3)
                        if projectile_command == "with_block" then
                            pulse(prefix .. "block", phase, first + delay + 1, 3)
                        end
                    end
                end
                if projectile_command == "native" and age < 600 and age % 4 == 0 then snap("projectile") end
            end
        end
        if square_test ~= "" and hud_frame > 0 and is_hud then
            local age = frame - hud_frame
            local side = fighter == "sonya" and 1 or 2
            local prefix = side == 1 and "" or "p2"
            local opponent = side == 1 and "p2" or ""
            local p1x, p2x = program:read_u16(0x01034f20), program:read_u16(0x01035130)
            local right = side == 1 and p1x < p2x or side == 2 and p2x < p1x
            local forward, back = prefix .. (right and "right" or "left"), prefix .. (right and "left" or "right")
            if square_test == "block" then pulse(opponent .. "block", age, 160, 120) end
            if square_test == "air" or square_test == "air_block" then
                pulse(opponent .. "up", age, 193, 3)
                if square_test == "air_block" then pulse(opponent .. "block", age, 198, 82) end
            end
            if square_test == "far" then
                pulse(opponent .. (right and "right" or "left"), age, 140, 40)
            end
            local delay = square_test == "expired" and 50 or 5
            if square_test == "airborne" then pulse(prefix .. "up", age, 172, 3) end
            pulse(square_test == "reversed" and back or forward, age, 180, 3)
            pulse(square_test == "reversed" and forward or back, age, 180 + delay, 3)
            pulse(prefix .. (square_test == "wrong_button" and "lp" or "hp"), age, 181 + delay, 3)
            if square_test == "with_block" then pulse(prefix .. "block", age, 181 + delay, 3) end
            -- A subsequent native ring command proves the square routine has
            -- returned to action-ready, not just stopped moving on the floor.
            pulse(prefix .. "down", age, 320, 3)
            pulse(forward, age, 325, 3)
            pulse(prefix .. "lp", age, 326, 3)
            if age == 160 or (age >= 176 and age <= 330) then
                local obj = program:read_u32(side == 1 and 0x01060220 or 0x01060df0)
                if age >= 176 then square_trace_fields = square_trace_fields + 1 end
                local y = program:read_u16(obj + 0xb0)
                if y >= 0x8000 then y = y - 0x10000 end
                local sample = {x=program:read_u16(obj + 0x90), y=y,
                    vx=program:read_u32(obj + 0x40), vy=program:read_u32(obj + 0x60),
                    gravity=program:read_u32(obj + 0x20),
                    health={program:read_u16(0x010602f0),program:read_u16(0x01060ec0)}}
                square_samples[age] = sample
                if age == 160 then square_baseline = sample end
                if square_trace then
                    print(string.format("MK2KS_SQUARE_STATE frame=%d age=%d side=%d x=%d y=%d vx=%08X vy=%08X gravity=%08X health=%d,%d",
                        frame, age, side, sample.x, sample.y, sample.vx, sample.vy, sample.gravity,
                        sample.health[1], sample.health[2]))
                end
                if age % 4 == 0 and age <= 244 then snap("square") end
            end
        end
        if leg_test ~= "" and hud_frame > 0 and is_hud then
            local age = frame - hud_frame
            local clock_age=age-leg_delay
            local function drive(name,first,duration) pulse(name,clock_age,first,duration) end
            local prefix = leg_side == 1 and "" or "p2"
            local opponent = prefix == "" and "p2" or ""
            local actor = program:read_u32(prefix == "" and 0x01060220 or 0x01060df0)
            local victim = program:read_u32(prefix == "" and 0x01060df0 or 0x01060220)
            local health = prefix == "" and 0x010602f0 or 0x01060ec0
            local victim_health = prefix == "" and 0x01060ec0 or 0x010602f0
            local function sample()
                local function signed(n) return n >= 0x8000 and n - 0x10000 or n end
                return {x=signed(program:read_u16(actor+0x90)), y=signed(program:read_u16(actor+0xb0)),
                    vx=program:read_u32(actor+0x40), vy=program:read_u32(actor+0x60),
                    tx=signed(program:read_u16(victim+0x90)), ty=signed(program:read_u16(victim+0xb0)),
                    tvx=program:read_u32(victim+0x40), tvy=program:read_u32(victim+0x60),
                    pose=program:read_u32(actor+0x1d0), target_pose=program:read_u32(victim+0x1d0),
                    suppression=program:read_u16(0x010619d0),
                    left=signed(program:read_u16(0x0105ecf0))+0x3a,
                    right=signed(program:read_u16(0x0105ed00))+0x15f,
                    action=program:read_u16(program:read_u32(leg_side==1 and 0x01060260 or 0x01060e30)+0x1f0),
                    target_action=program:read_u16(program:read_u32(leg_side==1 and 0x01060e30 or 0x01060260)+0x1f0),
                    id=program:read_u16(actor+0x1f0),target_id=program:read_u16(victim+0x1f0),
                    health=program:read_u16(health), target_health=program:read_u16(victim_health)}
            end
            if age == 160 then leg_baseline = sample() end
            if leg_corner then
                local edge=leg_test=="corner_left" and "left" or "right"
                pulse(prefix..edge,age,180,500)
                pulse(opponent..edge,age,180,500)
                if age==650 then leg_edge_start=sample() end
                if age==675 then
                    leg_edge_end=sample()
                    print(string.format("MK2KS_LEG_EDGE edge=%s baseline=%d,%d first=%d,%d last=%d,%d",
                        edge,leg_baseline.x,leg_baseline.tx,leg_edge_start.x,leg_edge_start.tx,leg_edge_end.x,leg_edge_end.tx))
                    snap("corner-approach")
                end
            end
            local forward = prefix .. (prefix == "" and "right" or "left")
            if leg_test ~= "far" and (not leg_negative or leg_test=="down_last") then drive(forward,180,30) end
            local duration=leg_test=="held" and 120 or 4
            local down_first,lp_first,block_first=300,300,300
            if leg_test=="block_first" or leg_test=="block2_first" then down_first,block_first=296,296 end
            if leg_test=="lp_first" or leg_test=="lp_first_block2" then down_first,lp_first=296,296 end
            if leg_test=="down_last" then lp_first,block_first=296,296 end
            local block_button=(leg_test=="block2" or leg_test=="block2_first" or leg_test=="lp_first_block2") and "block2" or "block"
            if leg_test~="no_down" then drive(prefix .. "down",down_first,300+duration-down_first) end
            if leg_test~="no_lp" then drive(prefix .. "lp",lp_first,300+duration-lp_first) end
            if leg_test~="no_block" then drive(prefix .. block_button,block_first,300+duration-block_first) end
            if clock_age==296 then
                print(string.format("MK2KS_LEG_COMMAND mode=%s side=%d down=%d lp=%d block=%d button=%s",
                    leg_test,leg_side,down_first+leg_delay,lp_first+leg_delay,block_first+leg_delay,block_button))
            end
            if leg_test=="extra_button" then drive(prefix .. "hp",300,duration) end
            if leg_test=="airborne" then drive(prefix .. "up",290,3) end
            if leg_test == "block" or leg_test == "duck_block" then drive(opponent .. "block",280,240) end
            if leg_test == "duck" or leg_test == "duck_block" then drive(opponent .. "down",280,240) end
            if leg_test == "air" then drive(opponent .. "up",290,3) end
            if clock_age >= 290 and clock_age <= 500 then
                local s=sample()
                leg_samples[age]=s
                print(string.format("MK2KS_LEG_STATE age=%d x=%d y=%d vx=%08X vy=%08X tx=%d ty=%d tvx=%08X tvy=%08X health=%d,%d action=%04X victim_action=%04X bounds=%d,%d",
                    age,s.x,s.y,s.vx,s.vy,s.tx,s.ty,s.tvx,s.tvy,s.health,s.target_health,
                    s.action,s.target_action,s.left,s.right))
                if clock_age >= 300 and clock_age <= 450 and clock_age % 3 == 0 then snap("leg-" .. age) end
                if os.getenv("MK2KS_TRACE_LEG") == "1" and (clock_age == 343 or clock_age == 347 or clock_age == 351) then
                    leg_geometry("pose-"..age, {actor,victim})
                end
            end
            if clock_age == 600 then leg_last = sample() end
            local facing_right=program:read_u16(actor+0x90)<program:read_u16(victim+0x90)
            drive(prefix .. "down",620,3)
            drive(prefix .. (facing_right and "right" or "left"),625,3)
            drive(prefix .. "lp",626,3)
            if leg_victim_id>=17 then
                drive(opponent .. "down",760,3)
                local right=(leg_victim_id==17 and facing_right) or
                    (leg_victim_id==18 and not facing_right)
                drive(opponent .. (right and "right" or "left"),765,3)
                drive(opponent .. (leg_victim_id==17 and "hp" or "lp"),766,3)
            else
                drive(opponent .. "up",760,3) -- actual victim-owned jump/recovery
            end
            if clock_age==950 then
                local s=sample()
                if s.ty~=leg_baseline.ty or s.tvy~=0 then leg_followups[2]=0 end
            end
        end
        if ball_test ~= "" and hud_frame > 0 and is_hud then
            local age = frame - hud_frame
            local side = fighter == "kano" and 1 or 2
            local prefix, opponent = side == 1 and "" or "p2", side == 1 and "p2" or ""
            local p1x, p2x = program:read_u16(0x01034f20), program:read_u16(0x01035130)
            local right = side == 1 and p1x < p2x or side == 2 and p2x < p1x
            pulse(prefix .. (ball_test == "wrong_button" and "hp" or "lk"), age, 180, ball_hold)
            if ball_test == "recharge" then pulse(prefix .. "lk", age, 300, 40) end
            if ball_test == "airborne" then pulse(prefix .. "up", age, 170 + ball_hold, 3) end
            if ball_test == "block" then pulse(opponent .. "block", age, 300, 290) end
            if ball_test == "miss" then pulse(opponent .. "down", age, 300, 290) end
            if ball_test ~= "held" then
                pulse(prefix .. "down", age, 620, 3)
                pulse(prefix .. (right and "left" or "right"), age, 625, 3)
                pulse(prefix .. "hp", age, 626, 3)
            end
            if age == 160 or (age >= 176 and age <= 580) then
                local obj = program:read_u32(side == 1 and 0x01060220 or 0x01060df0)
                local y = program:read_u16(obj + 0xb0)
                if y >= 0x8000 then y = y - 0x10000 end
                local sample = {x=program:read_u16(obj+0x90), y=y,
                    vx=program:read_u32(obj+0x40),vy=program:read_u32(obj+0x60),gravity=program:read_u32(obj+0x20),
                    health={program:read_u16(0x010602f0),program:read_u16(0x01060ec0)}}
                ball_samples[age]=sample
                if os.getenv("MK2KS_BALL_VICTIM_AIR_TRACE") == "1" and
                    age >= 356 and age <= 460 and age % 4 == 0 then
                    local victim = program:read_u32(side == 1 and 0x01060df0 or 0x01060220)
                    local attacker_task = program:read_u32(side == 1 and 0x01060260 or 0x01060e30)
                    local victim_task = program:read_u32(side == 1 and 0x01060e30 or 0x01060260)
                    local victim_y = program:read_u16(victim + 0xb0)
                    local victim_floor = program:read_u16(victim_task + 0x200)
                    print(string.format("MK2KS_BALL_VICTIM_AIR age=%d gap=%d attacker_y=%d attacker_action=%04X victim_height=%d victim_action=%04X",
                        age,math.abs(sample.x-program:read_u16(victim+0x90)),sample.y,
                        program:read_u16(attacker_task+0x1f0),
                        (victim_floor-victim_y)&0xffff,
                        program:read_u16(victim_task+0x1f0)))
                end
                if ball_trace then
                    print(string.format("MK2KS_BALL_STATE age=%d side=%d x=%d y=%d vx=%08X vy=%08X gravity=%08X health=%d,%d",
                        age,side,sample.x,sample.y,sample.vx,sample.vy,sample.gravity,sample.health[1],sample.health[2]))
                end
                if age >= 180 + ball_hold and age <= 270 + ball_hold and age % 4 == 0 then snap("ball") end
            end
        end
        if hud_frame > 0 and (frame == hud_frame + 120 or frame == hud_frame + 600 or frame == hud_frame + 1200) then
            snap("combat")
        end
        if os.getenv("MK2KS_TRACE_REACTIONS") == "1" and hud_frame > 0 and
            frame >= hud_frame + 180 and frame <= hud_frame + 900 and frame % 30 == 0 then snap("reaction_trace") end
    end
end)

emu.register_stop(function()
    local cpu = manager.machine.devices[":maincpu"]
    if cpu then
        local dump = {}
        for _, reg in ipairs({"PC", "SP", "A0", "A1", "A2", "A8", "A9", "A13"}) do
            dump[#dump + 1] = string.format("%s=%08X", reg, cpu.state[reg].value)
        end
        print("MK2KS_EXIT_STOP " .. table.concat(dump, " "))
        local sp = cpu.state["SP"].value
        print(string.format("MK2KS_EXIT_STACK %08X %08X %08X", program:read_u32(sp), program:read_u32(sp + 32), program:read_u32(sp + 64)))
    end
    local passed = css_frame > 0 and exit_frame > 0 and hud_frame > exit_frame and
        combat_frames > 300 and outside_frames > 300 and leaks == 0 and identity_errors == 0 and
        name_errors == 0 and (not name_mask or name_checks > 0) and (not two_player or p2_joined) and
        roster_errors == 0 and stalled_frames == 0 and trap_frames == 0 and unexpected_campaign_resets == 0 and
        (not name_mask or native_names > 0) and
        (not round_win or native_wins > 0 or allow_natural_loss and campaign_lost) and
        -- A stock P1 victim has no custom finish-prompt tap. Require two
        -- native P2 wins instead of treating that missing P1 tap as a loss.
        (not round_loss or native_finishes > 0 or
            fighter ~= "kano" and fighter ~= "sonya" and
            native_p2_wins >= 2)
    passed = passed and selection_errors == 0 and p2_identity_errors == 0 and
        (not name_mask or selection_checks > 0) and (not name_mask or two_player or ladder_entries > 0) and
        (confirm == "timeout" or exit_frame - css_frame < 400)
    if assert_native_display then
        local display_pass = display_checks > 0 and display_errors == 0
        passed = passed and display_pass
        print(string.format("MK2KS_DISPLAY_RESULT pass=%s checks=%d errors=%d",
            tostring(display_pass), display_checks, display_errors))
    end
    if assert_hud_shadow then
        local shadow_pass = hud_shadow_checks >= 6 and hud_shadow_errors == 0
        passed = passed and shadow_pass
        print(string.format("MK2KS_HUD_SHADOW_RESULT pass=%s checks=%d errors=%d",
            tostring(shadow_pass), hud_shadow_checks, hud_shadow_errors))
    end
    if test_projectiles then
        local positive = projectile_command == "native"
        local p1health, p2health = program:read_u16(0x010602f0), program:read_u16(0x01060ec0)
        local projectile_pass = positive and projectile_entries[1] >= 8 and projectile_entries[2] >= 8 and
            projectile_frames > 0 and p1health > 0 and p1health < 161 and p2health > 0 and p2health < 161
        if not positive then
            projectile_pass = projectile_entries[1] == 0 and projectile_entries[2] == 0 and projectile_frames == 0
        end
        passed = passed and projectile_pass
        print(string.format("MK2KS_PROJECTILES_RESULT pass=%s command=%s p1_entries=%d p2_entries=%d frame_reads=%d health=%d,%d",
            tostring(projectile_pass), projectile_command, projectile_entries[1], projectile_entries[2], projectile_frames,
            p1health, p2health))
    end
    if square_test ~= "" then
        local side = fighter == "sonya" and 1 or 2
        local negative = square_test == "reversed" or square_test == "expired" or
            square_test == "wrong_button" or square_test == "airborne" or square_test == "with_block"
        local first, recovered = square_baseline, square_samples[280]
        local rise_fields, flight_fields, fall_fields, height = 0, 0, 0, 0
        local trajectory_errors, contact_pause = 0, 0
        for age = 176, 280 do
            local sample = square_samples[age]
            if sample and first then
                height = math.max(height, first.y - sample.y)
                if sample.vy == 0xfff40000 then rise_fields = rise_fields + 1 end
                if sample.vx == 0x000a0000 or sample.vx == 0xfff60000 then
                    flight_fields = flight_fields + 1
                    if sample.y ~= first.y - 96 or sample.vy ~= 0 or sample.gravity ~= 0 or
                        sample.vx ~= (side == 1 and 0x000a0000 or 0xfff60000) then
                        trajectory_errors = trajectory_errors + 1
                    end
                end
                if sample.y == first.y - 96 and sample.vx == 0 and sample.vy == 0 and sample.gravity == 0 then
                    contact_pause = contact_pause + 1
                end
                if sample.gravity == 0x8000 and sample.vy > 0 and sample.vy < 0x80000000 then
                    fall_fields = fall_fields + 1
                end
            end
        end
        local own_damage = first and recovered and first.health[side] - recovered.health[side] or -1
        local damage = first and recovered and first.health[3-side] - recovered.health[3-side] or -1
        local expected_damage = (square_test == "air" or square_test == "air_block") and 27 or 0
        local grounded = first and recovered and recovered.y == first.y and
            recovered.vx == 0 and recovered.vy == 0 and recovered.gravity == 0
        local square_pass = square_trace_fields == 155 and grounded and own_damage == 0 and
            damage == expected_damage and square_followup_entries == 2 and square_entries[3-side] == 0
        if negative then
            square_pass = square_pass and square_entries[side] == 0 and square_attack_reads == 0
        else
            square_pass = square_pass and square_entries[side] == 2 and square_attack_reads > 0 and
                rise_fields == 8 and height == 96 and fall_fields == 16 and trajectory_errors == 0 and
                square_attack_reads == flight_fields * 9 and contact_pause == (expected_damage > 0 and 10 or 0)
            square_pass = square_pass and (expected_damage > 0 and flight_fields > 0 and flight_fields < 26 or
                expected_damage == 0 and flight_fields == 26)
        end
        passed = passed and square_pass
        print(string.format("MK2KS_SQUARE_RESULT pass=%s mode=%s entries=%d,%d attack_reads=%d damage=%d expected_damage=%d own_damage=%d rise=%d height=%d flight=%d fall=%d contact_pause=%d trajectory_errors=%d grounded=%s followup_entries=%d",
            tostring(square_pass), square_test, square_entries[1], square_entries[2], square_attack_reads,
            damage, expected_damage, own_damage, rise_fields, height, flight_fields, fall_fields, contact_pause,
            trajectory_errors, tostring(grounded), square_followup_entries))
    end
    if ball_test ~= "" then
        local side = fighter == "kano" and 1 or 2
        local first, last = ball_samples[160], ball_samples[580]
        local damage = first and last and first.health[3-side] - last.health[3-side] or -1
        local own_damage = first and last and first.health[side] - last.health[side] or -1
        local recovered = first and last and last.y == first.y and last.vx == 0 and last.vy == 0 and last.gravity == 0
        local expected_damage = (ball_negative or ball_test == "miss") and 0 or ball_test == "block" and 5 or 24
        local flight, rebound, trajectory_errors = 0, 0, 0
        for age=176,580 do
            local sample = ball_samples[age]
            if sample and first then
                if sample.vx == 0x000a0000 or sample.vx == 0xfff60000 then
                    flight = flight + 1
                    if sample.y ~= first.y + 16 or sample.vy ~= 0 or sample.gravity ~= 0 or
                        sample.vx ~= (side == 1 and 0x000a0000 or 0xfff60000) then
                        trajectory_errors = trajectory_errors + 1
                    end
                end
                if sample.gravity == 0x6000 then
                    rebound = rebound + 1
                    local velocity = ball_test == "block" and 0x10000 or 0x50000
                    if side == 1 then velocity = (0x100000000-velocity)&0xffffffff end
                    -- The native camera may stop horizontal motion at an edge.
                    if sample.vx ~= velocity and sample.vx ~= 0 then trajectory_errors = trajectory_errors + 1 end
                end
            end
        end
        local ball_pass = damage == expected_damage and own_damage == 0 and recovered and
            ball_followup_entries == (ball_test == "held" and 0 or 2)
        if ball_negative then
            ball_pass = ball_pass and ball_entries == 0 and ball_attack_reads == 0
        else
            ball_pass = ball_pass and ball_entries == (ball_test == "miss" and 2 or 4) and
                ball_first_collision and ball_start and ball_first_collision - ball_start == 7 and
                ball_start >= hud_frame + 180 + ball_hold and ball_start <= hud_frame + 184 + ball_hold and
                ball_attack_reads / 9 == flight - 6 and trajectory_errors == 0 and
                (ball_test == "miss" and flight == 26 and rebound == 0 or ball_test ~= "miss" and rebound > 30)
        end
        passed = passed and ball_pass
        print(string.format("MK2KS_BALL_RESULT pass=%s mode=%s hold=%d entries=%d attack_reads=%d damage=%d expected_damage=%d own_damage=%d flight=%d rebound=%d trajectory_errors=%d recovered=%s followup_entries=%d",
            tostring(ball_pass),ball_test,ball_hold,ball_entries,ball_attack_reads,damage,expected_damage,own_damage,
            flight,rebound,trajectory_errors,tostring(recovered),ball_followup_entries))
    end
    if leg_test ~= "" then
        local damage = leg_baseline and leg_last and leg_baseline.target_health-leg_last.target_health or -1
        local expected_damage = (leg_negative or leg_test == "far" or leg_test == "duck_block" or leg_test == "air") and 0 or 35
        local recovered = leg_baseline and leg_last and leg_last.y == leg_baseline.y and leg_last.ty == leg_baseline.ty and
            leg_last.vx == 0 and leg_last.vy == 0 and leg_last.tvx == 0 and leg_last.tvy == 0
        local trajectory_errors, paired_fields, release_delay = 0, 0, -1
        local function require_leg(condition,label)
            if not condition then
                trajectory_errors=trajectory_errors+1
                if trajectory_errors<=10 then print("MK2KS_LEG_ASSERT "..(label or "paired trajectory")) end
            end
        end
        if leg_corner then
            local direction=leg_test=="corner_left" and -1 or 1
            -- Both direction inputs remain held. The leading body must be at
            -- the actual native limit at both samples; the trailing body's
            -- ordinary push animation can oscillate by a pixel at the wall.
            local function at_edge(s)
                return s and (direction==-1 and math.min(s.x,s.tx)==s.left or
                    direction==1 and math.max(s.x,s.tx)==s.right)
            end
            require_leg(leg_edge_start and leg_edge_end and leg_baseline and
                at_edge(leg_edge_start) and at_edge(leg_edge_end) and
                direction*(leg_edge_end.x-leg_baseline.x)>200 and
                direction*(leg_edge_end.tx-leg_baseline.tx)>200,"edge approach")
        end
        if expected_damage==35 and leg_collision then
            local first=leg_collision-hud_frame+1
            local origin=leg_samples[first]
            local direction=leg_side==1 and 1 or -1
            local offsets=leg_victim_id==17 and {{85,0},{68,-41},{10,-80},{-56,-55},{-100,0}} or
                (leg_victim_id==18 and {{88,3},{67,-41},{7,-74},{-55,-38},{-111,0}} or leg_stock_offsets[leg_victim_id])
            local poses={0xfe83be60,0xfe83be00,0xfe83bda0,0xfe83bd40,0xfe83bce0}
            local victim_poses=leg_victim_poses[leg_victim_id]
            for elapsed=0,45 do
                local s=leg_samples[first+elapsed]
                if s and origin then
                    local pose=elapsed<30 and 1 or 2+(elapsed-30)//4
                    local shake=elapsed<30 and ((elapsed//3)%2==0 and 3 or 0) or 0
                    paired_fields=paired_fields+1
                    require_leg(s.x==origin.x and s.y==origin.y and s.vx==0 and s.vy==0 and s.tvx==0 and s.tvy==0)
                    require_leg(s.tx==origin.x+direction*offsets[pose][1] and s.ty==origin.y+offsets[pose][2]+shake)
                    require_leg(s.pose==poses[pose] and s.target_pose==victim_poses[pose])
                    require_leg(s.health==leg_baseline.health and s.target_health==leg_baseline.target_health and s.suppression>0)
                    require_leg(s.id==18 and s.target_id==leg_victim_id)
                    require_leg(s.action==0x110 and s.target_action==0x111,"paired state age="..(first+elapsed))
                else require_leg(false) end
            end
            -- Native task order may dispatch the victim on this field or the
            -- next, but the paired animation itself must be exactly 46 fields.
            for age=first,first+50 do
                local s=leg_samples[age]
                if s and s.target_health<leg_baseline.target_health then
                    release_delay=age-(leg_collision-hud_frame)
                    require_leg(release_delay==47 or release_delay==48)
                    require_leg(s.target_health==leg_baseline.target_health-35 and s.tvy==0xfffa0000)
                    require_leg(s.tvx==(direction==1 and 0xfffd0000 or 0x30000) and s.ty==leg_baseline.ty)
                    require_leg(s.target_action==0x506,"release state age="..age)
                    require_leg(leg_release_boundary_age and leg_release_boundary_age>=age and
                        leg_release_boundary_age<=age+1,"native boundary resumes on release")
                    break
                end
            end
            require_leg(release_delay~=-1)
            require_leg(leg_boundary_checks>0 and leg_boundary_errors==0,"native release boundaries")
            if (leg_test=="corner_left" and leg_side==1) or (leg_test=="corner_right" and leg_side==2) then
                require_leg(leg_release_clamps>0,"outward corner release must clamp")
            end
        end
        local activation=leg_negative and leg_entries==0 and leg_attack_reads==0 or
            not leg_negative and leg_entries==1 and leg_attack_reads==9 and leg_start and leg_collision and leg_collision-leg_start==10
        local leg_pass = activation and damage == expected_damage and recovered and
            leg_baseline.id==18 and leg_baseline.target_id==leg_victim_id and
            leg_last.id==18 and leg_last.target_id==leg_victim_id and
            leg_last.target_action~=0x111 and
            leg_baseline.health == leg_last.health and trajectory_errors==0 and
            (expected_damage~=35 or paired_fields==46) and leg_followups[1]>0 and leg_followups[2]>0
        passed = passed and leg_pass
        print(string.format("MK2KS_LEG_BOUNDARY_RESULT checks=%d errors=%d release_clamps=%d first_release_age=%d",
            leg_boundary_checks,leg_boundary_errors,leg_release_clamps,leg_release_boundary_age or -1))
        print(string.format("MK2KS_LEG_RESULT pass=%s mode=%s entries=%d attack_reads=%d damage=%d expected_damage=%d recovered=%s paired_fields=%d trajectory_errors=%d release_delay=%d ring_followup=%d victim_followup=%d victim=%s",
            tostring(leg_pass),leg_test,leg_entries,leg_attack_reads,damage,expected_damage,tostring(recovered),
            paired_fields,trajectory_errors,release_delay,leg_followups[1],leg_followups[2],leg_victim_name))
    end
    print(string.format("MK2KS_SELECTION_RESULT checks=%d errors=%d ladder_entries=%d p2=%s p2_identity_errors=%d",
        selection_checks, selection_errors, ladder_entries, p2_fighter, p2_identity_errors))
    print(string.format("MK2KS_P2_CPU_RESUME_RESULT checks=%d",p2_cpu_schedule_checks))
    print(string.format("MK2KS_P1_CPU_RESUME_RESULT checks=%d",p1_cpu_schedule_checks))
    print(string.format("MK2KS_P2_CPU_WIN_RESULT checks=%d",p2_cpu_win_checks))
    print(string.format("MK2KS_P2_CPU_LOSS_RESULT checks=%d",p2_cpu_loss_checks))
    print(string.format("MK2KS_NATIVE_RESULT roster_errors=%d hud_entries=%d win_entries=%d finish_prompts=%d released_actor_fields=%d constructing_actor_fields=%d transition_actor_fields=%d",
        roster_errors, native_names, native_wins, native_finishes, released_actor_fields,
        constructing_actor_fields, transition_actor_fields))
    print(string.format("MK2KS_STABILITY stalled_frames=%d trap_frames=%d", stalled_frames, trap_frames))
    print(string.format("MK2KS_CAMPAIGN_END_RESULT lost=%s unexpected_resets=%d completed=%s",
        tostring(campaign_lost), unexpected_campaign_resets, tostring(campaign_completed)))
    if assert_lifecycle then
        local lifecycle_pass = (allow_no_recovery or recoveries > 0) and
            recovery_errors == 0 and object_resets > 0 and
            ground_errors == 0 and position_errors == 0
        passed = passed and lifecycle_pass
        print(string.format("MK2KS_LIFECYCLE_RESULT pass=%s recoveries=%d recovery_errors=%d resets=%d ground_errors=%d position_errors=%d",
            tostring(lifecycle_pass), recoveries, recovery_errors, object_resets, ground_errors, position_errors))
    end
    print(string.format("MK2KS_EXIT_RESULT pass=%s fighter=%s confirm=%s css=%d exit=%d hud=%d outside=%d combat=%d leaks=%d identity_errors=%d name_checks=%d name_errors=%d frame=%d",
        tostring(passed), fighter, confirm, css_frame, exit_frame, hud_frame, outside_frames,
        combat_frames, leaks, identity_errors, name_checks, name_errors, frame))
    -- Release observer taps while Lua and the address space are still live.
    -- Do not leave callbacks to be collected during emulator destruction.
    for _, tap in ipairs(native_taps) do tap:remove() end
    for _, tap in ipairs(animation_taps) do tap:remove() end
    if finish_tap then finish_tap:remove() end
    if position_tap then position_tap:remove() end
    if dma_tap then dma_tap:remove() end
    native_taps, animation_taps = {}, {}
    finish_tap, position_tap, dma_tap = nil, nil, nil
    collectgarbage("collect")
end)
