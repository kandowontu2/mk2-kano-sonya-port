-- Three uninterrupted, earned two-human matches and native Kano Friendships.
-- Coin/start/directions/buttons only. No guest writes, save states or resets.
local cpu=manager.machine.devices[':maincpu']
local p,state=cpu.spaces.program,cpu.state
local side=assert(tonumber(os.getenv('MK2KS_REPEAT_SIDE')));assert(side==1 or side==2)
local wanted=assert(tonumber(os.getenv('MK2KS_REPEAT_MATCHES')));assert(wanted>=2 and wanted<=5)
local output=assert(os.getenv('MK2KS_REPEAT_OUT'))
local screen=manager.machine.screens[':screen']
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local buttons={}
for n=1,2 do
 buttons[n]={}
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[n][key]=manager.machine.ioport.ports[':IN0'].fields['P'..n..' '..key]end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=manager.machine.ioport.ports[':IN2'].fields['P'..n..' '..key]end
 buttons[n].Coin=manager.machine.ioport.ports[':IN1'].fields['Coin '..n]
 buttons[n].Start=manager.machine.ioport.ports[':IN1'].fields[n==1 and'1 Player Start'or'2 Players Start']
end
local frame,cycle,completed,kos,damage=0,1,0,0,0
local css,plans,exits={},{},{}
local window,action,command_start,join_start,live=nil,nil,nil,nil,nil
local cleanup=false
local taps={};local contexts={};local current=nil
local baseline=false;local stores=0
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 print(string.format('MK2_REPEAT_%s frame=%d side=%d cycle=%d writes=0 assistance=none %s',tag,frame,side,cycle,value or''))
end
local function press(n,key)buttons[n][key]:set_value(1);log('INPUT','slot='..n..' button='..key:gsub(' ','_'))end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return{actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),human=p:read_u16(s.state),
  hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
  pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140),action=p:read_u16(m+0x1f0),trail=p:read_u32(m+0x190)}
end
local function pair(h,v)return h and v and h.id==17 and v.id==18 and h.roster==17 and v.roster==18 and h.owner==h.actor and v.owner==v.actor and h.human==1 and v.human==1 end
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
 error('Missing original native selection route')
