-- Physical selection, two naturally won rounds, then the selected finisher.
-- All game/CPU observations are read-only. No cheats or forced finisher state.
local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local hi=m.ioport.ports[':IN0'].fields
local lo,sys
for _,port in pairs(m.ioport.ports) do
 if port.fields['P2 Low Punch'] then lo=port.fields end
 if port.fields['Coin 1'] then sys=port.fields end
end
assert(lo and sys)
local function u16(a) return p:read_u8(a)|(p:read_u8(a+8)<<8) end
local function u32(a) return u16(a)|(u16(a+16)<<16) end
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
local winner=assert(tonumber(os.getenv('KS_WINNER_STATUS')))
local death=assert(tonumber(os.getenv('KS_F_DEATH')))
local death2=assert(tonumber(os.getenv('KS_F_DEATH2')))
local ground=assert(tonumber(os.getenv('KS_GROUND_Y')))
local mirror=os.getenv('KS_EXTRACT_MIRROR')=='1'
local morphFinisher=os.getenv('KS_FINISHER_MORPH')=='1'
local morphCommandAge=nil
local morphFinishLog=morphFinisher and assert(io.open('morph_finish.csv','w')) or nil
if morphFinishLog then morphFinishLog:write('frame,selected,actual,winner,death,action\n') end
local side=mirror and 2 or 1
local kiss=os.getenv('KS_FINISH_KIND')=='kiss'
local bubble=os.getenv('KS_FINISH_KIND')=='bubble'
local laser=os.getenv('KS_FINISH_KIND')=='laser'
local baby=os.getenv('KS_FINISH_KIND')=='baby'
local friend=os.getenv('KS_FINISH_KIND')=='friend'
local stage=os.getenv('KS_FINISH_KIND')=='stage'
local deadpool=stage and os.getenv('KS_DEADPOOL')=='1'
local deadpoolNoChord=os.getenv('KS_DEADPOOL_NO_CHORD')=='1'
local deadpoolHeld=false
local deadpoolCaptureDue=0
local deadpoolLateCaptures={}
local deadpoolLog=deadpool and assert(io.open('deadpool_victim.csv','w')) or nil
if deadpoolLog then deadpoolLog:write('frame,character,action,shape,image,x,y,flags,death,ground,heldChord,masterWake,masterCountdown,thatsAll\n') end
local tongue=os.getenv('KS_FINISH_KIND')=='tongue'
local clap=os.getenv('KS_FINISH_KIND')=='clap'
local clapHeld=false
local drain=os.getenv('KS_FINISH_KIND')=='drain'
local swipe=os.getenv('KS_FINISH_KIND')=='swipe'
local impale=os.getenv('KS_FINISH_KIND')=='impale'
local arms=os.getenv('KS_FINISH_KIND')=='arms'
local kitkiss=os.getenv('KS_FINISH_KIND')=='kitana_kiss'
local bodysuck=os.getenv('KS_FINISH_KIND')=='bodysuck'
local shangburst=os.getenv('KS_FINISH_KIND')=='shangburst'
local raidenburst=os.getenv('KS_FINISH_KIND')=='raidenburst'
local laosplit=os.getenv('KS_FINISH_KIND')=='laosplit'
local raidenCapturing=false
local shangburstHeld=false
local kitkissHeld=false
local kissLateStart=nil
local kissLateLog=kitkiss and assert(io.open('kitana_kiss_late.csv','w')) or nil
if kissLateLog then kissLateLog:write('frame,mode,object,character,shape,flags,death\n') end
local bodysuckHeld=false
local inflationSeen,inflationCaptures={},{}
local inflationHidden=false
local superfreeze=os.getenv('KS_FINISH_KIND')=='superfreeze'
local shatter=os.getenv('KS_SHATTER')=='1'
local frozenAge,shatterAge=0,0
local iceLog=(superfreeze or arms or kitkiss or bodysuck or shangburst or raidenburst or laosplit) and assert(io.open(laosplit and 'laosplit_victim.csv' or (raidenburst and 'raidenburst_victim.csv' or (shangburst and 'shangburst_victim.csv' or (bodysuck and 'bodysuck_victim.csv' or (kitkiss and 'kitana_kiss_victim.csv' or (arms and 'arms_victim.csv' or 'superfreeze_victim.csv'))))),'w')) or nil
if iceLog then iceLog:write('frame,character,action,shape,palette,flags,death\n') end
local torso=os.getenv('KS_FINISH_KIND')=='torso' or swipe
local fan=os.getenv('KS_FINISH_KIND')=='fan' or tongue or clap or drain or torso or impale
local friendRejoin=friend and os.getenv('KS_FRIEND_REJOIN')=='1'
local finishRejoin=os.getenv('KS_FINISH_REJOIN')=='1'
local observeRejoin=friendRejoin or finishRejoin
local rematch=(stage and os.getenv('KS_STAGE_REMATCH')=='1') or observeRejoin
local freshFriendCombat=0
local oldEffectShapes={}
local captureFinish=os.getenv('KS_CAPTURE_FINISH')=='1'
local captureRaw,captureLog=nil,nil
local captureFields=0
local captureTail=0
local initialPal1,initialPal2=nil,nil
local initialSource1,initialSource2=nil,nil
local babyImageSeen=false
local cleanupLog=finishRejoin and assert(io.open('finisher_cleanup.csv','w')) or nil
if cleanupLog then cleanupLog:write('frame,shapeCount,objectsScanned,oldEffectObjects,p1palette,p2palette,initialP1palette,initialP2palette,p1source,p2source,initialP1source,initialP2source,p1colors,p2colors,p1rgbMismatch,p2rgbMismatch,babyImageSeen,babyObjects\n') end
local rejoinLog=observeRejoin and assert(io.open(finishRejoin and 'finisher_rejoin_events.csv' or 'friend_rejoin_events.csv','w')) or nil
if rejoinLog then rejoinLog:write('frame,phase\n') end
local pitProgress=stage and os.getenv('KS_PIT_PROGRESS')=='1'
local pitRejoin=pitProgress and os.getenv('KS_PIT_REJOIN')=='1'
local afterPitFight=0
local pitFirst,pitDone=0,0
local pitPoses={}
local pitlog=pitProgress and assert(io.open('pit_objects.csv','w')) or nil
if pitlog then
 pitlog:write('frame,object,character,shape,x,y,ground,death\n')
 local sequence=assert(tonumber(os.getenv('KS_PIT_SEQUENCE')))
 for _,index in ipairs({0,1,2,3,4,8}) do pitPoses[u32(sequence+index*32)]=true end
