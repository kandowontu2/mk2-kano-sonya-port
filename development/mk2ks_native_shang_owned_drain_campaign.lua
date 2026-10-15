-- Actual repair replay: original physical campaign, additional passive proof.
dofile('mk2ks_native_shang_drain_startup.lua')
local file=assert(io.open('mk2ks_native_sonya_shang_cache_cause.lua','rb'))
local source=file:read('a');file:close()
-- Only the observed primary-table identity changes. No input policy changes.
local count
source,count=source:gsub('0xff9d7770','0xffd88000')
assert(count==3,'Three exact original observed primary table references')
assert(load(source,'@mk2ks_native_sonya_shang_cache_cause.lua::actual_relocated_primary_table','t',_ENV))()

local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,busy,records=0,false,0
local taps,pending={},{}
local palettes={[0xffd89000]=true,[0xffd89500]=true,[0xffd89a00]=true,[0xffd89f00]=true}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function record(kind,at,data,mask)
 if busy then return end
 busy=true
 local main=cpu.A13.value
 if not valid(main)then busy=false;return end
 local owner,victim=p:read_u32(main+0xc0),p:read_u32(main+0x140)
 if not valid(owner)or not valid(victim)or owner==victim or p:read_u16(owner+0x1f0)~=6 then busy=false;return end
 local id=p:read_u16(victim+0x1f0)
 if (id~=17 and id~=18)or not palettes[cpu.A0.value]then busy=false;return end
 records=records+1
 if records<=192 then
  print(string.format('MK2_SHANG_OWNED_DRAIN_ROUTE frame=%d seconds=%.12f kind=%s pc=%08X at=%08X data=%04X mask=%04X main=%08X owner=%08X victim=%08X actor=%08X owner_id=%d victim_id=%d victim_flags=%04X owner_flags=%04X palette=%08X a1=%08X a11=%08X pose=%08X cache=%08X sp=%08X stage=%d writes=0 assistance=none',
   frame,emu.time(),kind,cpu.PC.value,at,data&0xffff,mask,main,owner,victim,cpu.A8.value,
   p:read_u16(owner+0x1f0),id,p:read_u16(victim+0x160),p:read_u16(owner+0x160),cpu.A0.value,
   cpu.A1.value,cpu.A11.value,p:read_u32(victim+0x1d0),p:read_u32(victim+0x1a0),cpu.SP.value,p:read_u16(0x01061b30)))
 end
 if kind=='enter' and not pending[id]then pending[id]={frame=frame}end
 busy=false
end
for _,entry in ipairs({{0xffd8a800,'enter'},{0xffd8acb0,'cache_call'},{0xffd8ad00,'return'}})do
 local at,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'passive actual owned drain palette routing',function(address,data,mask)
  if address==at and cpu.PC.value==at+16 then record(kind,address,data,mask)end
 end)
end
emu.register_frame_done(function()
 frame=frame+1
 assert(#taps==3,'All actual new helper entry/call/return observers retained')
 for id,event in pairs(pending)do
  local age=frame-event.frame
  if age==1 or age==20 or age==40 or age==80 or age==120 or age==160 or age==200 or age==260 or age==320 or age==400 then
   local raw,w,h=manager.machine.screens[':screen']:pixels()
   assert(w==400 and h==254 and #raw==406400)
   print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=shang_shrink_id%d_age%d.png seconds=%.12f width=400 height=254 bytes=406400 hex=%s',id,age,emu.time(),
    raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  end
 end
end)
emu.register_stop(function()
 print(string.format('MK2_SHANG_OWNED_DRAIN_ROUTE_RESULT frame=%d records=%d writes=0 assistance=none',frame,records))
 for _,tap in ipairs(taps)do tap:remove()end
end)
