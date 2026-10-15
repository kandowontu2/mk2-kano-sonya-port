local p=manager.machine.devices[':maincpu'].spaces.program
local frame=0
emu.register_frame_done(function()
 frame=frame+1;if frame~=3 then return end
 for i=0,40 do print(string.format('MK2_PHOTO_ROW index=%d value=%08X writes=0 assistance=none',i,p:read_u32(0xfffa4800+i*32)))end
 print(string.format('MK2_PHOTO_OPERAND value=%08X writes=0 assistance=none',p:read_u32(0xff8447b0)))
 manager.machine:exit()
end)
