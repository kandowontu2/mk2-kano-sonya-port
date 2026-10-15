-- Short, ordinary-input diagnosis only. This is NOT post-ending acceptance.
assert(os.getenv("MK2KS_TWO_PLAYER")~="1","CPU close-pair probe requires one player")
dofile("mk2ks_selector_exit_test.lua")
local target=assert(os.getenv("MK2KS_TEST_FIGHTER"))
local identity=assert(({kano=17,sonya=18})[target])
local pair=dofile("mk2ks_restart_pair.lua")(target,1)
local p=manager.machine.devices[":maincpu"].spaces.program
local frame,match,fields=0,nil,nil
emu.register_frame(function()
    frame=frame+1
    if not fields then
        local high=manager.machine.ioport.ports[":IN0"].fields
        local low=manager.machine.ioport.ports[":IN2"].fields
        fields={left=high["P1 Left"],right=high["P1 Right"],up=high["P1 Up"],down=high["P1 Down"],
            hp=high["P1 High Punch"],lp=low["P1 Low Punch"],hk=high["P1 High Kick"],lk=low["P1 Low Kick"],block=high["P1 Block"]}
    end
    if not match then
        local actor=p:read_u32(0x01060220)
        if p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and
            p:read_u16(0x01060280)==identity and p:read_u16(0x010602f0)==161 and
            actor>=0x01000000 and actor<0x01100000 and p:read_u16(actor+0x1f0)==identity then
            match=frame
            print(string.format("MK2_PAIR_PROBE_MATCH frame=%d target=%s id=%d actor=%08X writes=0 scope=cold_diagnosis_not_restart_acceptance",frame,target,identity,actor))
        end
    end
    if match then
        pair.drive(frame,match,fields)
        if frame-match==600 then
            print("MK2_PAIR_PROBE_RESULT pass="..tostring(pair.finish()).." scope=cold_diagnosis_not_restart_acceptance")
            manager.machine:exit()
        end
    end
end)
