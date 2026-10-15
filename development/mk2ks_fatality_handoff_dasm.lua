-- Read-only MKII fatality victim-handoff disassembly.
local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local debugger = manager.machine.debugger
    debugger.visible_cpu = manager.machine.devices[":maincpu"]
    for _, segment in ipairs({
        {"victim_process", 0xff838e00, 0xb00},
        {"actor_task_handoff", 0xff841f00, 0xf00},
        {"victim_setup", 0xff839f00, 0xe00},
        {"dragon_victim", 0xff8b7b00, 0x900},
        {"stock_death", 0xff841d00, 0x900},
        {"stock_fatality_text", 0xff8ca600, 0x900},
        {"palette_loader", 0xff906000, 0x1800},
        {"palette_copy", 0xff83f900, 0xb00},
        {"palette_alloc", 0xff80cc00, 0xa00},
        {"palette_blit", 0xff80c600, 0x600},
        {"object_create", 0xff83a900, 0x1000},
        {"object_attach", 0xff83e500, 0xe00},
        {"object_free", 0xff83ed00, 0xa00},
        {"object_actor_init", 0xff838c00, 0x500},
        {"object_animation", 0xff83c100, 0x1200},
        {"object_pose", 0xff840900, 0x600},
        {"object_graphic", 0xff809c00, 0x700},
        {"group_engine", 0xff83b900, 0xb00},
        {"group_draw", 0xff838600, 0x500},
        {"group_spawn_caller", 0xff9dee00, 0x900},
        {"kano_group_cleanup", 0xfffaf100, 0x500},
        {"group_free", 0xff840400, 0x500},
        {"group_attach", 0xff840f00, 0x500},
        {"palette_release", 0xff80c900, 0x500},
        {"palette_release_deep", 0xff80d580, 0x500},
        {"object_list_release", 0xff809500, 0x500},
        {"failure_trap", 0xffa1e700, 0x300},
    }) do
        debugger:command(string.format("dasm diagnostic_v94d_%s.asm,%08X,%X",
            segment[1], segment[2], segment[3]))
    end
    debugger.execution_state = "run"
end)
