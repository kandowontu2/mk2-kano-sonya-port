-- Observe native requests in their actual actor/Main context, no guest writes.
dofile('mk2ks_human_special_audio_v1397.lua')
local cpu=manager.machine.devices[':maincpu'];local p=cpu.spaces.program
local frame,taps=0,{}
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local file=assert(io.open(assert(os.getenv('MK2KS_AUDIO_OUTPUT'))..'/guest_maincpu.bin','wb'))
  for block=0,63 do
   local words={};for i=0,4095 do words[#words+1]=string.pack('<I4',p:read_u32(0xff800000+(block*4096+i)*32))end
   file:write(table.concat(words))
  end
  file:close()
  for _,entry in ipairs({0xffa11d30,0xffa11ea0,0xffa11fd0})do
   taps[#taps+1]=p:install_read_tap(entry,entry+15,'native grab audio actual actor',function(at)
    if cpu.state.PC.value~=entry+16 then return end
    local a,m=cpu.state.A8.value,cpu.state.A13.value
    if a<0x01000000 or a>=0x01100000 or m<0x01000000 or m>=0x01100000 then return end
    print(string.format('MK2_GRAB_AUDIO_REQUEST frame=%d entry=%08X pc=%08X actor=%08X main=%08X owner=%08X id=%d p1=%08X p2=%08X p1main=%08X p2main=%08X writes=0 assistance=none',frame,entry,cpu.state.PC.value,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u32(0x01060220),p:read_u32(0x01060df0),p:read_u32(0x01060260),p:read_u32(0x01060e30)))
   end)
  end
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
