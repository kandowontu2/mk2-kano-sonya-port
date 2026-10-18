-- True roster, physical D,B+HP / D,F+LP commands, read-only observations.
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
local log=assert(io.open('projectiles.csv','w'))
log:write('frame,pc,mode,p1char,p2char,p1hp,p2hp,p1action,p2action,p1pal,p2pal,p1projectiles,p2projectiles,p1projectileID,p2projectileID,p1projectileShape,p2projectileShape,missing\n')
emu.register_frame_done(function()
 n=n+1
 for _,name in ipairs({'P1 High Punch','P2 High Punch','P1 Down','P2 Down','P1 Left','P1 Right','P2 Left','P2 Right','P1 Block','P2 Block'}) do hi[name]:set_value(0) end
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
   if mirror then
    if c1~=18 then hi['P1 Right']:set_value(selection%30<5 and 1 or 0) end
    if c2~=17 then hi['P2 Left']:set_value(selection%30<5 and 1 or 0) end
   else
    if c1==1 then hi['P1 Left']:set_value(selection%30<5 and 1 or 0) end
    if c2==9 then hi['P2 Right']:set_value(selection%30<5 and 1 or 0) end
   end
  end
  if selection>160 and c1==(mirror and 18 or 17) and c2==(mirror and 17 or 18) then
   hi['P1 High Punch']:set_value(1);hi['P2 High Punch']:set_value(1);locked=true
  end
 end
 if mode==2 and locked and c1==(mirror and 18 or 17) and c2==(mirror and 17 or 18) then
  combat=combat+1
  local t=combat%240
  local valid=combat>=240
  hi['P'..kano..' Down']:set_value(t>=10 and t<13 and 1 or 0)
  hi['P'..kano..((valid~=mirror) and ' Left' or ' Right')]:set_value(t>=16 and t<19 and 1 or 0)
  hi['P'..kano..' High Punch']:set_value(t>=22 and t<25 and 1 or 0)
  hi['P'..sonya..' Down']:set_value(t>=90 and t<93 and 1 or 0)
  hi['P'..sonya..((valid~=mirror) and ' Left' or ' Right')]:set_value(t>=96 and t<99 and 1 or 0)
  lo['P'..sonya..' Low Punch']:set_value(t>=102 and t<105 and 1 or 0)
  if combat>=720 and combat<960 then
   if t<80 then hi['P'..sonya..' Block']:set_value(1) end
   if t>=80 and t<200 then hi['P'..kano..' Block']:set_value(1) end
  end
  if combat>=240 and combat<960 and t>=20 and t<=180 and t%4==0 then m.screens[':screen']:snapshot(string.format('proj_%05d.png',n)) end
 end
 if mode==2 or n%10==0 then
  local a,b=u32(0x01060220),u32(0x01060df0)
  local pa,pb=u32(0x01060260),u32(0x01060e30)
  local counts,ids,shapes={0,0},{0,0},{0,0}
  local proc=u32(active)
  for i=1,168 do
   if proc==0 then break end
   local id=p:read_u16(proc+0x20)
   local who=id==0x700 and 1 or (id==0x800 and 2 or 0)
   if who>0 then
    local obj=u32(proc+0xc0)
    counts[who]=counts[who]+1;ids[who]=p:read_u16(obj+0x1f0);shapes[who]=u32(obj+0x1d0)
   end
   proc=u32(proc)
  end
  log:write(string.format('%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%d\n',n,m.devices[':maincpu'].state['PC'].value,mode,c1,c2,p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(pa+0x1f0),p:read_u16(pb+0x1f0),p:read_u16(a+0x140),p:read_u16(b+0x140),counts[1],counts[2],ids[1],ids[2],shapes[1],shapes[2],u32(missing)));log:flush()
 end
 if m.devices[':maincpu'].state['PC'].value==recovery or n>=9000 then log:close();m:exit() end
end)
