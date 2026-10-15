-- New palette-route observer is read-only. The optional explicitly controlled
-- diagnostic delegates its one documented flag write to unchanged1063.
dofile('mk2ks_stock_fatality_display_v1077.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame=0
local taps,pending={},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_ARM_PALETTE_V1073_%s frame=%d writes=0 assistance=none %s',tag,frame,text))
end
local function observe(address,tag)
 taps[#taps+1]=p:install_read_tap(address,address+15,'native detached arm palette '..tag,function(at)
  if at~=address or not rawget(_G,'MK2_STOCK_V921_ACTION_START') then return end
  local prop=cpu.A8.value;local main=cpu.A13.value
  if not valid(prop) or not valid(main)then return end
  local victim=p:read_u32(main+0x140)
  if not valid(victim)then return end
  local data={prop=prop,main=main,victim=victim,id=p:read_u16(victim+0x1f0),
   flags=p:read_u16(victim+0x160),sp=cpu.SP.value,st=cpu.ST.value,
   a1=cpu.A1.value,a2=cpu.A2.value,a7=cpu.A7.value}
  if tag=='ENTRY'then pending[prop]=data end
  local before=pending[prop]
  local preserved=before and before.sp==data.sp and before.st==data.st
   and before.a1==data.a1 and before.a2==data.a2 and before.a7==data.a7
  log(tag,string.format('pc=%08X prop=%08X prop_id=%d main=%08X victim=%08X id=%d flags=%04X sp=%08X st=%08X a1=%08X a2=%08X a7=%08X palette=%08X preserved=%d',
   cpu.PC.value,prop,p:read_u16(prop+0x1f0),main,victim,data.id,data.flags,
   data.sp,data.st,data.a1,data.a2,data.a7,cpu.A0.value,preserved and 1 or 0))
 end)
end
observe(0xfffde000,'ENTRY')
observe(0xfffde000+35*16,'OWNED_APPLY')
observe(0xfffde000+42*16,'STOCK_FALLBACK')
observe(0xff841090,'ORIGINAL_APPLY')
emu.register_frame(function()frame=frame+1;assert(#taps==4)end)
