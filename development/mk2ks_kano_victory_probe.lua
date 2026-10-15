-- Read-only ABI check at the native victory dispatcher and its shared join.
dofile("mk2ks_finish_state_trace.lua")
local program=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local debugger=assert(manager.machine.debugger)
debugger.visible_cpu=manager.machine.devices[":maincpu"]
debugger:command("dasm audit_v259_victory_handoff.asm,FFA14860,2000")
debugger.execution_state="run"
local taps,reads={},0
for _,entry in ipairs({0xffa154d0,0xffa162d0}) do
    taps[#taps+1]=program:install_read_tap(entry,entry+15,"native winner ABI",function(offset)
        if offset~=entry or reads>=12 then return end
        local own,task=cpu.A8.value,cpu.A13.value
        if own<0x01000000 or own>=0x01100000 or task<0x01000000 or task>=0x01100000 then return end
        reads=reads+1
        local child=program:read_u32(task+0x190)
        local child_pose=child>=0x01000000 and child<0x01100000 and program:read_u32(child+0x1d0) or 0
        print(string.format("MK2_KANO_WINNER_ABI entry=%08X id=%d own=%08X pose=%08X task=%08X child=%08X child_pose=%08X",
            entry,program:read_u16(own+0x1f0),own,program:read_u32(own+0x1d0),task,child,child_pose))
    end)
end
emu.register_stop(function()
    print(string.format("MK2_KANO_WINNER_ABI_RESULT reads=%d",reads))
    for _,tap in ipairs(taps) do tap:remove() end
end)
