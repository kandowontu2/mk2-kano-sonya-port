-- Cold native selection, earned combat and true-ID Friendship input.
-- No guest RAM writes, cheats, health assistance or identity substitution.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local side=tonumber(os.getenv('MK2KS_FRIEND_SIDE')or'1');assert(side==1 or side==2)
local winner=assert(os.getenv('MK2KS_FRIEND_WINNER'))
local id=assert(({kano=17,sonya=18})[winner]);local victim_id=id==17 and 18 or 17
local case=os.getenv('MK2KS_FRIEND_CASE')or'positive';assert(case=='positive'or case=='wrong_command'or case=='punch_used')
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local buttons,plans,css,exits,taps,punch_rounds={},{},{},{},{},{}
for n=1,2 do
 buttons[n]={}
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[n][key]=manager.machine.ioport.ports[':IN0'].fields['P'..n..' '..key]end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=manager.machine.ioport.ports[':IN2'].fields['P'..n..' '..key]end
 buttons[n].Coin=manager.machine.ioport.ports[':IN1'].fields['Coin '..n]
 buttons[n].Start=manager.machine.ioport.ports[':IN1'].fields[n==1 and'1 Player Start'or'2 Players Start']
end
local frame,kos,damage,window,action,command_start=0,0,0,nil,nil,nil
local cleanup,part,last_part,last_pose,retired=false,nil,nil,nil,false
local morph_due,id_observer=nil,nil
local action_address=0xff800000+(id==17 and 0xf9a00 or 0xf9c00)*8
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,s)print(string.format('MK2_FRIEND_%s frame=%d side=%d winner=%s case=%s writes=0 assistance=none %s',tag,frame,side,winner,case,s or''))end
local function press(n,key)buttons[n][key]:set_value(1);log('INPUT','slot='..n..' button='..key:gsub(' ','_'))end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return{actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),hp=p:read_u16(s.hp),
  pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140),flags=p:read_u16(m+0x210)}
