-- Real credits, native selection, two earned rounds, physical held-HK release.
assert(not rawget(_G,'MK2_MILEENA_EARNED_V3781_ACTIVE'))
rawset(_G,'MK2_MILEENA_EARNED_V3781_ACTIVE',true)
local name=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local identity=assert(({kano=17,sonya=18})[name])
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local winner=3-side
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local high,system,low=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields,manager.machine.ioport.ports[':IN2'].fields
local buttons={}
for n=1,2 do
 buttons[n]={}
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[n][key]=high['P'..n..' '..key]end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=low['P'..n..' '..key]end
 buttons[n].Coin=system['Coin '..n];buttons[n].Start=system[n==1 and'1 Player Start'or'2 Players Start']
end
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,join,first,finish,approach,action=0,nil,nil,nil,nil,nil
local css,plans,taps={},{},{}
local damage,wins=0,0
local function log(tag,s)print(string.format('MK2_MILEENA_V3781_%s frame=%d victim=%s side=%d writes=0 assistance=none %s',tag,frame,name,side,s or''))end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {a=a,m=m,id=p:read_u16(a+0x1f0),owner=p:read_u32(m+0xc0),hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),pose=p:read_u32(a+0x1d0)}
end
local function press(n,key)buttons[n][key]:set_value(1);log('INPUT','slot='..n..' button='..key:gsub(' ','_'))end
local function route(start,target)
 local queue={{start,{}}};local seen={[start]=true};local index=1
 local adjacency={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
 while queue[index]do
  local item=queue[index];index=index+1;if item[1]==target then return item[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local id=p:read_u16(adjacency[key]+item[1]*16)
   if id<=18 and not seen[id]then local path={table.unpack(item[2])};path[#path+1]=key;queue[#queue+1]={id,path};seen[id]=true end
  end
 end
 error('No native selection route')
end
taps[#taps+1]=p:install_write_tap(slots[side].hp,slots[side].hp+15,'earned victim original damage',function(at,data,mask)
 if mask&0xffff~=0xffff or not first then return end
 local before=p:read_u16(at);local after=data&0xffff
 log('HEALTH',string.format('before=%d after=%d pc=%08X a8=%08X a13=%08X',before,after,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 if cpu.PC.value==0xff836700 and after<before and before<=161 then damage=damage+before-after end
end)
taps[#taps+1]=p:install_read_tap(0xff8d2410,0xff8d241f,'actual stock Mileena second fatality',function(at)
 if at~=0xff8d2410 then return end
 local own,victim=sample(winner),sample(side)
 if not own or not victim or cpu.A8.value~=own.a or cpu.A13.value~=own.m or own.id~=5 or victim.id~=identity or victim.hp~=0 then return end
 action=frame;log('ACTION',string.format('actor=%08X main=%08X victim_actor=%08X victim_main=%08X damage=%d gap=%d',own.a,own.m,victim.a,victim.m,damage,math.abs(own.x-victim.x)))
end)
taps[#taps+1]=p:install_read_tap(0xfffef800+5*32,0xfffef800+5*32+31,'actual native Mileena wins',function(at)
 if at==0xfffef800+5*32 and first and p:read_u16(slots[side].hp)==0 then wins=wins+1;log('WIN','count='..wins..' pc='..string.format('%08X',cpu.PC.value))end
end)
emu.register_frame(function()
 assert(#taps==3);frame=frame+1
 for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if frame>=300 and frame<304 then press(1,'High Punch')end
 if frame>=600 and frame<604 then press(1,'Coin')end
 if frame>=608 and frame<612 then press(2,'Coin')end
 if frame>=620 and frame<624 then press(1,'Start')end
 if join then
  local age=frame-join
  if age>=0 and age<4 then press(1,'Coin')end
  if age>=8 and age<12 then press(2,'Coin')end
  if age>=20 and age<24 then press(2,'Start')end
 end
 local mode=p:read_u16(0x010601d0)
 for n=1,2 do
  if mode~=4 then css[n]=nil end
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css[n]then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].id),n==side and identity or 5)
   if n==1 and not join then join=frame end
   log('SELECT','slot='..n..' target='..(n==side and identity or 5)..' path='..table.concat(plans[n],','))
  end
  if css[n]and mode==4 then
   local age=frame-css[n]
   for i,key in ipairs(plans[n])do if age>=56+(i-1)*12 and age<60+(i-1)*12 then press(n,key)end end
   if age>=148 and age<156 then press(n,'High Punch')end
  end
 end
 local own,victim=sample(winner),sample(side)
 if own and victim and own.id==5 and victim.id==identity and own.owner==own.a and victim.owner==victim.a then
  local forward=own.x<victim.x and'Right'or'Left';local back=forward=='Right'and'Left'or'Right'
  local gap=math.abs(own.x-victim.x);local flag=p:read_u16(0x01061b00)
  if (mode==2 or mode==6)and flag==0 and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then
   if not first then first=frame;log('FIRST_LIVE',string.format('own=%08X:%08X:%d victim=%08X:%08X:%d',own.a,own.m,own.id,victim.a,victim.m,victim.id))end
   if own.hp>0 and victim.hp>0 and frame-first>=180 then
    if gap>80 then press(winner,forward)else press(winner,'Down');if(frame-first)%42<4 then press(winner,'High Punch')end end
   end
  elseif flag==3 and own.hp>0 and victim.hp==0 and not action then
   finish=finish or frame
   if frame-finish>=65 and not approach then
    if gap<42 then press(winner,back)elseif gap>58 then press(winner,forward)else approach=frame;log('APPROACH','gap='..gap)end
   end
   if approach and frame-approach<180 then press(winner,'High Kick')end
   if approach and frame-approach==180 then log('HK_RELEASE','held_fields=180')end
  end
  if frame%15==0 and first then log('STATE',string.format('mode=%d flag=%d hp=%d,%d gap=%d ids=%d,%d poses=%08X,%08X',mode,flag,own.hp,victim.hp,gap,own.id,victim.id,own.pose,victim.pose))end
 end
 if action and frame-action>600 or frame>=7000 then log('HOST_EXIT','action='..(action or-1));manager.machine:exit()end
end)
emu.register_stop(function()log('RESULT',string.format('first=%d damage=%d wins=%d action=%d',first or-1,damage,wins,action or-1));for _,tap in ipairs(taps)do tap:remove()end end)
dofile('mk2ks_cache_provenance_retained_v3780.lua')
