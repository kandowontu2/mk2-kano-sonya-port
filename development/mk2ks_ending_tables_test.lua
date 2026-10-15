-- Read-only verification of the v60 native story tables and scripts.
local done=false
emu.register_frame(function()
    if done then return end
    done=true
    local program=manager.machine.devices[":maincpu"].spaces.program
    local source={0xff8f5550,0xff8f59d0}
    local operand={0xff8f51c0,0xff8f53e0}
    local expected={0xfffa5000,0xfffa5800}
    local checks,errors=0,0
    local function check(ok,label)
        checks=checks+1
        if not ok then errors=errors+1;print("MK2KS_ENDING_TEXT_ERROR "..label) end
    end
    for page=1,2 do
        local table=program:read_u32(operand[page])
        check(table==expected[page],"relocated page "..page)
        for id=0,11 do
            for segment=0,2 do
                local slot=(id*3+segment)*0x20
                check(program:read_u32(table+slot)==program:read_u32(source[page]+slot),
                    string.format("stock page=%d id=%d segment=%d",page,id,segment))
            end
        end
        for fighter=0,1 do
            for segment=0,(page==1 and 2 or 1) do
                local slot=((17+fighter)*3+segment)*0x20
                local script=program:read_u32(table+slot)
                local expected_script=0xff800000+(0xf4c00+(fighter*5+(page==1 and 0 or 3)+segment)*0xc0)*8
                check(script==expected_script,string.format("script pointer page=%d fighter=%d segment=%d",page,fighter,segment))
                local template=program:read_u32(source[page]+(8*3+segment)*0x20)
                for byte=0,23 do
                    check(program:read_u8(script+byte*8)==program:read_u8(template+byte*8),
                        string.format("native layout page=%d fighter=%d segment=%d byte=%d",page,fighter,segment,byte))
                end
                local count,has_newline=0,false
                while count<168 do
                    local char=program:read_u8(script+(24+count)*8)
                    if char==0 then break end
                    if char==string.byte("\\") then has_newline=true end
                    check(char>=32 and char<=126,"printable story text")
                    count=count+1
                end
                check(count>20 and count<168 and has_newline,"native story text length and line breaks")
            end
            if page==2 then
                check(program:read_u32(table+((17+fighter)*3+2)*0x20)==0,
                    "native second-page terminator")
            end
        end
    end
    print(string.format("MK2KS_ENDING_TEXT_RESULT pass=%s checks=%d errors=%d",
        tostring(errors==0),checks,errors))
    assert(errors==0,"Native ending text table verification failed")
end)
