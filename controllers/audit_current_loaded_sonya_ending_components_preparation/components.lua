local p=manager.machine.devices[":maincpu"].spaces.program
local frame=0
local function hexbytes(at,count)local s={} for i=0,count-1 do local a=at+i*8;local w=p:read_u16(a&~15);s[#s+1]=string.format("%02X",(w>>(a&8))&255)end return table.concat(s)end
emu.register_frame_done(function()
 frame=frame+1
 if frame~=3 then return end
 local q=p:read_u32(0xfffa56c0);print(string.format('MK2_ENDING_TEXT page=1 segment=0 pointer=%08X header=%s text=%s writes=0 assistance=none',q,hexbytes(q,24),hexbytes(q+192,53)))
 local q=p:read_u32(0xfffa56e0);print(string.format('MK2_ENDING_TEXT page=1 segment=1 pointer=%08X header=%s text=%s writes=0 assistance=none',q,hexbytes(q,24),hexbytes(q+192,56)))
 local q=p:read_u32(0xfffa5700);print(string.format('MK2_ENDING_TEXT page=1 segment=2 pointer=%08X header=%s text=%s writes=0 assistance=none',q,hexbytes(q,24),hexbytes(q+192,59)))
 local q=p:read_u32(0xfffa5ec0);print(string.format('MK2_ENDING_TEXT page=2 segment=0 pointer=%08X header=%s text=%s writes=0 assistance=none',q,hexbytes(q,24),hexbytes(q+192,70)))
 local q=p:read_u32(0xfffa5ee0);print(string.format('MK2_ENDING_TEXT page=2 segment=1 pointer=%08X header=%s text=%s writes=0 assistance=none',q,hexbytes(q,24),hexbytes(q+192,114)))
 local q=p:read_u32(0xfffa4e80);print(string.format('MK2_ENDING_PICTURE index=52 pointer=%08X width=%d height=%d planes=%d palette=%d writes=0 assistance=none',q,p:read_u16(q),p:read_u16(q+16),p:read_u16(q+32),p:read_u16(q+48)))
 local q=p:read_u32(0xfffa4ea0);print(string.format('MK2_ENDING_PICTURE index=53 pointer=%08X width=%d height=%d planes=%d palette=%d writes=0 assistance=none',q,p:read_u16(q),p:read_u16(q+16),p:read_u16(q+32),p:read_u16(q+48)))
 print(string.format('MK2_ENDING_OPERAND at=FF8F51C0 value=%08X writes=0 assistance=none',p:read_u32(0xff8f51c0)))
 print(string.format('MK2_ENDING_OPERAND at=FF8F53E0 value=%08X writes=0 assistance=none',p:read_u32(0xff8f53e0)))
 print(string.format('MK2_ENDING_OPERAND at=FF8447B0 value=%08X writes=0 assistance=none',p:read_u32(0xff8447b0)))
 print(string.format('MK2_ENDING_CONTINUATION at=FF844700 value=%04X writes=0 assistance=none',p:read_u16(0xff844700)))
 print(string.format('MK2_ENDING_CONTINUATION at=FF8448A0 value=%04X writes=0 assistance=none',p:read_u16(0xff8448a0)))
 print(string.format('MK2_ENDING_CONTINUATION at=FF844720 value=%04X writes=0 assistance=none',p:read_u16(0xff844720)))
 print(string.format('MK2_ENDING_CONTINUATION at=FF844970 value=%04X writes=0 assistance=none',p:read_u16(0xff844970)))
 print(string.format('MK2_ENDING_CONTINUATION at=FF844740 value=%04X writes=0 assistance=none',p:read_u16(0xff844740)))
 print(string.format('MK2_ENDING_CONTINUATION at=FF844AB0 value=%04X writes=0 assistance=none',p:read_u16(0xff844ab0)))
 print(string.format('MK2_ENDING_CONTINUATION at=FF844760 value=%04X writes=0 assistance=none',p:read_u16(0xff844760)))
 print(string.format('MK2_ENDING_CONTINUATION at=FF844B40 value=%04X writes=0 assistance=none',p:read_u16(0xff844b40)))
 print(string.format('MK2_ENDING_NULL at=FFFA5F00 value=%08X writes=0 assistance=none',p:read_u32(0xfffa5f00)))
 print("MK2_ENDING_COMPONENT_DONE fields=3 inputs=0 writes=0 assistance=none")
 manager.machine:exit()
end)