end
local retention=pitRejoin and assert(io.open('pit_retention.csv','w')) or nil
if retention then retention:write('frame,pitObjects,mode,background,p1char,p2char,p1hp,p2hp,death,missing\n') end
local rejoined=false
local wantRematch=false
local finishBackground=nil
local punchwins=os.getenv('KS_BABY_PUNCH_WINS')=='1'
local nonflawless=os.getenv('KS_FINISH_NONFLAWLESS')=='1'
local heldblock=os.getenv('KS_LASER_HELD_BLOCK')=='1'
local badhold=os.getenv('KS_BUBBLE_BAD_HOLD')=='1'
local objectlist=assert(tonumber(os.getenv('KS_OBJECT_LIST')))
local activelist=assert(tonumber(os.getenv('KS_ACTIVE_LIST')))
local fanObjects=(fan or arms or raidenburst or laosplit) and assert(io.open('fan_objects.csv','w')) or nil
local splitLifecycle=laosplit and assert(io.open('split_lifecycle.csv','w')) or nil
if splitLifecycle then splitLifecycle:write('frame,mode,matchingObjects,death\n') end
local splitHadObjects=false
local splitClearCaptures={}
local fanImages={}
local fanCaptured,fanPending={},{}
local swipeFinal=tonumber(os.getenv('KS_SWIPE_FINAL') or '0')
local swipeBottom=tonumber(os.getenv('KS_SWIPE_BOTTOM') or '0')
local swipeLandingDue=0
if fanObjects then
 fanObjects:write('frame,object,character,shape,image,x,y,death,missing,flags\n')
 for address in (os.getenv('KS_FAN_IMAGES') or ''):gmatch('[^,]+') do fanImages[assert(tonumber(address))]=true end
 if torso and tonumber(os.getenv('KS_EXTRACT_VICTIM'))==1 then
  fanImages={}
  local table=assert(tonumber(os.getenv('KS_TORSO_TABLE')))
  local root=u32(u32(table+32)+57*32)
  for _,index in ipairs({6,9,13,17,20,22,25}) do fanImages[u32(root+index*32)]=true end
 end
 if impale then
  fanImages={}
  local identity=assert(tonumber(os.getenv('KS_EXTRACT_VICTIM')))
  local table=assert(tonumber(os.getenv('KS_TORSO_TABLE')))
  local root=u32(u32(table+identity*32)+59*32)
  for _,index in ipairs({2,13,14,15}) do fanImages[u32(root+index*32)]=true end
 end
 if drain then
  local identity=assert(tonumber(os.getenv('KS_EXTRACT_VICTIM')))
  local root=u32(assert(tonumber(os.getenv('KS_DRAIN_TABLE')))+identity*32)
  for i=0,8 do local pose=u32(root+i*32);if pose~=0 then fanImages[pose]=true end end
  fanImages[u32(assert(tonumber(os.getenv('KS_FINAL_DRAIN'))))]=true
 end
end
local actor=((stage and os.getenv('KS_BABY_SONYA')=='1') or (friend and os.getenv('KS_FRIEND_KANO')~='1') or kiss or bubble or (baby and os.getenv('KS_BABY_SONYA')=='1')) and 18 or 17
local kind=stage and 'stage' or (friend and 'friend' or (baby and 'baby' or (laser and 'laser' or (bubble and 'bubble' or (kiss and 'kiss' or 'extract')))))
if fan then actor=4;kind='fan' end
if tongue then actor=9 end
if clap then actor=11 end
if drain then actor=6 end
if torso then actor=2 end
if swipe then actor=10 end
if impale then actor=3 end
if arms then actor=11;kind='arms' end
if kitkiss then actor=4;kind='kitana_kiss' end
if bodysuck then actor=5;kind='bodysuck' end
if shangburst then actor=6;kind='shangburst' end
if raidenburst then actor=7;kind='raidenburst' end
if laosplit then actor=0;kind='laosplit' end
if superfreeze then actor=8;kind='superfreeze' end
local navigation={}
for _,direction in ipairs({'Up','Down','Left','Right'}) do
 local values={};local i=0
 for value in (os.getenv('KS_SELECT_'..direction:upper()) or ''):gmatch('[^,]+') do values[i]=assert(tonumber(value));i=i+1 end
 navigation[direction]=values
end
local function nextDirection(start,destination)
 local queue={{start,nil}};local seen={[start]=true};local head=1
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
end
local victim=tonumber(os.getenv('KS_EXTRACT_VICTIM')) or 18
local stagelog=stage and assert(io.open('stage_environment.csv','w')) or nil
if stagelog then stagelog:write('frame,background,death\n') end
local inputlog=(friend or stage) and assert(io.open(kind..'_inputs.csv','w')) or nil
if inputlog then inputlog:write('frame,hpTimestamp,lpTimestamp,q0,q1,q2,q3\n') end
local eligibilitylog=(friend or baby) and assert(io.open('eligibility_inputs.csv','w')) or nil
if eligibilitylog then eligibilitylog:write('frame,hpTimestamp,lpTimestamp,actorX,victimX,j0,j1,j2,j3,b0,b1,b2,b3\n') end
local selectedActor=morphFinisher and 6 or actor
local target1=mirror and victim or selectedActor
local target2=mirror and selectedActor or victim
local frame,selection,combat,finish=0,0,0,0
local audioLog=assert(io.open('native_sound_writes.csv','w'))
audioLog:write('frame,address,data,mask,pc,seconds\n')
local audioTap=p:install_write_tap(0x01680000,0x0168000f,'ks_native_finisher_sound_observer',function(address,data,mask)
 audioLog:write(string.format('%d,%08x,%08x,%08x,%08x,%.9f\n',frame,address,data,mask,m.devices[':maincpu'].state['PC'].value,m.time:as_double()))
 audioLog:flush()
end)
local locked=false
local swipeHeld=false
local armed,commandField=false,0
local savedChild,savedProcess=0,0
local lifetime=(bubble or laser or (friend and actor==17)) and assert(io.open(kind..'_lifetime.csv','w')) or nil
local babylog=baby and assert(io.open('baby_objects.csv','w')) or nil
local babyimage=baby and assert(tonumber(os.getenv('KS_BABY_IMAGE'))) or 0
if babylog then babylog:write('frame,object,image,x,y,width,height,ground\n') end
if lifetime then lifetime:write('frame,child,process,childActive,processActive\n') end
local function contains(head,needle)
 local current=u32(head)
 for _=1,512 do
  if current==0 then return false end
  assert(current>=0x01000000 and current<0x01400000,'Invalid native list pointer')
  if current==needle then return true end
  current=u32(current)
 end
 error('Native list exceeded bounded traversal')
