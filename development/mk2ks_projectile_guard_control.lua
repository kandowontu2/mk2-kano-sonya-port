-- Cold two-human control for the restart driver's identical command timing.
-- This is NOT an ending/restart proof. It writes inputs only.
assert(os.getenv("MK2KS_TWO_PLAYER")=="1")
dofile("mk2ks_selector_exit_test.lua")
local target=assert(os.getenv("MK2KS_CONTROL_TARGET"))
local side=tonumber(os.getenv("MK2KS_CONTROL_SIDE") or "1")
local projectile=dofile("mk2ks_restart_projectile.lua")(target,side)
local identity=target=="kano" and 17 or 18
local frame,match,finished=0,nil,false
local p=manager.machine.devices[":maincpu"].spaces.program
local own=side==1 and {actor=0x01060220,state=0x010601f0,roster=0x01060280,health=0x010602f0} or
    {actor=0x01060df0,state=0x01060dc0,roster=0x01060e50,health=0x01060ec0}
local high,low=manager.machine.ioport.ports[":IN0"].fields,manager.machine.ioport.ports[":IN2"].fields
local fields={}
for key,label in pairs({up="Up",down="Down",left="Left",right="Right",hp="High Punch",block="Block"}) do fields[key]=high["P"..side.." "..label] end
fields.lp=low["P"..side.." Low Punch"]
emu.register_frame(function()
    frame=frame+1
    local actor=p:read_u32(own.actor)
    if not match and p:read_u16(0x010601d0)==2 and p:read_u16(own.state)==1 and p:read_u16(own.roster)==identity and
        actor>=0x01000000 and actor<0x01100000 and p:read_u16(actor+0x1f0)==identity and p:read_u16(own.health)==161 then
        match=frame
        print(string.format("MK2_COLD_GUARD_MATCH frame=%d target=%s side=%d scope=cold_two_human_not_restart writes=0",frame,target,side))
    end
    if not match or finished then return end
    if frame-match>=100 then fields.block:set_value(1) end
    projectile.drive(frame,match,fields)
    if frame-match==600 then
        finished=true
        print("MK2_COLD_GUARD_RESULT pass="..tostring(projectile.finish()).." scope=cold_two_human_not_restart")
        manager.machine:exit()
    end
end)
