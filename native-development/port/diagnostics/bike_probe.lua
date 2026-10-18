-- Native Bicycle Kick physical commands, paired motion and recovery observations.
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
local audioLog=assert(io.open('native_sound_writes.csv','w'))
audioLog:write('frame,address,data,mask,pc,seconds\n')
local audioTap=p:install_write_tap(0x01680000,0x0168000f,'ks_native_bike_sound_observer',function(address,data,mask)
 audioLog:write(string.format('%d,%08x,%08x,%08x,%08x,%.9f\n',n,address,data,mask,m.devices[':maincpu'].state['PC'].value,m.time:as_double()))
 audioLog:flush()
end)
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
local active=assert(tonumber(os.getenv('KS_ACTIVE_LIST')))
local mirror=os.getenv('KS_PROJECTILE_MIRROR')=='1'
local finalFrame=os.getenv('KS_BIKE_AUDIO_TAIL')=='1' and 9180 or 9000
local kano=mirror and 2 or 1
local sonya=mirror and 1 or 2
local log=assert(io.open('bike.csv','w'))
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
 if n<=9000 and mode==2 and locked and c1==(mirror and 18 or 17) and c2==(mirror and 17 or 18) then
  combat=combat+1
  local t=combat%400
  local a,b=u32(0x01060220),u32(0x01060df0)
  local ka,so=mirror and b or a,mirror and a or b
  local kx,sx=p:read_u16(ka+0x90),p:read_u16(so+0x90)
  local forward=sx>kx and ' Left' or ' Right'
  local backward=sx>kx and ' Right' or ' Left'
  local dist=math.abs(kx-sx)
  if combat>=400 and t<60 then
   if combat>=1600 and combat<2000 then
    hi['P'..sonya..backward]:set_value(1)
   elseif dist>90 then
    hi['P'..sonya..forward]:set_value(1)
   end
  end
  if (combat>=400 and t>=80 and t<83) or (t>=90 and t<93) then hi['P'..sonya..backward]:set_value(1) end
  hi['P'..sonya..' Down']:set_value(t>=100 and t<103 and 1 or 0)
  hi['P'..sonya..' High Kick']:set_value(t>=106 and t<110 and 1 or 0)
  if combat>=800 and combat<1200 and t>=70 and t<260 then hi['P'..kano..' Block']:set_value(1) end
  if combat>=1200 and combat<1600 and t>=60 and t<260 then hi['P'..kano..' Down']:set_value(1) end
  if combat<2000 and t>=100 and t<=300 and t%8==0 then m.screens[':screen']:snapshot(string.format('bike_%05d.png',n)) end
 end
 if mode==2 or n%10==0 then
  local a,b=u32(0x01060220),u32(0x01060df0)
  local pa,pb=u32(0x01060260),u32(0x01060e30)
  log:write(string.format('%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%08x,%08x,%08x,%08x,%d\n',n,m.devices[':maincpu'].state['PC'].value,mode,c1,c2,p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(pa+0x1f0),p:read_u16(pb+0x1f0),p:read_u16(a+0x90),p:read_u16(b+0x90),p:read_u16(a+0xb0),p:read_u16(b+0xb0),u32(a+0x40),u32(b+0x40),u32(a+0x60),u32(b+0x60),u32(a+0x1d0),u32(b+0x1d0),u32(missing)));log:flush()
 end
 if m.devices[':maincpu'].state['PC'].value==recovery or n>=finalFrame then log:close();audioLog:close();audioTap:remove();m:exit() end
end)
