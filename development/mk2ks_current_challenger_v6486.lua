-- Real single-player start, 600-field CPU game, challenger join, both native
-- highlights and ordinary play. No guest/HP/position/RNG/CPU state writes.
local fighter=assert(os.getenv('MK2PORT_CONTINUE_FIGHTER'))
local side=assert(tonumber(os.getenv('MK2PORT_CONTINUE_SIDE')))
assert((fighter=='kano' or fighter=='sonya') and (side==1 or side==2))
local identity=fighter=='kano' and 17 or 18
local identities={};identities[side]=identity;identities[3-side]=identity==17 and 18 or 17
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local gfx=manager.machine.memory.regions[':gfxrom']
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local high,low,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN2'].fields,manager.machine.ioport.ports[':IN1'].fields
local controls={{},{}}
for n=1,2 do
 for _,button in ipairs({'Up','Down','Left','Right','High Punch','Block'}) do controls[n][button]=high['P'..n..' '..button] end
 controls[n]['Low Punch']=low['P'..n..' Low Punch']
 controls[n].Coin=system['Coin '..n];controls[n].Start=system[n==1 and '1 Player Start' or '2 Players Start']
end
local frame,cold_css,cold_match,join,css,match,ready=0,nil,nil,nil,nil,nil,nil
local cold_route,routes=nil,{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)print(string.format('MK2_JR_%s frame=%d fighter=%s side=%d writes=0 assistance=none %s',tag,frame,fighter,side,value or ''))end
local function pulse(n,button,age,first,hold)
 if age>=first and age<first+(hold or 5) then controls[n][button]:set_value(1);log('INPUT',string.format('slot=%d button=%s value=1',n,button:gsub(' ','_'))) end
end
local function route(start,target)
 local adjacent={Up=0xffff1000,Down=0xffff1200,Left=0xffff1400,Right=0xffff1600}
 local queue={{start,{}}};local seen={[start]=true};local index=1
 while queue[index] do
  local row=queue[index];index=index+1
  if row[1]==target then return row[2] end
  for _,button in ipairs({'Left','Right','Up','Down'}) do
   local next_id=p:read_u16(adjacent[button]+row[1]*16)
   if next_id<=18 and not seen[next_id] then
    local steps={};for _,s in ipairs(row[2])do steps[#steps+1]=s end
    steps[#steps+1]=button;queue[#queue+1]={next_id,steps};seen[next_id]=true
   end
  end
 end
 error('No actual native selection route')
end
local function actor(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a) or not valid(m) then return nil end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.id),state=p:read_u16(s.state),
 hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
 vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),flags=p:read_u16(m+0x210),pose=p:read_u32(a+0x1d0)}
end
local function clean(a)return a and a.hp==161 and a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 end
local function css_visible()
 local pixels,width=screen:pixels();assert(width==400)
 local yellow=0
 for y=0,24,2 do for x=40,360,2 do
  local c=string.unpack('<I4',pixels,(y*width+x)*4+1)
  if (c>>16)&255>175 and (c>>8)&255>140 and c&255<100 then yellow=yellow+1 end
 end end
 return yellow>=400 and yellow<=430
end
local function hex(raw)return raw:gsub('.',function(c)return string.format('%02x',c:byte())end)end
local function rgb(label)
 local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_CR_RGB frame=%d filename=%s bytes=%d hex=%s',frame,label,#raw,hex(raw)))
end
local taps={}
for n,s in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(s.hp,s.hp+15,'current challenger native HP '..n,function(at,data,mask)
  if mask~=65535 then return end
  log('HEALTH',string.format('slot=%d before=%d after=%d pc=%08X',n,p:read_u16(at),data&65535,cpu.PC.value))
 end)
