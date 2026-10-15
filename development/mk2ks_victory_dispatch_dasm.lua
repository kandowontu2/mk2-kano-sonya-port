-- Read-only disassembly of the stock MKII victory callbacks and table.
local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local machine = manager.machine
    local debugger = machine.debugger
    debugger.visible_cpu = machine.devices[":maincpu"]
    debugger:command("dasm audit_v222_victory_dispatch_c100run.asm,FFA14900,1700")
    debugger:command("dasm audit_v222_victory_animation_helper_c100run.asm,FF83B900,900")
    debugger:command("dasm audit_v222_victory_animation_c100.asm,FF83C100,400")
    debugger.execution_state = "run"
    local program = machine.devices[":maincpu"].spaces.program
    local table = 0xff800000 + 0xfe680 * 8
    for id = 0, 18 do
        print(string.format("MK2_VICTORY_TABLE id=%d callback=%08X",
            id, program:read_u32(table + id * 0x20)))
    end
end)
