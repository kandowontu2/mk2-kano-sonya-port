-- Input-only Kano air-throw audit. The selector harness owns the real match.
assert(os.getenv("MK2KS_TWO_PLAYER") == "1")
local fighter = os.getenv("MK2KS_TEST_FIGHTER")
local opponent = os.getenv("MK2KS_P2_FIGHTER")
local attacker_side = tonumber(os.getenv("MK2KS_AIRTHROW_SIDE") or "1")
assert(attacker_side == 1 or attacker_side == 2)
local attacker_name = attacker_side == 1 and fighter or opponent
local victim_name = attacker_side == 1 and opponent or fighter
assert(attacker_name == "kano" or attacker_name == "jax")
local roster = {kung_lao=true, liu_kang=true, cage=true, baraka=true,
    kitana=true, mileena=true, shang_tsung=true, raiden=true,
    sub_zero=true, reptile=true, scorpion=true, jax=true,
    kano=true, sonya=true}
assert(roster[victim_name])
local distance_limit = tonumber(os.getenv("MK2KS_AIRTHROW_DISTANCE") or "63")
assert(distance_limit >= 20 and distance_limit <= 100)
local edge_frames = tonumber(os.getenv("MK2KS_AIRTHROW_EDGE_SHIFT") or "0")
local edge_direction = os.getenv("MK2KS_AIRTHROW_EDGE_DIRECTION") or "right"
local repeat_total = tonumber(os.getenv("MK2KS_AIRTHROW_REPEAT") or "1")
assert(edge_frames >= 0 and edge_frames <= 240)
assert(edge_direction == "right" or edge_direction == "left")
assert(repeat_total == 1 or repeat_total == 2)
dofile("mk2ks_selector_exit_test.lua")

local frame, hud, ready, command, health_start, health_end = 0, nil, nil, nil, nil, nil
local cpu, program, screen, p1, p2 = nil, nil, nil, nil, nil
local action_tap = nil
local root_taps = {}
local victim_taps = {}
local align_stream_dumped = false
local thrown = false
local completed_throws = 0
local shift_started, shift_done = nil, edge_frames == 0
local function signed(value) return value >= 0x8000 and value - 0x10000 or value end
local function sample(side)
    local actor = program:read_u32(side == 1 and 0x01060220 or 0x01060df0)
    local process = program:read_u32(side == 1 and 0x01060260 or 0x01060e30)
    return {
        actor = actor, process = process,
        id = program:read_u16(actor + 0x1f0),
        x = signed(program:read_u16(actor + 0x90)),
        y = signed(program:read_u16(actor + 0xb0)),
        floor = signed(program:read_u16(process + 0x200)),
        action = program:read_u16(process + 0x1f0),
        pose = program:read_u32(actor + 0x1d0),
        vx = program:read_u32(side == 1 and 0x010602d0 or 0x01060ea0),
        flags = program:read_u32(process + 0x210),
        health = program:read_u16(side == 1 and 0x010602f0 or 0x01060ec0),
    }
