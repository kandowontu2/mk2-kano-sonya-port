-- Two genuinely earned human rounds, then real Block U,U,B,D HK command.
-- Physical buttons and passive reads/taps only; no health/state assistance.
local side=assert(tonumber(os.getenv('MK2KS_ORB_SIDE')));assert(side==1 or side==2)
local victim_side=3-side
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local high,low,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN2'].fields,manager.machine.ioport.ports[':IN1'].fields
local buttons={{},{}}
for n=1,2 do
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[n][key]=high['P'..n..' '..key]end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=low['P'..n..' '..key]end
 buttons[n].Coin=system['Coin '..n];buttons[n].Start=system[n==1 and'1 Player Start'or'2 Players Start']
end
local frame,live,finish,approach,started,completed,join,last_mode=0,nil,nil,nil,nil,nil,nil,nil
local css,plans,taps,jobs,retired={},{},{},{},{}
local bones,clouds=0,0
local born_actor,born_seq,cloud_cache,cloud_born={},{},{},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)print(string.format('MK2_ORB_%s frame=%d side=%d age=%d writes=0 assistance=none %s',tag,frame,side,started and frame-started or-1,text or''))end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,id=p:read_u16(a+0x1f0),roster=p:read_u16(s.id),state=p:read_u16(s.state),hp=p:read_u16(s.hp),
  owner=p:read_u32(m+0xc0),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
  pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140),body=p:read_u16(a+0x160)}
