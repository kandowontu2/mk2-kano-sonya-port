-- Same immutable game, genuine stock/added victims and physical shatter; RAM-only PCM.
local file=assert(io.open('mk2ks_native_subzero_body_probe_v4933.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique native reference anchor')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('({kano=17,sonya=18})','({kano=17,sonya=18,kitana=4,liu_kang=1})')
replace('emu.register_frame(function()frame=frame+1 end)',[=[
local close_start,fracture,wrap=nil,nil,nil
local pcm_index=0
for _,entry in ipairs({{0xff8c0d90,'SHATTER_ENTRY'},{0xff8c1180,'HUMAN_PUNCH'},
 {0xff8c2e90,'FRACTURE_ENTRY'},{0xff8c3080,'LEGS_LOOKUP'},
 {0xffa12530,'SOUND_CALL'},{0xff9e1290,'ICE_EMITTER'},{0xff80e280,'EFFECT_SPAWN'},
 {0xff841ec0,'NATIVE_PARK'},{0xff8cdc40,'WIN_WRAP'}})do
 local address,tag=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'readonly native reference shatter',function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or not deep then return end
  local a,m=cpu.A8.value,cpu.A13.value
  if not valid(a)or not valid(m)or p:read_u32(m+0xc0)~=a then return end
  local id=p:read_u16(a+0x1f0)
  if id~=identity and id~=8 then return end
  if tag=='FRACTURE_ENTRY'then fracture=fracture or frame end
  if tag=='WIN_WRAP'and id==8 then wrap=wrap or frame end
  if tag=='SOUND_CALL'and cpu.A0.value~=0xd8 then return end
  if tag=='ICE_EMITTER'and id~=identity then return end
  if tag=='EFFECT_SPAWN'and cpu.A7.value~=0xff9ee3a0 then return end
  if tag=='NATIVE_PARK'and (id~=identity or p:read_u16(m+0x1f0)~=0x0408)then return end
  log(tag,string.format('entry=%08X pc=%08X value=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d action=%04X a0=%08X a1=%08X a7=%08X a9=%08X a11=%08X pose=%08X palette=%04X',
   at,cpu.PC.value,data&0xffff,mask,a,m,p:read_u32(m+0xc0),id,p:read_u16(m+0x1f0),cpu.A0.value,cpu.A1.value,cpu.A7.value,cpu.A9.value,cpu.A11.value,p:read_u32(a+0x1d0),p:read_u16(a+0x140)))
 end)
end
emu.register_frame(function()
 frame=frame+1
 local a,m,id,action=sample()
 if not deep or id~=identity then return end
 if native_main and p:read_u32(native_main+0xc0)==a then action=p:read_u16(native_main+0x1f0)end
 local other=p:read_u32(slots[winner].actor)
 if not valid(other)or p:read_u16(other+0x1f0)~=8 then return end
 local x,vx=p:read_i16(other+0x90),p:read_i16(a+0x90)
 local forward=x<vx and'Right'or'Left';local gap=math.abs(x-vx)
 local function press(key)
  buttons['P'..winner..' '..key]:set_value(1)
  log('FOLLOWUP_INPUT','slot='..winner..' button='..key:gsub(' ','_')..' gap='..gap)
 end
 if frame-deep>=60 and action==0x0616 and not close_start then
  if gap<=65 then close_start=frame;log('UPPERCUT_BEGIN','gap='..gap)else press(forward)end
 end
 if close_start then
  for i,key in ipairs(shatter)do
   local edge=10+(i-1)*8;local age=frame-close_start
   if age>=edge and age<edge+3 then press(key=='Forward'and forward or key)end
  end
 end
end)
emu.register_sound_update(function()
 if not deep or (wrap and frame-wrap>180)then return end
 local raw=manager.machine.sound:get_samples();assert(#raw%4==0)
 pcm_index=pcm_index+1
 print(string.format('MK2_EARNED_SUBZERO_PCM frame=%d index=%d seconds=%.12f bytes=%d hex=%s',
  frame,pcm_index,manager.machine.time:as_double(),#raw,raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))
end)
]=])
replace('if deep and frame-deep==100 then',
 'if deep and (frame-deep==100 or (fracture and frame-fracture==20)or (wrap and frame-wrap==150))then')
replace('frame-deep>=400','((wrap and frame-wrap>=180)or frame-deep>=600)')
replace("log('HOST_EXIT',string.format('deep=%d uppercut=%d completed=%d',deep or-1,uppercut or-1,completed or-1))",[[
  log('LIFECYCLE_END',string.format('deep=%d fracture=%d wrap=%d pcm_updates=%d mode=%d',deep or-1,fracture or-1,wrap or-1,pcm_index,p:read_u16(0x010601d0)))
  log('HOST_EXIT',string.format('deep=%d uppercut=%d completed=%d',deep or-1,uppercut or-1,completed or-1))]])
assert(load(source,'@actual_native_reference_pcm_v4961','t',_ENV))()
