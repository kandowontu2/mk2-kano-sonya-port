-- Physical command tests, no guest writes, cheats or saved-state injection.
local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local hi=m.ioport.ports[':IN0'].fields
local sys,lo
for _,port in pairs(m.ioport.ports) do
 if port.fields['Coin 1'] then sys=port.fields end
 if port.fields['P1 Low Kick'] then lo=port.fields end
end
assert(sys and lo)
local n,selection,combat,locked=0,0,0,false
local audioLog=assert(io.open('native_sound_writes.csv','w'))
audioLog:write('frame,address,data,mask,pc,seconds\n')
-- Passive stock-MAME tap: no integer return, therefore never changes a write.
local audioTap=p:install_write_tap(0x01680000,0x0168000f,'ks_native_sound_observer',function(address,data,mask)
 audioLog:write(string.format('%d,%08x,%08x,%08x,%08x,%.9f\n',n,address,data,mask,m.devices[':maincpu'].state['PC'].value,m.time:as_double()))
 audioLog:flush()
end)
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
local profile=os.getenv('KS_SPECIAL_PROFILE') or 'ball'
local mirror=os.getenv('KS_SPECIAL_MIRROR')=='1'
assert(profile=='ball' or profile=='square','Unknown special fixture profile')
local target1,target2=mirror and 18 or 17,mirror and 17 or 18
local log=assert(io.open('special.csv','w'))
log:write('frame,pc,mode,p1char,p2char,p1hp,p2hp,p1action,p2action,p1x,p2x,p1y,p2y,p1lk,missing,p2lk\n')
local function u32(a)
 local v=0
 for i=0,3 do v=v|(p:read_u8(a+i*8)<<(8*i)) end
 return v
end
emu.register_frame_done(function()
 n=n+1
 for _,name in ipairs({'P1 High Punch','P2 High Punch','P1 Left','P2 Right','P1 Right','P2 Left','P1 Up','P2 Up','P1 Down','P2 Down','P1 Block','P2 Block'}) do hi[name]:set_value(0) end
 lo['P1 Low Kick']:set_value(0)
 lo['P2 Low Kick']:set_value(0)
 for _,name in ipairs({'Coin 1','Coin 2','1 Player Start','2 Players Start'}) do sys[name]:set_value(0) end
 local mode=p:read_u16(0x010601d0)
 local c1,c2=p:read_u16(0x01060280),p:read_u16(0x01060e50)
 if n>3000 and selection==0 then
  sys['Coin 1']:set_value(n%600<6 and 1 or 0)
  sys['Coin 2']:set_value(n%600<6 and 1 or 0)
  sys['1 Player Start']:set_value(n%600>=60 and n%600<66 and 1 or 0)
  hi['P1 High Punch']:set_value(n%40<4 and 1 or 0)
 end
 if mode==4 and not locked then
  selection=selection+1
  if selection<160 then sys['2 Players Start']:set_value(selection%30<5 and 1 or 0) end
  if selection<120 then sys['Coin 1']:set_value(selection%30<5 and 1 or 0) end
  if selection>50 then
   if mirror then
    if c1~=target1 then hi['P1 Right']:set_value(selection%30<5 and 1 or 0) end
    if c2~=target2 then hi['P2 Left']:set_value(selection%30<5 and 1 or 0) end
   else
    if c1==1 then hi['P1 Left']:set_value(selection%30<5 and 1 or 0) end
    if c2==9 then hi['P2 Right']:set_value(selection%30<5 and 1 or 0) end
   end
  end
  if selection>(mirror and 200 or 160) and c1==target1 and c2==target2 then
   hi['P1 High Punch']:set_value(1); hi['P2 High Punch']:set_value(1); locked=true
  end
 end
 local a,b=u32(0x01060220),u32(0x01060df0)
 local pa,pb=u32(0x01060260),u32(0x01060e30)
 local held=0
 if mode==2 and locked and c1==target1 and c2==target2 then
  combat=combat+1
  local t=combat%(profile=='ball' and 500 or 400)
  -- First release is deliberately too short; next two exceed 0x50 fields.
  if profile=='ball' then
   held=((t>=10 and t<50) or (t>=130 and t<240) or (t>=330 and t<440)) and 1 or 0
   lo[(mirror and 'P2' or 'P1')..' Low Kick']:set_value(held)
   if combat>=1000 and combat<1500 then hi[(mirror and 'P1' or 'P2')..' Block']:set_value(1) end
  else
   -- Opposite player roles/facing, same timing and grounded-negative case.
   local owner,victim=mirror and 'P1' or 'P2',mirror and 'P2' or 'P1'
   local forward,backward=mirror and 'Right' or 'Left',mirror and 'Left' or 'Right'
   hi[victim..' Up']:set_value((t>=130 and t<134) and 1 or 0)
   hi[owner..' '..forward]:set_value(((t>=10 and t<13) or (t>=136 and t<139)) and 1 or 0)
   hi[owner..' '..backward]:set_value(((t>=16 and t<19) or (t>=142 and t<145)) and 1 or 0)
   hi[owner..' High Punch']:set_value(((t>=22 and t<25) or (t>=146 and t<150)) and 1 or 0)
  end
  if t==48 or t==54 or t==238 or t==244 or t==252 or t==268 or t==300 or (profile=='square' and (t==145 or t==154 or t==162 or t==178 or t==210)) then
   m.screens[':screen']:snapshot(string.format('special_%05d.png',n))
  end
 end
 if mode==2 or n%10==0 then
  log:write(string.format('%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',n,m.devices[':maincpu'].state['PC'].value,mode,c1,c2,p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(pa+0x1f0),p:read_u16(pb+0x1f0),p:read_u16(a+0x90),p:read_u16(b+0x90),p:read_u16(a+0xb0),p:read_u16(b+0xb0),mirror and 0 or held,u32(missing),mirror and held or 0))
  log:flush()
 end
 if m.devices[':maincpu'].state['PC'].value==recovery or n>=9000 then log:close();audioLog:close();audioTap:remove();m:exit() end
end)
