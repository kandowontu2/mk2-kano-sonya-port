-- Physical two-player normal-move requests; guest memory is read-only.
do
 local m=manager.machine
 local p=m.devices[':maincpu'].spaces.program
 local fields={}
 for _,port in pairs(m.ioport.ports) do for name,field in pairs(port.fields) do fields[name]=field end end
 local function set(name,value) if fields[name] then fields[name]:set_value(value) end end
 local function word(a)return p:read_u8(a)|(p:read_u8(a+8)<<8)end
 local function long(a)return word(a)|(word(a+16)<<16)end
 local function valid(a)return a>=0x01000000 and a<0x01400000 end
 local cases={
  {'hp','High Punch'}, {'lp','Low Punch'}, {'hk','High Kick'}, {'lk','Low Kick'},
  {'roundhouse','High Kick','Back'}, {'sweep','Low Kick','Back'},
  {'uppercut','High Punch','Down'}, {'jumpkick','High Kick','Up'},
  {'jumppunch','High Punch','Up'}, {'duckpunch','Low Punch','Down'},
  {'duckhighkick','High Kick','Down'}, {'ducklowkick','Low Kick','Down'},
  {'flyingkick','High Kick','ForwardJump'}, {'flyingpunch','High Punch','ForwardJump'}
 }
 local n,selection,combat,locked=0,0,0,false
 local soak=os.getenv('KS_NORMAL_SOAK')=='1'
 local previousMode=nil
 local state1=soak and assert(tonumber(os.getenv('KS_NORMAL_P1_STATE'))) or 0
 local state2=soak and assert(tonumber(os.getenv('KS_NORMAL_P2_STATE'))) or 0
 local state=soak and assert(io.open('soak_state.csv','w')) or nil
 if state then state:write('frame,mode,p1selected,p2selected,p1char,p2char,p1hp,p2hp,winner,p1wins,p2wins,round,missing,pc,locked,p1state,p2state\n') end
 local requested=os.getenv('KS_NORMAL_CASE') or ''
 local attacker=tonumber(os.getenv('KS_NORMAL_ATTACKER') or '1')
 local blocking=os.getenv('KS_NORMAL_BLOCK')=='1'
 local lowBlocking=os.getenv('KS_NORMAL_LOW_BLOCK')=='1'
 assert(not lowBlocking or blocking,'Low block requires Block')
 local gap=tonumber(os.getenv('KS_NORMAL_GAP') or '70')
 assert(gap==70 or gap==90 or gap==100 or gap==180 or gap==220,'Unsupported contact spacing')
 local placed=requested==''
 if requested~='' then
  local selected=nil
  for _,case in ipairs(cases) do if case[1]==requested then selected=case end end
  assert(selected and (attacker==1 or attacker==2),'Invalid contact profile')
  cases={selected}
 end
 local mirror=os.getenv('KS_NORMAL_MIRROR')=='1'
 local target1,target2=mirror and 18 or 17,mirror and 17 or 18
 local navigation={}
 if soak then
  for _,direction in ipairs({'Up','Down','Left','Right'}) do
   navigation[direction]=assert(tonumber(os.getenv('KS_NORMAL_NAV_'..direction:upper())))
  end
 end
 local function navigate(identity,target,prefix)
  if identity==target or identity>18 then return end
  local queue={{identity,nil}};local seen={[identity]=true};local cursor=1
  while queue[cursor] do
   local item=queue[cursor];cursor=cursor+1
   for _,direction in ipairs({'Up','Down','Left','Right'}) do
    local nextID=word(navigation[direction]+item[1]*16)
    if nextID<=18 and not seen[nextID] then
     local first=item[2] or direction
     if nextID==target then set(prefix..first,1);return end
     seen[nextID]=true;queue[#queue+1]={nextID,first}
    end
   end
  end
 end
 local log=assert(io.open('normals.csv','w'))
 local geometry=requested~='' and assert(io.open('normal_geometry.csv','w')) or nil
 if geometry then geometry:write('frame,combat,side,action,x,y,flags,left,right,top,bottom\n') end
 local function signed(a)local v=word(a);return v>=32768 and v-65536 or v end
 local function bounds(object)
  local image=long(object+0x1a0)
  local left,right,top,bottom=65535,-5000,65535,0
  for index=0,63 do
   local part=image+index*112
   assert(valid(part) and valid(part+112),'Invalid multipart bounds pointer')
   if long(part)==0 then assert(index>0);return left,right,top,bottom end
   local x=signed(object+0x90)-signed(part+80)
   local y=signed(object+0xb0)-signed(part+96)
   left=math.min(left,x);right=math.max(right,x+word(part+32))
   top=math.min(top,y);bottom=math.max(bottom,y+word(part+48))
  end
  error('Multipart bounds exceeded64 records')
 end
 log:write('frame,combat,case,age,mode,p1selected,p2selected,p1char,p2char,p1action,p2action,p1shape,p2shape,p1hp,p2hp,missing,p1x,p2x,p1hitby,p2hitby\n')
 local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
 local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
 emu.register_frame_done(function()
  n=n+1
  for name,_ in pairs(fields) do
   if name:match('^P[12] ') or name:match('^Coin ') or name:match('Player.*Start') then set(name,0) end
  end
  local mode=word(0x010601d0)
  local c1,c2=word(0x01060280),word(0x01060e50)
  if soak then
   if mode==1 or (mode==4 and previousMode~=4) then selection=0;combat=0;locked=false end
   if n>3000 and (word(state1)==0 or word(state1)==2 or word(state2)==0 or word(state2)==2) then
    locked=false
    set('Coin 1',n%120<4 and 1 or 0);set('Coin 2',n%120<4 and 1 or 0)
    if word(state1)==0 or word(state1)==2 then set('1 Player Start',n%120>=20 and n%120<24 and 1 or 0) end
    if word(state2)==0 or word(state2)==2 then set('2 Players Start',n%120>=40 and n%120<44 and 1 or 0) end
   end
  end
  if n>3000 and selection==0 then
   set('Coin 1',n%600<6 and 1 or 0);set('Coin 2',n%600<6 and 1 or 0)
   set('1 Player Start',n%600>=60 and n%600<66 and 1 or 0)
   set('P1 High Punch',n%40<4 and 1 or 0)
  end
  if mode==4 and not locked then
   selection=selection+1
   if selection<160 and not soak then set('2 Players Start',selection%30<5 and 1 or 0) end
   if selection<120 then set('Coin 1',selection%30<5 and 1 or 0) end
   if selection>50 then
    if soak then
     if selection%30<5 then navigate(c1,target1,'P1 ');navigate(c2,target2,'P2 ') end
    elseif mirror then
     if c1~=target1 then set('P1 Right',selection%30<5 and 1 or 0) end
     if c2~=target2 then set('P2 Left',selection%30<5 and 1 or 0) end
    else
     if c1==1 then set('P1 Left',selection%30<5 and 1 or 0) end
     if c2==9 then set('P2 Right',selection%30<5 and 1 or 0) end
    end
   end
   if selection>(mirror and 200 or 160) and c1==target1 and c2==target2 and
      (not soak or ((word(state1)==3 or word(state1)==4) and (word(state2)==3 or word(state2)==4))) then
    set('P1 High Punch',1);set('P2 High Punch',1);locked=true
   end
  end
  local a,b=long(0x01060220),long(0x01060df0)
  local pa,pb=long(0x01060260),long(0x01060e30)
  local index,age=0,0
  if mode==2 and locked and c1==target1 and c2==target2 and valid(a) and valid(b) and valid(pa) and valid(pb) then
   if not placed then
    local distance=math.abs(word(a+0x90)-word(b+0x90))
    if distance>gap or distance<gap-4 then
     local toward=(word(a+0x90)<word(b+0x90))==(attacker==1) and 'Right' or 'Left'
     local direction=distance>gap and toward or (toward=='Right' and 'Left' or 'Right')
     set('P'..attacker..' '..direction,1)
    else placed=true end
   end
   if requested~='' and blocking then set('P'..(3-attacker)..' Block',1) end
   if requested~='' and lowBlocking then set('P'..(3-attacker)..' Down',1) end
   if placed then
   combat=combat+1;index=math.floor((combat-1)/120)+1;age=(combat-1)%120
   if soak then index=(index-1)%#cases+1 end
   if index<=#cases then
    local case=cases[index]
    for side=1,2 do
     if requested=='' or side==attacker then
     local prefix='P'..side..' '
     local toward=(word(a+0x90)<word(b+0x90))==(side==1) and 'Right' or 'Left'
     local away=toward=='Right' and 'Left' or 'Right'
     if soak and math.abs(word(a+0x90)-word(b+0x90))>110 and case[3]~='Back' then set(prefix..toward,1) end
     local attackAge=(case[3]=='Up' or case[3]=='ForwardJump') and 16 or
      ((requested~='' and case[3]=='Down') and 24 or 12)
     local jumpAge=requested~='' and 20 or 0
     if requested~='' and (case[3]=='Up' or case[3]=='ForwardJump') then attackAge=48 end
     if case[3]=='Down' and age<attackAge+4 then set(prefix..'Down',1) end
     if case[3]=='Back' and age>=12 and age<16 then set(prefix..away,1) end
     if (case[3]=='Up' or case[3]=='ForwardJump') and age>=jumpAge and age<jumpAge+3 then
      set(prefix..'Up',1)
      if case[3]=='ForwardJump' then set(prefix..toward,1) end
     end
     if age>=attackAge and age<attackAge+3 then set(prefix..case[2],1) end
     end
    end
    if age==24 and not soak then m.screens[':screen']:snapshot('normal_'..case[1]..'.png') end
   end
   end
  end
  if mode==2 and valid(a) and valid(b) and valid(pa) and valid(pb) then
   if geometry and combat>0 and combat<=120 then
    for side,object in ipairs({a,b}) do
     local left,right,top,bottom=bounds(object)
     geometry:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',n,combat,side,
      word((side==1 and pa or pb)+0x1f0),signed(object+0x90),signed(object+0xb0),word(object+0xf0),left,right,top,bottom))
    end
    geometry:flush()
   end
   log:write(string.format('%d,%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%d,%d,%d,%d,%d,%d,%d\n',
    n,combat,cases[index] and cases[index][1] or 'idle',age,mode,c1,c2,word(a+0x1f0),word(b+0x1f0),
    word(pa+0x1f0),word(pb+0x1f0),long(a+0x1d0),long(b+0x1d0),word(0x010602f0),word(0x01060ec0),long(missing),word(a+0x90),word(b+0x90),word(pa+0x360),word(pb+0x360)))
   log:flush()
  end
  if state then
   state:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%d,%d,%d\n',n,mode,c1,c2,
    valid(a) and word(a+0x1f0) or -1,valid(b) and word(b+0x1f0) or -1,
    word(0x010602f0),word(0x01060ec0),word(0x01061b00),word(0x01060310),word(0x01060ee0),
    word(0x01061af0),long(missing),m.devices[':maincpu'].state['PC'].value,locked and 1 or 0,word(state1),word(state2)))
   if n%120==0 then state:flush() end
  end
  previousMode=mode
  if (not soak and (combat>=#cases*120+120 or n>=9000)) or (soak and n>=24000) or m.devices[':maincpu'].state['PC'].value==recovery then
   log:close();if geometry then geometry:close() end;if state then state:close() end;m:exit()
  end
 end)
end
