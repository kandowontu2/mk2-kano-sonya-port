-- Native BATTLE lookup provenance plus ordinary-input selector/combat checks.
dofile("mk2ks_battle_card_probe.lua")
local frame,checks,errors,combat_fields=0,0,0,0
local taps,reads,expected={},{},{}
local program=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"]
local names={kung_lao=0,liu_kang=1,cage=2,baraka=3,kitana=4,mileena=5,raiden=7,reptile=9,
    sub_zero=8,scorpion=10,jax=11,kano=17,sonya=18}
local ids={assert(names[os.getenv("MK2KS_TEST_FIGHTER")]),assert(names[os.getenv("MK2KS_P2_FIGHTER")])}
local function check(ok,label)
    checks=checks+1
    if not ok then errors=errors+1;print("MK2KS_BATTLE_NATIVE_ERROR "..label) end
end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local base=program:read_u32(0xff8a2250)
        check(base==0xfffa4300 and program:read_u32(0xff8a2380)==base,"native lookup operands")
        for _,id in ipairs(ids) do
            if not expected[id] then
                local at=base+id*32
                expected[id]=program:read_u32(at);reads[id]=0
                if id>=17 then
                    local p=expected[id]
                    check(p>=0x07200000 and p<0x07280000 and program:read_u16(p)==138 and
                        program:read_u16(p+16)==158 and program:read_u16(p+48)==256,"original-photo header "..id)
                else check(expected[id]==program:read_u32(0xff8f48f0+id*32),"stock pointer "..id) end
                taps[#taps+1]=program:install_read_tap(at,at+31,"actual native BATTLE lookup "..id,
                    function(offset,data,mask)
                        local pc=cpu.state.PC.value
                        if offset==at and pc>=0xff8a1c00 and pc<0xff8a2500 then
                            reads[id]=reads[id]+1
                            check((data&0xffff)==(expected[id]&0xffff) and (mask&0xffff)==0xffff,"native picture entry "..id)
                            print(string.format("MK2KS_BATTLE_NATIVE_LOOKUP frame=%d id=%d pc=%08X pointer=%08X roster=%d,%d",
                                frame,id,pc,expected[id],program:read_u16(0x01060280),program:read_u16(0x01060e50)))
                        end
                    end)
            end
        end
    end
    if frame>=1400 then
        local a1,a2=program:read_u32(0x01060220),program:read_u32(0x01060df0)
        local live=a1>=0x01000000 and a1<0x01100000 and a2>=0x01000000 and a2<0x01100000
        check(live and program:read_u16(0x010601f0)==1 and program:read_u16(0x01060dc0)==1 and
            program:read_u16(0x01060280)==ids[1] and program:read_u16(0x01060e50)==ids[2] and
            program:read_u16(a1+0x1f0)==ids[1] and program:read_u16(a2+0x1f0)==ids[2] and
            program:read_u16(0x010602f0)>0 and program:read_u16(0x01060ec0)>0,"both live owned combat actors")
        combat_fields=combat_fields+1
    end
end)
emu.register_stop(function()
    for _,id in ipairs(ids) do check(reads[id]>=(ids[1]==ids[2] and 2 or 1),"both owned native lookups "..id) end
    check(combat_fields>=500,"live combat coverage after card")
    print(string.format("MK2KS_BATTLE_NATIVE_RESULT pass=%s checks=%d errors=%d ids=%d,%d reads=%d,%d combat_fields=%d writes=0",
        tostring(errors==0 and checks>=500),checks,errors,ids[1],ids[2],reads[ids[1]],reads[ids[2]],combat_fields))
    for _,tap in ipairs(taps) do tap:remove() end
end)
