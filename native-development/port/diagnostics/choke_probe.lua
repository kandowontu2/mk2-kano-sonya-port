-- Native Choke physical commands, four damage pulses and paired release.
local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local hi=m.ioport.ports[':IN0'].fields
local sys,lo
for _,port in pairs(m.ioport.ports) do
 if port.fields['Coin 1'] then sys=port.fields end
 if port.fields['P2 Low Punch'] then lo=port.fields end
end
assert(sys and lo)
local function u32(a)
 local v=0
 for i=0,3 do v=v|(p:read_u8(a+i*8)<<(8*i)) end
 return v
end
local n,selection,combat,locked=0,0,0,false
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
local active=assert(tonumber(os.getenv('KS_ACTIVE_LIST')))
local mirror=os.getenv('KS_PROJECTILE_MIRROR')=='1'
local kano=mirror and 2 or 1
local sonya=mirror and 1 or 2
local victim=tonumber(os.getenv('KS_CHOKE_VICTIM')) or 18
local spacing=tonumber(os.getenv('KS_CHOKE_SPACING')) or 105
local fastCommand=os.getenv('KS_CHOKE_FAST_COMMAND')=='1'
local crouchEntry=os.getenv('KS_CHOKE_CROUCH_ENTRY')=='1'
assert(not crouchEntry or fastCommand)
assert(spacing>=40 and spacing<=105)
local navigate=os.getenv('KS_CHOKE_NAVIGATE')=='1'
local navigation={}
for _,direction in ipairs({'Up','Down','Left','Right'}) do
 local values={};local i=0
 for value in (os.getenv('KS_SELECT_'..direction:upper()) or ''):gmatch('[^,]+') do values[i]=assert(tonumber(value));i=i+1 end
 navigation[direction]=values
end
local function nextDirection(start,destination)
 if navigation.Up[start]==nil then return nil end -- player has not joined selection yet
 local queue={{start,nil}};local seen={[start]=true};local head=1
 while head<=#queue do
  local item=queue[head];head=head+1
  if item[1]==destination then return item[2] end
  for _,direction in ipairs({'Up','Down','Left','Right'}) do
   local neighbor=navigation[direction][item[1]]
   if neighbor and not seen[neighbor] then seen[neighbor]=true;queue[#queue+1]={neighbor,item[2] or direction} end
  end
 end
 error('No native selection route')
end
local target1=mirror and victim or 17
local target2=mirror and 17 or victim
local log=assert(io.open('choke.csv','w'))
log:write('frame,pc,mode,p1char,p2char,p1hp,p2hp,p1action,p2action,p1x,p2x,p1y,p2y,p1xvel,p2xvel,p1yvel,p2yvel,p1shape,p2shape,missing\n')
emu.register_frame_done(function()
 n=n+1
 for _,name in ipairs({'P1 High Punch','P2 High Punch','P1 High Kick','P2 High Kick','P1 Down','P2 Down','P1 Left','P1 Right','P2 Left','P2 Right','P1 Block','P2 Block'}) do hi[name]:set_value(0) end
 lo['P1 Low Punch']:set_value(0);lo['P2 Low Punch']:set_value(0)
 for _,name in ipairs({'Coin 1','Coin 2','1 Player Start','2 Players Start'}) do sys[name]:set_value(0) end
 local mode=p:read_u16(0x010601d0)
 local c1,c2=p:read_u16(0x01060280),p:read_u16(0x01060e50)
 if n>3000 and selection==0 then
  sys['Coin 1']:set_value(n%600<6 and 1 or 0);sys['Coin 2']:set_value(n%600<6 and 1 or 0)
  sys['1 Player Start']:set_value(n%600>=60 and n%600<66 and 1 or 0)
  hi['P1 High Punch']:set_value(n%40<4 and 1 or 0)
 end
 if mode==4 and not locked then
  selection=selection+1
  if selection<160 then sys['2 Players Start']:set_value(selection%30<5 and 1 or 0) end
  if selection<120 then sys['Coin 1']:set_value(selection%30<5 and 1 or 0) end
  if selection>50 then
   if navigate then
    for _,item in ipairs({{c1,target1,'P1 '},{c2,target2,'P2 '}}) do
     if item[1]~=item[2] then
      local direction=nextDirection(item[1],item[2])
      if direction then hi[item[3]..direction]:set_value(selection%30<5 and 1 or 0) end
     end
    end
   elseif mirror then
    if c1~=target1 then hi['P1 Right']:set_value(selection%30<5 and 1 or 0) end
    if c2~=17 then hi['P2 Left']:set_value(selection%30<5 and 1 or 0) end
   else
    if c1==1 then hi['P1 Left']:set_value(selection%30<5 and 1 or 0) end
    if victim==1 then
     if c2~=1 then hi['P2 Left']:set_value(selection%30<5 and 1 or 0) end
    elseif c2==9 then hi['P2 Right']:set_value(selection%30<5 and 1 or 0) end
   end
  end
  if selection>160 and c1==target1 and c2==target2 then
   hi['P1 High Punch']:set_value(1);hi['P2 High Punch']:set_value(1);locked=true
  end
 end
 if mode==2 and locked and c1==target1 and c2==target2 then
  combat=combat+1
  local t=combat%400
  local a,b=u32(0x01060220),u32(0x01060df0)
  local ka,so=mirror and b or a,mirror and a or b
  local kx,sx=p:read_u16(ka+0x90),p:read_u16(so+0x90)
  local forward=kx>sx and ' Left' or ' Right'
  local backward=kx>sx and ' Right' or ' Left'
  local dist=math.abs(kx-sx)
  if t<70 then
   if combat<400 or (combat>=1200 and combat<1600) then
    if dist<260 then hi['P'..kano..backward]:set_value(1) end
   elseif dist>spacing then hi['P'..kano..forward]:set_value(1) end
  end
  local downBegin=crouchEntry and 74 or 80
  hi['P'..kano..' Down']:set_value(t>=downBegin and t<83 and 1 or 0)
  local forwardBegin=fastCommand and 83 or 86
  local punchBegin=fastCommand and 86 or 92
  if t>=forwardBegin and t<forwardBegin+3 then hi['P'..kano..forward]:set_value(1) end
  lo['P'..kano..' Low Punch']:set_value(t>=punchBegin and t<punchBegin+4 and 1 or 0)
  if combat>=800 and combat<1200 and t>=70 and t<260 then hi['P'..sonya..' Block']:set_value(1) end
  if combat>=1600 and combat<2000 and t>=70 and t<260 then hi['P'..sonya..' Down']:set_value(1) end
  if combat<2000 and t>=88 and t<=248 and t%8==0 then m.screens[':screen']:snapshot(string.format('choke_%05d.png',n)) end
 end
 if mode==2 or n%10==0 then
  local a,b=u32(0x01060220),u32(0x01060df0)
  local pa,pb=u32(0x01060260),u32(0x01060e30)
  log:write(string.format('%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%08x,%08x,%08x,%08x,%d\n',n,m.devices[':maincpu'].state['PC'].value,mode,c1,c2,p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(pa+0x1f0),p:read_u16(pb+0x1f0),p:read_u16(a+0x90),p:read_u16(b+0x90),p:read_u16(a+0xb0),p:read_u16(b+0xb0),u32(a+0x40),u32(b+0x40),u32(a+0x60),u32(b+0x60),u32(a+0x1d0),u32(b+0x1d0),u32(missing)));log:flush()
 end
 if m.devices[':maincpu'].state['PC'].value==recovery or n>=9000 then log:close();m:exit() end
end)
