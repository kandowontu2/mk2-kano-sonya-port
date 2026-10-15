-- Read-only ROM search for native ending prose and its surrounding records.
local done=false
emu.register_frame(function()
    if done then return end
    done=true
    local program=manager.machine.devices[":maincpu"].spaces.program
    local targets={"WHEN SUB-ZERO","SUB-ZERO","SHAO KAHN'S RULE","WHERE IS SONYA"}
    local counts={0,0,0,0}
    for offset=0,0xfffff do
        local first=program:read_u8(0xff800000+offset*8)
        for index,target in ipairs(targets) do
            if first==target:byte(1) and counts[index]<20 then
                local matches=true
                for n=2,#target do
                    if program:read_u8(0xff800000+(offset+n-1)*8)~=target:byte(n) then
                        matches=false
                        break
                    end
                end
                if matches then
                    counts[index]=counts[index]+1
                    print(string.format("MK2KS_END_STRING text=%s address=%08X offset=%05X",
                        target,0xff800000+offset*8,offset))
                end
            end
        end
    end
    print(string.format("MK2KS_END_STRING_COUNTS %d,%d,%d,%d",table.unpack(counts)))
    for offset=0,0xffffc,2 do
        local value=program:read_u32(0xff800000+offset*8)
        if value>=0xff8fe000 and value<0xff8ff000 then
            print(string.format("MK2KS_END_POINTER from=%08X to=%08X",0xff800000+offset*8,value))
        end
        if value>=0xff8f5700 and value<0xff8f5d00 then
            print(string.format("MK2KS_END_TABLE_REF from=%08X to=%08X",0xff800000+offset*8,value))
        end
        if value>=0xff8f5200 and value<0xff8f5700 then
            print(string.format("MK2KS_END_DISPATCH_REF from=%08X to=%08X",0xff800000+offset*8,value))
        end
    end
    for at=0xff8f5600,0xff8f5d00-0x20,0x20 do
        local value=program:read_u32(at)
        print(string.format("MK2KS_END_TABLE address=%08X value=%08X",at,value))
    end
    for at=0xff8f53d0,0xff8f59f0,0x20 do
        local value=program:read_u32(at)
        if value>=0xff800000 and value<0xffa00000 then
            local chars={}
            for n=0,27 do
                local byte=program:read_u8(value+0xc0+n*8)
                chars[#chars+1]=(byte>=32 and byte<=126) and string.char(byte) or "."
            end
            print(string.format("MK2KS_END_ENTRY slot=%08X target=%08X text=%s",at,value,table.concat(chars)))
        end
    end
    for page=0,1 do
        local base=page==0 and 0xff8f5550 or 0xff8f59d0
        for segment=0,2 do
            local slot=base+(8*3+segment)*0x20
            print(string.format("MK2KS_END_TEMPLATE page=%d segment=%d slot=%08X pointer=%08X",
                page,segment,slot,program:read_u32(slot)))
        end
    end
    for id=0,11 do
        local slot=0xff8f59d0+(id*3+2)*0x20
        print(string.format("MK2KS_END_SECOND_THIRD id=%d pointer=%08X",id,program:read_u32(slot)))
    end
    for index=0,55 do
        print(string.format("MK2KS_END_IMAGE_ENTRY index=%d address=%08X value=%08X",index,
            0xff8f48f0+index*0x20,program:read_u32(0xff8f48f0+index*0x20)))
    end
    local gfx=manager.machine.memory.regions[":gfxrom"]
    for _,index in ipairs({16,17,32,33,38,39}) do
        local address=program:read_u32(0xff8f48f0+index*0x20)
        local bytes={}
        for n=0,47 do bytes[#bytes+1]=string.format("%02X",gfx:read_u8(address/8+n)) end
        print(string.format("MK2KS_END_IMAGE_DUMP index=%d bit=%08X %s",index,address,
            table.concat(bytes," ")))
        print(string.format("MK2KS_END_IMAGE_MAPPED index=%d words=%04X,%04X,%04X,%04X",
            index,program:read_u16(address),program:read_u16(address+16),
            program:read_u16(address+32),program:read_u16(address+48)))
        local words={}
        for n=4,27 do words[#words+1]=string.format("%04X",program:read_u16(address+n*16)) end
        print(string.format("MK2KS_END_IMAGE_MAPPED_BODY index=%d %s",index,table.concat(words," ")))
    end
    for offset=0x1fd00,0x1ff00,32 do
        local bytes,chars={},{}
        for n=0,31 do
            local byte=program:read_u8(0xff800000+(offset+n)*8)
            bytes[#bytes+1]=string.format("%02X",byte)
            chars[#chars+1]=(byte>=32 and byte<=126) and string.char(byte) or "."
        end
        print(string.format("MK2KS_END_DUMP %08X %s %s",0xff800000+offset*8,
            table.concat(bytes," "),table.concat(chars)))
    end
end)
