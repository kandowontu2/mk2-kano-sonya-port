-- Natural CPU losses, paid single-player continue and native re-selection.
-- Only ordinary physical buttons are set. All game state/taps are read-only.
local fighter=assert(os.getenv('MK2PORT_SINGLE_CONTINUE_FIGHTER'))
local target=assert(os.getenv('MK2PORT_SINGLE_CONTINUE_TARGET'))
local side=assert(tonumber(os.getenv('MK2PORT_SINGLE_CONTINUE_SIDE')))
local ids={kano=17,sonya=18};assert(ids[fighter] and ids[target] and (side==1 or side==2))
for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'}) do
 assert(not os.getenv(key),'Unassisted single-player test refuses '..key)
end
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local gfx=manager.machine.memory.regions[':gfxrom']
local high=manager.machine.ioport.ports[':IN0'].fields
local system=manager.machine.ioport.ports[':IN1'].fields
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local buttons={};for _,name in ipairs({'Left','Right','Up','Down','High Punch'}) do buttons[name]=high['P'..side..' '..name] end
buttons.Coin=system['Coin '..side];buttons.Start=system[side==1 and '1 Player Start' or '2 Players Start']
local frame,css,live,ready,ko,reset,nextReady,secondKO,continueAt,reselect,reselectExit,reLive,reReady=0
local initialPlan,rePlan,cpuID=nil,nil,nil
local phase,lastMode,lastRoster=1,nil,nil
local pixels,width,height=nil,nil,nil
local taps={}
local function log(tag,value)
 print(string.format('MK2_SC_%s frame=%d fighter=%s target=%s side=%d writes=0 assistance=none %s',tag,frame,fighter,target,side,value or ''))
end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function pulse(button,age,start,hold)
 if age>=start and age<start+(hold or 4) then buttons[button]:set_value(1);log('INPUT',string.format('button=%s age=%d',button:gsub(' ','_'),age))end
end
local adjacency={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
local function route(start,wanted)
 local queue={{start,{}}};local seen={[start]=true};local at=1
 while queue[at] do
  local current=queue[at];at=at+1
  if current[1]==wanted then return current[2]end
  for _,button in ipairs({'Left','Right','Down'})do
   local nextID=p:read_u16(adjacency[button]+current[1]*16)
   if nextID<=18 and not seen[nextID]then
    local steps={};for _,step in ipairs(current[2])do steps[#steps+1]=step end
    steps[#steps+1]=button;queue[#queue+1]={nextID,steps};seen[nextID]=true
   end
  end
 end
 error('No original native selection route from '..start..' to '..wanted)
end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return nil end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),state=p:read_u16(s.state),
  hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
  vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),flags=p:read_u16(m+0x210),
  action=p:read_u16(m+0x1f0),pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140)}
