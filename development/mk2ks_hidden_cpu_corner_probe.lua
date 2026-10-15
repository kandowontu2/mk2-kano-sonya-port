-- One-player hidden-CPU edge probe. The native observer (or stock-control
-- path) makes one pre-construction opponent-ID diagnostic write; combat
-- itself uses only P1 inputs and does not move actors or alter health/state.
local stock_jax_control = os.getenv("MK2KS_HIDDEN_STOCK_JAX_CONTROL") == "1"
if stock_jax_control then dofile("mk2ks_selector_exit_test.lua")
else dofile("mk2ks_cpu_ladder_trace.lua") end

local frame, program, controls = 0, nil, nil
local direction = os.getenv("MK2KS_HIDDEN_CORNER_DIRECTION") or "left"
assert(direction == "left" or direction == "right")
local strategy = os.getenv("MK2KS_HIDDEN_CORNER_STRATEGY") or "walk"
assert(strategy == "walk" or strategy == "mid_guard" or strategy == "edge_guard" or
    strategy == "edge_projectile" or strategy == "edge_projectile_guard" or
    strategy == "edge_jump" or strategy == "close_jump" or
    strategy == "pressure_uppercut")
local react_to_jump = os.getenv("MK2KS_HIDDEN_AIRTHROW_REACT") == "1"
local reaction_style = os.getenv("MK2KS_HIDDEN_REACTION_STYLE") or "immediate"
assert(reaction_style == "immediate" or reaction_style == "guard_then_jump" or
    reaction_style == "preemptive_air_block")
local reaction_target = os.getenv("MK2KS_HIDDEN_REACTION_TARGET") or "any"
assert(reaction_target == "any" or reaction_target == "action0200")
local jump_start_age = tonumber(os.getenv("MK2KS_HIDDEN_JUMP_START_AGE") or "451")
assert(jump_start_age >= 425 and jump_start_age <= 475)
local trace_airborne_prep = os.getenv("MK2KS_HIDDEN_TRACE_AIRBORNE_PREP") == "1"
local hidden_id = tonumber(os.getenv("MK2KS_DIAGNOSTIC_CPU_ID") or "14")
local stock_stage_index = tonumber(os.getenv("MK2KS_DIAGNOSTIC_LADDER_INDEX") or "")
assert(not stock_stage_index or stock_stage_index >= 0 and stock_stage_index <= 16)
local expected_player_id = stock_jax_control and 11 or 17
-- ID 8 (stock Sub-Zero) and IDs 17/18 are ordinary CPU controls for
-- the same jump detector in their respective ROMs.
assert(hidden_id == 8 or hidden_id == 14 or hidden_id == 15 or hidden_id == 16 or
    hidden_id == 17 or hidden_id == 18)
local entered, active, min_player_x, max_player_x, min_cpu_x, max_cpu_x = false, 0
local stationary_walk_fields, longest_stationary_walk, last_player_x = 0, 0, nil
local airborne, airborne_episodes, launch_like_episodes, non_launch_airborne_episodes,
    max_jump, was_airborne = 0, 0, 0, 0, 0, false
local voluntary_jump_episodes, last_ground_action = 0, nil
local player_airborne, player_jump_episodes, player_max_jump, player_was_airborne = 0, 0, 0, false
local health_changes, last_health = 0, nil
local cpu_health_changes, cpu_damage, last_cpu_health = 0, 0, nil
local knife_entries, knife_tap = 0, nil
local reaction_start, reaction_health = nil, nil
local airborne_prep = {}
local close_jump_epoch = nil
local stock_injected = false
local stock_regen_writes = 0
local function signed(word)
    return word >= 0x8000 and word - 0x10000 or word
end

