-- Actual stock Kitana victim, original physical BBBB LP; read-only corner QA.
dofile('mk2ks_stock_extended_earned_ram_v3958.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local frame=0
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local wanted={[41]=true,[89]=true,[170]=true,[176]=true,[182]=true,[608]=true}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  print('MK2_ARM_STOCK_GUEST bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
 end
end)
emu.register_frame_done(function()
 local origin=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if not origin or not wanted[frame-origin]then return end
 local field=side==1 and 0x01060220 or 0x01060df0
 local actor,main=p:read_u32(field),p:read_u32(field+0x40)
 print(string.format('MK2_ARM_STOCK_STATE frame=%d origin=%d age=%d side=%d writes=0 assistance=none actor=%08X main=%08X id=%d roster=%d x=%d y=%d floor=%d pose=%08X stageY=%d displayY=%d cameraY=%d cameraX=%d',
  frame,origin,frame-origin,side,actor,main,valid(actor)and p:read_u16(actor+0x1f0)or-1,p:read_u16(field+0x60),
  valid(actor)and p:read_i16(actor+0x90)or-1,valid(actor)and p:read_i16(actor+0xb0)or-1,
  valid(main)and p:read_i16(main+0x200)or-1,valid(actor)and p:read_u32(actor+0x1d0)or 0,
  p:read_i16(0x0105ecd0),p:read_i16(0x0105d060),p:read_i16(0x0105d130),p:read_i16(0x0105d110)))
 local raw=manager.machine.video:snapshot_pixels();assert(#raw==406400)
 print(string.format('MK2_ARM_STOCK_RGB frame=%d age=%d bytes=%d hex=%s',frame,frame-origin,#raw,
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end)
