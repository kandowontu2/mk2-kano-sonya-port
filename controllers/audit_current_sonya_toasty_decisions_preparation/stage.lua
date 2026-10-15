-- Genuine coin/start/select, earned two-player wins and native stage inputs.
-- No gameplay memory writes, forced arena, health/position assistance or cheats.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local side=tonumber(os.getenv('MK2KS_STAGE_SIDE')or'1');assert(side==1 or side==2)
local winner=assert(os.getenv('MK2KS_STAGE_WINNER'))
local target_arena=tonumber(os.getenv('MK2KS_STAGE_ARENA')or'6');assert(target_arena==7)
local case=os.getenv('MK2KS_STAGE_CASE')or'positive';assert(case=='positive'or case=='wrong_command'or case=='far')
local id=assert(({kano=17,sonya=18})[winner]);local victim_id=4
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local buttons,taps,css,plans,confirmed={},{},{},{},{}
local frame,match,kos,damage=0,0,0,0
local pending,window,command,action,lastmode=true,nil,nil,nil,nil
local rematch_at,action_arena,last_state=nil,nil,nil
local toast,accepted,secret,epoch,walkStart,walkX,jumpStart,punchStart,recovered=nil,nil,nil,nil,nil,nil,nil,nil,nil
local walked,jumped,punched=false,false,false
local function owned(a,identity,state)return a and a.id==identity and a.roster==identity and a.owner==a.actor and a.state==state end
local function ready(a)return a and a.y==a.floor and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 and(a.action==0 or a.action==771)end
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
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),hp=p:read_u16(s.hp),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),state=p:read_u16(s.state),
 floor=p:read_i16(m+0x200),action=p:read_u16(m+0x1f0),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20)}
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
 if frame>=28000 then log('HOST_BOUND','maximum_fields=28000');manager.machine:exit();return end
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
    plans[n]=nil
    log('SELECT_PENDING','slot='..n..' target='..target)
   end
   local age=frame-css[n]
   if age==56 then
    local target=n==side and id or victim_id
    plans[n]=route(p:read_u16(slots[n].roster),target)
    log('SELECT','slot='..n..' target='..target..' route='..table.concat(plans[n],','))
   end
   for index,key in ipairs(plans[n] or {})do local at=56+(index-1)*12;if age>=at and age<at+4 then press(n,key)end end
   if age==146 then
    local actual=p:read_u16(slots[n].roster);local target=n==side and id or victim_id
    log('SELECT_ID','slot='..n..' actual='..actual..' target='..target);assert(actual==target)
   end
   if age>=148 and age<156 then press(n,'High Punch');confirmed[n]=true end
  elseif mode~=4 then css[n]=nil;plans[n]=nil;confirmed[n]=nil end
 end
 local h,v=sample(side),sample(3-side)
 if accepted then
  if mode~=2 then
   epoch=nil;walkStart=nil;walkX=nil;jumpStart=nil;punchStart=nil;recovered=nil;walked=false;jumped=false;punched=false
  elseif owned(h,id,1)and owned(v,14,0)and h.hp>0 and v.hp>0 then
   if not secret then secret=frame;log('SECRET_FIGHT','human='..h.id..' cpu='..v.id..' arena='..arena)end
   if not epoch then epoch=frame;log('SECRET_EPOCH','human_hp='..h.hp..' cpu_hp='..v.hp)end
   if not walked then
    if ready(h)then
     walkStart=walkStart or frame;walkX=walkX or h.x
     if math.abs(h.x-walkX)>=4 then walked=true;log('SECRET_WALK','start='..walkStart..' x='..h.x..' from='..walkX)
     else press(side,h.x<v.x and'Left'or'Right')end
    else walkStart=nil;walkX=nil;press(side,'Block')end
   elseif not jumped then
    if jumpStart and h.y<h.floor and h.action~=1283 then jumped=true;log('SECRET_JUMP','start='..jumpStart..' action='..h.action..' y='..h.y..' floor='..h.floor)
    elseif ready(h)then jumpStart=jumpStart or frame;press(side,'Up')end
   elseif not punched then
    if punchStart and h.action==257 then punched=true;log('SECRET_PUNCH','start='..punchStart)
    elseif ready(h)and not punchStart then punchStart=frame;press(side,'High Punch')
    elseif punchStart and frame-punchStart<4 then press(side,'High Punch')
    elseif punchStart and frame-punchStart>30 then punchStart=nil end
   elseif not recovered then
    if ready(h)then recovered=frame;log('SECRET_RECOVER','hp='..h.hp)end
   elseif frame-recovered>=180 then
    log('SECRET_COMPLETE','epoch='..epoch..' recovered='..recovered..' human='..h.id..' cpu='..v.id..' arena='..arena);manager.machine:exit()
   else press(side,'Block')end
  end
  if h and v then log('SECRET_FIELD',string.format('mode=%d arena=%d ids=%d,%d rosters=%d,%d states=%d,%d actors=%08X,%08X owners=%08X,%08X mains=%08X,%08X hp=%d,%d actions=%d,%d',
   mode,arena,h.id,v.id,h.roster,v.roster,h.state,v.state,h.actor,v.actor,h.owner,v.owner,h.main,v.main,h.hp,v.hp,h.action,v.action))end
 end
 if not accepted and mode==2 and pending and h and v and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then
  assert(h.id==id and v.id==victim_id and h.owner==h.actor and v.owner==v.actor)
  match=match+1;pending=false;kos=0;damage=0;window=nil;command=nil;rematch_at=nil
  log('MATCH','arena='..arena..' ids='..h.id..','..v.id)
 end
 if not accepted and not action and not pending and h and v and (mode==2 or mode==7)and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then
  assert(h.id==id and v.id==victim_id and h.owner==h.actor and v.owner==v.actor)
  local finish=p:read_u16(0x01061b00)
  if frame%120==0 then log('LIVE',string.format('mode=%d arena=%d finish=%d kos=%d hp=%d,%d x=%d,%d',mode,arena,finish,kos,h.hp,v.hp,h.x,v.x))end
  local forward=h.x<v.x and'Right'or'Left';local back=forward=='Right'and'Left'or'Right'
  if mode==2 and finish==0 and h.hp>0 and v.hp>0 then
   if math.abs(h.x-v.x)>(arena==7 and 62 or 100)then press(side,forward)
   elseif arena==7 then
    press(side,'Down');if frame%48>=13 and frame%48<26 and frame%6<3 then press(side,'High Punch')end
   else if frame%32<4 then press(side,'High Kick')end end
   if arena==7 and toast and frame-toast<=48 then press(side,'Down');if(frame-toast)%8<4 then press(side,'Start')end end
  elseif finish==3 and kos==2 then
   if not window then window=frame;log('WINDOW','arena='..arena..' kos='..kos..' damage='..damage);assert(damage==322)end
   if false and arena==target_arena then
    if not command and frame-window>=65 then
     if case=='far'and math.abs(h.x-v.x)<130 then press(side,back)
     elseif case~='far'and math.abs(h.x-v.x)>65 then press(side,forward)
     else command=frame;log('COMMAND','arena='..arena..' gap='..math.abs(h.x-v.x))end
    end
    if command then
     local age=frame-command
     if winner=='kano'then
      if age>=5 and age<35 then press(side,'Block')end
      if age>=10 and age<14 or age>=20 and age<24 then press(side,'Up')
      elseif age>=30 and age<34 then press(side,case=='wrong_command'and forward or back)
      elseif age>=40 and age<44 then press(side,'Low Kick')end
     else
      if age>=10 and age<14 or age>=20 and age<24 then press(side,forward)
      elseif age>=30 and age<34 then press(side,case=='wrong_command'and back or'Down')
      elseif age>=40 and age<44 then press(side,'High Punch')end
     end
    end
   end
  end
 end
 -- A normal paid challenger after an expired finish window. Never touch state.
 if not accepted and not action and not command and window and frame-window>=720 and mode~=4 then
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

