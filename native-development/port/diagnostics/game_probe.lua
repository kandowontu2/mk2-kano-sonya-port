-- Actual roster selection through physical inputs. Guest RAM is read-only.
local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local screen=m.screens[':screen']
local hi=m.ioport.ports[':IN0'].fields
local sys
for _,port in pairs(m.ioport.ports) do
 if port.fields['Coin 1'] then sys=port.fields; break end
end
assert(sys)
local n,selection,locked=0,0,false
local log=assert(io.open('probe.csv','w'))
local debuglog=assert(io.open('state.txt','w'))
for name,_ in pairs(sys) do debuglog:write(name,'\n') end
debuglog:flush()
local captured=false
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
log:write('frame,pc,mode,p1char,p2char,p1hp,p2hp,p1objectchar,p2objectchar,p1x,p2x,missing\n')
local function u32(a)
 local v=0
 for i=0,3 do v=v|(p:read_u8(a+i*8)<<(i*8)) end
 return v
end
emu.register_frame_done(function()
 n=n+1
 for _,name in ipairs({'P1 High Punch','P2 High Punch','P1 Left','P2 Right','P1 Right','P2 Left','P1 Down','P2 Down'}) do hi[name]:set_value(0) end
 for _,name in ipairs({'Coin 1','Coin 2','1 Player Start','2 Players Start','2 Player Start'}) do
  if sys[name] then sys[name]:set_value(0) end
 end
 local mode=p:read_u16(0x010601d0)
 local c1,c2=p:read_u16(0x01060280),p:read_u16(0x01060e50)
 if n>3000 and selection==0 then
  sys['Coin 1']:set_value(n%600<6 and 1 or 0)
  if sys['Coin 2'] then sys['Coin 2']:set_value(n%600<6 and 1 or 0) end
  sys['1 Player Start']:set_value(n%600>=60 and n%600<66 and 1 or 0)
  -- Acknowledge CMOS diagnostics before gameplay starts.
  hi['P1 High Punch']:set_value(n%40<4 and 1 or 0)
 end
 if mode==4 and not locked then
  selection=selection+1
  local start2=sys['2 Players Start'] or sys['2 Player Start']
  if selection<160 and start2 then start2:set_value(selection%30<5 and 1 or 0) end
  if selection<120 then
   sys['Coin 1']:set_value(selection%30<5 and 1 or 0)
  end
  if selection>50 then
   if c1==1 then hi['P1 Left']:set_value(selection%30<5 and 1 or 0) end
   if c2==9 then hi['P2 Right']:set_value(selection%30<5 and 1 or 0) end
  end
  if selection>160 and c1==17 and c2==18 then
   hi['P1 High Punch']:set_value(1); hi['P2 High Punch']:set_value(1)
   locked=true
  end
 end
 if mode==2 and locked then
  local a,b=u32(0x01060220),u32(0x01060df0)
  if a~=0 and b~=0 and math.abs(p:read_u16(a+0x90)-p:read_u16(b+0x90))>40 then
   hi['P1 Right']:set_value(1); hi['P2 Left']:set_value(1)
  end
  hi['P1 High Punch']:set_value(n%40<4 and 1 or 0)
  hi['P2 High Punch']:set_value(n%53<4 and 1 or 0)
 end
 if n%10==0 then
  local a,b=u32(0x01060220),u32(0x01060df0)
  log:write(string.format('%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',n,m.devices[':maincpu'].state['PC'].value,mode,c1,c2,p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(a+0x1f0),p:read_u16(b+0x1f0),p:read_u16(a+0x90),p:read_u16(b+0x90),u32(missing))); log:flush()
 end
 if not captured and m.devices[':maincpu'].state['PC'].value==recovery then
  captured=true
  for name,reg in pairs(m.devices[':maincpu'].state) do debuglog:write(name,'=',string.format('%08x',reg.value),'\n') end
  local sp=m.devices[':maincpu'].state['SP'].value
  for i=0,31 do debuglog:write(string.format('stack %08x=%08x\n',sp+i*32,p:read_u32(sp+i*32))) end
  debuglog:flush()
 end
 if n>=3000 and n%120==0 then screen:snapshot(string.format('frame_%05d.png',n)) end
 if n>=9000 then log:close(); debuglog:close(); m:exit() end
end)
