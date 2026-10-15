-- Genuine coin/start/select, earned two-player wins and native stage inputs.
-- No gameplay memory writes, forced arena, health/position assistance or cheats.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local side=tonumber(os.getenv('MK2KS_STAGE_SIDE')or'1');assert(side==1 or side==2)
local winner=assert(os.getenv('MK2KS_STAGE_WINNER'))
local target_arena=tonumber(os.getenv('MK2KS_STAGE_ARENA')or'6');assert(target_arena==0 or target_arena==1 or target_arena==6)
local case=os.getenv('MK2KS_STAGE_CASE')or'positive';assert(case=='positive'or case=='wrong_command'or case=='far')
local id=assert(({kano=17,sonya=18})[winner]);local victim_id=id==17 and 18 or 17
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local buttons,taps,css,plans,confirmed={},{},{},{},{}
local frame,match,kos,damage=0,0,0,0
local pending,window,command,action,lastmode=true,nil,nil,nil,nil
local rematch_at,action_arena,last_state=nil,nil,nil
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,s)print(string.format('MK2_STAGE_%s frame=%d match=%d side=%d winner=%s writes=0 assistance=none %s',tag,frame,match,side,winner,s or''))end
for n=1,2 do
 buttons[n]={}
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[n][key]=manager.machine.ioport.ports[':IN0'].fields['P'..n..' '..key]end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=manager.machine.ioport.ports[':IN2'].fields['P'..n..' '..key]end
 buttons[n].Coin=manager.machine.ioport.ports[':IN1'].fields['Coin '..n]
 buttons[n].Start=manager.machine.ioport.ports[':IN1'].fields[n==1 and'1 Player Start'or'2 Players Start']
end
local function press(n,key)buttons[n][key]:set_value(1);log('INPUT','slot='..n..' button='..key:gsub(' ','_'))end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return{actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),hp=p:read_u16(s.hp),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210)}
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
taps[#taps+1]=p:install_write_tap(slots[3-side].hp,slots[3-side].hp+15,'earned stage wins',function(at,data,mask)
 if mask~=0xffff or pending or p:read_u16(0x010601d0)~=2 then return end
 local before,after=p:read_u16(at),data&0xffff;local h,v=sample(side),sample(3-side)
 if before>161 or after>=before or not h or not v or h.id~=id or v.id~=victim_id then return end
 damage=damage+before-after;if after==0 then kos=kos+1 end
 log('DAMAGE',string.format('before=%d after=%d total=%d kos=%d pc=%08X own=%08X target=%08X',before,after,damage,kos,cpu.PC.value,h.actor,v.actor))
end)
for _,entry in ipairs({0xfffaa200,0xfffaa400,0xff876d20,0xff876e50,0xff876e80,0xff876f40,
 0xff877000,0xff877120,0xff8771f0,0xff877270,0xff877280,0xff877300,0xff877350,0xff8773a0,0xff877420,
 0xff8bdde0,0xff8bdfe0,0xff861350})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'native stage entry',function(at)
  if at~=entry or cpu.PC.value~=at+16 or not window then return end
  if entry==0xff8bdde0 or entry==0xff8bdfe0 then action=action or frame;action_arena=action_arena or p:read_u16(0x01061ac0)end
  local a=cpu.A8.value
  log('ENTRY',string.format('entry=%08X arena=%d a8=%08X a13=%08X id=%d a0=%08X a1=%08X a3=%08X a11=%08X',entry,p:read_u16(0x01061ac0),a,cpu.A13.value,valid(a)and p:read_u16(a+0x1f0)or-1,cpu.A0.value,cpu.A1.value,cpu.A3.value,cpu.A11.value))
 end)