end
local function input(n,key)buttons[n][key]:set_value(1);log('INPUT','slot='..n..' key='..key:gsub(' ','_'))end
local function route(first,target)
 local queue={{first,{}}};local seen={[first]=true};local at=1
 while queue[at]do
  local row=queue[at];at=at+1;if row[1]==target then return row[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local base=key=='Left'and 0xffff1400 or key=='Right'and 0xffff1600 or 0xffff1200
   local next_id=p:read_u16(base+row[1]*16)
   if next_id<=18 and not seen[next_id]then local path={table.unpack(row[2])};path[#path+1]=key;queue[#queue+1]={next_id,path};seen[next_id]=true end
  end
 end
 error('No native selector route')
end
local function tap(address,name,fn)
 taps[#taps+1]=p:install_read_tap(address,address+15,name,function(at)
  if at==address and cpu.PC.value==address+16 then fn()end
 end)
end
tap(0xffd7b000,'actual guarded own Sonya second entry',function()
 local s,k=sample(side),sample(victim_side)
 if s and k and s.id==18 and k.id==17 and k.hp==0 and cpu.A8.value==s.actor and cpu.A13.value==s.main and not started then
  started=frame;log('ENTRY',string.format('actor=%08X main=%08X victim=%08X victim_main=%08X gap=%d hp=%d,%d',s.actor,s.main,k.actor,k.main,math.abs(s.x-k.x),s.hp,k.hp))
 end
end)
tap(0xffd78480,'real independent orb worker',function()
 if started then local m=cpu.A13.value;jobs[m]='worker';log('TASK',string.format('kind=worker job=%08X actor=%08X owner=%08X victim=%08X victim_main=%08X child=%08X',m,cpu.A8.value,p:read_u32(m+0xc0),p:read_u32(m+0x140),p:read_u32(m+0x170),p:read_u32(m+0x190)))end
end)
tap(0xff9f2e40,'real native bone constructor',function()
 if started and cpu.A13.value~=0 and p:read_u32(cpu.A13.value+0x250)>=0xffd72800 and p:read_u32(cpu.A13.value+0x250)<0xffd730c0 then
  local m=cpu.A13.value;jobs[m]='bone';born_seq[m]=p:read_u32(m+0x250);retired[m]=nil;bones=bones+1;log('TASK',string.format('kind=bone number=%d job=%08X actor=%08X owner=%08X seq=%08X x=%d y=%d',bones,m,cpu.A8.value,p:read_u32(m+0x60),p:read_u32(m+0x250),p:read_i16(m+0x2f0),p:read_i16(m+0x310)))
 end
end)
tap(0xffd77800,'real own smoke animation task',function()
 if started then local m=cpu.A13.value;jobs[m]='smoke';born_actor[m]=cpu.A8.value;cloud_cache[m]=p:read_u32(cpu.A8.value+0x1a0)-0x100;cloud_born[m]=frame;retired[m]=nil;clouds=clouds+1;log('TASK',string.format('kind=smoke number=%d job=%08X actor=%08X owner=%08X',clouds,m,cpu.A8.value,p:read_u32(m+0xc0)))end
end)
tap(0xff80de20,'actual native effect task retirement',function()
 local m=cpu.A13.value
 if started and jobs[m] then
  local kind=jobs[m]
  local same=kind=='worker' or (kind=='bone' and p:read_u16(m+0x20)==0x10c and p:read_u32(m+0x250)==born_seq[m]) or
   (kind=='smoke' and p:read_u16(m+0x20)==0x201 and cpu.A8.value==born_actor[m] and p:read_u32(m+0xc0)==born_actor[m])
  if same then retired[m]=true;log('RETIRE','kind='..kind..' job='..string.format('%08X',m)..' actor='..string.format('%08X',cpu.A8.value));jobs[m]=nil end
 end
end)
for _,address in ipairs({0xff840450,0xff80e0e0,0xff83efd0})do
 local at=address
 tap(at,'actual native palette/object/cache cleanup',function()
  if started and jobs[cpu.A13.value]then log('CLEANUP',string.format('kernel=%08X job=%08X actor=%08X a0=%08X',at,cpu.A13.value,cpu.A8.value,cpu.A0.value))end
 end)
end
tap(0xffa14860,'own Sonya native winner continuation',function()
 local own=sample(side)
 if started and own and cpu.A8.value==own.actor and cpu.A13.value==own.main and not completed then completed=frame;log('WINNER','main='..string.format('%08X',own.main))end
end)
tap(0xff877790,'actual original command-history comparison',function()
 if finish and not started then log('HISTORY',string.format('wanted=%d actual=%d tick=%d cursor=%08X',cpu.A8.value>>16,cpu.A0.value>>16,cpu.A0.value&0xffff,cpu.A11.value))end
end)
for n=1,2 do
 local number=n
 taps[#taps+1]=p:install_write_tap(slots[n].hp,slots[n].hp+15,'passive real earned health',function(at,data,mask)
  if at==slots[number].hp and mask==0xffff and live then log('HEALTH',string.format('slot=%d before=%d after=%d pc=%08X',number,p:read_u16(at),data&0xffff,cpu.PC.value))end
 end)
end
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'passive body cache overrun guard',function(at,data,mask)
 if cpu.PC.value==0xff838860 then log('OVERRUN',string.format('at=%08X data=%04X mask=%04X',at,data&0xffff,mask))end
end)
local function rgb(age)
 local raw,w,h=screen:pixels();assert(w==400 and h==254 and#raw==406400)
 print(string.format('MK2_ORB_RGB frame=%d age=%d width=%d height=%d bytes=%d hex=%s',frame,age,w,h,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
local function membership(target,head)
 local node=p:read_u32(head);local seen={}
 for i=1,512 do
  if node==target then return 'yes' end
  if not valid(node) or seen[node] then return 'no' end
  seen[node]=true;node=p:read_u32(node)
 end
 return 'overflow'
end
for _,address in ipairs({0xff80e450,0xff80e550})do
 local at=address
 tap(at,'passive real native masked process deletion',function()
  if started and frame-started<=300 then
   local target=cpu.A2.value
   log('MASS',string.format('pc=%08X current=%08X match=%08X mask=%08X target=%08X type=%04X actor=%08X ip=%08X known=%s caller=%08X active=%s free=%s',at,cpu.A13.value,cpu.A0.value,cpu.A1.value,target,valid(target)and p:read_u16(target+0x20)or 0,valid(target)and p:read_u32(target+0xc0)or 0,valid(target)and p:read_u32(target+0xe0)or 0,jobs[target]or 'unknown',p:read_u32(cpu.SP.value),membership(target,0x01068e30),membership(target,0x01068e50)))
  end
 end)
end
local sent=false
for _,address in ipairs({0xff80e0e0,0xff80e100,0xff80e160,0xff80e220})do
 local at=address
 tap(at,'passive independent effect deletion ownership',function()
  if started and frame-started<=300 then
   log('DELETE',string.format('pc=%08X current=%08X a0=%08X a1=%08X a2=%08X a3=%08X caller=%08X',at,cpu.A13.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,p:read_u32(cpu.SP.value)))
  end
 end)
end
-- Non-recursive observers: real repaired cursor and actual child palette.
for _,address in ipairs({0xffd6cf00,0xffd6cf90})do
 local at=address
 tap(at,'passive repaired native orb cursor',function()
  if started and jobs[cpu.A13.value]=='worker' and frame-started<=200 then
   log('CURSOR',string.format('pc=%08X a0=%08X a8=%08X a9=%08X a10=%08X a11=%08X',at,cpu.A0.value,cpu.A8.value,cpu.A9.value,cpu.A10.value,cpu.A11.value))
  end
 end)
end
emu.register_frame(function()
 frame=frame+1;for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if not sent then
  sent=true;local raw={};for at=0xff800000,0xfffffff0,16 do raw[#raw+1]=string.pack('<I2',p:read_u16(at))end;raw=table.concat(raw)
  print(string.format('MK2_ORB_GUEST bytes=%d hex=%s',#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
 if frame>=300 and frame<304 then input(1,'High Punch')end
 if frame>=600 and frame<604 then input(1,'Coin')end
 if frame>=608 and frame<612 then input(2,'Coin')end
 if frame>=620 and frame<624 then input(1,'Start')end
 if join then local age=frame-join;if age<4 then input(1,'Coin')elseif age>=8 and age<12 then input(2,'Coin')elseif age>=20 and age<24 then input(2,'Start')end end
 local mode=p:read_u16(0x010601d0)
 if mode~=last_mode then log('MODE','mode='..mode);last_mode=mode end
 for n=1,2 do
  if mode~=4 then css[n]=nil end
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css[n]then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].id),n==side and 18 or 17)
   if n==1 and not join then join=frame end
   log('SELECT','slot='..n..' target='..(n==side and 18 or 17)..' path='..table.concat(plans[n],','))
  end
  if css[n]and mode==4 then local age=frame-css[n]
   for i,key in ipairs(plans[n])do if age>=56+(i-1)*12 and age<60+(i-1)*12 then input(n,key)end end
   if age>=148 and age<156 then input(n,'High Punch')end
  end
 end
 local own,victim=sample(side),sample(victim_side)
 if not own or not victim or own.id~=18 or victim.id~=17 or own.roster~=18 or victim.roster~=17 or own.owner~=own.actor or victim.owner~=victim.actor then return end
 local forward=own.x<victim.x and'Right'or'Left';local back=forward=='Right'and'Left'or'Right'
 local gap=math.abs(own.x-victim.x);local flag=p:read_u16(0x01061b00)
 if mode==2 and flag==0 and own.hp>0 and victim.hp>0 and own.state==1 and victim.state==1 then
  live=live or frame
  if frame-live>=180 then if gap>80 then input(side,forward)else input(side,'Down');if(frame-live)%42<4 then input(side,'High Punch')end end end
 elseif flag==3 and own.hp>0 and victim.hp==0 and not started then
  finish=finish or frame
  if frame-finish>=65 and not approach then
   if gap<252 then input(side,back)elseif gap>260 then input(side,forward)else approach=frame;log('COMMAND_READY','gap='..gap)end
  end
  if approach then local age=frame-approach
   if age>=10 and age<46 then input(side,'Block')end
   for i,key in ipairs({'Up','Up',back,'Down','High Kick'})do local first=10+(i-1)*8;if age>=first and age<first+3 then input(side,key)end end
  end
 end
 if live and frame%60==0 then log('COMBAT',string.format('mode=%d flag=%d gap=%d hp=%d,%d ids=%d,%d',mode,flag,gap,own.hp,victim.hp,own.id,victim.id))end
end)
emu.register_frame_done(function()
 if started then
  local age=frame-started
  if age<=450 then
   for n=1,2 do local a=sample(n);if a then log('FIELD',string.format('slot=%d actor=%08X main=%08X id=%d roster=%d hp=%d x=%d y=%d floor=%d pose=%08X bank=%04X body=%04X child=%08X',n,a.actor,a.main,a.id,a.roster,a.hp,a.x,a.y,a.floor,a.pose,a.bank,a.body,p:read_u32(a.main+0x190)))end end
   for job,kind in pairs(jobs)do
    if not retired[job]then local actor=p:read_u32(job+0xc0)
     if valid(actor)then log('EFFECT',string.format('kind=%s job=%08X ip=%08X actor=%08X xraw=%08X yraw=%08X pose=%08X bank=%04X body=%04X child=%08X',kind,job,p:read_u32(job+0xe0),actor,p:read_u32(actor+0x80),p:read_u32(actor+0xa0),p:read_u32(actor+0x1d0),p:read_u16(actor+0x140),p:read_u16(actor+0x160),p:read_u32(job+0x190)))end
     local child=p:read_u32(job+0x190)
     if kind=='smoke' and actor==born_actor[job] then
      log('CLOUD_FIELD',string.format('job=%08X actor=%08X type=%04X cloud_age=%d ip=%08X pose=%08X cursor=%08X cache=%08X cache_type=%04X bank=%04X active=%s free=%s',job,actor,p:read_u16(job+0x20),frame-cloud_born[job],p:read_u32(job+0xe0),p:read_u32(actor+0x1d0),p:read_u32(job+0xa0),cloud_cache[job],p:read_u16(cloud_cache[job]+0x20),p:read_u16(actor+0x140),membership(job,0x01068e30),membership(job,0x01068e50)))
     end
     if kind=='smoke' and age>=190 and age<=245 then
      log('LIFETIME',string.format('job=%08X ip=%08X actor=%08X type=%04X next=%08X cadence=%08X cursor=%08X active=%s free=%s',job,p:read_u32(job+0xe0),actor,p:read_u16(job+0x20),p:read_u32(job),p:read_u32(job+0x80),p:read_u32(job+0xa0),membership(job,0x01068e30),membership(job,0x01068e50)))
     end
     if kind=='worker' and valid(child) and age<=220 then
      local bank=p:read_u16(child+0x140)&0xff
      local palette=p:read_u32(0x0105bb30+bank*0x40)
      log('CHILD',string.format('job=%08X child=%08X xraw=%08X yraw=%08X pose=%08X bank=%d palette=%08X cache=%08X cursor=%08X',job,child,p:read_u32(child+0x80),p:read_u32(child+0xa0),p:read_u32(child+0x1d0),bank,palette,p:read_u32(child+0x1a0),p:read_u32(job+0xa0)))
      if age==54 or age==75 or age==135 then
       local active={};for pen=0,31 do active[#active+1]=string.format('%04X',p:read_u16(0x01800000+(bank*256+pen)*16))end
       log('PALETTE',string.format('child=%08X bank=%d source=%08X active=%s',child,bank,palette,table.concat(active,',')))
      end
     end
    end
   end
  end
  if ({[1]=true,[21]=true,[54]=true,[75]=true,[90]=true,[117]=true,[135]=true,[156]=true,[168]=true,[190]=true,[220]=true,[235]=true,[240]=true,[280]=true,[450]=true,[600]=true,[750]=true})[age]then rgb(age)end
  if age>=750 then log('STOP',string.format('started=%d completed=%d bones=%d clouds=%d mode=%d',started,completed or-1,bones,clouds,p:read_u16(0x010601d0)));manager.machine:exit()end
 elseif frame>=8000 then log('STOP','reason=finite_input_test_deadline');manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('started=%d completed=%d bones=%d clouds=%d',started or-1,completed or-1,bones,clouds))
 for _,t in ipairs(taps)do t:remove()end
end)