emu.register_frame(function()
    frame = frame + 1
    if not program then
        program = manager.machine.devices[":maincpu"].spaces.program
        local cpu_state = manager.machine.devices[":maincpu"].state
        knife_tap = program:install_read_tap(0xff0004e0, 0xff0004ff,
            "hidden probe Kano knife action", function(offset, data, mask)
                if entered and cpu_state.A8.value == program:read_u32(0x01060220) then
                    knife_entries = knife_entries + 1
                    if knife_entries <= 8 then
                        print(string.format("MK2KS_HIDDEN_KNIFE_ENTRY frame=%d age=%d count=%d",
                            frame, active, knife_entries))
                    end
                end
            end)
        local high = manager.machine.ioport.ports[":IN0"].fields
        local low = manager.machine.ioport.ports[":IN2"].fields
        controls = {left=high["P1 Left"], right=high["P1 Right"],
            up=high["P1 Up"], down=high["P1 Down"], hp=high["P1 High Punch"],
            hk=high["P1 High Kick"], block=high["P1 Block"],
            lp=low["P1 Low Punch"], lk=low["P1 Low Kick"],
            block2=low["P1 Block 2"]}
    end
    if stock_jax_control and stock_stage_index and frame == 1100 then
        local old_stage = program:read_u16(0x01061b30)
        program:write_u16(0x01061b30, stock_stage_index)
        print(string.format("MK2KS_STOCK_HIDDEN_STAGE frame=%d old=%d requested=%d",
            frame, old_stage, stock_stage_index))
    end
    if stock_jax_control and not stock_injected and frame >= 1112 and frame < 1300 and
        program:read_u16(0x01060280) == 11 and
        program:read_u16(0x01060e50) <= 11 then
        local original = program:read_u16(0x01060e50)
        program:write_u16(0x01060e50, hidden_id)
        stock_injected = true
        print(string.format("MK2KS_STOCK_HIDDEN_INJECT frame=%d old=%d requested=%d",
            frame, original, hidden_id))
    end
    local player = program:read_u32(0x01060220)
    local opponent = program:read_u32(0x01060df0)
    if player < 0x01000000 or player >= 0x01100000 or
        opponent < 0x01000000 or opponent >= 0x01100000 or
        program:read_u16(opponent+0x1f0) ~= hidden_id or
        program:read_u16(player+0x1f0) ~= expected_player_id or
        program:read_u16(0x010602f0) == 0 or
        program:read_u16(0x01060ec0) == 0 or
        (not entered and (program:read_u16(0x010602f0) < 100 or
            program:read_u16(0x01060ec0) < 100)) then return end
    if not entered then
        entered = true
        print(string.format("MK2KS_HIDDEN_CPU_EDGE_ENTER frame=%d p1=%08X cpu=%08X",
            frame, player, opponent))
    end
    active = active + 1
    local px, ox = signed(program:read_u16(player+0x90)),
        signed(program:read_u16(opponent+0x90))
    min_player_x = math.min(min_player_x or px, px)
    max_player_x = math.max(max_player_x or px, px)
    min_cpu_x = math.min(min_cpu_x or ox, ox)
    max_cpu_x = math.max(max_cpu_x or ox, ox)
    if active <= 1100 and px == last_player_x then
        stationary_walk_fields=stationary_walk_fields+1
        longest_stationary_walk=math.max(longest_stationary_walk,stationary_walk_fields)
    else stationary_walk_fields=0 end
    last_player_x=px
    local oy=signed(program:read_u16(opponent+0xb0))
    local cpu_process=program:read_u32(0x01060e30)
    local ground_y=signed(program:read_u16(cpu_process+0x200))
    local jump=ground_y-oy
    -- Round teardown can temporarily repurpose the process floor slot;
    -- reject impossible offsets before classifying an airborne episode.
    local in_air=jump>20 and jump<=400
    local py=signed(program:read_u16(player+0xb0))
    local player_process=program:read_u32(0x01060260)
    local player_ground=signed(program:read_u16(player_process+0x200))
    local player_jump=player_ground-py
    if trace_airborne_prep and not reaction_start then
        airborne_prep[#airborne_prep + 1] = string.format(
            "frame=%d age=%d p1_x=%d p1_y=%d p1_action=%04X cpu_x=%d cpu_y=%d cpu_jump=%d cpu_action=%04X",
            frame, active, px, py, program:read_u16(player_process+0x1f0),
            ox, oy, jump, program:read_u16(cpu_process+0x1f0))
        if #airborne_prep > 24 then table.remove(airborne_prep, 1) end
    end
    local player_in_air=player_jump>20 and player_jump<=400
    if player_in_air then
        player_airborne=player_airborne+1
        player_max_jump=math.max(player_max_jump,player_jump)
        if not player_was_airborne then player_jump_episodes=player_jump_episodes+1 end
    end
    player_was_airborne=player_in_air
    local cpu_action=program:read_u16(cpu_process+0x1f0)
    if jump >= -4 and jump <= 4 then last_ground_action=cpu_action end
    local preemptive=(reaction_style == "preemptive_air_block" and
        (cpu_action == 0x030b or cpu_action == 0x010e or cpu_action == 0x0200) and
        player_jump > 4 and math.abs(px-ox) <= 150)
    local target_ok=(reaction_target == "any" or cpu_action == 0x0200)
    if react_to_jump and not reaction_start and target_ok and (preemptive or
        (jump>4 and jump<=400 and math.abs(px-ox)<=110)) then
        reaction_start, reaction_health=active,program:read_u16(0x01060ec0)
        print(string.format("MK2KS_HIDDEN_REACTIVE_THROW_START frame=%d age=%d id=%d x=%d,%d jump=%d p1_jump=%d cpu_action=%04X style=%s target=%s",
            frame,active,hidden_id,px,ox,jump,player_jump,cpu_action,reaction_style,reaction_target))
    end
    if in_air then
        airborne=airborne+1
        max_jump=math.max(max_jump,jump)
        if not was_airborne then
            airborne_episodes=airborne_episodes+1
            local action=program:read_u16(cpu_process+0x1f0)
            local launch_like=action==0x0503
            local voluntary=(not launch_like and last_ground_action==0x030b and
                action==0x010e)
            if launch_like then launch_like_episodes=launch_like_episodes+1
            else non_launch_airborne_episodes=non_launch_airborne_episodes+1 end
            if voluntary then voluntary_jump_episodes=voluntary_jump_episodes+1 end
            if trace_airborne_prep and not launch_like then
                for _, state in ipairs(airborne_prep) do
                    print("MK2KS_HIDDEN_AIRBORNE_PREP " .. state)
                end
            end
            print(string.format("MK2KS_HIDDEN_CPU_AIRBORNE frame=%d age=%d id=%d x=%d,%d height=%d action=%04X pose=%08X health=%d kind=%s",
                frame,active,hidden_id,px,ox,jump,action,
                program:read_u32(opponent+0x1d0),program:read_u16(0x01060ec0),
                launch_like and "launch_like" or
                (voluntary and "voluntary_jump" or "non_launch_unknown")))
        end
    end
    was_airborne=in_air
    local hp = program:read_u16(0x010602f0)
    if stock_jax_control and os.getenv("MK2KS_DIAGNOSTIC_P1_REGEN") == "1" and
        hp > 0 and hp < 161 then
        program:write_u16(0x010602f0, 161)
        stock_regen_writes = stock_regen_writes + 1
        if stock_regen_writes <= 3 then
            print(string.format("MK2KS_STOCK_HIDDEN_REGEN frame=%d old=%d", frame, hp))
        end
        hp = 161
    end
    if last_health and last_health ~= hp then health_changes=health_changes+1 end
    last_health=hp
    local cpu_hp = program:read_u16(0x01060ec0)
    -- Exclude the native 4-HP construction value and round resets; only
    -- count damage sustained during an active combat mode.
    if last_cpu_health and cpu_hp<last_cpu_health and cpu_hp>=10 and
        last_cpu_health>=10 and program:read_u16(0x01061b00)==0 then
        cpu_health_changes=cpu_health_changes+1
        cpu_damage=cpu_damage+last_cpu_health-cpu_hp
        if cpu_health_changes<=16 then
            print(string.format("MK2KS_HIDDEN_CPU_DAMAGE frame=%d age=%d amount=%d gap=%d p1_action=%04X cpu_action=%04X cpu_jump=%d",
                frame,active,last_cpu_health-cpu_hp,math.abs(px-ox),
                program:read_u16(player_process+0x1f0),
                program:read_u16(cpu_process+0x1f0),jump))
        end
    end
    last_cpu_health=cpu_hp
    -- Replace the observer's round-win inputs with actual P1 controls.
    -- None of these strategies writes combat state or assumes an edge was
    -- reached merely because the player held a direction.
    for _, field in pairs(controls) do field:set_value(0) end
    if strategy == "walk" then
        if active <= 1100 then controls[direction]:set_value(1)
        else controls.block:set_value(1) end
    elseif strategy == "mid_guard" then
        -- Stay near the ordinary opening spacing. Alternate standing and
        -- crouching guard without moving either actor through memory.
        if active % 160 < 80 then controls.block:set_value(1)
        else controls.down:set_value(1); controls.block:set_value(1) end
    elseif strategy == "edge_guard" then
        if active <= 600 then controls[direction]:set_value(1)
        else
            controls.down:set_value(1)
            if active % 34 < 4 then controls.hp:set_value(1)
            else controls.block:set_value(1) end
        end
    elseif strategy == "edge_projectile" or strategy == "edge_projectile_guard" then
        if active <= 450 and math.abs(px-ox) < 145 then
            controls[direction]:set_value(1)
        elseif math.abs(px-ox) > 125 then
            local phase=active%55
            local backward=px<ox and controls.left or controls.right
            if phase<3 then controls.down:set_value(1) end
            if phase>=5 and phase<8 then backward:set_value(1) end
            if phase>=6 and phase<9 then controls.hp:set_value(1) end
        else
            controls.down:set_value(1)
            if strategy == "edge_projectile" and active%34<4 then
                controls.hp:set_value(1)
            else controls.block:set_value(1) end
        end
    elseif strategy == "pressure_uppercut" then
        -- Repeated ordinary crouching uppercuts may launch a CPU-owned
        -- hidden victim; keep the approach entirely in controller input.
        if math.abs(px-ox)>68 then
            controls[ox>=px and "right" or "left"]:set_value(1)
        else
            controls.down:set_value(1)
            if active%28<4 then controls.hp:set_value(1) end
        end
        if active%28==0 and active<500 then
            print(string.format("MK2KS_HIDDEN_PRESSURE frame=%d age=%d gap=%d p1_action=%04X cpu_action=%04X cpu_hp=%d",
                frame,active,math.abs(px-ox),program:read_u16(player_process+0x1f0),
                program:read_u16(cpu_process+0x1f0),cpu_hp))
        end
    elseif strategy == "close_jump" then
        -- Approach through ordinary P1 controls, then provoke a CPU jump
        -- from actual air-throw spacing rather than a long cross-screen gap.
        local gap=math.abs(px-ox)
        if gap>90 then
            controls[ox>=px and "right" or "left"]:set_value(1)
        else
            close_jump_epoch=close_jump_epoch or active
            local phase=(active-close_jump_epoch)%110
            if phase<3 then
                controls.up:set_value(1)
            elseif phase>=18 and phase<31 then
                controls.block:set_value(1)
            elseif phase>=45 and gap>68 then
                controls[ox>=px and "right" or "left"]:set_value(1)
            else
                controls.block:set_value(1)
            end
        end
    else
        if active < jump_start_age then
            controls[direction]:set_value(1)
        else
            local phase=(active-jump_start_age)%130
            if phase<3 then
                controls.up:set_value(1)
                -- A forward jump is a real P1 input; the opponent remains
                -- entirely under the game's ordinary CPU control.
                if ox>=px then controls.right:set_value(1)
                else controls.left:set_value(1) end
            elseif phase>=35 then controls.block:set_value(1) end
        end
    end
    if reaction_start then
        local reaction_age=active-reaction_start
        if reaction_age<32 then
            for _, field in pairs(controls) do field:set_value(0) end
            local forward=ox>=px and controls.right or controls.left
            if reaction_style == "preemptive_air_block" then
                controls.block:set_value(1)
            elseif reaction_style == "guard_then_jump" then
                if reaction_age<5 then controls.block:set_value(1)
                elseif reaction_age<8 then controls.up:set_value(1); forward:set_value(1)
                elseif reaction_age<23 then forward:set_value(1)
                elseif reaction_age<31 then controls.block:set_value(1) end
            else
                if reaction_age<3 then
                    controls.up:set_value(1)
                    forward:set_value(1)
                elseif reaction_age<19 then forward:set_value(1)
                elseif reaction_age<28 then controls.block:set_value(1) end
            end
        end
        if reaction_age<=56 and reaction_age%4==0 then
        print(string.format("MK2KS_HIDDEN_REACTIVE_THROW_STATE age=%d x=%d,%d jump=%d p1_action=%04X p1_pose=%08X p1_health=%d cpu_action=%04X cpu_health=%d",
                reaction_age,px,ox,jump,
                program:read_u16(player_process+0x1f0),
                program:read_u32(player+0x1d0),program:read_u16(0x010602f0),
                program:read_u16(cpu_process+0x1f0),
                program:read_u16(0x01060ec0)))
        end
        if reaction_age==0 or reaction_age==16 or reaction_age==32 or reaction_age==52 then
            manager.machine.video:snapshot()
        end
        if reaction_age==56 then
            print(string.format("MK2KS_HIDDEN_REACTIVE_THROW_RESULT id=%d health_delta=%d",
                hidden_id,reaction_health-program:read_u16(0x01060ec0)))
        end
    end
    if trace_airborne_prep and active >= jump_start_age - 3 and
        active <= jump_start_age + 20 then
        print(string.format("MK2KS_HIDDEN_JUMP_WINDOW frame=%d age=%d x=%d,%d p1_action=%04X p1_jump=%d cpu_action=%04X cpu_jump=%d",
            frame, active, px, ox, program:read_u16(player_process+0x1f0),
            player_jump, cpu_action, jump))
    end
    if active % 300 == 0 then
        print(string.format("MK2KS_HIDDEN_CPU_EDGE_STATE frame=%d age=%d id=%d strategy=%s x=%d,%d cpu_y=%d floor=%d hp=%d,%d airborne=%d episodes=%d",
            frame, active, hidden_id, strategy, px, ox, oy, ground_y, hp,
            program:read_u16(0x01060ec0), airborne, airborne_episodes))
        manager.machine.video:snapshot()
    end
end)

emu.register_stop(function()
    print(string.format("MK2KS_HIDDEN_CPU_EDGE_RESULT entered=%s active=%d id=%d stock_jax_control=%s stock_injected=%s direction=%s strategy=%s p1_x=%s,%s cpu_x=%s,%s longest_stationary_walk=%d p1_airborne=%d p1_jump_episodes=%d p1_max_jump=%d cpu_airborne=%d airborne_episodes=%d launch_like_episodes=%d non_launch_airborne_episodes=%d voluntary_jump_episodes=%d max_jump=%d health_changes=%d cpu_health_changes=%d cpu_damage=%d knife_entries=%d stock_regen_writes=%d",
        tostring(entered), active, hidden_id, tostring(stock_jax_control),
        tostring(stock_injected), direction, strategy,
        tostring(min_player_x), tostring(max_player_x),
        tostring(min_cpu_x), tostring(max_cpu_x), longest_stationary_walk,
        player_airborne, player_jump_episodes, player_max_jump, airborne,
        airborne_episodes, launch_like_episodes, non_launch_airborne_episodes,
        voluntary_jump_episodes, max_jump,
        health_changes, cpu_health_changes, cpu_damage, knife_entries,
        stock_regen_writes))
end)