end
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(controls[n])do field:clear_value()end end
 if frame>=300 and frame<304 then controls[1]['High Punch']:set_value(1)end
 local mode=p:read_u16(0x010601d0)
 if not cold_css then
  local age=(frame-604)%300
  if frame>=604 then pulse(side,'Coin',age,0);pulse(side,'Coin',age,10);pulse(side,'Start',age,20)end
  if frame>700 and mode==4 and p:read_u16(slots[side].state)==3 and css_visible() then
   cold_css=frame;cold_route=route(p:read_u16(slots[side].id),identity)
   log('COLD_CSS','initial='..p:read_u16(slots[side].id)..' route='..table.concat(cold_route,','));rgb('cold_css')
  end
 elseif not cold_match then
  local age=frame-cold_css
  for i,button in ipairs(cold_route)do pulse(side,button,age,56+(i-1)*12)end
  pulse(side,'High Punch',age,176,8)
  local own=actor(side)
  if mode==2 and own and own.id==identity and own.roster==identity and own.owner==own.actor and own.state==1 and own.hp==161 and p:read_u16(slots[3-side].state)==0 then
   cold_match=frame;log('COLD_MATCH','id='..identity..' cpuID='..p:read_u16(slots[3-side].id));rgb('cold_match')
  end
 end
 if cold_match and not join then
  if frame-cold_match>=100 then controls[side].Block:set_value(1)end
  if frame-cold_match==600 then
   join=frame;log('JOIN','ownState='..p:read_u16(slots[side].state)..' otherState='..p:read_u16(slots[3-side].state)..' mode='..mode)
  end
 end
 if join and not css then
  local age=frame-join;pulse(3-side,'Coin',age,10);pulse(3-side,'Coin',age,30);pulse(3-side,'Start',age,60)
  if mode==4 and css_visible() and p:read_u16(slots[1].state)==3 and p:read_u16(slots[2].state)==3 then
   css=frame
   for n=1,2 do
    local initial=p:read_u16(slots[n].id);routes[n]=route(initial,identities[n])
    log('CSS',string.format('slot=%d initial=%d target=%d route=%s',n,initial,identities[n],table.concat(routes[n],',')))
   end
   rgb('joined_css')
  end
 end
 if css and not match then
  local age=frame-css
  for n=1,2 do
   for i,button in ipairs(routes[n])do pulse(n,button,age,56+(i-1)*12)end
   if age==156 then log('HIGHLIGHT',string.format('slot=%d expected=%d roster=%d state=%d',n,identities[n],p:read_u16(slots[n].id),p:read_u16(slots[n].state)))end
   pulse(n,'High Punch',age,176,8)
  end
  if age==156 then rgb('joined_highlight')end
  local a,b=actor(1),actor(2)
  if mode==2 and a and b and a.id==identities[1] and b.id==identities[2] and a.roster==a.id and b.roster==b.id and a.state==1 and b.state==1 and a.owner==a.actor and b.owner==b.actor and a.hp==161 and b.hp==161 then
   match=frame;log('MATCH');rgb('joined_match')
  end
 end
 if match then
  local a,b=actor(1),actor(2)
  if not ready and frame>=match+180 and clean(a) and clean(b) then ready=frame;log('READY');rgb('joined_ready')end
  if ready then
   local age=frame-ready
   for n=1,2 do
    pulse(n,n==1 and 'Right' or 'Left',age,24,20);pulse(n,'Up',age,64,8)
    pulse(n,'Down',age,140,16);pulse(n,'Block',age,180,16);pulse(n,'High Punch',age,220,8)
    pulse(n,n==1 and 'Left' or 'Right',age,312,16)
   end
   if age%30==0 then rgb('joined_play_'..age)end
   if age==600 then manager.machine:exit()end
  end
 end
 if frame==12000 then log('ERROR','reason=physical_route_deadline');manager.machine:exit()end
end)
emu.register_frame_done(function()
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  print('MK2_CR_GUEST frame=1 bytes=1048576 hex='..hex(raw))
  local bytes={};for i=0,11943 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa0000+i))end
  for i=0,7031 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa4000+i))end
  raw=table.concat(bytes);print('MK2_CR_GFX frame=1 bytes=18976 hex='..hex(raw))
 end
 for n=1,2 do
  local a=actor(n)
  if a then
   print(string.format('MK2_CR_FIELD frame=%d slot=%d mode=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d x=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X flags=%04X pose=%08X writes=0 assistance=none',frame,n,p:read_u16(0x010601d0),a.actor,a.main,a.owner,a.id,a.roster,a.state,a.hp,a.x,a.y,a.floor,a.vx,a.vy,a.gravity,a.flags,a.pose))
  end
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('coldCSS=%d coldMatch=%d join=%d css=%d match=%d ready=%d terminal=%d',cold_css or -1,cold_match or -1,join or -1,css or -1,match or -1,ready or -1,frame))
 for _,tap in ipairs(taps)do tap:remove()end
end)
