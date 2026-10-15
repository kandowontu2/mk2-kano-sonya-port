-- Cold real two-human selection, one human special and ordinary follow-up.
-- No guest writes or forced CPU/health/position/RNG. This is a diagnostic,
-- not complete native choreography/pixels/victim/CPU/finisher acceptance.
local move=assert(os.getenv('MK2KS_HUMAN_SPECIAL_MOVE'))
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local specs={knife={17,0xffffb000},ball={17,0xffffde00},blade={17,0xfff8cc00},choke={17,0xfff91400},
 ring={18,0xffffb400},square={18,0xffffca00},bicycle={18,0xfff9a400},leg={18,0xfff80800}}
local spec=assert(specs[move]);assert(side==1 or side==2)
for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX',
 'MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
 assert(not os.getenv(key),'Unassisted observer refuses '..key)
end
local p=manager.machine.devices[':maincpu'].spaces.program
local regs=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local high,low,system=manager.machine.ioport.ports[':IN0'].fields,
 manager.machine.ioport.ports[':IN2'].fields,manager.machine.ioport.ports[':IN1'].fields
local fields={{},{}}
for n=1,2 do
 for _,button in ipairs({'High Punch','High Kick','Block','Left','Right','Up','Down'})do fields[n][button]=high['P'..n..' '..button]end
 for _,button in ipairs({'Low Punch','Low Kick'})do fields[n][button]=low['P'..n..' '..button]end
 fields[n].Coin=system['Coin '..n];fields[n].Start=system[n==1 and '1 Player Start' or '2 Players Start']
end
local expected=side==1 and {spec[1],8}or{8,spec[1]}
local routes={
 {[17]={'Left'},[18]={'Right','Right','Right','Right'},[8]={'Down'}},
 {[17]={'Left','Left','Left','Left'},[18]={'Right'},[8]={'Left','Left','Left','Down'}}}
local frame,css,live,ready,settle,command,entry,recovered,followup=0,nil,nil,nil,nil,nil,nil,nil,nil
local forward,backward,taps=nil,nil,{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_HSPECIAL_%s frame=%d move=%s side=%d writes=0 assistance=none %s',tag,frame,move,side,text or''))
end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),state=p:read_u16(s.state),hp=p:read_u16(s.hp),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),
  action=p:read_u16(m+0x1f0),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),body=p:read_u16(a+0x160),trail=p:read_u32(m+0x190),bank=p:read_u16(a+0x140)}
end
local function pair_live(a,b)
 return a and b and p:read_u16(0x010601d0)==2 and a.id==expected[1]and b.id==expected[2]
  and a.roster==a.id and b.roster==b.id and a.state==1 and b.state==1 and a.owner==a.actor and b.owner==b.actor
end
local function clean(a)
 return a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 and a.body&0x0c==0 and a.trail==0
