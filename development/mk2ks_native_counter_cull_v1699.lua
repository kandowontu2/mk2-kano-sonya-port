-- Byte-identical accepted physical campaign inputs; extra native reads only.
-- Observe Kintaro's actual hit descriptors and every human hurt callback so
-- an off-top body cannot be accepted merely because a saved screen is blank.
dofile('mk2ks_natural_campaign_floor_v1698.lua')
local cpu=manager.machine.devices[':maincpu']
local p=cpu.spaces.program
local frame,tap,fields=0,nil,0
assert(os.getenv('MK2KS_TEST_FIGHTER')=='kano' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function context()
 if p:read_u16(0x010601d0)~=2 or p:read_u16(0x01061b30)~=15 then return end
 local a,m=p:read_u32(0x01060220),p:read_u32(0x01060260)
 local b,n=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 if not valid(a)or not valid(m)or not valid(b)or not valid(n)then return end
 if p:read_u16(a+0x1f0)~=17 or p:read_u16(0x01060280)~=17 or p:read_u16(b+0x1f0)~=12 then return end
 return a,m,b,n
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  tap=p:install_read_tap(0xff835440,0xff83544f,'actual original Kintaro counter descriptor',function(at)
   if at~=0xff835440 or cpu.state.PC.value~=0xff835450 then return end
   local a,m,b,n=context();if not a or cpu.state.A8.value~=b or cpu.state.A13.value~=n then return end
   local descriptor=cpu.state.A0.value;if descriptor<0xff800000 then return end
   local words={};for i=0,8 do words[#words+1]=string.format('%04X',p:read_u16(descriptor+i*16))end
   print(string.format('MK2_NATIVE_COUNTER_HITBOX frame=%d at=%08X pc=%08X actor=%08X main=%08X owner=%08X id=%d victim=%08X victimMain=%08X victimID=%d descriptor=%08X words=%s writes=0 assistance=none',frame,at,cpu.state.PC.value,b,n,p:read_u32(n+0xc0),p:read_u16(b+0x1f0),a,m,p:read_u16(a+0x1f0),descriptor,table.concat(words,',')))
  end)
 end
 local a,m,b,n=context();if not a then return end
 fields=fields+1
 print(string.format('MK2_NATIVE_COUNTER_FIELD frame=%d actor=%08X main=%08X owner=%08X id=%d roster=%d hp=%d x=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X pose=%08X action=%04X flags=%04X body=%04X facing=%04X cache=%08X cpuActor=%08X cpuMain=%08X cpuID=%d stageY=%d cameraY=%d displayY=%d writes=0 assistance=none',frame,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(0x01060280),p:read_u16(0x010602f0),p:read_i16(a+0x90),p:read_i16(a+0xb0),p:read_i16(m+0x200),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20),p:read_u32(a+0x1d0),p:read_u16(m+0x1f0),p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u16(a+0xf0),p:read_u32(a+0x1a0),b,n,p:read_u16(b+0x1f0),p:read_i16(0x0105ecd0),p:read_i16(0x0105d130),p:read_i16(0x0105d060)))
end)
emu.register_stop(function()
 if tap then tap:remove()end
 print(string.format('MK2_NATIVE_COUNTER_RESULT frame=%d observedFields=%d writes=0 assistance=none fullPortAcceptance=false',frame,fields))
end)
