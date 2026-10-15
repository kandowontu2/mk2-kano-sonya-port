-- Read-only native command and victim-animation reference discovery.
local debugger=assert(manager.machine.debugger)
debugger.visible_cpu=manager.machine.devices[":maincpu"]
local program=manager.machine.devices[":maincpu"].spaces.program
for _,row in ipairs({{"up",0xff040},{"hp",0xff180},{"lp",0xff1d0},{"block",0xff220},{"hk",0xff270}}) do
    local pointer=program:read_u32(0xff800000+row[2]*8+2*32)
    print(string.format("MK2_NATIVE_CAGE_COMMAND row=%s address=%08X",row[1],pointer))
    if pointer>=0xff800000 then
        debugger:command(string.format("dasm audit_v262_cage_%s.asm,%08X,1400",row[1],pointer))
    end
end
debugger.execution_state="run"