end
local function part(n,a)
 local text={'slot='..n,'mode='..p:read_u16(0x010601d0)}
 for _,key in ipairs({'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank'})do text[#text+1]=string.format('%s=%08X',key,a[key])end
 for _,key in ipairs({'id','roster','state','hp','x','y','floor','action'})do text[#text+1]=key..'='..a[key]end
 log('FIELD',table.concat(text,' '))
end
local function input(n,button)
 fields[n][button]:set_value(1);log('INPUT','slot='..n..' button='..button:gsub(' ','_'))
end
local function pulse(n,button,age,start,hold)
 if age>=start and age<start+(hold or 4)then input(n,button)end
end
for _,address in ipairs({spec[2],0xff861350,0xff861500})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'human special actual entry',function(at)
  if not command or regs.PC.value~=address+16 then return end
  local own=sample(side)
  if not own or regs.A8.value~=own.actor or regs.A13.value~=own.main then return end
  if address==spec[2]then entry=entry or frame end
  log('EVENT',string.format('entry=%08X pc=%08X actor=%08X main=%08X a8=%08X a13=%08X id=%d action=%d',
   address,regs.PC.value,own.actor,own.main,regs.A8.value,regs.A13.value,own.id,own.action))
 end)
end
taps[#taps+1]=p:install_write_tap(0x010602f0,0x010602ff,'human special P1 real health',function(at,data,mask)
 if command then log('HEALTH',string.format('slot=1 before=%d after=%d mask=%04X pc=%08X',p:read_u16(0x010602f0),data&0xffff,mask,regs.PC.value))end
end)
taps[#taps+1]=p:install_write_tap(0x01060ec0,0x01060ecf,'human special P2 real health',function(at,data,mask)
 if command then log('HEALTH',string.format('slot=2 before=%d after=%d mask=%04X pc=%08X',p:read_u16(0x01060ec0),data&0xffff,mask,regs.PC.value))end
end)
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(fields[n])do field:clear_value()end end
 if frame>=300 and frame<304 then input(1,'High Punch')end
 if not css and frame>=604 then
  local age=(frame-604)%300;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(1,'Start',age,20)
 end
 if not css and frame>700 then
  local pixels,width=screen:pixels();assert(width==400)
  local yellow,early=0,0
  for y=0,24,2 do for x=40,360,2 do
   local c=string.unpack('<I4',pixels,(y*width+x)*4+1);local r,g,b=(c>>16)&255,(c>>8)&255,c&255
   if r>175 and g>140 and b<100 then yellow=yellow+1;if y==4 then early=early+1 end end
  end end
  if yellow>=400 and yellow<=430 and early>=10 then css=frame;log('CSS')end
 end
 if css and not live then
  local age=frame-css;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(2,'Start',age,20)
  for n=1,2 do
   for i,button in ipairs(routes[n][expected[n]])do pulse(n,button,age,n==1 and(12+(i-1)*12)or(132+(i-1)*16))end
   pulse(n,'High Punch',age,n==1 and 96 or 220,8)
  end
 end
 local a,b=sample(1),sample(2)
 if not live and frame>1200 and pair_live(a,b)then live=frame;log('LIVE')end
 if live and not ready and frame>=live+180 and pair_live(a,b)and clean(a)and clean(b)then ready=frame;log('READY')end
 if ready then
  if not pair_live(a,b)then log('FAILED','reason=lost_native_live_pair');manager.machine:exit();return end
  local own,victim=side==1 and a or b,side==1 and b or a
  part(1,a);part(2,b)
  if not command then
   local gap=math.abs(own.x-victim.x)
   local far=move=='knife'or move=='ring'
   if not far and gap>63 then input(side,own.x<victim.x and'Right'or'Left');settle=nil
   elseif clean(own)and clean(victim)then
    settle=settle or frame
    if frame-settle>=30 then
     command=frame;forward=own.x<victim.x and'Right'or'Left';backward=forward=='Right'and'Left'or'Right'
     log('COMMAND',string.format('gap=%d forward=%s expectedEntry=%08X',gap,forward,spec[2]));screen:snapshot('special_before.png')
    end
   else settle=nil end
  end
  if command then
   local age=frame-command
   if move=='knife'or move=='ring'or move=='blade'or move=='choke'then
    pulse(side,'Down',age,0,3)
    pulse(side,move=='knife'and backward or forward,age,5,3)
    pulse(side,(move=='knife'or move=='blade')and'High Punch'or'Low Punch',age,6,3)
   elseif move=='square'then
    pulse(side,forward,age,0,3);pulse(side,backward,age,5,3);pulse(side,'High Punch',age,6,3)
   elseif move=='ball'then pulse(side,'Low Kick',age,0,84)
   elseif move=='bicycle'then
    pulse(side,backward,age,0,3);pulse(side,backward,age,6,3);pulse(side,'Down',age,12,3);pulse(side,'High Kick',age,13,3)
   elseif move=='leg'then
    pulse(side,'Down',age,0,7);pulse(side,'Low Punch',age,3,4);pulse(side,'Block',age,3,4)
   end
   if entry and not recovered and frame>entry+12 and clean(own)and clean(victim)then
    recovered=frame;followup=frame+16;log('RECOVERED');screen:snapshot('special_recovered.png')
   end
   if followup then
    local f=frame-followup
    pulse(side,forward,f,0,8);pulse(side,'Up',f,40,3);pulse(side,'High Punch',f,112,3)
    if f==160 then log('FINAL');screen:snapshot('special_final.png');manager.machine:exit()end
   elseif age>=400 then log('FAILED','reason=no_activation_or_full_recovery');manager.machine:exit()end
  end
 end
 if frame>=3000 and not ready then log('FAILED','reason=no_actual_match_ready');manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('css=%d live=%d ready=%d command=%d entry=%d recovered=%d followup=%d fullPortAcceptance=false scope=human_special_diagnostic_pending',
  css or-1,live or-1,ready or-1,command or-1,entry or-1,recovered or-1,followup or-1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