taps[#taps+1]=p:install_write_tap(0x01061cc0,0x01061ccf,'actual Toasty popup',function(at,data,mask)
 if mask==0xffff and cpu.PC.value==0xffa0baf0 and p:read_u16(0x01061ac0)==7 then
  toast=frame;log('SECRET_TOASTY',string.format('tick=%d pc=%08X',data&0xffff,cpu.PC.value))
 end
end)
taps[#taps+1]=p:install_write_tap(0x010601d0,0x010601df,'actual secret acceptance',function(at,data,mask)
 if mask==0xffff and data&0xffff==15 then
  accepted=frame;log('SECRET_ACCEPT',string.format('pc=%08X arena=%d task=%08X secretID=%d taskSide=%d in0=%08X tick=%d toastTick=%d',
   cpu.PC.value,p:read_u16(0x01061ac0),cpu.A13.value,p:read_u16(cpu.A13.value+0x120),p:read_u16(cpu.A13.value+0x100),p:read_u32(0x01600000),p:read_u16(0x0105d090),p:read_u16(0x01061cc0)))
 end
end)
for n=1,2 do
 taps[#taps+1]=p:install_write_tap(slots[n].hp,slots[n].hp+15,'secret native health',function(at,data,mask)
  if accepted and mask==0xffff then log('SECRET_HEALTH',string.format('slot=%d before=%d after=%d pc=%08X',n,p:read_u16(at),data&0xffff,cpu.PC.value))end
 end)
