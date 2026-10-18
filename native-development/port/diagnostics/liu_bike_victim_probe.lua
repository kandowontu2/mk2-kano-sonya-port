-- Real controller inputs only. Guest memory is observed, never modified.
local m=manager.machine
local cpu=m.devices[':maincpu']
local p=cpu.spaces.program
local fields={}
local mirror=os.getenv('KS_BIKE_MIRROR')=='1'
local orb=os.getenv('KS_ORB_VICTIM')=='1'
local throw=tonumber(os.getenv('KS_OWN_THROW') or '0')
local edge=os.getenv('KS_THROW_EDGE')=='1'
local backbreak=os.getenv('KS_BACKBREAK')=='1'
local shred=os.getenv('KS_SHRED')=='1'
local nut=os.getenv('KS_NUT')=='1'
local freeze=os.getenv('KS_FREEZE')=='1'
local lightning=os.getenv('KS_LIGHTNING')=='1'
local spear=os.getenv('KS_SPEAR')=='1'
local shock=os.getenv('KS_SHOCK')=='1'
local dive=os.getenv('KS_DIVE')=='1'
local blockkick=os.getenv('KS_BLOCKKICK')=='1'
local attacker=spear and 10 or ((lightning or shock or dive) and 7 or (freeze and 8 or (nut and 2 or (shred and 3 or (backbreak and 11 or (throw>0 and throw or (orb and 9 or 1)))))))
for _,port in pairs(m.ioport.ports) do
 for name,field in pairs(port.fields) do
  if mirror then
   if name:sub(1,2)=='P1' then name='P2'..name:sub(3)
   elseif name:sub(1,2)=='P2' then name='P1'..name:sub(3) end
  end
  fields[name]=field
 end
end
local function set(name,v) if fields[name] then fields[name]:set_value(v) end end
local function u16(a) return p:read_u8(a)|(p:read_u8(a+8)<<8) end
local function u32(a)
 local v=0
 for i=0,3 do v=v|(p:read_u8(a+i*8)<<(i*8)) end
 return v
end
local target=throw>0 and (throw==17 and 18 or 17) or assert(tonumber(os.getenv('KS_BIKE_VICTIM')))
if throw>0 and (os.getenv('KS_THROW_OVERRIDE')=='1' or tonumber(os.getenv('KS_THROW_VICTIM') or '0')>0) then target=tonumber(os.getenv('KS_THROW_VICTIM')) end
local navigation={}
for _,direction in ipairs({'Up','Down','Left','Right'}) do
 local values={}
 local i=0
 for value in (os.getenv('KS_SELECT_'..direction:upper()) or ''):gmatch('[^,]+') do values[i]=assert(tonumber(value));i=i+1 end
 navigation[direction]=values
