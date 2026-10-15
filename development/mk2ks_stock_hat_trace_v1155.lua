-- Original hat/native collision/flag consumers, read-only.
dofile('mk2ks_stock_hat_display_v1154.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,events,taps=0,0,{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,s)
 events=events+1
 print(string.format('MK2_HAT_V1155_%s frame=%d writes=0 assistance=none %s',tag,frame,s))
end
for _,address in ipairs({0xff8ae840,0xff8ae9e0,0xff8aeb80,0xff8aec80,0xff8aecb0,0xff8aed10,0xff8aedc0,0xff835e30,0xff8bd270,0xff8b6820,
 0xff8e0b80,0xff8e0c30,0xff8e0d20,0xffa16cb0,0xffa16f20,0xffa172f0})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'native hat state '..string.format('%08X',address),function(at)
  local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
  if not start or frame-start>200 or at~=address then return end
  local a,m=cpu.A8.value,cpu.A13.value
  if not valid(a)or not valid(m)then return end
  log('STATE',string.format('age=%d at=%08X pc=%08X actor=%08X main=%08X id=%d x=%d y=%d vx=%08X vy=%08X flags=%04X task270=%04X success=%d a0=%08X a1=%08X a7=%08X b2=%08X st=%08X a9=%08X floor=%d pose=%08X stageY=%d',
   frame-start,address,cpu.PC.value,a,m,p:read_u16(a+0x1f0),p:read_i16(a+0x90),p:read_i16(a+0xb0),p:read_u32(a+0x40),p:read_u32(a+0x60),
   p:read_u16(a+0x160),p:read_u16(m+0x270),p:read_u16(0x010619c0),cpu.A0.value,cpu.A1.value,cpu.A7.value,cpu.B2.value,cpu.ST.value,
   cpu.A9.value,p:read_i16(m+0x200),p:read_u32(a+0x1d0),p:read_i16(0x0105ecd0)))
 end)
end
taps[#taps+1]=p:install_write_tap(0x010619c0,0x010619cf,'native hat success flag writer',function(at,data,mask)
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if not start or frame-start>200 or at~=0x010619c0 or mask&0xffff~=0xffff then return end
 log('SUCCESS_WRITE',string.format('age=%d old=%d new=%d pc=%08X actor=%08X main=%08X',frame-start,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value))
end)
emu.register_frame(function()assert(#taps==17);frame=frame+1 end)
emu.register_stop(function()log('RESULT','events='..events)end)
