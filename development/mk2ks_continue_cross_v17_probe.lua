-- Real two-round loss, paid continue, native cross-character reselect and new-match control.
-- Diagnostic only; no RAM/health/position/identity/RNG writes.
local fighter = assert(os.getenv('MK2KS_GROUND_FIGHTER'))
local side = assert(tonumber(os.getenv('MK2KS_GROUND_SIDE')))
local boot = tonumber(os.getenv('MK2KS_GROUND_BOOT') or '604')
local ids = {kano=17, sonya=18, sub_zero=8, kitana=4}
assert(ids[fighter] and fighter~='kitana' and (side==1 or side==2))
local names = side==1 and {fighter,'kitana'} or {'kitana',fighter}
local routes = {
 {kano={'Left'},sonya={'Right','Right','Right','Right'},sub_zero={'Down'},kitana={'Right','Right','Down'}},
 {kano={'Left','Left','Left','Left'},sonya={'Right'},sub_zero={'Left','Left','Left','Down'},kitana={'Left','Down'}}}
local slots = {{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local p = manager.machine.devices[':maincpu'].spaces.program
local cpu = manager.machine.devices[':maincpu'].state
local screen = manager.machine.screens[':screen']
local gfx = manager.machine.memory.regions[':gfxrom']
local palette = manager.machine.palettes[':palette']
local high,system = manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local fields = {{},{}}
for n=1,2 do
 for _,button in ipairs({'High Punch','Left','Right','Up','Down'}) do fields[n][button]=high['P'..n..' '..button] end
 fields[n].Coin=system['Coin '..n]
 fields[n].Start=system[n==1 and '1 Player Start' or '2 Players Start']
end
local frame,css,live,ready = 0,nil,nil,nil
local regs,taps,emitted = {},{},{}
local ko,next_round,next_ready = nil,nil,nil
local phase,phase_ready,second_ko,last_mode=1,nil,nil,nil
local target=fighter=='kano' and 'sonya' or fighter=='sonya' and 'kano' or 'sub_zero'
local continue_at,reselect_at,reselect_exit,re_live,re_ready,plan=nil,nil,nil,nil,nil,nil
local portrait_refs=nil
local adjacency={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
local function route_from(start)
 local queue={{start,{}}};local seen={[start]=true};local at=1
 while queue[at] do
  local current=queue[at];at=at+1
  if current[1]==ids[target] then return current[2] end
  for _,button in ipairs({'Left','Right','Down'}) do
   local next_id=p:read_u16(adjacency[button]+current[1]*16)
   if next_id<=18 and not seen[next_id] then
    local steps={};for _,s in ipairs(current[2]) do steps[#steps+1]=s end
    steps[#steps+1]=button;queue[#queue+1]={next_id,steps};seen[next_id]=true
   end
  end
 end
 error('No real native selection path from '..start..' to '..ids[target])
end
local function valid(a) return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 print(string.format('MK2_GROUND_%s frame=%d fighter=%s side=%d writes=0 assistance=none %s',tag,frame,fighter,side,value or ''))
end
local function pulse(n,button,age,first,hold)
 if age>=first and age<first+(hold or 4) then
  fields[n][button]:set_value(1)
  log('INPUT',string.format('slot=%d button=%s age=%d',n,button:gsub(' ','_'),age))
 end
end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a) or not valid(m) then return nil end
 return {actor=a,main=m,id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),state=p:read_u16(s.state),
  hp=p:read_u16(s.hp),owner=p:read_u32(m+0xc0),pose=p:read_u32(a+0x1d0),cache=p:read_u32(a+0x1a0),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
  vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),
  action=p:read_u16(m+0x1f0),body=p:read_u16(a+0x160),flags=p:read_u16(m+0x210),
  bank=p:read_u16(a+0x140),facing=p:read_u16(a+0xf0)}
end
local function live_pair(a,b)
 return p:read_u16(0x010601d0)==2 and a and b and a.id==ids[names[1]] and b.id==ids[names[2]]
  and a.roster==a.id and b.roster==b.id and a.state==1 and b.state==1 and a.owner==a.actor and b.owner==b.actor
end
local function clean(a)
 return a.hp==161 and a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0
end
local function capture_age(age)
 local absolute=ready+age
 if reselect_at then
  if not reselect_exit then
   local a=absolute-reselect_at
   return absolute%2==0 and (a==8 or a>=122 and a<=138 or a>=146 and a<=162 or a>=170 and a<=184 or a==200 or a==224 or a==248 or a==272 or a==296 or a>=328)
  elseif not re_live then
   local a=absolute-reselect_exit
   return absolute%2==0 and (a<=100 or a%12<2)
  else
   return absolute%2==0 and (absolute-re_live<=12 or absolute%8==0)
  end
 end
 local local_age=phase_ready and absolute-phase_ready or age
 return age%8==0 and (local_age%300>=208 and local_age%300<=280 or local_age>=1400 and local_age<=2700)
end
local function part(n,a)
 local data={string.format('slot=%d age=%d mode=%d winner=%d stage=%d stageY=%d cameraX=%d suppression=%d input=%d',n,frame-ready,p:read_u16(0x010601d0),p:read_u16(0x01061b00),p:read_u16(0x01061b30),p:read_i16(0x0105ecd0),p:read_i16(0x0105d120),p:read_u16(0x010619d0),p:read_u16(0x01600000))}
 for _,key in ipairs({'actor','main','owner','pose','cache','vx','vy','gravity','body','flags','bank','facing'}) do data[#data+1]=string.format('%s=%08X',key,a[key]) end
 for _,key in ipairs({'id','roster','state','hp','x','y','floor','action'}) do data[#data+1]=string.format('%s=%d',key,a[key]) end
 log('FIELD',table.concat(data,' '))
 if not valid(a.cache) then return end
 for i=0,11 do
  local at=a.cache+i*0x70;local source=p:read_u32(at)
  if source==0 then break end
  log('PART',string.format('slot=%d age=%d part=%d source=%08X width=%d height=%d xoff=%d yoff=%d',
   n,frame-ready,i,source,p:read_u16(at+0x20),p:read_u16(at+0x30),p:read_i16(at+0x50),p:read_i16(at+0x60)))
 end
end
local mapping = {{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'ground actual DMA observation',function(at,data,mask)
 local bank=((regs[15] or 0)>>5)&1;local reg=mapping[bank+1][(at-0x01a80000)//16]
 regs[reg]=((regs[reg] or 0)&(~mask))|(data&mask)
 if reg~=1 or (data&0x8000)==0 or not ready then return end
 local age=frame-ready
 if not capture_age(age+2) and not capture_age(age) then return end
 local source=(regs[2] or 0)|((regs[3] or 0)<<16)
 local command=regs[1];local color=(regs[9] or 0)&255;local pal=(regs[8] or 0)&0x7f00
 local w,h=(regs[6] or 0)&0x3ff,(regs[7] or 0)&0x3ff
 if not ((command&15)==8 and color==15 or (command&15)==2 and (pal==0x200 or pal==0x300)) then return end
 log('DMA',string.format('age=%d source=%08X command=%04X palette=%04X color=%d x=%d y=%d width=%d height=%d scaleX=%d scaleY=%d left=%d right=%d top=%d bottom=%d skip=%d pc=%08X',
  age,source,command,pal,color,(regs[4] or 0)&0x3ff,(regs[5] or 0)&0x1ff,w,h,regs[10] or 0,regs[11] or 0,
  regs[12] or 0,regs[13] or 0,regs[16] or 0,regs[17] or 0,regs[0] or 0,cpu.PC.value))
 if command&15==2 and source>=0x10000000 and source<0x1a000000 then
  for n=1,2 do
   local a=sample(n)
   if a and valid(a.cache) then
    local sources={}
    for part=0,11 do
     local at=a.cache+part*0x70;local value=p:read_u32(at)
     if value==0 then break end
     sources[#sources+1]=string.format('%08X',value)
    end
    log('DMA_CACHE',string.format('age=%d slot=%d source=%08X actor=%08X main=%08X owner=%08X id=%d cache=%08X sources=%s y=%d floor=%d stageY=%d a8=%08X a13=%08X',
     age,n,source,a.actor,a.main,a.owner,a.id,a.cache,table.concat(sources,','),a.y,a.floor,p:read_i16(0x0105ecd0),cpu.A8.value,cpu.A13.value)..string.format(' cameraXY=%08X worldXY=%08X world2=%08X',p:read_u32(0x0105d050),p:read_u32(0x0105d120),p:read_u32(0x0105d140)))
   end
  end
 end
 local key=string.format('%08X_%04X_%d_%d',source,command,w,h)
 if emitted[key] or w==0 or h==0 then return end
 emitted[key]=true
 local offset=source
 if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000
 end -- MKII initializes the large graphics region; no stock bank wrap.
 if offset>=0xf8000000 then offset=offset-0xf8000000 end
 local first=offset//8
 local bytes=math.ceil((offset%8+w*h*((command>>12)&7)+(command&0x80~=0 and h*8 or 0))/8)+8
 local dump={}
 for i=first,first+bytes-1 do dump[#dump+1]=string.format('%02X',gfx:read_u8(i)) end
 log('GFX',string.format('key=%s offset=%d first=%d bytes=%d data=%s',key,offset,first,bytes,table.concat(dump)))
end)
for n,slot in ipairs(slots) do
 taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'native KO health ledger '..n,function(at,data,mask)
  if not ready or mask~=0xffff then return end
  log('HEALTH',string.format('slot=%d age=%d before=%d after=%d pc=%08X',n,frame-ready,p:read_u16(at),data&0xffff,cpu.PC.value))
 end)
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for _,range in ipairs({{0xfffe1800,0xfffe2400},{0xffff0800,0xffff3880}}) do
   local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at)) end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
 for n=1,2 do for _,field in pairs(fields[n]) do field:clear_value() end end
 if frame>=300 and frame<304 then fields[1]['High Punch']:set_value(1) end
 local pixels,width=screen:pixels();assert(width==400 and #pixels>=400*254*4)
 local yellow,early=0,0
 for y=0,24,2 do for x=40,360,2 do
  local c=string.unpack('<I4',pixels,(y*width+x)*4+1);local r,g,b=(c>>16)&255,(c>>8)&255,c&255
  if r>175 and g>140 and b<100 then yellow=yellow+1;if y==4 then early=early+1 end end
 end end
 if not css and frame>=boot then local age=(frame-boot)%300;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(1,'Start',age,20) end
 if not css and frame>700 and yellow>=400 and yellow<=430 and early>=10 then css=frame;log('CSS','yellow='..yellow..' early='..early) end
 if css and not live then
  local age=frame-css;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(2,'Start',age,20)
  for n=1,2 do
   for i,direction in ipairs(routes[n][names[n]]) do pulse(n,direction,age,n==1 and (12+(i-1)*12) or (132+(i-1)*16)) end
   pulse(n,'High Punch',age,n==1 and 96 or 220,8)
  end
 end
 local a,b=sample(1),sample(2)
 if not live and frame>1200 and live_pair(a,b) then live=frame;log('LIVE') end
 if live and not ready and frame%30==0 and a and b then
  log('WAIT',string.format('mode=%d aID=%d bID=%d aHP=%d bHP=%d aY=%d bY=%d aFloor=%d bFloor=%d aVX=%08X bVX=%08X aVY=%08X bVY=%08X aGravity=%08X bGravity=%08X aAction=%d bAction=%d aFlags=%04X bFlags=%04X',p:read_u16(0x010601d0),a.id,b.id,a.hp,b.hp,a.y,b.y,a.floor,b.floor,a.vx,b.vx,a.vy,b.vy,a.gravity,b.gravity,a.action,b.action,a.flags,b.flags))
 end
 if live and not ready and frame>=live+180 and live_pair(a,b) and clean(a) and clean(b) then
  ready=frame;phase_ready=frame;log('READY');log('ROUND_READY','round=1')
  for _,bank in ipairs({0,0x200,0x300}) do
   local colors={};for pen=0,63 do colors[#colors+1]=string.format('%06X',palette:pen_color(bank+pen)&0xffffff) end
   log('PALETTE',string.format('bank=%04X colors=%s',bank,table.concat(colors,',')))
  end
 end
 if ready then
  local age=frame-ready
  local mode=p:read_u16(0x010601d0)
  if mode~=last_mode then
   log('MODE',string.format('age=%d mode=%d round=%d winner=%d states=%d,%d roster=%d,%d actors=%08X,%08X',age,mode,phase,p:read_u16(0x01061b00),p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor)))
   last_mode=mode
  end
  if phase_ready and not (phase==1 and ko or phase==2 and second_ko) then
   local input_age=frame-phase_ready
   for cycle=0,4 do
    pulse(1,'Right',input_age,32+cycle*300,36);pulse(2,'Left',input_age,32+cycle*300,36)
    pulse(3-side,'Down',input_age,208+cycle*300,40);pulse(3-side,'High Punch',input_age,216+cycle*300,12)
   end
  end
  if a and b then
   part(1,a);part(2,b)
   local v=side==1 and a or b
   if not ko and v.id==ids[fighter] and v.hp==0 then
    ko=frame;log('KO',string.format('age=%d mode=%d winner=%d',age,p:read_u16(0x010601d0),p:read_u16(0x01061b00)))
   end
   if ko and not next_round and frame>ko+90 and a.hp==161 and b.hp==161 then
    next_round=frame;log('ROUND_RESET',string.format('age=%d mode=%d aID=%d bID=%d',age,p:read_u16(0x010601d0),a.id,b.id))
   end
   if next_round and not next_ready and frame>=next_round+180 and live_pair(a,b) and clean(a) and clean(b) then
    next_ready=frame;phase=2;phase_ready=frame;log('NEXT_READY','age='..age);log('ROUND_READY','round=2')
   end
   if phase==2 and not second_ko and v.id==ids[fighter] and v.hp==0 then
    second_ko=frame;log('SECOND_KO',string.format('age=%d roundAge=%d mode=%d winner=%d',age,frame-phase_ready,mode,p:read_u16(0x01061b00)))
   end
  else log('INVALID','age='..age) end
  if second_ko and not continue_at and mode==3 and p:read_u16(slots[side].state)==2 then
   continue_at=frame;log('CONTINUE',string.format('age=%d target=%s roster=%d',age,target,p:read_u16(slots[side].roster)))
  end
  if continue_at and not reselect_at then
   local c=frame-continue_at
   pulse(side,'Coin',c,20,5);pulse(side,'Coin',c,270,5);pulse(side,'Start',c,310,5)
   if mode==4 and p:read_u16(slots[side].state)==3 and yellow>=400 and yellow<=430 and early>=10 then
    reselect_at=frame
    local initial=p:read_u16(slots[side].roster);plan=route_from(initial)
    log('RESELECT',string.format('age=%d target=%s initial=%d plan=%s',age,target,initial,table.concat(plan,',')))
   end
  end
  if reselect_at and not reselect_exit then
   local c=frame-reselect_at
   if c==8 then
    portrait_refs={}
    for _,left in ipairs({23,323}) do for y=28,88,4 do for x=left+4,left+48,4 do
     portrait_refs[#portrait_refs+1]={x,y,string.unpack('<I4',pixels,(y*width+x)*4+1)&0xffffff}
    end end end
   end
   -- The other real human must choose/confirm too; do not wait for timeout.
   for i,button in ipairs(routes[3-side].kitana) do pulse(3-side,button,c,12+(i-1)*12) end
   pulse(3-side,'High Punch',c,96,8)
   for i,button in ipairs(plan) do pulse(side,button,c,56+(i-1)*12) end
   local to_stock=target=='kano' and 'Right' or 'Left'
   local to_native=target=='kano' and 'Left' or 'Right'
   if target~='sub_zero' then
   for _,step in ipairs({{to_stock,140},{to_native,164},{to_stock,188},{to_native,212},{'Down',236},{'Up',260},{to_native,284}}) do
    pulse(side,step[1],c,step[2])
   end
   end
   pulse(side,'High Punch',c,332,8)
   log('SELECT',string.format('sceneAge=%d roster=%d mode=%d target=%s otherRoster=%d otherState=%d',c,p:read_u16(slots[side].roster),mode,target,p:read_u16(slots[3-side].roster),p:read_u16(slots[3-side].state)))
   if c>332 and not (yellow>=400 and yellow<=430 and early>=10) then
    reselect_exit=frame;log('RESELECT_EXIT',string.format('sceneAge=%d roster=%d target=%s',c,p:read_u16(slots[side].roster),target))
   end
  end
  if reselect_exit then
   local matches={0,0}
   for i,r in ipairs(portrait_refs or {}) do
    if string.unpack('<I4',pixels,(r[2]*width+r[1])*4+1)&0xffffff==r[3] then
     local index=i<=192 and 1 or 2;matches[index]=matches[index]+1
    end
   end
   log('OUTSIDE',string.format('sceneAge=%d mode=%d css=%d kano_matches=%d sonya_matches=%d refs=%d',frame-reselect_exit,mode,(yellow>=400 and yellow<=430 and early>=10) and 1 or 0,matches[1],matches[2],portrait_refs and #portrait_refs/2 or 0))
  end
  if reselect_exit and not re_live then
   local own=side==1 and a or b
   if mode==2 and own and own.id==ids[target] and own.roster==own.id and own.owner==own.actor and own.state==1 then
    re_live=frame;log('RE_LIVE',string.format('target=%s id=%d stage=%d otherState=%d',target,own.id,p:read_u16(0x01061b30),p:read_u16(slots[3-side].state)))
   end
  end
  if re_live then
   local own=side==1 and a or b
   if not re_ready and frame>=re_live+180 and own and clean(own) then
    re_ready=frame;log('RE_READY',string.format('target=%s id=%d floor=%d',target,own.id,own.floor))
    for _,bank in ipairs({0,0x200,0x300}) do
     local colors={};for pen=0,63 do colors[#colors+1]=string.format('%06X',palette:pen_color(bank+pen)&0xffffff) end
     log('RE_PALETTE',string.format('bank=%04X colors=%s',bank,table.concat(colors,',')))
    end
   end
   if re_ready then
    local c=frame-re_ready
    pulse(side,side==1 and 'Right' or 'Left',c,24,20);pulse(side,'Up',c,64,8)
   end
  end
  if capture_age(age) then
   local file=string.format('ground_%04d.png',frame);screen:snapshot(file)
   local scene=re_live and 'continued_fight' or reselect_exit and 'transition' or reselect_at and 'reselect' or continue_at and 'continue' or 'ground'
   local origin=re_live or reselect_exit or reselect_at or continue_at or ready
   log('SNAP',string.format('age=%d scene=%s sceneAge=%d file=%s roster=%d target=%s',age,scene,frame-origin,file,p:read_u16(slots[side].roster),target))
  end
  if re_ready and frame>=re_ready+140 or age>=7000 then manager.machine:exit() end
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('css=%d live=%d ready=%d terminalAge=%d ko=%d reset=%d nextReady=%d secondKO=%d continue=%d reselect=%d reselectExit=%d reLive=%d reReady=%d target=%s scope=real_two_round_loss_paid_continue_cross_reselect_and_control_not_full_campaign',css or -1,live or -1,ready or -1,ready and frame-ready or -1,ko or -1,next_round or -1,next_ready or -1,second_ko or -1,continue_at or -1,reselect_at or -1,reselect_exit or -1,re_live or -1,re_ready or -1,target))
 for _,tap in ipairs(taps) do tap:remove() end
end)




