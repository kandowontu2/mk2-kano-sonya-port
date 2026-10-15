-- Physical walking/jumping approach, native FDFF HP; no guest/register assistance.
local file=assert(io.open('mk2ks_native_subzero_legs_body_v4997.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique owned-body source anchor')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('emu.register_frame(function()frame=frame+1 end)',[[
local jump_start,close_start,ground_y,previous_gap,stalled=nil,nil,nil,nil,0
for _,entry in ipairs({{0xff8c0d90,'SHATTER_ENTRY'},{0xff8c1180,'HUMAN_PUNCH'},
 {0xff8c2e90,'FRACTURE_ENTRY'},{0xff8c3080,'LEGS_LOOKUP'}})do
 local address,tag=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'readonly native shatter branches',function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or not deep then return end
  local actor=cpu.A8.value;local main=cpu.A13.value
  if not valid(actor)or not valid(main)or p:read_u32(main+0xc0)~=actor then return end
  log(tag,string.format('entry=%08X pc=%08X value=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d action=%04X a0=%08X a1=%08X a9=%08X pose=%08X',
   at,cpu.PC.value,data&0xffff,mask,actor,main,p:read_u32(main+0xc0),p:read_u16(actor+0x1f0),p:read_u16(main+0x1f0),
   cpu.A0.value,cpu.A1.value,cpu.A9.value,p:read_u32(actor+0x1d0)))
 end)
end
emu.register_frame(function()
 frame=frame+1
 if not deep then return end
 local a,m,id,action=sample()
 if id~=identity then return end
 if native_main and p:read_u32(native_main+0xc0)==a then action=p:read_u16(native_main+0x1f0)end
 local other=p:read_u32(slots[winner].actor);local ownmain=p:read_u32(slots[winner].main)
 if not valid(other)or not valid(ownmain)or p:read_u16(other+0x1f0)~=8 then return end
 local x,y=p:read_i16(other+0x90),p:read_i16(other+0xb0)
 local vx,vy=p:read_i16(a+0x90),p:read_i16(a+0xb0)
 local gap=math.abs(x-vx);local forward=x<vx and'Right'or'Left'
 ground_y=ground_y or y
 local function press(key)
  buttons['P'..winner..' '..key]:set_value(1)
  log('FOLLOWUP_INPUT','slot='..winner..' button='..key:gsub(' ','_')..' gap='..gap)
 end
 log('APPROACH_FIELD',string.format('gap=%d x=%d y=%d victim_x=%d victim_y=%d ground_y=%d action=%04X own_action=%04X own_flags=%04X own_main=%08X finish=%d jump=%d close=%d',
  gap,x,y,vx,vy,ground_y,action,p:read_u16(ownmain+0x1f0),p:read_u16(ownmain+0x210),ownmain,p:read_u16(0x01061b00),jump_start or-1,close_start or-1))
 if frame-deep>=60 and action==0x0616 and not close_start then
  if gap<=65 and y==ground_y then close_start=frame;log('UPPERCUT_BEGIN','gap='..gap)
  else
   if gap>55 then press(forward)end
   if previous_gap==gap and y==ground_y then stalled=stalled+1 else stalled=0 end
   if not jump_start and stalled>=20 then jump_start=frame;log('PHYSICAL_JUMP','gap='..gap)end
   if jump_start and frame-jump_start<3 then press('Up')end
  end
 end
 previous_gap=gap
 if close_start then
  local age=frame-close_start
  for i,key in ipairs(shatter)do
   local edge=10+(i-1)*8
   if age>=edge and age<edge+3 then press(key=='Forward'and forward or key)end
  end
 end
end)
]])
replace('local a,m,id,action=sample();assert(id==identity)',[[local a,m,id,action=sample()
  if id~=identity then
   log('NATURAL_TRANSITION','id='..tostring(id));manager.machine:exit();return
  end]])
replace('frame-deep>=400','frame-deep>=500')
assert(load(source,'@owned_body_physical_native_shatter_v4939','t',_ENV))()