end
emu.register_frame(function()
 frame=frame+1
 if frame>=12000 then log('HOST_BOUND','maximum_fields=12000');manager.machine:exit();return end
 for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if frame==1 then
  log('BOOT','own_id='..id..' victim_id='..victim_id..' guest_writes=0 target_arena='..target_arena..' command_case='..case)
  -- No raw guest capture.
 end
 if frame>=300 and frame<304 then press(1,'High Punch')end
 local mode=p:read_u16(0x010601d0);local arena=p:read_u16(0x01061ac0)
 if mode~=lastmode then log('MODE','mode='..mode..' arena='..arena..' states='..p:read_u16(slots[1].state)..','..p:read_u16(slots[2].state));lastmode=mode end
 for n=1,2 do
  if frame>=600 and frame<604 or frame>=640 and frame<644 then press(n,'Coin')end
  if n==1 and frame>=620 and frame<624 or n==2 and frame>=660 and frame<664 then press(n,'Start')end
  if mode==4 and p:read_u16(slots[n].state)==3 and p:read_u16(slots[n].roster)<=18 then
   if not css[n] then
    pending=true;css[n]=frame;confirmed[n]=nil
    local target=n==side and id or victim_id
    plans[n]=route(p:read_u16(slots[n].roster),target)
    log('SELECT','slot='..n..' target='..target..' route='..table.concat(plans[n],','))
   end
   local age=frame-css[n]
   for index,key in ipairs(plans[n])do local at=56+(index-1)*12;if age>=at and age<at+4 then press(n,key)end end
   if age==146 then
    local actual=p:read_u16(slots[n].roster);local target=n==side and id or victim_id
    log('SELECT_ID','slot='..n..' actual='..actual..' target='..target);assert(actual==target)
   end
   if age>=148 and age<156 then press(n,'High Punch');confirmed[n]=true end
  elseif mode~=4 then css[n]=nil;plans[n]=nil;confirmed[n]=nil end
 end
 local h,v=sample(side),sample(3-side)
 if mode==2 and pending and h and v and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then
  assert(h.id==id and v.id==victim_id and h.owner==h.actor and v.owner==v.actor)
  match=match+1;pending=false;kos=0;damage=0;window=nil;command=nil;rematch_at=nil
  log('MATCH','arena='..arena..' ids='..h.id..','..v.id)
 end
 if not action and not pending and h and v and (mode==2 or mode==7)and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then
  assert(h.id==id and v.id==victim_id and h.owner==h.actor and v.owner==v.actor)
  local finish=p:read_u16(0x01061b00)
  if frame%120==0 then log('LIVE',string.format('mode=%d arena=%d finish=%d kos=%d hp=%d,%d x=%d,%d',mode,arena,finish,kos,h.hp,v.hp,h.x,v.x))end
  local forward=h.x<v.x and'Right'or'Left';local back=forward=='Right'and'Left'or'Right'
  if mode==2 and finish==0 and h.hp>0 and v.hp>0 then
   if math.abs(h.x-v.x)>62 then press(side,forward)
   else press(side,'Down');if frame%22<4 then press(side,'Low Kick')end end
  elseif finish==3 and kos==2 then
   if not window then window=frame;log('WINDOW','arena='..arena..' kos='..kos..' damage='..damage);assert(damage==322)end
   if arena==target_arena then
    if not command and frame-window>=65 then
     if case=='far'and math.abs(h.x-v.x)<130 then press(side,back)
     elseif case~='far'and math.abs(h.x-v.x)>65 then press(side,forward)
     else command=frame;log('COMMAND','arena='..arena..' gap='..math.abs(h.x-v.x))end
    end
    if command then
     local age=frame-command
     if age>=16 and age<64 then press(side,'Low Punch');press(side,'Low Kick')end
     if age>=0 and age<70 then press(side,'Down')end
     if age>=48 and age<52 then press(side,'High Punch')end
    end
   end
  end
 end
 -- A normal paid challenger after an expired finish window. Never touch state.
 if not action and not command and window and frame-window>=720 and mode~=4 then
  rematch_at=rematch_at or frame
  local age=(frame-rematch_at)%180
  if age<4 then press(3-side,'Coin')elseif age>=20 and age<24 then press(3-side,'Start')end
 end
end)
emu.register_frame_done(function()
 if not action and command and frame-command>=1100 then
  log('REJECT_END','mode='..p:read_u16(0x010601d0)..' arena='..p:read_u16(0x01061ac0));manager.machine:exit()
 end
 if not action then return end
 local age=frame-action;local h,v=sample(side),sample(3-side)
 local state=string.format('mode=%d arena=%d finish=%d own=%08X main=%08X id=%d pose=%08X x=%d y=%d victim=%08X victim_main=%08X victim_id=%d victim_pose=%08X victim_x=%d victim_y=%d',
  p:read_u16(0x010601d0),p:read_u16(0x01061ac0),p:read_u16(0x01061b00),h and h.actor or 0,h and h.main or 0,h and h.id or-1,h and h.pose or 0,h and h.x or-1,h and h.y or-1,
  v and v.actor or 0,v and v.main or 0,v and v.id or-1,v and v.pose or 0,v and v.x or-1,v and v.y or-1)
 if age<=800 or state~=last_state then log('FIELD','age='..age..' '..state);last_state=state end
 if age>=1100 then manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('matches=%d kos=%d damage=%d window=%d command=%d action=%d action_arena=%d guest_writes=0',match,kos,damage,window or-1,command or-1,action or-1,action_arena or-1))
 for _,tap in ipairs(taps)do tap:remove()end
end)

taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'actual earned uppercut',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=at+16 or not command or p:read_u16(0x01061ac0)~=0 then return end
 local own=sample(side)
 if not own or own.id~=id or cpu.A8.value~=own.actor then return end
 action=action or frame;action_arena=0
 log('ACID_UPPERCUT_ENTRY',string.format('entry=%08X pc=%08X actor=%08X main=%08X a8=%08X a13=%08X id=%d',at,cpu.PC.value,own.actor,own.main,cpu.A8.value,cpu.A13.value,own.id))
end)

emu.register_frame_done(function()
 if not command or frame-command>200 then return end
 for n=1,2 do
  local row=sample(n)
  if row then
   log('ACID_ACTION_FIELD',string.format('age=%d slot=%d actor=%08X main=%08X owner=%08X id=%d native_action=%d flags=%04X body=%04X x=%d y=%d floor=%d hp=%d mode=%d finish=%d',
    frame-command,n,row.actor,row.main,row.owner,row.id,p:read_u16(row.main+0x1f0),row.flags,p:read_u16(row.actor+0x160),row.x,row.y,p:read_i16(row.main+0x200),row.hp,p:read_u16(0x010601d0),p:read_u16(0x01061b00)))
  end
 end
end)
