local identity=assert(tonumber(os.getenv('MK2KS_STANDING_ID')))
local side=assert(tonumber(os.getenv('MK2KS_STANDING_SIDE')))
assert((identity==17 or identity==18)and(side==1 or side==2))
local spec={identity};local move='standing';local air=false
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
local victim_name='kitana';local victim_id=4
local expected=side==1 and {identity,4}or{4,identity}
local frame,css,live,ready,settle,command,entry,recovered,followup=0,nil,nil,nil,nil,nil,nil,nil,nil
local forward,backward,taps=nil,nil,{}
local attempt,completed=0,0
local marks,origins,css_marks,plans={},{},{},{}
local join_at=nil
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_HSPECIAL_%s frame=%d move=%s side=%d attempt=%d air=%d victim=%s writes=0 assistance=none %s',tag,frame,move,side,attempt,air and 1 or 0,victim_name,text or''))
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
 return a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 and a.body&0x0c==0 and a.trail==0 and a.action==0x303
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
local function route(start,target)
 local pending={{start,{}}};local seen={[start]=true};local next_index=1
 for _=1,40 do
  local item=pending[next_index];if not item then break end;next_index=next_index+1
  if item[1]==target then return item[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local address=({Left=0xffff1400,Right=0xffff1600,Down=0xffff1200})[key]
   local id=p:read_u16(address+item[1]*16)
   if id<=18 and not seen[id]then
    local path={table.unpack(item[2])};path[#path+1]=key;pending[#pending+1]={id,path};seen[id]=true
   end
  end
 end
 error('No actual native CSS route')
end
local capture=nil;local projection={}
local tap=p:install_read_tap(0xff8042a0,0xff8042af,'standing actual projected body',function(at)
 if not capture or frame~=capture or at~=0xff8042a0 or regs.PC.value~=0xff8042b0 then return end
 for n=1,2 do local a=sample(n)
  if a and regs.A0.value==a.actor then projection[n]=(projection[n]or 0)+1
   log('PROJECTION',string.format('slot=%d actor=%08X pose=%08X source=%08X size=%08X xy=%08X display=%08X command=%08X pc=%08X',n,a.actor,a.pose,regs.A11.value,regs.A9.value,regs.A10.value,regs.A5.value,regs.A12.value,regs.PC.value))
  end
 end
end)
emu.register_frame_done(function()
 if capture~=frame then return end
 local a,b=sample(1),sample(2);assert(pair_live(a,b)and clean(a)and clean(b))
 assert(projection[1]and projection[2],'Missing same-frame native projection')
 part(1,a);part(2,b);log('CAPTURE','arena='..p:read_u16(0x01061ac0)..' width=400 height=254 cameraEvidence=native_display_and_xy')
 screen:snapshot(assert(os.getenv('MK2KS_STANDING_PNG')))
 log('COMPLETE','pngCount=1 rawBuffers=0');manager.machine:exit()
end)
emu.register_stop(function()tap:remove()end)
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(fields[n])do field:clear_value()end end
 if frame>=300 and frame<304 then input(1,'High Punch')end
 if frame>=600 and frame<604 then input(1,'Coin')end
 if frame>=608 and frame<612 then input(2,'Coin')end
 if frame>=620 and frame<624 then input(1,'Start')end
 if join_at then
  local age=frame-join_at;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(2,'Start',age,20)
 end
 local mode=p:read_u16(0x010601d0)
 for n=1,2 do
  if mode~=4 then css_marks[n]=nil end
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css_marks[n]then
   css_marks[n]=frame;css=css or frame;plans[n]=route(p:read_u16(slots[n].roster),expected[n])
   if n==1 and not join_at then join_at=frame;log('JOIN_BEGIN','slot=2')end
   log('SELECT','slot='..n..' target='..expected[n]..' path='..table.concat(plans[n],','))
  end
  if css_marks[n]and mode==4 then
   local age=frame-css_marks[n]
   for i,button in ipairs(plans[n])do pulse(n,button,age,56+(i-1)*12)end
   pulse(n,'High Punch',age,148,8)
  end
 end
 local a,b=sample(1),sample(2)
 if not live and frame>1200 and pair_live(a,b)then live=frame;log('LIVE')end
 if live and not ready and frame>=live+60 and pair_live(a,b)and clean(a)and clean(b)then ready=frame;log('READY')end

 if ready and not capture and clean(a)and clean(b)then settle=settle or frame;if frame-settle>=30 then capture=frame+1 end elseif not capture then settle=nil end
 if frame>6000 then log('FAILED','bounded_field_limit');manager.machine:exit()end
end)
