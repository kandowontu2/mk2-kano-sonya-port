-- Genuine two-player rounds and added fighter's own native Babality input.
-- No guest writes, cheats, identity substitutions or diagnostic state setup.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local side=tonumber(os.getenv('MK2KS_BABY_WINNER_SIDE')or'1')
assert(side==1 or side==2)
local victim_name=assert(os.getenv('MK2KS_BABY_VICTIM'))
local victim_id=assert(({liu_kang=1,kano=17,sonya=18})[victim_name])
local winner_name=assert(os.getenv('MK2KS_BABY_WINNER'))
local winner_id=assert(({kano=17,sonya=18,kitana=4})[winner_name])
local command_case=os.getenv('MK2KS_BABY_CASE')or'positive'
assert(command_case=='positive'or command_case=='wrong_direction'or command_case=='punch_used')
local wanted={[side]=6,[3-side]=victim_id}
local morph_due,id_observer=nil,nil
local punch_rounds={}
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local buttons={}
for n=1,2 do
 buttons[n]={}
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do
  buttons[n][key]=manager.machine.ioport.ports[':IN0'].fields['P'..n..' '..key]
 end
 for _,key in ipairs({'Low Punch','Low Kick'})do
  buttons[n][key]=manager.machine.ioport.ports[':IN2'].fields['P'..n..' '..key]
 end
 buttons[n].Coin=manager.machine.ioport.ports[':IN1'].fields['Coin '..n]
 buttons[n].Start=manager.machine.ioport.ports[':IN1'].fields[n==1 and'1 Player Start'or'2 Players Start']
end
local frame,wins,damage,window,action=0,0,0,nil,nil
local native_kos=0
local css,plans,exits={},{},{}
local taps={}
local entry_seen={}
local previous_state
local baby_actor,baby_frame
local baby_reused=false
local baby_table=p:read_u32(0xff87eb30)
local function log(tag,value)
 print(string.format('MK2_NATIVE_BABY_%s frame=%d winner_slot=%d victim=%s writes=0 assistance=none %s',tag,frame,side,victim_name,value or''))
end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),
  hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
  action=p:read_u16(m+0x1f0),flags=p:read_u16(m+0x210),pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140)}
