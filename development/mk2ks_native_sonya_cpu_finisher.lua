-- Exact established Kano P2 selection/ladder/180-field guard fixture first.
-- Then released human input and ordinary paid continues; CPU AI/RNG untouched.
assert(os.getenv('MK2KS_UI_FIGHTER')=='kano' and os.getenv('MK2KS_UI_SIDE')=='2')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,started,completed,busy=0,nil,nil,false
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),
  state=p:read_u16(s.state),hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),
  floor=p:read_i16(m+0x200),pose=p:read_u32(a+0x1d0),action=p:read_u16(m+0x1f0),
  flags=p:read_u16(m+0x210),body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140)}
end
local function own()
 local s,k=sample(1),sample(2)
 return s and k and s.id==18 and s.roster==18 and s.state==0 and
  k.id==17 and k.roster==17 and k.state==1 and
  cpu.A8.value==s.actor and cpu.A13.value==s.main and p:read_u16(0x010601d0)==2
end
local function geometry(tag)
 local s,k=sample(1),sample(2)
 if not s or not k then return end
 local child=p:read_u32(s.main+0x190);local cv=valid(child)
 print(string.format('MK2_SONYA_CPU_FINISH_%s frame=%d age=%d seconds=%.12f mode=%d stage=%d schedule=%08X pc=%08X a0=%08X a1=%08X s_actor=%08X s_main=%08X s_context=%08X s_id=%d s_roster=%d s_state=%d s_hp=%d s_x=%d s_y=%d s_floor=%d s_pose=%08X s_action=%d s_flags=%04X s_body=%04X s_bank=%04X k_actor=%08X k_main=%08X k_context=%08X k_id=%d k_roster=%d k_state=%d k_hp=%d k_x=%d k_y=%d k_floor=%d k_pose=%08X k_action=%d k_flags=%04X k_body=%04X k_bank=%04X child=%08X child_valid=%d child_x=%d child_y=%d child_pose=%08X child_body=%04X child_bank=%04X gap=%d writes=0 assistance=none',
 tag,frame,started and frame-started or -1,emu.time(),p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u32(0x01061b10),
 cpu.PC.value,cpu.A0.value,cpu.A1.value,s.actor,s.main,s.owner,s.id,s.roster,s.state,s.hp,s.x,s.y,s.floor,s.pose,s.action,s.flags,s.body,s.bank,
 k.actor,k.main,k.owner,k.id,k.roster,k.state,k.hp,k.x,k.y,k.floor,k.pose,k.action,k.flags,k.body,k.bank,
 child,cv and 1 or 0,cv and p:read_i16(child+0x90)or -32768,cv and p:read_i16(child+0xb0)or -32768,
 cv and p:read_u32(child+0x1d0)or 0,cv and p:read_u16(child+0x160)or 0,cv and p:read_u16(child+0x140)or 0,math.abs(s.x-k.x)))
end
taps[#taps+1]=p:install_read_tap(0xff83b850,0xff83b85f,'readonly real CPU Sonya distance/performer lookup',function(at)
 if busy or at~=0xff83b850 or cpu.PC.value~=0xff83b860 or not own()then return end
 if cpu.A1.value==0xfff9cae0 or cpu.A1.value==0xfffa1900 or cpu.A1.value==0xfffa1b60 then
  busy=true;geometry(cpu.A1.value==0xfff9cae0 and 'DISTANCE' or 'PERFORMER');busy=false
 end
end)
for _,entry in ipairs({{0xfffab200,'OWN_ENTRY'},{0xffa14860,'WINNER_HANDOFF'}})do
 local at,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'readonly own CPU Sonya finisher lifecycle',function(address)
  if busy or address~=at or cpu.PC.value~=at+16 or not own()then return end
  busy=true
  if kind=='OWN_ENTRY' and not started then started=frame;geometry(kind)
  elseif kind=='WINNER_HANDOFF' and started and not completed then completed=frame;geometry(kind)end
  busy=false
 end)