end
local function table_state(tag)
 local words={}
 for index=0,59 do
  local cell=0x0105bb30+index*0x40
  words[#words+1]=string.format('%08X:%04X:%04X',p:read_u32(cell),p:read_u16(cell+0x20),p:read_u16(cell+0x30))
 end
 local h,v=sample(side),sample(3-side)
 log(tag,string.format('table=%s mode=%d clock=%d winner=%d kos=%d damage=%d ownActor=%08X ownMain=%08X ownID=%d ownRoster=%d ownState=%d ownHP=%d victimActor=%08X victimMain=%08X victimID=%d victimRoster=%d victimState=%d victimHP=%d',
  table.concat(words,','),p:read_u16(0x010601d0),p:read_u16(0x0105d090),p:read_u16(0x01061b00),kos,damage,
  h and h.actor or 0,h and h.main or 0,h and h.id or -1,h and h.roster or -1,h and h.human or -1,h and h.hp or -1,
  v and v.actor or 0,v and v.main or 0,v and v.id or -1,v and v.roster or -1,v and v.human or -1,v and v.hp or -1))
end
local function ensure_baseline()if not baseline then baseline=true;table_state('BASELINE')end end
local function chain(head,sprite)
 local at=p:read_u32(head);local result,seen={},{}
 while at~=0 do
  if sprite and at==0x0105b950 then return result,at,true end
  if not valid(at)or seen[at]or #result>=1024 then return result,at,false end
  result[#result+1]=string.format('%08X',at);seen[at]=true;at=p:read_u32(at)
 end
 return result,0,true
end
local function lists(tag,ctx)
 local result={}
 for _,item in ipairs({{'tasks',0x01068e30,false},{'freeTasks',0x01068e50,false},{'objects',0x0105d480,true},{'freeObjects',0x01060130,true}})do
  local nodes,stop,ok=chain(item[2],item[3]);result[#result+1]=string.format('%s=%s %sCount=%d %sStop=%08X %sValid=%d',item[1],#nodes>0 and table.concat(nodes,',')or'-',item[1],#nodes,item[1],stop,item[1],ok and 1 or 0)
 end
 log(tag,string.format('context=%d task=%08X object=%08X %s',ctx.cycle,ctx.task or 0,ctx.object or 0,table.concat(result,' ')))
end
taps[#taps+1]=p:install_write_tap(0x0105bb30,0x0105ca2f,'all native palette words throughout uninterrupted matches',function(at,data,mask)
 ensure_baseline();stores=stores+1
 log('TABLE_STORE',string.format('at=%08X before=%04X data=%04X mask=%04X pc=%08X a0=%08X a1=%08X a2=%08X a3=%08X a8=%08X a13=%08X',at,p:read_u16(at),data,mask,state.PC.value,state.A0.value,state.A1.value,state.A2.value,state.A3.value,state.A8.value,state.A13.value))
end)
taps[#taps+1]=p:install_write_tap(slots[3-side].hp,slots[3-side].hp+15,'earned repeated match health stores',function(at,data,mask)
 local h,v=sample(side),sample(3-side)
 if action or mask~=0xffff or p:read_u16(0x010601d0)~=2 or not pair(h,v)then return end
 local before,after=p:read_u16(at),data&0xffff
 if before>161 or after>=before then return end
 damage=damage+before-after;if after==0 then kos=kos+1 end
 log('DAMAGE',string.format('before=%d after=%d damage=%d kos=%d own=%08X target=%08X pc=%08X mask=%04X',before,after,damage,kos,h.actor,v.actor,state.PC.value,mask))
end)
local action_address=0xff800000+0xf9a00*8
taps[#taps+1]=p:install_read_tap(action_address,action_address+15,'actual repeated Kano Friendship action',function(at)
 if at~=action_address or state.PC.value~=at+16 or action then return end
 local h,v=sample(side),sample(3-side)
 if not pair(h,v)or state.A8.value~=h.actor or state.A13.value~=h.main then return end
 action=frame;current={cycle=cycle,action=frame,parent=h.actor,parentMain=h.main};contexts[#contexts+1]=current
 log('ACTION',string.format('entry=%08X actor=%08X main=%08X id=17 kos=%d damage=%d',at,h.actor,h.main,kos,damage));table_state('ACTION_TABLE')
end)
for _,address in ipairs({0xff83ae70,0xff83aea0,0xff83af70})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'original repeated native bubble constructor',function(at)
  local ctx=current;if not ctx or ctx.object or at~=address or state.PC.value~=at+16 or state.A13.value~=ctx.parentMain then return end
  if address~=0xff83af70 and state.A8.value~=ctx.parent then return end
  if address==0xff83ae70 then
   log('ALLOC_PRE',string.format('context=%d parent=%08X parentMain=%08X freeHead=%08X a1=%08X a7=%08X',ctx.cycle,ctx.parent,ctx.parentMain,p:read_u32(0x01068e50),state.A1.value,state.A7.value))
  elseif address==0xff83aea0 then
   ctx.task=state.A0.value;assert(valid(ctx.task),'Original native allocated group task')
   log('ALLOC_TASK',string.format('context=%d task=%08X taskID=%d resume=%08X owner=%08X pc=%08X',ctx.cycle,ctx.task,p:read_u16(ctx.task+0x20),p:read_u32(ctx.task+0xe0),p:read_u32(ctx.task+0xc0),state.PC.value))
  elseif ctx.task and state.A0.value==ctx.task then
   local a=state.A8.value;local pose=p:read_u32(a+0x1d0)
   if not valid(a)or pose<0xfe9d2610 or pose>0xfe9d2790 then return end
   ctx.object=a;ctx.palette=p:read_u16(a+0x140);ctx.constructed=frame
   log('CONSTRUCT',string.format('context=%d task=%08X object=%08X parent=%08X parentMain=%08X palette=%04X cache=%08X pose=%08X objectTask=%08X pc=%08X',ctx.cycle,ctx.task,a,ctx.parent,ctx.parentMain,ctx.palette,p:read_u32(a+0x1a0),pose,p:read_u32(a+0x20),state.PC.value));table_state('CONSTRUCT_TABLE')
  end
 end)
end
for _,item in ipairs({{'ALLOC_ENTRY',0xff80cf60},{'ALLOC_RETURN',0xff80d570},{'RELEASE_ENTRY',0xff80d580},{'RELEASE_RETURN',0xff80d790},{'POOL_RESET',0xff83f060},{'TASK_RETURN',0xff80e5d0}})do
 local tag,address=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual native repeated palette/lifecycle boundary',function(at)
  if at~=address or state.PC.value~=at+16 then return end
  log(tag,string.format('entry=%08X a0=%08X a1=%08X a2=%08X a3=%08X a8=%08X a13=%08X',at,state.A0.value,state.A1.value,state.A2.value,state.A3.value,state.A8.value,state.A13.value))
  if tag=='POOL_RESET' and current and current.object and not current.reset then
   current.reset=frame;log('BUBBLE_POOL_RESET','context='..current.cycle..' object='..string.format('%08X',current.object))
  elseif tag=='TASK_RETURN' then
   for _,ctx in ipairs(contexts)do
    if ctx.task and not ctx.taskReturn and p:read_u32(0x01068e50)==ctx.task and state.A2.value==ctx.task then
     ctx.taskReturn=frame;log('BUBBLE_TASK_RETURN','context='..ctx.cycle..' task='..string.format('%08X',ctx.task))
    end
   end
  end
 end)
end
for _,item in ipairs({{'TASK',0x01068e50},{'OBJECT',0x01060130}})do
 local kind,address=item[1],item[2]
 taps[#taps+1]=p:install_write_tap(address,address+31,'original repeated native free-head changes',function(at,data,mask)
  local shift=at-address;local before=p:read_u32(address);local merged=(before&(~(mask<<shift)))|((data&mask)<<shift)
  for _,ctx in ipairs(contexts)do
   local target=kind=='TASK'and ctx.task or ctx.object
   if target and(before==target or merged==target)then
    log('FREE_'..kind..'_STORE',string.format('context=%d at=%08X before=%08X data=%04X mask=%04X merged=%08X target=%08X next=%08X pc=%08X a0=%08X a2=%08X',ctx.cycle,at,before,data,mask,merged,target,p:read_u32(target),state.PC.value,state.A0.value,state.A2.value))
   end
  end
 end)
end
taps[#taps+1]=p:install_read_tap(0xff880cc0,0xff880ccf,'original repeated Friendship cleanup',function(at)
 if at==0xff880cc0 and state.PC.value==at+16 and action then cleanup=true;log('CLEANUP','entry=FF880CC0')end
end)
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if frame==1 then
  ensure_baseline();local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  local f=assert(io.open(output..'/guest_maincpu.bin','wb'));f:write(raw);f:close()
  log('BOOT','matches='..wanted..' own_id=17 victim_id=18')
 end
 if frame>=300 and frame<304 then press(1,'High Punch')end
 local mode=p:read_u16(0x010601d0)
 if cycle==1 then
  for n=1,2 do
   if frame>=600 and frame<604 or frame>=640 and frame<644 then press(n,'Coin')end
   if n==1 and frame>=620 and frame<624 or n==2 and frame>=660 and frame<664 then press(n,'Start')end
  end
 end
 if action and current and current.reset and frame-action>=750 then
  if completed<cycle then
   completed=cycle;log('MATCH_COMPLETE',string.format('action=%d reset=%d cleanup=%d kos=%d damage=%d',action,current.reset,cleanup and 1 or 0,kos,damage));table_state('COMPLETE_TABLE');lists('COMPLETE_LISTS',current)
  end
  if completed==wanted then log('DONE','matches='..completed);manager.machine:exit();return end
  join_start=join_start or frame
  local age=(frame-join_start)%120
  if age<4 then press(3-side,'Coin')end
  if age>=20 and age<24 then press(3-side,'Start')end
  if mode==4 then
   cycle=cycle+1;kos=0;damage=0;window=nil;action=nil;command_start=nil;join_start=nil;live=nil;cleanup=false;css={};plans={};exits={}
   log('RESELECT',string.format('mode=%d state1=%d state2=%d roster1=%d roster2=%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].roster),p:read_u16(slots[2].roster)))
  end
 end
 for n=1,2 do
  local target=n==side and 17 or 18
  if not css[n] and frame>700 and mode==4 and p:read_u16(slots[n].state)==3 and p:read_u16(slots[n].roster)<=18 then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].roster),target);log('SELECT','slot='..n..' target='..target..' route='..table.concat(plans[n],','))
  end
  if css[n] and not exits[n]then
   local age=frame-css[n]
   for index,key in ipairs(plans[n])do local at=56+(index-1)*12;if age>=at and age<at+4 then press(n,key)end end
   if age==146 then log('SELECT_ID','slot='..n..' actual='..p:read_u16(slots[n].roster)..' target='..target)end
   if age>=148 and age<156 then press(n,'High Punch')end
   if age>148 and mode~=4 then exits[n]=frame end
  end
 end
 local h,v=sample(side),sample(3-side)
 if not action and(mode==2 or mode==7)and pair(h,v)then
  local finish=p:read_u16(0x01061b00)
  if not live then live=frame;log('LIVE',string.format('mode=%d finish=%d own=%08X victim=%08X hp=%d,%d',mode,finish,h.actor,v.actor,h.hp,v.hp))end
  if mode==2 and finish==0 and h.hp>0 and v.hp>0 then
   if math.abs(h.x-v.x)>62 then press(side,h.x<v.x and'Right'or'Left')
   else press(side,'Down');if frame%22<4 then press(side,'Low Kick')end end
  elseif finish==3 and kos==2 then
   if not window then
    window=frame;log('WINDOW',string.format('kos=%d damage=%d hp_counters=%d,%d lp_counters=%d,%d',kos,damage,p:read_u16(0x01061e40),p:read_u16(0x01061e50),p:read_u16(0x01061e60),p:read_u16(0x01061e70)))
   end
   local back=h.x<v.x and'Left'or'Right'
   if not command_start then
    if math.abs(h.x-v.x)<160 then press(side,back);return end
    command_start=frame;log('COMMAND','gap='..math.abs(h.x-v.x))
   end
   local age=frame-command_start
   if age>=15 and age<25 then press(side,'Down')end
   for _,step in ipairs({{20,'Low Kick'},{30,'Block'},{40,'Block'},{50,'High Kick'}})do
    if age>=step[1]and age<step[1]+4 then press(side,step[2])end
   end
  end
 end
 if frame%240==0 then log('PROGRESS',string.format('completed=%d mode=%d kos=%d damage=%d action=%d join=%d state1=%d state2=%d roster1=%d roster2=%d',completed,mode,kos,damage,action or -1,join_start or -1,p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].roster),p:read_u16(slots[2].roster)))end
 if frame>=48000 then log('FAILED','reason=uninterrupted_repeat_did_not_finish');manager.machine:exit()end