end
local function route(start,target)
 local queue={{start,{}}};local seen={[start]=true};local cursor=1
 local adjacent={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
 while queue[cursor]do
  local item=queue[cursor];cursor=cursor+1
  if item[1]==target then return item[2]end
  for _,button in ipairs({'Left','Right','Down'})do
   local id=p:read_u16(adjacent[button]+item[1]*16)
   if id<=18 and not seen[id]then
    local path={};for _,step in ipairs(item[2])do path[#path+1]=step end
    path[#path+1]=button;queue[#queue+1]={id,path};seen[id]=true
   end
  end
 end
 error('No native selection route')
end
local function press(n,button)
 buttons[n][button]:set_value(1);log('INPUT','slot='..n..' button='..button:gsub(' ','_'))
end
taps[#taps+1]=p:install_write_tap(slots[3-side].hp,slots[3-side].hp+15,'native baby earned combat',function(at,data,mask)
 if mask~=0xffff or p:read_u16(0x010601d0)~=2 then return end
 local before,after=p:read_u16(at),data&0xffff
 if before>161 or after>=before then return end
 local h,v=sample(side),sample(3-side)
 if not h or not v or (h.id~=6 and h.id~=winner_id)or v.id~=victim_id then return end
 damage=damage+before-after
 if after==0 then native_kos=native_kos+1 end
 log('DAMAGE',string.format('before=%d after=%d total=%d pc=%08X a8=%08X a13=%08X own=%08X victim_actor=%08X',before,after,damage,cpu.PC.value,cpu.A8.value,cpu.A13.value,h.actor,v.actor))
end)
taps[#taps+1]=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,'native baby round wins',function(at)
 local own=sample(side)
 if not own or cpu.PC.value~=0xff8296b0 or(at~=0xfffef800+own.id*32 and at~=0xfffef800+own.roster*32)or own.roster~=6 or own.owner~=own.actor or p:read_u16(slots[side].hp)==0 or p:read_u16(slots[3-side].hp)~=0 then return end
 wins=wins+1;log('WIN',string.format('wins=%d total_damage=%d pc=%08X entry=%08X actor_id=%d roster=%d actor=%08X main=%08X owner=%08X hp=%d victim_hp=%d',wins,damage,cpu.PC.value,at,own.id,own.roster,own.actor,own.main,own.owner,own.hp,p:read_u16(slots[3-side].hp)))
end)
for _,entry in ipairs({0xff87e120,0xff87e230,0xff87e300,0xff87e520,0xff87e8d0,0xff87eb20,0xffa1e700})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'native baby entry',function(at)
  if at~=entry or not window then return end
  if entry==0xffa1e700 and entry_seen[entry]then return end
  entry_seen[entry]=true
  if entry==0xff87e520 then action=action or frame end
  log('ENTRY',string.format('entry=%08X pc=%08X a8=%08X a13=%08X a0=%08X a11=%08X',entry,cpu.PC.value,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A11.value))
 end)
end
taps[#taps+1]=p:install_read_tap(baby_table,baby_table+19*32-1,'native baby victim lookup',function(at,data,mask)
 if not window then return end
 log('LOOKUP',string.format('entry=%08X value=%04X mask=%04X pc=%08X a8=%08X a13=%08X live_id=%d',at,data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,valid(cpu.A8.value)and p:read_u16(cpu.A8.value+0x1f0)or -1))
end)
taps[#taps+1]=p:install_read_tap(0xff87ebc0,0xff87ebcf,'native baby constructed',function(at)
 if at~=0xff87ebc0 or not window then return end
 baby_actor=cpu.A8.value;baby_frame=cpu.A5.value
 local s=sample(3-side)
 log('CONSTRUCT',string.format('actor=%08X frame_pointer=%08X original_victim=%08X victim_id=%d table=%08X pc=%08X',baby_actor,baby_frame,cpu.A10.value,s and s.id or -1,baby_table,cpu.PC.value))
end)
for n=1,2 do
 for _,pointer in ipairs({slots[n].actor,slots[n].main})do
  taps[#taps+1]=p:install_write_tap(pointer,pointer+31,'native babality actor retirement',function(at,data,mask)
   if not window then return end
   log('RETIRE',string.format('slot=%d entry=%08X value=%04X mask=%04X before=%04X pc=%08X',n,at,data&0xffff,mask,p:read_u16(at),cpu.PC.value))
  end)
 end
end
emu.register_frame_done(function()
 if not window then return end
 local age=frame-window
 if age%8==0 then
  for n=1,2 do
   local s=sample(n)
   if s then log('FIELD',string.format('age=%d slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d hp=%d x=%d y=%d floor=%d action=%04X flags=%04X pose=%08X bank=%04X pc=%08X',age,n,s.actor,s.main,s.owner,s.id,s.roster,s.hp,s.x,s.y,s.floor,s.action,s.flags,s.pose,s.bank,cpu.PC.value))end
  end
  if baby_actor and valid(baby_actor)and p:read_u32(baby_actor+0x1a0)==baby_frame then
   local bank=p:read_u16(baby_actor+0x140)&0x7f00
   local colors={};for index=0,31 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01800000+(bank+index)*16))end
   log('BABY',string.format('age=%d actor=%08X x=%d y=%d width=%d height=%d graphic=%08X bank=%04X colors=%s',age,baby_actor,p:read_i16(baby_actor+0x90),p:read_i16(baby_actor+0xb0),p:read_u16(baby_actor+0x120),p:read_u16(baby_actor+0x130),p:read_u32(baby_actor+0x1a0),bank,table.concat(colors,',')))
  elseif baby_actor and not baby_reused then
   baby_reused=true;log('BABY_REUSED',string.format('age=%d actor=%08X next_graphic=%08X',age,baby_actor,p:read_u32(baby_actor+0x1a0)))
  end
  
 end
 if age>=720 then manager.machine:exit()end
end)
emu.register_frame(function()
 frame=frame+1
 if frame>=5500 then log('HOST_BOUND','limit=5500');manager.machine:exit();return end
 for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if frame==1 then
  log('BOOT','schema=10 own_id='..winner_id..' winner='..winner_name..' case='..command_case..' victim_id='..victim_id..' guest_writes=0 baby_table='..string.format('%08X',baby_table))
 end
 if frame>=300 and frame<304 then press(1,'High Punch')end
 local mode=p:read_u16(0x010601d0)
 for n=1,2 do
  -- Default MKII pricing takes two credits per player. Buy and start P1,
  -- then buy/start P2 separately; simultaneous starts let P2 consume them.
  if frame>=600 and frame<604 or frame>=640 and frame<644 then press(n,'Coin')end
  if n==1 and frame>=620 and frame<624 or n==2 and frame>=660 and frame<664 then press(n,'Start')end
  if not css[n] and frame>700 and mode==4 and p:read_u16(slots[n].state)==3 and p:read_u16(slots[n].roster)<=18 then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].roster),wanted[n])
   log('SELECT','slot='..n..' initial='..p:read_u16(slots[n].roster)..' target='..wanted[n]..' route='..table.concat(plans[n],','))
  end
  if css[n] and not exits[n] then
   local age=frame-css[n]
   for i,key in ipairs(plans[n])do local at=56+(i-1)*12;if age>=at and age<at+4 then press(n,key)end end
   if age==146 then log('SELECT_ID','slot='..n..' actual='..p:read_u16(slots[n].roster)..' target='..wanted[n]);end
   if age>=148 and age<156 then press(n,'High Punch')end
   if age>148 and mode~=4 then exits[n]=frame end
  end
 end
 local h,v=sample(side),sample(3-side)
 local state=string.format('mode=%d states=%d,%d roster=%d,%d winner=%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u16(0x01061b00))
 if state~=previous_state then log('STATE',state);previous_state=state end
 -- Once the native action is accepted, victim Main legitimately owns the
 -- newly allocated baby object. Human ownership applies before that handoff.
 if not action and (mode==2 or mode==7) and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 and h and v then
  assert((h.id==6 or h.id==winner_id)and h.roster==6 and v.id==victim_id and h.owner==h.actor and v.owner==v.actor,'Actual Shang roster/current form and native victim')
  if not id_observer then
   id_observer=p:install_write_tap(h.actor+0x1f0,h.actor+0x1ff,'actual native morph ID',function(at,data,mask)
    local current=sample(side)
    if not current or at~=current.actor+0x1f0 or mask&0xffff~=0xffff then return end
    log('MORPH_STORE',string.format('old=%d id=%d roster=%d actor=%08X main=%08X pc=%08X a9=%08X a0=%08X',
     current.id,data&0xffff,current.roster,current.actor,current.main,cpu.PC.value,cpu.A9.value,cpu.A0.value))
   end)
   taps[#taps+1]=id_observer
  end
  local winner=p:read_u16(0x01061b00)
  if frame%60==0 then log('LIVE',string.format('own_id=%d victim_id=%d own=%08X own_main=%08X target=%08X target_main=%08X health=%d,%d winner=%d',h.id,v.id,h.actor,h.main,v.actor,v.main,h.hp,v.hp,winner))end
  if mode==2 and winner==0 and h.hp>0 and v.hp>0 then
   if native_kos==1 and v.hp<=32 and h.id==6 and not morph_due then
    morph_due=frame+80;log('MORPH_PLAN','due='..morph_due..' victim_hp='..v.hp)
   end
   if morph_due and frame-morph_due<40 then
    local age=frame-morph_due
    local back=h.x<v.x and'Left'or'Right'
    if winner_name=='kano' then
     if age>=0 and(age<2 or(age>=8 and age<10))then press(side,back)end
     if age>=4 and age<6 then press(side,'Down')end
     if age>=8 and age<10 then press(side,'Low Kick')end
    elseif age>=0 and age<8 then
     press(side,'Down');press(side,'Low Punch');press(side,'Block')
    end
   elseif math.abs(h.x-v.x)>62 then press(side,h.x<v.x and'Right'or'Left')
   -- Native MKII babality FF87E180..E230 checks the winning player's
   -- HP/LP use counters, not Block. Earn both rounds with kicks only.
   elseif command_case=='punch_used'and not punch_rounds[native_kos]then
    punch_rounds[native_kos]=true;press(side,'High Punch');log('PUNCH_ELIGIBILITY','round='..native_kos)
   else press(side,'Down');if frame%22<4 then press(side,'Low Kick')end end
  elseif winner==3 and native_kos==2 then
   if not window then window=frame;log('FINISH_WINDOW','wins='..wins..' native_kos='..native_kos..' damage='..damage..' hp_counters='..p:read_u16(0x01061e40)..','..p:read_u16(0x01061e50)..' lp_counters='..p:read_u16(0x01061e60)..','..p:read_u16(0x01061e70));end
   local age=frame-window
   local forward=h.x<v.x and'Right'or'Left'
   if command_case=='wrong_direction'then forward=forward=='Right'and'Left'or'Right'end
   if winner_name=='kano'then
    if age>=20 and age<24 or age>=32 and age<36 then press(side,forward)end
    if age>=44 and age<48 or age>=56 and age<60 then press(side,'Down')end
    if age>=58 and age<62 then press(side,'Low Kick')end
   elseif winner_name=='sonya'then
    if age>=20 and age<24 or age>=32 and age<36 then press(side,'Down')end
    if age>=44 and age<48 then press(side,forward)end
    if age>=46 and age<50 then press(side,'Low Kick')end
   else
    if age>=20 and age<24 or age>=32 and age<36 or age>=44 and age<48 then press(side,'Down')end
    if age>=46 and age<50 then press(side,'Low Kick')end
   end
  end
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('wins=%d damage=%d window=%d action=%d winner=%s case=%s native_rows_supported=independent_check_pending scope=own_babality_observation_not_full_finisher_acceptance',wins,damage,window or -1,action or -1,winner_name,command_case))
 for _,tap in ipairs(taps)do tap:remove()end
end)
