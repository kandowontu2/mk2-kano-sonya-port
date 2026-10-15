-- Passive actual packed-victim handoffs; all original physical inputs intact.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,busy=0,false
local taps,counts,printed={},{},{}
local pending=nil
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function record(kind,at,data,mask)
 if busy then return end
 local main=cpu.A13.value
 if not valid(main)then return end
 local owner=p:read_u32(main+0xc0)
 local victim=p:read_u32(main+0x140)
 local vm=p:read_u32(main+0x170)
 if not valid(owner)or not valid(victim)or not valid(vm)or p:read_u32(vm+0xc0)~=victim then return end
 local id=p:read_u16(victim+0x1f0)
 if id~=17 and id~=18 then return end
 if kind=='after_render' and p:read_u32(cpu.SP.value+32)~=0xff8753f0 then return end
 busy=true
 counts[kind]=(counts[kind]or 0)+1
 local table=p:read_u32(0xff8752a0)
 local packed=p:read_u32(table+id*32)
 local key=kind..':'..p:read_u16(owner+0x1f0)..':'..id
 printed[key]=(printed[key]or 0)+1
 if printed[key]<=24 then
  print(string.format('MK2_PAIRED_STUMBLE_VICTIM frame=%d seconds=%.12f kind=%s pc=%08X at=%08X data=%04X mask=%04X actor=%08X owner_actor=%08X victim_actor=%08X main=%08X victim_main=%08X owner_id=%d victim_id=%d packed=%08X a0=%08X a1=%08X a9=%08X pose=%08X cache=%08X action=%04X health=%d,%d stage=%d writes=0 assistance=none',
   frame,emu.time(),kind,cpu.PC.value,at,data&0xffff,mask,cpu.A8.value,owner,victim,main,vm,
   p:read_u16(owner+0x1f0),id,packed,cpu.A0.value,cpu.A1.value,cpu.A9.value,
   p:read_u32(victim+0x1d0),p:read_u32(victim+0x1a0),p:read_u16(main+0x1f0),
   p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(0x01061b30)))
 end
 if kind=='after_render' and not pending and id==18 and p:read_u16(owner+0x1f0)==7 then
  pending={frame=frame}
 end
 busy=false
end
for _,entry in ipairs({{0xff8752f0,'packed_input'},{0xff8753c0,'after_lookup'},{0xff842330,'after_render'}})do
 local at,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'passive actual paired stumble table handoff',function(address,data,mask)
  if address==at and cpu.PC.value==at+16 then record(kind,address,data,mask)end
 end)
end
emu.register_frame_done(function()
 frame=frame+1
 if pending then
  local age=frame-pending.frame
  if age==1 or age==4 or age==12 or age==48 then
   local raw,w,h=manager.machine.screens[':screen']:pixels()
   assert(w==400 and h==254 and #raw==406400)
   print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=paired_stumble_victim_age%d.png seconds=%.12f width=400 height=254 bytes=406400 hex=%s',age,emu.time(),
    raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  end
 end
 assert(#taps==3,'All exact passive actual handoff observers retained')
end)
emu.register_stop(function()
 print(string.format('MK2_PAIRED_STUMBLE_RESULT frame=%d packed_inputs=%d after_lookups=%d after_renders=%d writes=0 assistance=none',
  frame,counts.packed_input or 0,counts.after_lookup or 0,counts.after_render or 0))
 for _,tap in ipairs(taps)do tap:remove()end
end)
dofile('mk2ks_native_kano_laser_sonya_postending_leg_guard_late.lua')
