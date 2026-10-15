-- Passive lookup/animation provenance. All successful inputs remain unchanged.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,busy,first_bad,records=0,false,nil,0
local taps,ring,counts={},{},{}
local ring_size=4096
local pending=nil
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function peek(a)
 if a>=0xfe800000 and a<=0xffffffc0 then return p:read_u32(a)end
 return 0
end
local function roles()
 local ha,hm=p:read_u32(0x01060220),p:read_u32(0x01060260)
 local ca,cm=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 if not valid(ha)or not valid(hm)or not valid(ca)or not valid(cm)or ha==ca or hm==cm then return end
 if p:read_u32(hm+0xc0)~=ha or p:read_u32(cm+0xc0)~=ca or
  p:read_u16(ha+0x1f0)~=18 or p:read_u16(ca+0x1f0)~=6 or
  p:read_u16(0x01060280)~=18 or p:read_u16(0x01060e50)~=6 or
  p:read_u16(0x010601f0)~=1 or p:read_u16(0x01060dc0)~=0 or
  p:read_u16(0x01061b30)~=14 then return end
 local actor,main=cpu.A8.value,cpu.A13.value
 if (actor~=ha and actor~=ca)or(main~=hm and main~=cm)then return end
 return ha,hm,ca,cm
end
local essential={caller_input=true,victim_index_input=true,index_start=true,
 true_id_loaded=true,index_cell=true,index_result=true,caller_result=true}
local function record(kind,at,data,mask)
 if busy or frame<394481 then return end
 busy=true
 local ha,hm,ca,cm=roles()
 if not ha then busy=false;return end
 local actor,main=cpu.A8.value,cpu.A13.value
 records=records+1;counts[kind]=(counts[kind]or 0)+1
 local text=string.format('MK2_SONYA_SHANG_CACHE_CAUSE frame=%d seconds=%.12f kind=%s pc=%08X at=%08X data=%04X mask=%04X actor=%08X main=%08X main_owner=%08X main_other=%08X main_other_main=%08X human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X human_id=%d human_roster=%d cpu_id=%d cpu_roster=%d health=%d,%d state=%d,%d mode=%d stage=%d winner=%d action=%04X pose=%08X cache=%08X bank=%04X a0=%08X a1=%08X a5=%08X a6=%08X a7=%08X a9=%08X a11=%08X a14=%08X sp=%08X a0_rom=%08X a5_rom=%08X a9_rom=%08X a9_prev_rom=%08X stack0=%08X stack1=%08X stack2=%08X writes=0 assistance=none',
  frame,emu.time(),kind,cpu.PC.value,at,data&0xffff,mask,actor,main,p:read_u32(main+0xc0),
  p:read_u32(main+0x140),p:read_u32(main+0x170),ha,hm,ca,cm,
  p:read_u16(ha+0x1f0),p:read_u16(0x01060280),p:read_u16(ca+0x1f0),p:read_u16(0x01060e50),
  p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(0x010601f0),p:read_u16(0x01060dc0),
  p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u16(0x01061b00),
  p:read_u16(main+0x1f0),p:read_u32(ha+0x1d0),p:read_u32(ha+0x1a0),p:read_u16(ha+0x140),
  cpu.A0.value,cpu.A1.value,cpu.A5.value,cpu.A6.value,cpu.A7.value,cpu.A9.value,cpu.A11.value,cpu.A14.value,cpu.SP.value,
  peek(cpu.A0.value),peek(cpu.A5.value),peek(cpu.A9.value),peek(cpu.A9.value-32),
  p:read_u32(cpu.SP.value),p:read_u32(cpu.SP.value+32),p:read_u32(cpu.SP.value+64))
 ring[(records-1)%ring_size+1]=text
 if essential[kind] and (cpu.A0.value==0xff9d7770 or cpu.A1.value==0xff9d7770 or
    kind=='caller_input' or kind=='caller_result')then print(text)end
 if kind=='caller_input' and cpu.A0.value==0xff9d7770 and actor==ca and main==cm and
    p:read_u16(0x010602f0)==0 and not pending then pending={frame=frame}end
 busy=false
end
for _,entry in ipairs({{0xff8cb010,'caller_input'},{0xff842ed0,'victim_helper_enter'},
 {0xff842f30,'victim_index_input'},{0xff83b7f0,'index_start'},
 {0xff83b820,'true_id_loaded'},{0xff83b840,'index_cell'},{0xff83b850,'index_result'},
 {0xff8cb040,'caller_result'},{0xff842360,'victim_animation_enter'},
 {0xff83bb00,'animation_token_before'},{0xff83bb50,'animation_token_consumed'},
 {0xff838790,'cache_begin'},{0xff8387f0,'group_next'},
 {0xff838810,'descriptor'},{0xff838a30,'cache_end'}})do
 local at,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'passive actual Sonya victim Shang lookup/animation provenance',function(address,data,mask)
  if address==at and cpu.PC.value==at+16 then record(kind,address,data,mask)end
 end)
end
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'passive first actual Shang victim global cache write',function(at,data,mask)
 if busy or first_bad or cpu.PC.value~=0xff838860 then return end
 busy=true;local ha=roles();busy=false
 if not ha then return end
 first_bad=frame;record('first_global_write',at,data,mask)
 for serial=math.max(1,records-ring_size+1),records do print(ring[(serial-1)%ring_size+1])end
end)
emu.register_frame_done(function()
 frame=frame+1;assert(#taps==16,'All exact passive Shang provenance locations retained')
 if pending then
  local age=frame-pending.frame
  if age==1 or age==4 or age==12 or age==24 or age==48 or age==80 or age==100 or age==128 then
   local raw,w,h=manager.machine.screens[':screen']:pixels()
   assert(w==400 and h==254 and #raw==406400)
   print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=shang_victim_provenance_age%d.png seconds=%.12f width=400 height=254 bytes=406400 hex=%s',age,emu.time(),
    raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  end
 end
end)
emu.register_stop(function()
 print(string.format('MK2_SONYA_SHANG_CACHE_CAUSE_RESULT frame=%d first_bad=%d records=%d retained=%d writes=0 assistance=none',frame,first_bad or-1,records,math.min(records,ring_size)))
 for _,tap in ipairs(taps)do tap:remove()end
end)
dofile('mk2ks_native_paired_stumble_liu_early_leg.lua')
