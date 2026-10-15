-- Read-only instruction-time pose/cache correlation. Keep the original real
-- selection/charged-roll/held-duck fixture and every input unchanged.
-- v1's misleading list labels are not reused: cache is actor+1A0, Main is
-- the real process pointer, flags are Main+210, body is actor+160.
dofile('mk2ks_human_special_negative_v9.lua')
local cpu=manager.machine.devices[':maincpu']
local p,r=cpu.spaces.program,cpu.state
local screen=manager.machine.screens[':screen']
local gfx=manager.machine.memory.regions[':gfxrom']
local emitted={}
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local slots={{0x01060220,0x01060260},{0x01060df0,0x01060e30}}
local frame,taps,pending=0,{},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 for _,f in ipairs(pending)do
  if frame==f+1 then
   local name=string.format('ball_comparison_%04d.png',f)
   screen:snapshot(name)
   print(string.format('MK2_BALL_V2_SNAPSHOT comparison=%d frame=%d phase=done file=%s writes=0',f,frame,name))
  end
 end
end)
local function actor(role,a,m)
 local cache=p:read_u32(a+0x1a0)
 print(string.format('MK2_BALL_V2_ACTOR frame=%d side=%d role=%s actor=%08X main=%08X owner=%08X cache=%08X pose=%08X id=%d action=%04X x=%d y=%d floor=%d facing=%04X flags=%04X body=%04X palette=%04X writes=0',
  frame,side,role,a,m,p:read_u32(m+0xc0),cache,p:read_u32(a+0x1d0),p:read_u16(a+0x1f0),p:read_u16(m+0x1f0),p:read_i16(a+0x90),p:read_i16(a+0xb0),p:read_i16(m+0x200),p:read_u16(a+0xf0),p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u16(a+0x140)))
 if not valid(cache)then return end
 for part=0,7 do
  local at=cache+part*0x70;local source=p:read_u32(at)
  if source==0 then break end
  print(string.format('MK2_BALL_V2_PART frame=%d side=%d role=%s part=%d source=%08X width=%d height=%d command=%04X dx=%d dy=%d writes=0',
   frame,side,role,part,source,p:read_u16(at+0x20),p:read_u16(at+0x30),p:read_u16(at+0x40),p:read_i16(at+0x50),p:read_i16(at+0x60)))
  local width,height,command=p:read_u16(at+0x20),p:read_u16(at+0x30),p:read_u16(at+0x40)|0x8002
  local key=string.format('%08X_%04X_%d_%d',source,command,width,height)
  if not emitted[key]then
   emitted[key]=true
   local offset=source
   if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000 end
   if offset>=0xf8000000 then offset=offset-0xf8000000 end
   local bpp=(command>>12)&7;if bpp==0 then bpp=8 end
   local first=offset//8
   assert(first>=0 and first<0x2000000,'Actual collision-time graphics bounds')
   local count=math.min(math.ceil((offset%8+width*height*bpp+(command&0x80~=0 and height*8 or 0))/8)+8,0x2000000-first)
   local hex={};for index=first,first+count-1 do hex[#hex+1]=string.format('%02X',gfx:read_u8(index))end
   print(string.format('MK2_BALL_V3_GFX frame=%d key=%s offset=%d bytes=%d data=%s writes=0',frame,key,offset,count,table.concat(hex)))
  end
 end
end
taps[#taps+1]=p:install_read_tap(0xff835b70,0xff835b7f,'native roll instruction-time pose/cache v2',function(at)
 if at~=0xff835b70 or r.PC.value~=0xff835b80 then return end
 local own,main=p:read_u32(slots[side][1]),p:read_u32(slots[side][2])
 if not valid(own)or not valid(main)or own~=r.A8.value or main~=r.A13.value or p:read_u16(main+0x1f0)~=0x20b then return end
 local victim,vm=p:read_u32(slots[3-side][1]),p:read_u32(slots[3-side][2])
 if not valid(victim)or not valid(vm)then return end
 print(string.format('MK2_BALL_V2_GEOMETRY frame=%d side=%d pc=%08X actor=%08X main=%08X victim=%08X victim_main=%08X victim_min=%08X victim_max=%08X attack_min=%08X attack_max=%08X bounds=%d writes=0',
  frame,side,r.PC.value,own,main,victim,vm,r.A2.value,r.A3.value,r.A4.value,r.A5.value,r.A6.value))
 actor('own',own,main);actor('victim',victim,vm)
 pending[#pending+1]=frame
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
