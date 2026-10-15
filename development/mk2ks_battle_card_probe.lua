-- Read-only frame captures spanning the stock two-player BATTLE:1 card.
-- The selector harness supplies ordinary credits, grid movement, and HP.
dofile("mk2ks_selector_exit_test.lua")
local frame = 0
local blit_dir = os.getenv("MK2KS_CARD_BLIT_DIR")
local blit_start = tonumber(os.getenv("MK2KS_CARD_BLIT_START") or "1020")
local blit_end = tonumber(os.getenv("MK2KS_CARD_BLIT_END") or "1080")
local cpu_trace = os.getenv("MK2KS_CARD_CPU_TRACE")
local trace_start = tonumber(os.getenv("MK2KS_CARD_TRACE_START") or "1040")
local trace_end = tonumber(os.getenv("MK2KS_CARD_TRACE_END") or "1053")
local dasm_path = os.getenv("MK2KS_CARD_DASM")
local table_trace = os.getenv("MK2KS_CARD_TABLE_TRACE") == "1"
local free_trace = os.getenv("MK2KS_CARD_FREE_TRACE") == "1"
emu.register_frame(function()
    frame = frame + 1
    if free_trace and frame == 1 then
        local program = manager.machine.devices[":maincpu"].spaces.program
        local first = nil
        for at = 0xf4000, 0xf6000, 2 do
            local free = at < 0xf6000 and program:read_u16(0xff800000 + at * 8) == 0xffff
            if free and not first then first = at end
            if not free and first then
                if at - first >= 0x50 then
                    print(string.format("MK2KS_CARD_FREE_ROM start=%05X end=%05X bytes=%X",
                        first, at, at - first))
                end
                first = nil
            end
        end
    end
    if table_trace and frame == 1 then
        local program = manager.machine.devices[":maincpu"].spaces.program
        for _, id in ipairs({0, 4, 11, 17, 18}) do
            local ptr = program:read_u32(0xff8f48f0 + id * 32)
            print(string.format("MK2KS_CARD_STOCK_TABLE id=%d ptr=%08X width=%d height=%d",
                id, ptr, program:read_u16(ptr), program:read_u16(ptr + 16)))
        end
        for _, id in ipairs({50, 52}) do
            local ptr = program:read_u32(0xfffa4800 + id * 32)
            print(string.format("MK2KS_CARD_NATIVE_ENDING_TABLE index=%d ptr=%08X width=%d height=%d",
                id, ptr, program:read_u16(ptr), program:read_u16(ptr + 16)))
        end
        if program:read_u32(0xfffa4300) ~= 0xffffffff then
            for _, id in ipairs({0, 4, 11, 17, 18}) do
                local ptr = program:read_u32(0xfffa4300 + id * 32)
                print(string.format("MK2KS_CARD_NATIVE_BATTLE_TABLE id=%d ptr=%08X width=%d height=%d",
                    id, ptr, program:read_u16(ptr), program:read_u16(ptr + 16)))
            end
        end
    end
    if dasm_path and frame == 1 then
        assert(manager.machine.debugger, "Card disassembly requires -debug")
        manager.machine.debugger:command("dasm " .. dasm_path .. ",FF8A1C00,A00")
    end
    if cpu_trace and frame == trace_start then
        assert(manager.machine.debugger, "Card CPU trace requires -debug")
        manager.machine.debugger:command("trace " .. cpu_trace .. ",maincpu")
        print("MK2KS_CARD_TRACE_ON " .. cpu_trace)
    elseif cpu_trace and frame == trace_end then
        manager.machine.debugger:command("trace off,maincpu")
        print("MK2KS_CARD_TRACE_OFF")
    end
    if blit_dir and frame == blit_start then
        assert(manager.machine.debugger, "Card blit capture requires -debug")
        manager.machine.debugger:command("midblit pngdma,1," .. blit_dir .. ",1")
        print("MK2KS_CARD_BLIT_ON " .. blit_dir)
    elseif blit_dir and frame == blit_end then
        manager.machine.debugger:command("midblit pngdma,0")
        print("MK2KS_CARD_BLIT_OFF")
    end
    if frame >= 1040 and frame <= 1220 and frame % 10 == 0 then
        manager.machine.screens[":screen"]:snapshot(
            string.format("battle_card_frame%04d.png", frame))
    end
end)