end)
emu.register_frame_done(function()
 ensure_baseline();table_state('STATE')
 if not current then return end
 -- Instruction callbacks can occur halfway through a native list mutation.
 -- Observe the actual complete lists only at the stable native field boundary.
 local listrows={}
 for _,item in ipairs({{'tasks',0x01068e30,false},{'freeTasks',0x01068e50,false},{'objects',0x0105d480,true},{'freeObjects',0x01060130,true}})do
  local nodes,stop,ok=chain(item[2],item[3]);listrows[item[1]]={nodes=nodes,stop=stop,ok=ok}
 end
 local function member(kind,pointer)
  local target=string.format('%08X',pointer)
  for _,node in ipairs(listrows[kind].nodes)do if node==target then return 1 end end
  return 0
 end
 for _,ctx in ipairs(contexts)do
  if ctx.object then
   log('PHASE',string.format('context=%d task=%08X object=%08X taskActive=%d taskFree=%d objectActive=%d objectFree=%d tasksValid=%d freeTasksValid=%d objectsValid=%d freeObjectsValid=%d taskID=%d taskOwner=%08X taskResume=%08X objectCache=%08X objectPose=%08X objectPalette=%04X mode=%d ownActor=%08X ownMain=%08X parentTrail=%08X',
    ctx.cycle,ctx.task,ctx.object,member('tasks',ctx.task),member('freeTasks',ctx.task),member('objects',ctx.object),member('freeObjects',ctx.object),
    listrows.tasks.ok and 1 or 0,listrows.freeTasks.ok and 1 or 0,listrows.objects.ok and 1 or 0,listrows.freeObjects.ok and 1 or 0,
    p:read_u16(ctx.task+0x20),p:read_u32(ctx.task+0xc0),p:read_u32(ctx.task+0xe0),p:read_u32(ctx.object+0x1a0),p:read_u32(ctx.object+0x1d0),p:read_u16(ctx.object+0x140),
    p:read_u16(0x010601d0),p:read_u32(slots[side].actor),p:read_u32(slots[side].main),p:read_u32(ctx.parentMain+0x190)))
   if not ctx.fieldSeen or ctx.taskReturn==frame or ctx.reset==frame then
    lists('BOUNDARY_LISTS',ctx);ctx.fieldSeen=true
   end
  end
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('requested=%d completed=%d contexts=%d paletteStores=%d kos=%d damage=%d fullPortAcceptance=false',wanted,completed,#contexts,stores,kos,damage))
 for _,tap in ipairs(taps)do tap:remove()end
end)
