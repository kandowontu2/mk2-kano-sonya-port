-- Same real morph driver/full native capture; observe actual direct projection.
-- No shadow position is supplied or changed by this observer.
dofile('mk2ks_native_morph_floor_display_v3165.lua')
do
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local side=tonumber(assert(os.getenv('MK2KS_HUMAN_SHANG_SIDE')))
local target=assert(os.getenv('MK2KS_HUMAN_SHANG_TARGET'))
local slots={{a=0x01060220,m=0x01060260},{a=0x01060df0,m=0x01060e30}}
local frame,start,restored=0,nil,nil
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame(function()frame=frame+1 end)
for _,address in ipairs({0xff86e480,0xffa16700})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual direct morph shadow observation window',function(at)
  if at~=address or cpu.PC.value~=address+16 then return end
  local a,m=p:read_u32(slots[side].a),p:read_u32(slots[side].m)
  if valid(a)and valid(m)and cpu.A8.value==a and cpu.A13.value==m and p:read_u32(m+0xc0)==a then
   if address==0xff86e480 and not start then start=frame
   elseif address==0xffa16700 and start and not restored then restored=frame end
  end
 end)
end
taps[#taps+1]=p:install_read_tap(0xff8012b0,0xff8012bf,'actual original shadow world/camera/ground registers',function(at)
 if not start or frame>(restored and restored+30 or start+900)or at~=0xff8012b0 or cpu.PC.value~=0xff8012c0 then return end
 local row=cpu.A9.value
 for slot,s in ipairs(slots)do
  local a,m=p:read_u32(s.a),p:read_u32(s.m)
  if valid(a)and valid(m)and p:read_u32(m+0xc0)==a then
   local cache=p:read_u32(a+0x1a0)
   if valid(cache)and row>=cache and row<cache+12*112 and(row-cache)%112==0 then
    local world=((p:read_u16(a+0xb0)&0xffff)<<16)|p:read_u16(a+0x90)
    print(string.format('MK2_NAT_CAMPAIGN_FLOOR_SHADOW_PROJECTION frame=%d human_slot=%d fighter=%s writes=0 assistance=none slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d pose=%08X cache=%08X row=%08X component=%d body=%04X facing=%04X world=%08X b1=%08X b2=%08X b4=%08X b7=%08X a0=%08X a5=%08X shadow_camera=%08X stageY=%d displayY=%d cameraY=%d floor=%d pc=%08X',
     frame,side,target,slot,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(s.a+0x60),
     p:read_u32(a+0x1d0),cache,row,(row-cache)//112,p:read_u16(a+0x160),p:read_u16(a+0xf0),
     world,cpu.B1.value,cpu.B2.value,cpu.B4.value,cpu.B7.value,cpu.A0.value,cpu.A5.value,
     cpu.B1.value|p:read_u16(0x0105d350),p:read_i16(0x0105ecd0),p:read_i16(0x0105d060),p:read_i16(0x0105d130),p:read_i16(m+0x200),cpu.PC.value))
   end
  end
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
end
