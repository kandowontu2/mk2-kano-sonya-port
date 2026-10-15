local p=manager.machine.devices[":maincpu"].spaces.program
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if frame~=3 then return end
 for i=0,18 do print(string.format('MK2_DISPATCH_ROW table=decision index=%d value=%08X writes=0 assistance=none',i,p:read_u32(0xfffa2000+i*32)))end
 for i=0,18 do print(string.format('MK2_DISPATCH_ROW table=round index=%d value=%08X writes=0 assistance=none',i,p:read_u32(0xfffa2800+i*32)))end
 for i=0,23 do print(string.format('MK2_DISPATCH_ROW table=followup index=%d value=%08X writes=0 assistance=none',i,p:read_u32(0xfffa4000+i*32)))end
 for i=0,23 do print(string.format('MK2_DISPATCH_ROW table=special index=%d value=%08X writes=0 assistance=none',i,p:read_u32(0xfffa2400+i*32)))end
 for i=0,18 do print(string.format('MK2_DISPATCH_ROW table=reaction index=%d value=%08X writes=0 assistance=none',i,p:read_u32(0xfffe4800+i*32)))end
 print(string.format('MK2_DISPATCH_OPERAND at=FF9B1D60 value=%08X writes=0 assistance=none',p:read_u32(0xff9b1d60)))
 print(string.format('MK2_DISPATCH_OPERAND at=FF9B21C0 value=%08X writes=0 assistance=none',p:read_u32(0xff9b21c0)))
 print(string.format('MK2_DISPATCH_OPERAND at=FF9B7680 value=%08X writes=0 assistance=none',p:read_u32(0xff9b7680)))
 print(string.format('MK2_DISPATCH_OPERAND at=FF8A5920 value=%08X writes=0 assistance=none',p:read_u32(0xff8a5920)))
 print(string.format('MK2_DISPATCH_OPERAND at=FF835DE0 value=%08X writes=0 assistance=none',p:read_u32(0xff835de0)))
 for i=0,4 do print(string.format('MK2_DISPATCH_FALLBACK index=%d value=%04X writes=0 assistance=none',i,p:read_u16(0xfffbc700+i*16)))end
 manager.machine:exit()
end)