end
local function owned(a,id)return a and a.id==id and a.roster==id and a.owner==a.actor and a.state==1 end
local function grounded(a)return a and a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 end
local function snap(label)
 assert(width==400 and height==254 and #pixels==406400)
 log('RGB',string.format('label=%s bytes=%d width=%d height=%d hex=%s',label,#pixels,width,height,pixels:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
local function select_inputs(origin,plan,id)
 local age=frame-origin
 for i,button in ipairs(plan)do pulse(button,age,12+(i-1)*12)end
 pulse('High Punch',age,120,8)
 local roster=p:read_u16(slots[side].roster)
 if roster~=lastRoster then log('SELECT',string.format('origin=%d roster=%d wanted=%d',origin,roster,id));lastRoster=roster end
 if age==10 or age==98 or age==119 then snap(origin==css and 'initial_select' or 'continue_select')end
end
for n,s in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(s.hp,s.hp+15,'unassisted single-player native health ledger '..n,function(at,data,mask)
  local a=sample(n)
  log('HEALTH',string.format('slot=%d before=%d after=%d mask=%04X pc=%08X mode=%d state=%d id=%d actor=%08X main=%08X owner=%08X a8=%08X a13=%08X',
   n,p:read_u16(at),data&65535,mask,cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(s.state),a and a.id or -1,a and a.actor or 0,a and a.main or 0,a and a.owner or 0,cpu.A8.value,cpu.A13.value))
 end)
end
emu.register_frame(function()
 frame=frame+1
 for _,field in pairs(buttons)do field:clear_value()end
 if frame>=300 and frame<304 then high['P1 High Punch']:set_value(1)end -- dismiss native startup screen only
 pixels,width,height=screen:pixels()
 assert(width==400 and height==254 and #pixels==406400)
 local mode=p:read_u16(0x010601d0)
 local state=p:read_u16(slots[side].state)
 if mode~=lastMode then log('MODE',string.format('mode=%d state1=%d state2=%d roster1=%d roster2=%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].roster),p:read_u16(slots[2].roster)));lastMode=mode end
 if not css and frame>=604 then local age=(frame-604)%300;pulse('Coin',age,0);pulse('Start',age,20)end
 if not css and frame>700 and mode==4 and state==3 then css=frame;initialPlan=route(p:read_u16(slots[side].roster),ids[fighter]);log('CSS','plan='..table.concat(initialPlan,','))end
 if css and not live and mode==4 then select_inputs(css,initialPlan,ids[fighter])end
 local own,enemy=sample(side),sample(3-side)
 if not live and css and mode==2 and owned(own,ids[fighter])and enemy and enemy.state==0 then
  live=frame;cpuID=enemy.id;log('LIVE',string.format('humanID=%d cpuID=%d cpuState=%d',own.id,cpuID,enemy.state));snap('initial_match')
 end
 if live and not ready and mode==2 and owned(own,ids[fighter])and own.hp==161 and grounded(own)then ready=frame;log('READY')end
 if ready and not ko and mode==2 and owned(own,ids[fighter])and own.hp==0 then ko=frame;log('KO','cpuID='..cpuID);snap('first_cpu_ko')end
 if ko and not reset and frame>ko+60 and mode==2 and owned(own,ids[fighter])and own.hp==161 and enemy and enemy.hp==161 then reset=frame;log('ROUND_RESET')end
 if reset and not nextReady and mode==2 and owned(own,ids[fighter])and own.hp==161 and grounded(own)then nextReady=frame;phase=2;log('NEXT_READY')end
 if nextReady and not secondKO and frame>nextReady and mode==2 and owned(own,ids[fighter])and own.hp==0 then secondKO=frame;log('SECOND_KO','cpuID='..cpuID);snap('second_cpu_ko')end
 if secondKO and not continueAt and mode==3 and state==2 then continueAt=frame;log('CONTINUE','roster='..p:read_u16(slots[side].roster));snap('continue_prompt')end
 if continueAt and not reselect then
  local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Start',age,80,5)
  if mode==4 and state==3 then reselect=frame;rePlan=route(p:read_u16(slots[side].roster),ids[target]);lastRoster=nil;log('RESELECT','plan='..table.concat(rePlan,','))end
 end
 if reselect and not reselectExit then
  if mode==4 then select_inputs(reselect,rePlan,ids[target])
  else reselectExit=frame;log('RESELECT_EXIT','roster='..p:read_u16(slots[side].roster));snap('continue_ladder')end
 end
 if reselectExit and not reLive and mode==2 and owned(own,ids[target])and enemy and enemy.state==0 then
  reLive=frame;log('RE_LIVE',string.format('humanID=%d cpuID=%d cpuState=%d',own.id,enemy.id,enemy.state));snap('continued_match')
 end
 if reLive and not reReady and mode==2 and owned(own,ids[target])and own.hp>0 and grounded(own)then reReady=frame;log('RE_READY')end
 if reReady then
  local age=frame-reReady
  local away=own and enemy and own.x<enemy.x and 'Left' or 'Right'
  pulse(away,age,12,24);pulse('Up',age,64,3);pulse('High Punch',age,128,3)
  if age==38 or age==80 or age==145 or age==180 then snap('continued_control')end
  if age>=180 then manager.machine:exit()end
 end
 if frame>=14000 then log('DEADLINE','reason=route_incomplete');manager.machine:exit()end
end)
emu.register_frame_done(function()
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  log('GUEST','bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
  local bytes={};for i=0,11943 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa0000+i))end
  for i=0,7031 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa4000+i))end
  raw=table.concat(bytes);log('GFX','bytes=18976 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
 end
 for n=1,2 do
  local a=sample(n)
  if a then
   local values={string.format('slot=%d mode=%d',n,p:read_u16(0x010601d0))}
   for _,k in ipairs({'actor','main','owner','vx','vy','gravity','flags','pose','bank'})do values[#values+1]=string.format('%s=%08X',k,a[k])end
   for _,k in ipairs({'id','roster','state','hp','x','y','floor','action'})do values[#values+1]=string.format('%s=%d',k,a[k])end
   log('FIELD',table.concat(values,' '))
  end
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('css=%d live=%d ready=%d ko=%d reset=%d nextReady=%d secondKO=%d continue=%d reselect=%d reselectExit=%d reLive=%d reReady=%d cpuID=%d scope=unassisted_CPU_loss_paid_single_player_continue_not_full_port',
  css or -1,live or -1,ready or -1,ko or -1,reset or -1,nextReady or -1,secondKO or -1,continueAt or -1,reselect or -1,reselectExit or -1,reLive or -1,reReady or -1,cpuID or -1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