end
for n,slot in ipairs(slots)do
 local number=n
 taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'readonly actually earned native health '..n,function(at,data,mask)
  if mask~=0xffff then return end
  print(string.format('MK2_SONYA_CPU_FINISH_HEALTH frame=%d seconds=%.12f slot=%d at=%08X before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X writes=0 assistance=none',
  frame,emu.time(),number,at,p:read_u16(at),data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 end)
end
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'readonly actual global-render-cache overrun',function(at,data,mask)
 if busy or cpu.PC.value~=0xff838860 then return end
 busy=true
 print(string.format('MK2_SONYA_CPU_FINISH_OVERRUN frame=%d at=%08X data=%04X mask=%04X pc=%08X a8=%08X a13=%08X writes=0 assistance=none',
 frame,at,data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 manager.machine:exit();busy=false
end)
local function snapshot(name)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=%s seconds=%.12f width=400 height=254 bytes=406400 hex=%s',
 name,emu.time(),raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
local high,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local buttons={Coin=system['Coin 2'],Start=system['2 Players Start']}
for _,name in ipairs({'High Punch','Left','Right','Down'})do buttons[name]=high['P2 '..name]end
local loss_at,css_at,plan,last_mode,losses=nil,nil,nil,nil,0
local checked=false
local function input(button,f)
 buttons[button]:set_value(1)
 print(string.format('MK2_SONYA_CPU_CONTINUE_INPUT frame=%d button=%s writes=0 assistance=none',f,button:gsub(' ','_')))
end
local function route(start)
 local queue={{start,{}}};local visited={[start]=true};local at=1
 while queue[at]do
  local row=queue[at];at=at+1
  if row[1]==17 then return row[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local base=key=='Left'and 0xffff1400 or key=='Right'and 0xffff1600 or 0xffff1200
   local next_id=p:read_u16(base+row[1]*16)
   if next_id<=18 and not visited[next_id]then
    local steps={};for _,step in ipairs(row[2])do steps[#steps+1]=step end
    steps[#steps+1]=key;queue[#queue+1]={next_id,steps};visited[next_id]=true
   end
  end
 end
 error('No ordinary native cursor route to Kano')
end
local function continuation(f)
 for _,field in pairs(buttons)do field:clear_value()end
 local mode,state=p:read_u16(0x010601d0),p:read_u16(slots[2].state)
 if not checked then
  checked=true;local s,k=sample(1),sample(2)
  print(string.format('MK2_SONYA_CPU_CONTINUE_INITIAL frame=%d mode=%d s_id=%d s_roster=%d s_state=%d k_id=%d k_roster=%d k_state=%d writes=0 assistance=none',
  f,mode,s and s.id or-1,s and s.roster or-1,s and s.state or-1,k and k.id or-1,k and k.roster or-1,k and k.state or-1))
  if not(s and k and s.id==18 and s.roster==18 and s.state==0 and k.id==17 and k.roster==17 and k.state==1)then
   print('MK2_SONYA_CPU_CONTINUE_UNEXPECTED_INITIAL_OPPONENT actual_fixture_not_game_failure=true')
   manager.machine:exit();return
  end
 end
 if last_mode~=mode then
  print(string.format('MK2_SONYA_CPU_CONTINUE_STATE frame=%d mode=%d states=%d,%d roster=%d,%d actors=%08X,%08X health=%d,%d winner=%d stage=%d schedule=%08X writes=0 assistance=none',
  f,mode,p:read_u16(slots[1].state),state,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),
  p:read_u32(slots[1].actor),p:read_u32(slots[2].actor),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),
  p:read_u16(0x01061b00),p:read_u16(0x01061b30),p:read_u32(0x01061b10)))
  last_mode=mode
 end
 if mode==2 and state==1 then loss_at=nil;css_at=nil;plan=nil end
 if not loss_at and mode==3 and state==2 and p:read_u16(0x01061b00)==1 and p:read_u32(slots[2].actor)==0 then
  losses=losses+1;loss_at=f
  print(string.format('MK2_SONYA_CPU_CONTINUE_LOSS frame=%d number=%d writes=0 assistance=none',f,losses))
 end
 if loss_at and not css_at then
  local age=f-loss_at
  if age>=20 and age<25 or age>=270 and age<275 then input('Coin',f)end
  if age>=310 and age<315 then input('Start',f)end
 end
 if loss_at and not css_at and mode==4 and state==3 and p:read_u16(slots[2].roster)<=18 then
  css_at=f;plan=route(p:read_u16(slots[2].roster))
  print(string.format('MK2_SONYA_CPU_CONTINUE_SELECT frame=%d roster=%d route=%s writes=0 assistance=none',f,p:read_u16(slots[2].roster),table.concat(plan,',')))
 end
 if css_at and mode==4 and state==3 then
  local age=f-css_at
  for n,key in ipairs(plan)do local begin=20+(n-1)*12;if age>=begin and age<begin+4 then input(key,f)end end
  local confirm=20+#plan*12+24
  if age>=confirm and age<confirm+4 then input('High Punch',f)end
 end
end
emu.register_frame_done(function()
 frame=frame+1;assert(#taps==6,'All actual passive lookup/lifecycle/health/cache taps retained')
 if started then
  local age=frame-started;geometry('FIELD')
  for _,n in ipairs({1,30,60,90,180,240,330,450,900})do
   if age==n then snapshot('postjoin_sonya_cpu_finish_age'..age..'.png')end
  end
  if completed and frame-completed==30 then snapshot('postjoin_sonya_cpu_finish_winner30.png')end
  if completed and age>=900 then
   print(string.format('MK2_SONYA_CPU_FINISH_STOP frame=%d started=%d completed=%d mode=%d losses=%d writes=0 assistance=none',
   frame,started,completed,p:read_u16(0x010601d0),losses));manager.machine:exit()
  end
 end
end)
emu.register_stop(function()
 print(string.format('MK2_SONYA_CPU_FINISH_RESULT frame=%d started=%d completed=%d losses=%d writes=0 assistance=none',
 frame,started or-1,completed or-1,losses))
 for _,tap in ipairs(taps)do tap:remove()end
end)
local f=assert(io.open('mk2ks_native_ui_flow_v2_probe.lua','rb'))
local source=f:read('a');f:close()
local function once(before,after)
 local a,b=source:find(before,1,true);assert(a and not source:find(before,b+1,true),'One exact original physical UI boundary')
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
once('screen:snapshot(name)','_sonya_cpu_snapshot(name)')
once(' if live_at then\n',
 ' if live_at and frame>live_at+180 then _sonya_cpu_continue(frame)end\n if live_at and frame<=live_at+180 then\n')
once('  if frame>=live_at+180 then manager.machine:exit()end',
 '  -- Original finite UI phase completed; release and continue through normal inputs.')
local environment=setmetatable({_sonya_cpu_snapshot=snapshot,_sonya_cpu_continue=continuation},{__index=_ENV})
assert(load(source,'@mk2ks_native_ui_flow_v2_probe.lua::exact_original_UI_then_natural_CPU_finish','t',environment))()
emu.register_frame(function()
 if frame==0 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  print('MK2_CAMPAIGN_GUEST_RAM frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
 end
end)