end
local function route(start,target)
 local queue={{start,{}}};local seen={[start]=true};local cursor=1
 local adjacent={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
 while queue[cursor]do
  local item=queue[cursor];cursor=cursor+1;if item[1]==target then return item[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local next_id=p:read_u16(adjacent[key]+item[1]*16)
   if next_id<=18 and not seen[next_id]then
    local path={};for _,step in ipairs(item[2])do path[#path+1]=step end
    path[#path+1]=key;queue[#queue+1]={next_id,path};seen[next_id]=true
   end
  end
 end
 error('Missing native selection route')
end
taps[#taps+1]=p:install_write_tap(slots[3-side].hp,slots[3-side].hp+15,'earned friendship wins',function(at,data,mask)
 if mask~=0xffff or p:read_u16(0x010601d0)~=2 then return end
 local before,after=p:read_u16(at),data&0xffff;local h,v=sample(side),sample(3-side)
 if before>161 or after>=before or not h or not v or (h.id~=6 and h.id~=id)or v.id~=victim_id then return end
 damage=damage+before-after;if after==0 then kos=kos+1 end
 log('DAMAGE',string.format('before=%d after=%d total=%d kos=%d pc=%08X own=%08X target=%08X',before,after,damage,kos,cpu.PC.value,h.actor,v.actor))
end)
for _,entry in ipairs({0xff880770,0xff8808c0,0xff880960,0xff880d30,0xff880bf0,0xff880cc0,action_address,
 0xff800000+0xf9e00*8,0xff800000+0xf9e80*8})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'native friendship entry',function(at)
  if at~=entry or not window then return end
  if entry==action_address then action=action or frame end
  if entry==0xff880cc0 then cleanup=true end
  local actor=cpu.A8.value
  log('ENTRY',string.format('entry=%08X a8=%08X a13=%08X id=%d a0=%08X a11=%08X',entry,actor,cpu.A13.value,valid(actor)and p:read_u16(actor+0x1f0)or-1,cpu.A0.value,cpu.A11.value))
 end)
end
taps[#taps+1]=p:install_read_tap(0x01061e40,0x01061e7f,'native original eligibility counter read',function(at,data,mask)
 if not window or cpu.PC.value<0xff880770 or cpu.PC.value>=0xff880a70 then return end
 log('ELIGIBILITY_READ',string.format('at=%08X data=%04X mask=%08X pc=%08X a8=%08X a13=%08X',at,data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
end)
emu.register_frame(function()
 frame=frame+1
 if frame>=5500 then log('HOST_BOUND','limit=5500');manager.machine:exit();return end
 for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if frame==1 then
  log('BOOT','own_id='..id..' victim_id='..victim_id..' guest_writes=0')
  for at=0xff880770,0xff880890,16 do
   log('ORIGINAL_GATE_WORD',string.format('at=%08X word=%04X',at,p:read_u16(at)))
  end
 end
 if frame>=300 and frame<304 then press(1,'High Punch')end
 local mode=p:read_u16(0x010601d0)
 for n=1,2 do
  if frame>=600 and frame<604 or frame>=640 and frame<644 then press(n,'Coin')end
  if n==1 and frame>=620 and frame<624 or n==2 and frame>=660 and frame<664 then press(n,'Start')end
  local target=n==side and 6 or victim_id
  if not css[n]and frame>700 and mode==4 and p:read_u16(slots[n].state)==3 and p:read_u16(slots[n].roster)<=18 then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].roster),target);log('SELECT','slot='..n..' target='..target..' route='..table.concat(plans[n],','))
  end
  if css[n]and not exits[n]then
   local age=frame-css[n]
   for index,key in ipairs(plans[n])do local at=56+(index-1)*12;if age>=at and age<at+4 then press(n,key)end end
   if age==146 then log('SELECT_ID','slot='..n..' actual='..p:read_u16(slots[n].roster)..' target='..target)end
   if age>=148 and age<156 then press(n,'High Punch')end
   if age>148 and mode~=4 then exits[n]=frame end
  end
 end
 local h,v=sample(side),sample(3-side)
 if not action and(mode==2 or mode==7)and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 and h and v then
  assert((h.id==6 or h.id==id)and h.roster==6 and v.id==victim_id and h.owner==h.actor and v.owner==v.actor,'True native Shang roster/current-form ownership')
  if not id_observer then
   id_observer=p:install_write_tap(h.actor+0x1f0,h.actor+0x1ff,'actual native morph ID',function(at,data,mask)
    local current=sample(side)
    if not current or at~=current.actor+0x1f0 or mask&0xffff~=0xffff then return end
    log('MORPH_STORE',string.format('old=%d id=%d roster=%d actor=%08X main=%08X pc=%08X a9=%08X a0=%08X',
     current.id,data&0xffff,current.roster,current.actor,current.main,cpu.PC.value,cpu.A9.value,cpu.A0.value))
   end)
   taps[#taps+1]=id_observer
  end
  local finish=p:read_u16(0x01061b00)
  if frame%120==0 then log('LIVE',string.format('mode=%d finish=%d kos=%d hp=%d,%d x=%d,%d flags=%04X',mode,finish,kos,h.hp,v.hp,h.x,v.x,h.flags))end
  if mode==2 and finish==0 and h.hp>0 and v.hp>0 then
   if kos==1 and v.hp<=32 and h.id==6 and not morph_due then
    morph_due=frame+80;log('MORPH_PLAN','due='..morph_due..' victim_hp='..v.hp)
   end
   if morph_due and frame-morph_due<40 then
    local age=frame-morph_due
    local back=h.x<v.x and'Left'or'Right'
    if winner=='kano' then
     if age>=0 and(age<2 or(age>=8 and age<10))then press(side,back)end
     if age>=4 and age<6 then press(side,'Down')end
     if age>=8 and age<10 then press(side,'Low Kick')end
    elseif age>=0 and age<8 then
     press(side,'Down');press(side,'Low Punch');press(side,'Block')
    end
   elseif math.abs(h.x-v.x)>62 then press(side,h.x<v.x and'Right'or'Left')
   elseif case=='punch_used'and not punch_rounds[kos]then punch_rounds[kos]=true;press(side,'High Punch')
   else press(side,'Down');if frame%22<4 then press(side,'Low Kick')end end
  elseif finish==3 and kos==2 then
   if not window then
    window=frame;log('WINDOW',string.format('kos=%d damage=%d hp_counters=%d,%d lp_counters=%d,%d',kos,damage,p:read_u16(0x01061e40),p:read_u16(0x01061e50),p:read_u16(0x01061e60),p:read_u16(0x01061e70)))
   end
   local forward=h.x<v.x and'Right'or'Left';local back=forward=='Right'and'Left'or'Right'
   if not command_start then
    if math.abs(h.x-v.x)<160 then press(side,back);return end
    command_start=frame;log('COMMAND_POSITION','gap='..math.abs(h.x-v.x))
   end
   local age=frame-command_start
   if winner=='kano'then
    if age>=15 and age<25 then press(side,'Down')end
    for _,step in ipairs({{20,'Low Kick'},{30,'Block'},{40,case=='wrong_command'and'Low Kick'or'Block'},{50,'High Kick'}})do
     if age>=step[1]and age<step[1]+4 then press(side,step[2])end
    end
   else
    for _,step in ipairs({{20,back},{30,forward},{40,case=='wrong_command'and forward or back},{50,'Down'},{52,'Block'}})do
     if age>=step[1]and age<step[1]+4 then press(side,step[2])end
    end
   end
  end
 end
end)
emu.register_frame_done(function()
 if not window then return end
 local age=frame-window
 local h,v=sample(side),sample(3-side)
 if action then
  local action_age=frame-action
  if h and h.id==id and h.pose~=last_pose then
   log('POSE',string.format('age=%d actor=%08X main=%08X owner=%08X id=%d roster=%d pose=%08X x=%d y=%d floor=%d bank=%04X',action_age,h.actor,h.main,h.owner,h.id,h.roster,h.pose,h.x,h.y,h.floor,h.bank));last_pose=h.pose
  end
  if h and h.id==id then
   local child=p:read_u32(h.main+0x190)
   if valid(child)and p:read_u32(child+0x1d0)>=0xfe9d2610 and p:read_u32(child+0x1d0)<=0xfe9d2790 then
    part=part or child
    local pose=p:read_u32(child+0x1d0)
    if pose~=last_part then
     local bank=p:read_u16(child+0x140)&0x7f00;local colors={}
     for index=0,15 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01800000+(bank+index)*16))end
     log('PART',string.format('age=%d actor=%08X pose=%08X x=%d y=%d flags=%04X bank=%04X colors=%s',action_age,child,pose,p:read_i16(child+0x90),p:read_i16(child+0xb0),p:read_u16(child+0xf0),bank,table.concat(colors,',')));last_part=pose
    end
   end
  elseif not retired then retired=true;log('RETIRE','age='..action_age)end
 end
 if age%8==0 then
  log('FIELD',string.format('age=%d mode=%d finish=%d ids=%d,%d',age,p:read_u16(0x010601d0),p:read_u16(0x01061b00),h and h.id or-1,v and v.id or-1))
 end
 if(action and frame-action>=650)or(not action and age>=720)then manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('kos=%d damage=%d window=%d action=%d cleanup=%s retired=%s guest_writes=0',kos,damage,window or-1,action or-1,tostring(cleanup),tostring(retired)))
 for _,tap in ipairs(taps)do tap:remove()end
end)
