-- Read-only full-pixel verification against an independent original-ROM oracle.
-- Oracle bytes: header, 256 exact xRGB555 colors, top-down pixel indices.
local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local program = manager.machine.devices[":maincpu"].spaces.program
    local pictures = program:read_u32(0xff8447b0)
    local checks, errors = 0, 0
    local function check(ok,label)
        checks=checks+1
        if not ok then
            errors=errors+1
            if errors<20 then print("MK2KS_ENDING_PICTURE_ERROR "..label) end
        end
    end
    check(pictures==0xfffa4800,"relocated picture table")
    for index=0,39 do
        check(program:read_u32(pictures+index*32)==program:read_u32(0xff8f48f0+index*32),
              "preserved stock picture "..index)
    end
    for index=40,49 do check(program:read_u32(pictures+index*32)==0,"unused entry "..index) end
    local stock=program:read_u32(pictures+32*32)
    local stock_stream=stock+(4+program:read_u16(stock+48))*16
    local folder=assert(os.getenv("MK2KS_ENDING_PICTURE_REFERENCE"),"Set original-ROM oracle directory")
    local prior=0
    local function bit(address)
        return (program:read_u16(address&0xfffffff0)>>(address&15))&1
    end
    for fighter,name in ipairs({"kano","sonya"}) do
        for page=0,1 do
            local file=assert(io.open(folder.."/"..name.."_page_"..(page+1)..".bin","rb"))
            local reference=file:read("a");file:close()
            local width,height,frames,colors=string.unpack("<I2I2I2I2",reference)
            check(width==(page==0 and 124 or 280) and height==(page==0 and 163 or 119) and
                  frames==1 and colors==256,"independent oracle header")
            check(#reference==8+colors*2+width*height,"independent oracle size")
            local index=50+(fighter-1)*2+page
            local pointer=program:read_u32(pictures+index*32)
            check(pointer>=0x07100000 and pointer<0x07200000 and pointer>prior,"picture pointer "..index)
            prior=pointer
            for byte=0,8+colors*2-1 do
                check(program:read_u8(pointer+byte*8)==reference:byte(byte+1),
                      "original palette/header picture="..index.." byte="..byte)
            end
            local stream=pointer+(4+colors)*16
            for byte=0,24 do
                check(program:read_u8(stream+byte*8)==program:read_u8(stock_stream+byte*8),
                      "native codebook picture="..index.." byte="..byte)
            end
            local first=stream+25*8
            for y=0,height-1 do
                for x=0,width-1 do
                    local pixel=first+(y*width+x)*9
                    check(bit(pixel)==1,"native literal marker picture="..index)
                    local actual=0
                    for b=0,7 do actual=actual|(bit(pixel+1+b)<<b) end
                    local expected=reference:byte(8+colors*2+(height-1-y)*width+x+1)
                    check(actual==expected,"original photo pixel picture="..index.." x="..x.." y="..y)
                end
            end
            print("MK2KS_ENDING_PHOTO_ORIGINAL picture="..index.." pixels="..width*height.." errors="..errors)
        end
    end
    print(string.format("MK2KS_ENDING_PICTURE_RESULT pass=%s checks=%d errors=%d",tostring(errors==0),checks,errors))
    assert(errors==0,"Native ending original-photo verification failed")
end)
