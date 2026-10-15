-- Diagnostic-only renderer for the native slideshow picture records.
local done=false
emu.register_frame(function()
    if done then return end
    done=true
    local program=manager.machine.devices[":maincpu"].spaces.program
    for _,index in ipairs({32,33}) do
        local address=program:read_u32(0xff8f48f0+index*0x20)
        local width,height=program:read_u16(address),program:read_u16(address+16)
        local colors=program:read_u16(address+48)
        assert(width>0 and height>0 and width*height<100000 and colors<=255)
        local palette={}
        for entry=0,colors do
            local rgb=program:read_u16(address+(8+entry*2)*8)
            palette[entry]=string.char(((rgb>>10)&31)*255//31,
                ((rgb>>5)&31)*255//31,(rgb&31)*255//31)
        end
        local start=address+(8+(colors+1)*2)*8
        local output=assert(io.open(string.format("diagnostic_v59_ending_image_%d.ppm",index),"wb"))
        output:write(string.format("P6\n%d %d\n255\n",width,height))
        for y=0,height-1 do
            for x=0,width-1 do
                local pixel=program:read_u8(start+(y*width+x)*8)
                output:write(palette[pixel] or "\0\0\0")
            end
        end
        output:close()
        print(string.format("MK2KS_END_DECODE index=%d address=%08X width=%d height=%d colors=%d",
            index,address,width,height,colors))
    end
end)
