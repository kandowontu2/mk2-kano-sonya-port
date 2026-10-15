-- Read-only complete original-photo pixel oracle for native BATTLE records.
local done=false
emu.register_frame(function()
    if done then return end
    done=true
    local program=manager.machine.devices[":maincpu"].spaces.program
    local pictures=program:read_u32(0xff8a2250)
    local checks,errors=0,0
    local function check(ok,label)
        checks=checks+1
        if not ok then errors=errors+1;if errors<20 then print("MK2KS_BATTLE_PICTURE_ERROR "..label) end end
    end
    check(pictures==0xfffa4300 and program:read_u32(0xff8a2380)==pictures,"both native lookup operands")
    for id=0,16 do
        check(program:read_u32(pictures+id*32)==program:read_u32(0xff8f48f0+id*32),"preserved stock "..id)
    end
    local stock=program:read_u32(0xff8f48f0+32*32)
    local stock_stream=stock+(4+program:read_u16(stock+48))*16
    local folder=assert(os.getenv("MK2KS_ENDING_PICTURE_REFERENCE"),"Set original-ROM oracle directory")
    local prior_end=0x07200000
    local function bit(address)
        return (program:read_u16(address&0xfffffff0)>>(address&15))&1
    end
    for fighter,name in ipairs({"kano","sonya"}) do
        local file=assert(io.open(folder.."/"..name.."_battle.bin","rb"))
        local reference=file:read("a");file:close()
        local width,height,frames,colors=string.unpack("<I2I2I2I2",reference)
        check(width==138 and height==158 and frames==1 and colors==256,"oracle header")
        check(#reference==8+colors*2+width*height,"oracle size")
        local id=16+fighter
        local pointer=program:read_u32(pictures+id*32)
        check(pointer>=prior_end and pointer<0x07280000 and pointer%16==0,"independent bounded pointer "..id)
        prior_end=pointer+(8+colors*2+25+(width*height*9+7)//8)*8
        check(prior_end<=0x07280000,"record fits reserved area "..id)
        for byte=0,8+colors*2-1 do
            check(program:read_u8(pointer+byte*8)==reference:byte(byte+1),"palette/header "..id..":"..byte)
        end
        local stream=pointer+(4+colors)*16
        for byte=0,24 do
            check(program:read_u8(stream+byte*8)==program:read_u8(stock_stream+byte*8),"codebook "..id..":"..byte)
        end
        local first=stream+25*8
        for y=0,height-1 do
            for x=0,width-1 do
                local at=first+(y*width+x)*9
                check(bit(at)==1,"native literal marker "..id)
                local actual=0
                for b=0,7 do actual=actual|(bit(at+1+b)<<b) end
                check(actual==reference:byte(8+colors*2+(height-1-y)*width+x+1),"photo pixel "..id..":"..x..","..y)
            end
        end
        print("MK2KS_BATTLE_PHOTO_ORIGINAL id="..id.." pixels="..width*height.." errors="..errors)
    end
    print(string.format("MK2KS_BATTLE_PICTURE_RESULT pass=%s checks=%d errors=%d",tostring(errors==0),checks,errors))
    assert(errors==0,"Native BATTLE original-photo verification failed")
end)
