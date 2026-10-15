-- Read-only audit for addresses behind the build report's missing mappings.
-- Most high-numbered "special" cells are embedded component data, not real
-- dispatch-table entries; a read tap here is not proof of a missing move.
-- Run with the ordinary selector harness or a finisher harness via the env var.
local base = os.getenv("MK2KS_ANIM_PROBE_BASE") or "mk2ks_selector_exit_test.lua"
dofile(base)

local entries = {
    {"kano", "main", 0xff000000, {59, 60, 61}},
    {"kano", "special", 0xff000840, {13, 62, 64}},
    {"sonya", "main", 0xff020000, {48, 59, 60, 61}},
    {"sonya", "special", 0xff020840, {60, 62, 63, 64}},
}
if os.getenv("MK2KS_ANIM_AUDIT_STOCK_LIU59") == "1" then
    entries[#entries + 1] = {"liu", "main", 0xff91fc60, {59}}
end
local frame, cpu, program = 0, nil, nil
local taps, counts, first_frames, last_frames = {}, {}, {}, {}
local pending_snapshot = nil
local first_main_trace = nil
local trace_key = os.getenv("MK2KS_ANIM_AUDIT_TRACE_KEY")
local direct48_counts = {}

emu.register_frame(function()
    frame = frame + 1
    if pending_snapshot then
        manager.machine.video:snapshot()
        print(string.format("MK2KS_ANIM_AUDIT_SNAPSHOT frame=%d key=%s", frame, pending_snapshot))
        pending_snapshot = nil
    end
    if program and first_main_trace and frame - first_main_trace <= 48 then
        local age = frame - first_main_trace
        local actor, opponent = program:read_u32(0x01060220), program:read_u32(0x01060df0)
        local process, opponent_process = program:read_u32(0x01060260), program:read_u32(0x01060e30)
        if actor >= 0x01000000 and actor < 0x01100000 and
            opponent >= 0x01000000 and opponent < 0x01100000 and
            process >= 0x01000000 and process < 0x01100000 and
            opponent_process >= 0x01000000 and opponent_process < 0x01100000 then
            print(string.format("MK2KS_ANIM_FIRST_MAIN_STATE age=%d p1_action=%04X p1_pose=%08X p1_hp=%d p2_action=%04X p2_pose=%08X p2_hp=%d",
                age,program:read_u16(process + 0x1f0),program:read_u32(actor + 0x1d0),
                program:read_u16(0x010602f0),program:read_u16(opponent_process + 0x1f0),
                program:read_u32(opponent + 0x1d0),program:read_u16(0x01060ec0)))
            if age == 4 or age == 12 or age == 24 or age == 40 then
                manager.machine.video:snapshot()
            end
        end
    end
    if program then return end
    cpu = manager.machine.devices[":maincpu"]
    program = cpu.spaces.program
    print("MK2KS_ANIM_AUDIT_BASE " .. base)
    if os.getenv("MK2KS_ANIM_AUDIT_COMPARE_WORDS") == "1" then
        print(string.format("MK2KS_ANIM_AUDIT_WORDS kano=%08X sonya=%08X",
            program:read_u32(0xff0015e0), program:read_u32(0xff0214e0)))
    end
    for _, entry in ipairs(entries) do
        local fighter, kind, root, ids = entry[1], entry[2], entry[3], entry[4]
        for _, id in ipairs(ids) do
            local key = fighter .. ":" .. kind .. ":" .. id
            local address = root + id * 32
            counts[key] = 0
            taps[#taps + 1] = program:install_read_tap(address, address + 31,
                "missing donor animation " .. key, function(offset, data, mask)
                    counts[key] = counts[key] + 1
                    first_frames[key] = first_frames[key] or frame
                    if kind == "main" and (not trace_key or trace_key == key) and
                        not first_main_trace and
                        os.getenv("MK2KS_ANIM_AUDIT_TRACE_FIRST_MAIN") == "1" then
                        first_main_trace = frame
                    end
                    if counts[key] == 1 and os.getenv("MK2KS_ANIM_AUDIT_SNAPSHOTS") == "1" then
                        pending_snapshot = key
                    end
                    if last_frames[key] ~= frame then
                        local detail = ""
                        if os.getenv("MK2KS_ANIM_AUDIT_ACTOR_STATE") == "1" then
                            local actor, opponent = program:read_u32(0x01060220),
                                program:read_u32(0x01060df0)
                            local process, opponent_process = program:read_u32(0x01060260),
                                program:read_u32(0x01060e30)
                            local valid_p1 = actor >= 0x01000000 and actor < 0x01100000 and
                                process >= 0x01000000 and process < 0x01100000
                            local valid_p2 = opponent >= 0x01000000 and opponent < 0x01100000 and
                                opponent_process >= 0x01000000 and opponent_process < 0x01100000
                            detail = string.format(" stage=%d a8=%08X a13=%08X p1_id=%04X p1_action=%04X p1_pose=%08X p2_id=%04X p2_action=%04X p2_pose=%08X",
                                program:read_u16(0x01061b30),cpu.state.A8.value,cpu.state.A13.value,
                                valid_p1 and program:read_u16(actor + 0x1f0) or 0xffff,
                                valid_p1 and program:read_u16(process + 0x1f0) or 0xffff,
                                valid_p1 and program:read_u32(actor + 0x1d0) or 0,
                                valid_p2 and program:read_u16(opponent + 0x1f0) or 0xffff,
                                valid_p2 and program:read_u16(opponent_process + 0x1f0) or 0xffff,
                                valid_p2 and program:read_u32(opponent + 0x1d0) or 0)
                        end
                        print(string.format("MK2KS_ANIM_AUDIT_READ frame=%d key=%s at=%08X data=%08X pc=%08X%s",
                            frame, key, offset, data, cpu.state.PC.value, detail))
                    end
                    last_frames[key] = frame
                end)
        end
    end
    if os.getenv("MK2KS_ANIM_AUDIT_DIRECT48") == "1" then
        -- MKII main 48 has two standalone Liu frame words after the active
        -- group-pointer sequence. The builder reports them as unmapped. Prove
        -- whether Shang's throw ever reads them before treating this as art.
        for index, address in ipairs({0xff0287b0, 0xff0287d0}) do
            local key = "sonya:main:48:direct" .. index
            direct48_counts[key] = 0
            taps[#taps + 1] = program:install_read_tap(address, address + 31,
                "main48 direct frame " .. key, function(offset, data, mask)
                    direct48_counts[key] = direct48_counts[key] + 1
                    if direct48_counts[key] <= 4 then
                        print(string.format("MK2KS_ANIM_DIRECT48_READ frame=%d key=%s at=%08X data=%08X pc=%08X",
                            frame, key, offset, data, cpu.state.PC.value))
                    end
                end)
        end
    end
end)

emu.register_stop(function()
    local total = 0
    for _, entry in ipairs(entries) do
        for _, id in ipairs(entry[4]) do
            local key = entry[1] .. ":" .. entry[2] .. ":" .. id
            local count = counts[key] or 0
            total = total + count
            print(string.format("MK2KS_ANIM_AUDIT_ENTRY key=%s reads=%d first=%d last=%d",
                key, count, first_frames[key] or -1, last_frames[key] or -1))
        end
    end
    print(string.format("MK2KS_ANIM_AUDIT_RESULT frames=%d total_reads=%d", frame, total))
    for _, key in ipairs({"sonya:main:48:direct1", "sonya:main:48:direct2"}) do
        if direct48_counts[key] then
            print(string.format("MK2KS_ANIM_DIRECT48_RESULT key=%s reads=%d", key, direct48_counts[key]))
        end
    end
    for _, tap in ipairs(taps) do tap:remove() end
end)