end
local log=assert(io.open(kind..'.csv','w'))
log:write('frame,pc,mode,p1char,p2char,p1hp,p2hp,p1action,p2action,p1x,p2x,p1y,p2y,p1shape,p2shape,child,childshape,winner,death,death2,missing,childx,childy,childxval,childyval,childflags,ground\n')
local function track_kiss(victimObject)
 local shape=u32(victimObject+0x1d0)
 for phase=0,5 do
  local expected=tonumber(os.getenv('KS_INFLATE_POSE_'..phase))
  if expected and shape==expected and not inflationSeen[phase] then
   inflationSeen[phase]=true
   inflationCaptures[frame+3]='phase'..phase
  end
 end
 if (u16(victimObject+0x160)&0x20)~=0 and not inflationHidden then
  inflationHidden=true
  for _,delay in ipairs({12,30,60}) do inflationCaptures[frame+delay]='burst'..delay end
 end
end
emu.register_frame_done(function()
 frame=frame+1
 for due,label in pairs(inflationCaptures) do
  if frame==due then
   m.screens[':screen']:snapshot(string.format((raidenburst and 'raiden_' or (bodysuck and 'ingest_' or 'inflate_'))..label..'_%05d.png',frame))
   inflationCaptures[due]=nil
  end
 end
 if deadpoolCaptureDue>0 and frame==deadpoolCaptureDue then
  m.screens[':screen']:snapshot(string.format('deadpool_complete_%05d.png',frame))
  deadpoolCaptureDue=-1
 end
 for due,age in pairs(deadpoolLateCaptures) do
  if frame==due then
   m.screens[':screen']:snapshot(string.format('deadpool_after%d_%05d.png',age,frame))
   deadpoolLateCaptures[due]=nil
  end
 end
 if swipeLandingDue>0 and frame==swipeLandingDue then
  m.screens[':screen']:snapshot(string.format('swipe_landed_%05d.png',frame))
 end
 for address,due in pairs(fanPending) do
  if frame>=due then
   m.screens[':screen']:snapshot(string.format('fan_pose_%08x_%05d.png',address,frame))
   fanPending[address]=nil
  end
 end
 for _,name in ipairs({'P1 High Punch','P2 High Punch','P1 High Kick','P2 High Kick','P1 Up','P2 Up','P1 Down','P2 Down','P1 Left','P1 Right','P2 Left','P2 Right','P1 Block','P2 Block'}) do hi[name]:set_value(0) end
 for _,name in ipairs({'P1 Low Punch','P2 Low Punch','P1 Low Kick','P2 Low Kick'}) do lo[name]:set_value(0) end
 for _,name in ipairs({'Coin 1','Coin 2','1 Player Start','2 Players Start'}) do sys[name]:set_value(0) end
 local mode=u16(0x010601d0)
 local c1,c2=u16(0x01060280),u16(0x01060e50)
 local canRejoin=pitFirst==0 or (pitRejoin and pitDone>0 and frame-pitDone>=240)
 if rematch and (not rejoined or pitProgress) and canRejoin and finish>0 then
  local background=u16(assert(tonumber(os.getenv('KS_CURBACK'))))
  if u16(death)==65535 or (finishBackground~=nil and background~=finishBackground) then wantRematch=true end
 end
 if wantRematch and (not rejoined or pitProgress) then
  if mode==4 then
   if rejoinLog then rejoinLog:write(string.format('%d,selection\n',frame));rejoinLog:flush() end
   rejoined=true;wantRematch=false;locked=false;selection=0;finish=0;combat=0;armed=false;commandField=0;finishBackground=nil
  else
   sys['Coin 1']:set_value(frame%120<4 and 1 or 0)
   if sys['Coin 2'] then sys['Coin 2']:set_value(frame%120<4 and 1 or 0) end
   local start2=sys['2 Players Start'] or sys['2 Player Start']
   local rejoinStart=mirror and sys['1 Player Start'] or start2
   if rejoinStart then rejoinStart:set_value(frame%120>=20 and frame%120<24 and 1 or 0) end
  end
 end
 if frame>3000 and selection==0 then
  sys['Coin 1']:set_value(frame%600<6 and 1 or 0);sys['Coin 2']:set_value(frame%600<6 and 1 or 0)
  sys['1 Player Start']:set_value(frame%600>=60 and frame%600<66 and 1 or 0)
  hi['P1 High Punch']:set_value(frame%40<4 and 1 or 0)
 end
 if mode==4 and not locked then
  selection=selection+1
  if selection<160 then sys['2 Players Start']:set_value(selection%30<5 and 1 or 0) end
  if selection<120 then sys['Coin 1']:set_value(selection%30<5 and 1 or 0) end
  if selection>50 then
   -- Dedicated edge slots are not both reachable by wrapping the same way.
   if morphFinisher or fan or superfreeze or arms or kitkiss or bodysuck or shangburst or raidenburst or laosplit then
    for _,item in ipairs({{c1,target1,'P1 '},{c2,target2,'P2 '}}) do
     if item[1]~=item[2] then
      local direction=nextDirection(item[1],item[2])
      if direction then hi[item[3]..direction]:set_value(selection%30<5 and 1 or 0) end
     end
    end
   else
    if c1~=target1 then hi[target1==18 and 'P1 Right' or 'P1 Left']:set_value(selection%30<5 and 1 or 0) end
    if c2~=target2 then hi[target2==18 and 'P2 Right' or 'P2 Left']:set_value(selection%30<5 and 1 or 0) end
   end
  end
  if selection>160 and c1==target1 and c2==target2 then
   hi['P1 High Punch']:set_value(1);hi['P2 High Punch']:set_value(1);locked=true
  end
 end
 local a,b=u32(0x01060220),u32(0x01060df0)
 local pa,pb=u32(0x01060260),u32(0x01060e30)
 local ws,fd=u16(winner),u16(death)
 if morphFinishLog then
  local object=mirror and b or a
  local process=mirror and pb or pa
  morphFinishLog:write(string.format('%d,%d,%d,%d,%d,%d\n',frame,mirror and c2 or c1,object~=0 and u16(object+0x1f0) or -1,ws,fd,process~=0 and u16(process+0x1f0) or -1))
  morphFinishLog:flush()
 end
 if kitkiss and locked and c1==target1 and c2==target2 then
  if fd==2 and not kissLateStart then kissLateStart=frame end
  local victimObject=mirror and a or b
  if kissLateStart and frame-kissLateStart<600 and victimObject>=0x01000000 and victimObject<0x01400000 then
   track_kiss(victimObject)
   kissLateLog:write(string.format('%d,%d,%08x,%d,%08x,%d,%d\n',frame,mode,victimObject,u16(victimObject+0x1f0),u32(victimObject+0x1d0),u16(victimObject+0x160),fd))
   kissLateLog:flush()
  end
 end
 if deadpool and locked and c1==target1 and c2==target2 and finish>0 and fd==65535 and deadpoolCaptureDue==0 then
  deadpoolCaptureDue=frame+2
  for _,age in ipairs({20,40,80}) do deadpoolLateCaptures[frame+age]=age end
 end
 if fanObjects and frame>3000 then
  local current=u32(objectlist)
  local matchingObjects=0
  for _=1,512 do
   if current==0 then break end
   assert(current>=0x01000000 and current<0x01400000,'Invalid native fatality object list')
   local shape,image=u32(current+0x1d0),u32(current+0x1a0)
   if fanImages[shape] or fanImages[image] then
    matchingObjects=matchingObjects+1
    if swipe and shape==swipeFinal and swipeLandingDue==0 and u16(current+0xb0)+swipeBottom==u16(ground) then swipeLandingDue=frame+2 end
    local address=fanImages[shape] and shape or image
    if not fanCaptured[address] then fanCaptured[address]=true;fanPending[address]=frame+2 end
    fanObjects:write(string.format('%d,%08x,%d,%08x,%08x,%d,%d,%d,%d,%d\n',
     frame,current,u16(current+0x1f0),shape,image,u16(current+0x90),u16(current+0xb0),fd,u32(missing),u16(current+0xf0)))
   end
   current=u32(current)
  end
  fanObjects:flush()
  if splitLifecycle then
   splitLifecycle:write(string.format('%d,%d,%d,%d\n',frame,mode,matchingObjects,fd))
   splitLifecycle:flush()
   if matchingObjects>0 then splitHadObjects=true end
   if splitHadObjects and matchingObjects==0 then
    m.screens[':screen']:snapshot(string.format('split_objects_cleared_%05d.png',frame))
    for _,age in ipairs({3,12,30,60,120,240}) do splitClearCaptures[frame+age]=age end
    splitHadObjects=false
   end
   if splitClearCaptures[frame] then
    m.screens[':screen']:snapshot(string.format('split_after_clear_%02d_%05d.png',splitClearCaptures[frame],frame))
    splitClearCaptures[frame]=nil
   end
  end
 end
 if pitProgress then
  local background=u16(assert(tonumber(os.getenv('KS_CURBACK'))))
  if pitFirst==0 and fd==6 and background==6 and c1==target1 and c2==target2 then pitFirst=frame end
  if pitFirst>0 then
   if pitDone==0 and fd==65535 then pitDone=frame end
   local current=u32(objectlist)
   local pitObjects=0
   for _=1,512 do
    if current==0 then break end
    assert(current>=0x01000000 and current<0x01400000,'Invalid native Pit object list')
    local shape=u32(current+0x1d0)
    if pitPoses[shape] then
     pitObjects=pitObjects+1
     pitlog:write(string.format('%d,%08x,%d,%08x,%d,%d,%d,%d\n',frame,current,u16(current+0x1f0),shape,
       u16(current+0x90),u16(current+0xb0),u16(ground),fd));pitlog:flush()
    end
    current=u32(current)
   end
   if retention then
    retention:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,pitObjects,mode,background,c1,c2,
      u16(0x010602f0),u16(0x01060ec0),fd,u32(missing)));retention:flush()
    if pitDone>0 and frame>pitDone+240 and mode==2 and background==7 and c1==target1 and c2==target2 then
     if afterPitFight==0 and u16(0x010602f0)>0 and u16(0x01060ec0)>0 then afterPitFight=frame end
     if afterPitFight>0 and (frame-afterPitFight==120 or frame-afterPitFight==599) then m.screens[':screen']:snapshot(string.format('after_pit_%05d.png',frame)) end
    end
   end
   if frame%12==0 and (pitDone==0 or frame-pitDone<72) then m.screens[':screen']:snapshot(string.format('pit_%05d.png',frame)) end
  end
 end
 if stagelog and (mode==2 or (captureFinish and stage and captureRaw~=nil)) then stagelog:write(string.format('%d,%d,%d\n',frame,u16(assert(tonumber(os.getenv('KS_CURBACK')))),fd));stagelog:flush() end
 if inputlog and ws==3 then
  local hp=assert(tonumber(os.getenv('KS_L_HP')))+(mirror and 16 or 0)
  local lp=assert(tonumber(os.getenv('KS_L_LP')))+(mirror and 16 or 0)
  local key=stage and (mirror and 'KS_P2_JCQ' or 'KS_P1_JCQ') or (mirror and 'KS_P2_BCQ' or 'KS_P1_BCQ')
  local head=assert(tonumber(os.getenv(key)))
  local cursor=u32(head);local values={}
  for i=1,4 do cursor=cursor-32;if cursor<=head then cursor=cursor+32*20 end;values[i]=u32(cursor) end
  inputlog:write(string.format('%d,%d,%d,%08x,%08x,%08x,%08x\n',frame,u16(hp),u16(lp),values[1],values[2],values[3],values[4]));inputlog:flush()
 end
 if mode==2 and locked and c1==target1 and c2==target2 then
  if eligibilitylog and ws==3 then
   local values={}
   for _,suffix in ipairs({'JCQ','BCQ'}) do
    local head=assert(tonumber(os.getenv('KS_P'..side..'_'..suffix)))
    local cursor=u32(head)
    assert(cursor>=head+32 and cursor<=head+32*20 and (cursor-head)%32==0,'invalid native input queue cursor')
    for i=1,4 do
     cursor=cursor-32;if cursor<=head then cursor=cursor+32*20 end
     values[#values+1]=string.format('%08x',u32(cursor))
    end
   end
   local hp=assert(tonumber(os.getenv('KS_L_HP')))+(mirror and 16 or 0)
   local lp=assert(tonumber(os.getenv('KS_L_LP')))+(mirror and 16 or 0)
   eligibilitylog:write(string.format('%d,%d,%d,%d,%d,%s\n',frame,u16(hp),u16(lp),u16((mirror and b or a)+0x90),u16((mirror and a or b)+0x90),table.concat(values,',')))
   eligibilitylog:flush()
  end
  if observeRejoin and rejoined then
   freshFriendCombat=freshFriendCombat+1
   if freshFriendCombat==1 then rejoinLog:write(string.format('%d,combat\n',frame));rejoinLog:flush() end
  end
  combat=combat+1
  local ko,vo=mirror and b or a,mirror and a or b
  local x1,x2=u16(ko+0x90),u16(vo+0x90)
  local player='P'..side
  local forward=x1<x2 and ' Right' or ' Left'
  local back=x1<x2 and ' Left' or ' Right'
  if deadpool and not deadpoolNoChord then
   local victimHealth=u16(mirror and 0x010602f0 or 0x01060ec0)
   if ws~=3 and victimHealth>12 then deadpoolHeld=false end
   if victimHealth>0 and victimHealth<=12 then deadpoolHeld=true end
   if deadpoolHeld then lo[player..' Low Punch']:set_value(1);lo[player..' Low Kick']:set_value(1) end
  end
  if swipe and ws~=3 and u16(mirror and 0x010602f0 or 0x01060ec0)>12 then swipeHeld=false end
  if swipe and (swipeHeld or u16(mirror and 0x010602f0 or 0x01060ec0)<=12) then
   swipeHeld=true
   hi[player..' High Punch']:set_value(1)
  end
  if raidenburst then hi[player..' High Punch']:set_value(1) end
  if shangburst and ws~=3 and u16(mirror and 0x010602f0 or 0x01060ec0)>40 then shangburstHeld=false end
  if shangburst and (shangburstHeld or u16(mirror and 0x010602f0 or 0x01060ec0)<=40) then
   shangburstHeld=true
   hi[player..' High Kick']:set_value(1)
  end
  if bodysuck and ws~=3 and u16(mirror and 0x010602f0 or 0x01060ec0)>40 then bodysuckHeld=false end
  if bodysuck and (bodysuckHeld or u16(mirror and 0x010602f0 or 0x01060ec0)<=40) then
   bodysuckHeld=true
   lo[player..' Low Kick']:set_value(1)
   hi[player..' High Kick']:set_value(1)
  end
  if kitkiss and ws~=3 and u16(mirror and 0x010602f0 or 0x01060ec0)>40 then kitkissHeld=false end
  if kitkiss and (kitkissHeld or u16(mirror and 0x010602f0 or 0x01060ec0)<=40) then
   kitkissHeld=true
   lo[player..' Low Kick']:set_value(1)
  end
  -- Begin charging before the KO so a fresh LP press cannot ordinarily
  -- finish a nearby victim before Jax's release-only command is ready.
  if clap and ws~=3 and u16(mirror and 0x010602f0 or 0x01060ec0)>40 then clapHeld=false end
  if clap and (clapHeld or u16(mirror and 0x010602f0 or 0x01060ec0)<=40) then
   clapHeld=true
   if ws~=3 then lo[player..' Low Punch']:set_value(1) end
  end
  if ws==3 then
   -- jx_lp_open requires a physical LP hold >=40h before release.
   if clap and not armed then lo[player..' Low Punch']:set_value(1) end
   finish=finish+1
   if stage and finishBackground==nil then finishBackground=u16(assert(tonumber(os.getenv('KS_CURBACK')))) end
   if morphFinisher and fd==0 and u16(ko+0x1f0)~=actor then
    local ownProcess=mirror and pb or pa
    if not morphCommandAge and u16(ownProcess+0x1f0)==0x303 then morphCommandAge=0 end
    if morphCommandAge then morphCommandAge=morphCommandAge+1 end
    local t=morphCommandAge and morphCommandAge%60 or 0
    if actor==17 then
     if t>=6 and t<10 or t>=22 and t<26 then hi[player..back]:set_value(1) end
     if t>=14 and t<18 then hi[player..' Down']:set_value(1) end
     if t>=30 and t<34 then lo[player..' Low Kick']:set_value(1) end
    else
     if t>=6 and t<20 then hi[player..' Down']:set_value(1);hi[player..' Block']:set_value(1) end
     if t>=10 and t<20 then lo[player..' Low Punch']:set_value(1) end
    end
   elseif fd==0 then
    if kitkiss and not armed then lo[player..' Low Kick']:set_value(1) end
    if not armed then
     if bubble or laser or baby or friend or tongue or superfreeze or arms or shangburst or laosplit then
      local range=(morphFinisher and (bubble or friend or baby)) and 160 or (laosplit and 180 or ((arms or shangburst) and 100 or (superfreeze and 150 or ((laser or tongue) and 200 or 220))))
      if math.abs(x1-x2)<range then hi[player..back]:set_value(1) end
      if finish>=80 and math.abs(x1-x2)>=range then armed=true;commandField=0 end
     else
      local range=(kitkiss or bodysuck or raidenburst) and 68 or (deadpool and 70 or (impale and 120 or (swipe and 69 or (torso and 68 or (fan and 70 or (stage and 70 or 90))))))
      if math.abs(x1-x2)>range then hi[player..forward]:set_value(1) end
      if finish>=80 and math.abs(x1-x2)<=range then armed=true;commandField=0 end
     end
    else
     commandField=commandField+1
     local t=commandField%80
     if laosplit then
      if (t>=6 and t<8) or (t>=14 and t<16) or (t>=22 and t<24) then hi[player..forward]:set_value(1) end
      if t>=30 and t<34 then lo[player..' Low Kick']:set_value(1) end
     elseif raidenburst then
      hi[player..' High Punch']:set_value(t>=1 and t<38 and 1 or 0)
     elseif shangburst then
      hi[player..' High Kick']:set_value(t>=1 and t<38 and 1 or 0)
     elseif bodysuck then
      -- fn2_hk_open checks elapsed l_lk >=080h, then HK release.
      -- Preserve the native gate through physical charge only.
      lo[player..' Low Kick']:set_value(1)
      hi[player..' High Kick']:set_value(t>=1 and t<38 and 1 or 0)
     elseif kitkiss then
      local age=commandField%80
      lo[player..' Low Kick']:set_value(age>=1 and age<38 and 1 or 0)
      if (age>=6 and age<10) or (age>=14 and age<18) or (age>=30 and age<34) then hi[player..forward]:set_value(1) end
      if age>=22 and age<26 then hi[player..' Down']:set_value(1) end
     elseif arms then
      if (t>=6 and t<10) or (t>=14 and t<18) or (t>=22 and t<26) or (t>=30 and t<34) then hi[player..' Block']:set_value(1) end
      if t>=38 and t<42 then lo[player..' Low Punch']:set_value(1) end
     elseif superfreeze then
      local victimProc=mirror and pa or pb
      if shatter and u16(victimProc+0x1f0)==0x616 then
       frozenAge=frozenAge+1
       if frozenAge>=60 then
        if math.abs(x1-x2)>68 then hi[player..forward]:set_value(1)
        else
         shatterAge=shatterAge+1
         local age=shatterAge%64
         if (age>=6 and age<10) or (age>=22 and age<26) or (age>=30 and age<34) then hi[player..forward]:set_value(1) end
         if age>=14 and age<18 then hi[player..' Down']:set_value(1) end
         if age>=38 and age<42 then hi[player..' High Punch']:set_value(1) end
        end
       end
      else
       if (t>=6 and t<10) or (t>=14 and t<18) then hi[player..forward]:set_value(1) end
       if t>=22 and t<26 then hi[player..' Down']:set_value(1) end
       if t>=30 and t<34 then hi[player..' High Kick']:set_value(1) end
      end
     elseif impale then
      if t>=6 and t<10 then hi[player..back]:set_value(1) end
      if (t>=14 and t<18) or (t>=30 and t<34) then hi[player..forward]:set_value(1) end
      if t>=22 and t<26 then hi[player..' Down']:set_value(1) end
      if t>=38 and t<42 then lo[player..' Low Punch']:set_value(1) end
     elseif swipe then
      hi[player..' High Punch']:set_value(t>=1 and t<47 and 1 or 0)
      if t>=6 and t<10 then hi[player..' Down']:set_value(1) end
      if (t>=14 and t<18) or (t>=22 and t<26) or (t>=30 and t<34) then hi[player..forward]:set_value(1) end
     elseif torso then
      if (t>=6 and t<10) or (t>=14 and t<18) then hi[player..' Down']:set_value(1) end
      if (t>=22 and t<26) or (t>=30 and t<34) then hi[player..forward]:set_value(1) end
      if t>=38 and t<42 then lo[player..' Low Punch']:set_value(1) end
     elseif drain then
      hi[player..' Block']:set_value(t>=4 and t<36 and 1 or 0)
      if (t>=6 and t<10) or (t>=22 and t<26) then hi[player..' Up']:set_value(1) end
      if t>=14 and t<18 then hi[player..' Down']:set_value(1) end
      if t>=30 and t<34 then lo[player..' Low Kick']:set_value(1) end
     elseif clap then
      lo[player..' Low Punch']:set_value(t<30 and 1 or 0)
      if (t>=6 and t<10) or (t>=14 and t<18) or (t>=22 and t<26) then hi[player..forward]:set_value(1) end
     elseif tongue then
      if (t>=6 and t<10) or (t>=14 and t<18) then hi[player..back]:set_value(1) end
      if t>=22 and t<26 then hi[player..' Down']:set_value(1) end
      if t>=30 and t<34 then lo[player..' Low Punch']:set_value(1) end
     elseif fan then
      if (t>=6 and t<10) or (t>=14 and t<18) or (t>=22 and t<26) then hi[player..' Block']:set_value(1) end
      if t>=30 and t<34 then hi[player..' High Kick']:set_value(1) end
     elseif stage then
      if deadpool then
       -- LP+LK were held before the KO; pressing LP now would kill normally.
       if t>=38 and t<72 then hi[player..' Down']:set_value(1) end
       if t>=50 and t<54 then hi[player..' High Punch']:set_value(1) end
      elseif actor==17 then
       if t>=4 and t<22 then hi[player..' Block']:set_value(1) end
       if (t>=6 and t<10) or (t>=14 and t<18) then hi[player..' Up']:set_value(1) end
       if t==22 then hi[player..back]:set_value(1) end
       if t>=38 and t<42 then lo[player..' Low Kick']:set_value(1) end
      else
       if (t>=6 and t<10) or (t>=14 and t<18) then hi[player..forward]:set_value(1) end
       if t>=22 and t<26 then hi[player..' Down']:set_value(1) end
       if t>=30 and t<34 then hi[player..' High Punch']:set_value(1) end
      end
     elseif friend then
      if actor==17 then
       if t>=6 and t<10 then lo[player..' Low Kick']:set_value(1) end
       if (t>=30 and t<34) or (t>=38 and t<42) then hi[player..' Block']:set_value(1) end
       if t>=54 and t<58 then hi[player..' High Kick']:set_value(1) end
      else
       if (t>=6 and t<10) or (t>=22 and t<26) then hi[player..back]:set_value(1) end
       if t>=14 and t<18 then hi[player..forward]:set_value(1) end
       if t>=30 and t<34 then hi[player..' Down']:set_value(1) end
       if t>=38 and t<41 then hi[player..' Block']:set_value(1) end
      end
     elseif baby then
      if morphFinisher then hi[player..' Block']:set_value(t<(actor==17 and 34 or 26) and 1 or 0) end
      if actor==17 then
       if (t>=6 and t<10) or (t>=14 and t<18) then hi[player..forward]:set_value(1) end
       if (t>=22 and t<26) or (t>=30 and t<34) then hi[player..' Down']:set_value(1) end
       if t>=38 and t<41 then lo[player..' Low Kick']:set_value(1) end
      else
       if (t>=6 and t<10) or (t>=14 and t<18) then hi[player..' Down']:set_value(1) end
       if t>=22 and t<26 then hi[player..forward]:set_value(1) end
       if t>=30 and t<34 then lo[player..' Low Kick']:set_value(1) end
      end
     elseif laser then
      if t>=6 and t<10 then lo[player..' Low Punch']:set_value(1) end
      if (t>=14 and t<18) or (t>=22 and t<26) or (heldblock and t>=26 and t<34) then hi[player..' Block']:set_value(1) end
      if t>=30 and t<34 then hi[player..' High Kick']:set_value(1) end
     elseif bubble then
      hi[player..' Block']:set_value((badhold and commandField<80 and t>=11 and t<13) and 0 or 1)
      if (t>=6 and t<10) or (t>=14 and t<18) then hi[player..' Up']:set_value(1) end
      if t>=22 and t<26 then hi[player..back]:set_value(1) end
      if t>=30 and t<41 then hi[player..' Down']:set_value(1) end
      if t>=38 and t<41 then hi[player..' High Kick']:set_value(1) end
     elseif kiss then
      if t>=6 and t<10 then hi[player..back]:set_value(1) end
      if t>=14 and t<18 then hi[player..forward]:set_value(1) end
      if (t>=22 and t<26) or (t>=30 and t<34) then hi[player..' Down']:set_value(1) end
      if t>=38 and t<41 then lo[player..' Low Punch']:set_value(1) end
     else
      if t>=6 and t<10 then hi[player..back]:set_value(1) end
      if t>=14 and t<18 then hi[player..' Down']:set_value(1) end
      if t>=22 and t<26 then hi[player..forward]:set_value(1) end
      if t>=26 and t<29 then hi[player..' High Kick']:set_value(1) end
     end
    end
   end
   if finish<440 and finish%6==0 then m.screens[':screen']:snapshot(string.format(kind..'_%05d.png',frame)) end
  elseif u16(mirror and 0x010602f0 or 0x01060ec0)>0 then
   if nonflawless and u16(mirror and 0x01060ec0 or 0x010602f0)==161 then
    -- Receive one real opponent strike each round; never edit health/flags.
    local opponent='P'..(mirror and 1 or 2)
    if math.abs(x1-x2)>75 then
     hi[player..forward]:set_value(1);hi[opponent..back]:set_value(1)
    else
     hi[opponent..' High Punch']:set_value(combat%24<3 and 1 or 0)
    end
   else
    if math.abs(x1-x2)>65 then hi[player..forward]:set_value(1) end
    hi[player..((((baby or friend) and not punchwins) or raidenburst) and ' High Kick' or ' High Punch')]:set_value((swipe and swipeHeld) and 1 or (combat%32<2 and 1 or 0))
   end
  end
 end
 if iceLog and mode==2 and locked and c1==target1 and c2==target2 then
  local victimObject=mirror and a or b
  local victimProc=mirror and pa or pb
  if raidenburst and fd==2 and not raidenCapturing then
   raidenCapturing=true
   for _,delay in ipairs({60,120,180,240,320,400}) do inflationCaptures[frame+delay]='age'..delay end
  end
  if bodysuck and fd==2 then
   local shape=u32(victimObject+0x1d0)
   for phase=0,7 do
    local expected=tonumber(os.getenv('KS_INGEST_POSE_'..phase))
    if expected and shape==expected and not inflationSeen[phase] then
     inflationSeen[phase]=true
     inflationCaptures[frame+3]='phase'..phase
    end
   end
   if (u16(victimObject+0x160)&0x20)~=0 and not inflationHidden then
    inflationHidden=true
    inflationCaptures[frame+12]='invisible12'
    inflationCaptures[frame+30]='invisible30'
   end
  end
  if kitkiss and fd==2 then track_kiss(victimObject) end
  iceLog:write(string.format('%d,%d,%d,%08x,%d,%d,%d\n',frame,u16(victimObject+0x1f0),
   u16(victimProc+0x1f0),u32(victimObject+0x1d0),u16(victimObject+0x140),u16(victimObject+0x160),fd))
  iceLog:flush()
 end
 if finishRejoin and rejoined and mode==2 and locked then
  -- Bounded fresh-match probe, not another rapid-KO finisher setup.
  local player='P'..side
  for _,button in ipairs({'High Punch','High Kick','Up','Down','Left','Right','Block'}) do hi[player..' '..button]:set_value(0) end
  for _,button in ipairs({'Low Punch','Low Kick'}) do lo[player..' '..button]:set_value(0) end
  local ko,vo=mirror and b or a,mirror and a or b
  local x1,x2=u16(ko+0x90),u16(vo+0x90)
  if math.abs(x1-x2)>75 then hi[player..(x1<x2 and ' Right' or ' Left')]:set_value(1)
  elseif swipe and freshFriendCombat%180>=48 and freshFriendCombat%180<63 then
   -- Scorpion needs native duck-entry time before the fresh-match HP pulse.
   hi[player..' Down']:set_value(1)
   if freshFriendCombat%180>=60 then hi[player..' High Punch']:set_value(1) end
  elseif freshFriendCombat%180>=60 and freshFriendCombat%180<63 then
   hi[player..' Down']:set_value(1);hi[player..' High Punch']:set_value(1)
  end
 end
 if mode==2 or (captureFinish and stage and (mode==9 or (pitProgress and mode==5))) or frame%10==0 then
  local captureActive=fd~=0 and fd~=65535
  if pitProgress and captureRaw and fd==65535 then
   captureTail=captureTail+1;captureActive=captureTail<=60
  end
  if deadpool then
   local background=u16(assert(tonumber(os.getenv('KS_CURBACK'))))
   local victimProcess=mirror and pa or pb
   local actorProcess=mirror and pb or pa
   local uppercut=ws==3 and finish>0 and u16(actorProcess+0x1f0)==0x107
   captureActive=background==0 and fd~=65535 and (captureRaw~=nil or uppercut or u16(victimProcess+0x1f0)==0x50a)
  end
  local captureBackground=tonumber(os.getenv('KS_CAPTURE_BACKGROUND') or '-1')
  if stage and captureBackground>=0 then
   captureActive=captureActive and u16(assert(tonumber(os.getenv('KS_CURBACK'))))==captureBackground
  end
  local captureMode=mode==2 or (stage and captureRaw~=nil and (mode==9 or (pitProgress and mode==5)))
  if captureFinish and captureMode and c1==target1 and c2==target2 and captureActive then
   if not captureRaw then
    captureRaw=assert(io.open('finisher_capture.bgra','wb'))
    captureLog=assert(io.open('finisher_capture.csv','w'))
    captureLog:write('frame,seconds,width,height,bytes\n')
   end
   captureFields=captureFields+1;assert(captureFields<=400,'Bounded finisher capture exceeded')
   local screen=m.screens[':screen'];local raw=screen:pixels()
   assert(screen.width==400 and screen.height==254 and #raw==400*254*4)
   assert(captureRaw:write(raw))
   captureLog:write(string.format('%d,%.12f,%d,%d,%d\n',frame,m.time:as_double(),screen.width,screen.height,#raw));captureLog:flush()
  elseif captureRaw then
   captureRaw:close();captureLog:close();captureRaw=nil;captureLog=nil;captureFinish=false
  end
  local child=u32((mirror and pb or pa)+0x190)
  local childshape=(child>=0x01000000 and child<0x01400000) and u32(child+0x1d0) or 0
  local valid=child>=0x01000000 and child<0x01400000
  if finishRejoin and not rejoined and mode==2 and locked and c1==target1 and c2==target2 and initialPal1==nil then
   initialPal1=u16(a+0x140);initialPal2=u16(b+0x140)
   local base=assert(tonumber(os.getenv('KS_PALRAM')))
   initialSource1=u32(base+(initialPal1&255)*64);initialSource2=u32(base+(initialPal2&255)*64)
  end
  if finishRejoin and not rejoined and mode==2 and fd~=0 and fd~=65535 and valid then
   if childshape~=0 then oldEffectShapes[childshape]=true end
  end
  if finishRejoin and rejoined and mode==2 and locked and c1==target1 and c2==target2 then
   local shapeCount=0
   for _ in pairs(oldEffectShapes) do shapeCount=shapeCount+1 end
   local current=u32(objectlist);local seen={};local count,remaining,babyObjects=0,0,0
   while current~=0 do
    assert(current>=0x01000000 and current<0x01400000,'Invalid cleanup object pointer')
    assert(not seen[current] and count<512,'Cyclic or oversized cleanup object list')
    seen[current]=true;count=count+1
    if oldEffectShapes[u32(current+0x1d0)] then remaining=remaining+1 end
    if baby and u32(current+0x1a0)==babyimage then babyObjects=babyObjects+1 end
    current=u32(current)
   end
   local base=assert(tonumber(os.getenv('KS_PALRAM')))
   local source1=u32(base+(u16(a+0x140)&255)*64)
   local source2=u32(base+(u16(b+0x140)&255)*64)
   local function rgbMismatch(object,source)
    assert(source>=0xff800000 and source<=0xffffffff,'Invalid ROM palette source')
    local colors=u16(source);assert(colors>=1 and colors<=256,'Invalid palette color count')
    local destination=0x01880000+(u16(object+0x140)&255)*256*16
    local mismatches=0
    for color=0,colors-1 do
     if (u16(destination+color*16)&0x7fff)~=(u16(source+16+color*16)&0x7fff) then mismatches=mismatches+1 end
    end
    return colors,mismatches
   end
   local colors1,mismatch1=rgbMismatch(a,source1)
   local colors2,mismatch2=rgbMismatch(b,source2)
   cleanupLog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%08x,%08x,%d,%d,%d,%d,%d,%d\n',frame,shapeCount,count,remaining,u16(a+0x140),u16(b+0x140),assert(initialPal1),assert(initialPal2),source1,source2,assert(initialSource1),assert(initialSource2),colors1,colors2,mismatch1,mismatch2,babyImageSeen and 1 or 0,babyObjects));cleanupLog:flush()
  end
  if babylog and mode==2 and c1==target1 and c2==target2 then
   local current=u32(objectlist)
   for _=1,512 do
    if current==0 then break end
    assert(current>=0x01000000 and current<0x01400000,'Invalid baby object list pointer')
    if u32(current+0x1a0)==babyimage then
     if not rejoined then babyImageSeen=true end
     babylog:write(string.format('%d,%08x,%08x,%d,%d,%d,%d,%d\n',frame,current,babyimage,
      u16(current+0x90),u16(current+0xb0),u16(current+0x120),u16(current+0x130),u16(ground)))
     babylog:flush()
    end
    current=u32(current)
   end
  end
  if lifetime and mode==2 and c1==target1 and c2==target2 then
   if valid and savedChild==0 then savedChild=child;savedProcess=u32(child+0x20) end
   if savedChild~=0 then
    lifetime:write(string.format('%d,%08x,%08x,%d,%d\n',frame,savedChild,savedProcess,
      contains(objectlist,savedChild) and 1 or 0,contains(activelist,savedProcess) and 1 or 0));lifetime:flush()
   end
  end
  log:write(string.format('%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%08x,%08x,%d,%d,%d,%d,%d,%d,%08x,%08x,%d,%d\n',
   frame,m.devices[':maincpu'].state['PC'].value,mode,c1,c2,u16(0x010602f0),u16(0x01060ec0),u16(pa+0x1f0),u16(pb+0x1f0),
   u16(a+0x90),u16(b+0x90),u16(a+0xb0),u16(b+0xb0),u32(a+0x1d0),u32(b+0x1d0),child,childshape,ws,fd,u16(death2),u32(missing),
   valid and u16(child+0x90) or 0,valid and u16(child+0xb0) or 0,
   valid and u32(child+0x80) or 0,valid and u32(child+0xa0) or 0,valid and u16(child+0xf0) or 0,u16(ground)))
  log:flush()
 end
 if deadpoolLog and mode==2 and finish>0 and locked and c1==target1 and c2==target2 then
  local victimObject=mirror and a or b
  local victimProc=mirror and pa or pb
  if victimObject>=0x01000000 and victimObject<0x01400000 and victimProc>=0x01000000 and victimProc<0x01400000 then
   local masterWake,masterCountdown=0,0
   local current=u32(activelist)
   for _=1,512 do
    if current==0 then break end
    assert(current>=0x01000000 and current<0x01400000,'Invalid native master process list')
    if u16(current+0x20)==3 then masterWake=u32(current+0xe0);masterCountdown=u32(current+0x60);break end
    current=u32(current)
   end
   deadpoolLog:write(string.format('%d,%d,%d,%08x,%08x,%d,%d,%d,%d,%d,%d,%08x,%d,%d\n',frame,
    u16(victimObject+0x1f0),u16(victimProc+0x1f0),u32(victimObject+0x1d0),u32(victimObject+0x1a0),
    u16(victimObject+0x90),u16(victimObject+0xb0),u16(victimObject+0x160),u16(death),u16(ground),
    ((~u32(0x0187ff80))>>(mirror and 20 or 16))&3,masterWake,masterCountdown,
    u16(assert(tonumber(os.getenv('KS_F_THATSALL'))))))
   deadpoolLog:flush()
  end
 end
 if m.devices[':maincpu'].state['PC'].value==recovery then
  local fault=assert(io.open(kind..'_fault.txt','w'))
  for _,name in ipairs({'PC','SP','ST','A0','A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14'}) do
   local reg=m.devices[':maincpu'].state[name]
   if reg then fault:write(string.format('%s=%08x\n',name,reg.value)) end
  end
  local stack=m.devices[':maincpu'].state['SP']
  if stack and stack.value>=0x01000000 and stack.value<0x01400000 then
   for offset=-128,512,32 do fault:write(string.format('stack[%08x]=%08x\n',stack.value+offset,u32(stack.value+offset))) end
  end
  fault:close()
 end
 if m.devices[':maincpu'].state['PC'].value==recovery or frame>=(pitProgress and 45000 or (rematch and 18000 or 9000)) or (pitDone>0 and not pitRejoin and frame-pitDone>=240) or (afterPitFight>0 and frame-afterPitFight>=600) or freshFriendCombat>=600 then log:close();if rejoinLog then rejoinLog:close() end;if lifetime then lifetime:close() end;audioLog:close();audioTap:remove();m:exit() end
end)