end
emu.register_frame(function()
    frame = frame + 1
    if not program then
        cpu = manager.machine.devices[":maincpu"]
        program = cpu.spaces.program
        screen = manager.machine.screens[":screen"]
        if os.getenv("MK2KS_AIRTHROW_DASM") == "1" then
            local debugger = assert(manager.machine.debugger)
            debugger.visible_cpu = cpu
            debugger:command("dasm audit_airthrow_damage_helper.asm,FF83A700,900")
            debugger:command("dasm audit_airthrow_victim_sequence.asm,FF8DA700,900")
            debugger:command("dasm audit_airthrow_victim_handoff.asm,FF842600,700")
            debugger:command("dasm audit_airthrow_jax_action.asm,FF8B7000,C00")
            debugger:command("dasm audit_airthrow_physics.asm,FF876650,600")
            debugger:command("dasm audit_airthrow_hvelocity.asm,FF876BE0,300")
            debugger:command("dasm audit_airthrow_setvelocity.asm,FF831AC0,180")
            debugger:command("dasm audit_airthrow_position.asm,FF804000,500")
            debugger:command("dasm audit_airthrow_integrate.asm,FF83C870,380")
            debugger:command("dasm audit_airthrow_v172_step.asm,FFFFF800,180")
            debugger:command("dasm audit_airthrow_align.asm,FF83CC20,500")
            debugger:command("dasm audit_airthrow_victim_anim_select.asm,FF906000,200")
            debugger:command("dasm audit_airthrow_victim_pose_setup.asm,FF838700,180")
            debugger:command("dasm audit_airthrow_victim_hold.asm,FF839240,500")
            debugger:command("dasm audit_v198_airthrow_recovery.asm,FF82FD50,900")
            debugger:command("dasm audit_v198_attacker_fall_caller.asm,FF8E4C00,400")
            debugger:command("dasm audit_v199_attacker_fall_entry.asm,FF8E4700,700")
            debugger:command("dasm audit_v199_fall_router.asm,FFFC1400,800")
            debugger:command("dasm audit_v201_victim_recovery.asm,FF8E6D00,800")
            debugger.execution_state = "run"
        end
        if os.getenv("MK2KS_AIRTHROW_STANCE_DASM") == "1" then
            local debugger = assert(manager.machine.debugger)
            debugger.visible_cpu = cpu
            debugger:command("dasm audit_v210_stance_recovery.asm,FF82F800,A00")
            debugger:command("dasm audit_v212_getup.asm,FF8EA240,700")
            debugger:command("dasm audit_v213_getup_setup.asm,FF8E6B00,400")
            debugger.execution_state = "run"
        end
        if os.getenv("MK2KS_AIRTHROW_RECOVERY_STACK_TRACE") == "1" then
            for _, address in ipairs({0xff82fd70, 0xff83c430, 0xff83c5a0,
                                      0xff82fe00, 0xff8e6d00, 0xff8e6e00}) do
                root_taps[#root_taps + 1] = program:install_read_tap(
                    address, address + 15, "airthrow attacker recovery stack",
                    function(offset, data, mask)
                        if offset == address and command and
                           frame >= command + 45 and frame <= command + 105 then
                            local stack = cpu.state.A12.value
                            local task = cpu.state.A13.value
                            print(string.format("MK2KS_AIRTHROW_RECOVERY_STACK age=%d pc=%08X task=%08X actor=%08X action=%04X a12=%08X top=%08X next=%08X a7=%08X a9=%08X",
                                frame - command, address, task, cpu.state.A8.value,
                                program:read_u16(task + 0x1f0), stack,
                                program:read_u32(stack), program:read_u32(stack + 32),
                                cpu.state.A7.value, cpu.state.A9.value))
                        end
                    end)
            end
        end
        local inputs = manager.machine.ioport.ports[":IN0"].fields
        p1 = {right = assert(inputs["P1 Right"]), left = assert(inputs["P1 Left"]),
            up = assert(inputs["P1 Up"]),
            block = assert(inputs["P1 Block"])}
        p2 = {left = assert(inputs["P2 Left"]), right = assert(inputs["P2 Right"]),
            up = assert(inputs["P2 Up"]),
            block = assert(inputs["P2 Block"])}
        if os.getenv("MK2KS_AIRTHROW_TRACE") == "1" then
            for _, range in ipairs({{0xff000000, 0xff00083f, "main"},
                                     {0xff000840, 0xff00107f, "special"}}) do
                root_taps[#root_taps + 1] = program:install_read_tap(range[1], range[2],
                    "Kano airthrow animation root", function(offset, data, mask)
                        if command and frame >= command - 5 and frame <= command + 90 and
                           offset % 32 == 0 then
                            print(string.format("MK2KS_AIRTHROW_ROOT frame=%d kind=%s index=%d data=%08X pc=%08X",
                                frame, range[3], (offset - range[1]) // 32,
                                data, cpu.state.PC.value))
                        end
                    end)
            end
            if attacker_name == "jax" then
                root_taps[#root_taps + 1] = program:install_read_tap(
                    0xff980000, 0xff9a0000, "Jax airthrow root search",
                    function(offset, data, mask)
                        if command and frame >= command + 14 and frame <= command + 22 and
                           offset % 32 == 0 then
                            print(string.format("MK2KS_JAX_AIR_ROOT frame=%d at=%08X data=%08X pc=%08X",
                                frame, offset, data, cpu.state.PC.value))
                        end
                    end)
            end
        end
        if os.getenv("MK2KS_AIRTHROW_ALIGN_TRACE") == "1" then
            root_taps[#root_taps + 1] = program:install_read_tap(
                0xff83cc20, 0xff83cc3f, "airthrow alignment caller",
                function(offset, data, mask)
                    if command and frame >= command + 12 and frame <= command + 120 and
                        offset == 0xff83cc20 then
                        local sp = cpu.state.SP.value
                        local a9 = cpu.state.A9.value
                        print(string.format("MK2KS_AIRTHROW_ALIGN frame=%d pc=%08X a0=%08X a1=%08X a8=%08X a9=%08X prev=%04X,%04X a13=%08X sp=%08X return=%08X",
                            frame, cpu.state.PC.value, cpu.state.A0.value, cpu.state.A1.value,
                            cpu.state.A8.value, a9, program:read_u16(a9 - 32),
                            program:read_u16(a9 - 16), cpu.state.A13.value, sp,
                            program:read_u32(sp)))
                        local task = cpu.state.A13.value
                        local owner = program:read_u32(task + 0x170)
                        print(string.format("MK2KS_AIRTHROW_ALIGN_TASK frame=%d anim=%04X action=%04X owner=%08X ownerid=%04X owneractor=%08X peer=%08X taskpc=%08X",
                            frame, program:read_u16(task + 0x360),
                            program:read_u16(task + 0x1f0), owner,
                            program:read_u16(owner + 0x1f0), program:read_u32(owner + 0x170),
                            program:read_u32(task + 0x140), program:read_u32(task + 0xe0)))
                        local p1_actor, p2_actor = program:read_u32(0x01060220), program:read_u32(0x01060df0)
                        local p1_process, p2_process = program:read_u32(0x01060260), program:read_u32(0x01060e30)
                        print(string.format("MK2KS_AIRTHROW_ALIGN_PLAYERS frame=%d p1actor=%08X p2actor=%08X p1process=%08X p2process=%08X p1id=%04X p2id=%04X",
                            frame, p1_actor, p2_actor, p1_process, p2_process,
                            program:read_u16(p1_actor + 0x1f0), program:read_u16(p2_actor + 0x1f0)))
                        for at = 0, 0x400, 0x20 do
                            local pointer = program:read_u32(task + at)
                            if pointer == p1_actor or pointer == p2_actor or
                                pointer == p1_process or pointer == p2_process then
                                print(string.format("MK2KS_AIRTHROW_ALIGN_TASK_PTR frame=%d at=%03X value=%08X",
                                    frame, at, pointer))
                            end
                        end
                        if not align_stream_dumped then
                            align_stream_dumped = true
                            for at = a9 - 160, a9 + 160, 16 do
                                print(string.format("MK2KS_AIRTHROW_ALIGN_STREAM address=%08X word=%04X",
                                    at, program:read_u16(at)))
                            end
                        end
                    end
                end)
        end
        if os.getenv("MK2KS_AIRTHROW_GROUP_TRACE") == "1" then
            root_taps[#root_taps + 1] = program:install_read_tap(
                0xff83bb50, 0xff83bb5f, "airthrow group renderer",
                function(offset, data, mask)
                    if command and frame >= command + 20 and frame <= command + 58 and
                        offset == 0xff83bb50 then
                        local peer_process = program:read_u32(cpu.state.A13.value + 0x170)
                        print(string.format("MK2KS_AIRTHROW_GROUP frame=%d group=%08X callback=%08X actor=%08X stream=%08X task=%08X action=%04X attacker=%08X peerproc=%08X peer_callback=%08X",
                            frame, cpu.state.A0.value, cpu.state.A6.value,
                            cpu.state.A8.value, cpu.state.A9.value, cpu.state.A13.value,
                            program:read_u16(cpu.state.A13.value + 0x1f0),
                            program:read_u32(cpu.state.A13.value + 0xc0),
                            peer_process, program:read_u32(peer_process + 0x290)))
                    end
                end)
        end
        if os.getenv("MK2KS_AIRTHROW_ATTACKER_VEL_TRACE") == "1" then
            root_taps[#root_taps + 1] = program:install_read_tap(
                0xff876650, 0xff87665f, "attacker fall setup",
                function(offset, data, mask)
                    if command and frame >= command + 45 and frame <= command + 60 and
                        offset == 0xff876650 then
                        local sp = cpu.state.SP.value
                        local peer_process = program:read_u32(cpu.state.A13.value + 0x170)
                        print(string.format("MK2KS_AIRTHROW_FALL_SETUP frame=%d a8=%08X task=%08X a0=%08X a1=%08X a2=%08X a3=%08X a7=%08X a12=%08X ret=%08X sp=%08X top=%08X next=%08X own_action=%04X own_callback=%08X peer=%08X peer_callback=%08X",
                            frame, cpu.state.A8.value, cpu.state.A13.value,
                            cpu.state.A0.value, cpu.state.A1.value,
                            cpu.state.A2.value, cpu.state.A3.value,
                            cpu.state.A7.value, cpu.state.A12.value,
                            program:read_u32(cpu.state.A12.value), sp,
                            program:read_u32(sp), program:read_u32(sp + 0x20),
                            program:read_u16(cpu.state.A13.value + 0x1f0),
                            program:read_u32(cpu.state.A13.value + 0x290),
                            peer_process, program:read_u32(peer_process + 0x290)))
                    end
                end)
        end
        if os.getenv("MK2KS_AIRTHROW_FALL_ROUTER_TRACE") == "1" then
            root_taps[#root_taps + 1] = program:install_read_tap(
                0xff8e4c10, 0xff8e4d3f, "stock fall entry path",
                function(offset, data, mask)
                    if command and frame >= command + 48 and frame <= command + 60 and
                        (offset == 0xff8e4c10 or offset == 0xff8e4c30 or
                            offset == 0xff8e4d30) then
                        print(string.format("MK2KS_AIRTHROW_FALL_ENTRY frame=%d pc=%08X a0=%08X a1=%08X a2=%08X",
                            frame, offset, cpu.state.A0.value, cpu.state.A1.value,
                            cpu.state.A2.value))
                    end
                end)
            local checkpoints = { [0xfffc1440]=true, [0xfffc14a0]=true,
                [0xfffc1510]=true, [0xfffc15c0]=true,
                [0xfffc15f0]=true, [0xfffc1650]=true, [0xfffc1660]=true }
            root_taps[#root_taps + 1] = program:install_read_tap(
                0xfffc1400, 0xfffc16af, "Kano fall router path",
                function(offset, data, mask)
                    if command and frame >= command + 48 and frame <= command + 60 and
                        checkpoints[offset] then
                        local task = cpu.state.A13.value
                        local peer = program:read_u32(task + 0x170)
                        print(string.format("MK2KS_AIRTHROW_FALL_ROUTER frame=%d pc=%08X a0=%08X a1=%08X actor=%08X attacker=%08X action=%04X peer_callback=%08X",
                            frame, offset, cpu.state.A0.value, cpu.state.A1.value,
                            cpu.state.A8.value, program:read_u32(task + 0xc0),
                            program:read_u16(task + 0x1f0),
                            program:read_u32(peer + 0x290)))
                    end
                end)
        end
        if os.getenv("MK2KS_AIRTHROW_VICTIM_END_TRACE") == "1" then
            root_taps[#root_taps + 1] = program:install_read_tap(
                0xff8e6f90, 0xff8e6f9f, "victim prone tail",
                function(offset, data, mask)
                    if command and frame >= command + 55 and frame <= command + 100 and
                        offset == 0xff8e6f90 then
                        local task = cpu.state.A13.value
                        local attacker_process = program:read_u32(task + 0x170)
                        local attacker_actor = program:read_u32(attacker_process + 0xc0)
                        print(string.format("MK2KS_AIRTHROW_VICTIM_END frame=%d task=%08X actor=%08X action=%04X callback=%08X attacker_process=%08X attacker_actor=%08X attacker_id=%04X stream=%08X pose=%08X",
                            frame, task, cpu.state.A8.value,
                            program:read_u16(task + 0x1f0),
                            program:read_u32(task + 0x290), attacker_process,
                            attacker_actor, program:read_u16(attacker_actor + 0x1f0),
                            cpu.state.A9.value, program:read_u32(cpu.state.A8.value + 0x1d0)))
                    end
                end)
        end
        if os.getenv("MK2KS_AIRTHROW_RECOVERY_TRACE") == "1" then
            root_taps[#root_taps + 1] = program:install_read_tap(
                0xff8e6e00, 0xff8e6f6f, "victim get-up frame transition",
                function(offset, data, mask)
                    if command and frame >= command + 48 and frame <= command + 82 and
                        (offset == 0xff8e6e30 or offset == 0xff8e6f10) then
                        local task = cpu.state.A13.value
                        print(string.format("MK2KS_AIRTHROW_RECOVERY frame=%d pc=%08X task=%08X callback=%08X stream=%08X next=%08X pose=%08X",
                            frame, offset, task, program:read_u32(task + 0x290),
                            cpu.state.A9.value, program:read_u32(cpu.state.A9.value),
                            program:read_u32(cpu.state.A8.value + 0x1d0)))
                    end
                end)
            root_taps[#root_taps + 1] = program:install_read_tap(
                0xfffc1400, 0xfffc15ff, "trial victim recovery router",
                function(offset, data, mask)
                    if command and frame >= command + 48 and frame <= command + 80 and
                        (offset == 0xfffc1400 or offset == 0xfffc1430 or
                            offset == 0xfffc1470 or offset == 0xfffc1490 or
                            offset == 0xfffc14b0 or offset == 0xfffc14f0 or
                            offset == 0xfffc1520 or offset == 0xfffc1570) then
                        local task = cpu.state.A13.value
                        print(string.format("MK2KS_AIRTHROW_RECOVERY_ROUTER frame=%d pc=%08X callback=%08X actor=%08X pose=%08X a0=%08X a1=%08X",
                            frame, offset, program:read_u32(task + 0x290),
                            cpu.state.A8.value, program:read_u32(cpu.state.A8.value + 0x1d0),
                            cpu.state.A0.value, cpu.state.A1.value))
                    end
                end)
        end
    end
    if not hud then
        local pixels, width = screen:pixels()
        if width ~= 400 or frame < 900 then return end
        local green = 0
        for x = 20, 380 do
            local c = string.unpack("<I4", pixels, (30 * width + x) * 4 + 1)
            local r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
            if g > 100 and g > r * 3 // 2 and g > b * 3 // 2 then green = green + 1 end
        end
        if green > 250 then hud = frame end
        return
    end
    if frame < hud + 180 or frame > hud + 500 + edge_frames + (repeat_total - 1) * 500 then return end
    local a, b = sample(attacker_side), sample(3 - attacker_side)
    if not command then
        if not shift_done then
            if not shift_started and math.abs(a.x - b.x) <= distance_limit then
                shift_started = frame
            end
            if shift_started then
                if frame - shift_started < edge_frames then
                    p1[edge_direction]:set_value(1)
                    p2[edge_direction]:set_value(1)
                    return
                end
                p1[edge_direction]:set_value(0)
                p2[edge_direction]:set_value(0)
                shift_done, ready = true, nil
            end
        end
        if math.abs(a.x - b.x) > distance_limit then
            if attacker_side == 1 then p1.right:set_value(1)
            else p2.left:set_value(1) end
            ready = nil
        else
            if attacker_side == 1 then p1.right:set_value(0)
            else p2.left:set_value(0) end
            ready = ready or frame
            if frame - ready >= 30 then
                command, health_start = frame + 20, b.health
                if os.getenv("MK2KS_AIRTHROW_TRACE") == "1" then
                    local process = a.process
                    action_tap = program:install_write_tap(process + 0x1f0, process + 0x1ff,
                        "airthrow action", function(offset, data, mask)
                            if frame >= command - 5 and frame <= command + 90 then
                                print(string.format("MK2KS_AIRTHROW_WRITE frame=%d at=%08X data=%08X mask=%08X pc=%08X",
                                    frame, offset, data, mask, cpu.state.PC.value))
                                print(string.format("MK2KS_AIRTHROW_REGS A0=%08X A1=%08X A7=%08X A8=%08X A9=%08X A12=%08X A13=%08X SP=%08X",
                                    cpu.state.A0.value, cpu.state.A1.value, cpu.state.A7.value,
                                    cpu.state.A8.value, cpu.state.A9.value, cpu.state.A12.value,
                                    cpu.state.A13.value, cpu.state.SP.value))
                            end
                        end)
                    for _, item in ipairs({{b.actor + 0x90, "x"},
                                            {b.actor + 0xb0, "y"},
                                            {b.actor + 0x1d0, "pose"},
                                            {attacker_side == 1 and 0x01060ec0 or 0x010602f0, "health"}}) do
                        victim_taps[#victim_taps + 1] = program:install_write_tap(
                            item[1], item[1] + (item[2] == "pose" and 31 or 15),
                            "airthrow victim " .. item[2], function(offset, data, mask)
                                if frame >= command - 3 and frame <= command + 70 then
                                    print(string.format("MK2KS_AIRTHROW_VICTIM_WRITE frame=%d field=%s data=%08X pc=%08X",
                                        frame, item[2], data, cpu.state.PC.value))
                                    if cpu.state.PC.value == 0xfffff880 then
                                        print(string.format("MK2KS_AIRTHROW_STEP_REGS A8=%08X A13=%08X A0=%08X A1=%08X speed=%08X",
                                            cpu.state.A8.value, cpu.state.A13.value,
                                            cpu.state.A0.value, cpu.state.A1.value,
                                            program:read_u32(cpu.state.A13.value + 0x70)))
                                    end
                                end
                            end)
                    end
                    for _, item in ipairs({{a.actor + 0x1f0, "attacker_id"},
                                            {b.actor + 0x1f0, "victim_id"}}) do
                        victim_taps[#victim_taps + 1] = program:install_read_tap(
                            item[1], item[1] + 15, "airthrow " .. item[2],
                            function(offset, data, mask)
                                if frame >= command + 50 and frame <= command + 65 and
                                   cpu.state.PC.value >= 0xfffff100 and
                                   cpu.state.PC.value < 0xfffff500 then
                                    print(string.format("MK2KS_AIRTHROW_ID_READ frame=%d field=%s at=%08X data=%08X pc=%08X",
                                        frame, item[2], offset, data, cpu.state.PC.value))
                                end
                            end)
                    end
                end
                if os.getenv("MK2KS_AIRTHROW_ATTACKER_VEL_TRACE") == "1" then
                    for _, item in ipairs({{a.actor + 0x20, "horizontal_velocity"},
                                            {a.actor + 0x60, "vertical_velocity"},
                                            {a.actor + 0xb0, "y"}}) do
                        victim_taps[#victim_taps + 1] = program:install_write_tap(
                            item[1], item[1] + (item[2] == "y" and 15 or 31),
                            "airthrow attacker " .. item[2], function(offset, data, mask)
                                if frame >= command + 44 and frame <= command + 78 then
                                    print(string.format("MK2KS_AIRTHROW_ATTACKER_WRITE frame=%d field=%s data=%08X pc=%08X",
                                        frame, item[2], data, cpu.state.PC.value))
                                end
                            end)
                    end
                end
                print(string.format("MK2KS_AIRTHROW_COMMAND frame=%d distance=%d id=%d,%d health=%d",
                    command, math.abs(a.x - b.x), a.id, b.id, health_start))
            end
        end
        return
    end
    local age = frame - command
    if os.getenv("MK2KS_AIRTHROW_ATTACKER_MOTION_TRACE") == "1" and
        age >= 48 and age <= 96 and age % 2 == 0 then
        local attacker = attacker_side == 1 and a or b
        print(string.format("MK2KS_AIRTHROW_ATTACKER_MOTION age=%d y=%d floor=%d actor_vy=%08X actor_accel=%08X process_vx=%08X action=%04X pose=%08X",
            age, attacker.y, attacker.floor,
            program:read_u32(attacker.actor + 0x60),
            program:read_u32(attacker.actor + 0x70), attacker.vx,
            attacker.action, attacker.pose))
    end
    if os.getenv("MK2KS_AIRTHROW_BOUNCE_TRACE") == "1" and
        age >= 40 and age <= 80 and age % 2 == 0 then
        local victim = attacker_side == 1 and b or a
        print(string.format("MK2KS_AIRTHROW_BOUNCE age=%d y=%d floor=%d actor_vx=%08X actor_vy=%08X actor_accel=%08X process_vx=%08X callback=%08X pose=%08X victim_pc=%08X",
            age, victim.y, victim.floor,
            program:read_u32(victim.actor + 0x20),
            program:read_u32(victim.actor + 0x60),
            program:read_u32(victim.actor + 0x70), victim.vx,
            program:read_u32(victim.process + 0x290), victim.pose,
            program:read_u32(victim.process + 0xe0)))
    end
    if os.getenv("MK2KS_AIRTHROW_TASK_PC_TRACE") == "1" and
       age >= 20 and age <= 92 and age % 4 == 0 then
        local attacker = attacker_side == 1 and a or b
        local hits = {}
        for offset = 0, 0x400, 4 do
            local value = program:read_u32(attacker.process + offset)
            if value >= 0xff8b7000 and value < 0xff8b7c00 then
                hits[#hits + 1] = string.format("+%03X=%08X", offset, value)
            end
        end
        print(string.format("MK2KS_AIRTHROW_TASK_PC age=%d process=%08X pc=%08X next=%08X hits=%s",
            age, attacker.process, program:read_u32(attacker.process + 0xe0),
            program:read_u32(attacker.process + 0xe4), table.concat(hits, ",")))
        local victim = attacker_side == 1 and b or a
        local victim_hits = {}
        for offset = 0, 0x400, 4 do
            local value = program:read_u32(victim.process + offset)
            if value >= 0xff8da000 and value < 0xff8dc000 then
                victim_hits[#victim_hits + 1] = string.format("+%03X=%08X", offset, value)
            end
        end
        print(string.format("MK2KS_AIRTHROW_VICTIM_TASK age=%d process=%08X pc=%08X next=%08X flags=%08X saved=%s",
            age, victim.process, program:read_u32(victim.process + 0xe0),
            program:read_u32(victim.process + 0xe4),
            program:read_u32(victim.process + 0x210), table.concat(victim_hits, ",")))
    end
    if os.getenv("MK2KS_AIRTHROW_TRACE") == "1" and age == 53 then
        for _, item in ipairs({{"p1", a}, {"p2", b}}) do
            local owner = program:read_u32(item[2].process + 0x170)
            local rival = program:read_u32(item[2].process + 0x140)
            print(string.format("MK2KS_AIRTHROW_PROCESS frame=%d side=%s process=%08X actor=%08X owner=%08X owner_id=%d rival=%08X rival_id=%d",
                frame, item[1], item[2].process, item[2].actor, owner,
                program:read_u16(owner + 0x1f0), rival,
                program:read_u16(rival + 0x1f0)))
        end
    end
    if os.getenv("MK2KS_AIRTHROW_CPU_TRACE") == "1" then
        if age == 53 then
            local debugger = assert(manager.machine.debugger)
            debugger.visible_cpu = cpu
            debugger:command("dasm audit_v167_airthrow_router.asm,FFFF1000,600")
            debugger:command("trace audit_v167_airthrow_cpu.trace,maincpu")
            debugger.execution_state = "run"
            print("MK2KS_AIRTHROW_CPU_TRACE_START")
        elseif age == 65 then
            manager.machine.debugger:command("trace off,maincpu")
            print("MK2KS_AIRTHROW_CPU_TRACE_STOP")
        end
    end
    if os.getenv("MK2KS_AIRTHROW_NOJUMP") ~= "1" and age >= 0 and age < 3 then
        p1.up:set_value(1); p2.up:set_value(1)
    end
    if age >= 20 and age < 26 then
        if attacker_side == 1 then p1.block:set_value(1)
        else p2.block:set_value(1) end
    end
    if age >= 15 and age <= 115 and age % 4 == 0 then
        print(string.format("MK2KS_AIRTHROW_STATE age=%d distance=%d p1=%d,%d floor=%d action=%04X pose=%08X vx=%08X flags=%08X p2=%d,%d floor=%d action=%04X pose=%08X vx=%08X flags=%08X health=%d",
            age, math.abs(a.x - b.x), a.x, a.y, a.floor, a.action, a.pose, a.vx, a.flags,
            b.x, b.y, b.floor, b.action, b.pose, b.vx, b.flags, b.health))
    end
    if age == 30 or age == 55 or age == 65 or age == 75 or age == 85 then
        screen:snapshot()
    end
    if os.getenv("MK2KS_AIRTHROW_LATE_SNAPSHOTS") == "1" and
        (age == 95 or age == 105 or age == 115) then
        screen:snapshot()
    end
    if os.getenv("MK2KS_AIRTHROW_RECOVERY_SNAPSHOTS") == "1" and
        age >= 52 and age <= 92 and age % 4 == 0 then
        print(string.format("MK2KS_AIRTHROW_RECOVERY_SNAPSHOT age=%d pose=%08X",
            age, b.pose))
        screen:snapshot()
    end
    if os.getenv("MK2KS_AIRTHROW_FINE_SNAPSHOTS") == "1" and
        age >= 32 and age <= 52 and age % 2 == 0 then
        screen:snapshot()
    end
    if os.getenv("MK2KS_AIRTHROW_DONOR_REVIEW_SNAPSHOTS") == "1" and
        (age == 24 or age == 32 or age == 40 or age == 48 or age == 56 or
         age == 64 or age == 72 or age == 76 or age == 80 or age == 84 or
         age == 88 or age == 92 or age == 96) then
        screen:snapshot(string.format("kano_airthrow_age%03d.png",age))
    end
    if os.getenv("MK2KS_AIRTHROW_LANDING_FRAME_SNAPSHOTS") == "1" and
        age >= 64 and age <= 74 then
        screen:snapshot(string.format("kano_landing_age%03d.png",age))
    end
    if age == 120 then
        health_end = b.health
        thrown = health_end < health_start
        print(string.format("MK2KS_AIRTHROW_RESULT observed_throw=%s damage=%d id=%d,%d",
            tostring(thrown), health_start - health_end, a.id, b.id))
        if repeat_total == 2 then
            if thrown then completed_throws = completed_throws + 1 end
            print(string.format("MK2KS_AIRTHROW_REPEAT completed=%d target=%d",
                completed_throws, repeat_total))
            if completed_throws == 1 then
                command, ready, health_start, health_end = nil, nil, nil, nil
            end
        end
    end
end)
emu.register_stop(function()
    if action_tap then action_tap:remove() end
    for _, tap in ipairs(root_taps) do tap:remove() end
    for _, tap in ipairs(victim_taps) do tap:remove() end
end)
