-- Cold diagnostic only; never a substitute for completed source endings.
assert(os.getenv("MK2KS_TWO_PLAYER")~="1")
dofile("mk2ks_selector_exit_test.lua")
local target=assert(os.getenv("MK2KS_TEST_FIGHTER"))
local identity=assert(({kano=17,sonya=18})[target])
local life=dofile("mk2ks_restart_lifecycle.lua")(target,1)
local p=manager.machine.devices[":maincpu"].spaces.program
local frame,match,started=0,nil,false
emu.register_frame(function()
    frame=frame+1
    if not match then
        local actor=p:read_u32(0x01060220)
        if p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and
            p:read_u16(0x01060280)==identity and p:read_u16(0x010602f0)==161 and
            actor>=0x01000000 and actor<0x01100000 and p:read_u16(actor+0x1f0)==identity then
            match=frame;print("MK2_LIFE_COLD_MATCH frame="..frame.." scope=cold_diagnosis_not_post_ending")
        end
    end
    if match and not started and frame-match==600 then started=true;life.begin(frame) end
    if started then life.drive(frame)
    elseif match and frame-match>=100 then manager.machine.ioport.ports[":IN0"].fields["P1 Block"]:set_value(1) end
end)
