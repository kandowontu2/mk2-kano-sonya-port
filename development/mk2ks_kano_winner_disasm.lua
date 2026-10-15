-- Read-only verification of the loaded winner table and guarded callback.
local debugger=assert(manager.machine.debugger)
debugger.visible_cpu=manager.machine.devices[":maincpu"]
debugger:command("dasm audit_v260_kano_winner_hold.asm,FFFBCA00,400")
local program=manager.machine.devices[":maincpu"].spaces.program
print(string.format("MK2_KANO_WINNER_TABLE kano=%08X sonya=%08X operand=%08X",
    program:read_u32(0xff800000+0xfe680*8+17*32),
    program:read_u32(0xff800000+0xfe680*8+18*32),program:read_u32(0xffa14920)))
debugger.execution_state="run"
