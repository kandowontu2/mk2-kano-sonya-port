-- Genuine two-human rounds and stock Reptile command; physical inputs only.
assert(not rawget(_G,'MK2_REPTILE_V879_ACTIVE'),'Duplicate observer/driver')
rawset(_G,'MK2_REPTILE_V879_ACTIVE',true)
local name=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local identity=assert(({kano=17,sonya=18})[name])
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
assert(side==1 or side==2)
local winner_side=3-side
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local high,system,low=manager.machine.ioport.ports[':IN0'].fields,
 manager.machine.ioport.ports[':IN1'].fields,manager.machine.ioport.ports[':IN2'].fields
local buttons={}
for n=1,2 do
 buttons[n]={}
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do
  buttons[n][key]=high['P'..n..' '..key]
 end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=low['P'..n..' '..key]end
 buttons[n].Coin=system['Coin '..n]
 buttons[n].Start=system[n==1 and '1 Player Start'or'2 Players Start']
end
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,first_live,finish_start,approach_done,action_start,wrap=0,nil,nil,nil,nil,nil
local css,plans,taps={},{},{}
local damage,wins,last_mode=0,0,nil
local join_at=nil
local function log(tag,s)
 print(string.format('MK2_REPTILE_V879_%s frame=%d victim=%s side=%d writes=0 assistance=none %s',tag,frame,name,side,s or''))
end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),
  roster=p:read_u16(s.id),hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),
  pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140),flags=p:read_u16(a+0x160)}
end
local function press(n,key)
 buttons[n][key]:set_value(1);log('INPUT',string.format('slot=%d button=%s',n,key:gsub(' ','_')))