end
local function nextDirection(start,destination)
 local queue={{start,nil}}
 local seen={[start]=true}
 local head=1
 while head<=#queue do
  local item=queue[head];head=head+1
  if item[1]==destination then return item[2] end
  for _,direction in ipairs({'Up','Down','Left','Right'}) do
   local neighbor=navigation[direction][item[1]]
   if neighbor and not seen[neighbor] then
    seen[neighbor]=true;queue[#queue+1]={neighbor,item[2] or direction}
   end
  end
 end
 return nil
end
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local log=assert(io.open(nut and 'nut.csv' or (shred and 'shred.csv' or (backbreak and 'backbreak.csv' or (throw>0 and 'throw.csv' or 'liu_bike.csv'))),'w'))
log:write('frame,fight,mode,p1selected,p2selected,p1char,p2char,action,savedA11,victimShape,p1x,p2x,victimHP,missing,pc,victimAction,ownerShape,ownerY,victimY,ownerGround,victimGround,edgeReady\n')
local n,selection,fight=0,0,0
local freezeLog=(freeze or lightning or spear or shock) and assert(io.open('freeze_palette.csv','w')) or nil
if freezeLog then freezeLog:write('frame,fight,character,action,paletteSelector,shape,missing\n') end
local locked=false
local didThrow=false
local throwAge=0
local throwCaptures={}
local backbreakPoses={}
if backbreak then
 local phase=0
 for value in (os.getenv('KS_BACKBREAK_POSES') or ''):gmatch('[^,]+') do
  if tonumber(value)~=0 then backbreakPoses[tonumber(value)]=phase end
  phase=phase+1
 end
end
local backbreakCaptures={}
local backbreakPending={}
local previousVictimX=-1
local edgeStall=0
local edgeReady=false
local backbreakJumpAt=150
if edge then backbreakJumpAt=nil end
emu.register_frame_done(function()
 n=n+1
 for _,name in ipairs({'Coin 1','Coin 2','1 Player Start','2 Players Start','2 Player Start',
 'P1 High Punch','P1 Low Punch','P1 Low Kick','P1 Block','P1 Left','P1 Right','P1 Up','P1 Down',
 'P2 High Punch','P2 Block','P2 Left','P2 Right','P2 Up','P2 Down'}) do set(name,0) end
 local mode=u16(0x010601d0)
 local c1,c2=u16(0x01060280),u16(0x01060e50)
 if mirror then c1,c2=c2,c1 end
 if n>3000 and selection==0 then
  set('Coin 1',n%600<6 and 1 or 0);set('Coin 2',n%600<6 and 1 or 0)
  set('1 Player Start',n%600>=60 and n%600<66 and 1 or 0)
  set('P1 High Punch',n%40<4 and 1 or 0)
 end
 if mode==4 and not locked then
  selection=selection+1
  if selection<160 then
   set('2 Players Start',selection%30<5 and 1 or 0)
   set('2 Player Start',selection%30<5 and 1 or 0)
  end
  if selection<120 then set('Coin 1',selection%30<5 and 1 or 0) end
  if selection>50 and selection%30<5 and c2~=target then
   local direction=nextDirection(c2,target)
   if direction then set('P2 '..direction,1) end
  end
  if selection>50 and selection%30<5 and c1~=attacker then
   local direction=nextDirection(c1,attacker)
   if direction then set('P1 '..direction,1) end
  end
  if selection>160 and c1==attacker and c2==target then
   set('P1 High Punch',1);set('P2 High Punch',1);locked=true
  end
 end
 local a,b=u32(0x01060220),u32(0x01060df0)
 if mirror then a,b=b,a end
 local proc=u32(mirror and 0x01060e30 or 0x01060260)
 local x1,x2=a~=0 and u16(a+0x90) or 0,b~=0 and u16(b+0x90) or 0
 if mode==2 and locked then
  fight=fight+1
  if blockkick then
   if fight>=60 and fight<250 then set('P2 Block',1) end
   if (fight>=100 and fight<103) or (fight>=108 and fight<111) then set(x1<x2 and 'P1 Right' or 'P1 Left',1) end
   if fight>=116 and fight<119 then set('P1 High Kick',1) end
   if fight>=130 and fight<=300 and fight%10==0 then m.screens[':screen']:snapshot(string.format('blockkick_%d.png',fight)) end
  elseif dive then
   if (fight>=100 and fight<103) or (fight>=108 and fight<111) then set(x1<x2 and 'P1 Left' or 'P1 Right',1) end
   if fight>=116 and fight<119 then set(x1<x2 and 'P1 Right' or 'P1 Left',1) end
   if fight>=130 and fight<=350 and fight%10==0 then m.screens[':screen']:snapshot(string.format('dive_%d.png',fight)) end
  elseif shock then
   if fight>=60 and fight<150 and math.abs(x2-x1)>60 then set(x1<x2 and 'P1 Right' or 'P1 Left',1) end
   if fight>=60 and fight<165 then set('P1 High Punch',1) end
   if fight>=170 and fight<=330 and fight%10==0 then m.screens[':screen']:snapshot(string.format('shock_%d.png',fight)) end
  elseif spear then
   if (fight>=100 and fight<104) or (fight>=108 and fight<112) then set(x1<x2 and 'P1 Left' or 'P1 Right',1) end
   if fight>=116 and fight<120 then set('P1 Low Punch',1) end
   if fight>=140 and fight<=300 and fight%10==0 then m.screens[':screen']:snapshot(string.format('spear_%d.png',fight)) end
  elseif freeze or lightning then
   if fight>=100 and fight<104 then set('P1 Down',1) end
   if fight>=105 and fight<108 then set(x1<x2 and 'P1 Right' or 'P1 Left',1) end
   if fight>=110 and fight<113 then set('P1 Low Punch',1) end
   if fight>=140 and fight<=400 and fight%40==0 then m.screens[':screen']:snapshot(string.format('freeze_%d.png',fight)) end
  elseif nut then
   if fight>=60 and fight<150 and math.abs(x2-x1)>65 then set(x1<x2 and 'P1 Right' or 'P1 Left',1) end
   if fight>=160 and fight<164 then set('P1 Low Punch',1);set('P1 Block',1) end
   if fight==180 or fight==220 then m.screens[':screen']:snapshot(string.format('nut_%d.png',fight)) end
  elseif shred then
   if fight>=60 and fight<150 and math.abs(x2-x1)>65 then set(x1<x2 and 'P1 Right' or 'P1 Left',1) end
   local age=fight-160
   if (age>=0 and age<2) or (age>=6 and age<8) or (age>=12 and age<14) then set(x1<x2 and 'P1 Left' or 'P1 Right',1) end
   if age>=18 and age<20 then set('P1 Low Punch',1) end
   if fight>=180 and fight<=270 and fight%10==0 then m.screens[':screen']:snapshot(string.format('shred_%d.png',fight)) end
  elseif backbreak then
   if edge and not edgeReady and fight>60 then
    edgeStall=x2==previousVictimX and edgeStall+1 or 0
    previousVictimX=x2
    if edgeStall>=30 and fight>160 then
     edgeReady=true;backbreakJumpAt=fight+20
     local setup=assert(io.open('backbreak_edge_setup.json','w'))
     setup:write(string.format('{"fight":%d,"ownerX":%d,"victimX":%d,"stationaryFieldsWhileAwayHeld":%d,"guestWrites":false}\n',fight,x1,x2,edgeStall));setup:close()
    else set(x1<x2 and 'P2 Right' or 'P2 Left',1) end
    set(x1<x2 and 'P1 Right' or 'P1 Left',1)
   end
   if backbreakJumpAt then
    if fight>=60 and fight<backbreakJumpAt-10 and math.abs(x2-x1)>65 then set(x1<x2 and 'P1 Right' or 'P1 Left',1) end
    local age=fight-backbreakJumpAt
    if age>=0 and age<4 then set('P1 Up',1);set('P2 Up',1) end
    if age>=22 and age<38 and (age-22)%4<2 then set('P1 Block',1) end
   end
  elseif throw>0 then
   if proc~=0 and u16(proc+0x1f0)==0x507 then didThrow=true;throwAge=throwAge+1 end
   if not didThrow and fight>60 then
    if edge and not edgeReady then
     edgeStall=x2==previousVictimX and edgeStall+1 or 0
     previousVictimX=x2
     if edgeStall>=30 and fight>160 then
      edgeReady=true
      local setup=assert(io.open('throw_edge_setup.json','w'))
      setup:write(string.format('{"fight":%d,"ownerX":%d,"victimX":%d,"stationaryFieldsWhileAwayHeld":%d,"guestWrites":false}\n',fight,x1,x2,edgeStall));setup:close()
     else set(x1<x2 and 'P2 Right' or 'P2 Left',1) end
    end
    set(x1<x2 and 'P1 Right' or 'P1 Left',1)
    if (not edge or edgeReady) and fight%40>=20 and fight%40<24 then set('P1 Low Punch',1) end
   end
   if not throwCaptures[throwAge] and (throwAge==4 or throwAge==12 or throwAge==20 or throwAge==28 or throwAge==36 or throwAge==48) then
    throwCaptures[throwAge]=true
    m.screens[':screen']:snapshot(string.format('throw_age%d.png',throwAge))
   end
  elseif orb then
   if fight>=100 and fight<104 or fight>=110 and fight<114 then set(mirror and 'P1 Right' or 'P1 Left',1) end
   if fight>=120 and fight<124 then set('P1 High Punch',1) end
   if fight>=122 and fight<126 then set('P1 Low Punch',1) end
  else
   if fight>=60 and fight<230 then set('P1 Low Kick',1) end
   if fight>=120 and fight<220 and math.abs(x2-x1)>100 then set(mirror and 'P1 Left' or 'P1 Right',1) end
  end
  if fight==260 or fight==290 or fight==330 then m.screens[':screen']:snapshot(string.format('liu_bike_%d.png',fight)) end
  if backbreak and b~=0 then
   local shape=u32(b+0x1d0)
   -- Capture after display-list/framebuffer latency, even if the live
   -- animation descriptor has advanced to its next two-field pose already.
   if backbreakPoses[shape]~=nil and not backbreakCaptures[shape] and not backbreakPending[shape] then
    backbreakPending[shape]={due=n+2,phase=backbreakPoses[shape]}
   end
   for pendingShape,request in pairs(backbreakPending) do
    if n>=request.due then
     backbreakCaptures[pendingShape]=true
     m.screens[':screen']:snapshot(string.format('backbreak_pose%d.png',request.phase))
     backbreakPending[pendingShape]=nil
    end
   end
  end
 end
 local victimProc=u32(mirror and 0x01060260 or 0x01060e30)
 if freezeLog and mode==2 and b~=0 then
  freezeLog:write(string.format('%d,%d,%d,%d,%d,%08x,%d\n',n,fight,u16(b+0x1f0),u16(victimProc+0x1f0),u16(b+0x140),u32(b+0x1d0),u32(missing)))
 end
 log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%d,%d,%d,%d,%08x,%d,%08x,%d,%d,%d,%d,%d\n',
 n,fight,mode,c1,c2,a~=0 and u16(a+0x1f0) or -1,b~=0 and u16(b+0x1f0) or -1,
 proc~=0 and u16(proc+0x1f0) or 0,proc~=0 and u32(proc+0x60) or 0,
 b~=0 and u32(b+0x1d0) or 0,x1,x2,u16(mirror and 0x010602f0 or 0x01060ec0),u32(missing),cpu.state['PC'].value,
 victimProc~=0 and u16(victimProc+0x1f0) or 0,a~=0 and u32(a+0x1d0) or 0,
 a~=0 and u16(a+0xb0) or 0,b~=0 and u16(b+0xb0) or 0,proc~=0 and u16(proc+0x200) or 0,victimProc~=0 and u16(victimProc+0x200) or 0,edgeReady and 1 or 0))
 if n%120==0 then log:flush() end
 if backbreak and u32(missing)>0 then
  local issue=assert(io.open('backbreak_missing.json','w'))
  issue:write(string.format('{"frame":%d,"fight":%d,"missingCount":%d,"tag":%d,"actor":%d,"attackerAction":%d,"gameplayVerified":false}\n',
   n,fight,u32(missing),u16(assert(tonumber(os.getenv('KS_MISSING_TAG')))),u16(assert(tonumber(os.getenv('KS_MISSING_ACTOR')))),proc~=0 and u16(proc+0x1f0) or 0))
  issue:close();log:close();m:exit()
 elseif cpu.state['PC'].value==recovery or n>=9000 then log:close();if freezeLog then freezeLog:close() end;m:exit() end
end)
