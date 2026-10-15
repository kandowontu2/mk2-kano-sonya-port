-- Earn the existing complete Sonya campaign and fresh Kano P1 join unchanged.
-- Only after the old361-field join test: released inputs / ordinary continues.
-- No guest, health, ID, AI, RNG or register writes.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,started,completed,joined=0,nil,nil,nil
local taps={}
local slots={{0x01060220,0x01060260,0x01060280,0x010601f0,0x010602f0},
 {0x01060df0,0x01060e30,0x01060e50,0x01060dc0,0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s[1]),p:read_u32(s[2])
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,id=p:read_u16(a+0x1f0),roster=p:read_u16(s[3]),state=p:read_u16(s[4]),hp=p:read_u16(s[5]),
 owner=p:read_u32(m+0xc0),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
 pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140),body=p:read_u16(a+0x160)}
end
local function log(tag,s)
 print(string.format('MK2_LASER_%s frame=%d side=2 age=%d writes=0 assistance=none %s',tag,frame,started and frame-started or-1,s or''))
end
local function owns()
 local k,h=sample(2),sample(1)
 return k and h and k.id==17 and k.roster==17 and k.state==0 and k.owner==k.actor and
 h.id==17 and h.roster==17 and h.state==1 and h.owner==h.actor and
 cpu.A8.value==k.actor and cpu.A13.value==k.main and p:read_u16(0x010601d0)==2,k,h
end
local function tap(at,label,fn)
 taps[#taps+1]=p:install_read_tap(at,at+15,label,function(where)
  if where==at and cpu.PC.value==at+16 then fn()end
 end)
end
for _,entry in ipairs({{0xff876b40,'CPU_FIRST_DISPATCH'},{0xff876b80,'CPU_SECOND_DISPATCH'},
 {0xffd86600,'CPU_LASER_GUARD'},{0xfffaae00,'CPU_FRIENDSHIP'},{0xff83b850,'CPU_LOOKUP'}})do
 local at,tag=entry[1],entry[2]
 tap(at,'passive real CPU finisher dispatch',function()
  local ok,k,h=owns();if not ok then return end
  log(tag,string.format('pc=%08X a0=%08X a1=%08X actor=%08X main=%08X victim=%08X gap=%d hp=%d,%d',
   cpu.PC.value,cpu.A0.value,cpu.A1.value,k.actor,k.main,h.actor,math.abs(k.x-h.x),k.hp,h.hp))
 end)
end
tap(0xffd85800,'passive naturally selected CPU laser performer',function()
 local ok,k,h=owns();if not ok or started then return end
 assert(h.hp==0 and k.hp>0)
 started=frame;_mk2_cpu_laser_started=frame
 log('ENTRY',string.format('actor=%08X main=%08X victim=%08X victim_main=%08X gap=%d hp=%d,%d cpu_state=%d victim_state=%d',
 k.actor,k.main,h.actor,h.main,math.abs(k.x-h.x),k.hp,h.hp,k.state,h.state))
end)
tap(0xffd84800,'passive genuine CPU laser victim contact',function()
 if started then log('CONTACT',string.format('actor=%08X main=%08X id=%d bank=%04X',cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A8.value+0x1f0),p:read_u16(cpu.A8.value+0x140)))end
end)
tap(0xffa14860,'passive CPU laser native winner',function()
 local k=sample(2)
 if started and not completed and k and cpu.A8.value==k.actor and cpu.A13.value==k.main then completed=frame;log('WINNER',string.format('main=%08X',k.main))end
end)
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'passive native render-copy overrun',function(at,data,mask)
 if cpu.PC.value==0xff838860 then log('OVERRUN',string.format('at=%08X data=%04X mask=%04X',at,data&0xffff,mask))end
