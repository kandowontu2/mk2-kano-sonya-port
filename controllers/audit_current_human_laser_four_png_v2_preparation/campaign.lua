-- Physically earn two human rounds, then LP,Block,Block,HK at150 pixels.
-- Passive taps/reads only. No health/state/ID/AI/RNG/register assistance.
local side=1
local other=3-side
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local high,low,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN2'].fields,manager.machine.ioport.ports[':IN1'].fields
local buttons={{},{}}
for n=1,2 do
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[n][key]=high['P'..n..' '..key]end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=low['P'..n..' '..key]end
 buttons[n].Coin=system['Coin '..n];buttons[n].Start=system[n==1 and'1 Player Start'or'2 Players Start']
end
local frame,started,completed,live,finish,approach,join,last_mode=0,nil,nil,nil,nil,nil,nil,nil
local css,plans,taps={},{},{}
local captures,pending={},{}
local continue_frame,next_css=nil,nil
local bones,particles,emitters=0,0,0
local function address(at)return 0xff800000+at*8 end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)print(string.format('MK2_LASER_%s frame=%d side=%d age=%d writes=0 assistance=none %s',tag,frame,side,started and frame-started or-1,text or''))end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,id=p:read_u16(a+0x1f0),roster=p:read_u16(s.id),state=p:read_u16(s.state),hp=p:read_u16(s.hp),
  owner=p:read_u32(m+0xc0),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
  pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140),body=p:read_u16(a+0x160)}
end
local function input(n,key)buttons[n][key]:set_value(1);log('INPUT','slot='..n..' key='..key:gsub(' ','_'))end
local function route(first,target)
 local queue={{first,{}}};local seen={[first]=true};local at=1
 while queue[at]do local row=queue[at];at=at+1;if row[1]==target then return row[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local base=key=='Left'and 0xffff1400 or key=='Right'and 0xffff1600 or 0xffff1200
   local next_id=p:read_u16(base+row[1]*16)
   if next_id<=18 and not seen[next_id]then local path={table.unpack(row[2])};path[#path+1]=key;queue[#queue+1]={next_id,path};seen[next_id]=true end
  end
 end
 error('No native selector route')
end
local function tap(at,name,fn)
 taps[#taps+1]=p:install_read_tap(at,at+15,name,function(where)if where==at and cpu.PC.value==at+16 then fn()end end)
end
tap(address(0xb0b00),'actual own Kano laser action',function()
 local own,victim=sample(side),sample(other)
 if own and victim and own.id==17 and victim.id==18 and victim.hp==0 and cpu.A8.value==own.actor and cpu.A13.value==own.main and not started then
  started=frame;log('ENTRY',string.format('actor=%08X main=%08X victim=%08X victim_main=%08X gap=%d hp=%d,%d',own.actor,own.main,victim.actor,victim.main,math.abs(own.x-victim.x),own.hp,victim.hp))
 end
end)
tap(address(0xb0900),'actual true victim contact',function()if started then log('CONTACT',string.format('actor=%08X main=%08X id=%d bank=%04X',cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A8.value+0x1f0),p:read_u16(cpu.A8.value+0x140)))end end)
for _,at in ipairs({0xff840450,0xff80e0e0,0xff83efd0,0xff83f930,0xff838f60})do
 local kernel=at
 tap(kernel,'actual native owned cleanup/park/hide',function()
  if started then log('CLEANUP',string.format('kernel=%08X job=%08X actor=%08X a0=%08X a7=%08X',kernel,cpu.A13.value,cpu.A8.value,cpu.A0.value,cpu.A7.value))end
 end)
end
tap(0xffa14860,'actual own native winner continuation',function()
 local own=sample(side)
 if started and own and cpu.A8.value==own.actor and cpu.A13.value==own.main and not completed then completed=frame;log('WINNER','main='..string.format('%08X',own.main))end
end)
tap(0xff877790,'actual native button history comparison',function()
 if finish and not started then log('HISTORY',string.format('wanted=%d actual=%d tick=%d cursor=%08X',cpu.A8.value>>16,cpu.A0.value>>16,cpu.A0.value&0xffff,cpu.A11.value))end
end)
for n=1,2 do local slot=n
 taps[#taps+1]=p:install_write_tap(slots[n].hp,slots[n].hp+15,'passive genuine health',function(at,data,mask)
  if at==slots[slot].hp and mask==0xffff and live then log('HEALTH',string.format('slot=%d before=%d after=%d pc=%08X',slot,p:read_u16(at),data&0xffff,cpu.PC.value))end
 end)
end
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'passive body copier overrun guard',function(at,data,mask)
 if cpu.PC.value==0xff838860 then log('OVERRUN',string.format('at=%08X data=%04X mask=%04X',at,data&0xffff,mask))end
end)
emu.register_frame(function()
 frame=frame+1;for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if frame>=8000 then log('BOUND','maximum_fields=8000');manager.machine:exit();return end
 if frame>=300 and frame<304 then input(1,'High Punch')end
 if frame>=600 and frame<604 then input(1,'Coin')end
 if frame>=608 and frame<612 then input(2,'Coin')end
 if frame>=620 and frame<624 then input(1,'Start')end
 if join then local age=frame-join;if age<4 then input(1,'Coin')elseif age>=8 and age<12 then input(2,'Coin')elseif age>=20 and age<24 then input(2,'Start')end end
 local mode=p:read_u16(0x010601d0)
 if started and completed and mode==3 then
  continue_frame=continue_frame or frame
  local age=frame-continue_frame
  if age>=20 and age<24 then input(2,'Coin')end
  if age>=50 and age<54 then input(2,'Coin')end
  if age>=80 and age<84 then input(2,'Start')end
 end
 if started and completed and mode==4 then next_css=next_css or frame end
 if mode~=last_mode then log('MODE','mode='..mode);last_mode=mode end
 for n=1,2 do
  if mode~=4 then css[n]=nil end
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css[n]then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].id),n==side and 17 or 18)
   if n==1 and not join then join=frame end
   log('SELECT','slot='..n..' target='..(n==side and 17 or 18)..' path='..table.concat(plans[n],','))
  end
  if css[n]and mode==4 then local age=frame-css[n]
   for i,key in ipairs(plans[n])do if age>=56+(i-1)*12 and age<60+(i-1)*12 then input(n,key)end end
   if age>=148 and age<156 then input(n,'High Punch')end
  end
 end
 local own,victim=sample(side),sample(other)
 if not own or not victim or own.id~=17 or victim.id~=18 or own.roster~=17 or victim.roster~=18 or own.owner~=own.actor or victim.owner~=victim.actor then return end
 local forward=own.x<victim.x and'Right'or'Left';local back=forward=='Right'and'Left'or'Right'
 local gap=math.abs(own.x-victim.x);local flag=p:read_u16(0x01061b00)
 if mode==2 and flag==0 and own.hp>0 and victim.hp>0 and own.state==1 and victim.state==1 then
  live=live or frame
  if frame-live>=180 then if gap>80 then input(side,forward)else input(side,'Down');if(frame-live)%42<4 then input(side,'High Punch')end end end
 elseif flag==3 and own.hp>0 and victim.hp==0 and not started then
  finish=finish or frame
  if frame-finish>=65 and not approach then
   if gap<146 then input(side,back)elseif gap>154 then input(side,forward)else approach=frame;log('COMMAND_READY','gap='..gap)end
  end
  if approach then local age=frame-approach
   for i,key in ipairs({'Low Punch','Block','Block','High Kick'})do local first=10+(i-1)*8;if age>=first and age<first+3 then input(side,key)end end
  end
 end
 if live and frame%60==0 then log('COMBAT',string.format('mode=%d flag=%d gap=%d hp=%d,%d ids=%d,%d',mode,flag,gap,own.hp,victim.hp,own.id,victim.id))end
