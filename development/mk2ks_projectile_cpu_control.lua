-- Differential cold P1-versus-native-CPU control. Inputs only; NOT restart proof.
assert(os.getenv("MK2KS_TWO_PLAYER")=="0")
assert(os.getenv("MK2KS_TEST_FIGHTER")=="kano")
dofile("mk2ks_selector_exit_test.lua")
local projectile=dofile("mk2ks_restart_projectile.lua")("kano",1)
local p=manager.machine.devices[":maincpu"].spaces.program
local frame,match,finished=0,nil,false
local high,low=manager.machine.ioport.ports[":IN0"].fields,manager.machine.ioport.ports[":IN2"].fields
local fields={}
for key,label in pairs({up="Up",down="Down",left="Left",right="Right",hp="High Punch",block="Block"}) do fields[key]=high["P1 "..label] end
fields.lp=low["P1 Low Punch"]
emu.register_frame(function()
    frame=frame+1
    local actor=p:read_u32(0x01060220)
    if not match and p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and
        p:read_u16(0x01060280)==17 and actor>=0x01000000 and actor<0x01100000 and
        p:read_u16(actor+0x1f0)==17 and p:read_u16(0x010602f0)==161 then
        match=frame
        print(string.format("MK2_COLD_CPU_MATCH frame=%d target=kano side=1 cpu=%d cpu_state=%d scope=cold_native_cpu_not_restart writes=0",
            frame,p:read_u16(0x01060e50),p:read_u16(0x01060dc0)))
    end
    if not match or finished then return end
    if frame-match>=100 then fields.block:set_value(1) end
    projectile.drive(frame,match,fields)
    if frame-match==600 then
        finished=true
        print("MK2_COLD_CPU_RESULT pass="..tostring(projectile.finish()).." scope=cold_native_cpu_not_restart")
        manager.machine:exit()
    end
end)