end

taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'native Portal uppercut',function(at)
 if at==0xff870dc0 and p:read_u16(0x01061ac0)==7 then
  local h,v=sample(side),sample(3-side)
  if h and v then log('PORTAL_UPPERCUT',string.format('a8=%08X a13=%08X own=%08X main=%08X gap=%d ids=%d,%d',cpu.A8.value,cpu.A13.value,h.actor,h.main,math.abs(h.x-v.x),h.id,v.id))end
 end
end)

for _,entry in ipairs({0xff8debf0,0xff8def20,0xff8df070,0xff8df0f0,0xff8df120,0xffa0ba10})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'native Toasty decision chain',function(at)
  if at==entry and p:read_u16(0x01061ac0)==7 then
   local h,v=sample(side),sample(3-side)
   if h and v then log('TOASTY_DECISION',string.format('entry=%08X pc=%08X a0=%08X a1=%08X actor=%08X task=%08X own=%08X victim=%08X ids=%d,%d states=%d,%d',
    entry,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,h.actor,v.actor,h.id,v.id,h.state,v.state))end
  end
 end)
end
emu.register_frame_done(function()
 if frame~=600 then return end
 do local at=0xff8de9f0;local words={0xb5a1,0x01f0,0x0b41,0xfaf5,0xca80,0xd9d0,0xffa0,0x0b41,0xfbf7,0xca80,0x2e90,0xff8c,0x0b41,0xfaf9,0xca00,0x0c9a,0x0b41,0xfaf7,0xca00,0x0be1,0x0d5f,0x9a30,0xff83,0xc906,0x09e7,0x8fc0,0xff8e,0x0d5f,0x2710,0xff84,0x09c1,0x0100,0x09e7,0xef20,0xff8d,0x0d5f,0xe280,0xff80,0x1820,0x0d5f,0x5b00,0xff9a,0x09e1,0x001c,0x001b,0x0d5f,0x4350,0xffa1,0x18c6,0x0d3f,0xf5c5,0x0d5f,0x1fd0,0xffa1,0x09eb,0x0006,0x0006,0x0d5f,0x1290,0xff9e,0x09e0,0x0000,0x0002,0x09e1,0x0000,0xfff4,0x09c2,0x6000,0x18a3,0x09c9,0x000f,0x0147,0x0b07,0x0060,0xa2ec,0xc080,0x6650,0xff87,0x0d5f,0x1ee0,0xffa1,0xc000,0x0b26,0x09c0,0x0010,0x0d5f,0xdcc0,0xff80,0x0d5f,0xd610,0xff83,0xc82d,0x05a0,0x01d0,0x0106,0x0b40,0xfffe,0xca27,0x05a0,0x1ac0,0x0106,0x0b40,0xfff8,0xcb06,0x0d5f,0xe740,0xff81,0x0b40,0xfffd,0xcb08,0x09c0,0x0028,0x0d5f,0xec20,0xff80,0xc880,0xba10,0xffa0,0x05a0,0x1ac0,0x0106,0x0b40,0xfff7,0xcb03,0x09c0,0x00b3,0xc007,0x18a0,0x0d5f,0xeae0,0xff80,0x1420,0x0b00,0x0030,0x0d5f,0x2430,0xffa1,0xc080,0xde20,0xff80};local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('TOASTY_STOCK_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches));assert(mismatches==0)
 end
 do local at=0xff81e740;local words={0x5600,0x05a1,0x01f0,0x0106,0x0d3f,0x0003,0x05a1,0x0dc0,0x0106,0x0b41,0xfffe,0xcb01,0x1020,0x0960};local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('TOASTY_STOCK_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches));assert(mismatches==0)
 end
 do local at=0xff80e980;local words={0xa22f,0x07a0,0xb950,0x0105,0x2020,0xcc03,0x0ba0,0x0002,0x0000,0x0780,0xb950,0x0105,0x5621,0x4220,0x05a1,0x01c0,0xc000,0x6820,0x4c00,0x09af,0x0002,0x0960,0xa22f,0x4c01,0x0d3f,0xffe6,0x5e20,0x1020,0x09af,0x0002,0x0960,0x098f,0x4000,0x4c01,0x2420,0x0d5f,0xeae0,0xff80,0x4420,0x09af,0x0002,0x0960,0x098f,0x6000,0x4c02,0x0d5f,0xe980,0xff80,0x09c1,0x03e8,0x5e20,0x4840,0x09af,0x0006,0x0960};local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('TOASTY_STOCK_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches));assert(mismatches==0)
 end
end)