end)

taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'independent fullword laser phases',function(at,data,mask)
 if at~=0x01d01030 or mask~=0xffff or data<0x6b40 or data>0x6b44 then return end
 local own,victim=sample(side),sample(other)
 log('PHASE_RAW',string.format('cue=%04X pc=%08X actor=%08X main=%08X',data,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 if not started or not own or not victim then return end
 assert(own.id==17 and own.roster==17 and own.state==1 and own.owner==own.actor and own.hp>0)
 assert(victim.id==18 and victim.roster==18 and victim.state==1 and victim.owner==victim.actor and victim.hp==0)
 if data==0x6b40 or data==0x6b41 then
  assert(cpu.A8.value==own.actor and cpu.A13.value==own.main)
 elseif data==0x6b42 then
  assert(cpu.A8.value==victim.actor and cpu.A13.value==victim.main)
 else
  assert(cpu.A8.value==victim.actor and cpu.A13.value==own.main)
 end
 local label=({[0x6b40]='charge',[0x6b41]='beam',[0x6b43]='burst'})[data]
 log('PHASE_OWNED',string.format('cue=%04X actor=%08X main=%08X victim=%08X victim_main=%08X',data,own.actor,own.main,victim.actor,victim.main))
 if label and not captures[label]then pending[frame+4]=label end
end)

emu.register_frame_done(function()
 if started then local age=frame-started
  if age<=1000 then
   for n=1,2 do local s=sample(n);if s then log('FIELD',string.format('slot=%d actor=%08X main=%08X id=%d roster=%d hp=%d x=%d y=%d floor=%d pose=%08X bank=%04X body=%04X child=%08X',n,s.actor,s.main,s.id,s.roster,s.hp,s.x,s.y,s.floor,s.pose,s.bank,s.body,p:read_u32(s.main+0x190)))end end
  end
  if next_css and frame-next_css==100 then pending[frame]='next_paid_selection' end
  local label=pending[frame]
  if label and not captures[label]then
   local count=0;for _ in pairs(captures)do count=count+1 end;assert(count<4)
   captures[label]=true;log('CAPTURE','label='..label..' mode='..p:read_u16(0x010601d0))
   screen:snapshot(assert(os.getenv('MK2KS_LASER_PNG_DIR'))..'/'..label..'.png')
  end
  if captures.next_paid_selection then log('STOP',string.format('started=%d completed=%d bones=%d particles=%d emitters=%d mode=%d',started,completed or-1,bones,particles,emitters,p:read_u16(0x010601d0)));manager.machine:exit()end
 elseif frame>=8000 then log('STOP','reason=finite_input_test_deadline');manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('started=%d completed=%d bones=%d particles=%d emitters=%d',started or-1,completed or-1,bones,particles,emitters))
 for _,t in ipairs(taps)do t:remove()end
end)