end)
local high,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local buttons={Coin=system['Coin 1'],Start=system['1 Player Start']}
for _,key in ipairs({'High Punch','Left','Right','Down'})do buttons[key]=high['P1 '..key]end
local loss,css,plan,lastmode,losses=nil,nil,nil,nil,0
local function input(key)buttons[key]:set_value(1);log('CPU_CONTINUE_INPUT','key='..key:gsub(' ','_'))end
local function route(first)
 local q={{first,{}}};local seen={[first]=true};local at=1
 while q[at]do local r=q[at];at=at+1;if r[1]==17 then return r[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local base=key=='Left'and 0xffff1400 or key=='Right'and 0xffff1600 or 0xffff1200
   local next_id=p:read_u16(base+r[1]*16)
   if next_id<=18 and not seen[next_id]then local path={table.unpack(r[2])};path[#path+1]=key;q[#q+1]={next_id,path};seen[next_id]=true end
  end
 end
 error('No normal native cursor route to Kano')
end
local function followup(f)
 joined=joined or f
 for _,field in pairs(buttons)do field:clear_value()end
 if started then return end
 local mode,state=p:read_u16(0x010601d0),p:read_u16(slots[1][4])
 if mode~=lastmode then
  log('CPU_CONTINUE_MODE',string.format('mode=%d states=%d,%d ids=%d,%d hp=%d,%d winner=%d losses=%d',mode,state,p:read_u16(slots[2][4]),p:read_u16(slots[1][3]),p:read_u16(slots[2][3]),p:read_u16(slots[1][5]),p:read_u16(slots[2][5]),p:read_u16(0x01061b00),losses));lastmode=mode
 end
 if mode==2 and state==1 then loss=nil;css=nil;plan=nil end
 if not loss and mode==3 and state==2 and p:read_u16(0x01061b00)==2 and p:read_u32(slots[1][1])==0 then
  loss=f;losses=losses+1;log('CPU_CONTINUE_LOSS','number='..losses)
 end
 if loss and not css then local age=f-loss
  if age>=20 and age<25 or age>=270 and age<275 then input('Coin')end
  if age>=310 and age<315 then input('Start')end
 end
 if loss and not css and mode==4 and state==3 and p:read_u16(slots[1][3])<=18 then
  css=f;plan=route(p:read_u16(slots[1][3]));log('CPU_CONTINUE_SELECT','path='..table.concat(plan,','))
 end
 if css and mode==4 and state==3 then local age=f-css
  for n,key in ipairs(plan)do local begin=20+(n-1)*12;if age>=begin and age<begin+4 then input(key)end end
  local confirm=20+#plan*12+24;if age>=confirm and age<confirm+4 then input('High Punch')end
 end
end
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 if started then local age=frame-started
  for n=1,2 do local s=sample(n);if s then log('FIELD',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d x=%d y=%d floor=%d pose=%08X bank=%04X body=%04X child=%08X',n,s.actor,s.main,s.owner,s.id,s.roster,s.state,s.hp,s.x,s.y,s.floor,s.pose,s.bank,s.body,p:read_u32(s.main+0x190)))end end
  if ({[1]=true,[21]=true,[48]=true,[68]=true,[72]=true,[100]=true,[132]=true,[164]=true,[169]=true,[172]=true,[175]=true,[196]=true,[240]=true,[450]=true,[600]=true,[750]=true})[age]then
   local raw,w,h=manager.machine.screens[':screen']:pixels();assert(w==400 and h==254 and#raw==406400)
   print(string.format('MK2_LASER_RGB frame=%d age=%d width=%d height=%d bytes=%d hex=%s',frame,age,w,h,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  end
  if age>=750 then log('STOP',string.format('started=%d completed=%d mode=%d losses=%d',started,completed or-1,p:read_u16(0x010601d0),losses));manager.machine:exit()end
 elseif joined and frame-joined>=40000 then log('STOP','reason=finite_native_CPU_choice_observation');manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('started=%d completed=%d losses=%d',started or-1,completed or-1,losses))
 for _,t in ipairs(taps)do t:remove()end
end)
local path='mk2ks_native_kano_p2_postending_sonya.lua'
local file=assert(io.open(path,'r'));local template=file:read('a'):gsub('\r\n','\n');file:close()
local function once(before,after)
 local a,b=assert(template:find(before,1,true));assert(not template:find(before,b+1,true))
 template=template:sub(1,a-1)..after..template:sub(b+1)
end
once(' local age=frame-ending_completed-300\n',' if join_done then _cpu_laser_followup(frame);return end\n local age=frame-ending_completed-300\n')
once("   manager.machine:exit()\n  end\n end\n if age>=1800", "   -- The subsequent released-input CPU observation owns terminal exit.\n  end\n end\n if age>=1800")
local native_io=io
local scoped_io=setmetatable({open=function(name,mode)
 if name==path then assert(mode=='rb');return {read=function(_,format)assert(format=='a');return template end,close=function()return true end}end
 return native_io.open(name,mode)
end},{__index=native_io})
local environment=setmetatable({io=scoped_io,_cpu_laser_followup=followup},{__index=_G})
file=assert(io.open('mk2ks_native_sonya_p1_postending_kano.lua','r'));local source=file:read('a');file:close()
assert(load(source,'@mk2ks_native_sonya_p1_postending_kano.lua::unchanged_campaign_then_released_CPU_observation','t',environment))()