end
local function route(start,target)
 local queue={{start,{}}};local seen={[start]=true};local index=1
 local tables={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
 while queue[index]do
  local item=queue[index];index=index+1
  if item[1]==target then return item[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local id=p:read_u16(tables[key]+item[1]*16)
   if id<=18 and not seen[id]then
    local path={table.unpack(item[2])};path[#path+1]=key
    queue[#queue+1]={id,path};seen[id]=true
   end
  end
 end
 error('No native CSS route')
end
local function tap(address,label,callback)
 taps[#taps+1]=p:install_read_tap(address,address+15,label,function(at)
  if at==address and frame>600 then callback()end
 end)
end
taps[#taps+1]=p:install_write_tap(slots[side].hp,slots[side].hp+15,'actual victim health',function(at,data,mask)
 if at~=slots[side].hp or mask~=0xffff or not first_live then return end
 local before,after=p:read_u16(at),data&0xffff
 log('HEALTH',string.format('before=%d after=%d pc=%08X',before,after,cpu.PC.value))
 if cpu.PC.value==0xff836700 and after<before and before<=161 then damage=damage+before-after end
end)
tap(0xff876fa0,'stock fatality distance gate',function()
 if cpu.A7.value==0xff8c81f0 then
  log('GATE',string.format('action=%08X distance=%d limit=%d actor=%08X main=%08X pc=%08X',
   cpu.A7.value,cpu.A3.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,cpu.PC.value))
 end
end)
tap(0xff8c81f0,'original Reptile head-eating action',function()
 local own,victim=sample(winner_side),sample(side)
 if own and victim and frame%60==0 then log('ACTORS',string.format('mode=%d own=%08X:%08X:%08X:%d:%d victim=%08X:%08X:%08X:%d:%d',mode,own.actor,own.main,own.owner,own.id,own.roster,victim.actor,victim.main,victim.owner,victim.id,victim.roster))end
 if not own or not victim or cpu.A8.value~=own.actor or cpu.A13.value~=own.main or
  own.id~=9 or victim.id~=identity or victim.hp~=0 then return end
 action_start=frame
 log('ACTION',string.format('actor=%08X main=%08X victim_actor=%08X victim_main=%08X damage=%d mode=%d',
  own.actor,own.main,victim.actor,victim.main,damage,p:read_u16(0x010601d0)))
end)
local table_address=p:read_u32(0xff8c8a70)
assert(table_address==0xfffd4000,'Native independent victim rows required')
taps[#taps+1]=p:install_read_tap(table_address,table_address+19*64-1,'native Reptile true victim row',function(at,data,mask)
 if not action_start or mask~=0xffff then return end
 local field=((at-table_address)%64)//16;local row=(at-table_address)//64
 local pcs={0xff8c8aa0,0xff8c8ab0,0xff8c8af0,0xff8c8b30}
 if row~=identity or cpu.PC.value~=pcs[field+1]then return end
 log('ROW',string.format('row=%d field=%d at=%08X data=%04X mask=%04X pc=%08X',row,field,at,data&0xffff,mask,cpu.PC.value))
end)
tap(0xff8c8ec0,'original native victim head descriptor',function()
 if action_start then log('HEAD',string.format('age=%d descriptor=%08X stream=%08X',frame-action_start,cpu.A5.value,cpu.A9.value))end
end)
tap(0xff8c9680,'original native Reptile wrap',function()
 if action_start then wrap=frame;log('WRAP',string.format('age=%d pc=%08X',frame-action_start,cpu.PC.value))end
end)
tap(0xff90c8d0,'actual selected native death palette',function()
 if not action_start then return end
 local a=cpu.A8.value;local own=sample(side)
 if not valid(a)or p:read_u16(a+0x1f0)~=identity then return end
 log('PALETTE',string.format('age=%d pointer=%08X actor=%08X main=%08X id=%d flags=%04X physical_actor=%08X physical_main=%08X owner=%08X pc=%08X',
  frame-action_start,cpu.A0.value,a,cpu.A13.value,p:read_u16(a+0x1f0),p:read_u16(a+0x160),
  own and own.actor or 0,own and own.main or 0,own and own.owner or 0,cpu.PC.value))
end)
taps[#taps+1]=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,'actual native round wins',function(at)
 if first_live and at==0xfffef800+9*32 and p:read_u16(slots[side].hp)==0 then
  wins=wins+1;log('WIN','count='..wins)
 end
end)
taps[#taps+1]=p:install_write_tap(0x01060100,0x010610ff,'reject body-cache global overrun',function(at,data,mask)
 if cpu.PC.value==0xff838860 then log('CACHE_OVERWRITE',string.format('at=%08X data=%04X mask=%04X',at,data&0xffff,mask))end
end)
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if frame>=300 and frame<304 then press(1,'High Punch')end
 if frame>=600 and frame<604 then press(1,'Coin')end
 if frame>=608 and frame<612 then press(2,'Coin')end
 if frame>=620 and frame<624 then press(1,'Start')end
 local mode=p:read_u16(0x010601d0)
 if join_at then
  local age=frame-join_at
  if age>=0 and age<4 then press(1,'Coin')end
  if age>=8 and age<12 then press(2,'Coin')end
  if age>=20 and age<24 then press(2,'Start')end
 end
 if mode~=last_mode then log('MODE',string.format('mode=%d states=%d,%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state)));last_mode=mode end
 for n=1,2 do
  if mode~=4 then css[n]=nil end
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css[n]then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].id),n==side and identity or 9)
   if n==1 and not join_at then join_at=frame;log('JOIN_BEGIN','slot=2')end
   log('SELECT',string.format('slot=%d target=%d path=%s',n,n==side and identity or 9,table.concat(plans[n],',')))
  end
  if css[n]and mode==4 then
   local age=frame-css[n]
   for i,key in ipairs(plans[n])do if age>=56+(i-1)*12 and age<60+(i-1)*12 then press(n,key)end end
   if age>=148 and age<156 then press(n,'High Punch')end
  end
 end
 local own,victim=sample(winner_side),sample(side)
 if not own or not victim or own.id~=9 or victim.id~=identity or own.owner~=own.actor or victim.owner~=victim.actor then return end
 local forward=own.x<victim.x and'Right'or'Left';local back=forward=='Right'and'Left'or'Right'
 local gap=math.abs(own.x-victim.x)
 if (mode==2 or mode==6)and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then
  if not first_live then first_live=frame;log('FIRST_LIVE',string.format('own=%08X victim=%08X ids=%d,%d',own.actor,victim.actor,own.id,victim.id))end
  if p:read_u16(0x01061b00)==0 and own.hp>0 and victim.hp>0 and frame-first_live>=180 then
   if gap>80 then press(winner_side,forward)
   else press(winner_side,'Down');if(frame-first_live)%42<4 then press(winner_side,'High Punch')end end
  end
 elseif mode==3 and own.hp>0 and victim.hp==0 and not action_start then
  finish_start=finish_start or frame
  local age=frame-finish_start
  if age>=65 and not approach_done then
   if gap<130 then press(winner_side,back)
   elseif gap>150 then press(winner_side,forward)
   else approach_done=frame;log('APPROACH','gap='..gap)end
  end
  if approach_done then
   local command_age=frame-approach_done
   if command_age>=10 and command_age<14 or command_age>=20 and command_age<24 then press(winner_side,back)
   elseif command_age>=30 and command_age<34 then press(winner_side,'Down')
   elseif command_age>=40 and command_age<44 then press(winner_side,'Low Punch')end
  end
 end
 if frame%15==0 and first_live then log('STATE',string.format('mode=%d own=%08X:%08X:%d victim=%08X:%08X:%d hp=%d,%d gap=%d poses=%08X,%08X banks=%04X,%04X',
  mode,own.actor,own.main,own.id,victim.actor,victim.main,victim.id,own.hp,victim.hp,gap,own.pose,victim.pose,own.bank,victim.bank))end
end)
emu.register_frame_done(function()
 if action_start and frame-action_start<=300 and(frame-action_start)%10==0 then
  screen:snapshot(string.format('reptile_victim_%d_%03d.png',action_start,frame-action_start))
  log('DISPLAY','age='..(frame-action_start))
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('damage=%d wins=%d first_live=%d action=%d wrap=%d scope=diagnostic_no_full_art_acceptance',damage,wins,first_live or-1,action_start or-1,wrap or-1))
end)
