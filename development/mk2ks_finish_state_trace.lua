-- Diagnostic only: reuse the input-driven roster harness and report the
-- native arena/finish state fields that gate stock finisher commands.
if os.getenv("MK2_TRACE_LADDER") == "1" then
    dofile("mk2ks_cpu_ladder_trace.lua")
else
    dofile("mk2ks_selector_exit_test.lua")
end

local frame = 0
local last = ""
local finish_start = nil
local ports = manager.machine.ioport.ports
local high, low = ports[":IN0"].fields, ports[":IN2"].fields
local native_side = tonumber(os.getenv("MK2_TRACE_NATIVE_FINISH_SIDE") or "1")
assert(native_side == 1 or native_side == 2)
local label = native_side == 1 and "P1 " or "P2 "
local input = {down=high[label.."Down"],up=high[label.."Up"],
    left=high[label.."Left"],right=high[label.."Right"],
    hp=high[label.."High Punch"],hk=high[label.."High Kick"],
    lp=low[label.."Low Punch"],lk=low[label.."Low Kick"],
    block=high[label.."Block"]}
local stage_fighter = os.getenv("MK2_TRACE_STAGE_FINISH")
assert(not stage_fighter or stage_fighter == "kano" or stage_fighter == "sonya")
local native_fighter = os.getenv("MK2_TRACE_NATIVE_FINISH")
assert(not native_fighter or native_fighter == "kano" or native_fighter == "sonya")
local stock_scorpion_fire = os.getenv("MK2_TRACE_SCORPION_FIRE") == "1"
local input_only_approach = os.getenv("MK2_TRACE_INPUT_ONLY_APPROACH") == "1"
local approach_gap = tonumber(os.getenv("MK2_TRACE_APPROACH_GAP") or "65")
assert(approach_gap >= 60 and approach_gap <= 180)
local retreat_gap = tonumber(os.getenv("MK2_TRACE_INITIAL_RETREAT_GAP") or "")
assert(not retreat_gap or input_only_approach and retreat_gap >= 60 and retreat_gap <= 180)
assert(not input_only_approach or native_fighter or stock_scorpion_fire or stage_fighter)
assert(not input_only_approach or os.getenv("MK2_TRACE_POSITION_ASSIST") ~= "1")
local approach_done
local retreat_done
local action_tap, saw_action
local p2_takeover_checks, p2_takeover_errors, p2_takeover_first = 0, 0, nil
local post_finish_ladder_start
local post_finish_scene_start
local last_actor_finish_state = ""
local last_skeleton_pose
local last_kano_victim_phase
local first_skeleton_frame
local saw_burn_palette = false
local saw_burn_fire_palette = false
local saw_kano_victim_palette = false
local saw_jax_victim_palette = false
local saw_subzero_victim_palette = false
local finish_call_taps = {}
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 and stage_fighter and os.getenv("MK2_TRACE_STAGE_GATE") == "1" then
        local program = manager.machine.devices[":maincpu"].spaces.program
        local cpu = manager.machine.devices[":maincpu"].state
        local parser = stage_fighter == "kano" and 0xfffaa200 or 0xfffaa400
        for _,address in ipairs({parser,0xff876d20,0xff876e50,0xff876e80,
            0xff876f40,0xff877000,0xff877120,0xff8771f0,
            0xff877270,0xff877280,0xff877300,0xff877350,
            0xff8773a0,0xff877420}) do
            finish_call_taps[#finish_call_taps+1] = program:install_read_tap(
                address,address+15,"native stage finisher gate",function(offset)
                    if offset == address and finish_start and frame-finish_start <= 180 then
                        print(string.format("MK2_STAGE_GATE frame=%d age=%d arena=%d at=%08X pc=%08X a0=%08X a1=%08X a3=%08X a8=%08X",
                            frame,frame-finish_start,program:read_u16(0x01061ac0),address,cpu.PC.value,
                            cpu.A0.value,cpu.A1.value,cpu.A3.value,cpu.A8.value))
                    end
                end)
        end
    end
    if frame == 1 and os.getenv("MK2_TRACE_FINISH_SOUND") == "1" then
        local program = manager.machine.devices[":maincpu"].spaces.program
        local cpu = manager.machine.devices[":maincpu"].state
        finish_call_taps[#finish_call_taps + 1] = program:install_write_tap(
            0x01d01020, 0x01d0103f, "finish sound port trace", function(offset, data, mask)
                if finish_start and frame - finish_start <= 500 then
                    print(string.format("MK2_FINISH_SOUND_PORT frame=%d age=%d address=%08X data=%04X mask=%04X pc=%08X",
                        frame, frame - finish_start, offset, data & 0xffff,
                        mask & 0xffff, cpu.PC.value))
                end
            end)
        finish_call_taps[#finish_call_taps + 1] = program:install_read_tap(
            0xffa12530, 0xffa1253f, "finish sound command trace", function(offset)
                if offset == 0xffa12530 and finish_start and frame - finish_start <= 500 then
                    print(string.format("MK2_FINISH_SOUND frame=%d age=%d pc=%08X command=%04X actor=%08X",
                        frame, frame - finish_start, cpu.PC.value,
                        cpu.A0.value & 0xffff, cpu.A8.value))
                    if os.getenv("MK2_TRACE_FINISH_SOUND_CALLER") == "1" then
                        local sp = cpu.SP.value
                        print(string.format("MK2_FINISH_SOUND_STACK frame=%d command=%04X sp=%08X top=%08X next=%08X",
                            frame, cpu.A0.value & 0xffff, sp,
                            program:read_u32(sp), program:read_u32(sp + 0x20)))
                    end
                end
            end)
    end
    if frame == 1 and stock_scorpion_fire and
        os.getenv("MK2_TRACE_SCORPION_GATE") == "1" then
        local program = manager.machine.devices[":maincpu"].spaces.program
        local cpu = manager.machine.devices[":maincpu"].state
        for _, address in ipairs({0xff868bd0, 0xff868cd0, 0xff868d70,
            0xff868ef0, 0xff8775d0}) do
            finish_call_taps[#finish_call_taps + 1] = program:install_read_tap(
                address, address + 15, "stock Scorpion finish gate", function(offset)
                    if offset == address and finish_start and frame - finish_start <= 170 then
                        print(string.format("MK2_SCORPION_GATE frame=%d age=%d at=%08X pc=%08X a0=%08X a1=%08X a3=%08X a11=%08X",
                            frame, frame - finish_start, address, cpu.PC.value,
                            cpu.A0.value, cpu.A1.value, cpu.A3.value, cpu.A11.value))
                    end
                end)
        end
    end
    if frame == 1 and os.getenv("MK2_TRACE_FINISH_CALLS") == "1" then
        local program = manager.machine.devices[":maincpu"].spaces.program
        local cpu = manager.machine.devices[":maincpu"].state
        for _, address in ipairs({0xff8b7000, 0xff8c6f40, 0xff842730,
            0xff839260, 0xff83aa20, 0xff842710, 0xff8b7bc0,
            0xff8cdc40, 0xffa14860}) do
            finish_call_taps[#finish_call_taps + 1] = program:install_read_tap(
                address, address + 15, "stock finish call trace", function(offset)
                    if offset == address and finish_start and frame - finish_start <= 400 then
                        print(string.format("MK2_FINISH_CALL frame=%d age=%d entry=%08X pc=%08X a0=%08X a1=%08X a7=%08X a8=%08X a9=%08X a13=%08X",
                            frame, frame - finish_start, address, cpu.PC.value,
                            cpu.A0.value, cpu.A1.value, cpu.A7.value,
                            cpu.A8.value, cpu.A9.value, cpu.A13.value))
                    end
                end)
        end
    end
    if frame == 1 and native_fighter then
        local program = manager.machine.devices[":maincpu"].spaces.program
        if native_fighter == "sonya" and os.getenv("MK2_TRACE_KISS_CALLS") == "1" then
            local cpu = manager.machine.devices[":maincpu"].state
            for _, address in ipairs({0xfffb3000,0xfffb3400,0xfffb3800,
                0xff83ae20,0xff83ada0,0xff83f610,0xff83e8f0,
                0xff8093e0,0xff840b60,0xff83efd0,0xfffae400,
                0xff83c340,0xfffaf100,0xff80c6b0}) do
                finish_call_taps[#finish_call_taps+1]=program:install_read_tap(
                    address,address+15,"Sonya kiss call trace",function(offset)
                        if offset==address and finish_start and frame-finish_start<400 then
                            print(string.format("MK2_KISS_CALL frame=%d age=%d entry=%08X pc=%08X a0=%08X a1=%08X a8=%08X a9=%08X a13=%08X sp=%08X child=%08X facing=%04X flip=%04X",
                                frame,frame-finish_start,address,cpu.PC.value,cpu.A0.value,
                                cpu.A1.value,cpu.A8.value,cpu.A9.value,cpu.A13.value,
                                cpu.SP.value,program:read_u32(cpu.A13.value+0x190),
                                cpu.A8.value>=0x01000000 and cpu.A8.value<0x01100000 and
                                    program:read_u16(cpu.A8.value+0xc0) or 0xffff,
                                cpu.A8.value>=0x01000000 and cpu.A8.value<0x01100000 and
                                    program:read_u16(cpu.A8.value+0xf0) or 0xffff))
                        end
                    end)
            end
            if os.getenv("MK2_TRACE_KISS_DATA") == "1" then
                for _, range in ipairs({{0xfffb1800,0xfffb1a00},
                    {0xfffb2800,0xfffb2b80},{0xfffb2c00,0xfffb2d00},
                    {0xff700800,0xff700c00}}) do
                    finish_call_taps[#finish_call_taps+1]=program:install_read_tap(
                        range[1],range[2]-1,"Sonya kiss data trace",function(offset)
                            if finish_start and frame-finish_start>=197 and
                                frame-finish_start<205 then
                                print(string.format("MK2_KISS_DATA frame=%d age=%d at=%08X pc=%08X a0=%08X a8=%08X a9=%08X a11=%08X a13=%08X",
                                    frame,frame-finish_start,offset,cpu.PC.value,
                                    cpu.A0.value,cpu.A8.value,
                                    cpu.A9.value,cpu.A11.value,cpu.A13.value))
                            end
                        end)
                end
            end
        end
        if os.getenv("MK2_TRACE_PALETTE_COPY") == "1" then
            local cpu=manager.machine.devices[":maincpu"].state
            finish_call_taps[#finish_call_taps+1]=program:install_read_tap(
                0xff80c6b0,0xff80c6bf,"finish palette copy",function(offset)
                    if offset==0xff80c6b0 and finish_start and
                        (cpu.A0.value==0xfec95df0 or cpu.A0.value==0xfeccbf30) then
                        print(string.format("MK2_FINISH_PALETTE_CALL frame=%d pc=%08X a0=%08X a1=%08X a2=%08X a10=%08X a13=%08X source=%04X,%04X,%04X",
                            frame,cpu.PC.value,cpu.A0.value,cpu.A1.value,
                            cpu.A2.value,cpu.A10.value,cpu.A13.value,
                            program:read_u16(cpu.A0.value),
                            program:read_u16(cpu.A0.value+0x10),
                            program:read_u16(cpu.A0.value+0x20)))
                    end
                end)
        end
        if native_fighter == "kano" and os.getenv("MK2_TRACE_KANO_CLEANUP") == "1" then
            local cpu = manager.machine.devices[":maincpu"].state
            for _, address in ipairs({0xfffaf100,0xfffaf170,0xfffaf1a0,0xfffaf1c0,
                0xff83efd0,0xff840450,0xff80cad0,0xff80d580,
                0xff809670,0xffa1d860,0xff80e0e0}) do
                finish_call_taps[#finish_call_taps+1]=program:install_read_tap(
                    address,address+15,"Kano cleanup call trace",function(offset)
                        if offset==address and finish_start and frame-finish_start<500 then
                            local child=program:read_u32(cpu.A13.value+0x190)
                            local palette=child>=0x01000000 and child<0x01100000 and
                                program:read_u16(child+0x140) or 0xffff
                            local refcount=palette<0x1000 and program:read_u16(
                                0x0105bb30+(palette&0xff)*0x40+0x20) or 0xffff
                            local lists={}
                            for _,head in ipairs({0x0105d480,0x0105d4a0,0x0105d4c0}) do
                                local node=program:read_u32(head)
                                local found=false
                                for index=1,100 do
                                    if node==child then found=true;break end
                                    if node<0x01000000 or node>=0x01100000 then break end
                                    node=program:read_u32(node)
                                end
                                lists[#lists+1]=string.format("%08X:%s",head,tostring(found))
                            end
                            print(string.format("MK2_KANO_CLEANUP frame=%d age=%d entry=%08X pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X sp=%08X child=%08X palette=%04X refs=%d lists=%s",
                                frame,frame-finish_start,address,cpu.PC.value,cpu.A0.value,
                                cpu.A1.value,cpu.A8.value,cpu.A13.value,cpu.SP.value,
                                child,palette,refcount,table.concat(lists,",")))
                        end
                    end)
            end
        end
        local action = 0xff800000 + (native_fighter == "kano" and 0xf55c0 or 0xf5640) * 8
        action_tap = program:install_read_tap(action, action + 15,
            "native individual finish action", function(offset)
                if offset == action and not saw_action then
                    saw_action = true
                    print(string.format("MK2_NATIVE_FINISH_ACTION fighter=%s side=%d frame=%d address=%08X",
                        native_fighter, native_side, frame, action))
                end
            end)
    end
    if frame < 600 then return end
    local space = manager.machine.devices[":maincpu"].spaces.program
    -- Historical trace label: this field tracks ladder progression, not a
    -- fixed background (index 6 rendered different scenes in two controls).
    local arena = space:read_u16(0x01061ac0)
    local mode = space:read_u16(0x01061b00)
    local stage = space:read_u16(0x01061b30)
    local health1 = space:read_u16(0x010602f0)
    local health2 = space:read_u16(0x01060ec0)
    local key = string.format("%d:%d:%d", arena, mode, stage)
    if os.getenv("MK2_TRACE_P2_TAKEOVER") == "1" and native_side == 2 and
        saw_action and space:read_u16(0x010601d0) == 7 and
        space:read_u16(0x01060280) == 18 and health1 > 0 then
        local actor = space:read_u32(0x01060220)
        if actor >= 0x01000000 and actor < 0x01100000 then
            p2_takeover_checks = p2_takeover_checks + 1
            if space:read_u16(actor + 0x1f0) ~= 18 then
                p2_takeover_errors = p2_takeover_errors + 1
            end
            if not p2_takeover_first then
                p2_takeover_first = frame
                print(string.format("MK2_P2_TAKEOVER frame=%d roster=%04X actor=%08X id=%04X",
                    frame,space:read_u16(0x01060280),actor,
                    space:read_u16(actor+0x1f0)))
            elseif frame == p2_takeover_first + 24 then
                manager.machine.video:snapshot()
                print(string.format("MK2_P2_TAKEOVER_SNAPSHOT frame=%d",frame))
            end
        end
    end
    if key ~= last or (frame % 300 == 0 and health1 < 1000 and health2 < 1000) then
        print(string.format("MK2_FINISH_STATE frame=%d arena=%d mode=%d stage=%d hp1=%d hp2=%d",
            frame, arena, mode, stage, health1, health2))
        last = key
    end
    if os.getenv("MK2_TRACE_POST_FINISH_LADDER_SNAPSHOT") == "1" and saw_action then
        if stage == 1 and not post_finish_ladder_start then
            post_finish_ladder_start = frame
        end
        if post_finish_ladder_start and frame == post_finish_ladder_start + 20 then
            manager.machine.video:snapshot()
            print(string.format("MK2_POST_FINISH_LADDER_SNAPSHOT frame=%d stage=%d mode=%d",
                frame, stage, mode))
        end
    end
    if mode ~= 3 and finish_start and (saw_action or stock_scorpion_fire) and
        not post_finish_scene_start then
        post_finish_scene_start = frame
    end
    if os.getenv("MK2_TRACE_POST_FINISH_SCENE_SNAPSHOTS") == "1" and
        post_finish_scene_start and frame - post_finish_scene_start <= 240 and
        (frame - post_finish_scene_start) % 20 == 0 then
        manager.machine.video:snapshot()
        print(string.format("MK2_POST_FINISH_SCENE_SNAPSHOT frame=%d age=%d mode=%d",
            frame, frame - post_finish_scene_start, mode))
    end
    if mode ~= 3 then finish_start, approach_done, retreat_done = nil, nil, nil end
    if (os.getenv("MK2_TRACE_LIU_FINISH") == "1" or native_fighter or
        stock_scorpion_fire or
        stage_fighter and arena == 1) and mode == 3 then
        local p1 = space:read_u32(0x01060220)
        local p2 = space:read_u32(0x01060df0)
        if p1 < 0x01000000 or p1 >= 0x01100000 or
            p2 < 0x01000000 or p2 >= 0x01100000 then return end
        local x1, x2 = space:read_u16(p1 + 0x90), space:read_u16(p2 + 0x90)
        local attacker = native_side == 1 and p1 or p2
        local victim = native_side == 1 and p2 or p1
        local attacker_x = native_side == 1 and x1 or x2
        local victim_x = native_side == 1 and x2 or x1
        if not finish_start then
            finish_start = frame
            print(string.format("MK2_FINISH_ATTEMPT frame=%d x1=%d x2=%d",
                frame, x1, x2))
        end
        local age = frame - finish_start
        if native_fighter=="kano" and os.getenv("MK2_TRACE_KANO_PALETTE_TIMELINE")=="1" and
            (age==136 or age==137 or age==138 or age==139 or age==145 or age==198) then
            local bank=space:read_u16(p2+0x140)&0x7f00
            print(string.format("MK2_KANO_VICTIM_COLORS frame=%d age=%d bank=%04X first=%04X,%04X,%04X,%04X",
                frame,age,bank,
                space:read_u16(0x01800000+(bank+0)*0x10),
                space:read_u16(0x01800000+(bank+1)*0x10),
                space:read_u16(0x01800000+(bank+2)*0x10),
                space:read_u16(0x01800000+(bank+3)*0x10)))
        end
        if os.getenv("MK2_TRACE_FINISH_ACTORS") == "1" and age >= 0 and age <= 450 then
            local task1, task2 = space:read_u32(0x01060260), space:read_u32(0x01060e30)
            local function actor_state(object, task)
                local action = task >= 0x01000000 and task < 0x01100000 and
                    space:read_u16(task + 0x1f0) or 0xffff
                return string.format("%08X:%04X:%08X:%04X:%d:%d:%08X:%04X", object,
                    space:read_u16(object + 0x1f0), space:read_u32(object + 0x1d0),
                    action, space:read_u16(object + 0x90), space:read_u16(object + 0xb0),
                    space:read_u32(object + 0x1a0), space:read_u16(object + 0x1c0))
            end
            local current = actor_state(p1, task1) .. " " .. actor_state(p2, task2)
            if current ~= last_actor_finish_state then
                print(string.format("MK2_FINISH_ACTORS frame=%d age=%d mode=%d p1=%s p2=%s",
                    frame, age, mode, actor_state(p1, task1), actor_state(p2, task2)))
                last_actor_finish_state = current
            end
            if native_fighter=="kano" and os.getenv("MK2_TRACE_VICTIM_PHASE_SNAPSHOTS")=="1" then
                local id=space:read_u16(victim+0x1f0)
                local pose=space:read_u32(victim+0x1d0)
                local own_pose=space:read_u32(attacker+0x1d0)
                if id<19 and own_pose>=0xfe9b2670 and own_pose<=0xfe9b2810 then
                    for phase=0,5 do
                        if pose==space:read_u32(0xff800000+0xf7a00*8+id*256+phase*32) and
                            phase~=last_kano_victim_phase then
                            last_kano_victim_phase=phase
                            manager.machine.screens[":screen"]:snapshot(string.format("kano_victim_phase_%02d.png",phase))
                            print(string.format("MK2_FINISH_VICTIM_PHASE_SNAPSHOT frame=%d age=%d phase=%d pose=%08X",
                                frame,age,phase,pose))
                        end
                    end
                end
            end
            if os.getenv("MK2_TRACE_SKELETON_OBJECT") == "1" and native_fighter == "kano" then
                local owner_task = native_side == 1 and task1 or task2
                local attached = owner_task >= 0x01000000 and owner_task < 0x01100000 and
                    space:read_u32(owner_task+0x190) or 0
                if attached >= 0x01000000 and attached < 0x01100000 then
                    local pose=space:read_u32(attached+0x1d0)
                    local graphic=space:read_u32(attached+0x1a0)
                    local skeleton_state=string.format("%08X:%08X",pose,graphic)
                    if os.getenv("MK2_TRACE_SKELETON_FIRST_FIELDS") == "1" then
                        first_skeleton_frame=first_skeleton_frame or frame
                        local field=frame-first_skeleton_frame
                        if field<4 then
                            local bank=space:read_u16(attached+0x140)&0x7f00
                            local colors={}
                            for index=0,31 do colors[#colors+1]=string.format("%04X",
                                space:read_u16(0x01800000+(bank+index)*0x10)) end
                            manager.machine.screens[":screen"]:snapshot(string.format("kano_skeleton_first_%02d.png",field))
                            print(string.format("MK2_FINISH_SKELETON_FIRST frame=%d field=%d bank=%04X colors=%s",
                                frame,field,bank,table.concat(colors,",")))
                        end
                    end
                    if skeleton_state~=last_skeleton_pose then
                        local bank=space:read_u16(attached+0x140)&0x7f00
                        local colors={}
                        for index=0,31 do colors[#colors+1]=string.format("%04X",
                            space:read_u16(0x01800000+(bank+index)*0x10)) end
                        print(string.format("MK2_FINISH_SKELETON frame=%d age=%d task=%08X object=%08X pose=%08X graphic=%08X x=%d y=%d palette=%04X owner_palette=%04X victim_palette=%04X colors=%s",
                            frame,age,owner_task,attached,pose,graphic,space:read_u16(attached+0x90),
                            space:read_u16(attached+0xb0),bank,space:read_u16(attacker+0x140)&0x7f00,
                            space:read_u16(victim+0x140)&0x7f00,table.concat(colors,",")))
                        last_skeleton_pose=skeleton_state
                    end
                end
            end
            if not saw_burn_palette and space:read_u32(victim+0x1d0) == 0xfe9b0ae0 then
                saw_burn_palette = true
                local bank = space:read_u16(victim+0x140)&0x7f00
                local colors = {}
                for index=0,63 do
                    colors[#colors+1] = string.format("%04X",space:read_u16(0x01800000+(bank+index)*0x10))
                end
                print(string.format("MK2_FINISH_BURN_PALETTE frame=%d bank=%04X colors=%s",
                    frame,bank,table.concat(colors,",")))
            end
            if not saw_burn_fire_palette and space:read_u32(victim+0x1d0) == 0xfe9b0b20 then
                saw_burn_fire_palette = true
                local bank = space:read_u16(victim+0x140)&0x7f00
                local colors = {}
                for index=0,31 do
                    colors[#colors+1] = string.format("%04X",space:read_u16(0x01800000+(bank+index)*0x10))
                end
                print(string.format("MK2_FINISH_FIRE_PALETTE frame=%d bank=%04X colors=%s",
                    frame,bank,table.concat(colors,",")))
            end
            if native_fighter=="kano" and not saw_kano_victim_palette and
                space:read_u32(victim+0x1d0)==0xfe9b29b0 then
                saw_kano_victim_palette=true
                local bank=space:read_u16(victim+0x140)&0x7f00
                local colors={}
                for index=0,31 do colors[#colors+1]=string.format("%04X",
                    space:read_u16(0x01800000+(bank+index)*0x10)) end
                print(string.format("MK2_FINISH_KANO_VICTIM_PALETTE frame=%d bank=%04X colors=%s",
                    frame,bank,table.concat(colors,",")))
            end
            if native_fighter=="kano" and not saw_jax_victim_palette and
                space:read_u32(victim+0x1d0)==0xfe9b3110 then
                saw_jax_victim_palette=true
                local bank=space:read_u16(victim+0x140)&0x7f00
                local colors={}
                for index=0,63 do colors[#colors+1]=string.format("%04X",
                    space:read_u16(0x01800000+(bank+index)*0x10)) end
                print(string.format("MK2_FINISH_JAX_VICTIM_PALETTE frame=%d bank=%04X colors=%s",
                    frame,bank,table.concat(colors,",")))
            end
            if native_fighter=="kano" and not saw_subzero_victim_palette and
                space:read_u32(victim+0x1d0)==0xfe9b3890 then
                saw_subzero_victim_palette=true
                local bank=space:read_u16(victim+0x140)&0x7f00
                local colors={}
                for index=0,63 do colors[#colors+1]=string.format("%04X",
                    space:read_u16(0x01800000+(bank+index)*0x10)) end
                print(string.format("MK2_FINISH_SUBZERO_VICTIM_PALETTE frame=%d bank=%04X colors=%s",
                    frame,bank,table.concat(colors,",")))
            end
        end
        for _, field in pairs(input) do field:clear_value() end
        local forward = attacker_x < victim_x and "right" or "left"
        local back = forward == "right" and "left" or "right"
        -- MKII's native body separation stops a walking fighter roughly 60
        -- X units from the opponent; 50 would be unreachable without a grab.
        if retreat_gap and not retreat_done and age >= 65 and
            math.abs(attacker_x-victim_x) >= retreat_gap then
            retreat_done = age
            print(string.format("MK2_FINISH_INPUT_RETREAT frame=%d age=%d gap=%d",
                frame, age, math.abs(attacker_x-victim_x)))
        end
        if input_only_approach and not approach_done and (not retreat_gap or retreat_done) and
            age >= (stock_scorpion_fire and 15 or 65) and
            math.abs(attacker_x-victim_x) <= approach_gap then
            approach_done = age
            print(string.format("MK2_FINISH_INPUT_APPROACH frame=%d age=%d gap=%d",
                frame, age, math.abs(attacker_x-victim_x)))
        end
        local script_age = input_only_approach and
            (approach_done and age-approach_done+65 or 0) or age
        if age == 70 and os.getenv("MK2_TRACE_POSITION_ASSIST") == "1" then
            -- Diagnostic only: force close range after the round-ending recoil.
            -- Never use this as evidence of an input-only fatality.
            space:write_u16(attacker + 0x90,
                victim_x + (attacker_x < victim_x and -40 or 40))
            print("MK2_FINISH_POSITION_ASSIST applied")
        end
        if retreat_gap and not retreat_done and age >= 65 then input[back]:set_value(1)
        elseif script_age < 65 then input[forward]:set_value(1)
        elseif native_fighter == "kano" then
            if script_age >= 75 and script_age < 79 then input[back]:set_value(1)
            elseif script_age >= 85 and script_age < 89 then input.down:set_value(1)
            elseif script_age >= 95 and script_age < 99 then input[forward]:set_value(1)
            elseif script_age >= 105 and script_age < 109 then input.hk:set_value(1) end
        elseif native_fighter == "sonya" then
            if script_age >= 75 and script_age < 79 then input[back]:set_value(1)
            elseif script_age >= 85 and script_age < 89 then input[forward]:set_value(1)
            elseif script_age >= 95 and script_age < 99 or script_age >= 105 and script_age < 109 then input.down:set_value(1)
            elseif script_age >= 115 and script_age < 119 then input.lp:set_value(1) end
        elseif stage_fighter == "kano" then
            if script_age >= 70 and script_age < 100 then input.block:set_value(1) end
            if script_age >= 75 and script_age < 79 or script_age >= 85 and script_age < 89 then input.up:set_value(1)
            elseif script_age >= 95 and script_age < 99 then input[back]:set_value(1)
            elseif script_age >= 105 and script_age < 109 then input.lk:set_value(1) end
        elseif stage_fighter == "sonya" then
            if script_age >= 75 and script_age < 79 or script_age >= 85 and script_age < 89 then input[forward]:set_value(1)
            elseif script_age >= 95 and script_age < 99 then input.down:set_value(1)
            elseif script_age >= 105 and script_age < 109 then input.hp:set_value(1) end
        elseif stock_scorpion_fire then
            -- Stock MKII comparison: hold Block for Up, Up, then release it
            -- before HP. This only drives input; the game owns the action.
            if script_age >= 70 and script_age < 95 then input.block:set_value(1) end
            if script_age >= 75 and script_age < 79 or
                script_age >= 85 and script_age < 89 then input.up:set_value(1)
            elseif script_age >= 105 and script_age < 109 then input.hp:set_value(1) end
        else
            if age >= 75 and age < 79 then input.down:set_value(1)
            elseif age >= 85 and age < 89 then input[forward]:set_value(1)
            elseif age >= 95 and age < 99 then input[back]:set_value(1)
            elseif age >= 105 and age < 109 then input[back]:set_value(1)
            elseif age >= 115 and age < 119 then input.hk:set_value(1) end
        end
        if os.getenv("MK2_TRACE_FINISH_SNAPSHOTS") == "1" and age >= 65 and age <= 360 and age % 30 == 0 then
            manager.machine.video:snapshot()
            print(string.format("MK2_FINISH_FRAME_SNAPSHOT frame=%d age=%d", frame, age))
        end
        if os.getenv("MK2_TRACE_FINISH_FINE_SNAPSHOTS") == "1" and
            age >= 248 and age <= 288 and age % 8 == 0 then
            manager.machine.video:snapshot()
            print(string.format("MK2_FINISH_FINE_SNAPSHOT frame=%d age=%d", frame, age))
        end
        if native_fighter == "sonya" and os.getenv("MK2_TRACE_KISS_SNAPSHOTS") == "1" and
            age >= 198 and age <= 240 and age % 6 == 0 then
            manager.machine.video:snapshot()
            print(string.format("MK2_KISS_FRAME_SNAPSHOT frame=%d age=%d", frame, age))
        end
        if age % 15 == 0 then
            print(string.format("MK2_FINISH_ATTEMPT_STATE frame=%d age=%d x1=%d x2=%d fighter_id=%04X",
                frame, age, space:read_u16(p1 + 0x90), space:read_u16(p2 + 0x90),
                space:read_u16(attacker + 0x1f0)))
        end
        if native_fighter and os.getenv("MK2_TRACE_NATIVE_CPU") == "1" and age >= 100 then
            local cpu = manager.machine.devices[":maincpu"].state
            print(string.format("MK2_NATIVE_CPU frame=%d age=%d pc=%08X a8=%08X a9=%08X a10=%08X a13=%08X sp=%08X mode=%d",
                frame, age, cpu.PC.value, cpu.A8.value, cpu.A9.value,
                cpu.A10.value, cpu.A13.value, cpu.SP.value, mode))
        end
    end
end)
emu.register_stop(function()
    if os.getenv("MK2_TRACE_P2_TAKEOVER") == "1" then
        print(string.format("MK2_P2_TAKEOVER_RESULT pass=%s checks=%d errors=%d first=%s finish_action=%s",
            tostring(p2_takeover_checks >= 20 and p2_takeover_errors == 0 and saw_action),
            p2_takeover_checks,p2_takeover_errors,tostring(p2_takeover_first),
            tostring(saw_action)))
    end
end)
