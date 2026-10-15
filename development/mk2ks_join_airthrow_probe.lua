-- Cold native join diagnosis. Never accepted as a post-ending restart.
assert(os.getenv("MK2KS_TWO_PLAYER")~="1")
local side=tonumber(os.getenv("MK2KS_AIR_JOIN_SIDE") or "1")
assert(side==1,"Cold join probe starts an ordinary P1 Kano game")
dofile("mk2ks_selector_exit_test.lua")
local air=dofile("mk2ks_restart_airthrow.lua")(side,os.getenv("MK2KS_AIR_JOIN_VICTIM"))
local p=manager.machine.devices[":maincpu"].spaces.program
local frame,match,started=0,nil,false
emu.register_frame(function()
    frame=frame+1
    if not match then
        local actor=p:read_u32(0x01060220)
        if p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and
            p:read_u16(0x01060280)==17 and p:read_u16(0x010602f0)==161 and
            actor>=0x01000000 and actor<0x01100000 and p:read_u16(actor+0x1f0)==17 then
            match=frame;print("MK2_AIR_COLD_MATCH frame="..frame.." scope=cold_diagnosis_not_post_ending")
        end
    end
    if match and not started and frame-match==600 then started=true;air.begin(frame) end
    if started then air.drive(frame)
    elseif match and frame-match>=100 then manager.machine.ioport.ports[":IN0"].fields["P1 Block"]:set_value(1) end
end)
