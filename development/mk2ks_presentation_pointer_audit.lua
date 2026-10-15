-- Read-only scan of MKII's current program image for old presentation
-- table literals. It runs once after native ROM initialization.
local targets = {
    [0xff8f48f0] = "stock_full_picture_table",
    [0xff894c00] = "stock_select_portraits",
    [0xff8a0e70] = "stock_ladder_portraits",
    [0xff8f5550] = "stock_ending_text_page1",
    [0xff8f59d0] = "stock_ending_text_page2",
    [0xffa14980] = "stock_victory_animation",
}
local ran = false
emu.register_frame(function()
    if ran then return end
    ran = true
    local program = manager.machine.devices[":maincpu"].spaces.program
    local counts = {}
    for at = 0, 0xffffc, 2 do
        local value = program:read_u32(0xff800000 + at * 8)
        local name = targets[value]
        if name then
            counts[name] = (counts[name] or 0) + 1
            print(string.format("MK2KS_PRESENTATION_POINTER name=%s at=%08X offset=%05X value=%08X",
                name, 0xff800000 + at * 8, at, value))
        end
    end
    local is_port = manager.machine.system.name == "mk2ks"
    local passed = true
    for _, name in pairs(targets) do
        local expected = is_port and 0 or (name == "stock_full_picture_table" and 3 or 1)
        if (counts[name] or 0) ~= expected then passed = false end
        print(string.format("MK2KS_PRESENTATION_POINTER_COUNT name=%s count=%d",
            name, counts[name] or 0))
    end
    print(string.format("MK2KS_PRESENTATION_POINTER_RESULT pass=%s game=%s",
        tostring(passed), manager.machine.system.name))
end)
